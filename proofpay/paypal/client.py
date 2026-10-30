"""Thin PayPal REST client: Orders v2, Payments v2, webhook verification.

Sandbox only. Every mutating call takes a `request_id` sent as PayPal-Request-Id,
so retrying an operation with the same id can never double-capture or
double-refund. Field names are from docs/verified-facts.md; the ones still
marked OPEN there are read defensively and fail loudly if missing.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

import httpx

SANDBOX = "https://api-m.sandbox.paypal.com"


class PayPalError(RuntimeError):
    def __init__(self, status: int, body: dict | str, op: str):
        self.status, self.body, self.op = status, body, op
        super().__init__(f"PayPal {op} failed ({status}): {body}")


def money(value: float | Decimal, currency: str) -> dict:
    return {"currency_code": currency, "value": str(Decimal(str(value)).quantize(Decimal("0.01"), ROUND_HALF_UP))}


@dataclass(frozen=True)
class OrderItem:
    name: str
    sku: str
    unit_amount: float  # in PayPal currency
    quantity: int = 1


@dataclass(frozen=True)
class Authorization:
    order_id: str
    authorization_id: str
    payer_id: str | None
    amount: str
    status: str
    raw: dict


class PayPalClient:
    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str | None = None,
        currency: str = "USD",
        transport: httpx.BaseTransport | None = None,
    ):
        self.client_id = client_id or os.environ.get("PAYPAL_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("PAYPAL_CLIENT_SECRET", "")
        self.base_url = base_url or os.environ.get("PAYPAL_API_BASE", SANDBOX)
        if "sandbox" not in self.base_url and transport is None:
            raise ValueError("Proofpay only talks to the PayPal sandbox")
        self.currency = currency
        self._http = httpx.Client(base_url=self.base_url, transport=transport, timeout=30)
        self._token: str | None = None
        self._token_expiry = 0.0

    # --- auth ---------------------------------------------------------------

    def _access_token(self) -> str:
        if self._token and time.time() < self._token_expiry - 60:
            return self._token
        r = self._http.post(
            "/v1/oauth2/token",
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
        )
        if r.status_code != 200:
            raise PayPalError(r.status_code, _body(r), "oauth2/token")
        j = r.json()
        self._token, self._token_expiry = j["access_token"], time.time() + float(j.get("expires_in", 300))
        return self._token

    def _call(self, method: str, path: str, op: str, json: dict | None = None, request_id: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {self._access_token()}", "Prefer": "return=representation"}
        if request_id:
            headers["PayPal-Request-Id"] = request_id
        r = self._http.request(method, path, json=json, headers=headers)
        if r.status_code >= 300:
            raise PayPalError(r.status_code, _body(r), op)
        return r.json() if r.content else {}

    # --- Orders v2 ------------------------------------------------------------

    def create_order(self, items: list[OrderItem], reference_id: str, request_id: str) -> dict:
        """Create an AUTHORIZE order. The amount is exactly the item total."""
        total = sum(Decimal(money(i.unit_amount, self.currency)["value"]) * i.quantity for i in items)
        body = {
            "intent": "AUTHORIZE",
            "purchase_units": [
                {
                    "reference_id": reference_id,
                    "custom_id": reference_id,
                    "amount": {
                        **money(total, self.currency),
                        "breakdown": {"item_total": money(total, self.currency)},
                    },
                    "items": [
                        {
                            "name": i.name[:127],
                            "sku": i.sku[:127],
                            "quantity": str(i.quantity),
                            "unit_amount": money(i.unit_amount, self.currency),
                        }
                        for i in items
                    ],
                }
            ],
        }
        return self._call("POST", "/v2/checkout/orders", "create_order", body, request_id)

    def get_order(self, order_id: str) -> dict:
        return self._call("GET", f"/v2/checkout/orders/{order_id}", "get_order")

    def authorize_order(self, order_id: str, request_id: str) -> Authorization:
        j = self._call("POST", f"/v2/checkout/orders/{order_id}/authorize", "authorize_order", {}, request_id)
        try:
            auth = j["purchase_units"][0]["payments"]["authorizations"][0]
        except (KeyError, IndexError) as e:
            raise PayPalError(200, j, "authorize_order: no authorization in response") from e
        return Authorization(
            order_id=order_id,
            authorization_id=auth["id"],
            payer_id=(j.get("payer") or {}).get("payer_id"),
            amount=auth["amount"]["value"],
            status=auth["status"],
            raw=j,
        )

    # --- Payments v2 ----------------------------------------------------------

    def capture_authorization(
        self, authorization_id: str, amount: float, invoice_id: str, request_id: str,
        final_capture: bool = True, note_to_payer: str | None = None,
    ) -> dict:
        body: dict = {
            "amount": money(amount, self.currency),
            "final_capture": final_capture,
            "invoice_id": invoice_id[:127],  # must be unique per capture
        }
        if note_to_payer:
            body["note_to_payer"] = note_to_payer[:255]
        return self._call("POST", f"/v2/payments/authorizations/{authorization_id}/capture", "capture", body, request_id)

    def void_authorization(self, authorization_id: str, request_id: str) -> dict:
        return self._call("POST", f"/v2/payments/authorizations/{authorization_id}/void", "void", None, request_id)

    def reauthorize(self, authorization_id: str, amount: float, request_id: str) -> dict:
        body = {"amount": money(amount, self.currency)}
        return self._call("POST", f"/v2/payments/authorizations/{authorization_id}/reauthorize", "reauthorize", body, request_id)

    def refund_capture(self, capture_id: str, amount: float, request_id: str, note_to_payer: str | None = None) -> dict:
        body: dict = {"amount": money(amount, self.currency)}
        if note_to_payer:
            body["note_to_payer"] = note_to_payer[:255]
        return self._call("POST", f"/v2/payments/captures/{capture_id}/refund", "refund", body, request_id)

    # --- Webhooks -------------------------------------------------------------

    def verify_webhook(self, headers: dict[str, str], event: dict, webhook_id: str) -> bool:
        h = {k.lower(): v for k, v in headers.items()}
        try:
            body = {
                "auth_algo": h["paypal-auth-algo"],
                "cert_url": h["paypal-cert-url"],
                "transmission_id": h["paypal-transmission-id"],
                "transmission_sig": h["paypal-transmission-sig"],
                "transmission_time": h["paypal-transmission-time"],
                "webhook_id": webhook_id,
                "webhook_event": event,
            }
        except KeyError:
            return False
        j = self._call("POST", "/v1/notifications/verify-webhook-signature", "verify_webhook", body)
        return j.get("verification_status") == "SUCCESS"


def _body(r: httpx.Response) -> dict | str:
    try:
        return r.json()
    except ValueError:
        return r.text
