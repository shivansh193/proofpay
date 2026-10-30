import pytest

from proofpay.checkout import BasketLine, CheckoutError, CheckoutService
from proofpay.paypal import PayPalClient
from proofpay.paypal.fake import FakePayPal
from proofpay.store import Store
from proofpay.trust import Event


class Clock:
    def __init__(self, t=1000.0):
        self.t = t

    def __call__(self):
        return self.t


@pytest.fixture
def env():
    fake = FakePayPal(payer_id="PAYER1")
    client = PayPalClient("id", "secret", base_url="https://api-m.sandbox.paypal.com", transport=fake.transport())
    clock = Clock()
    svc = CheckoutService(Store(), client, clock=clock, inr_per_usd=100.0)
    return svc, fake, clock


def basket(*ps, price=200.0):
    return [BasketLine(f"l{i}", f"Item {i}", f"SKU{i}", price, p) for i, p in enumerate(ps)]


def test_new_customer_full_flow_captures_only_verified(env):
    svc, fake, _ = env
    s = svc.start("cust1", basket(0.995, 0.6, 0.1))
    assert s["status"] == "created" and s["policy"] in ("standard", "strict")
    disp = {ln["line_id"]: ln["disposition"] for ln in s["lines"]}
    assert disp["l2"] == "release"

    s = svc.authorize(s["session_id"])
    assert s["status"] == "authorized" and s["subject"] == "PAYER1"

    verdicts = {ln["line_id"]: False for ln in s["lines"] if ln["disposition"] == "staff_check"}
    s = svc.exit(s["session_id"], verdicts)
    billed = [ln for ln in s["lines"] if ln["billed"]]
    assert [ln["line_id"] for ln in billed] == (["l0"] if disp["l0"] == "auto_capture" else [])
    if billed:
        assert s["status"] == "captured" and s["captured_amount"] == "2.00"
        assert any(e.kind == "capture_verified" for e in svc.store.events("PAYER1"))


def test_uncertain_line_never_billed_without_staff(env):
    svc, _, _ = env
    s = svc.authorize(svc.start("c", basket(0.995, 0.6))["session_id"])
    with pytest.raises(CheckoutError):
        svc.exit(s["session_id"], {})


def test_nothing_billed_voids(env):
    svc, fake, _ = env
    s = svc.authorize(svc.start("c", basket(0.6))["session_id"])
    s = svc.exit(s["session_id"], {"l0": False})
    assert s["status"] == "voided"
    assert ("POST", f"/v2/payments/authorizations/{s['authorization_id']}/void") in fake.calls


def test_not_mine_refunds_and_records(env):
    svc, fake, _ = env
    s = svc.authorize(svc.start("c", basket(0.995, 0.995))["session_id"])
    verdicts = {ln["line_id"]: True for ln in s["lines"] if ln["disposition"] == "staff_check"}
    s = svc.exit(s["session_id"], verdicts)
    s = svc.not_mine(s["session_id"], "l1", footage_shows_take=False)
    assert next(ln for ln in s["lines"] if ln["line_id"] == "l1")["refunded"] == 1
    # Repeating the tap does not refund twice.
    svc.not_mine(s["session_id"], "l1", footage_shows_take=False)
    assert sum(1 for m, p in fake.calls if p.endswith("/refund")) == 1
    kinds = [e.kind for e in svc.store.events("PAYER1")]
    assert "line_disputed_upheld" in kinds


def test_rejected_dispute_counts_against_customer(env):
    svc, _, _ = env
    s = svc.authorize(svc.start("c", basket(0.995))["session_id"])
    s = svc.exit(s["session_id"], {ln["line_id"]: True for ln in s["lines"] if ln["disposition"] == "staff_check"})
    before = svc.reputation("PAYER1").score
    svc.not_mine(s["session_id"], "l0", footage_shows_take=True)
    assert svc.reputation("PAYER1").score < before


def test_found_at_exit_is_billed_and_recorded(env):
    svc, _, _ = env
    s = svc.authorize(svc.start("c", basket(0.995, 0.6))["session_id"])
    found = [BasketLine("x1", "Hidden item", "SKUX", 20.0, 0.0)]
    s = svc.exit(s["session_id"], {"l1": True, **{ln["line_id"]: True for ln in s["lines"] if ln["disposition"] == "staff_check"}}, found)
    assert any(ln["found_at_exit"] for ln in s["lines"])
    assert "exit_mismatch" in [e.kind for e in svc.store.events("PAYER1")]


def test_returning_customer_earns_express(env):
    svc, _, clock = env
    for i in range(40):
        svc.store.add_event(Event("PAYER1", "capture_verified", clock.t - 280 + i * 7, (0.99,), 600.0))
    svc.store.link_payer("loyal", "PAYER1")
    s = svc.start("loyal", basket(0.995, 0.995, 0.99, price=60.0))
    assert s["policy"] == "express"
    assert all(ln["disposition"] == "auto_capture" for ln in s["lines"])


def test_strict_adds_hold_buffer_line(env):
    svc, fake, clock = env
    svc.store.add_event(Event("PAYER1", "chargeback", clock.t - 1))
    svc.store.link_payer("risky", "PAYER1")
    s = svc.start("risky", basket(0.995, 0.6))
    assert s["policy"] == "strict"
    items = fake.orders[s["order_id"]]["purchase_units"][0]["items"]
    assert items[-1]["sku"] == "HOLD-BUFFER"


def test_paypal_retries_are_idempotent(env):
    svc, fake, _ = env
    s = svc.authorize(svc.start("c", basket(0.995))["session_id"])
    auth = s["authorization_id"]
    for _ in range(2):
        out = svc.paypal.capture_authorization(auth, 1.0, "inv", "same-request-id")
    assert fake.auths[auth]["captured"] == 1


def test_dispute_webhooks_feed_trust(env):
    svc, _, _ = env
    s = svc.authorize(svc.start("c", basket(0.995))["session_id"])
    s = svc.exit(s["session_id"], {ln["line_id"]: True for ln in s["lines"] if ln["disposition"] == "staff_check"})
    ev = {"id": "WH-1", "event_type": "CUSTOMER.DISPUTE.CREATED",
          "resource": {"dispute_id": "D1", "disputed_transactions": [{"seller_transaction_id": s["capture_id"]}]}}
    assert svc.on_webhook(ev) == "dispute_opened"
    assert svc.on_webhook(ev) == "duplicate"
    assert "dispute_opened" in [e.kind for e in svc.store.events("PAYER1")]


def test_live_base_url_refused():
    with pytest.raises(ValueError):
        PayPalClient("id", "secret", base_url="https://api-m.paypal.com")
