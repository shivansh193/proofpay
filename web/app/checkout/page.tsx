"use client";

import { PayPalOneTimePaymentButton, PayPalProvider } from "@paypal/react-paypal-js/sdk-v6";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { PolicyCosts, TrustCard } from "@/components/Decision";
import { api, DISPOSITION, inr, pct, type Config, type Session } from "@/lib/api";

type Scenario = { scenario: string; title: string; customer_id: string };

export default function Checkout() {
  const [cfg, setCfg] = useState<Config | null>(null);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [pick, setPick] = useState("");
  const [s, setS] = useState<Session | null>(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api<Config>("/api/config").then(setCfg).catch((e) => setErr(String(e)));
    api<Scenario[]>("/api/scenarios").then((x) => { setScenarios(x); setPick(x[0]?.scenario ?? ""); });
  }, []);

  const refresh = useCallback(async (id: string) => setS(await api<Session>(`/api/sessions/${id}`)), []);

  // Wait for the staff exit check to close the session.
  useEffect(() => {
    if (!s || s.status !== "authorized") return;
    const h = setInterval(() => refresh(s.session_id).catch(() => {}), 2000);
    return () => clearInterval(h);
  }, [s, refresh]);

  const run = async (f: () => Promise<unknown>) => {
    setErr(""); setBusy(true);
    try { await f(); } catch (e) { setErr(e instanceof Error ? e.message : String(e)); } finally { setBusy(false); }
  };

  const start = () => run(async () => setS(await api<Session>("/api/sessions/from-scenario", { scenario: pick })));
  const authorize = () => run(async () => setS(await api<Session>(`/api/sessions/${s!.session_id}/authorize`, {})));

  return (
    <>
      <h1>Checkout</h1>
      <p className="lede">
        The cameras tracked what the shopper picked up. PayPal authorizes the basket now. At the exit, Proofpay
        captures only what was verified and releases the rest.
      </p>
      {err && <div className="err">{err}</div>}

      <div className="panel row">
        <select value={pick} onChange={(e) => setPick(e.target.value)} disabled={busy}>
          {scenarios.map((x) => <option key={x.scenario} value={x.scenario}>{x.title} ({x.customer_id})</option>)}
        </select>
        <button className="primary" onClick={start} disabled={busy || !pick}>Start visit</button>
        <span className="muted small">Detections are replayed from a recorded trace (vision engine: {cfg?.vision_engine ?? "…"}).</span>
      </div>

      {s && (
        <>
          <div className="panel">
            <div className="row">
              <h2 style={{ margin: 0 }}>Basket</h2>
              <span className={`chip ${s.status}`}>{s.status}</span>
              <span className="spacer" />
              <span className="muted small mono">order {s.order_id ?? "none"}</span>
            </div>
            <div className="scroll">
              <table className="t" style={{ marginTop: 10 }}>
                <thead>
                  <tr><th>Item</th><th className="num">Price</th><th className="num">Camera: taken?</th><th>At exit</th><th>Result</th><th /></tr>
                </thead>
                <tbody>
                  {s.lines.map((ln) => (
                    <tr key={ln.line_id}>
                      <td>{ln.name}{ln.found_at_exit ? <span className="chip strict" style={{ marginLeft: 6 }}>found at exit</span> : null}</td>
                      <td className="num">{inr(ln.price)}</td>
                      <td className="num">{ln.found_at_exit ? "not seen" : pct(ln.p)}</td>
                      <td><span className={`chip ${ln.disposition}`}>{DISPOSITION[ln.disposition]}</span></td>
                      <td>{s.status === "captured" || s.status === "voided" ? (ln.refunded ? "Refunded" : ln.billed ? "Charged" : "Not charged") : "—"}</td>
                      <td>{s.status === "captured" && ln.billed && !ln.refunded && !ln.found_at_exit ? <NotMine s={s} line={ln.line_id} onDone={setS} /> : null}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {s.status === "created" && cfg && (
            <div className="panel">
              <h2>Pay with PayPal</h2>
              <p className="muted small">
                Authorizes {s.authorized_amount ?? `about $${(s.decision.hold_amount / s.inr_per_usd).toFixed(2)}`} (held, not charged).
                Rupee prices are converted at a fixed demo rate of ₹{s.inr_per_usd}/USD because PayPal doesn&apos;t list INR.
              </p>
              {cfg.mode === "sandbox" && cfg.paypal_client_id ? (
                <PayPalProvider clientId={cfg.paypal_client_id} environment="sandbox" components={["paypal-payments"]} pageType="checkout">
                  <PayPalOneTimePaymentButton
                    createOrder={async () => ({ orderId: s.order_id! })}
                    onApprove={async () => { await authorize(); }}
                  />
                </PayPalProvider>
              ) : (
                <button className="primary" onClick={authorize} disabled={busy}>Approve with PayPal (offline stand-in)</button>
              )}
            </div>
          )}

          {s.status === "authorized" && (
            <div className="note">
              Authorized {s.authorized_amount} USD. Walk to the exit: the <Link href={`/staff/?s=${s.session_id}`}>staff exit screen</Link> closes the visit.
            </div>
          )}

          {(s.status === "captured" || s.status === "voided") && (
            <div className="panel">
              <h2>Receipt</h2>
              <dl className="kv">
                <dt>Authorized</dt><dd>${s.authorized_amount}</dd>
                <dt>Captured</dt><dd><b>${s.captured_amount ?? "0.00"}</b> {s.capture_id && <span className="mono muted small">({s.capture_id})</span>}</dd>
                <dt>Released</dt><dd>${(Number(s.authorized_amount) - Number(s.captured_amount ?? 0)).toFixed(2)}</dd>
                <dt>Refunded</dt><dd>${s.lines.filter((l) => l.refunded).reduce((a, l) => a + l.price_usd, 0).toFixed(2)}</dd>
              </dl>
            </div>
          )}

          <div className="grid2">
            <PolicyCosts s={s} />
            <TrustCard t={s.decision.trust} title="Shopper trust at entry" />
          </div>
        </>
      )}
    </>
  );
}

function NotMine({ s, line, onDone }: { s: Session; line: string; onDone: (s: Session) => void }) {
  const [rec, setRec] = useState<{ recommendation: string; reasoning: string; backend: string } | null>(null);
  const [busy, setBusy] = useState(false);
  if (!rec) {
    return (
      <button disabled={busy} onClick={async () => {
        setBusy(true);
        setRec(await api(`/api/sessions/${s.session_id}/lines/${line}/triage`, {}));
        setBusy(false);
      }}>Not mine</button>
    );
  }
  const decide = async (take: boolean) => {
    setBusy(true);
    onDone(await api<Session>(`/api/sessions/${s.session_id}/lines/${line}/not-mine`, { footage_shows_take: take }));
  };
  return (
    <div style={{ minWidth: 240 }}>
      <div className="ai"><b>AI triage ({rec.backend}): {rec.recommendation}</b><br />{rec.reasoning}</div>
      <div className="row small"><span className="muted">Staff:</span>
        <button className="good" disabled={busy} onClick={() => decide(false)}>Refund</button>
        <button className="bad" disabled={busy} onClick={() => decide(true)}>Footage shows take</button>
      </div>
    </div>
  );
}
