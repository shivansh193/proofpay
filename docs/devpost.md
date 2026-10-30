# Devpost submission text

Paste each section into the matching Devpost field. Lines marked **[UPDATE]** need a fact that only exists after the live sandbox run; fix or delete them before submitting.

---

## Tagline

Pay for what the camera proved, at the friction your history earned.

## Inspiration

Cashierless stores make one of two bad choices. Either they trust everyone, and absorb the losses, or they check everyone, and rebuild the queue they set out to remove. The card hold underneath both choices is all-or-nothing: the store charges the whole basket and refunds later, or it doesn't hold at all.

PayPal's authorize-then-capture flow already allows something better: hold the basket, then capture only part of it. What was missing was something that decides *which part*, and *how much checking a given shopper needs*.

## What it does

Proofpay is a checkout layer on PayPal for camera-tracked stores and for AI shopping agents.

1. **Hold.** At entry the shopper approves a PayPal order with intent `AUTHORIZE`. The hold covers the basket, plus a 15% buffer for shoppers with no history.
2. **Verify.** Computer vision gives each item a probability that it was actually taken. Only items above 0.90, or confirmed by staff, are billable. An uncertain item is never charged on trust.
3. **Capture what was proved.** At exit Proofpay captures the verified total against the authorization and releases the rest. If nothing was verified, it voids the authorization.
4. **"Not mine."** After the visit, the shopper can dispute any line. An AI triage compares the claim with the camera evidence and recommends; staff decide; an upheld claim becomes a partial PayPal refund.
5. **Trust sets the friction, never the price.** Each PayPal payer has a reputation built only from their history on the platform: verified captures, rejected disputes, items found at exit, PayPal disputes and chargebacks (via webhooks). The score sets which exit policy they get:
   - **Express:** no exit check.
   - **Standard:** staff check uncertain lines.
   - **Strict:** larger hold, everything over ₹200 checked.

   The policy is chosen by expected cost, and the staff screen shows the cost of each option.
6. **Agents earn spending limits.** An LLM buying agent plans a supply order and pays through PayPal, but every payment first passes Proofpay's guard: allow, ask the human, or deny. Its limit grows only as purchases are confirmed correct, and returns shrink it.

## How we built it

- **Trust engine** (Python, pure functions): a Beta reputation per payer.
  - Positive evidence is weighted by vision confidence.
  - Evidence decays with a 90-day half-life.
  - An empirical-Bayes cohort prior means a new payer starts uncertain rather than trusted.
  - Decisions use the 10th-percentile lower bound, not the mean.
  - Anti-gaming: a weekly cap on positive evidence, a value-at-risk block when a basket is far above the payer's usual, and an auto-capture cap for new payers.
- **Simulator:** 500 synthetic shoppers × 30 visits across four behaviours: honest, careless, opportunistic and fraudster (builds trust, then cashes out). It compares Proofpay with three baselines: no trust, static rules, and the Beta mean. One seeded command reproduces every figure.
- **PayPal (sandbox)**, called from a FastAPI backend:
  - **Orders v2:** create order with `intent: AUTHORIZE`, then authorize.
  - **Payments v2:**
    - capture the verified total with `final_capture` and a unique `invoice_id`;
    - void;
    - reauthorize;
    - partial refund on captures.
  - **Webhooks:** verified with `verify-webhook-signature`, de-duplicated, and written into the trust event log. Capture, refund, void and dispute events all feed reputation.
  - **Idempotency:** every mutating call sends a deterministic `PayPal-Request-Id`, so a retried capture or refund can't run twice.
  - **JS SDK v6** (`@paypal/react-paypal-js`) for the buyer's approval.
  - **Agent client:** the PayPal Agent Toolkit's payment tools are merchant-side, so the buying agent calls the same Orders and Payments endpoints directly, behind the trust guard.
- **AI:**
  1. **Vision verification.** A per-item probability of "taken" is what makes partial capture possible. The demo replays recorded detection traces through a pluggable vision interface.
  2. **Exit-check explainer** (Gemini, JSON-schema output). For each uncertain line it gives staff a plain-language summary of the evidence and the trust reasoning. It only recommends, and the staff-agreement rate is logged.
  3. **Dispute triage** (Gemini). It recommends uphold, reject or review footage for a "Not mine" claim.
  4. **Agent planner** (Gemini). It turns a task ("restock the front desk") into a catalog order.
- **Front end:** a static Next.js export served by FastAPI, using AG Grid for the event, line, visit and PayPal-call tables. Pages: Checkout, Staff exit, Trust inspector, Agent console and Simulator.
- **Deploy:** one Docker image on Render (free plan).

## Challenges we ran into

- **Holding more for risky shoppers.** PayPal caps captures at 115% of the authorization or USD 75 more, whichever is less, so over-capturing can't provide a bigger hold. Strict authorizes the buffer up front as its own order line instead.
- **INR isn't a PayPal REST currency.** The store and the trust maths run in rupees, and PayPal amounts are USD at a fixed, labelled demo rate.
- **The lower bound buys caution, not savings.** In simulation the 10th-percentile score gives almost the same loss as the Beta mean, but sends 28% of honest visits to Strict, against 7%. We report this rather than tuning it away.
- **Agent Toolkit fit.** The toolkit's tools are built for the merchant side of the payment, so the agent's buy-side calls go straight to REST behind the guard.

## Accomplishments that we're proud of

- **Trust can never create a charge.** It can only change how much checking happens, and the code enforces this: a line is billable only at p ≥ 0.90 or with staff confirmation.
- **Learned trust halves loss** in simulation compared with static rules or no trust: ₹22.5 against ₹42.1 and ₹50.3 per visit. Fraud cash-out loss falls to under a third of the no-trust level.
- **Every PayPal call is visible on the staff screen,** with its idempotency key.
- **Every decision explains itself:** the events used, their weights, the cost of each policy, and why the cheapest allowed one won.

## What we learned

- Partial capture turns "did they really take it?" into a payments question that has a precise answer.
- Most of the value comes from learning trust at all. Squeezing more out of the uncertainty bound mostly moves friction around.
- Vision error rates and shopper behaviour are the assumptions everything rests on. They live in one file, labelled as assumptions.

## What's next for Proofpay

- Live vision on real shelf footage in place of recorded traces.
- Calibrating the concealment assumption (the share of a basket a dishonest shopper hides) from real exit-check data. It drives how often honest shoppers get Strict, and the README shows the trade-off.
- Postgres and multi-store cohorts.
- Wrapping the buyer agent in the Agent Toolkit if it gains buyer-side tools.

## Built with

python, fastapi, sqlite, scipy, numpy, matplotlib, httpx, next.js, react, typescript, ag-grid, paypal-orders-api, paypal-payments-api, paypal-webhooks, paypal-js-sdk, gemini, docker, render

## Links

- Repo: https://github.com/shivansh193/proofpay (Apache-2.0)
- Live demo: https://proofpay-6jk0.onrender.com
- Video: **[UPDATE]** YouTube link

## Notes for the submission form

- **New or existing project:** new. Every commit in the repo was written during the submission period, starting with `ed88ea0` on 2026-10-30.
- **[UPDATE]** After the sandbox run, confirm that the hosted demo runs in sandbox mode, or say it runs offline, and name the sandbox transaction shown in the video.
- **Team:** **[UPDATE]**
