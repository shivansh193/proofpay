// Same origin in production (FastAPI serves the export); set NEXT_PUBLIC_API_BASE for `next dev`.
export const API = process.env.NEXT_PUBLIC_API_BASE ?? "";

export async function api<T = any>(path: string, body?: unknown): Promise<T> {
  const r = await fetch(`${API}${path}`, {
    method: body === undefined ? "GET" : "POST",
    headers: body === undefined ? undefined : { "content-type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail ?? j));
  return j as T;
}

export type Line = {
  line_id: string;
  name: string;
  sku: string;
  price: number;
  price_usd: number;
  p: number;
  disposition: "auto_capture" | "staff_check" | "release";
  staff_verdict: number | null;
  billed: number;
  refunded: number;
  found_at_exit: number;
  evidence: { events?: { t: number; type: string; conf: number }[]; notes?: string };
};

export type PolicyCost = {
  policy: string;
  unchecked_loss: number;
  concealment_loss: number;
  wrong_charge_loss: number;
  staff_seconds: number;
  customer_seconds: number;
  friction_cost: number;
  total: number;
  allowed: boolean;
};

export type Trust = {
  subject: string;
  alpha: number;
  beta: number;
  mean: number;
  score: number;
  interval: [number, number];
  verified_captures: number;
  median_basket: number | null;
  prior: { alpha0: number; beta0: number };
  events: { kind: string; t: number; raw: number; capped: number; decay: number; alpha: number; beta: number; note: string }[];
};

export type Session = {
  session_id: string;
  customer_id: string;
  subject: string;
  status: string;
  policy: string;
  order_id: string | null;
  authorization_id: string | null;
  authorized_amount: string | null;
  capture_id: string | null;
  captured_amount: string | null;
  created_t: number;
  decision: { policy: string; score: number; hold_amount: number; reasons: string[]; costs: Record<string, PolicyCost>; trust: Trust };
  lines: Line[];
  paypal_calls: { op: string; request_id: string; ok: number; detail: string; t: number }[];
  inr_per_usd: number;
  ai?: { line_id: string; kind: string; recommendation: string; summary: string; backend: string; staff_decision: string | null }[];
  scenario?: { title: string; hidden: { item_id: string; name: string; sku: string; price: number; notes?: string }[] };
};

export type Config = { mode: "offline" | "sandbox"; paypal_client_id: string; currency: string; inr_per_usd: number; vision_engine: string; ai_backend: string };

export const inr = (v: number) => `₹${v.toLocaleString("en-IN", { maximumFractionDigits: 0 })}`;
export const pct = (v: number) => `${(v * 100).toFixed(v > 0.99 && v < 1 ? 1 : 0)}%`;
export const DISPOSITION: Record<string, string> = {
  auto_capture: "Auto-capture",
  staff_check: "Staff check",
  release: "Released",
};
