"""SQLite persistence for the demo. Plain SQL, so moving to Postgres is a driver swap."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from pathlib import Path

from proofpay.trust import Event

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    payer_id TEXT
);
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,              -- created | authorized | captured | voided
    policy TEXT,
    decision TEXT,                     -- JSON explanation
    order_id TEXT,
    authorization_id TEXT,
    authorized_amount TEXT,            -- PayPal currency, as PayPal returned it
    capture_id TEXT,
    captured_amount TEXT,
    created_t REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS lines (
    session_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    name TEXT NOT NULL,
    sku TEXT NOT NULL,
    price REAL NOT NULL,               -- store currency (INR)
    p REAL NOT NULL,
    evidence TEXT,                     -- JSON: crop URLs, frame times
    disposition TEXT,                  -- auto_capture | staff_check | release
    staff_verdict INTEGER,             -- 1 taken, 0 not taken, NULL unchecked
    billed INTEGER NOT NULL DEFAULT 0,
    refunded INTEGER NOT NULL DEFAULT 0,
    found_at_exit INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (session_id, line_id)
);
CREATE TABLE IF NOT EXISTS trust_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    kind TEXT NOT NULL,
    t REAL NOT NULL,
    line_p TEXT NOT NULL,
    value REAL NOT NULL,
    meta TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS trust_events_subject ON trust_events(subject);
CREATE TABLE IF NOT EXISTS webhook_events (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    received_t REAL NOT NULL,
    body TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ai_recommendations (
    session_id TEXT NOT NULL,
    line_id TEXT NOT NULL,
    kind TEXT NOT NULL,                -- exit | dispute
    recommendation TEXT NOT NULL,
    summary TEXT NOT NULL,
    backend TEXT NOT NULL,
    staff_decision TEXT,               -- filled when staff decide
    PRIMARY KEY (session_id, line_id, kind)
);
CREATE TABLE IF NOT EXISTS agent_purchases (
    purchase_id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    items TEXT NOT NULL,               -- JSON
    amount REAL NOT NULL,              -- INR
    verdict TEXT NOT NULL,             -- allow | ask_human | deny
    status TEXT NOT NULL,              -- pending_approval | paid | denied | rejected
    outcome TEXT,                      -- ok | returned | overridden
    reasons TEXT NOT NULL,
    order_id TEXT,
    capture_id TEXT,
    created_t REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS paypal_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    op TEXT NOT NULL,
    request_id TEXT,
    ok INTEGER NOT NULL,
    detail TEXT,
    t REAL NOT NULL
);
"""


