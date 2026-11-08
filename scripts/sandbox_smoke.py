"""Live PayPal sandbox smoke test, step by step. Reads keys from .env; prints no secrets.

    python scripts/sandbox_smoke.py create              # OAuth + an AUTHORIZE order; prints the approve link
    python scripts/sandbox_smoke.py authorize ORDER_ID  # after the buyer approves in the browser
    python scripts/sandbox_smoke.py capture AUTH_ID AMOUNT [--final]
    python scripts/sandbox_smoke.py void AUTH_ID
    python scripts/sandbox_smoke.py refund CAPTURE_ID AMOUNT
    python scripts/sandbox_smoke.py get-auth AUTH_ID | get-order ORDER_ID
Every response is saved to scripts/sandbox-responses/ (git-ignored) so docs/verified-facts.md can cite real shapes.
"""
import json
import os
import sys
import time
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proofpay.paypal.client import OrderItem, PayPalClient  # noqa: E402

OUT = ROOT / "scripts" / "sandbox-responses"


def env():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def save(name, data):
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{int(time.time())}-{name}.json"
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return path


def main():
    env()
    pp = PayPalClient(os.environ["PAYPAL_CLIENT_ID"], os.environ["PAYPAL_CLIENT_SECRET"],
                      os.environ.get("PAYPAL_API_BASE", "https://api-m.sandbox.paypal.com"))
    cmd, args = sys.argv[1], sys.argv[2:]
    rid = f"smoke-{int(time.time())}"
    if cmd == "create":
        items = [OrderItem("Amul milk 1 L", "MILK-1L", Decimal("0.80"), 1),
                 OrderItem("Dark chocolate 100 g", "CHOC-100", Decimal("2.12"), 1),
                 OrderItem("Proofpay hold buffer", "HOLD-BUFFER", Decimal("0.44"), 1)]
        # Same body the app sends. Adding payment_source.paypal.experience_context (a return URL) made the
        # IN sandbox merchant decline with "To comply with international regulations" (2026-11-08).
        j = pp.create_order(items, reference_id=rid, request_id=rid + "-create")
        approve = next((l["href"] for l in j.get("links", []) if l.get("rel") in ("approve", "payer-action")), None)
        print("status:", j.get("status"), "| order:", j.get("id"), "| intent:", j.get("intent"))
        print("approve link:", approve)
        print("saved", save("create_order", j))
    elif cmd == "authorize":
        a = pp.authorize_order(args[0], request_id=rid + "-authorize")
        print("authorization:", a)
        print("saved", save("authorize_order", pp.get_order(args[0])))
    elif cmd == "capture":
        j = pp.capture_authorization(args[0], Decimal(args[1]), invoice_id=rid, request_id=rid + "-capture",
                                     final_capture="--final" in args)
        print("status:", j.get("status"), "| capture:", j.get("id"), "| amount:", j.get("amount"))
        print("saved", save("capture", j))
    elif cmd == "void":
        j = pp.void_authorization(args[0], request_id=rid + "-void")
        print("void response:", j)
        print("saved", save("void", j))
    elif cmd == "refund":
        j = pp.refund_capture(args[0], Decimal(args[1]), request_id=rid + "-refund")
        print("status:", j.get("status"), "| refund:", j.get("id"), "| amount:", j.get("amount"))
        print("saved", save("refund", j))
    elif cmd == "get-auth":
        j = pp._call("GET", f"/v2/payments/authorizations/{args[0]}", "get_authorization")
        print("status:", j.get("status"), "| amount:", j.get("amount"))
        print("saved", save("get_authorization", j))
    elif cmd == "get-order":
        j = pp.get_order(args[0])
        print(json.dumps({k: j.get(k) for k in ("id", "status", "intent")}))
        print("saved", save("get_order", j))


if __name__ == "__main__":
    main()
