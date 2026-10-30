"use client";

import { useEffect, useState } from "react";
import { API, api, pct } from "@/lib/api";

type Row = {
  strategy: string;
  q?: number;
  loss_per_visit: number;
  staff_s_per_visit: number;
  customer_wait_s_per_visit: number;
  honest_sent_to_strict: number;
  honest_express_share: number;
  fraud_cashout_loss: number;
};
type Results = { seed: number; results: Row[]; quantile_sweep: Row[] };

const LABEL: Record<string, string> = {
  proofpay: "Proofpay (10th percentile)",
  beta_mean: "Beta mean",
  static_rules: "Static rules",
  no_trust: "No trust (all Standard)",
};

export default function Sim() {
  const [r, setR] = useState<Results | null>(null);
  const [err, setErr] = useState("");
  useEffect(() => { api<Results>("/api/sim").then(setR).catch((e) => setErr(String(e))); }, []);

  return (
    <>
      <h1>Simulator</h1>
      <p className="lede">
        500 simulated shoppers × 30 visits (honest, careless, opportunistic, fraudsters who build trust then cash out).
        Vision error rates are assumptions, not measurements. Reproduce with <code>python -m proofpay.sim --seed 0</code>.
      </p>
      {err && <div className="err">{err}</div>}
      {r && (
        <>
          <div className="panel scroll">
            <h2>Results (seed {r.seed})</h2>
            <Table rows={r.results} label={(x) => LABEL[x.strategy]} />
          </div>
          <div className="grid2">
            <div className="panel"><img className="fig" src={`${API}/eval/loss_vs_friction.png`} alt="Loss per visit against friction per visit for each strategy" /></div>
            <div className="panel"><img className="fig" src={`${API}/eval/by_archetype.png`} alt="Loss and staff time per visit by shopper archetype" /></div>
          </div>
          <div className="panel scroll">
            <h2>Where Proofpay is worse</h2>
            <p className="small">
              At the default 10th-percentile score, Proofpay sends more honest visits to Strict than the Beta mean, for almost
              the same loss. Loss is nearly flat across score quantiles while friction falls, so in this world the lower bound&apos;s
              caution mostly buys friction. Static rules have the least friction but nearly twice the loss.
            </p>
            <Table rows={r.quantile_sweep} label={(x) => `Proofpay q = ${x.q}`} />
          </div>
        </>
      )}
    </>
  );
}

function Table({ rows, label }: { rows: Row[]; label: (r: Row) => string }) {
  return (
    <table className="t">
      <thead>
        <tr>
          <th>Strategy</th><th className="num">Loss ₹/visit</th><th className="num">Staff s/visit</th><th className="num">Wait s/visit</th>
          <th className="num">Honest → Strict</th><th className="num">Honest → Express</th><th className="num">Fraud cash-out loss ₹</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((x) => (
          <tr key={label(x)}>
            <td>{label(x)}</td>
            <td className="num">{x.loss_per_visit.toFixed(1)}</td>
            <td className="num">{x.staff_s_per_visit.toFixed(1)}</td>
            <td className="num">{x.customer_wait_s_per_visit.toFixed(1)}</td>
            <td className="num">{pct(x.honest_sent_to_strict)}</td>
            <td className="num">{pct(x.honest_express_share)}</td>
            <td className="num">{x.fraud_cashout_loss.toLocaleString("en-IN")}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
