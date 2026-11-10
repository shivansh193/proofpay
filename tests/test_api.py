import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("PROOFPAY_PAYPAL", "offline")
    monkeypatch.setenv("PROOFPAY_DB", str(tmp_path / "t.db"))
    monkeypatch.setenv("GEMINI_API_KEY", "")
    monkeypatch.setenv("CHANNEL3_API_KEY", "")
    monkeypatch.setenv("PROOFPAY_ALLOW_UNVERIFIED_WEBHOOKS", "1")
    import proofpay.api as api

    importlib.reload(api)
    return TestClient(api.app)


def staff_all(s, taken=True):
    return {ln["line_id"]: taken for ln in s["lines"] if ln["disposition"] == "staff_check"}


def test_scenario_flow_with_explainer_and_refund(client):
    assert client.get("/api/config").json()["mode"] == "offline"
    s = client.post("/api/sessions/from-scenario", json={"scenario": "01-first-visit"}).json()
    sid = s["session_id"]
    assert s["policy"] in ("standard", "strict")
    shampoo = next(ln for ln in s["lines"] if ln["sku"] == "SHAMP-340")
    assert shampoo["disposition"] == "release"

    s = client.post(f"/api/sessions/{sid}/authorize").json()
    assert s["subject"] == "OFFLINE-ASHA"
    recs = client.post(f"/api/sessions/{sid}/explain").json()
    assert recs and all(r["backend"] == "template" for r in recs)

    s = client.post(f"/api/sessions/{sid}/exit", json={"staff_verdicts": staff_all(s)}).json()
    assert s["status"] == "captured"
    line = next(ln for ln in s["lines"] if ln["billed"])
    tri = client.post(f"/api/sessions/{sid}/lines/{line['line_id']}/triage").json()
    assert tri["recommendation"] in ("uphold", "reject", "review_footage")
    s = client.post(f"/api/sessions/{sid}/lines/{line['line_id']}/not-mine", json={"footage_shows_take": False}).json()
    assert next(x for x in s["lines"] if x["line_id"] == line["line_id"])["refunded"] == 1
    assert client.get("/api/ai/agreement").json()["decided"] >= 1


def test_history_earns_express(client):
    s = client.post("/api/sessions/from-scenario", json={"scenario": "02-regular-visit"}).json()
    assert s["policy"] != "express"  # brand new
    client.post("/api/demo/seed-history", json={"customer_id": "asha", "visits": 30, "basket_inr": 200})
    s = client.post("/api/sessions/from-scenario", json={"scenario": "02-regular-visit"}).json()
    assert s["policy"] == "express"


def test_demo_path_reaches_express(client):
    # The video's order: first visit with an upheld "Not mine", then the trust page's 20 seeded visits.
    s = client.post("/api/sessions/from-scenario", json={"scenario": "01-first-visit"}).json()
    sid = s["session_id"]
    s = client.post(f"/api/sessions/{sid}/authorize").json()
    s = client.post(f"/api/sessions/{sid}/exit", json={"staff_verdicts": staff_all(s)}).json()
    line = next(ln for ln in s["lines"] if ln["billed"])
    client.post(f"/api/sessions/{sid}/lines/{line['line_id']}/not-mine", json={"footage_shows_take": False})
    client.post("/api/demo/seed-history", json={"customer_id": "asha", "visits": 20, "basket_inr": 200})
    s = client.post("/api/sessions/from-scenario", json={"scenario": "02-regular-visit"}).json()
    assert s["policy"] == "express"
    sid = s["session_id"]
    client.post(f"/api/sessions/{sid}/authorize")
    s = client.post(f"/api/sessions/{sid}/exit", json={}).json()
    assert s["status"] == "captured" and s["captured_amount"] == s["authorized_amount"]


def test_large_basket_steps_up_and_finds_hidden_item(client):
    client.post("/api/demo/seed-history", json={"customer_id": "ravi", "visits": 30, "basket_inr": 200})
    s = client.post("/api/sessions/from-scenario", json={"scenario": "03-large-basket"}).json()
    assert s["policy"] in ("standard", "strict")
    assert any("usual" in r for r in s["decision"]["reasons"])
    hidden = s["scenario"]["hidden"][0]
    sid = s["session_id"]
    s = client.post(f"/api/sessions/{sid}/authorize").json()
    found = [{"line_id": hidden["item_id"], "name": hidden["name"], "sku": hidden["sku"], "price": hidden["price"], "p": 0.0}]
    s = client.post(f"/api/sessions/{sid}/exit", json={"staff_verdicts": staff_all(s), "found": found}).json()
    assert any(ln["found_at_exit"] for ln in s["lines"])
    kinds = [e["kind"] for e in client.get("/api/trust/OFFLINE-RAVI").json()["events"]]
    assert "exit_mismatch" in kinds


