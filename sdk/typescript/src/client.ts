import type { ClientOptions } from "./client-options.js";
import { ApiError, type Declared, type Undeclared } from "./core/api-error.js";
import type { ApiPromise } from "./core/api-promise.js";
import type { RequestOptions } from "./core/api-request.js";
import { noneAuth } from "./core/auth/schemes.js";
import { buildCoreClientOptions } from "./core/client-options.js";
import { RawClient } from "./core/raw-client.js";
import type { ErrorDecoders } from "./core/response-decoder.js";
import * as host from "./core/runtime-environment.js";
import { uuid } from "./core/uuid.js";
import * as s from "./core/validation/index.js";
import { decideInSchema, type DecideIn } from "./models/decide-in.js";
import { exitInInternalSchema, type ExitIn } from "./models/exit-in.js";
import { httpValidationErrorSchema, type HttpValidationError } from "./models/http-validation-error.js";
import { notMineInSchema, type NotMineIn } from "./models/not-mine-in.js";
import { outcomeInSchema, type OutcomeIn } from "./models/outcome-in.js";
import { planInSchema, type PlanIn } from "./models/plan-in.js";
import { purchaseInSchema, type PurchaseIn } from "./models/purchase-in.js";
import { scenarioInSchema, type ScenarioIn } from "./models/scenario-in.js";
import { seedInInternalSchema, type SeedIn } from "./models/seed-in.js";
import { startInInternalSchema, type StartIn } from "./models/start-in.js";
import { buildServers, type Servers } from "./servers.js";

/**
 * Witnessed API: PayPal holds that capture only what the camera saw handed over.
 */
export class WitnessedClient {
  readonly #rawClient: RawClient;
  readonly #servers: Servers;

