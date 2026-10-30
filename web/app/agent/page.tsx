"use client";

import { useCallback, useEffect, useState } from "react";
import { TrustCard } from "@/components/Decision";
import { api, inr, type Trust } from "@/lib/api";

type Purchase = {
  purchase_id: string;
  items: { lines: { sku: string; name: string; price: number; qty: number }[]; task: string };
  amount: number;
  verdict: "allow" | "ask_human" | "deny";
  status: string;
  outcome: string | null;
  reasons: string[];
  order_id: string | null;
  capture_id: string | null;
};
type Status = { agent_id: string; limit: number; trust: Trust; purchases: Purchase[] };
type Plan = { items: { sku: string; qty: number }[]; rationale: string; planner: string };

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
        A purchasing agent buys supplies through PayPal. Proofpay gates every payment: within the limit it pays,
        up to 3× the limit it asks you, above that it refuses. The limit grows only as the agent&apos;s purchases turn out right.
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
              <b>Plan ({plan.planner})</b>: {plan.items.map((i) => `${i.qty} × ${i.sku}`).join(", ")}<br />{plan.rationale}
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
                  <td className="num">{inr(p.amount)}</td>
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
                      <button disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/complete`, {}))}>Payer approved: complete</button>
                    )}
                    {p.status === "paid" && !p.outcome && (
                      <div className="row">
                        <button className="good" disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/outcome`, { outcome: "ok" }))}>Correct</button>
                        <button className="bad" disabled={busy} onClick={() => run(() => api(`/api/agents/purchases/${p.purchase_id}/outcome`, { outcome: "returned" }))}>Returned</button>
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
