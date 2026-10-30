"""HTTP API for the web app. Run: uvicorn proofpay.api:app --reload"""

from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from proofpay.agent import AgentError, AgentService
from proofpay.ai import Advisor
from proofpay.checkout import BasketLine, CheckoutError, CheckoutService
from proofpay.paypal import PayPalClient, PayPalError
from proofpay.paypal.fake import FakePayPal
from proofpay.store import Store
from proofpay.trust import Event
from proofpay.vision import ReplayEngine, to_lines

ROOT = Path(__file__).resolve().parent.parent


def _load_env() -> None:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
MODE = os.environ.get("PROOFPAY_PAYPAL", "offline")  # offline | sandbox
INR_PER_USD = float(os.environ.get("DEMO_INR_PER_USD", "85"))

store = Store(os.environ.get("PROOFPAY_DB", ROOT / "proofpay.db"))
fake = FakePayPal() if MODE != "sandbox" else None
paypal = (
    PayPalClient()
    if MODE == "sandbox"
    else PayPalClient("offline", "offline", base_url="https://api-m.sandbox.paypal.com", transport=fake.transport())
)
advisor = Advisor()
svc = CheckoutService(store, paypal, inr_per_usd=INR_PER_USD)
agents = AgentService(store, paypal, advisor, inr_per_usd=INR_PER_USD)
vision = ReplayEngine()

app = FastAPI(title="Proofpay")
app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
                   allow_methods=["*"], allow_headers=["*"])


class LineIn(BaseModel):
    line_id: str
    name: str
    sku: str
    price: float = Field(gt=0)
    p: float = Field(ge=0, le=1)
    evidence: dict | None = None


class StartIn(BaseModel):
    customer_id: str
    lines: list[LineIn]


class ScenarioIn(BaseModel):
    scenario: str


class ExitIn(BaseModel):
    staff_verdicts: dict[str, bool] = {}
    found: list[LineIn] = []


class NotMineIn(BaseModel):
    footage_shows_take: bool


class PlanIn(BaseModel):
    task: str


class PurchaseIn(BaseModel):
    items: list[dict]
    task: str = ""


class DecideIn(BaseModel):
    approve: bool


class OutcomeIn(BaseModel):
    outcome: str


class SeedIn(BaseModel):
    customer_id: str
    visits: int = Field(default=12, ge=1, le=60)
    basket_inr: float = Field(default=250, gt=0)