  constructor(options: ClientOptions = {}) {
    this.#rawClient = new RawClient({
      ...buildCoreClientOptions(options, "WITNESSED_CLIENT_LOG"),
      defaultHeaders: [
        { name: "User-Agent", value: "WitnessedClient/1.0.0 TypeScript", schema: s.string() },
        { name: "X-APIMatic-Lang", value: "TypeScript", schema: s.string() },
        { name: "X-APIMatic-Package-Version", value: "1.0.0", schema: s.string() },
        { name: "X-APIMatic-Gen-Version", value: "4.0.0", schema: s.string() },
        { name: "X-APIMatic-OS", value: host.operatingSystem(), schema: s.optional(s.string()) },
        { name: "X-APIMatic-Runtime", value: host.runtimeDescription(), schema: s.optional(s.string()) },
      ],
      defaultQuery: [],
      defaultPathParams: [],
    });

    this.#servers = buildServers(options);
  }

  /**
   * Agent Complete
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.AgentCompleteError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  agentComplete(
    request: WitnessedClient.AgentCompleteRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.AgentCompleteError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/agents/purchases/{purchase_id}/complete"),
        auth: noneAuth,
        pathParams: [{ name: "purchase_id", value: request.purchaseId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.AgentCompleteError,
      },
      options,
    );
  }

  /**
   * Agent Decide
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.AgentDecideError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  agentDecide(
    request: WitnessedClient.AgentDecideRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.AgentDecideError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/agents/purchases/{purchase_id}/decide"),
        auth: noneAuth,
        pathParams: [{ name: "purchase_id", value: request.purchaseId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: decideInSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.AgentDecideError,
      },
      options,
    );
  }

  /**
   * Agent Outcome
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.AgentOutcomeError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  agentOutcome(
    request: WitnessedClient.AgentOutcomeRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.AgentOutcomeError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/agents/purchases/{purchase_id}/outcome"),
        auth: noneAuth,
        pathParams: [{ name: "purchase_id", value: request.purchaseId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: outcomeInSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.AgentOutcomeError,
      },
      options,
    );
  }

  /**
   * Agent Plan
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.AgentPlanError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  agentPlan(
    request: WitnessedClient.AgentPlanRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.AgentPlanError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/agents/{agent_id}/plan"),
        auth: noneAuth,
        pathParams: [{ name: "agent_id", value: request.agentId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: planInSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.AgentPlanError,
      },
      options,
    );
  }

  /**
   * Agent Purchase
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.AgentPurchaseError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  agentPurchase(
    request: WitnessedClient.AgentPurchaseRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.AgentPurchaseError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/agents/{agent_id}/purchases"),
        auth: noneAuth,
        pathParams: [{ name: "agent_id", value: request.agentId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: purchaseInSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.AgentPurchaseError,
      },
      options,
    );
  }

  /**
   * Agent Status
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.AgentStatusError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  agentStatus(
    request: WitnessedClient.AgentStatusRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.AgentStatusError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/agents/{agent_id}"),
        auth: noneAuth,
        pathParams: [{ name: "agent_id", value: request.agentId, schema: s.string() }],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.AgentStatusError,
      },
      options,
    );
  }

  /**
   * Agreement
   *
   * @remarks
   * How often staff agreed with the AI. "check_bag" / "review_footage" defer to staff, so they're
   * counted separately rather than as agreement.
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  agreement(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/ai/agreement"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Authorize
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.AuthorizeError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  authorize(
    request: WitnessedClient.AuthorizeRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.AuthorizeError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/sessions/{session_id}/authorize"),
        auth: noneAuth,
        pathParams: [{ name: "session_id", value: request.sessionId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.AuthorizeError,
      },
      options,
    );
  }

  /**
   * Config
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  config(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/config"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Evidence
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.EvidenceError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  evidence(
    request: WitnessedClient.EvidenceRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.EvidenceError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/sessions/{session_id}/evidence"),
        auth: noneAuth,
        pathParams: [{ name: "session_id", value: request.sessionId, schema: s.string() }],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.EvidenceError,
      },
      options,
    );
  }

  /**
   * Exit Check
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.ExitCheckError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  exitCheck(
    request: WitnessedClient.ExitCheckRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.ExitCheckError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/sessions/{session_id}/exit"),
        auth: noneAuth,
        pathParams: [{ name: "session_id", value: request.sessionId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: exitInInternalSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.ExitCheckError,
      },
      options,
    );
  }

  /**
   * Explain
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.ExplainError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  explain(
    request: WitnessedClient.ExplainRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.ExplainError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/sessions/{session_id}/explain"),
        auth: noneAuth,
        pathParams: [{ name: "session_id", value: request.sessionId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.ExplainError,
      },
      options,
    );
  }

  /**
   * List Holds
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  listHolds(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/holds"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Not Mine
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.NotMineError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  notMine(
    request: WitnessedClient.NotMineRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.NotMineError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/sessions/{session_id}/lines/{line_id}/not-mine"),
        auth: noneAuth,
        pathParams: [
          { name: "session_id", value: request.sessionId, schema: s.string() },
          { name: "line_id", value: request.lineId, schema: s.string() },
        ],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: notMineInSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.NotMineError,
      },
      options,
    );
  }

  /**
   * Paypal Webhook
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  paypalWebhook(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/webhooks/paypal"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Rescue Hold
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.RescueHoldError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  rescueHold(
    request: WitnessedClient.RescueHoldRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.RescueHoldError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/holds/{session_id}/rescue"),
        auth: noneAuth,
        pathParams: [{ name: "session_id", value: request.sessionId, schema: s.string() }],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.RescueHoldError,
      },
      options,
    );
  }

  /**
   * Scenarios
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  scenarios(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/scenarios"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Seed History
   *
   * @remarks
   * Add SIMULATED weekly verified visits for a demo customer (labelled simulated).
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.SeedHistoryError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  seedHistory(
    request: WitnessedClient.SeedHistoryRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.SeedHistoryError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/seed-history"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: seedInInternalSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.SeedHistoryError,
      },
      options,
    );
  }

  /**
   * Seed Holds
   *
   * @remarks
   * Add SIMULATED holds of different ages (offline stand-in) to the timeline.
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  seedHolds(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/demo/seed-holds"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Session
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.SessionError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  session(
    request: WitnessedClient.SessionRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.SessionError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/sessions/{session_id}"),
        auth: noneAuth,
        pathParams: [{ name: "session_id", value: request.sessionId, schema: s.string() }],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.SessionError,
      },
      options,
    );
  }

  /**
   * Sessions
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  sessions(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/sessions"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Sim Results
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  simResults(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/sim"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Start
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.StartError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  start(
    request: WitnessedClient.StartRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.StartError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/sessions"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: startInInternalSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.StartError,
      },
      options,
    );
  }

  /**
   * Start From Scenario
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.StartFromScenarioError} when the API answers with an error
   * status — narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  startFromScenario(
    request: WitnessedClient.StartFromScenarioRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.StartFromScenarioError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/sessions/from-scenario"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "json", value: request.body, schema: scenarioInSchema },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.StartFromScenarioError,
      },
      options,
    );
  }

  /**
   * Subjects
   *
   * @returns Successful Response
   *
   * @throws {@link ApiError} when the API answers with an error status
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  subjects(options?: RequestOptions): ApiPromise<Record<string, unknown>, ApiError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/subjects"),
        auth: noneAuth,
        pathParams: [],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: ApiError,
      },
      options,
    );
  }

  /**
   * Triage
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.TriageError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  triage(
    request: WitnessedClient.TriageRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.TriageError> {
    return this.#rawClient.execute(
      {
        method: "POST",
        urlTemplate: this.#servers.default("/api/sessions/{session_id}/lines/{line_id}/triage"),
        auth: noneAuth,
        pathParams: [
          { name: "session_id", value: request.sessionId, schema: s.string() },
          { name: "line_id", value: request.lineId, schema: s.string() },
        ],
        query: [],
        headers: [{ name: "Idempotency-Key", value: uuid(), schema: s.string() }],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.TriageError,
      },
      options,
    );
  }

  /**
   * Trust
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.TrustError} when the API answers with an error status — narrow
   * on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  trust(
    request: WitnessedClient.TrustRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.TrustError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/trust/{subject}"),
        auth: noneAuth,
        pathParams: [{ name: "subject", value: request.subject, schema: s.string() }],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.TrustError,
      },
      options,
    );
  }

  /**
   * Trust History
   *
   * @remarks
   * Score just after each event, plus now: the trust inspector's line chart.
   *
   * @returns Successful Response
   *
   * @throws {@link WitnessedClient.TrustHistoryError} when the API answers with an error status —
   * narrow on `err.payload.kind`
   *
   * @throws {@link WitnessedError} when no usable response was produced: a connection failure, a
   * timeout, a body that would not decode, a value that would not encode, or a credential that
   * could not be obtained
   */
  trustHistory(
    request: WitnessedClient.TrustHistoryRequest,
    options?: RequestOptions,
  ): ApiPromise<Record<string, unknown>, WitnessedClient.TrustHistoryError> {
    return this.#rawClient.execute(
      {
        method: "GET",
        urlTemplate: this.#servers.default("/api/trust/{subject}/history"),
        auth: noneAuth,
        pathParams: [{ name: "subject", value: request.subject, schema: s.string() }],
        query: [],
        headers: [],
        body: { kind: "empty" },
      },
      {
        success: { kind: "json", schema: s.record(s.string(), s.unknown()) },
        errorFactory: WitnessedClient.TrustHistoryError,
      },
      options,
    );
  }
}

