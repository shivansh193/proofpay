"use client";

import { useEffect, useState } from "react";
import { TrustCard } from "@/components/Decision";
import { Grid } from "@/components/Grid";
import { api, type Trust } from "@/lib/api";

type Subject = { subject: string; score: number; mean: number; verified_captures: number };
type Point = { t: number; score: number; mean: number; lo: number; hi: number };

export default function TrustPage() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [pick, setPick] = useState("");
  const [t, setT] = useState<Trust | null>(null);
  const [hist, setHist] = useState<Point[]>([]);
  const [seedFor, setSeedFor] = useState("asha");
  const [msg, setMsg] = useState("");

  const loadSubjects = () => api<Subject[]>("/api/subjects").then((x) => { setSubjects(x); if (!pick && x[0]) setPick(x[0].subject); });
  useEffect(() => { loadSubjects(); }, []); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (!pick) return;
    api<Trust>(`/api/trust/${encodeURIComponent(pick)}`).then(setT);
    api<Point[]>(`/api/trust/${encodeURIComponent(pick)}/history`).then(setHist);
  }, [pick]);

  const seed = async () => {
    try {
      const r = await api<Trust>("/api/demo/seed-history", { customer_id: seedFor, visits: 20, basket_inr: 200 });
      setMsg(`Added 20 simulated weekly visits for ${seedFor}.`);
      await loadSubjects();
      setPick(r.subject);
    } catch (e) { setMsg(String(e)); }
  };

  const t0 = hist[0]?.t ?? 0;
  return (
    <>
      <h1>Trust inspector</h1>
      <p className="lede">
        Every score is explained: the events behind it, how much each counted after confidence weighting, the weekly cap
        and time decay (half-life 90 days). Only payment and verification history on this platform is used.
      </p>

      <div className="panel row">
        <select value={pick} onChange={(e) => setPick(e.target.value)}>
          {subjects.map((s) => <option key={s.subject} value={s.subject}>{s.subject} · {s.score.toFixed(2)}</option>)}
        </select>
        <span className="spacer" />
        <span className="muted small">Demo:</span>
        <input value={seedFor} onChange={(e) => setSeedFor(e.target.value)} style={{ width: 120 }} />
        <button onClick={seed}>Add simulated history</button>
      </div>
      {msg && <div className="note">{msg} Simulated events are labelled <code>simulated</code> in their metadata.</div>}

      {t && (
        <>
          <div className="grid2">
            <TrustCard t={t} />
            <div className="panel">
              <h3>Score over time</h3>
              <Chart points={hist} />
              <p className="muted small">Shaded: 80% credible interval. Line: lower bound (used). Days since first event.</p>
            </div>
          </div>
          <div className="panel">
            <h2>Evidence</h2>
            <Grid
              rows={t.events}
              height={360}
              cols={[
                { field: "kind", headerName: "Event", flex: 2 },
                { field: "t", headerName: "Day", valueFormatter: (p) => (p.value - t0).toFixed(1) },
                { field: "raw", headerName: "Raw weight", valueFormatter: (p) => p.value.toFixed(2) },
                { field: "capped", headerName: "After cap", valueFormatter: (p) => p.value.toFixed(2) },
                { field: "decay", headerName: "Decay ×", valueFormatter: (p) => p.value.toFixed(2) },
                { field: "alpha", headerName: "+α", valueFormatter: (p) => p.value.toFixed(2) },
                { field: "beta", headerName: "+β", valueFormatter: (p) => p.value.toFixed(2) },
                { field: "note", headerName: "Note", flex: 2 },
              ]}
            />
          </div>
        </>
      )}
      {!t && <div className="panel muted">No subjects yet. Complete a checkout or add simulated history.</div>}
    </>
  );
}

function Chart({ points }: { points: Point[] }) {
  if (points.length < 2) return <div className="muted small">Not enough history to plot.</div>;
  const W = 520, H = 180, P = 28;
  const t0 = points[0].t, t1 = points[points.length - 1].t || t0 + 1;
  const x = (t: number) => P + ((t - t0) / Math.max(1e-9, t1 - t0)) * (W - 2 * P);
  const y = (v: number) => H - P + -v * (H - 2 * P);
  const band = points.map((p) => `${x(p.t)},${y(p.hi)}`).join(" ") + " " + [...points].reverse().map((p) => `${x(p.t)},${y(p.lo)}`).join(" ");
  const line = points.map((p) => `${x(p.t)},${y(p.score)}`).join(" ");
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%", height: "auto" }} role="img" aria-label="Trust score over time">
      {[0, 0.5, 1].map((v) => (
        <g key={v}>
          <line x1={P} x2={W - P} y1={y(v)} y2={y(v)} stroke="var(--line)" />
          <text x={4} y={y(v) + 4} fontSize="10" fill="var(--muted)">{v}</text>
        </g>
      ))}
      <polygon points={band} fill="var(--accent)" opacity="0.15" />
      <polyline points={line} fill="none" stroke="var(--accent)" strokeWidth="2" />
      <text x={W - P} y={H - 6} fontSize="10" fill="var(--muted)" textAnchor="end">{(t1 - t0).toFixed(0)} days</text>
    </svg>
  );
}
