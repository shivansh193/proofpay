"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { api, type Config } from "@/lib/api";

const TABS = [
  ["/checkout/", "Checkout"],
  ["/staff/", "Staff exit"],
  ["/trust/", "Trust inspector"],
  ["/agent/", "Agent"],
  ["/sim/", "Simulator"],
];

export function Nav() {
  const path = usePathname();
  const [cfg, setCfg] = useState<Config | null>(null);
  useEffect(() => {
    api<Config>("/api/config").then(setCfg).catch(() => setCfg(null));
  }, []);
  return (
    <nav className="nav">
      <Link href="/" className="brand">Proofpay</Link>
      {TABS.map(([href, label]) => (
        <Link key={href} href={href} className={`tab ${path === href ? "on" : ""}`}>{label}</Link>
      ))}
      {cfg && (
        <span className="mode muted">
          PayPal: <span className={`chip ${cfg.mode === "sandbox" ? "allow" : "standard"}`}>{cfg.mode === "sandbox" ? "sandbox" : "offline stand-in"}</span>{" "}
          AI: <span className="chip">{cfg.ai_backend}</span>
        </span>
      )}
    </nav>
  );
}
