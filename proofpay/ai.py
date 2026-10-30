"""AI helpers for staff: exit-check explainer and "Not mine" dispute triage.

Both only recommend. Staff decide, and every recommendation is stored with the
staff decision so the agreement rate can be reported.

Backend: Gemini (REST generateContent) when GEMINI_API_KEY is set, otherwise a
deterministic template that says it is a template. The model id comes from
GEMINI_MODEL (default below, a stable Flash-tier id as of 2026-10-30).
"""

from __future__ import annotations

import json
import os

import httpx

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = "gemini-3.8-flash"

EXPLAIN_PROMPT = """You help a store employee at the exit of a camera-checkout shop.
For each line below, the camera system was not sure whether the shopper took the item.
Using ONLY the evidence given, write one or two plain sentences per line for the employee:
what the camera saw, and what to look for in the bag. Then recommend "taken", "not_taken"
or "check_bag". Never accuse the shopper; the employee decides.
Shopper trust context (history on this platform only): {trust}
Lines: {lines}"""

TRIAGE_PROMPT = """A shopper tapped "Not mine" on a charged item. Compare the claim with the
camera evidence and recommend "uphold" (refund) or "reject" (the evidence shows the take),
or "review_footage" if the evidence is not enough. Two sentences of reasoning, plain language.
Do not use anything except the evidence below. Staff make the final decision.
Item and evidence: {line}"""

EXPLAIN_SCHEMA = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "line_id": {"type": "STRING"},
            "summary": {"type": "STRING"},
            "recommendation": {"type": "STRING", "enum": ["taken", "not_taken", "check_bag"]},
        },
        "required": ["line_id", "summary", "recommendation"],
    },
}

TRIAGE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "recommendation": {"type": "STRING", "enum": ["uphold", "reject", "review_footage"]},
        "reasoning": {"type": "STRING"},
    },
    "required": ["recommendation", "reasoning"],
}


class Advisor:
    def __init__(self, api_key: str | None = None, model: str | None = None, transport: httpx.BaseTransport | None = None):
        self.api_key = api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "")
        self.model = model or os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
        self._http = httpx.Client(timeout=30, transport=transport)

    @property
    def backend(self) -> str:
        return f"gemini:{self.model}" if self.api_key else "template"

    def _gemini(self, prompt: str, schema: dict):
        r = self._http.post(
            GEMINI_URL.format(model=self.model),
            headers={"x-goog-api-key": self.api_key},
            json={
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json", "responseSchema": schema,
                                     "temperature": 0.2},
            },
        )
        r.raise_for_status()
        text = "".join(p.get("text", "") for p in r.json()["candidates"][0]["content"]["parts"])
        return json.loads(text)

    # --- exit check -------------------------------------------------------------

    def explain_exit(self, lines: list[dict], trust: dict) -> list[dict]:
        """lines: session lines needing a staff check. Returns one recommendation per line."""
        if not lines:
            return []
        compact = [
            {"line_id": ln["line_id"], "item": ln["name"], "price_inr": ln["price"], "p_taken": round(ln["p"], 3),
             "evidence": ln.get("evidence", {})}
            for ln in lines
        ]
        trust_ctx = {k: trust.get(k) for k in ("score", "mean", "verified_captures")}
        if self.api_key:
            try:
                out = self._gemini(EXPLAIN_PROMPT.format(trust=json.dumps(trust_ctx), lines=json.dumps(compact)),
                                   EXPLAIN_SCHEMA)
                return [{**o, "backend": self.backend} for o in out]
            except (httpx.HTTPError, KeyError, ValueError) as e:
                return [{**r, "backend": f"template (model error: {type(e).__name__})"} for r in self._template_exit(compact)]
        return [{**r, "backend": "template"} for r in self._template_exit(compact)]

    @staticmethod
    def _template_exit(lines: list[dict]) -> list[dict]:
        out = []
        for ln in lines:
            p = ln["p_taken"]
            ev = ln["evidence"].get("events", [])
            seen = ", ".join(f"{e.get('type')} at {e.get('t')}s" for e in ev) or "no clear pick or put-back"
            rec = "taken" if p >= 0.8 else "not_taken" if p < 0.45 else "check_bag"
            out.append({
                "line_id": ln["line_id"],
                "summary": f"Camera put {ln['item']} at {p:.0%} likely taken ({seen}). "
                           + ("Look for it in the bag." if rec != "not_taken" else "It was probably put back."),
                "recommendation": rec,
            })
        return out

    # --- dispute triage -----------------------------------------------------------

    def triage_dispute(self, line: dict) -> dict:
        compact = {"item": line["name"], "price_inr": line["price"], "p_taken": round(line["p"], 3),
                   "staff_verdict": line.get("staff_verdict"), "evidence": line.get("evidence", {})}
        if self.api_key:
            try:
                return {**self._gemini(TRIAGE_PROMPT.format(line=json.dumps(compact)), TRIAGE_SCHEMA),
                        "backend": self.backend}
            except (httpx.HTTPError, KeyError, ValueError) as e:
                return {**self._template_triage(compact), "backend": f"template (model error: {type(e).__name__})"}
        return {**self._template_triage(compact), "backend": "template"}

    @staticmethod
    def _template_triage(line: dict) -> dict:
        if line.get("staff_verdict") == 1:
            return {"recommendation": "review_footage",
                    "reasoning": "A staff member confirmed this item at the exit. Check the footage before deciding."}
        p = line["p_taken"]
        if p >= 0.98:
            return {"recommendation": "review_footage",
                    "reasoning": f"The camera was {p:.0%} sure this item left with the shopper. Check the footage."}
        return {"recommendation": "uphold",
                "reasoning": f"The camera was only {p:.0%} sure, so a wrong charge is plausible. Refunding is reasonable."}
