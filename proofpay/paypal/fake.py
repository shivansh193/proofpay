"""Offline stand-in for the PayPal sandbox, as an httpx transport.

Used by the tests and by `PROOFPAY_PAYPAL=offline` so the demo runs without
sandbox keys. It mimics only the fields Proofpay reads, enforces the rules
Proofpay relies on (amount = item total, capture <= authorization, refund <=
capture, idempotent PayPal-Request-Id), and is labelled "offline" in the UI.
It is not evidence of how the real sandbox behaves.
"""

from __future__ import annotations

import json
import uuid
from decimal import Decimal

import httpx


class FakePayPal:
    def __init__(self, payer_id: str = "FAKEPAYER001"):
        self.payer_id = payer_id
        self.orders: dict[str, dict] = {}
        self.auths: dict[str, dict] = {}
        self.captures: dict[str, dict] = {}
        self.seen: dict[str, tuple[int, bytes]] = {}
        self.calls: list[tuple[str, str]] = []

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    def handle(self, req: httpx.Request) -> httpx.Response:
        path = req.url.path
        self.calls.append((req.method, path))
        rid = req.headers.get("PayPal-Request-Id")
        if rid and rid in self.seen:
            status, content = self.seen[rid]
            return httpx.Response(status, content=content, headers={"content-type": "application/json"})
        body = json.loads(req.content) if req.content and req.headers.get("content-type", "").startswith("application/json") else {}
        resp = self._route(req.method, path, body)
        if rid and resp.status_code < 300:
            self.seen[rid] = (resp.status_code, resp.read())
        return resp

    def _route(self, method: str, path: str, body: dict) -> httpx.Response:
        parts = path.strip("/").split("/")
        if path == "/v1/oauth2/token":
            return _ok({"access_token": "fake-token", "expires_in": 32400})
        if path == "/v1/notifications/verify-webhook-signature":
            return _ok({"verification_status": "SUCCESS"})
        if path == "/v2/checkout/orders" and method == "POST":
            pu = body["purchase_units"][0]
            total = sum(Decimal(i["unit_amount"]["value"]) * int(i["quantity"]) for i in pu["items"])
            if Decimal(pu["amount"]["value"]) != total:
                return _err(422, "AMOUNT_MISMATCH")
            oid = "ORDER-" + uuid.uuid4().hex[:10].upper()
            self.orders[oid] = {"id": oid, "status": "CREATED", "intent": body["intent"], "purchase_units": [pu]}
            return _ok(self.orders[oid], 201)
        if parts[:3] == ["v2", "checkout", "orders"] and len(parts) == 5 and parts[4] == "authorize":
            o = self.orders.get(parts[3])
            if not o:
                return _err(404, "RESOURCE_NOT_FOUND")
            aid = "AUTH-" + uuid.uuid4().hex[:10].upper()
            amount = o["purchase_units"][0]["amount"]
            self.auths[aid] = {"id": aid, "status": "CREATED", "amount": dict(amount), "captured": Decimal(0)}
            o["status"] = "COMPLETED"
            return _ok({
                "id": o["id"], "status": "COMPLETED",
                "payer": {"payer_id": self.payer_id},
                "purchase_units": [{"payments": {"authorizations": [
                    {"id": aid, "status": "CREATED", "amount": amount}]}}],
            }, 201)
        if parts[:3] == ["v2", "payments", "authorizations"] and len(parts) == 5:
            a = self.auths.get(parts[3])
            if not a:
                return _err(404, "RESOURCE_NOT_FOUND")
            if parts[4] == "void":
                if a["status"] != "CREATED":
                    return _err(422, "AUTHORIZATION_ALREADY_CAPTURED")
                a["status"] = "VOIDED"
                return httpx.Response(204)
            if parts[4] == "capture":
                if a["status"] not in ("CREATED", "PARTIALLY_CAPTURED"):
                    return _err(422, "AUTHORIZATION_ALREADY_CAPTURED")
                amt = Decimal(body["amount"]["value"])
                if a["captured"] + amt > Decimal(a["amount"]["value"]):
                    return _err(422, "CAPTURE_AMOUNT_EXCEEDS_AUTHORIZATION")
                a["captured"] += amt
                a["status"] = "CAPTURED" if body.get("final_capture") else "PARTIALLY_CAPTURED"
                cid = "CAP-" + uuid.uuid4().hex[:10].upper()
                self.captures[cid] = {"id": cid, "status": "COMPLETED", "amount": body["amount"], "refunded": Decimal(0)}
                return _ok({"id": cid, "status": "COMPLETED", "amount": body["amount"],
                            "final_capture": bool(body.get("final_capture"))}, 201)
        if parts[:3] == ["v2", "payments", "captures"] and len(parts) == 5 and parts[4] == "refund":
            c = self.captures.get(parts[3])
            if not c:
                return _err(404, "RESOURCE_NOT_FOUND")
            amt = Decimal(body["amount"]["value"])
            if c["refunded"] + amt > Decimal(c["amount"]["value"]):
                return _err(422, "REFUND_AMOUNT_EXCEEDED")
            c["refunded"] += amt
            return _ok({"id": "REF-" + uuid.uuid4().hex[:10].upper(), "status": "COMPLETED", "amount": body["amount"]}, 201)
        return _err(404, "NOT_FOUND")


def _ok(j: dict, status: int = 200) -> httpx.Response:
    return httpx.Response(status, json=j)


def _err(status: int, issue: str) -> httpx.Response:
    return httpx.Response(status, json={"name": "UNPROCESSABLE_ENTITY", "details": [{"issue": issue}]})
