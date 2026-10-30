# Demo video script (under 3:00)

The video follows the five beats the hackathon video needs. Narration is about 390 words, roughly 2:40 at a normal pace, which leaves room for clicks. Record at 1280×800 or larger with the browser zoomed so the AG Grid tables are readable.

## Before recording

1. Use a fresh database so the tables start empty. Locally: delete `proofpay.db` and start `uvicorn proofpay.api:app`. On Render: use **Manual Deploy → Restart service**.
2. If the sandbox is ready, set `PROOFPAY_PAYPAL=sandbox`. Then log in to the sandbox merchant account at sandbox.paypal.com in a second tab, ready to show the authorization and the partial capture. If not, record in offline mode: the "PayPal: offline stand-in" chip stays on screen, and the narration must not claim it's a sandbox transaction.
3. Open these tabs in order: Home, Checkout, Staff exit, Trust inspector, Agent, Simulator, and the GitHub repo.
4. Seeding history adds events. Do it once per recording, because seeding twice makes the trust curve look odd.

---

## 0:00 to 0:20: the problem

**Screen:** home page, then a slow scroll over the demo path.

> Camera-tracked stores have two bad options: trust every shopper and eat the losses, or check every shopper and bring the queue back. The card hold underneath is all-or-nothing. Proofpay uses PayPal's authorize-and-capture to charge only for what the cameras proved, and uses each payer's history to decide how much checking they need.

## 0:20 to 1:20: a new customer

**Screen:** Checkout → **Start visit** on "First visit".

> Asha's first visit. Vision gives each item a probability that she took it. Milk and bread are near certain. The chocolate was half hidden, at 63%. She picked up the shampoo and put it back, so it sits at 11% and will never be billed.

**Screen:** point at the policy chip (Strict) and the hold amount.

> With no history, the trust score is a cautious 0.32. Proofpay compares the expected cost of each exit policy and picks Strict. The hold is the basket plus a 15% buffer, because PayPal won't capture much beyond what was authorized.

**Screen:** click **Pay with PayPal** (or **Approve with PayPal (offline stand-in)**), then switch to Staff exit.

> PayPal authorizes the hold. On the staff screen, the AI explains the uncertain line in plain language. It recommends; the staff member decides.

**Screen:** **Explain uncertain lines (AI)** → **Taken** on the chocolate → **Close visit: capture verified, release the rest**. Scroll to the **PayPal calls** grid.

> Closing the visit captures only the verified total, $3.57 of the $4.10 held. The shampoo and the buffer are released. Every PayPal call is logged with its idempotency key, so a retry can't charge twice.

**Screen (sandbox only):** the merchant tab showing the authorization and the partial capture.

**Screen:** back on Checkout's receipt, **Not mine** on the bread → the AI triage card → **Refund**.

> Back home, Asha says the bread wasn't hers. The AI compares her claim with the camera evidence and recommends; staff confirm; PayPal issues a partial refund.

## 1:20 to 1:50: the same customer, months later

**Screen:** Trust inspector → **Add simulated history** for `asha` (the label "simulated" is visible) → the score chart and the events grid.

> Fast-forward: twenty weekly visits, all verified. These are simulated, and they're labelled that way. Each event's weight and decay is visible. The score is now the 10th percentile of her reputation, not the average, so it has to be earned.

**Screen:** Checkout → **Start visit** on "Regular visit" → Express → approve → Staff exit → close.

> Same store, same shopper: Express. Every item is above the auto-capture bar, so there's no exit check and no queue. The reasons are on screen, and PayPal captures the full basket.

## 1:50 to 2:25: an AI agent with an earned limit

**Screen:** Agent → **Plan purchase** → **Ask to pay**.

> The same engine gates AI shopping agents. This agent plans a restock and pays through PayPal, but every payment passes Proofpay's guard first. Its limit starts at ₹500. This ₹1,400 order is over the limit but under three times it, so it asks a human.

**Screen:** **Approve** → **Payer approved: complete** → mark **Correct**. Then try "far over" (the fridge) and show **deny**. Point at the limit after a few **Correct** marks.

> I approve it. A ₹48,000 fridge is refused outright. As purchases are confirmed correct, the limit grows. A returned purchase would shrink it.

## 2:25 to 2:55: does it work, and where doesn't it

**Screen:** Simulator page, the loss-vs-friction chart.

> We simulated 500 shoppers over 30 visits each, including fraudsters who build trust and then cash out. Any learned trust roughly halves loss compared with static rules or no trust. The honest part: our cautious lower bound gives about the same loss as the plain average, but sends far more honest shoppers to Strict. The grey line shows that trade-off, and the README has the numbers.

**Screen:** GitHub repo: README, then the commit list.

> Everything is open source under Apache-2.0, built from scratch during the hackathon. Trust changes friction, never the charge.

---

## Checks before upload

- [ ] Under 3:00.
- [ ] No unlicensed music, and no third-party logos beyond PayPal's own sandbox UI.
- [ ] If recorded offline, the narration never calls it a sandbox transaction.
- [ ] Uploaded to YouTube as **Public**, with the link pasted into `docs/devpost.md` and Devpost.
