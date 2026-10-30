import { inr, pct, type Session, type Trust } from "@/lib/api";

export function PolicyCosts({ s }: { s: Session }) {
  const d = s.decision;
  return (
    <div className="panel">
      <div className="row">
        <h2 style={{ margin: 0 }}>Policy: <span className={`chip ${d.policy}`}>{d.policy}</span></h2>
        <span className="spacer" />
        <span className="muted small">Hold {inr(d.hold_amount)} (≈ ${(d.hold_amount / s.inr_per_usd).toFixed(2)})</span>
      </div>
      <p className="muted small" style={{ marginTop: 8 }}>
        Expected cost of each policy for this basket. The cheapest allowed one is chosen.
      </p>
      <div className="scroll">
        <table className="t">
          <thead>
            <tr>
              <th>Policy</th>
              <th className="num">Unchecked items</th>
              <th className="num">Hidden items</th>
              <th className="num">Wrong charges</th>
              <th className="num">Staff s</th>
              <th className="num">Friction</th>
              <th className="num">Total</th>
            </tr>
          </thead>
          <tbody>
            {Object.values(d.costs).map((c) => (
              <tr key={c.policy} className={c.policy === d.policy ? "chosen" : c.allowed ? "" : "blocked"}>
                <td><span className={`chip ${c.policy}`}>{c.policy}</span>{!c.allowed && " blocked"}</td>
                <td className="num">{inr(c.unchecked_loss)}</td>
                <td className="num">{inr(c.concealment_loss)}</td>
                <td className="num">{inr(c.wrong_charge_loss)}</td>
                <td className="num">{c.staff_seconds.toFixed(0)}</td>
                <td className="num">{inr(c.friction_cost)}</td>
                <td className="num"><b>{inr(c.total)}</b></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <h3 style={{ marginTop: 14 }}>Why</h3>
      <ul className="reasons small">{d.reasons.map((r) => <li key={r}>{r}</li>)}</ul>
    </div>
  );
}

export function TrustCard({ t, title = "Trust" }: { t: Trust; title?: string }) {
  const [lo, hi] = t.interval;
  return (
    <div className="panel">
      <h3>{title}</h3>
      <div className="row">
        <div className="score">{t.score.toFixed(2)}</div>
        <div className="muted small">
          lower bound used for decisions<br />mean {t.mean.toFixed(2)}, 80% interval {lo.toFixed(2)}–{hi.toFixed(2)}
        </div>
      </div>
      <div className="bar" style={{ margin: "10px 0" }} title="80% credible interval; tick = mean">
        <span style={{ left: pct(lo), width: pct(hi - lo), opacity: 0.35 }} />
        <span style={{ left: pct(t.score), width: 3 }} />
      </div>
      <dl className="kv">
        <dt>Subject</dt><dd className="mono">{t.subject}</dd>
        <dt>Verified visits</dt><dd>{t.verified_captures}</dd>
        <dt>Usual basket</dt><dd>{t.median_basket ? inr(t.median_basket) : "no history"}</dd>
        <dt>Beta</dt><dd className="mono">α {t.alpha.toFixed(2)}, β {t.beta.toFixed(2)} (prior {t.prior.alpha0.toFixed(1)}, {t.prior.beta0.toFixed(1)})</dd>
      </dl>
    </div>
  );
}
