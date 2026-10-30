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

## Currency

- INR is **not** in PayPal's REST currency list (https://developer.paypal.com/api/rest/reference/currency-codes/). Store prices stay in INR (the trust engine is calibrated in rupees); sandbox amounts are USD at a fixed demo rate (`DEMO_INR_PER_USD`, default 85). This is a demo constant, not an exchange-rate quote.

## Webhook verification

- `POST /v1/notifications/verify-webhook-signature` with `auth_algo`, `cert_url`, `transmission_id`, `transmission_sig`, `transmission_time` (from the `PAYPAL-AUTH-ALGO`, `PAYPAL-CERT-URL`, `PAYPAL-TRANSMISSION-ID`, `PAYPAL-TRANSMISSION-SIG`, `PAYPAL-TRANSMISSION-TIME` headers), `webhook_id`, `webhook_event`. Response `verification_status`, sample `"SUCCESS"`. (https://developer.paypal.com/docs/api/webhooks/v1/verify-webhook-signature-post)
- OPEN: dispute outcome codes. The code treats any `dispute_outcome.outcome_code` containing `BUYER` as a chargeback. Check against a real sandbox dispute.

## JS SDK

- v6 is live (https://developer.paypal.com/community/blog/paypal-js-sdk-v6/). The web app uses `@paypal/react-paypal-js@10.6.1` from `/sdk-v6`: `PayPalProvider` (`environment="sandbox"`) and `PayPalOneTimePaymentButton` with `createOrder` returning `{ orderId }`. The order and its `AUTHORIZE` intent are created server-side.
- OPEN: confirm in sandbox that the v6 button approves an `AUTHORIZE` order. Fall back to the v5 components in the same package if not.

## Agent toolkit (https://github.com/paypal/agent-toolkit, Apache-2.0)

- Python package `paypal-agent-toolkit`. Payment tools: `create_order`, `get_order`, `pay_order` ("Process payment for an authorized order"), plus invoices, disputes, subscriptions, catalog and reporting. They are merchant-side, so the agent client calls the same REST endpoints directly behind the trust guard (the spec allows this).

## Gemini

- REST `POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`; text at `candidates[0].content.parts[].text`; JSON output via `generationConfig.responseMimeType` + `responseSchema`. (https://ai.google.dev/api/generate-content)
- Stable Flash-tier ids listed 2026-10-30: `gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`. (https://ai.google.dev/gemini-api/docs/models) Default `gemini-3.8-flash`, override with `GEMINI_MODEL`.
- The key is sent in the `x-goog-api-key` header rather than the `?key=` query string the reference examples use. OPEN: confirm with a real key.
