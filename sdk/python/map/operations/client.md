<!-- Generated file — do not edit; regenerated with the SDK. -->

# Client — operations

Accessor: `client` · Source: `witnessed/client.py` · 28 operations

Each `###` block is one operation and assumes `sdk-map.md` is loaded: blocks omit what its invariants table covers and are otherwise self-contained, so chunk at block level. Signatures are the sync parsed spelling; the async and raw spellings take the same parameters (see sdk-map.md). **Type sources** names the module declaring each type an operation mentions, so resolving a body, return or error payload is a lookup rather than a search; the runtime types `RawError` and `ApiResult` are excluded, and an operation with no table mentions nothing but builtins and those.

### client.agent_complete

- **Route**: `POST /api/agents/purchases/{purchase_id}/complete`
- **Signature**: `def agent_complete(purchase_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `purchase_id`
- **Params**: `purchase_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, AgentCompleteErrorBody]`
- **Error**: `AgentCompleteErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `AgentCompleteErrorBody` | `witnessed/errors/agent_complete_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.agent_decide

- **Route**: `POST /api/agents/purchases/{purchase_id}/decide`
- **Signature**: `def agent_decide(purchase_id: str, body: DecideIn | DecideInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `purchase_id`, `body`
- **Params**: `purchase_id` — path · `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, AgentDecideErrorBody]`
- **Error**: `AgentDecideErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `DecideIn` | `witnessed/models/decide_in.py` |
| `DecideInDict` | `witnessed/models/decide_in.py` |
| `AgentDecideErrorBody` | `witnessed/errors/agent_decide_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.agent_outcome

- **Route**: `POST /api/agents/purchases/{purchase_id}/outcome`
- **Signature**: `def agent_outcome(purchase_id: str, body: OutcomeIn | OutcomeInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `purchase_id`, `body`
- **Params**: `purchase_id` — path · `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, AgentOutcomeErrorBody]`
- **Error**: `AgentOutcomeErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `OutcomeIn` | `witnessed/models/outcome_in.py` |
| `OutcomeInDict` | `witnessed/models/outcome_in.py` |
| `AgentOutcomeErrorBody` | `witnessed/errors/agent_outcome_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.agent_plan

- **Route**: `POST /api/agents/{agent_id}/plan`
- **Signature**: `def agent_plan(agent_id: str, body: PlanIn | PlanInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `agent_id`, `body`
- **Params**: `agent_id` — path · `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, AgentPlanErrorBody]`
- **Error**: `AgentPlanErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `PlanIn` | `witnessed/models/plan_in.py` |
| `PlanInDict` | `witnessed/models/plan_in.py` |
| `AgentPlanErrorBody` | `witnessed/errors/agent_plan_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.agent_purchase

- **Route**: `POST /api/agents/{agent_id}/purchases`
- **Signature**: `def agent_purchase(agent_id: str, body: PurchaseIn | PurchaseInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `agent_id`, `body`
- **Params**: `agent_id` — path · `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, AgentPurchaseErrorBody]`
- **Error**: `AgentPurchaseErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `PurchaseIn` | `witnessed/models/purchase_in.py` |
| `PurchaseInDict` | `witnessed/models/purchase_in.py` |
| `AgentPurchaseErrorBody` | `witnessed/errors/agent_purchase_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.agent_status

- **Route**: `GET /api/agents/{agent_id}`
- **Signature**: `def agent_status(agent_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `agent_id`
- **Params**: `agent_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, AgentStatusErrorBody]`
- **Error**: `AgentStatusErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `AgentStatusErrorBody` | `witnessed/errors/agent_status_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.agreement

- **Route**: `GET /api/ai/agreement`
- **Signature**: `def agreement(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.authorize

- **Route**: `POST /api/sessions/{session_id}/authorize`
- **Signature**: `def authorize(session_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`
- **Params**: `session_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, AuthorizeErrorBody]`
- **Error**: `AuthorizeErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `AuthorizeErrorBody` | `witnessed/errors/authorize_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.config

- **Route**: `GET /api/config`
- **Signature**: `def config(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.evidence

- **Route**: `GET /api/sessions/{session_id}/evidence`
- **Signature**: `def evidence(session_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`
- **Params**: `session_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, EvidenceErrorBody]`
- **Error**: `EvidenceErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `EvidenceErrorBody` | `witnessed/errors/evidence_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.exit_check

- **Route**: `POST /api/sessions/{session_id}/exit`
- **Signature**: `def exit_check(session_id: str, body: ExitIn | ExitInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`, `body`
- **Params**: `session_id` — path · `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, ExitCheckErrorBody]`
- **Error**: `ExitCheckErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `ExitIn` | `witnessed/models/exit_in.py` |
| `ExitInDict` | `witnessed/models/exit_in.py` |
| `ExitCheckErrorBody` | `witnessed/errors/exit_check_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.explain

- **Route**: `POST /api/sessions/{session_id}/explain`
- **Signature**: `def explain(session_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`
- **Params**: `session_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, ExplainErrorBody]`
- **Error**: `ExplainErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `ExplainErrorBody` | `witnessed/errors/explain_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.list_holds

- **Route**: `GET /api/holds`
- **Signature**: `def list_holds(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.not_mine

- **Route**: `POST /api/sessions/{session_id}/lines/{line_id}/not-mine`
- **Signature**: `def not_mine(session_id: str, line_id: str, body: NotMineIn | NotMineInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`, `line_id`, `body`
- **Params**: `session_id` — path · `line_id` — path · `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, NotMineErrorBody]`
- **Error**: `NotMineErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `NotMineIn` | `witnessed/models/not_mine_in.py` |
| `NotMineInDict` | `witnessed/models/not_mine_in.py` |
| `NotMineErrorBody` | `witnessed/errors/not_mine_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.paypal_webhook

- **Route**: `POST /api/webhooks/paypal`
- **Signature**: `def paypal_webhook(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.rescue_hold

- **Route**: `POST /api/holds/{session_id}/rescue`
- **Signature**: `def rescue_hold(session_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`
- **Params**: `session_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RescueHoldErrorBody]`
- **Error**: `RescueHoldErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `RescueHoldErrorBody` | `witnessed/errors/rescue_hold_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.scenarios

- **Route**: `GET /api/scenarios`
- **Signature**: `def scenarios(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.seed_history

- **Route**: `POST /api/demo/seed-history`
- **Signature**: `def seed_history(body: SeedIn | SeedInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `body`
- **Params**: `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, SeedHistoryErrorBody]`
- **Error**: `SeedHistoryErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `SeedIn` | `witnessed/models/seed_in.py` |
| `SeedInDict` | `witnessed/models/seed_in.py` |
| `SeedHistoryErrorBody` | `witnessed/errors/seed_history_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.seed_holds

- **Route**: `POST /api/demo/seed-holds`
- **Signature**: `def seed_holds(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.session

- **Route**: `GET /api/sessions/{session_id}`
- **Signature**: `def session(session_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`
- **Params**: `session_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, SessionErrorBody]`
- **Error**: `SessionErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `SessionErrorBody` | `witnessed/errors/session_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.sessions

- **Route**: `GET /api/sessions`
- **Signature**: `def sessions(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.sim_results

- **Route**: `GET /api/sim`
- **Signature**: `def sim_results(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.start

- **Route**: `POST /api/sessions`
- **Signature**: `def start(body: StartIn | StartInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `body`
- **Params**: `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, StartErrorBody]`
- **Error**: `StartErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `StartIn` | `witnessed/models/start_in.py` |
| `StartInDict` | `witnessed/models/start_in.py` |
| `StartErrorBody` | `witnessed/errors/start_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.start_from_scenario

- **Route**: `POST /api/sessions/from-scenario`
- **Signature**: `def start_from_scenario(body: ScenarioIn | ScenarioInDict, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `body`
- **Params**: `body` — JSON body
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, StartFromScenarioErrorBody]`
- **Error**: `StartFromScenarioErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `ScenarioIn` | `witnessed/models/scenario_in.py` |
| `ScenarioInDict` | `witnessed/models/scenario_in.py` |
| `StartFromScenarioErrorBody` | `witnessed/errors/start_from_scenario_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.subjects

- **Route**: `GET /api/subjects`
- **Signature**: `def subjects(*, request_options: RequestOptionsOrDict | None = None)`
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, RawError]`
- **Error**: `RawError` — **Case B**

### client.triage

- **Route**: `POST /api/sessions/{session_id}/lines/{line_id}/triage`
- **Signature**: `def triage(session_id: str, line_id: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `session_id`, `line_id`
- **Params**: `session_id` — path · `line_id` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, TriageErrorBody]`
- **Error**: `TriageErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `TriageErrorBody` | `witnessed/errors/triage_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.trust

- **Route**: `GET /api/trust/{subject}`
- **Signature**: `def trust(subject: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `subject`
- **Params**: `subject` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, TrustErrorBody]`
- **Error**: `TrustErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `TrustErrorBody` | `witnessed/errors/trust_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

### client.trust_history

- **Route**: `GET /api/trust/{subject}/history`
- **Signature**: `def trust_history(subject: str, *, request_options: RequestOptionsOrDict | None = None)`
  - required, positional: `subject`
- **Params**: `subject` — path
- **Returns (parsed)**: `Any`
- **Returns (raw)**: `ApiResult[Any, TrustHistoryErrorBody]`
- **Error**: `TrustHistoryErrorBody` — **Case A (typed)**
- **Error arms**: `HttpValidationError` [422] · `RawError` [anything unmapped]

| Type | Source |
| --- | --- |
| `TrustHistoryErrorBody` | `witnessed/errors/trust_history_error.py` |
| `HttpValidationError` | `witnessed/models/http_validation_error.py` |

