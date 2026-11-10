<!-- Generated file — do not edit; regenerated with the SDK. -->

# WitnessedClient — ungrouped operations

Accessor: `client` (the client itself) · Source: `src/client.ts` · 28 operations · Request and error types: namespace `WitnessedClient`

Operations the spec leaves untagged are methods on the client rather than on a resource, so there is no accessor property to go through. The request type still lives in a namespace merged onto the exported class, so you write `WitnessedClient.AgentCompleteRequest`.

**Type sources**: every type an operation names, with the file that declares it and the schema value exported beside it. Import every name from `witnessed`; the `Source` path is where to **read** the shape, never what to import. `ApiError`, the runtime error family and the file vocabulary are excluded — see sdk-map.md.

### agentComplete

- **Signature**: `agentComplete(request: WitnessedClient.AgentCompleteRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.AgentCompleteError>`
- **Wire**: `POST /api/agents/purchases/{purchase_id}/complete`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.AgentCompleteError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.AgentCompleteRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `purchaseId` | `path` | `purchase_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### agentDecide

- **Signature**: `agentDecide(request: WitnessedClient.AgentDecideRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.AgentDecideError>`
- **Wire**: `POST /api/agents/purchases/{purchase_id}/decide`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.AgentDecideError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.AgentDecideRequest` (2):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `purchaseId` | `path` | `purchase_id` | `string` | yes |
| `body` | `body` | — | `DecideIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `DecideIn` | `decideInSchema` | `src/models/decide-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### agentOutcome

- **Signature**: `agentOutcome(request: WitnessedClient.AgentOutcomeRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.AgentOutcomeError>`
- **Wire**: `POST /api/agents/purchases/{purchase_id}/outcome`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.AgentOutcomeError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.AgentOutcomeRequest` (2):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `purchaseId` | `path` | `purchase_id` | `string` | yes |
| `body` | `body` | — | `OutcomeIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `OutcomeIn` | `outcomeInSchema` | `src/models/outcome-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### agentPlan

- **Signature**: `agentPlan(request: WitnessedClient.AgentPlanRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.AgentPlanError>`
- **Wire**: `POST /api/agents/{agent_id}/plan`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.AgentPlanError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.AgentPlanRequest` (2):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `agentId` | `path` | `agent_id` | `string` | yes |
| `body` | `body` | — | `PlanIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `PlanIn` | `planInSchema` | `src/models/plan-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### agentPurchase

- **Signature**: `agentPurchase(request: WitnessedClient.AgentPurchaseRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.AgentPurchaseError>`
- **Wire**: `POST /api/agents/{agent_id}/purchases`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.AgentPurchaseError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.AgentPurchaseRequest` (2):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `agentId` | `path` | `agent_id` | `string` | yes |
| `body` | `body` | — | `PurchaseIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `PurchaseIn` | `purchaseInSchema` | `src/models/purchase-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### agentStatus

- **Signature**: `agentStatus(request: WitnessedClient.AgentStatusRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.AgentStatusError>`
- **Wire**: `GET /api/agents/{agent_id}`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.AgentStatusError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.AgentStatusRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `agentId` | `path` | `agent_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### agreement

- **Signature**: `agreement(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/ai/agreement`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### authorize

- **Signature**: `authorize(request: WitnessedClient.AuthorizeRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.AuthorizeError>`
- **Wire**: `POST /api/sessions/{session_id}/authorize`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.AuthorizeError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.AuthorizeRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### config

- **Signature**: `config(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/config`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### evidence

- **Signature**: `evidence(request: WitnessedClient.EvidenceRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.EvidenceError>`
- **Wire**: `GET /api/sessions/{session_id}/evidence`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.EvidenceError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.EvidenceRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### exitCheck

- **Signature**: `exitCheck(request: WitnessedClient.ExitCheckRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.ExitCheckError>`
- **Wire**: `POST /api/sessions/{session_id}/exit`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.ExitCheckError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.ExitCheckRequest` (2):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |
| `body` | `body` | — | `ExitIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `ExitIn` | `exitInSchema` | `src/models/exit-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### explain

- **Signature**: `explain(request: WitnessedClient.ExplainRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.ExplainError>`
- **Wire**: `POST /api/sessions/{session_id}/explain`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.ExplainError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.ExplainRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### listHolds

- **Signature**: `listHolds(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/holds`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### notMine

- **Signature**: `notMine(request: WitnessedClient.NotMineRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.NotMineError>`
- **Wire**: `POST /api/sessions/{session_id}/lines/{line_id}/not-mine`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.NotMineError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.NotMineRequest` (3):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |
| `lineId` | `path` | `line_id` | `string` | yes |
| `body` | `body` | — | `NotMineIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `NotMineIn` | `notMineInSchema` | `src/models/not-mine-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### paypalWebhook

- **Signature**: `paypalWebhook(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `POST /api/webhooks/paypal`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### rescueHold

- **Signature**: `rescueHold(request: WitnessedClient.RescueHoldRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.RescueHoldError>`
- **Wire**: `POST /api/holds/{session_id}/rescue`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.RescueHoldError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.RescueHoldRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### scenarios

- **Signature**: `scenarios(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/scenarios`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### seedHistory

- **Signature**: `seedHistory(request: WitnessedClient.SeedHistoryRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.SeedHistoryError>`
- **Wire**: `POST /api/demo/seed-history`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.SeedHistoryError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.SeedHistoryRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `body` | `body` | `SeedIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `SeedIn` | `seedInSchema` | `src/models/seed-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### seedHolds

- **Signature**: `seedHolds(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `POST /api/demo/seed-holds`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### session

- **Signature**: `session(request: WitnessedClient.SessionRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.SessionError>`
- **Wire**: `GET /api/sessions/{session_id}`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.SessionError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.SessionRequest` (1):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### sessions

- **Signature**: `sessions(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/sessions`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### simResults

- **Signature**: `simResults(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/sim`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### start

- **Signature**: `start(request: WitnessedClient.StartRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.StartError>`
- **Wire**: `POST /api/sessions`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.StartError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.StartRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `body` | `body` | `StartIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `StartIn` | `startInSchema` | `src/models/start-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### startFromScenario

- **Signature**: `startFromScenario(request: WitnessedClient.StartFromScenarioRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.StartFromScenarioError>`
- **Wire**: `POST /api/sessions/from-scenario`
- **Auth**: none — public; no credential is sent
- **Request body**: `application/json` — the `body` field
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.StartFromScenarioError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.StartFromScenarioRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `body` | `body` | `ScenarioIn` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `ScenarioIn` | `scenarioInSchema` | `src/models/scenario-in.ts` |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### subjects

- **Signature**: `subjects(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError>`
- **Wire**: `GET /api/subjects`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"` — untyped, `payload.kind` always `"undeclared"`

### triage

- **Signature**: `triage(request: WitnessedClient.TriageRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.TriageError>`
- **Wire**: `POST /api/sessions/{session_id}/lines/{line_id}/triage`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **SDK-sent**: `header Idempotency-Key` (minted per call)
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.TriageError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.TriageRequest` (2):

| Field | Channel | Wire | Type | Req |
| --- | --- | --- | --- | --- |
| `sessionId` | `path` | `session_id` | `string` | yes |
| `lineId` | `path` | `line_id` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### trust

- **Signature**: `trust(request: WitnessedClient.TrustRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.TrustError>`
- **Wire**: `GET /api/trust/{subject}`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.TrustError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.TrustRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `subject` | `path` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

### trustHistory

- **Signature**: `trustHistory(request: WitnessedClient.TrustHistoryRequest, options?: RequestOptions): ApiPromise<Record<string, unknown>, WitnessedClient.TrustHistoryError>`
- **Wire**: `GET /api/trust/{subject}/history`
- **Auth**: none — public; no credential is sent
- **Request body**: none — no `Content-Type` header is sent
- **Returns**: `Record<string, unknown>` — a bare `application/json` map; the success type *is* the map
- **Error**: `WitnessedError` with `kind: "api"`, an instance of `WitnessedClient.TrustHistoryError` — **typed arms**, narrowed on `err.payload.kind`
- **Error arms**: `"httpValidationError"` [422] `HttpValidationError` · `"undeclared"` [any other] `rawBody: ArrayBuffer`

**Fields** — `WitnessedClient.TrustHistoryRequest` (1):

| Field | Channel | Type | Req |
| --- | --- | --- | --- |
| `subject` | `path` | `string` | yes |

| Type | Schema value | Source |
| --- | --- | --- |
| `HttpValidationError` | `httpValidationErrorSchema` | `src/models/http-validation-error.ts` |