def test_agent_limit_and_approval(client):
    st = client.get("/api/agents/bot1").json()
    assert st["limit"] == 500
    plan = client.post("/api/agents/bot1/plan", json={"task": "weekly restock"}).json()
    assert plan["items"]
    small = client.post("/api/agents/bot1/purchases", json={"items": [{"sku": "SUP-RCPT-10", "qty": 1}]}).json()
    assert small["verdict"] == "allow" and small["status"] == "held"
    mid = client.post("/api/agents/bot1/purchases", json={"items": [{"sku": "SUP-BULB-4", "qty": 1}]}).json()
    assert mid["verdict"] == "ask_human" and mid["status"] == "pending_approval"
    mid = client.post(f"/api/agents/purchases/{mid['purchase_id']}/decide", json={"approve": True}).json()
    assert mid["status"] == "held"
    big = client.post("/api/agents/bot1/purchases", json={"items": [{"sku": "SUP-FRIDGE", "qty": 1}]}).json()
    assert big["verdict"] == "deny"
    for p in (small, mid):
        client.post(f"/api/agents/purchases/{p['purchase_id']}/outcome", json={"outcome": "ok"})
    assert client.get("/api/agents/bot1").json()["limit"] > 500


def test_webhook_dedup(client):
    ev = {"id": "WH-9", "event_type": "PAYMENT.CAPTURE.COMPLETED", "resource": {}}
    assert client.post("/api/webhooks/paypal", json=ev).json()["result"] == "recorded"
    assert client.post("/api/webhooks/paypal", json=ev).json()["result"] == "duplicate"


def test_unverified_webhooks_off_by_default(client, monkeypatch):
    monkeypatch.delenv("PROOFPAY_ALLOW_UNVERIFIED_WEBHOOKS")
    r = client.post("/api/webhooks/paypal", json={"id": "x", "event_type": "y"})
    assert r.status_code == 403


def test_holds_timeline_seed_and_rescue(client):
    seeded = client.post("/api/demo/seed-holds").json()["seeded"]
    assert len(seeded) == 5
    assert client.post("/api/demo/seed-holds").json()["seeded"] == []  # idempotent
    hs = {h["session_id"]: h for h in client.get("/api/holds").json()["holds"]}
    assert all(hs[i]["simulated"] for i in seeded)
    young, decided, past_honor, mid, old = (hs[i] for i in seeded)
    assert young["risk"] == "low" and "reauthorize" not in young["allowed"]
    assert "reauthorize" in past_honor["allowed"] and past_honor["risk"] == "high"
    assert any(f.startswith("expires") for f in old["flags"])

    # Undecided lines, past the honor period: the template reauthorizes (once).
    r = client.post(f"/api/holds/{past_honor['session_id']}/rescue").json()
    assert r["recommendation"]["action"] == "reauthorize"
    assert r["hold"]["reauthorized_t"] and "reauthorize" not in r["hold"]["allowed"]
    # Every line decided: capture the verified lines.
    r = client.post(f"/api/holds/{decided['session_id']}/rescue").json()
    assert r["recommendation"]["action"] == "capture_verified" and r["hold"]["status"] == "captured"
    assert float(r["result"]["amount"]) > 0


def test_evidence_record(client):
    s = client.post("/api/sessions/from-scenario", json={"scenario": "01-first-visit"}).json()
    sid = s["session_id"]
    s = client.post(f"/api/sessions/{sid}/authorize").json()
    client.post(f"/api/sessions/{sid}/exit", json={"staff_verdicts": staff_all(s)})
    ev = client.get(f"/api/sessions/{sid}/evidence").json()
    assert ev["record"] == "witnessed.handover-evidence/v1" and len(ev["sha256"]) == 64
    charged = [ln for ln in ev["lines"] if ln["charged"]]
    assert charged and all(ln["basis"] for ln in ev["lines"])
    assert any("put back" in ln["basis"] for ln in ev["lines"] if not ln["charged"])


def test_agent_buys_channel3_products_hold_then_capture(tmp_path):
    import json as _json

    import httpx

    from proofpay.agent import AgentService, task_to_searches
    from proofpay.ai import Advisor
    from proofpay.catalog import Channel3
    from proofpay.paypal import PayPalClient
    from proofpay.paypal.fake import FakePayPal
    from proofpay.store import Store

    assert task_to_searches("Restock bags, receipt rolls and cleaning supplies for next week.") == [
        "bags", "receipt rolls", "cleaning supplies"]

    def handler(req):
        q = _json.loads(req.content)["query"]
        prod = lambda pid, price: {"id": pid, "title": f"{q} {pid}", "brands": [{"name": "B"}], "images": [],
                                   "offers": [{"url": f"https://buy.example/{pid}", "domain": "shop.example",
                                               "price": {"price": price, "currency": "USD"}, "availability": "InStock"}]}
        return httpx.Response(200, json={"products": [prod("a1", 9.39), prod("a2", 4.25)]})

    fake = FakePayPal()
    pp = PayPalClient("x", "y", base_url="https://api-m.sandbox.paypal.com", transport=fake.transport())
    agents = AgentService(Store(tmp_path / "a.db"), pp, Advisor(api_key=""),
                          products=Channel3("k", transport=httpx.MockTransport(handler)))
    plan = agents.plan("Buy paper bags")
    assert plan["catalog"] == "channel3" and plan["items"][0]["price_usd"] == 4.25  # cheapest offer
    p = agents.request("bot", [{"sku": plan["items"][0]["sku"], "qty": 1}])
    assert p["verdict"] == "allow" and p["status"] == "held"
    assert fake.auths[p["authorization_id"]]["status"] == "CREATED"  # held, not charged
    p = agents.outcome(p["purchase_id"], "ok")
    assert p["status"] == "paid" and fake.auths[p["authorization_id"]]["status"] == "CAPTURED"
