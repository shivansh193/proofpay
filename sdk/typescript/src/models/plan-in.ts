import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

export type PlanIn = {
  task: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const planInSchema: Schema<PlanIn> = s.object<PlanIn>(
  {
    task: s.string(),
  },
  { additionalProperties: s.json() },
);
