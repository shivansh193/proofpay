import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

export type OutcomeIn = {
  outcome: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const outcomeInSchema: Schema<OutcomeIn> = s.object<OutcomeIn>(
  {
    outcome: s.string(),
  },
  { additionalProperties: s.json() },
);
