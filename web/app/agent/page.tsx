"use client";

import { useCallback, useEffect, useState } from "react";
import { TrustCard } from "@/components/Decision";
import { api, inr, type Trust } from "@/lib/api";

type Purchase = {
  purchase_id: string;
  items: { lines: { sku: string; name: string; price: number; qty: number; price_usd?: number; retailer?: string; url?: string }[]; task: string };
  amount: number;
  verdict: "allow" | "ask_human" | "deny";
  status: string;
  outcome: string | null;
  reasons: string[];
  order_id: string | null;
  capture_id: string | null;
};
type Status = { agent_id: string; limit: number; trust: Trust; purchases: Purchase[] };
type PlanItem = { sku: string; qty: number; name?: string; price_usd?: number; retailer?: string; url?: string; image?: string; brand?: string; query?: string };
type Plan = { items: PlanItem[]; rationale: string; planner: string; catalog?: string };

const AGENT = "restock-agent";

export default function AgentPage() {
  const [st, setSt] = useState<Status | null>(null);
  const [task, setTask] = useState("Restock bags, receipt rolls and cleaning supplies for next week.");
  const [plan, setPlan] = useState<Plan | null>(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => setSt(await api<Status>(`/api/agents/${AGENT}`)), []);
  useEffect(() => { load(); }, [load]);

  const run = async (f: () => Promise<unknown>) => {
    setErr(""); setBusy(true);
    try { await f(); await load(); } catch (e) { setErr(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };

  return (
    <>
      <h1>Agent console</h1>
      <p className="lede">
        An AI shopping agent finds real products through Channel3 and buys them through PayPal. Witnessed gates every
        payment: within the limit it goes ahead, up to 3× the limit it asks you, above that it refuses. Like the store exit,
        PayPal only <b>holds</b> the money; it is captured when you confirm the delivery, and voided if you send it back.
        The limit grows only as the agent&apos;s purchases turn out right.
      </p>
      {err && <div className="err">{err}</div>}

      <div className="grid2">
        <div className="panel">
          <h2>Task</h2>
          <textarea rows={3} value={task} onChange={(e) => setTask(e.target.value)} />
          <div className="row" style={{ marginTop: 8 }}>
            <button disabled={busy} onClick={() => run(async () => setPlan(await api<Plan>(`/api/agents/${AGENT}/plan`, { task })))}>Plan purchase</button>
            {plan && (
              <button className="primary" disabled={busy || !plan.items.length} onClick={() => run(async () => {
                await api(`/api/agents/${AGENT}/purchases`, { items: plan.items, task });
                setPlan(null);
              })}>Ask to pay</button>
            )}
          </div>
          {plan && (
            <div className="ai" style={{ marginTop: 10 }}>
              <b>Plan</b> <span className="small muted">(planner: {plan.planner}; products: {plan.catalog ?? "demo catalog"})</span>
              <ul className="small" style={{ margin: "6px 0" }}>
                {plan.items.map((i) => (
                  <li key={i.sku}>
                    {i.image && <img src={i.image} alt="" width={36} height={36} style={{ objectFit: "contain", verticalAlign: "middle", marginRight: 6, background: "#fff", borderRadius: 4 }} />}
                    {i.qty} × {i.name ?? i.sku}
                    {i.price_usd != null && <> — ${i.price_usd.toFixed(2)} at {i.url ? <a href={i.url} target="_blank" rel="noreferrer">{i.retailer}</a> : i.retailer}</>}
                    {i.query && <span className="muted"> (searched &ldquo;{i.query}&rdquo;)</span>}
                  </li>
                ))}
              </ul>
              {plan.rationale}
              {plan.catalog === "channel3" && <div className="small muted">Prices are real Channel3 offers. The payment is a PayPal sandbox payment to Witnessed&apos;s test merchant; nothing is ordered from the retailer.</div>}
            </div>
          )}
          <h3 style={{ marginTop: 16 }}>Quick requests (for the demo)</h3>
          <div className="row">
            {[["SUP-RCPT-10", 1, "small"], ["SUP-BULB-4", 1, "over limit"], ["SUP-FRIDGE", 1, "far over"]].map(([sku, qty, label]) => (
              <button key={sku as string} disabled={busy} onClick={() => run(() => api(`/api/agents/${AGENT}/purchases`, { items: [{ sku, qty }], task: label }))}>
                {sku} ({label})
              </button>
            ))}
          </div>
        </div>
        <div>
          {st && (
            <div className="panel">
              <h3>Spending limit</h3>
              <div className="score">{inr(st.limit)}</div>
              <p className="muted small">Asks a human up to {inr(st.limit * 3)}; refuses above.</p>
            </div>
          )}
          {st && <TrustCard t={st.trust} title="Agent trust" />}
        </div>
      </div>

      <div className="panel">
        <h2>Purchases</h2>
        <div className="scroll">
          <table className="t">
            <thead><tr><th>Items</th><th className="num">Amount</th><th>Guard</th><th>Status</th><th>Why</th><th /></tr></thead>
            <tbody>
              {st?.purchases.map((p) => (
                <tr key={p.purchase_id}>
                  <td>{p.items.lines.map((l) => `${l.qty} × ${l.name}`).join(", ")}</td>
                  <td className="num">{inr(p.amount)}{p.items.lines.some((l) => l.price_usd != null) && <div className="small muted">${p.items.lines.reduce((a, l) => a + (l.price_usd ?? 0) * l.qty, 0).toFixed(2)}</div>}</td>
                  <td><span className={`chip ${p.verdict}`}>{p.verdict.replace("_", " ")}</span></td>
                  <td><span className={`chip ${p.status}`}>{p.status.replace("_", " ")}</span>{p.outcome && <div className="small muted">{p.outcome}</div>}</td>
                  <td className="small">{p.reasons.join(". ")}</td>
                  <td>
                    {p.status === "pending_approval" && (
                      <div className="row">
                        <button className="good" disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/decide`, { approve: true }))}>Approve</button>
                        <button className="bad" disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/decide`, { approve: false }))}>Reject</button>
                      </div>
                    )}
                    {p.status === "awaiting_payer" && (
                      <div className="row">
                        {p.order_id && <a className="btn" href={`https://www.sandbox.paypal.com/checkoutnow?token=${p.order_id}`} target="_blank" rel="noreferrer">Approve in PayPal</a>}
                        <button disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/complete`, {}))}>Approved: place hold</button>
                      </div>
                    )}
                    {(p.status === "held" || p.status === "paid") && !p.outcome && (
                      <div className="row">
                        <button className="good" disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/outcome`, { outcome: "ok" }))}>{p.status === "held" ? "Delivered: capture" : "Correct"}</button>
                        <button className="bad" disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/outcome`, { outcome: "returned" }))}>{p.status === "held" ? "Sent back: void" : "Returned"}</button>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!st?.purchases.length && <p className="muted small">No purchases yet.</p>}
        </div>
      </div>
    </>
  );
}
