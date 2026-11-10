import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

export type SeedIn = {
  customerId: string;
  /** @default 12 */
  visits?: number;
  /** @default 250 */
  basketInr?: number;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

const seedInProperties: s.Shape<SeedIn> = {
  customerId: s.string(),
  visits: s.defaulted(s.int(), 12),
  basketInr: s.defaulted(s.float64(), 250),
  _keysMap: {
    customerId: "customer_id",
    basketInr: "basket_inr",
  },
};

export const seedInInternalSchema: Schema<SeedIn> = s.object<SeedIn>(seedInProperties, {
  additionalProperties: s.json(),
});

export const seedInSchema: Schema<SeedIn> = s.lazySchema(() =>
  s.object<SeedIn>(
    {
      ...seedInProperties,
      visits: s.defaulted(s.int().check(s.gte(1), s.lte(60)), 12),
      basketInr: s.defaulted(s.float64().check(s.gt(0)), 250),
    },
    { additionalProperties: s.json() },
  ),
);
