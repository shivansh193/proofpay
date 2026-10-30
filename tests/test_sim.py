from proofpay.sim.__main__ import summarise
from proofpay.sim.run import run_strategy
from proofpay.sim.world import WorldConfig, build_world

SMALL = WorldConfig(
    archetypes={"honest": 8, "careless": 3, "opportunistic": 3, "fraudster": 3}, visits_per_subject=15
)


def test_same_seed_same_results():
    a = summarise(run_strategy("proofpay", build_world(1, SMALL), SMALL))
    b = summarise(run_strategy("proofpay", build_world(1, SMALL), SMALL))
    assert a == b


def test_all_strategies_see_the_same_world():
    world = build_world(2, SMALL)
    visits = {summarise(run_strategy(s, world, SMALL))["visits"] for s in ("proofpay", "no_trust")}
    assert visits == {17 * 15}


def test_trust_beats_no_trust_on_fraud_loss():
    world = build_world(3, SMALL)
    pp = run_strategy("proofpay", world, SMALL)
    nt = run_strategy("no_trust", world, SMALL)
    assert pp.fraud_cashout_loss < nt.fraud_cashout_loss
