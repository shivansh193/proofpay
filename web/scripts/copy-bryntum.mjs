// Copies Bryntum's prebuilt UMD bundle and styles into public/bryntum/, so the page
// loads them with plain <script>/<link> tags. Importing the package instead makes
// `next build` type-check a 16 MB .d.ts and minify 4.6 MB of obfuscated trial code,
// which took over 7 GB of RAM.
import { cpSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const web = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(web, "node_modules", "@bryntum", "scheduler");
const out = join(web, "public", "bryntum");
mkdirSync(join(out, "fontawesome"), { recursive: true });
for (const f of ["scheduler.umd.js", "scheduler.css", "stockholm-dark.css"]) cpSync(join(src, f), join(out, f));
cpSync(join(src, "fontawesome", "css"), join(out, "fontawesome", "css"), { recursive: true });
cpSync(join(src, "fontawesome", "webfonts"), join(out, "fontawesome", "webfonts"), { recursive: true });
console.log("bryntum assets copied to public/bryntum");
