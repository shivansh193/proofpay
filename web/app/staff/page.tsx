"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useCallback, useEffect, useState } from "react";
import { PolicyCosts, TrustCard } from "@/components/Decision";
import { Grid } from "@/components/Grid";
import { api, DISPOSITION, inr, pct, type Session } from "@/lib/api";

type Hidden = { item_id: string; name: string; sku: string; price: number; notes?: string };
type Rec = { line_id: string; summary: string; recommendation: string; backend: string };

export default function StaffPage() {
  return <Suspense><Staff /></Suspense>;
}

function Staff() {
  const params = useSearchParams();
  const [list, setList] = useState<Session[]>([]);
  const [s, setS] = useState<Session | null>(null);
  const [verdicts, setVerdicts] = useState<Record<string, boolean>>({});
  const [found, setFound] = useState<Hidden[]>([]);
  const [hidden, setHidden] = useState<Hidden[]>([]);
  const [recs, setRecs] = useState<Rec[]>([]);
  const [agree, setAgree] = useState<{ decided: number; firm: number; agreement_rate: number | null } | null>(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => setList(await api<Session[]>("/api/sessions")), []);
  const open = useCallback(async (id: string) => {
    const x = await api<Session>(`/api/sessions/${id}`);
    setS(x); setVerdicts({}); setFound([]);
    setRecs((x.ai ?? []).filter((r) => r.kind === "exit") as Rec[]);
    const sc = await api<{ customer_id: string; hidden: Hidden[] }[]>("/api/scenarios");
    setHidden(sc.filter((c) => c.customer_id === x.customer_id).flatMap((c) => c.hidden));
  }, []);

  useEffect(() => {
    load();
    api("/api/ai/agreement").then(setAgree);
    const id = params.get("s");
    if (id) open(id);
    const h = setInterval(load, 3000);
    return () => clearInterval(h);
  }, [load, open, params]);

  const run = async (f: () => Promise<unknown>) => {
    setErr(""); setBusy(true);
    try { await f(); } catch (e) { setErr(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };

  const toCheck = s?.lines.filter((l) => l.disposition === "staff_check" && !l.found_at_exit) ?? [];
  const ready = s?.status === "authorized" && toCheck.every((l) => l.line_id in verdicts);

  return (
    <>
      <h1>Staff exit check</h1>
      <p className="lede">
        Lines the camera is sure about are captured automatically (when policy allows). Uncertain lines need you.
        You decide; the AI only explains the evidence.
      </p>
      {err && <div className="err">{err}</div>}

      <div className="panel">
        <div className="row"><h2 style={{ margin: 0 }}>Visits</h2><span className="spacer" />
          {agree && <span className="muted small">AI agreement: {agree.agreement_rate === null ? "no decisions yet" : `${pct(agree.agreement_rate)} of ${agree.firm} firm recommendations`}</span>}
        </div>
        <Grid<Session>
          rows={list}
          height={220}
          onRowClicked={(r) => open(r.session_id)}
          cols={[
            { field: "session_id", headerName: "Visit" },
            { field: "customer_id", headerName: "Customer" },
            { field: "policy", headerName: "Policy" },
            { field: "status", headerName: "Status" },
            { headerName: "Score", valueGetter: (p) => p.data?.decision?.score?.toFixed(2) },
            { field: "authorized_amount", headerName: "Authorized $" },
            { field: "captured_amount", headerName: "Captured $" },
          ]}
        />
      </div>

      {s && (
        <>
          <div className="panel">
            <div className="row">
              <h2 style={{ margin: 0 }}>Visit {s.session_id}</h2>
              <span className={`chip ${s.policy}`}>{s.policy}</span>
              <span className={`chip ${s.status}`}>{s.status}</span>
              <span className="spacer" />
              {s.status === "authorized" && toCheck.length > 0 && (
                <button disabled={busy} onClick={() => run(async () => setRecs(await api<Rec[]>(`/api/sessions/${s.session_id}/explain`, {})))}>
                  Explain uncertain lines (AI)
                </button>
              )}
            </div>
            <div className="scroll">
              <table className="t" style={{ marginTop: 10 }}>
                <thead><tr><th>Item</th><th className="num">Price</th><th className="num">Camera</th><th>Disposition</th><th>Evidence</th><th>Decision</th></tr></thead>
                <tbody>
                  {s.lines.map((ln) => {
                    const rec = recs.find((r) => r.line_id === ln.line_id);
                    const v = verdicts[ln.line_id];
                    return (
                      <tr key={ln.line_id}>
                        <td>{ln.name}</td>
                        <td className="num">{inr(ln.price)}</td>
                        <td className="num">{ln.found_at_exit ? "—" : pct(ln.p)}</td>
                        <td><span className={`chip ${ln.disposition}`}>{DISPOSITION[ln.disposition]}</span></td>
                        <td className="small">
                          {(ln.evidence.events ?? []).map((e) => `${e.type} @${e.t}s (${pct(e.conf)})`).join(", ")}
                          {ln.evidence.notes && <div className="muted">{ln.evidence.notes}</div>}
                          {rec && <div className="ai"><b>AI ({rec.backend}): {rec.recommendation.replace("_", " ")}</b><br />{rec.summary}</div>}
                        </td>
                        <td>
                          {ln.disposition === "staff_check" && s.status === "authorized" && !ln.found_at_exit ? (
                            <div className="row">
                              <button className={v === true ? "good" : ""} onClick={() => setVerdicts({ ...verdicts, [ln.line_id]: true })}>Taken</button>
                              <button className={v === false ? "bad" : ""} onClick={() => setVerdicts({ ...verdicts, [ln.line_id]: false })}>Not taken</button>
                            </div>
                          ) : ln.billed ? (ln.refunded ? "Refunded" : "Charged") : s.status === "authorized" ? (ln.disposition === "auto_capture" ? "Will charge" : "Won't charge") : "Not charged"}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {s.status === "authorized" && (
              <>
                <h3 style={{ marginTop: 16 }}>Items found in the bag that the cameras missed</h3>
                {found.map((f) => <div key={f.item_id} className="small">{f.name} · {inr(f.price)}</div>)}
                <div className="row" style={{ marginTop: 6 }}>
                  {hidden.filter((h) => !found.some((f) => f.item_id === h.item_id)).map((h) => (
                    <button key={h.item_id} onClick={() => setFound([...found, h])}>+ {h.name} ({inr(h.price)})</button>
                  ))}
                  {hidden.length === 0 && <span className="muted small">None for this visit.</span>}
                </div>
                <div className="row" style={{ marginTop: 16 }}>
                  <button className="primary" disabled={!ready || busy} onClick={() => run(async () => {
                    setS(await api<Session>(`/api/sessions/${s.session_id}/exit`, {
                      staff_verdicts: verdicts,
                      found: found.map((f) => ({ line_id: f.item_id, name: f.name, sku: f.sku, price: f.price, p: 0 })),
                    }));
                    api("/api/ai/agreement").then(setAgree);
                    load();
                  })}>Close visit: capture verified, release the rest</button>
                  {!ready && <span className="muted small">Decide every staff-check line first.</span>}
                </div>
              </>
            )}
          </div>

          <div className="grid2">
            <PolicyCosts s={s} />
            <TrustCard t={s.decision.trust} title="Shopper trust at entry" />
          </div>

          <div className="panel">
            <h2>PayPal calls</h2>
            <Grid
              rows={s.paypal_calls}
              height={200}
              cols={[
                { field: "op", headerName: "Operation" },
                { field: "request_id", headerName: "PayPal-Request-Id", flex: 2 },
                { field: "ok", headerName: "OK", valueFormatter: (p) => (p.value ? "yes" : "no") },
                { field: "detail", headerName: "Response", flex: 3 },
              ]}
            />
          </div>
        </>
      )}
    </>
  );
}
