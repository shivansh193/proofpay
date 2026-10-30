"""Run each checkout strategy over the same world and score it."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field

from proofpay.trust import DEFAULT, Event, Line, TrustConfig, choose_policy, evaluate, fit_cohort_prior, reputation
from proofpay.trust.reputation import Reputation, raw_weight

from .world import Subject, Visit, WorldConfig

Decide = Callable[[list[Line], Reputation, list[Event], float, TrustConfig], tuple[str, dict[str, str], float, float]]


def proofpay_decide(lines, rep, evs, now, cfg):
    d = choose_policy(lines, rep, cfg)
    c = d.costs[d.policy]
    return d.policy, d.dispositions, c.staff_seconds, c.customer_seconds


def beta_mean_decide(lines, rep, evs, now, cfg):
    d = choose_policy(lines, rep, cfg, score=rep.mean)
    c = d.costs[d.policy]
    return d.policy, d.dispositions, c.staff_seconds, c.customer_seconds


def no_trust_decide(lines, rep, evs, now, cfg):
    c = evaluate("standard", lines, 0.5, cfg)
    return "standard", c.dispositions, c.staff_seconds, c.customer_seconds


def static_rules_decide(lines, rep, evs, now, cfg):
    """Hand thresholds: any bad event in 180 days -> strict; 5+ clean visits and a
    basket under ₹1000 -> express; else standard."""
    bad = any(e.kind in cfg.severity and now - e.t <= 180 for e in evs)
    basket = sum(ln.price for ln in lines)
    if bad:
        policy = "strict"
    elif rep.verified_captures >= 5 and basket <= 1000:
        policy = "express"
    else:
        policy = "standard"
    c = evaluate(policy, lines, 0.5, cfg)
    return policy, c.dispositions, c.staff_seconds, c.customer_seconds


STRATEGIES: dict[str, tuple[Decide, bool]] = {
    # name: (decide, fits a cohort prior)
    "proofpay": (proofpay_decide, True),
    "beta_mean": (beta_mean_decide, True),
    "static_rules": (static_rules_decide, False),
    "no_trust": (no_trust_decide, False),
}


@dataclass
class Tally:
    visits: int = 0
    loss: float = 0.0
    staff_seconds: float = 0.0
    customer_seconds: float = 0.0
    strict_visits: int = 0
    express_visits: int = 0
    unrefunded_wrong_charges: int = 0
    revenue: float = 0.0


@dataclass
class Result:
    strategy: str
    by_archetype: dict[str, Tally] = field(default_factory=lambda: defaultdict(Tally))
    # Fraudster id -> visits from first cash-out to first caught concealment (None = never).
    fraud_catch_delay: dict[str, int | None] = field(default_factory=dict)
    fraud_cashout_loss: float = 0.0

    def total(self) -> Tally:
        t = Tally()
        for a in self.by_archetype.values():
            for k in t.__dict__:
                setattr(t, k, getattr(t, k) + getattr(a, k))
        return t


def _outcome(s: Subject, v: Visit, disp: dict[str, str], policy: str, w: WorldConfig, cfg: TrustConfig):
    """What happens at checkout. Returns (loss, revenue, unrefunded_wrong, events, caught_any)."""
    arch = s.archetype
    loss = revenue = 0.0
    wrong = 0
    evs: list[Event] = []
    billed: list[int] = []
    for i, it in enumerate(v.items):
        d = disp[f"l{i}"]
        if d == "staff_check":
            right = v.u_staff[i] < w.staff_accuracy
            bill = it.taken if right else not it.taken
        else:
            bill = d == "auto_capture"
        if bill:
            billed.append(i)
            revenue += it.price
            if not it.taken:
                if v.u_notice[i] < w.notices_wrong_charge[arch]:
                    if v.u_review[i] < w.footage_review_accuracy:
                        revenue -= it.price
                        evs.append(Event(s.sid, "line_disputed_upheld", v.t, value=it.price))
                    else:
                        wrong += 1
                        evs.append(Event(s.sid, "line_disputed_rejected", v.t, value=it.price))
                else:
                    wrong += 1
        elif it.taken:
            loss += it.price

    true_billed = [i for i in billed if v.items[i].taken]
    if true_billed and v.u_false_dispute < w.false_dispute_prob[arch]:
        i = true_billed[int(v.u_false_pick * len(true_billed))]
        if v.u_review[i] < w.footage_review_accuracy:
            evs.append(Event(s.sid, "line_disputed_rejected", v.t, value=v.items[i].price))
        else:
            loss += v.items[i].price
            revenue -= v.items[i].price
            evs.append(Event(s.sid, "line_disputed_upheld", v.t, value=v.items[i].price))

    caught = False
    for price, u in zip(v.concealed, v.u_catch):
        if u < cfg.catch_rate[policy]:
            caught = True
            revenue += price
        else:
            loss += price
    if caught:
        evs.append(Event(s.sid, "exit_mismatch", v.t))
    if billed:
        evs.insert(
            0,
            Event(s.sid, "capture_verified", v.t, line_p=tuple(v.items[i].p for i in billed),
                  value=sum(v.items[i].price for i in billed)),
        )
    return loss, revenue, wrong, evs, caught


def run_strategy(name: str, world: list[Subject], w: WorldConfig, cfg: TrustConfig = DEFAULT,
                 refit_every_days: float = 30.0) -> Result:
    decide, fits_prior = STRATEGIES[name]
    res = Result(name)
    events: dict[str, list[Event]] = defaultdict(list)
    prior = cfg.default_prior
    next_refit = refit_every_days
    first_cashout: dict[str, int] = {}
    queue = sorted(((v.t, si, vi) for si, s in enumerate(world) for vi, v in enumerate(s.visits)))

    for t, si, vi in queue:
        s, v = world[si], world[si].visits[vi]
        if fits_prior and t >= next_refit:
            prior = _refit(world, events, t, prior, cfg)
            next_refit += refit_every_days
        evs = events[s.sid]
        rep = reputation(s.sid, evs, now=t, prior=prior, cfg=cfg)
        lines = [Line(f"l{i}", f"item{i}", it.price, it.p) for i, it in enumerate(v.items)]
        policy, disp, staff_s, cust_s = decide(lines, rep, evs, t, cfg)
        loss, revenue, wrong, new, caught = _outcome(s, v, disp, policy, w, cfg)
        evs.extend(new)

        tl = res.by_archetype[s.archetype]
        tl.visits += 1
        tl.loss += loss
        tl.revenue += revenue
        tl.staff_seconds += staff_s
        tl.customer_seconds += cust_s
        tl.strict_visits += policy == "strict"
        tl.express_visits += policy == "express"
        tl.unrefunded_wrong_charges += wrong

        if s.archetype == "fraudster":
            res.fraud_catch_delay.setdefault(s.sid, None)
            if v.cashout:
                res.fraud_cashout_loss += loss
                first_cashout.setdefault(s.sid, vi)
                if caught and res.fraud_catch_delay[s.sid] is None:
                    res.fraud_catch_delay[s.sid] = vi - first_cashout[s.sid]
    return res


def _refit(world, events, now, prior, cfg) -> tuple[float, float]:
    """Empirical-Bayes cohort prior from each subject's evidence so far."""
    rates = []
    for s in world:
        evs = events.get(s.sid)
        if not evs or len(evs) < 3:
            continue
        pos = neg = 0.0
        for e in evs:
            a, b = raw_weight(e, cfg)
            pos, neg = pos + a, neg + b
        if pos + neg > 0:
            rates.append(pos / (pos + neg))
    return fit_cohort_prior(rates, cfg) if rates else prior
