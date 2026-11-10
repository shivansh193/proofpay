import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { lineInInternalSchema, lineInSchema, type LineIn } from "./line-in.js";

export type StartIn = {
  customerId: string;
  lines: LineIn[];
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

const startInProperties: s.Shape<StartIn> = {
  customerId: s.string(),
  lines: s.array(s.lazy(() => lineInInternalSchema)),
  _keysMap: {
    customerId: "customer_id",
  },
};

export const startInInternalSchema: Schema<StartIn> = s.object<StartIn>(startInProperties, {
  additionalProperties: s.json(),
});

export const startInSchema: Schema<StartIn> = s.lazySchema(() =>
  s.object<StartIn>(
    {
      ...startInProperties,
      lines: s.array(s.lazy(() => lineInSchema)),
    },
    { additionalProperties: s.json() },
  ),
);
