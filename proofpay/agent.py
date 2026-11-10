"""Agent client: an LLM shopping agent whose PayPal spending is gated by earned trust.

The agent plans a purchase from a catalog (Gemini when GEMINI_API_KEY is set, a
fixed shopping list otherwise). Every purchase goes through
`authorize_agent_spend`: allow pays straight away, ask_human waits for a
person, deny stops it. The human later marks the purchase ok or returned,
and those outcomes are the agent's trust evidence.

Payments use the same REST client as checkout. The PayPal Agent Toolkit's
tools are merchant-side (create_order / get_order / pay_order), so wrapping
them would not change what the guard sees. See README.
"""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

from proofpay.ai import Advisor
from proofpay.catalog import Channel3
from proofpay.checkout import days_now
from proofpay.paypal import OrderItem, PayPalClient, PayPalError
from proofpay.store import Store
from proofpay.trust import DEFAULT, Event, TrustConfig, agent_limit, authorize_agent_spend, reputation

CATALOG = Path(__file__).resolve().parent.parent / "demo" / "catalog.json"

PLAN_PROMPT = """You are a purchasing agent for a small shop. Task: {task}
Choose items ONLY from this catalog (use the exact sku), with quantities, to complete the task.
Keep the total sensible for the task. Catalog: {catalog}"""

PLAN_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "items": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {"sku": {"type": "STRING"}, "qty": {"type": "INTEGER"}},
                "required": ["sku", "qty"],
            },
        },
        "rationale": {"type": "STRING"},
    },
    "required": ["items", "rationale"],
}


SEARCH_PROMPT = """You are a purchasing agent for a small shop. Task: {task}
Turn the task into 1 to 4 product searches for an online product catalog, each a short
product phrase (e.g. "paper grocery bags"), with the quantity to buy. Keep it sensible."""

SEARCH_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "searches": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {"query": {"type": "STRING"}, "qty": {"type": "INTEGER"}},
                "required": ["query", "qty"],
            },
        },
        "rationale": {"type": "STRING"},
    },
    "required": ["searches", "rationale"],
}


def task_to_searches(task: str) -> list[str]:
    """Template planner: "Restock bags, receipt rolls and cleaning supplies for next week."
    becomes ["bags", "receipt rolls", "cleaning supplies"]."""
    t = re.sub(r"\b(for|by|before)\b.*$", "", task.strip().rstrip("."), flags=re.I)
    t = re.sub(r"^\s*(please\s+)?(restock|buy|order|get|purchase|find)\b", "", t, flags=re.I)
    parts = [x.strip() for x in re.split(r",|\band\b", t) if x.strip()]
    return parts[:4] or [task.strip()]


class AgentError(RuntimeError):
    pass


