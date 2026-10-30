# Proofpay

**Pay for what the camera proved, at the friction your history earned.**

At checkout, PayPal authorizes the whole basket. Computer vision decides which items actually left with the customer. Proofpay captures only the verified lines, releases the rest, and refunds upheld "Not mine" disputes. A trust score learned from each payer's history sets how much is held, how strict the exit check is, and when capture happens without a human. The same engine gives an AI shopping agent a spending limit that grows as its purchases turn out correct.

> Status (2026-10-30): the trust engine, unit tests and simulator are done. The PayPal sandbox flow, vision adapter, web app and agent client are next.

## The one rule

**Trust changes friction, never charges.** A line is billable only if vision probability `p ≥ 0.90` or a staff member confirmed it. Trust can lower the bar for *skipping the human* on lines that are already billable, within `[0.95, 0.99]`. It never makes an uncertain line chargeable. Trust uses only payment and verification history on this platform: no demographics, location or device fingerprints.

## Trust engine (`proofpay/trust/`)

Pure functions, no I/O. Every output carries an explanation: the events used, their weights, and the resulting parameters.

**Evidence.** Each subject (a PayPal `payer_id`, or an agent id) has a Beta(α, β) reputation.

| Event | Effect |
|---|---|
| `capture_verified` | α += mean over lines of f(p), with f(p) = clip((p − 0.5)/0.5, 0, 1) |
| `agent_purchase_ok` | α += 1 |
| `line_disputed_rejected` | β += 3 (footage shows the take) |
| `exit_mismatch` | β += 5 (staff found an untracked item) |
| `dispute_opened` / `chargeback` | β += 2 / 10 |
| `agent_purchase_returned` / `_overridden` | β += 1 / 2 |
| `line_disputed_upheld`, `refund` | recorded, not scored (an upheld dispute is the camera's error) |

**Decay.** Each event's weight is multiplied by 0.5^(age / 90 days).

**Prior.** A cohort Beta(α₀, β₀) fitted by method of moments (empirical Bayes), clamped to strength 2–6 and mean ≤ 0.8, so a new subject starts uncertain rather than trusted.

**Score.** Decisions use the 10th percentile of Beta(α, β), not the mean. Less history means a wider posterior, which means a lower score.

**Anti-gaming.**
- Positive evidence is capped at 3 per 7-day window.
- A basket above 3× the subject's median basket can't use Express.
- Subjects with fewer than 3 verified visits can't auto-capture more than ₹500.

**Policy choice.** For each basket, every policy's expected cost is computed and the cheapest allowed one wins:

```
cost = Σ_unchecked p·price                       (uncertain lines nobody checks)
     + (1 − score) · 0.3 · basket · (1 − catch)   (items hidden from the cameras)
     + Σ_auto (1 − p)(price + ₹50)               (auto-captured false positives)
     + ₹0.1/s · (staff_s + 2 · customer_s)        (friction)
```

| Policy | Auto-capture bar | Uncertain lines | Exit-check catch rate | Hold |
|---|---|---|---|---|
| Express | 0.99 → 0.95 as trust rises | released unbilled | 10% | verified lines |
| Standard | 0.99 | staff check | 50% | verified + uncertain |
| Strict | 0.99, nothing above ₹200 | staff check | 90% | basket + 15% |

The Strict buffer is authorized up front because PayPal caps over-capture at 115% or USD 75 more, whichever is less (see [docs/verified-facts.md](docs/verified-facts.md)).

**Agent limit.** `limit = ₹500 + (₹20,000 − ₹500) · max(0, (score − 0.35)/0.65)`. A request within the limit is allowed. Up to 3× the limit goes to the human for approval. Anything above that is denied.

All defaults, with the reasoning for each, are in [proofpay/trust/config.py](proofpay/trust/config.py).

## Evaluation (`proofpay/sim/`)

To reproduce every number and figure:

```bash
python -m proofpay.sim --seed 0
```

The simulated population is 500 shoppers × 30 visits:
- 300 honest
- 100 careless (forget items, dispute honestly)
- 60 opportunistic (occasional false "Not mine")
- 40 fraudsters (build trust on small baskets, then hide half of large ones)

**The vision error rates are assumptions, not measurements.** They're listed in [proofpay/sim/world.py](proofpay/sim/world.py). Every strategy sees the same pre-drawn world.

![Loss vs friction](docs/eval/loss_vs_friction.png)

Results for seed 0 ([full table](docs/eval/results.md)):

| Strategy | Loss ₹/visit | Staff s/visit | Honest → Strict | Fraud cash-out loss ₹ |
|---|---|---|---|---|
| Proofpay (10th percentile) | **22.5** | 72.0 | 28.2% | **155,982** |
| Beta mean | 22.9 | 56.4 | 7.1% | 171,143 |
| Static rules | 42.1 | **49.0** | **0.6%** | 175,620 |
| No trust (all Standard) | 50.3 | 53.0 | 0.0% | 581,583 |

**What this shows:**
- Any learned trust roughly halves loss compared with static rules or no trust.
- It also cuts fraud cash-out loss to under a third of the no-trust level, because caught fraudsters move to Strict and stay there.

**Where Proofpay is worse:**
- At the default 10th-percentile score, it sends 28% of honest visits to Strict and costs about 15 more staff-seconds per visit than the Beta mean, for almost the same loss.
- The quantile sweep (grey line) shows loss is nearly flat across q = 0.02–0.5, while friction falls steadily. In this world the lower bound's caution mostly buys friction.
- Static rules have the least friction and the fewest false Strict visits, but nearly twice the loss.
- "Fraudsters caught" is 40/40 for every strategy, because a cash-out basket trips the value-at-risk check. The useful number is cash-out loss.

## Repository layout

```
proofpay/trust/   trust engine (reputation, policy, config)
proofpay/sim/     population simulator and baselines
tests/            unit tests (pytest)
docs/             verified PayPal/Devpost facts, eval outputs
```

## Development

```bash
python -m venv .venv && .venv/Scripts/activate   # Windows; use bin/activate elsewhere
pip install -e ".[dev]"
pytest
```

## Licence

Apache-2.0. See [LICENSE](LICENSE).
