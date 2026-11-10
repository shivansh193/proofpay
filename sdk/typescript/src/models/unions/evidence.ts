import * as s from "../../core/validation/index.js";
import type { Schema } from "../../core/validation/schema.js";

export type Evidence = Record<string, unknown>;

export const evidenceSchema: Schema<Evidence> = s.of<Evidence>(s.union([s.record(s.string(), s.unknown())]));
