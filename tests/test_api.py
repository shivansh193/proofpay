import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("PROOFPAY_PAYPAL", "offline")
    monkeypatch.setenv("PROOFPAY_DB", str(tmp_path / "t.db"))
    monkeypatch.setenv("GEMINI_API_KEY", "")
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
    assert small["verdict"] == "allow" and small["status"] == "paid"
    mid = client.post("/api/agents/bot1/purchases", json={"items": [{"sku": "SUP-BULB-4", "qty": 1}]}).json()
    assert mid["verdict"] == "ask_human" and mid["status"] == "pending_approval"
    mid = client.post(f"/api/agents/purchases/{mid['purchase_id']}/decide", json={"approve": True}).json()
    assert mid["status"] == "paid"
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
