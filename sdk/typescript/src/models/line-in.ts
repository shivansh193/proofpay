import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";
import { evidenceSchema, type Evidence } from "./unions/evidence.js";

export type LineIn = {
  lineId: string;
  name: string;
  sku: string;
  price: number;
  p: number;
  evidence?: Evidence;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

const lineInProperties: s.Shape<LineIn> = {
  lineId: s.string(),
  name: s.string(),
  sku: s.string(),
  price: s.float64(),
  p: s.float64(),
  evidence: s.optional(s.lazy(() => evidenceSchema)),
  _keysMap: {
    lineId: "line_id",
  },
};

export const lineInInternalSchema: Schema<LineIn> = s.object<LineIn>(lineInProperties, {
  additionalProperties: s.json(),
});

export const lineInSchema: Schema<LineIn> = s.lazySchema(() =>
  s.object<LineIn>(
    {
      ...lineInProperties,
      price: s.float64().check(s.gt(0)),
      p: s.float64().check(s.gte(0), s.lte(1)),
    },
    { additionalProperties: s.json() },
  ),
);
