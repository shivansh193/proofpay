"""A seeded population of shoppers and their pre-drawn visits.

Every random draw is made here, up front, so each checkout strategy faces the
exact same shoppers, baskets, vision outputs and coin flips. Only the
strategy's decisions differ between runs.

The vision numbers below are ASSUMPTIONS, not measurements. They describe a
detector that is usually confident and right, sometimes unsure, and rarely
confidently wrong. Change them in `WorldConfig` and rerun.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class WorldConfig:
    archetypes: dict[str, int] = field(
        default_factory=lambda: {"honest": 300, "careless": 100, "opportunistic": 60, "fraudster": 40}
    )
    visits_per_subject: int = 30
    mean_days_between_visits: float = 10.0
    mean_items: float = 4.0
    price_median: float = 120.0
    price_sigma: float = 0.7
    # --- Vision assumptions -------------------------------------------------
    put_back_rate: float = 0.10  # picked up, then returned to the shelf
    hard_case_rate: float = 0.08  # taken, but occluded: detector unsure
    taken_p: tuple[float, float] = (40.0, 1.0)  # Beta for taken items, mean 0.976
    hard_p: tuple[float, float] = (3.0, 2.0)  # Beta for hard taken items, mean 0.6
    put_back_p: tuple[float, float] = (1.0, 8.0)  # Beta for returned items, mean 0.11
    false_positive_rate: float = 0.04  # a returned item still looks taken
    # --- Behaviour ----------------------------------------------------------
    conceal_prob: dict[str, float] = field(
        default_factory=lambda: {"honest": 0.0, "careless": 0.05, "opportunistic": 0.02, "fraudster": 0.0}
    )
    notices_wrong_charge: dict[str, float] = field(
        default_factory=lambda: {"honest": 0.9, "careless": 0.6, "opportunistic": 0.95, "fraudster": 0.95}
    )
    false_dispute_prob: dict[str, float] = field(
        default_factory=lambda: {"honest": 0.0, "careless": 0.03, "opportunistic": 0.12, "fraudster": 0.0}
    )
    # Fraudsters shop small and clean for a while, then hide half of big baskets.
    fraud_warmup_visits: tuple[int, int] = (5, 12)
    fraud_cashout_items: tuple[int, int] = (10, 20)
    fraud_conceal_share: float = 0.5
    # --- Humans in the loop -------------------------------------------------
    staff_accuracy: float = 0.98  # staff see the truth on a checked line
    footage_review_accuracy: float = 0.95  # dispute review gets it right


@dataclass(frozen=True)
class Item:
    price: float
    taken: bool
    p: float  # vision probability


@dataclass(frozen=True)
class Visit:
    t: float
    items: tuple[Item, ...]  # what the cameras tracked
    concealed: tuple[float, ...]  # prices of items hidden from the cameras
    cashout: bool
    # Uniform draws, consumed by the outcome logic in a fixed order.
    u_catch: tuple[float, ...]  # one per concealed item
    u_staff: tuple[float, ...]  # one per tracked item
    u_notice: tuple[float, ...]  # one per tracked item
    u_review: tuple[float, ...]  # one per tracked item
    u_false_dispute: float
    u_false_pick: float


@dataclass(frozen=True)
class Subject:
    sid: str
    archetype: str
    visits: tuple[Visit, ...]


def _item(rng: np.random.Generator, w: WorldConfig) -> Item:
    price = float(np.round(rng.lognormal(np.log(w.price_median), w.price_sigma), 0)) or 10.0
    if rng.random() < w.put_back_rate:
        fp = rng.random() < w.false_positive_rate
        p = rng.beta(*(w.taken_p if fp else w.put_back_p))
        return Item(price, False, float(p))
    p = rng.beta(*(w.hard_p if rng.random() < w.hard_case_rate else w.taken_p))
    return Item(price, True, float(p))


def build_world(seed: int, w: WorldConfig = WorldConfig()) -> list[Subject]:
    rng = np.random.default_rng(seed)
    subjects: list[Subject] = []
    for arch, n in w.archetypes.items():
        for k in range(n):
            warmup = int(rng.integers(*w.fraud_warmup_visits)) if arch == "fraudster" else 10**9
            t = float(rng.uniform(0, w.mean_days_between_visits))
            visits = []
            for v in range(w.visits_per_subject):
                cashout = v >= warmup
                if cashout:
                    n_items = int(rng.integers(*w.fraud_cashout_items))
                elif arch == "fraudster":
                    n_items = 1 + int(rng.poisson(1.0))
                else:
                    n_items = 1 + int(rng.poisson(w.mean_items - 1))
                items = [_item(rng, w) for _ in range(n_items)]
                concealed: list[float] = []
                if cashout:
                    budget = w.fraud_conceal_share * sum(i.price for i in items)
                    while sum(concealed) < budget:
                        concealed.append(_item(rng, w).price)
                elif rng.random() < w.conceal_prob[arch]:
                    concealed.append(_item(rng, w).price)
                visits.append(
                    Visit(
                        t=t,
                        items=tuple(items),
                        concealed=tuple(concealed),
                        cashout=cashout,
                        u_catch=tuple(rng.random(len(concealed))),
                        u_staff=tuple(rng.random(n_items)),
                        u_notice=tuple(rng.random(n_items)),
                        u_review=tuple(rng.random(n_items)),
                        u_false_dispute=float(rng.random()),
                        u_false_pick=float(rng.random()),
                    )
                )
                t += float(rng.exponential(w.mean_days_between_visits)) + 0.5
            subjects.append(Subject(f"{arch}-{k}", arch, tuple(visits)))
    return subjects
