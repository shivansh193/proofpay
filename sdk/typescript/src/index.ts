export { WitnessedClient } from "./client.js";
export type { ClientOptions } from "./client-options.js";

export { decideInSchema, type DecideIn } from "./models/decide-in.js";
export { evidenceSchema, type Evidence } from "./models/unions/evidence.js";
export { exitInSchema, type ExitIn } from "./models/exit-in.js";
export { httpValidationErrorSchema, type HttpValidationError } from "./models/http-validation-error.js";
export {
  httpValidationErrorErrorSchema,
  type HttpValidationErrorError,
} from "./models/http-validation-error-error.js";
export { lineInSchema, type LineIn } from "./models/line-in.js";
export { locationSchema, type Location } from "./models/unions/location.js";
export { notMineInSchema, type NotMineIn } from "./models/not-mine-in.js";
export { outcomeInSchema, type OutcomeIn } from "./models/outcome-in.js";
export { planInSchema, type PlanIn } from "./models/plan-in.js";
export { purchaseInSchema, type PurchaseIn } from "./models/purchase-in.js";
export { scenarioInSchema, type ScenarioIn } from "./models/scenario-in.js";
export { seedInSchema, type SeedIn } from "./models/seed-in.js";
export { startInSchema, type StartIn } from "./models/start-in.js";
export { validationErrorSchema, type ValidationError } from "./models/validation-error.js";

export {
  CoreError as WitnessedError,
  ResponseError,
  DecodeError,
  EncodeError,
  ConnectionError,
  TimeoutError,
  AuthError,
  PaginationError,
  ConfigurationError,
} from "./core/errors.js";
export { ApiError } from "./core/api-error.js";
export { SchemaError } from "./core/validation/schema-error.js";
export {
  defaultLoggingOptions,
  type LoggingOptions,
  type RequestLoggingOptions,
  type Logger,
  type LogDetails,
  type HttpRequestDetails,
  type RequestHeadersDetails,
  type RequestBodyDetails,
  type HttpResponseDetails,
  type ResponseHeadersDetails,
  type HttpRetryingDetails,
  type HttpFailedDetails,
  type LogLevel,
} from "./core/logging.js";
export type { ApiPromise, ApiResult } from "./core/api-promise.js";
export type { Pageable, PageableApiResult } from "./core/pagination/pageable.js";
export type { HttpMethod, RequestOptions } from "./core/api-request.js";
export type { RetryOptions, RequestRetryOptions, RetryAttempt, RetryReason } from "./core/retry.js";
export type { BinaryContent, BinaryData, BinaryErrorContent, FileData, FileInput } from "./core/binary.js";
export type { ErrorKind } from "./core/errors.js";
export type { Declared, Undeclared } from "./core/api-error.js";
export type { Schema, EnumSchema, Encoded, ValidationResult, JsonValue } from "./core/validation/schema.js";