class AgentService:
    def __init__(self, store: Store, paypal: PayPalClient, advisor: Advisor, cfg: TrustConfig = DEFAULT,
                 clock=days_now, inr_per_usd: float = 85.0, catalog_path: Path = CATALOG,
                 products: Channel3 | None = None):
        self.store, self.paypal, self.advisor, self.cfg = store, paypal, advisor, cfg
        self.clock, self.inr_per_usd = clock, inr_per_usd
        self.catalog = {c["sku"]: c for c in json.loads(catalog_path.read_text(encoding="utf-8"))}
        self.products = products if products and products.api_key else None
        self.found: dict[str, dict] = {}  # Channel3 products seen in plans, by sku

    @property
    def catalog_source(self) -> str:
        return "channel3" if self.products else "demo catalog"

    def status(self, agent_id: str) -> dict:
        rep = reputation(agent_id, self.store.events(agent_id), self.clock(), cfg=self.cfg)
        return {"agent_id": agent_id, "limit": round(agent_limit(rep.score, self.cfg), 2), "trust": rep.explain(),
                "purchases": [self._view(p) for p in self.store.purchases(agent_id)]}

    # --- planning ---------------------------------------------------------------

    def plan(self, task: str) -> dict:
        if self.products:
            return self._plan_channel3(task)
        catalog = [{"sku": c["sku"], "name": c["name"], "price_inr": c["price"]} for c in self.catalog.values()]
        if self.advisor.api_key:
            try:
                out = self.advisor._gemini(PLAN_PROMPT.format(task=task, catalog=json.dumps(catalog)), PLAN_SCHEMA)
                items = [i for i in out["items"] if i["sku"] in self.catalog and i["qty"] > 0]
                return {"items": items, "rationale": out["rationale"], "planner": self.advisor.backend}
            except Exception as e:  # noqa: BLE001 - any model failure falls back to the fixed list
                fallback = f"fixed list (model error: {type(e).__name__})"
        else:
            fallback = "fixed list (no GEMINI_API_KEY)"
        default = [c for c in self.catalog.values() if c.get("default_qty")]
        return {"items": [{"sku": c["sku"], "qty": c["default_qty"]} for c in default],
                "rationale": "Weekly restock list.", "planner": fallback}

    def _plan_channel3(self, task: str) -> dict:
        planner, rationale = "template", ""
        searches = [{"query": q, "qty": 1} for q in task_to_searches(task)]
        if self.advisor.api_key:
            try:
                out = self.advisor._gemini(SEARCH_PROMPT.format(task=task), SEARCH_SCHEMA)
                got = [x for x in out["searches"] if x["query"].strip() and x["qty"] > 0][:4]
                if got:
                    searches, rationale, planner = got, out["rationale"], self.advisor.backend
            except Exception as e:  # noqa: BLE001 - any model failure falls back to the template split
                planner = f"template (model error: {type(e).__name__})"
        items, missing = [], []
        for sr in searches:
            hits = self.products.search(sr["query"])
            if not hits:
                missing.append(sr["query"])
                continue
            pick = min(hits, key=lambda h: h["price_usd"])  # cheapest in-stock USD offer
            self.found[pick["sku"]] = pick
            items.append({"sku": pick["sku"], "qty": min(int(sr["qty"]), 10), "name": pick["name"],
                          "price_usd": pick["price_usd"], "retailer": pick["retailer"], "url": pick["url"],
                          "image": pick["image"], "brand": pick["brand"], "query": sr["query"]})
        why = rationale or ("Searched Channel3 for " + ", ".join(repr(x["query"]) for x in searches)
                            + "; took the cheapest in-stock offer for each.")
        if missing:
            why += f" Nothing in stock for {', '.join(missing)}."
        return {"items": items, "rationale": why, "planner": planner, "catalog": "channel3"}

    def _line(self, sku: str, qty: int) -> dict:
        if sku in self.found:
            c = self.found[sku]
            return {"sku": sku, "name": c["name"], "price": round(c["price_usd"] * self.inr_per_usd, 2),
                    "price_usd": c["price_usd"], "qty": qty, "retailer": c["retailer"], "url": c["url"],
                    "source": "channel3"}
        c = self.catalog.get(sku)
        if not c:
            hint = " (plan again: Channel3 results are kept in memory)" if sku.startswith("c3:") else ""
            raise AgentError(f"unknown sku {sku}{hint}")
        return {"sku": c["sku"], "name": c["name"], "price": c["price"], "qty": qty}

    # --- purchase -----------------------------------------------------------------

    def request(self, agent_id: str, items: list[dict], task: str = "") -> dict:
        lines = [self._line(i["sku"], int(i["qty"])) for i in items]
        amount = round(sum(ln["price"] * ln["qty"] for ln in lines), 2)
        rep = reputation(agent_id, self.store.events(agent_id), self.clock(), cfg=self.cfg)
        d = authorize_agent_spend(rep, amount, self.cfg)
        pid = uuid.uuid4().hex[:12]
        status = {"allow": "approved", "ask_human": "pending_approval", "deny": "denied"}[d.verdict]
        self.store.insert_purchase({
            "purchase_id": pid, "agent_id": agent_id, "items": json.dumps({"lines": lines, "task": task}),
            "amount": amount, "verdict": d.verdict, "status": status, "reasons": json.dumps(list(d.reasons)),
            "created_t": self.clock(),
        })
        if d.verdict == "allow":
            self._pay(pid)
        return self._view(self.store.purchase(pid))

    def decide(self, purchase_id: str, approve: bool) -> dict:
        """A human answers an ask_human request."""
        p = self._purchase(purchase_id, "pending_approval")
        if approve:
            self.store.update_purchase(purchase_id, status="approved")
            self._pay(purchase_id)
        else:
            self.store.update_purchase(purchase_id, status="rejected", outcome="overridden")
            self.store.add_event(Event(p["agent_id"], "agent_purchase_overridden", self.clock(),
                                       value=p["amount"], meta={"purchase_id": purchase_id}))
        return self._view(self.store.purchase(purchase_id))

    def complete_payment(self, purchase_id: str) -> dict:
        """After the payer approved the PayPal order (sandbox), authorize and capture it."""
        self._purchase(purchase_id, "awaiting_payer")
        self._pay(purchase_id)
        return self._view(self.store.purchase(purchase_id))

    def outcome(self, purchase_id: str, outcome: str) -> dict:
        """The human reports whether the purchase was right (ok) or sent back (returned)."""
        if outcome not in ("ok", "returned"):
            raise AgentError("outcome must be ok or returned")
        p = self.store.purchase(purchase_id)
        if not p or p["status"] not in ("held", "paid"):
            raise AgentError(f"purchase is {p['status'] if p else 'missing'}, expected held")
        if p["outcome"]:
            return self._view(p)
        if p["status"] == "held":
            # Hold-then-capture, as at the store exit: charge only once delivery is confirmed.
            if outcome == "ok":
                rid = f"agent-{purchase_id}-capture"
                cap = self.paypal.capture_authorization(p["authorization_id"], self._order_usd(p), f"agent-{purchase_id}",
                                                        rid, True, "Captured after the delivery was confirmed.")
                self.store.update_purchase(purchase_id, status="paid", capture_id=cap["id"])
            else:
                self.paypal.void_authorization(p["authorization_id"], f"agent-{purchase_id}-void")
                self.store.update_purchase(purchase_id, status="voided")
        elif outcome == "returned" and p["capture_id"]:
            rid = f"agent-{purchase_id}-refund"
            self.paypal.refund_capture(p["capture_id"], self._order_usd(p), rid, "Returned by the buyer.")
        self.store.update_purchase(purchase_id, outcome=outcome)
        kind = "agent_purchase_ok" if outcome == "ok" else "agent_purchase_returned"
        self.store.add_event(Event(p["agent_id"], kind, self.clock(), value=p["amount"],
                                   meta={"purchase_id": purchase_id}))
        return self._view(self.store.purchase(purchase_id))

    # --- internals ------------------------------------------------------------------

    def _usd(self, inr: float) -> float:
        return round(inr / self.inr_per_usd, 2)

    def _line_usd(self, ln: dict) -> float:
        return ln["price_usd"] if ln.get("price_usd") is not None else self._usd(ln["price"])

    def _order_usd(self, p: dict) -> float:
        return round(sum(self._line_usd(ln) * ln["qty"] for ln in json.loads(p["items"])["lines"]), 2)

    def _pay(self, pid: str) -> None:
        p = self.store.purchase(pid)
        lines = json.loads(p["items"])["lines"]
        order_id = p["order_id"]
        if not order_id:
            items = [OrderItem(ln["name"], ln["sku"][:127], self._line_usd(ln), ln["qty"]) for ln in lines]
            order = self.paypal.create_order(items, f"agent-{pid}", f"agent-{pid}-create")
            order_id = order["id"]
            self.store.update_purchase(pid, order_id=order_id)
        try:
            auth = self.paypal.authorize_order(order_id, f"agent-{pid}-authorize")
        except PayPalError as e:
            if "ORDER_NOT_APPROVED" in json.dumps(e.body):
                # Sandbox: the payer must approve the order once in PayPal.
                self.store.update_purchase(pid, status="awaiting_payer")
                return
            raise
        # Hold only. The capture happens when a person confirms the delivery (outcome "ok").
        self.store.update_purchase(pid, status="held", authorization_id=auth.authorization_id)

    def _purchase(self, pid: str, status: str) -> dict:
        p = self.store.purchase(pid)
        if not p:
            raise AgentError("no such purchase")
        if p["status"] != status:
            raise AgentError(f"purchase is {p['status']}, expected {status}")
        return p

    @staticmethod
    def _view(p: dict) -> dict:
        return {**p, "items": json.loads(p["items"]), "reasons": json.loads(p["reasons"])}
