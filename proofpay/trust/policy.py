"""Pick the checkout policy with the lowest expected cost, and size the agent's spend limit.

cost(policy) = expected loss + friction cost

Expected loss has three parts:
  * uncertain lines nobody checks:   sum(p_i * price_i)       (taken, never billed)
  * items hidden from the cameras:   d * concealment * basket * (1 - catch_rate)
  * auto-captured false positives:   sum((1 - p_i) * (price_i + wrong_charge_cost))
where d = 1 - trust score is the chance this shopper is dishonest.

Rule 7: trust never makes a line billable. Only lines with p >= bill_threshold
can be captured without a human, and trust may only lower the auto-capture
bar within [auto_capture_min, auto_capture_max], both above bill_threshold.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from .config import DEFAULT, TrustConfig
from .reputation import Reputation

POLICIES = ("express", "standard", "strict")


@dataclass(frozen=True)
class Line:
    line_id: str
    name: str
    price: float
    p: float  # vision probability that the item left with the customer


@dataclass(frozen=True)
class PolicyCost:
    policy: str
    unchecked_loss: float
    concealment_loss: float
    wrong_charge_loss: float
    staff_seconds: float
    customer_seconds: float
    friction_cost: float
    total: float
    allowed: bool
    dispositions: dict[str, str]  # line_id -> auto_capture | staff_check | release


@dataclass(frozen=True)
class Decision:
    policy: str
    score: float
    hold_amount: float
    costs: dict[str, PolicyCost]
    reasons: tuple[str, ...]
    dispositions: dict[str, str] = field(default_factory=dict)

    def explain(self) -> dict:
        return {
            "policy": self.policy,
            "score": self.score,
            "hold_amount": self.hold_amount,
            "reasons": list(self.reasons),
            "costs": {k: v.__dict__ for k, v in self.costs.items()},
        }


def auto_capture_threshold(score: float, cfg: TrustConfig = DEFAULT) -> float:
    """Vision bar for skipping the human on a billable line. Higher trust, lower bar."""
    s = min(1.0, max(0.0, score))
    t = cfg.auto_capture_max - (cfg.auto_capture_max - cfg.auto_capture_min) * s
    return max(t, cfg.bill_threshold)


def _dispositions(policy: str, lines: Sequence[Line], score: float, cfg: TrustConfig) -> dict[str, str]:
    out: dict[str, str] = {}
    bar = auto_capture_threshold(score, cfg) if policy == "express" else cfg.auto_capture_max
    for ln in lines:
        if ln.p < cfg.ignore_threshold:
            out[ln.line_id] = "release"
        elif ln.p < cfg.bill_threshold:
            # Uncertain: only a human can make it billable. Express skips the check.
            out[ln.line_id] = "release" if policy == "express" else "staff_check"
        else:
            out[ln.line_id] = "auto_capture" if ln.p >= bar else "staff_check"
    if policy == "strict":
        auto_value = sum(ln.price for ln in lines if out[ln.line_id] == "auto_capture")
        if auto_value > cfg.strict_auto_capture_cap:
            out = {k: ("staff_check" if v == "auto_capture" else v) for k, v in out.items()}
    return out


def evaluate(policy: str, lines: Sequence[Line], score: float, cfg: TrustConfig = DEFAULT) -> PolicyCost:
    """Expected cost and line dispositions of one policy, ignoring anti-gaming blocks."""
    disp = _dispositions(policy, lines, score, cfg)
    basket = sum(ln.price for ln in lines if ln.p >= cfg.ignore_threshold)
    d = 1.0 - score
    unchecked = sum(
        ln.p * ln.price
        for ln in lines
        if disp[ln.line_id] == "release" and ln.p >= cfg.ignore_threshold
    )
    concealed = d * cfg.concealment_ratio * basket * (1.0 - cfg.catch_rate[policy])
    wrong = sum(
        (1.0 - ln.p) * (ln.price + cfg.wrong_charge_cost)
        for ln in lines
        if disp[ln.line_id] == "auto_capture"
    )
    checked = sum(1 for v in disp.values() if v == "staff_check")
    staff = cfg.staff_seconds_base[policy] + cfg.staff_seconds_per_line * checked
    customer = cfg.customer_seconds_base + staff
    friction = cfg.rupees_per_second * (staff + cfg.customer_time_weight * customer)
    return PolicyCost(
        policy, unchecked, concealed, wrong, staff, customer, friction,
        unchecked + concealed + wrong + friction, True, disp,
    )


def choose_policy(
    lines: Sequence[Line],
    rep: Reputation,
    cfg: TrustConfig = DEFAULT,
    score: float | None = None,
) -> Decision:
    """Cheapest allowed policy for this basket. `score` overrides rep.score (for baselines)."""
    s = rep.score if score is None else score
    basket = sum(ln.price for ln in lines if ln.p >= cfg.ignore_threshold)
    reasons: list[str] = [f"trust score {s:.2f} (P(dishonest) taken as {1 - s:.2f})"]
    costs = {p: evaluate(p, lines, s, cfg) for p in POLICIES}

    blocked: set[str] = set()
    is_new = rep.verified_captures < cfg.new_subject_captures
    if is_new:
        auto = sum(
            ln.price for ln in lines if costs["express"].dispositions[ln.line_id] == "auto_capture"
        )
        if auto > cfg.new_subject_auto_capture_cap:
            blocked.add("express")
            reasons.append(
                f"new subject ({rep.verified_captures} verified visits): auto-capture "
                f"₹{auto:.0f} exceeds the ₹{cfg.new_subject_auto_capture_cap:.0f} cap"
            )
    if rep.median_basket and basket > cfg.value_at_risk_multiple * rep.median_basket:
        blocked.add("express")
        reasons.append(
            f"basket ₹{basket:.0f} is over {cfg.value_at_risk_multiple:g}x the usual "
            f"₹{rep.median_basket:.0f}: checks stepped up"
        )
    for p in blocked:
        costs[p] = PolicyCost(**{**costs[p].__dict__, "allowed": False})

    chosen = min((c for c in costs.values() if c.allowed), key=lambda c: c.total)
    reasons.append(
        f"{chosen.policy} has the lowest expected cost (₹{chosen.total:.0f}); "
        + ", ".join(f"{c.policy} ₹{c.total:.0f}" for c in costs.values() if c is not chosen)
    )
    hold = sum(
        ln.price for ln in lines if chosen.dispositions[ln.line_id] != "release"
    )
    if chosen.policy == "strict":
        # Hold enough to bill untracked items the exit check finds.
        hold = round(basket * (1.0 + cfg.strict_hold_buffer), 2)
    return Decision(chosen.policy, s, round(hold, 2), costs, tuple(reasons), chosen.dispositions)


@dataclass(frozen=True)
class AgentDecision:
    verdict: str  # allow | ask_human | deny
    limit: float
    score: float
    reasons: tuple[str, ...]


def agent_limit(score: float, cfg: TrustConfig = DEFAULT) -> float:
    z = cfg.agent_score_zero
    headroom = max(0.0, (score - z) / (1.0 - z))
    return cfg.agent_floor_limit + (cfg.agent_max_limit - cfg.agent_floor_limit) * headroom


def authorize_agent_spend(rep: Reputation, amount: float, cfg: TrustConfig = DEFAULT) -> AgentDecision:
    """Gate one agent purchase. The limit grows only as the lower bound rises."""
    limit = round(agent_limit(rep.score, cfg), 2)
    why = [f"agent trust score {rep.score:.2f} gives a limit of ₹{limit:.0f}"]
    if amount <= limit:
        return AgentDecision("allow", limit, rep.score, tuple(why + [f"₹{amount:.0f} is within the limit"]))
    if amount <= cfg.agent_ask_multiple * limit:
        return AgentDecision(
            "ask_human", limit, rep.score, tuple(why + [f"₹{amount:.0f} is over the limit: ask the human"])
        )
    return AgentDecision(
        "deny", limit, rep.score,
        tuple(why + [f"₹{amount:.0f} is over {cfg.agent_ask_multiple:g}x the limit"]),
    )
