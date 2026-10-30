"""Checkout flow: trust decision -> PayPal authorize -> exit check -> capture verified lines.

Store prices are in INR, which the trust engine is calibrated for. PayPal's
currency list doesn't include INR, so sandbox amounts are converted to USD at a
fixed demo rate (`inr_per_usd`). That rate is a demo constant, not a quote.
"""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass

from proofpay.paypal import OrderItem, PayPalClient, PayPalError
from proofpay.store import Store
from proofpay.trust import (
    DEFAULT,
    Event,
    Line,
    TrustConfig,
    choose_policy,
    fit_cohort_prior,
    reputation,
)
from proofpay.trust.reputation import Reputation, raw_weight


class CheckoutError(RuntimeError):
    pass


@dataclass(frozen=True)
class BasketLine:
    line_id: str
    name: str
    sku: str
    price: float  # INR
    p: float
    evidence: dict | None = None


def days_now() -> float:
    return time.time() / 86400.0


class CheckoutService:
    def __init__(
        self,
        store: Store,
        paypal: PayPalClient,
        cfg: TrustConfig = DEFAULT,
        clock: Callable[[], float] = days_now,
        inr_per_usd: float = 85.0,
    ):
        self.store, self.paypal, self.cfg, self.clock, self.inr_per_usd = store, paypal, cfg, clock, inr_per_usd

    # --- trust ------------------------------------------------------------------

    def cohort_prior(self) -> tuple[float, float]:
        rates = []
        by_subject: dict[str, list[Event]] = {}
        for e in self.store.events():
            by_subject.setdefault(e.subject, []).append(e)
        for evs in by_subject.values():
            if len(evs) < 3:
                continue
            pos = sum(raw_weight(e, self.cfg)[0] for e in evs)
            neg = sum(raw_weight(e, self.cfg)[1] for e in evs)
            if pos + neg > 0:
                rates.append(pos / (pos + neg))
        return fit_cohort_prior(rates, self.cfg)

    def reputation(self, subject: str) -> Reputation:
        return reputation(subject, self.store.events(subject), self.clock(), self.cohort_prior(), self.cfg)

    def usd(self, inr: float) -> float:
        return round(inr / self.inr_per_usd, 2)

    def _paypal(self, session_id: str | None, op: str, request_id: str | None, fn, *args, **kw):
        try:
            out = fn(*args, **kw)
        except PayPalError as e:
            self.store.log_call(session_id, op, request_id, False, json.dumps(e.body, default=str), self.clock())
            raise
        detail = out.raw if hasattr(out, "raw") else out
        self.store.log_call(session_id, op, request_id, True, json.dumps(detail, default=str), self.clock())
        return out

    # --- 1. basket -> decision -> PayPal order ----------------------------------

    def start(self, customer_id: str, basket: list[BasketLine]) -> dict:
        if not basket:
            raise CheckoutError("empty basket")
        payer = self.store.payer_for(customer_id)
        subject = payer or f"customer:{customer_id}"
        rep = self.reputation(subject)
        lines = [Line(b.line_id, b.name, b.price, b.p) for b in basket]
        d = choose_policy(lines, rep, self.cfg)

        held = [b for b in basket if d.dispositions[b.line_id] != "release"]
        items = [OrderItem(b.name, b.sku, self.usd(b.price)) for b in held]
        buffer_inr = round(d.hold_amount - sum(b.price for b in held), 2)
        if buffer_inr > 0:
            # Strict: authorized up front so items found at the exit check can
            # be captured. Shown to the buyer as a refundable hold.
            items.append(OrderItem("Exit-check hold (released if unused)", "HOLD-BUFFER", self.usd(buffer_inr)))

        session_id = uuid.uuid4().hex[:12]
        order = (
            self._paypal(session_id, "create_order", f"{session_id}-create",
                         self.paypal.create_order, items, session_id, f"{session_id}-create")
            if items else None
        )
        self.store.insert_session(
            {
                "session_id": session_id,
                "customer_id": customer_id,
                "subject": subject,
                "status": "created" if order else "voided",
                "policy": d.policy,
                "decision": json.dumps({**d.explain(), "trust": rep.explain()}, default=str),
                "order_id": order["id"] if order else None,
                "created_t": self.clock(),
            },
            [
                {
                    "session_id": session_id, "line_id": b.line_id, "name": b.name, "sku": b.sku,
                    "price": b.price, "p": b.p, "evidence": json.dumps(b.evidence or {}),
                    "disposition": d.dispositions[b.line_id],
                }
                for b in basket
            ],
        )
        return self.view(session_id)

    # --- 2. buyer approved -> authorize -----------------------------------------

    def authorize(self, session_id: str) -> dict:
        s = self._session(session_id, "created")
        rid = f"{session_id}-authorize"
        auth = self._paypal(session_id, "authorize_order", rid, self.paypal.authorize_order, s["order_id"], rid)
        fields = {"status": "authorized", "authorization_id": auth.authorization_id, "authorized_amount": auth.amount}
        if auth.payer_id:
            self.store.link_payer(s["customer_id"], auth.payer_id)
            if s["subject"] != auth.payer_id:
                self.store.rename_subject(s["subject"], auth.payer_id)
                fields["subject"] = auth.payer_id
        self.store.update_session(session_id, **fields)
        return self.view(session_id)

    # --- 3. exit check -> capture verified, release the rest ---------------------

    def exit(self, session_id: str, staff_verdicts: dict[str, bool], found: list[BasketLine] = ()) -> dict:
        """Close the visit.

        staff_verdicts: line_id -> True if staff saw the item taken. Required for
        every line whose disposition is staff_check.
        found: untracked items staff found at the exit. Billed (a human verified
        them) and recorded as an exit mismatch.
        """
        s = self._session(session_id, "authorized")
        lines = self.store.lines(session_id)
        missing = [ln["line_id"] for ln in lines if ln["disposition"] == "staff_check" and ln["line_id"] not in staff_verdicts]
        if missing:
            raise CheckoutError(f"staff verdict needed for {missing}")

        billed, billed_p = [], []
        for ln in lines:
            if ln["disposition"] == "auto_capture":
                bill = True
            elif ln["disposition"] == "staff_check":
                bill = bool(staff_verdicts[ln["line_id"]])
                self.store.update_line(session_id, ln["line_id"], staff_verdict=int(bill))
            else:
                bill = False
            if bill:
                billed.append(ln)
                billed_p.append(ln["p"])
                self.store.update_line(session_id, ln["line_id"], billed=1)
        for f in found:
            self.store.add_line({
                "session_id": session_id, "line_id": f.line_id, "name": f.name, "sku": f.sku, "price": f.price,
                "p": 0.0, "evidence": json.dumps(f.evidence or {}), "disposition": "staff_check",
                "staff_verdict": 1, "billed": 1, "found_at_exit": 1,
            })
            billed.append({"price": f.price})

        total_usd = round(sum(self.usd(b["price"]) for b in billed), 2)
        authorized = float(s["authorized_amount"])
        if total_usd > authorized:
            # Can't capture beyond the hold; the excess is recorded, not charged.
            total_usd = authorized
        now = self.clock()
        if total_usd <= 0:
            rid = f"{session_id}-void"
            self._paypal(session_id, "void", rid, self.paypal.void_authorization, s["authorization_id"], rid)
            self.store.update_session(session_id, status="voided", captured_amount="0.00")
        else:
            rid = f"{session_id}-capture"
            cap = self._paypal(
                session_id, "capture", rid, self.paypal.capture_authorization,
                s["authorization_id"], total_usd, f"proofpay-{session_id}", rid, True,
                "Charged only for items verified at checkout.",
            )
            self.store.update_session(session_id, status="captured", capture_id=cap["id"],
                                      captured_amount=cap["amount"]["value"])
        if billed_p:
            self.store.add_event(Event(
                s["subject"], "capture_verified", now, tuple(billed_p),
                sum(ln["price"] for ln in billed if "line_id" in ln), {"session_id": session_id},
            ))
        if found:
            self.store.add_event(Event(s["subject"], "exit_mismatch", now, value=sum(f.price for f in found),
                                       meta={"session_id": session_id}))
        return self.view(session_id)

    # --- 4. "Not mine" ------------------------------------------------------------

    def not_mine(self, session_id: str, line_id: str, footage_shows_take: bool) -> dict:
        """Staff have reviewed the footage. Refund if it doesn't show the take."""
        s = self._session(session_id, "captured")
        ln = next((x for x in self.store.lines(session_id) if x["line_id"] == line_id), None)
        if not ln or not ln["billed"]:
            raise CheckoutError("line was not billed")
        if ln["refunded"]:
            return self.view(session_id)
        now = self.clock()
        if footage_shows_take:
            self.store.add_event(Event(s["subject"], "line_disputed_rejected", now, value=ln["price"],
                                       meta={"session_id": session_id, "line_id": line_id}))
            return self.view(session_id)
        rid = f"{session_id}-refund-{line_id}"
        self._paypal(session_id, "refund", rid, self.paypal.refund_capture, s["capture_id"], self.usd(ln["price"]), rid,
                     f"Refund: {ln['name']} was not yours.")
        self.store.update_line(session_id, line_id, refunded=1)
        self.store.add_event(Event(s["subject"], "line_disputed_upheld", now, value=ln["price"],
                                   meta={"session_id": session_id, "line_id": line_id}))
        return self.view(session_id)

    # --- webhooks -----------------------------------------------------------------

    def on_webhook(self, event: dict) -> str:
        """Feed a verified PayPal webhook into trust_events. Returns what was done."""
        eid, etype = event.get("id", ""), event.get("event_type", "")
        if not self.store.record_webhook(eid, etype, self.clock(), event):
            return "duplicate"
        res = event.get("resource") or {}
        now = self.clock()
        if etype == "CUSTOMER.DISPUTE.CREATED":
            for s in self._sessions_for_dispute(res):
                self.store.add_event(Event(s["subject"], "dispute_opened", now, meta={"dispute_id": res.get("dispute_id")}))
            return "dispute_opened"
        if etype == "CUSTOMER.DISPUTE.RESOLVED":
            outcome = (res.get("dispute_outcome") or {}).get("outcome_code", "")
            if "BUYER" in outcome.upper():
                for s in self._sessions_for_dispute(res):
                    self.store.add_event(Event(s["subject"], "chargeback", now,
                                               meta={"dispute_id": res.get("dispute_id"), "outcome": outcome}))
                return "chargeback"
            return "dispute_resolved_for_seller"
        # Capture, refund and void events confirm what the service already recorded.
        return "recorded"

    def _sessions_for_dispute(self, res: dict) -> list[dict]:
        out = []
        for tx in res.get("disputed_transactions") or []:
            s = self.store.session_by("capture_id", tx.get("seller_transaction_id", ""))
            if s:
                out.append(s)
        return out

    # --- views ----------------------------------------------------------------------

    def _session(self, session_id: str, status: str) -> dict:
        s = self.store.session(session_id)
        if not s:
            raise CheckoutError("no such session")
        if s["status"] != status:
            raise CheckoutError(f"session is {s['status']}, expected {status}")
        return s

    def view(self, session_id: str) -> dict:
        s = self.store.session(session_id)
        if not s:
            raise CheckoutError("no such session")
        s["decision"] = json.loads(s["decision"]) if s["decision"] else None
        lines = self.store.lines(session_id)
        for ln in lines:
            ln["evidence"] = json.loads(ln["evidence"] or "{}")
            ln["price_usd"] = self.usd(ln["price"])
        return {**s, "lines": lines, "paypal_calls": self.store.calls(session_id), "inr_per_usd": self.inr_per_usd}
