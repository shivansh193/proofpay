import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { lineInInternalSchema, lineInSchema, type LineIn } from "./line-in.js";

export type ExitIn = {
  staffVerdicts?: Record<string, boolean>;
  found?: LineIn[];
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

const exitInProperties: s.Shape<ExitIn> = {
  staffVerdicts: s.optional(s.record(s.string(), s.boolean())),
  found: s.optional(s.array(s.lazy(() => lineInInternalSchema))),
  _keysMap: {
    staffVerdicts: "staff_verdicts",
  },
};

export const exitInInternalSchema: Schema<ExitIn> = s.object<ExitIn>(exitInProperties, {
  additionalProperties: s.json(),
});

export const exitInSchema: Schema<ExitIn> = s.lazySchema(() =>
  s.object<ExitIn>(
    {
      ...exitInProperties,
      found: s.optional(s.array(s.lazy(() => lineInSchema))),
    },
    { additionalProperties: s.json() },
  ),
);
