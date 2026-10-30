import pytest

from proofpay.trust import (
    DEFAULT,
    Event,
    Line,
    agent_limit,
    authorize_agent_spend,
    auto_capture_threshold,
    choose_policy,
    confidence_weight,
    fit_cohort_prior,
    reputation,
)


def cap(t, p=0.98, value=300.0, subject="s"):
    return Event(subject, "capture_verified", t, line_p=(p,), value=value)


def neg(kind, t, subject="s"):
    return Event(subject, kind, t)


# --- evidence weighting ------------------------------------------------------


def test_confidence_weight_is_monotone_and_bounded():
    ws = [confidence_weight(p / 100) for p in range(101)]
    assert ws == sorted(ws)
    assert ws[0] == 0 and ws[-1] == 1
    assert confidence_weight(0.98) == pytest.approx(0.96)
    assert confidence_weight(0.7) < confidence_weight(0.98) / 2


def test_uncertain_captures_build_less_trust():
    sure = reputation("s", [cap(i * 7, p=0.98) for i in range(10)], now=70)
    unsure = reputation("s", [cap(i * 7, p=0.7) for i in range(10)], now=70)
    assert sure.score > unsure.score


def test_unknown_event_kind_rejected():
    with pytest.raises(ValueError):
        Event("s", "bogus", 0)
    with pytest.raises(ValueError):
        Event("s", "capture_verified", 0)


# --- score -------------------------------------------------------------------


def test_new_subject_is_uncertain_not_trusted():
    r = reputation("s", [], now=0)
    assert r.score < 0.5
    assert r.interval[1] - r.interval[0] > 0.4


def test_lower_bound_rewards_history_at_same_mean():
    # Same 2:1 ratio of evidence, ten times more of it.
    short = reputation("s", [], now=0, prior=(2, 1))
    long = reputation("s", [], now=0, prior=(20, 10))
    assert short.mean == pytest.approx(long.mean)
    assert long.score > short.score


def test_negative_events_lower_score_and_neutral_ones_do_not():
    base = [cap(i * 7) for i in range(8)]
    r0 = reputation("s", base, now=60)
    r_upheld = reputation("s", base + [neg("line_disputed_upheld", 59)], now=60)
    r_rejected = reputation("s", base + [neg("line_disputed_rejected", 59)], now=60)
    r_chargeback = reputation("s", base + [neg("chargeback", 59)], now=60)
    assert r_upheld.score == pytest.approx(r0.score)
    assert r_chargeback.score < r_rejected.score < r0.score


def test_old_mistakes_fade():
    goods = [cap(400 + i * 7) for i in range(8)]
    recent = reputation("s", goods + [neg("exit_mismatch", 455)], now=460)
    old = reputation("s", goods + [neg("exit_mismatch", 0)], now=460)
    assert old.score > recent.score


def test_weekly_cap_stops_trust_farming():
    # 50 baskets in one week count no more than the cap.
    farm = reputation("s", [cap(i * 0.1) for i in range(50)], now=5)
    assert farm.alpha - farm.prior[0] <= DEFAULT.max_positive_per_week + 1e-9
    assert any("weekly cap" in c.note for c in farm.contributions)
    spread = reputation("s", [cap(i * 7) for i in range(50)], now=350)
    assert spread.score > farm.score


def test_future_and_foreign_events_ignored():
    r = reputation("s", [cap(10), cap(1, subject="other")], now=5)
    assert r.verified_captures == 0


# --- cohort prior ------------------------------------------------------------


def test_prior_falls_back_and_is_clamped():
    assert fit_cohort_prior([0.9, 0.9]) == DEFAULT.default_prior
    a0, b0 = fit_cohort_prior([0.99, 0.98, 0.99, 0.97, 0.99, 0.98])
    lo, hi = DEFAULT.prior_strength_range
    assert lo <= a0 + b0 <= hi + 1e-9
    assert a0 / (a0 + b0) <= DEFAULT.prior_mean_cap + 1e-9


def test_prior_method_of_moments_recovers_moderate_cohort():
    rates = [0.5, 0.6, 0.7, 0.4, 0.6, 0.5, 0.7, 0.3]
    a0, b0 = fit_cohort_prior(rates)
    assert a0 / (a0 + b0) == pytest.approx(sum(rates) / len(rates))


# --- policy ------------------------------------------------------------------


def trusted():
    return reputation("s", [cap(i * 7, value=400) for i in range(40)], now=280)


def basket(*ps, price=100.0):
    return [Line(f"l{i}", f"item{i}", price, p) for i, p in enumerate(ps)]


def test_new_customer_gets_checked_trusted_gets_express():
    lines = basket(0.995, 0.99, 0.985)
    new = choose_policy(lines, reputation("s", [], now=0))
    old = choose_policy(lines, trusted())
    assert new.policy in ("standard", "strict")
    assert old.policy == "express"
    assert set(new.costs) == {"express", "standard", "strict"}


def test_likely_uncertain_line_is_worth_a_check_even_when_trusted():
    # Releasing an 85%-likely ₹100 item costs more than a 15 s check.
    d = choose_policy(basket(0.99, 0.85), trusted())
    assert d.policy != "express"
    assert d.dispositions["l1"] == "staff_check"


def test_rule7_trust_never_bills_low_confidence_lines():
    lines = basket(0.89, 0.5, 0.31, 0.1)
    for score in (0.0, 0.5, 0.99, 1.0):
        d = choose_policy(lines, trusted(), score=score)
        for c in d.costs.values():
            assert "auto_capture" not in c.dispositions.values()
    assert auto_capture_threshold(1.0) >= DEFAULT.bill_threshold


def test_low_vision_lines_are_released():
    d = choose_policy(basket(0.1, 0.99), trusted())
    assert d.dispositions["l0"] == "release"


def test_value_at_risk_blocks_express_for_big_basket():
    big = basket(*[0.99] * 30)  # ₹3000 vs a ₹400 median
    d = choose_policy(big, trusted())
    assert not d.costs["express"].allowed
    assert d.policy != "express"
    assert any("usual" in r for r in d.reasons)


def test_new_subject_auto_capture_cap():
    d = choose_policy(basket(*[0.995] * 8), reputation("s", [], now=0), score=0.99)
    assert not d.costs["express"].allowed


def test_strict_holds_buffer():
    lines = basket(0.99, 0.6)
    d = choose_policy(lines, reputation("s", [neg("chargeback", 0)], now=1))
    assert d.policy == "strict"
    assert d.hold_amount == pytest.approx(200 * (1 + DEFAULT.strict_hold_buffer))


def test_decision_is_explained():
    e = choose_policy(basket(0.99), trusted()).explain()
    assert e["reasons"] and set(e["costs"]) == {"express", "standard", "strict"}


# --- agent -------------------------------------------------------------------


def agent_events(n_ok, n_bad=0):
    evs = [Event("a", "agent_purchase_ok", i * 7) for i in range(n_ok)]
    evs += [Event("a", "agent_purchase_returned", n_ok * 7 + i) for i in range(n_bad)]
    return evs


def test_agent_limit_grows_with_correct_purchases():
    limits = [agent_limit(reputation("a", agent_events(n), now=n * 7 + 10).score) for n in (0, 5, 20)]
    assert limits == sorted(limits) and limits[0] == DEFAULT.agent_floor_limit
    assert limits[2] > limits[0]


def test_agent_verdicts():
    rep = reputation("a", agent_events(0), now=0)
    assert authorize_agent_spend(rep, 100).verdict == "allow"
    assert authorize_agent_spend(rep, 1000).verdict == "ask_human"
    assert authorize_agent_spend(rep, 100000).verdict == "deny"