def _guard(fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except (CheckoutError, AgentError) as e:
        raise HTTPException(409, str(e)) from e
    except PayPalError as e:
        raise HTTPException(502, {"op": e.op, "status": e.status, "paypal": e.body}) from e


def _offline_payer(customer_id: str) -> str:
    return f"OFFLINE-{customer_id.upper()}"


# --- config ---------------------------------------------------------------------


@app.get("/api/config")
def config():
    return {
        "mode": MODE,
        "paypal_client_id": os.environ.get("PAYPAL_CLIENT_ID", "") if MODE == "sandbox" else "",
        "currency": paypal.currency,
        "inr_per_usd": INR_PER_USD,
        "vision_engine": vision.name,
        "ai_backend": advisor.backend,
    }


# --- checkout -------------------------------------------------------------------


@app.get("/api/scenarios")
def scenarios():
    return vision.scenarios()


@app.post("/api/sessions/from-scenario")
def start_from_scenario(body: ScenarioIn):
    trace = vision.basket(body.scenario)
    s = _guard(svc.start, trace.customer_id, to_lines(trace))
    return {**s, "scenario": {"title": trace.title, "hidden": list(trace.hidden), "clip": trace.clip}}


@app.post("/api/sessions")
def start(body: StartIn):
    return _guard(svc.start, body.customer_id, [BasketLine(**ln.model_dump()) for ln in body.lines])


@app.get("/api/sessions")
def sessions():
    return [svc.view(s["session_id"]) for s in store.sessions()]


@app.get("/api/sessions/{session_id}")
def session(session_id: str):
    s = _guard(svc.view, session_id)
    return {**s, "ai": store.recommendations(session_id)}


@app.post("/api/sessions/{session_id}/authorize")
def authorize(session_id: str):
    if fake is not None:
        # Offline stand-in: give each demo customer a stable fake payer id.
        s = _guard(svc.view, session_id)
        fake.payer_id = _offline_payer(s["customer_id"])
    return _guard(svc.authorize, session_id)


@app.post("/api/sessions/{session_id}/explain")
def explain(session_id: str):
    s = _guard(svc.view, session_id)
    todo = [ln for ln in s["lines"] if ln["disposition"] == "staff_check"]
    trust = s["decision"]["trust"] if s["decision"] else {}
    recs = advisor.explain_exit(todo, trust)
    for r in recs:
        store.save_recommendation(session_id, r["line_id"], "exit", r["recommendation"], r["summary"], r["backend"])
    return recs


@app.post("/api/sessions/{session_id}/exit")
def exit_check(session_id: str, body: ExitIn):
    out = _guard(svc.exit, session_id, body.staff_verdicts, [BasketLine(**f.model_dump()) for f in body.found])
    for line_id, taken in body.staff_verdicts.items():
        store.record_staff_decision(session_id, line_id, "exit", "taken" if taken else "not_taken")
    return out


@app.post("/api/sessions/{session_id}/lines/{line_id}/triage")
def triage(session_id: str, line_id: str):
    s = _guard(svc.view, session_id)
    ln = next((x for x in s["lines"] if x["line_id"] == line_id), None)
    if not ln:
        raise HTTPException(404, "no such line")
    rec = advisor.triage_dispute(ln)
    store.save_recommendation(session_id, line_id, "dispute", rec["recommendation"], rec["reasoning"], rec["backend"])
    return rec


@app.post("/api/sessions/{session_id}/lines/{line_id}/not-mine")
def not_mine(session_id: str, line_id: str, body: NotMineIn):
    out = _guard(svc.not_mine, session_id, line_id, body.footage_shows_take)
    store.record_staff_decision(session_id, line_id, "dispute", "reject" if body.footage_shows_take else "uphold")
    return out


@app.get("/api/ai/agreement")
def agreement():
    """How often staff agreed with the AI. "check_bag" / "review_footage" defer to
    staff, so they're counted separately rather than as agreement."""
    rows = [r for r in store.recommendations() if r["staff_decision"]]
    firm = [r for r in rows if r["recommendation"] not in ("check_bag", "review_footage")]
    agreed = sum(r["recommendation"] == r["staff_decision"] for r in firm)
    return {
        "decided": len(rows),
        "deferred_to_staff": len(rows) - len(firm),
        "firm": len(firm),
        "agreement_rate": agreed / len(firm) if firm else None,
    }


# --- trust ------------------------------------------------------------------------


@app.get("/api/trust/{subject}")
def trust(subject: str):
    return svc.reputation(subject).explain()


@app.get("/api/subjects")
def subjects():
    out = []
    for s in store.subjects():
        r = svc.reputation(s)
        out.append({"subject": s, "score": r.score, "mean": r.mean, "interval": r.interval,
                    "verified_captures": r.verified_captures})
    return sorted(out, key=lambda x: -x["score"])


@app.post("/api/demo/seed-history")
def seed_history(body: SeedIn):
    """Add SIMULATED weekly verified visits for a demo customer (labelled simulated)."""
    payer = store.payer_for(body.customer_id) or (_offline_payer(body.customer_id) if fake else None)
    if not payer:
        raise HTTPException(409, "customer has no PayPal payer yet; complete one checkout first")
    store.link_payer(body.customer_id, payer)
    now = svc.clock()
    for i in range(body.visits):
        store.add_event(Event(payer, "capture_verified", now - 7 * (body.visits - i), (0.99, 0.995),
                              body.basket_inr, {"simulated": True}))
    return svc.reputation(payer).explain()


# --- agent ------------------------------------------------------------------------


@app.get("/api/agents/{agent_id}")
def agent_status(agent_id: str):
    return agents.status(agent_id)


@app.post("/api/agents/{agent_id}/plan")
def agent_plan(agent_id: str, body: PlanIn):
    return agents.plan(body.task)


@app.post("/api/agents/{agent_id}/purchases")
def agent_purchase(agent_id: str, body: PurchaseIn):
    return _guard(agents.request, agent_id, body.items, body.task)


@app.post("/api/agents/purchases/{purchase_id}/decide")
def agent_decide(purchase_id: str, body: DecideIn):
    return _guard(agents.decide, purchase_id, body.approve)


@app.post("/api/agents/purchases/{purchase_id}/complete")
def agent_complete(purchase_id: str):
    return _guard(agents.complete_payment, purchase_id)


@app.post("/api/agents/purchases/{purchase_id}/outcome")
def agent_outcome(purchase_id: str, body: OutcomeIn):
    return _guard(agents.outcome, purchase_id, body.outcome)


# --- simulator results --------------------------------------------------------------


@app.get("/api/sim")
def sim_results():
    f = ROOT / "docs" / "eval" / "results.json"
    if not f.exists():
        raise HTTPException(404, "run: python -m proofpay.sim --seed 0")
    return json.loads(f.read_text())


# --- webhooks -------------------------------------------------------------------------


@app.post("/api/webhooks/paypal")
async def paypal_webhook(request: Request):
    event = json.loads(await request.body())
    if MODE == "sandbox":
        webhook_id = os.environ.get("PAYPAL_WEBHOOK_ID", "")
        if not webhook_id or not paypal.verify_webhook(dict(request.headers), event, webhook_id):
            raise HTTPException(400, "webhook signature not verified")
    elif os.environ.get("PROOFPAY_ALLOW_UNVERIFIED_WEBHOOKS") != "1":
        # Offline mode can't verify signatures, so it only accepts simulated
        # webhooks when explicitly enabled (local demos and tests).
        raise HTTPException(403, "unverified webhooks are disabled")
    return {"result": svc.on_webhook(event)}
