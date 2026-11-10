"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Grid } from "@/components/Grid";
import { api } from "@/lib/api";

type Hold = {
  session_id: string; customer_id: string; status: string; simulated: boolean; authorization_id: string;
  authorized_amount: string; captured_amount: string | null; authorized_t: number; reauthorized_t: number | null;
  honor_end_t: number; reauth_from_t: number; expiry_t: number; age_days: number; verified_usd: number;
  pending_lines: number; lines: number; risk: "high" | "medium" | "low" | "none"; flags: string[]; allowed: string[];
  last_action: { recommendation: string; summary: string; backend: string } | null;
};
type Rescue = { recommendation: { action: string; reasoning: string; backend: string }; result: Record<string, string> };

const day = 86400000;
const toDate = (t: number) => new Date(t * day);

function events(h: Hold) {
  const ev: Record<string, unknown>[] = [];
  const id = h.session_id;
  const closed = h.status !== "authorized";
  const end = closed ? null : h.expiry_t;
  // PayPal guarantees the funds in the honor period (3 days, restarted by a reauthorization).
  ev.push({ id: `${id}-honor`, resourceId: id, name: "Honor period (funds guaranteed)", startDate: toDate(h.authorized_t),
            endDate: toDate(Math.min(h.authorized_t + 3, h.expiry_t)), eventColor: "green" });
  if (h.reauthorized_t) {
    ev.push({ id: `${id}-reauth`, resourceId: id, name: "Reauthorized: new honor period", startDate: toDate(h.reauthorized_t),
              endDate: toDate(Math.min(h.reauthorized_t + 3, h.expiry_t)), eventColor: "teal" });
  }
  if (end) {
    ev.push({ id: `${id}-open`, resourceId: id, name: "Capturable, not guaranteed", startDate: toDate(h.authorized_t + 3),
              endDate: toDate(end), eventColor: h.risk === "high" ? "orange" : "gray" });
    ev.push({ id: `${id}-expiry`, resourceId: id, name: "Expires (day 29)", startDate: toDate(end), duration: 0,
              eventColor: "red" });
  } else {
    const label = h.status === "captured" ? `Captured $${h.captured_amount}` : "Voided";
    const at = h.last_action ? Date.now() / day : h.authorized_t + 0.1;
    ev.push({ id: `${id}-closed`, resourceId: id, name: label, startDate: toDate(Math.max(at, h.authorized_t)),
              duration: 0, eventColor: h.status === "captured" ? "blue" : "gray" });
  }
  return ev;
}

// Bryntum is loaded from public/bryntum (copied there by scripts/copy-bryntum.mjs), not
// bundled: see that script for why.
let bryntumPromise: Promise<any> | null = null;
function loadBryntum(): Promise<any> {
  if (bryntumPromise) return bryntumPromise;
  for (const href of ["scheduler.css", "stockholm-dark.css", "fontawesome/css/fontawesome.css", "fontawesome/css/solid.css"]) {
    const l = document.createElement("link");
    l.rel = "stylesheet"; l.href = `/bryntum/${href}`;
    document.head.appendChild(l);
  }
  bryntumPromise = new Promise((resolve, reject) => {
    const sc = document.createElement("script");
    sc.src = "/bryntum/scheduler.umd.js";
    sc.onload = () => {
      const w = window as any;
      const ns = w.bryntum?.scheduler ?? w.bryntum;
      ns?.Scheduler ? resolve(ns) : reject(new Error("Bryntum Scheduler did not load"));
    };
    sc.onerror = () => reject(new Error("could not load /bryntum/scheduler.umd.js"));
    document.head.appendChild(sc);
  });
  return bryntumPromise;
}

