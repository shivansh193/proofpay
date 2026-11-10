"""Open PayPal authorizations ("holds") on a timeline, and keeping them from lapsing.

PayPal's rules, as documented and as the sandbox enforces them (docs/verified-facts.md):
- An authorization has a 3-day honor period; after it, the funds are no longer guaranteed.
- It stays capturable for 29 days.
- Reauthorization is only allowed from day 4 to day 29, and the sandbox enforces "only once"
  (error REAUTHORIZATION_TOO_SOON before day 4). A reauthorization returns a new
  authorization ID with a fresh 3-day honor period, up to the original 29 days.

Each open hold gets a risk level and a set of allowed actions computed from those rules.
The AI picks among the allowed actions only, and the service performs the choice with PayPal.
"""

from __future__ import annotations

import json

from proofpay.checkout import CheckoutError, CheckoutService
from proofpay.trust import Event

HONOR_DAYS = 3.0
REAUTH_FROM_DAY = 3.0  # "Day 4" = after 3 full days
VALID_DAYS = 29.0
EXPIRY_WARN_DAYS = 3.0

ACTIONS = ("capture_verified", "reauthorize", "void", "wait")

RESCUE_PROMPT = """You manage PayPal authorization holds for an in-person store. Pick ONE action
for this hold from the allowed list, and explain it to the store manager in two plain sentences.
- capture_verified: charge only the lines with handover evidence now, release the rest.
- reauthorize: renew the hold with PayPal (fresh 3-day honor period); allowed once, day 4-29.
- void: release the whole hold (nothing was verified).
- wait: leave it; it is safe for now.
Prefer keeping the buyer's money free: don't keep holding funds once every line is decided.
Hold facts: {facts}
Allowed actions: {allowed}"""

RESCUE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "action": {"type": "STRING", "enum": list(ACTIONS)},
        "reasoning": {"type": "STRING"},
    },
    "required": ["action", "reasoning"],
}


