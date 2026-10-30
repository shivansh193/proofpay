# Verified facts

Checked 2026-10-30. Each line names its source. "OPEN" means not yet confirmed; re-check before building on it.

## Hackathon (https://paypalaihackathon.devpost.com/rules)

- Submission period ends **Thu Nov 12, 2026, 12:00 PM PT** (= Nov 13, 00:30 IST).
- Judging Dec 1 to Dec 15, 2026; winners around Dec 21.
- Must integrate the PayPal developer platform (sandbox) plus any AI tool. "Any AI tool works, as long as PayPal integration is central."
- New or existing projects; existing ones "must have been significantly updated after the start of the Submission Period" and entrants "should explain how".
- Multiple submissions allowed, but each "must be unique and substantially different" from the entrant's other submissions.
- Functional demo: hosted URL **or** complete setup/run instructions. Mockups don't count.
- Public GitHub/Bitbucket/GitLab repo with an OSS licence file detectable in the About section.
- Video under 3 minutes, public on YouTube, shows the project working, no unlicensed music or third-party trademarks.
- Judging criteria, equally weighted: Technological Implementation, Design, Potential Impact, Innovation, Presentation. A pass/fail viability stage comes first.
- Prizes: 1st $12k, 2nd $8k, 3rd $5k; honourable mentions $5k each (Most Creative, Most Impactful, Best Demo Delivery, Best Use of PayPal + AI, Best Use of Agentic Commerce). Sponsor prizes: AG Grid (3), APIMatic, Bryntum, Channel3, Render (3, credits). Sponsor eligibility is "submissions that use any <sponsor> tools". No further requirement is stated in the rules.
- Max one grand or honourable-mention prize plus one sponsor prize per project.

## PayPal Payments v2

- Endpoints: `POST /v2/payments/authorizations/{id}/capture`, `/void`, `/reauthorize`; `POST /v2/payments/captures/{id}/refund`. (https://developer.paypal.com/docs/api/payments/v2/)
- Capture body: `amount {currency_code, value}`, `final_capture` (bool, default false: "Set to false if you intend to capture additional payments against the authorization"), `invoice_id` (≤127), `note_to_payer` (≤255), `soft_descriptor` (≤22), `payment_instruction`. (https://developer.paypal.com/docs/api/payments/v2/authorizations-capture)
- `PayPal-Request-Id` header provides idempotency. (same page; https://developer.paypal.com/api/rest/reference/idempotency)
- Honor period 3 days; authorization holds funds 29 days; each reauthorization creates a **new authorization ID** and restarts the honour period. (https://developer.paypal.com/docs/checkout/standard/customize/authorization/)
- Multiple captures: `final_capture: false` on each non-final call, **unique `invoice_id` per capture**. Partial captures for PayPal payments **must be enabled on the PayPal account**. (https://developer.paypal.com/docs/integration/direct/payments/capture-payment/)
- Over-capture: total captured must not exceed **115% of the authorization or USD 75 more, whichever is less**. (same guide) So a Strict "bigger hold" can't come from over-capture. It has to be authorized up front, e.g. a buffer line in the order.
- OPEN: whether `final_capture: true` releases the uncaptured remainder automatically in v2. Legacy NVP docs say yes; v2 guides say void or let it expire. Test in sandbox at step 3 and record the result here.
- OPEN: whether the sandbox merchant has partial/multiple capture enabled by default.

## Orders v2

- `POST /v2/checkout/orders`, `POST /v2/checkout/orders/{id}/authorize`. (https://developer.paypal.com/docs/api/orders/v2/)
- OPEN: exact response path to the authorization id (expected `purchase_units[0].payments.authorizations[0].id`) and presence of `payer.payer_id`. Confirm from a real sandbox response at step 3.
- OPEN: whether `amount.value` must equal the breakdown sum (expected yes, else `AMOUNT_MISMATCH`).

## Webhooks (https://developer.paypal.com/api/rest/webhooks/event-names/)

`PAYMENT.AUTHORIZATION.CREATED`, `PAYMENT.AUTHORIZATION.VOIDED`, `PAYMENT.CAPTURE.COMPLETED`, `PAYMENT.CAPTURE.REFUNDED`, `PAYMENT.CAPTURE.REVERSED`, `CUSTOMER.DISPUTE.CREATED|UPDATED|RESOLVED`, `CHECKOUT.ORDER.APPROVED`.
OPEN: whether sandbox emits dispute events. If not, simulated disputes are labelled as simulated.

## JS SDK

- v6 is live (https://developer.paypal.com/community/blog/paypal-js-sdk-v6/). Uses `createPayPalOneTimePaymentSession`. The order (and its `intent`) is created server-side, so the client only passes an order id.
- OPEN: confirm a v6 one-time session works with an `AUTHORIZE` order. Fall back to v5 `?intent=authorize` if not.

## Agent toolkit

- OPEN: official package names (`paypal-agent-toolkit` on PyPI, `@paypal/agent-toolkit` on npm, per third-party listings) and which actions work in sandbox. Check https://github.com/paypal/agent-toolkit before step 6.
