import * as s from "../core/validation/index.js";
import type { JsonValue, Schema } from "../core/validation/schema.js";

export type ScenarioIn = {
  scenario: string;
  /** Properties the service sent or accepts beyond those declared. */
  additionalProperties?: Record<string, JsonValue>;
};

export const scenarioInSchema: Schema<ScenarioIn> = s.object<ScenarioIn>(
  {
    scenario: s.string(),
  },
  { additionalProperties: s.json() },
);
