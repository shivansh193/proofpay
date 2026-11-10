"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { api } from "@/lib/api";

type Line = {
  line_id: string; item: string; sku: string; price_usd: number; camera_p_taken: number;
  camera_events: { t: number; type: string; conf: number }[]; camera_note: string | null;
  charged: boolean; basis: string; refunded: boolean;
};
type Record_ = {
  record: string; session_id: string; payer: string; policy: string; sha256: string; lines: Line[];
  paypal: { order_id: string; authorization_id: string; authorized: string; capture_id: string | null; captured: string | null; status: string };
  paypal_calls: { op: string; request_id: string; ok: number; t: number }[];
};

export default function EvidencePage() {
  return <Suspense><Evidence /></Suspense>;
}

function Evidence() {
  const sid = useSearchParams().get("s");
  const [r, setR] = useState<Record_ | null>(null);
  const [err, setErr] = useState("");
  useEffect(() => {
    if (sid) api<Record_>(`/api/sessions/${sid}/evidence`).then(setR).catch((e) => setErr(String(e)));
  }, [sid]);

  if (!sid) return <p>Open this page from a receipt, or from the link in the PayPal capture note.</p>;
  if (err) return <p className="error">{err}</p>;
  if (!r) return <p className="muted">Loading…</p>;
  return (
    <>
      <h1>Handover evidence</h1>
      <p className="lede">
        A shipped parcel has a tracking number. This record is the in-person equivalent: for every item in the visit,
        what the camera saw, who decided, and what PayPal charged. The PayPal capture&apos;s note links here.
      </p>
      <div className="panel">
        <dl className="kv small">
          <dt>Visit</dt><dd className="mono">{r.session_id}</dd>
          <dt>PayPal order</dt><dd className="mono">{r.paypal.order_id}</dd>
          <dt>Authorization</dt><dd className="mono">{r.paypal.authorization_id} (${r.paypal.authorized} held)</dd>
          <dt>Capture</dt><dd className="mono">{r.paypal.capture_id ?? "none"} {r.paypal.captured ? `($${r.paypal.captured} charged)` : ""}</dd>
          <dt>Status</dt><dd>{r.paypal.status}</dd>
          <dt>Exit policy</dt><dd>{r.policy}</dd>
          <dt>SHA-256</dt><dd className="mono small">{r.sha256}</dd>
        </dl>
      </div>
      <div className="panel">
        <h2>Items</h2>
        <table className="small">
          <thead><tr><th>Item</th><th>$</th><th>Camera</th><th>What the camera saw</th><th>Charged?</th><th>Why</th></tr></thead>
          <tbody>
            {r.lines.map((ln) => (
              <tr key={ln.line_id}>
                <td>{ln.item}</td>
                <td>{ln.price_usd.toFixed(2)}</td>
                <td>{(ln.camera_p_taken * 100).toFixed(1)}%</td>
                <td>
                  {ln.camera_events.map((e) => `${e.type} @${e.t}s (${Math.round(e.conf * 100)}%)`).join(", ")}
                  {ln.camera_note && <div className="muted">{ln.camera_note}</div>}
                </td>
                <td>{ln.charged ? (ln.refunded ? "charged, refunded" : "yes") : "no"}</td>
                <td>{ln.basis}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="small muted">
        Raw JSON: <a href={`/api/sessions/${r.session_id}/evidence`}>/api/sessions/{r.session_id}/evidence</a>.{" "}
        Back to the <Link href={`/checkout/?s=${r.session_id}`}>receipt</Link>.
      </p>
    </>
  );
}
