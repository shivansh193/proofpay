// Builds the submission video: slides (slides.html, one <section> each) around the recorded walkthrough
// (out/demo.mp4 from record-demo.mjs), at 1920x1080 / 30 fps with short fades and a silent audio track.
//   CHANNEL=msedge node make-video.mjs   ->  out/proofpay-demo.mp4 and out/preview-sheet.jpg
import { chromium } from "playwright";
import { execFileSync } from "node:child_process";
import { mkdirSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const OUT = process.env.OUT ?? "out";
const FADE = 0.4;
// Order and on-screen seconds. "demo" is the walkthrough at its own length.
const PLAN = [
  ["title", 6],
  ["glance", 10],
  ["trust", 10],
  ["demo", null],
  ["results", 12],
  ["outro", 6],
];
const LIMIT = 180;

const ffmpeg = (args) => execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...args], { stdio: "inherit" });
const probe = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString());

async function main() {
  const dir = join(OUT, "slides");
  mkdirSync(dir, { recursive: true });
  const browser = await chromium.launch({ channel: process.env.CHANNEL || undefined });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(pathToFileURL(resolve("slides.html")).href);
  for (const [id] of PLAN.filter(([id]) => id !== "demo")) {
    await page.locator(`#${id}`).screenshot({ path: join(dir, `${id}.png`) });
  }
  await browser.close();

  const demo = join(OUT, "demo.mp4");
  const lengths = PLAN.map(([id, s]) => (id === "demo" ? probe(demo) : s));
  const total = lengths.reduce((a, b) => a + b, 0);
  console.log(`plan: ${PLAN.map(([id], i) => `${id} ${lengths[i].toFixed(1)}s`).join(", ")} = ${total.toFixed(1)}s`);
  if (total >= LIMIT) throw new Error(`video is ${total.toFixed(1)}s, over the ${LIMIT}s limit`);

  // One segment per item, same format, each faded in and out against the page background.
  const segs = [];
  PLAN.forEach(([id], i) => {
    const seg = join(OUT, `seg-${i}-${id}.mp4`);
    const d = lengths[i];
    const fades = `fade=t=in:st=0:d=${FADE}:color=0xf6f7f9,fade=t=out:st=${(d - FADE).toFixed(2)}:d=${FADE}:color=0xf6f7f9`;
    if (id === "demo") {
      // 1440x900 scaled to 1728x1080 and centred on the background colour.
      ffmpeg(["-i", demo, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", String(d),
        "-vf", `scale=1728:1080:flags=lanczos,pad=1920:1080:96:0:0xf6f7f9,fps=30,${fades},format=yuv420p`,
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "128k", "-shortest", seg]);
    } else {
      ffmpeg(["-loop", "1", "-framerate", "30", "-t", String(d), "-i", join(dir, `${id}.png`), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", `${fades},format=yuv420p`, "-map", "0:v", "-map", "1:a", "-t", String(d),
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-tune", "stillimage", "-c:a", "aac", "-b:a", "128k", seg]);
    }
    segs.push(seg);
  });

  const list = join(OUT, "segments.txt");
  const { writeFileSync } = await import("node:fs");
  writeFileSync(list, segs.map((s) => `file '${resolve(s).replace(/\\/g, "/")}'`).join("\n"));
  const final = join(OUT, "proofpay-demo.mp4");
  ffmpeg(["-f", "concat", "-safe", "0", "-i", list, "-c", "copy", "-movflags", "+faststart", final]);

  // 20-frame preview sheet over the whole video.
  const dur = probe(final);
  ffmpeg(["-i", final, "-vf", `fps=20/${dur.toFixed(2)},scale=480:-1,tile=5x4`, "-frames:v", "1", join(OUT, "preview-sheet.jpg")]);
  console.log(`wrote ${final} (${dur.toFixed(1)}s) and preview-sheet.jpg`);
}

main().catch((e) => { console.error(e); process.exit(1); });
