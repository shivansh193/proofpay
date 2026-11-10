import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

export type DecideIn = {
  approve: boolean;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const decideInSchema: Schema<DecideIn> = s.object<DecideIn>(
  {
    approve: s.boolean(),
  },
  { additionalProperties: s.json() },
);