export default function HoldsPage() {
  const host = useRef<HTMLDivElement>(null);
  const sched = useRef<any>(null);
  const [holds, setHolds] = useState<Hold[]>([]);
  const [last, setLast] = useState<Rescue | null>(null);
  const [busy, setBusy] = useState("");
  const [ready, setReady] = useState(false);
  const [err, setErr] = useState("");

  const load = useCallback(async () => {
    const r = await api<{ holds: Hold[] }>("/api/holds");
    setHolds(r.holds);
  }, []);

  useEffect(() => { load().catch((e) => setErr(String(e))); }, [load]);

  useEffect(() => {
    let alive = true;
    loadBryntum().then(({ Scheduler, StringHelper }) => {
      if (!alive || !host.current || sched.current) return;
      const now = new Date();
      sched.current = new Scheduler({
        appendTo: host.current,
        startDate: new Date(now.getTime() - 30 * day),
        endDate: new Date(now.getTime() + 30 * day),
        viewPreset: "weekAndDayLetter",
        rowHeight: 46,
        barMargin: 8,
        readOnly: true,
        eventStyle: "filled",
        features: {
          timeRanges: { showCurrentTimeLine: { name: "Now" } },
          eventTooltip: {
            template: ({ eventRecord }: any) =>
              `<b>${StringHelper.encodeHtml(eventRecord.name)}</b><br>${eventRecord.startDate.toLocaleString()}` +
              (eventRecord.duration ? ` to ${eventRecord.endDate.toLocaleString()}` : ""),
          },
        },
        columns: [
          { text: "Order", field: "name", width: 190,
            renderer: ({ record }: any) => StringHelper.encodeHtml(record.name) },
          { text: "Hold", field: "amount", width: 80 },
          { text: "Risk", field: "risk", width: 80 },
        ],
        resources: [],
        events: [],
      });
      setReady(true);
    }).catch((e) => setErr(String(e)));
    return () => { alive = false; sched.current?.destroy(); sched.current = null; };
  }, []);

  useEffect(() => {
    const s = sched.current;
    if (!s) return;
    s.resources = holds.map((h) => ({
      id: h.session_id,
      name: `${h.customer_id} · ${h.simulated ? "simulated" : "PayPal sandbox"}`,
      amount: `$${h.authorized_amount}`,
      risk: h.status === "authorized" ? h.risk : h.status,
    }));
    s.events = holds.flatMap(events);
  }, [holds, ready]);

  const rescue = async (h: Hold) => {
    setBusy(h.session_id); setErr("");
    try {
      setLast(await api<Rescue>(`/api/holds/${h.session_id}/rescue`, {}));
      await load();
    } catch (e) { setErr(String(e)); } finally { setBusy(""); }
  };
  const seed = async () => { await api("/api/demo/seed-holds", {}); await load(); };
  const open = holds.filter((h) => h.status === "authorized");

  return (
    <>
      <h1>Holds</h1>
      <p className="lede">
        Every open PayPal authorization on one timeline. PayPal guarantees the funds for a 3-day honor period and lets
        the hold be captured for 29 days. A hold can be reauthorized once, from day 4 to day 29 (the sandbox refuses earlier
        with <code>REAUTHORIZATION_TOO_SOON</code>). The AI picks what to do with each hold at risk, from the actions those
        rules allow, and Witnessed does it with PayPal.
      </p>
      <div className="panel">
        <div className="row" style={{ justifyContent: "space-between" }}>
          <span className="small muted">Green: honor period. Teal: renewed by a reauthorization. Orange: guarantee lapsed. Red: expiry. Simulated holds run on the offline stand-in, because no real authorization can be back-dated.</span>
          {!holds.some((h) => h.simulated) && <button onClick={seed}>Add simulated holds</button>}
        </div>
        <div ref={host} style={{ height: Math.max(220, 70 + holds.length * 46) }} />
      </div>
      {err && <p className="error">{err}</p>}
      {last && (
        <div className="panel">
          <h2>AI decision: {last.recommendation.action.replace("_", " ")}</h2>
          <p>{last.recommendation.reasoning}</p>
          <p className="small muted">Model: {last.recommendation.backend}. PayPal result: {JSON.stringify(last.result)}</p>
        </div>
      )}
      <div className="panel">
        <h2>Open holds</h2>
        <Grid<Hold>
          rows={open}
          height={Math.max(160, 60 + open.length * 42)}
          cols={[
            { field: "customer_id", headerName: "Customer" },
            { headerName: "Source", valueGetter: (p) => (p.data?.simulated ? "simulated" : "PayPal sandbox") },
            { field: "authorized_amount", headerName: "Held $" },
            { field: "verified_usd", headerName: "Verified $" },
            { field: "age_days", headerName: "Age (days)" },
            { field: "risk", headerName: "Risk" },
            { headerName: "Why", flex: 2, valueGetter: (p) => p.data?.flags.join("; ") || "safe for now" },
            { headerName: "", minWidth: 150, cellRenderer: (p: { data?: Hold }) => p.data && (
                <button disabled={!!busy} onClick={() => rescue(p.data!)}>{busy === p.data.session_id ? "Working…" : "Ask AI to act"}</button>) },
          ]}
        />
      </div>
    </>
  );
}
