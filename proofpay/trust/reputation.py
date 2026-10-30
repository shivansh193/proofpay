"""Beta reputation per subject: evidence -> (alpha, beta) -> score with explanation."""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from scipy.stats import beta as beta_dist

from .config import DEFAULT, TrustConfig
from .events import Event


@dataclass(frozen=True)
class Contribution:
    kind: str
    t: float
    raw: float  # weight before the weekly cap and decay
    capped: float  # after the weekly cap (positive evidence only)
    decay: float  # multiplier from age
    alpha: float  # added to alpha
    beta: float  # added to beta
    note: str = ""


@dataclass(frozen=True)
class Reputation:
    subject: str
    prior: tuple[float, float]
    alpha: float
    beta: float
    mean: float
    score: float  # lower credible bound used for decisions
    interval: tuple[float, float]
    verified_captures: int
    median_basket: float | None
    contributions: tuple[Contribution, ...]

    def explain(self) -> dict:
        return {
            "subject": self.subject,
            "prior": {"alpha0": self.prior[0], "beta0": self.prior[1]},
            "alpha": self.alpha,
            "beta": self.beta,
            "mean": self.mean,
            "score": self.score,
            "interval": list(self.interval),
            "verified_captures": self.verified_captures,
            "median_basket": self.median_basket,
            "events": [c.__dict__ for c in self.contributions],
        }


def confidence_weight(p: float, cfg: TrustConfig = DEFAULT) -> float:
    """f(p): how much one verified line at vision probability p is worth."""
    p0 = cfg.confidence_floor
    return min(1.0, max(0.0, (p - p0) / (1.0 - p0)))


def decay(age_days: float, cfg: TrustConfig = DEFAULT) -> float:
    return 0.5 ** (max(0.0, age_days) / cfg.half_life_days)


def raw_weight(e: Event, cfg: TrustConfig = DEFAULT) -> tuple[float, float]:
    """(positive, negative) weight of one event before cap and decay."""
    if e.kind == "capture_verified":
        return sum(confidence_weight(p, cfg) for p in e.line_p) / len(e.line_p), 0.0
    if e.kind in cfg.positive:
        return cfg.positive[e.kind], 0.0
    if e.kind in cfg.severity:
        return 0.0, cfg.severity[e.kind]
    return 0.0, 0.0


def quantile(a: float, b: float, q: float) -> float:
    return float(beta_dist.ppf(q, a, b))


def reputation(
    subject: str,
    events: Iterable[Event],
    now: float,
    prior: tuple[float, float] | None = None,
    cfg: TrustConfig = DEFAULT,
) -> Reputation:
    """Score one subject from its events up to `now`. Events after `now` are ignored."""
    a0, b0 = prior or cfg.default_prior
    evs = sorted((e for e in events if e.subject == subject and e.t <= now), key=lambda e: e.t)

    alpha, beta = a0, b0
    contribs: list[Contribution] = []
    week_used: dict[int, float] = {}
    t_first = evs[0].t if evs else now
    baskets: list[float] = []

    for e in evs:
        pos, neg = raw_weight(e, cfg)
        note = ""
        capped = pos
        if pos > 0:
            week = math.floor((e.t - t_first) / 7.0)
            room = max(0.0, cfg.max_positive_per_week - week_used.get(week, 0.0))
            capped = min(pos, room)
            week_used[week] = week_used.get(week, 0.0) + capped
            if capped < pos:
                note = f"weekly cap: {pos - capped:.2f} not counted"
        elif e.kind in cfg.neutral:
            note = "recorded, not scored against subject"
        d = decay(now - e.t, cfg)
        alpha += capped * d
        beta += neg * d
        if e.kind == "capture_verified":
            baskets.append(e.value)
        contribs.append(Contribution(e.kind, e.t, pos or neg, capped if pos else neg, d, capped * d, neg * d, note))

    lo, hi = cfg.interval
    baskets.sort()
    median = baskets[len(baskets) // 2] if baskets else None
    return Reputation(
        subject=subject,
        prior=(a0, b0),
        alpha=alpha,
        beta=beta,
        mean=alpha / (alpha + beta),
        score=quantile(alpha, beta, cfg.score_quantile),
        interval=(quantile(alpha, beta, lo), quantile(alpha, beta, hi)),
        verified_captures=len(baskets),
        median_basket=median,
        contributions=tuple(contribs),
    )


def fit_cohort_prior(
    rates: Sequence[float], cfg: TrustConfig = DEFAULT
) -> tuple[float, float]:
    """Empirical-Bayes Beta prior from per-subject good-outcome rates (method of moments).

    The fitted strength and mean are clamped (see config) so a new subject
    starts uncertain however honest the cohort is. Falls back to the default
    prior when there are too few subjects or no variance.
    """
    if len(rates) < 5:
        return cfg.default_prior
    n = len(rates)
    m = sum(rates) / n
    v = sum((r - m) ** 2 for r in rates) / (n - 1)
    if v <= 0 or not 0 < m < 1:
        return cfg.default_prior
    strength = m * (1 - m) / v - 1
    lo, hi = cfg.prior_strength_range
    strength = min(hi, max(lo, strength))
    m = min(m, cfg.prior_mean_cap)
    return m * strength, (1 - m) * strength
