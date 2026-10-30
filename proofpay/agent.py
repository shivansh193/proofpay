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
import uuid
from pathlib import Path

from proofpay.ai import Advisor
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


class AgentError(RuntimeError):
    pass


class AgentService:
    def __init__(self, store: Store, paypal: PayPalClient, advisor: Advisor, cfg: TrustConfig = DEFAULT,
                 clock=days_now, inr_per_usd: float = 85.0, catalog_path: Path = CATALOG):
        self.store, self.paypal, self.advisor, self.cfg = store, paypal, advisor, cfg
        self.clock, self.inr_per_usd = clock, inr_per_usd
        self.catalog = {c["sku"]: c for c in json.loads(catalog_path.read_text(encoding="utf-8"))}

    def status(self, agent_id: str) -> dict:
        rep = reputation(agent_id, self.store.events(agent_id), self.clock(), cfg=self.cfg)
        return {"agent_id": agent_id, "limit": round(agent_limit(rep.score, self.cfg), 2), "trust": rep.explain(),
                "purchases": [self._view(p) for p in self.store.purchases(agent_id)]}

    # --- planning ---------------------------------------------------------------

    def plan(self, task: str) -> dict:
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

    # --- purchase -----------------------------------------------------------------

    def request(self, agent_id: str, items: list[dict], task: str = "") -> dict:
        lines = []
        for i in items:
            c = self.catalog.get(i["sku"])
            if not c:
                raise AgentError(f"unknown sku {i['sku']}")
            lines.append({"sku": c["sku"], "name": c["name"], "price": c["price"], "qty": int(i["qty"])})
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
        p = self._purchase(purchase_id, "paid")
        if p["outcome"]:
            return self._view(p)
        if outcome == "returned" and p["capture_id"]:
            rid = f"agent-{purchase_id}-refund"
            self.paypal.refund_capture(p["capture_id"], self._usd(p["amount"]), rid, "Returned by the buyer.")
        self.store.update_purchase(purchase_id, outcome=outcome)
        kind = "agent_purchase_ok" if outcome == "ok" else "agent_purchase_returned"
        self.store.add_event(Event(p["agent_id"], kind, self.clock(), value=p["amount"],
                                   meta={"purchase_id": purchase_id}))
        return self._view(self.store.purchase(purchase_id))

    # --- internals ------------------------------------------------------------------

    def _usd(self, inr: float) -> float:
        return round(inr / self.inr_per_usd, 2)

    def _pay(self, pid: str) -> None:
        p = self.store.purchase(pid)
        lines = json.loads(p["items"])["lines"]
        order_id = p["order_id"]
        if not order_id:
            items = [OrderItem(ln["name"], ln["sku"], self._usd(ln["price"]), ln["qty"]) for ln in lines]
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
        cap = self.paypal.capture_authorization(auth.authorization_id, float(auth.amount), f"agent-{pid}",
                                                f"agent-{pid}-capture", True)
        self.store.update_purchase(pid, status="paid", capture_id=cap["id"])

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