class HoldsService:
    def __init__(self, store, live: CheckoutService, simulated: CheckoutService, advisor):
        self.store, self.live, self.sim, self.advisor = store, live, simulated, advisor

    def _svc(self, s: dict) -> CheckoutService:
        return self.sim if s.get("simulated") else self.live

    # --- facts -----------------------------------------------------------------------

    def assess(self, s: dict, now: float) -> dict:
        lines = self.store.lines(s["session_id"])
        verified = [ln for ln in lines if ln["disposition"] == "auto_capture" or ln["staff_verdict"] == 1]
        pending = [ln for ln in lines if ln["disposition"] == "staff_check" and ln["staff_verdict"] is None]
        svc = self._svc(s)
        verified_usd = round(sum(svc.usd(ln["price"]) for ln in verified), 2)
        t0 = s["authorized_t"]
        cur = s["reauthorized_t"] or t0  # honor period restarts on reauthorization
        age = now - t0
        honor_end, expiry = cur + HONOR_DAYS, t0 + VALID_DAYS
        open_ = s["status"] == "authorized"

        allowed, flags = [], []
        if open_:
            if age >= VALID_DAYS:
                flags.append("expired: PayPal no longer lets this hold be captured")
            else:
                if verified_usd > 0:
                    allowed.append("capture_verified")
                else:
                    allowed.append("void")
                if REAUTH_FROM_DAY <= age < VALID_DAYS and not s["reauthorized_t"]:
                    allowed.append("reauthorize")
                allowed.append("wait")
                if now >= honor_end:
                    flags.append("honor period over: funds no longer guaranteed")
                if expiry - now <= EXPIRY_WARN_DAYS:
                    flags.append(f"expires in {max(expiry - now, 0):.1f} days")
                if not pending and verified_usd > 0:
                    flags.append("every line decided but the hold is still open")
        risk = "none" if not open_ else ("high" if any(f.startswith(("honor", "expires", "expired")) for f in flags)
                                         else "medium" if flags else "low")
        return {
            "session_id": s["session_id"], "customer_id": s["customer_id"], "status": s["status"],
            "simulated": bool(s["simulated"]), "authorization_id": s["authorization_id"],
            "authorized_amount": s["authorized_amount"], "captured_amount": s["captured_amount"],
            "authorized_t": t0, "reauthorized_t": s["reauthorized_t"], "honor_end_t": honor_end,
            "reauth_from_t": t0 + REAUTH_FROM_DAY, "expiry_t": expiry, "age_days": round(age, 2),
            "verified_usd": verified_usd, "pending_lines": len(pending), "lines": len(lines),
            "risk": risk, "flags": flags, "allowed": allowed,
            "last_action": self._last_action(s["session_id"]),
        }

    def _last_action(self, session_id: str) -> dict | None:
        recs = [r for r in self.store.recommendations(session_id) if r["kind"] == "hold"]
        return recs[-1] if recs else None

    def holds(self) -> list[dict]:
        now = self.live.clock()
        out = [self.assess(s, now) for s in self.store.sessions(limit=200) if s.get("authorized_t")]
        order = {"high": 0, "medium": 1, "low": 2, "none": 3}
        return sorted(out, key=lambda h: (order[h["risk"]], h["expiry_t"]))

    # --- AI rescue ---------------------------------------------------------------------

    def recommend(self, h: dict) -> dict:
        allowed = h["allowed"]
        if not allowed:
            return {"action": "wait", "reasoning": "This hold is closed; nothing to do.", "backend": "rules"}
        facts = {k: h[k] for k in ("age_days", "authorized_amount", "verified_usd", "pending_lines", "lines", "flags")}
        facts["reauthorized_already"] = bool(h["reauthorized_t"])
        if self.advisor.api_key:
            try:
                out = self.advisor._gemini(RESCUE_PROMPT.format(facts=json.dumps(facts), allowed=allowed), RESCUE_SCHEMA)
                if out["action"] in allowed:
                    return {**out, "backend": self.advisor.backend}
                tmpl = self._template(h)
                return {**tmpl, "backend": f"template (model picked a disallowed action: {out['action']})"}
            except Exception as e:  # noqa: BLE001 - fall back, and say so
                return {**self._template(h), "backend": f"template (model error: {type(e).__name__})"}
        return {**self._template(h), "backend": "template"}

    @staticmethod
    def _template(h: dict) -> dict:
        a, v = h["allowed"], h["verified_usd"]
        late = any(f.startswith(("honor", "expires")) for f in h["flags"])
        if "capture_verified" in a and (h["pending_lines"] == 0 or (late and "reauthorize" not in a)):
            return {"action": "capture_verified",
                    "reasoning": f"${v:.2f} of lines have handover evidence. Capturing them now releases the rest of the "
                                 "buyer's money instead of holding it while the authorization ages."}
        if late and "reauthorize" in a:
            return {"action": "reauthorize",
                    "reasoning": "Lines are still undecided and the honor period has passed. Reauthorizing renews the "
                                 "guarantee for 3 days; PayPal allows this once."}
        if "void" in a and late:
            return {"action": "void", "reasoning": "Nothing was verified and the hold is ageing; release it."}
        return {"action": "wait", "reasoning": "The hold is inside its honor period and lines are still being decided."}

    def rescue(self, session_id: str) -> dict:
        s = self.store.session(session_id)
        if not s or not s.get("authorized_t"):
            raise CheckoutError("no such hold")
        h = self.assess(s, self.live.clock())
        rec = self.recommend(h)
        result = self.perform(s, rec["action"])
        self.store.save_recommendation(session_id, f"hold-{len(self.store.recommendations(session_id))}", "hold",
                                       rec["action"], rec["reasoning"], rec["backend"])
        return {"recommendation": rec, "result": result, "hold": self.assess(self.store.session(session_id), self.live.clock())}

    def perform(self, s: dict, action: str) -> dict:
        svc, sid = self._svc(s), s["session_id"]
        if action == "wait":
            return {"done": "nothing"}
        if action == "reauthorize":
            rid = f"{sid}-reauthorize"
            j = svc._paypal(sid, "reauthorize", rid, svc.paypal.reauthorize, s["authorization_id"],
                            float(s["authorized_amount"]), rid)
            self.store.update_session(sid, authorization_id=j["id"], reauthorized_t=svc.clock())
            return {"done": "reauthorized", "new_authorization_id": j["id"]}
        if action == "void":
            rid = f"{sid}-void"
            svc._paypal(sid, "void", rid, svc.paypal.void_authorization, s["authorization_id"], rid)
            self.store.update_session(sid, status="voided", captured_amount="0.00")
            return {"done": "voided"}
        if action == "capture_verified":
            lines = self.store.lines(sid)
            billed = [ln for ln in lines if ln["disposition"] == "auto_capture" or ln["staff_verdict"] == 1]
            total = min(round(sum(svc.usd(ln["price"]) for ln in billed), 2), float(s["authorized_amount"]))
            rid = f"{sid}-capture"
            cap = svc._paypal(sid, "capture", rid, svc.paypal.capture_authorization, s["authorization_id"], total,
                              f"witnessed-{sid}", rid, True, svc.capture_note(sid))
            for ln in billed:
                self.store.update_line(sid, ln["line_id"], billed=1)
            self.store.update_session(sid, status="captured", capture_id=cap["id"], captured_amount=cap["amount"]["value"])
            if billed:
                self.store.add_event(Event(s["subject"], "capture_verified", svc.clock(), tuple(ln["p"] for ln in billed),
                                           sum(ln["price"] for ln in billed), {"session_id": sid, "via": "hold_rescue"}))
            return {"done": "captured", "capture_id": cap["id"], "amount": cap["amount"]["value"]}
        raise CheckoutError(f"unknown action {action}")

    # --- demo data ---------------------------------------------------------------------

    def seed(self, vision, to_lines, fake) -> list[str]:
        """Simulated holds of different ages on the offline stand-in, so the timeline has
        something at every stage. Labelled simulated everywhere they appear."""
        now = self.live.clock()
        plan = [  # (scenario, customer, age in days, staff decided?)
            ("01-first-visit", "meera", 0.4, False),
            ("02-regular-visit", "ravi", 1.8, True),
            ("03-large-basket", "kabir", 3.4, False),
            ("01-first-visit", "zoya", 9.0, False),
            ("02-regular-visit", "dev", 26.8, True),
        ]
        ids = []
        for scen, cust, age, decided in plan:
            trace = vision.basket(scen)
            s = self.sim.start(f"sim-{cust}", to_lines(trace))
            fake.payer_id = f"SIM-{cust.upper()}"
            self.sim.authorize(s["session_id"])
            sid = s["session_id"]
            self.store.update_session(sid, simulated=1, authorized_t=now - age, created_t=now - age)
            if decided:
                for ln in self.store.lines(sid):
                    if ln["disposition"] == "staff_check":
                        self.store.update_line(sid, ln["line_id"], staff_verdict=1)
            ids.append(sid)
        return ids
