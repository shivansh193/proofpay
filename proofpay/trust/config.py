"""Every tunable number in the trust engine, with the reason for its default.

Money is in rupees. Time is in days (event timestamps are float days) except
friction, which is in seconds and converted to rupees with `rupees_per_second`.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TrustConfig:
    # --- Evidence weighting -------------------------------------------------
    # A verified capture adds f(p) to alpha, f(p) = clip((p - p0) / (1 - p0), 0, 1).
    # p0 = 0.5 means a coin-flip detection proves nothing; p = 0.98 adds 0.96,
    # p = 0.7 adds 0.4. Monotone, so uncertain captures can't build much trust.
    confidence_floor: float = 0.5

    # Negative evidence, added to beta. Ordered by how strongly each event
    # points at the customer rather than at noise.
    severity: dict[str, float] = field(
        default_factory=lambda: {
            # Footage shows the take after a "Not mine": a deliberate false claim.
            "line_disputed_rejected": 3.0,
            # Staff found an item the cameras never billed. Could be forgetful,
            # so below a chargeback, but above a rejected dispute because it is
            # the exact behaviour Express skips checking for.
            "exit_mismatch": 5.0,
            # A dispute opened with PayPal. Often legitimate, so mild on its own.
            "dispute_opened": 2.0,
            # A chargeback the merchant lost: strongest signal we get.
            "chargeback": 10.0,
            # Agent client: the human returned or overrode the purchase.
            "agent_purchase_returned": 1.0,
            "agent_purchase_overridden": 2.0,
        }
    )
    # Positive evidence per event kind, other than capture_verified (which uses f(p)).
    positive: dict[str, float] = field(
        default_factory=lambda: {"agent_purchase_ok": 1.0}
    )
    # Recorded but not scored against the subject. An upheld "Not mine" is the
    # vision system's error, and a refund on its own says nothing.
    neutral: frozenset[str] = frozenset({"line_disputed_upheld", "refund"})

    # --- Time decay ---------------------------------------------------------
    # Event weight halves every `half_life_days`. 90 days is about a quarter of
    # shopping habits, so a mistake from last year barely counts.
    half_life_days: float = 90.0

    # --- Anti-gaming --------------------------------------------------------
    # At most this much positive evidence per 7-day window, so fifty tiny
    # baskets in a week earn no more than three honest weekly shops.
    max_positive_per_week: float = 3.0
    # A basket above this multiple of the subject's median past basket steps
    # the policy up one level, whatever the score.
    value_at_risk_multiple: float = 3.0
    # Subjects with fewer than this many verified captures are "new".
    new_subject_captures: int = 3
    # New subjects can't auto-capture more than this in one basket.
    new_subject_auto_capture_cap: float = 500.0

    # --- Prior and score ----------------------------------------------------
    # Fallback prior when there's no cohort to fit: mean 0.67, strength 3.
    default_prior: tuple[float, float] = (2.0, 1.0)
    # Fitted prior strength (alpha0 + beta0) is clamped to this range. The upper
    # bound keeps a new subject uncertain even in a very honest cohort.
    prior_strength_range: tuple[float, float] = (2.0, 6.0)
    # And its mean is capped, so a cohort can never make strangers look trusted.
    prior_mean_cap: float = 0.8
    # Decisions use this quantile of the Beta (lower credible bound), not the mean.
    score_quantile: float = 0.10
    # Interval shown in the UI.
    interval: tuple[float, float] = (0.10, 0.90)

    # --- Vision thresholds (rule 7: trust never moves these down) -----------
    # A line is billable only at or above this vision probability.
    bill_threshold: float = 0.90
    # Lines below this are treated as not taken and released without a check.
    ignore_threshold: float = 0.30
    # Billable lines at or above this are auto-captured under Express. Trust can
    # lower it towards `auto_capture_min`, but never below `bill_threshold`.
    auto_capture_max: float = 0.99
    auto_capture_min: float = 0.95

    # --- Policy cost model --------------------------------------------------
    # Share of basket value a dishonest shopper hides from the cameras.
    concealment_ratio: float = 0.3
    # Chance the exit check finds untracked items, per policy.
    catch_rate: dict[str, float] = field(
        default_factory=lambda: {"express": 0.1, "standard": 0.5, "strict": 0.9}
    )
    # Seconds of staff time: fixed per basket, plus per line a human checks.
    staff_seconds_base: dict[str, float] = field(
        default_factory=lambda: {"express": 0.0, "standard": 10.0, "strict": 45.0}
    )
    staff_seconds_per_line: float = 15.0
    # The customer waits as long as the staff check, plus a fixed walk-out time.
    customer_seconds_base: float = 5.0
    # Rupee value of one second of staff or customer time. ₹0.1/s = ₹360/h.
    rupees_per_second: float = 0.1
    # Customers count double: a queue costs goodwill as well as time.
    customer_time_weight: float = 2.0
    # Handling cost of a wrong charge that has to be refunded (support, goodwill).
    wrong_charge_cost: float = 50.0
    # Strict holds this much extra so items found at the exit check can be
    # captured. Must be authorized up front: PayPal won't over-capture past
    # 115% or USD 75 (see docs/verified-facts.md).
    strict_hold_buffer: float = 0.15
    # Strict auto-captures nothing above this amount.
    strict_auto_capture_cap: float = 200.0

    # --- Agent client -------------------------------------------------------
    agent_floor_limit: float = 500.0
    agent_max_limit: float = 20000.0
    # Requests up to this multiple of the limit go to the human; above it, deny.
    agent_ask_multiple: float = 3.0
    # A lower bound at or below this earns no headroom above the floor. Just
    # above the default prior's 10th percentile (0.316), so a new agent starts
    # at the floor.
    agent_score_zero: float = 0.35


DEFAULT = TrustConfig()
