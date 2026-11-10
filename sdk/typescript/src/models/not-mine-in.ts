import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

export type NotMineIn = {
  footageShowsTake: boolean;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const notMineInSchema: Schema<NotMineIn> = s.object<NotMineIn>(
  {
    footageShowsTake: s.boolean(),
    _keysMap: {
      footageShowsTake: "footage_shows_take",
    },
  },
  { additionalProperties: s.json() },
);
