"""Real products for the shopping agent, from Channel3's product search API.

Channel3 (https://trychannel3.com) returns structured products across retailers:
title, brand, images, and offers with a price, currency, availability and a buy URL.
`POST https://api.trychannel3.com/v1/search` with header `x-api-key`.

Witnessed only reads products here. The agent still pays through PayPal (sandbox),
behind the trust guard, with a hold that is captured when the delivery is confirmed.
The sandbox payment goes to Witnessed's sandbox merchant, not to the retailer.
"""

from __future__ import annotations

import os

import httpx

SEARCH_URL = "https://api.trychannel3.com/v1/search"


class Channel3:
    def __init__(self, api_key: str | None = None, transport: httpx.BaseTransport | None = None):
        self.api_key = api_key if api_key is not None else os.environ.get("CHANNEL3_API_KEY", "")
        self.http = httpx.Client(timeout=30, transport=transport)

    def search(self, query: str, limit: int = 6) -> list[dict]:
        r = self.http.post(SEARCH_URL, headers={"x-api-key": self.api_key},
                           json={"query": query, "limit": limit, "filters": {"availability": ["InStock"]}})
        r.raise_for_status()
        out = []
        for p in r.json().get("products", []):
            offers = [o for o in p.get("offers") or []
                      if (o.get("price") or {}).get("currency") == "USD" and (o["price"].get("price") or 0) > 0]
            if not offers:
                continue
            o = min(offers, key=lambda x: x["price"]["price"])
            img = next((i.get("cleaned_url") or i.get("url") for i in p.get("images") or [] if i.get("is_main_image")), None)
            out.append({
                "sku": f"c3:{p['id']}",
                "name": p["title"][:120],
                "brand": ", ".join(b["name"] for b in p.get("brands") or []) or None,
                "price_usd": round(float(o["price"]["price"]), 2),
                "retailer": o.get("domain"),
                "url": o.get("url"),
                "image": img,
                "availability": o.get("availability"),
                "query": query,
                "source": "channel3",
            })
        return out