export namespace WitnessedClient {
  export type AgentCompleteRequest = {
    purchaseId: string;
  };

  export class AgentCompleteError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<AgentCompleteError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type AgentDecideRequest = {
    purchaseId: string;
    body: DecideIn;
  };

  export class AgentDecideError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<AgentDecideError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type AgentOutcomeRequest = {
    purchaseId: string;
    body: OutcomeIn;
  };

  export class AgentOutcomeError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<AgentOutcomeError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type AgentPlanRequest = {
    agentId: string;
    body: PlanIn;
  };

  export class AgentPlanError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<AgentPlanError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type AgentPurchaseRequest = {
    agentId: string;
    body: PurchaseIn;
  };

  export class AgentPurchaseError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<AgentPurchaseError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type AgentStatusRequest = {
    agentId: string;
  };

  export class AgentStatusError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<AgentStatusError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type AuthorizeRequest = {
    sessionId: string;
  };

  export class AuthorizeError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<AuthorizeError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type EvidenceRequest = {
    sessionId: string;
  };

  export class EvidenceError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<EvidenceError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type ExitCheckRequest = {
    sessionId: string;
    body: ExitIn;
  };

  export class ExitCheckError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<ExitCheckError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type ExplainRequest = {
    sessionId: string;
  };

  export class ExplainError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<ExplainError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type NotMineRequest = {
    sessionId: string;
    lineId: string;
    body: NotMineIn;
  };

  export class NotMineError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<NotMineError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type RescueHoldRequest = {
    sessionId: string;
  };

  export class RescueHoldError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<RescueHoldError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type SeedHistoryRequest = {
    body: SeedIn;
  };

  export class SeedHistoryError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<SeedHistoryError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type SessionRequest = {
    sessionId: string;
  };

  export class SessionError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<SessionError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type StartRequest = {
    body: StartIn;
  };

  export class StartError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<StartError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type StartFromScenarioRequest = {
    body: ScenarioIn;
  };

  export class StartFromScenarioError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<StartFromScenarioError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type TriageRequest = {
    sessionId: string;
    lineId: string;
  };

  export class TriageError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<TriageError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type TrustRequest = {
    subject: string;
  };

  export class TrustError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<TrustError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }

  export type TrustHistoryRequest = {
    subject: string;
  };

  export class TrustHistoryError extends ApiError {
    declare readonly payload: Declared<"httpValidationError", HttpValidationError> | Undeclared;

    static readonly errors: ErrorDecoders<TrustHistoryError> = [
      { on: 422, kind: "httpValidationError", decode: { kind: "json", schema: httpValidationErrorSchema } },
    ];
  }
}