class Store:
    def __init__(self, path: str | Path = ":memory:"):
        self.db = sqlite3.connect(str(path), check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    # --- customers ------------------------------------------------------------

    def payer_for(self, customer_id: str) -> str | None:
        r = self.db.execute("SELECT payer_id FROM customers WHERE customer_id=?", (customer_id,)).fetchone()
        return r["payer_id"] if r else None

    def link_payer(self, customer_id: str, payer_id: str) -> None:
        with self.db:
            self.db.execute(
                "INSERT INTO customers(customer_id, payer_id) VALUES(?,?) "
                "ON CONFLICT(customer_id) DO UPDATE SET payer_id=excluded.payer_id",
                (customer_id, payer_id),
            )

    # --- sessions and lines ---------------------------------------------------

    def insert_session(self, row: dict, lines: Iterable[dict]) -> None:
        with self.db:
            self.db.execute(
                f"INSERT INTO sessions({','.join(row)}) VALUES({','.join('?' * len(row))})", tuple(row.values())
            )
            for ln in lines:
                self.db.execute(
                    f"INSERT INTO lines({','.join(ln)}) VALUES({','.join('?' * len(ln))})", tuple(ln.values())
                )

    def update_session(self, session_id: str, **fields) -> None:
        with self.db:
            sets = ",".join(f"{k}=?" for k in fields)
            self.db.execute(f"UPDATE sessions SET {sets} WHERE session_id=?", (*fields.values(), session_id))

    def update_line(self, session_id: str, line_id: str, **fields) -> None:
        with self.db:
            sets = ",".join(f"{k}=?" for k in fields)
            self.db.execute(
                f"UPDATE lines SET {sets} WHERE session_id=? AND line_id=?", (*fields.values(), session_id, line_id)
            )

    def add_line(self, ln: dict) -> None:
        with self.db:
            self.db.execute(f"INSERT INTO lines({','.join(ln)}) VALUES({','.join('?' * len(ln))})", tuple(ln.values()))

    def session(self, session_id: str) -> dict | None:
        r = self.db.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone()
        return dict(r) if r else None

    def session_by(self, column: str, value: str) -> dict | None:
        assert column in {"order_id", "authorization_id", "capture_id"}
        r = self.db.execute(f"SELECT * FROM sessions WHERE {column}=?", (value,)).fetchone()
        return dict(r) if r else None

    def sessions(self, limit: int = 50) -> list[dict]:
        rows = self.db.execute("SELECT * FROM sessions ORDER BY created_t DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

    def lines(self, session_id: str) -> list[dict]:
        rows = self.db.execute("SELECT * FROM lines WHERE session_id=? ORDER BY line_id", (session_id,)).fetchall()
        return [dict(r) for r in rows]

    # --- trust events -----------------------------------------------------------

    def add_event(self, e: Event) -> None:
        with self.db:
            self.db.execute(
                "INSERT INTO trust_events(subject, kind, t, line_p, value, meta) VALUES(?,?,?,?,?,?)",
                (e.subject, e.kind, e.t, json.dumps(list(e.line_p)), e.value, json.dumps(e.meta)),
            )

    def events(self, subject: str | None = None) -> list[Event]:
        q, args = "SELECT * FROM trust_events", ()
        if subject is not None:
            q, args = q + " WHERE subject=?", (subject,)
        rows = self.db.execute(q + " ORDER BY t, id", args).fetchall()
        return [
            Event(r["subject"], r["kind"], r["t"], tuple(json.loads(r["line_p"])), r["value"], json.loads(r["meta"]))
            for r in rows
        ]

    def subjects(self) -> list[str]:
        return [r[0] for r in self.db.execute("SELECT DISTINCT subject FROM trust_events").fetchall()]

    def rename_subject(self, old: str, new: str) -> None:
        """Fold a pre-payment placeholder subject into the PayPal payer id."""
        with self.db:
            self.db.execute("UPDATE trust_events SET subject=? WHERE subject=?", (new, old))
            self.db.execute("UPDATE sessions SET subject=? WHERE subject=?", (new, old))

    # --- AI recommendations -------------------------------------------------------

    def save_recommendation(self, session_id: str, line_id: str, kind: str, rec: str, summary: str, backend: str):
        with self.db:
            self.db.execute(
                "INSERT INTO ai_recommendations(session_id, line_id, kind, recommendation, summary, backend) "
                "VALUES(?,?,?,?,?,?) ON CONFLICT(session_id, line_id, kind) DO UPDATE SET "
                "recommendation=excluded.recommendation, summary=excluded.summary, backend=excluded.backend",
                (session_id, line_id, kind, rec, summary, backend),
            )

    def record_staff_decision(self, session_id: str, line_id: str, kind: str, decision: str):
        with self.db:
            self.db.execute(
                "UPDATE ai_recommendations SET staff_decision=? WHERE session_id=? AND line_id=? AND kind=?",
                (decision, session_id, line_id, kind),
            )

    def recommendations(self, session_id: str | None = None) -> list[dict]:
        q, args = "SELECT * FROM ai_recommendations", ()
        if session_id:
            q, args = q + " WHERE session_id=?", (session_id,)
        return [dict(r) for r in self.db.execute(q, args).fetchall()]

    # --- agent purchases ------------------------------------------------------------

    def insert_purchase(self, row: dict) -> None:
        with self.db:
            self.db.execute(
                f"INSERT INTO agent_purchases({','.join(row)}) VALUES({','.join('?' * len(row))})", tuple(row.values())
            )

    def update_purchase(self, purchase_id: str, **fields) -> None:
        with self.db:
            sets = ",".join(f"{k}=?" for k in fields)
            self.db.execute(f"UPDATE agent_purchases SET {sets} WHERE purchase_id=?", (*fields.values(), purchase_id))

    def purchase(self, purchase_id: str) -> dict | None:
        r = self.db.execute("SELECT * FROM agent_purchases WHERE purchase_id=?", (purchase_id,)).fetchone()
        return dict(r) if r else None

    def purchases(self, agent_id: str) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM agent_purchases WHERE agent_id=? ORDER BY created_t DESC", (agent_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    # --- webhooks and audit -----------------------------------------------------

    def record_webhook(self, event_id: str, event_type: str, t: float, body: dict) -> bool:
        """False if this event id was already processed."""
        try:
            with self.db:
                self.db.execute(
                    "INSERT INTO webhook_events VALUES(?,?,?,?)", (event_id, event_type, t, json.dumps(body))
                )
            return True
        except sqlite3.IntegrityError:
            return False

    def log_call(self, session_id: str | None, op: str, request_id: str | None, ok: bool, detail: str, t: float):
        with self.db:
            self.db.execute(
                "INSERT INTO paypal_calls(session_id, op, request_id, ok, detail, t) VALUES(?,?,?,?,?,?)",
                (session_id, op, request_id, int(ok), detail[:2000], t),
            )

    def calls(self, session_id: str) -> list[dict]:
        rows = self.db.execute("SELECT * FROM paypal_calls WHERE session_id=? ORDER BY id", (session_id,)).fetchall()
        return [dict(r) for r in rows]
