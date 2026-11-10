import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

export type PurchaseIn = {
  items: Record<string, unknown>[];
  task?: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const purchaseInSchema: Schema<PurchaseIn> = s.object<PurchaseIn>(
  {
    items: s.array(s.record(s.string(), s.unknown())),
    task: s.optional(s.string()),
  },
  { additionalProperties: s.json() },
);
