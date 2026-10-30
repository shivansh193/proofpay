"""python -m proofpay.sim --seed 0  ->  docs/eval/{results.json, results.md, *.png}"""

from __future__ import annotations

import argparse
import json
import statistics
from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from proofpay.trust import DEFAULT  # noqa: E402

from .run import STRATEGIES, Result, run_strategy  # noqa: E402
from .world import WorldConfig, build_world  # noqa: E402

SWEEP_QUANTILES = (0.02, 0.05, 0.1, 0.2, 0.35, 0.5)

LABELS = {
    "proofpay": "Proofpay (lower bound)",
    "beta_mean": "Beta mean",
    "static_rules": "Static rules",
    "no_trust": "No trust (all Standard)",
}


def summarise(r: Result) -> dict:
    t = r.total()
    honest = r.by_archetype["honest"]
    delays = [d for d in r.fraud_catch_delay.values() if d is not None]
    per_arch = {
        a: {
            "loss_per_visit": x.loss / x.visits,
            "staff_s_per_visit": x.staff_seconds / x.visits,
            "strict_share": x.strict_visits / x.visits,
            "express_share": x.express_visits / x.visits,
        }
        for a, x in sorted(r.by_archetype.items())
    }
    return {
        "strategy": r.strategy,
        "visits": t.visits,
        "loss_total": round(t.loss, 0),
        "loss_per_visit": t.loss / t.visits,
        "staff_minutes": t.staff_seconds / 60,
        "staff_s_per_visit": t.staff_seconds / t.visits,
        "customer_wait_s_per_visit": t.customer_seconds / t.visits,
        "honest_sent_to_strict": honest.strict_visits / honest.visits,
        "honest_express_share": honest.express_visits / honest.visits,
        "unrefunded_wrong_charges": t.unrefunded_wrong_charges,
        "fraud_cashout_loss": round(r.fraud_cashout_loss, 0),
        "fraudsters_caught": f"{len(delays)}/{len(r.fraud_catch_delay)}",
        "fraud_median_visits_to_catch": statistics.median(delays) if delays else None,
        "by_archetype": per_arch,
    }


def plot(rows: list[dict], sweep: list[tuple[float, dict]], out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    xs = [r["staff_s_per_visit"] + r["customer_wait_s_per_visit"] for _, r in sweep]
    ys = [r["loss_per_visit"] for _, r in sweep]
    ax.plot(xs, ys, "-", color="grey", alpha=0.5, zorder=0)
    for (q, _), x, y in zip(sweep, xs, ys):
        ax.annotate(f"q={q:g}", (x, y), textcoords="offset points", xytext=(-10, -12), fontsize=7, color="grey")
    for r in rows:
        x = r["staff_s_per_visit"] + r["customer_wait_s_per_visit"]
        y = r["loss_per_visit"]
        ax.scatter(x, y, s=70)
        ax.annotate(LABELS[r["strategy"]], (x, y), textcoords="offset points", xytext=(8, 4), fontsize=9)
    ax.set_xlabel("Friction per visit (staff + customer seconds)")
    ax.set_ylabel("Loss per visit (₹)")
    ax.set_title("Loss vs friction (lower-left is better)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out / "loss_vs_friction.png", dpi=150)
    plt.close(fig)

    archs = list(rows[0]["by_archetype"])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    width = 0.8 / len(rows)
    for k, r in enumerate(rows):
        xs = [i + k * width for i in range(len(archs))]
        axes[0].bar(xs, [r["by_archetype"][a]["loss_per_visit"] for a in archs], width, label=LABELS[r["strategy"]])
        axes[1].bar(xs, [r["by_archetype"][a]["staff_s_per_visit"] for a in archs], width)
    for ax, title in zip(axes, ("Loss per visit (₹)", "Staff seconds per visit")):
        ax.set_xticks([i + 0.4 - width / 2 for i in range(len(archs))], archs)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.3)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "by_archetype.png", dpi=150)
    plt.close(fig)


def table(rows: list[dict], label=lambda r: LABELS[r["strategy"]]) -> str:
    cols = [
        ("Strategy", label),
        ("Loss ₹/visit", lambda r: f"{r['loss_per_visit']:.1f}"),
        ("Staff s/visit", lambda r: f"{r['staff_s_per_visit']:.1f}"),
        ("Wait s/visit", lambda r: f"{r['customer_wait_s_per_visit']:.1f}"),
        ("Honest → Strict", lambda r: f"{100 * r['honest_sent_to_strict']:.1f}%"),
        ("Honest → Express", lambda r: f"{100 * r['honest_express_share']:.1f}%"),
        ("Fraud cash-out loss ₹", lambda r: f"{r['fraud_cashout_loss']:.0f}"),
        ("Fraudsters caught", lambda r: r["fraudsters_caught"]),
        ("Median visits to catch", lambda r: str(r["fraud_median_visits_to_catch"])),
    ]
    head = "| " + " | ".join(c for c, _ in cols) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "".join("| " + " | ".join(f(r) for _, f in cols) + " |\n" for r in rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="docs/eval")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    w = WorldConfig()
    world = build_world(args.seed, w)
    rows = [summarise(run_strategy(name, world, w)) for name in STRATEGIES]
    # Proofpay at other credible-bound quantiles: the loss/friction frontier.
    sweep = [
        (q, summarise(run_strategy("proofpay", world, w, replace(DEFAULT, score_quantile=q))))
        for q in SWEEP_QUANTILES
    ]
    (out / "results.json").write_text(
        json.dumps(
            {"seed": args.seed, "world": w.__dict__, "results": rows,
             "quantile_sweep": [{"q": q, **r} for q, r in sweep]},
            indent=1, default=str,
        )
    )
    md = (
        f"Seed {args.seed}, {len(world)} shoppers, {rows[0]['visits']} visits.\n\n"
        + table(rows)
        + "\nProofpay at other score quantiles (q = 0.5 is roughly the median):\n\n"
        + table([{**r, "q": q} for q, r in sweep], label=lambda r: f"Proofpay q = {r['q']:g}")
    )
    (out / "results.md").write_text(md, encoding="utf-8")
    plot(rows, sweep, out)
    print(md)


if __name__ == "__main__":
    main()
