// Records the demo path from docs/video-script.md as one silent video with a visible cursor and captions,
// plus a screenshot per beat. Run against a server with a fresh database:
//   BASE=http://localhost:8001 OUT=out node record-demo.mjs
// Then narrate over out/demo.mp4. Captions are part of the frame; pass CAPTIONS=0 for a clean take.
import { chromium } from "playwright";
import { execFileSync } from "node:child_process";
import { mkdirSync, readdirSync, renameSync, rmSync } from "node:fs";
import { join } from "node:path";

const BASE = process.env.BASE ?? "http://localhost:8001";
const OUT = process.env.OUT ?? "out";
const CAPTIONS = process.env.CAPTIONS !== "0";
const W = 1440, H = 900;

// Overlay: a cursor and a caption bar that survive page navigations (state in sessionStorage).
const OVERLAY = `(() => {
  const add = () => {
    if (document.getElementById("pp-cursor")) return;
    const c = document.createElement("div");
    c.id = "pp-cursor";
    c.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24"><path d="M3 2l7 19 2.5-7.5L20 11z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
    const pos = JSON.parse(sessionStorage.getItem("ppCursor") || '{"x":720,"y":450}');
    Object.assign(c.style, { position: "fixed", left: "0", top: "0", zIndex: 2147483647, pointerEvents: "none",
      transform: "translate(" + pos.x + "px," + pos.y + "px)", transition: "transform 0.55s cubic-bezier(.3,.7,.2,1)" });
    document.documentElement.appendChild(c);
    const b = document.createElement("div");
    b.id = "pp-caption";
    Object.assign(b.style, { position: "fixed", left: "50%", bottom: "28px", transform: "translateX(-50%)", zIndex: 2147483646,
      pointerEvents: "none", maxWidth: "1100px", padding: "12px 22px", borderRadius: "10px", font: "600 22px/1.35 system-ui, sans-serif",
      color: "#fff", background: "rgba(15,18,28,.86)", boxShadow: "0 6px 24px rgba(0,0,0,.25)", textAlign: "center",
      transition: "opacity .25s", opacity: "0" });
    document.documentElement.appendChild(b);
    const text = sessionStorage.getItem("ppCaption") || "";
    b.textContent = text; b.style.opacity = text ? "1" : "0";
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", add); else add();
})();`;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  rmSync(OUT, { recursive: true, force: true });
  mkdirSync(join(OUT, "shots"), { recursive: true });
  // CHANNEL=msedge or chrome uses an installed browser instead of Playwright's download.
  const browser = await chromium.launch({ channel: process.env.CHANNEL || undefined, executablePath: process.env.CHROME || undefined });
  const ctx = await browser.newContext({
    viewport: { width: W, height: H },
    colorScheme: "light",
    recordVideo: { dir: join(OUT, "raw"), size: { width: W, height: H } },
  });
  await ctx.addInitScript(OVERLAY);
  const page = await ctx.newPage();
  let n = 0;

  const caption = async (text) => {
    if (!CAPTIONS) text = "";
    await page.evaluate((t) => {
      sessionStorage.setItem("ppCaption", t);
      const b = document.getElementById("pp-caption");
      if (b) { b.textContent = t; b.style.opacity = t ? "1" : "0"; }
    }, text);
  };
  const shot = async (name) => {
    // Screenshots skip the overlay so they can be reused as clean UI stills.
    await page.evaluate(() => document.querySelectorAll("#pp-cursor,#pp-caption").forEach((e) => (e.style.visibility = "hidden")));
    await page.screenshot({ path: join(OUT, "shots", `${String(++n).padStart(2, "0")}-${name}.png`) });
    await page.evaluate(() => document.querySelectorAll("#pp-cursor,#pp-caption").forEach((e) => (e.style.visibility = "")));
  };
  const moveTo = async (loc) => {
    await loc.scrollIntoViewIfNeeded();
    const b = await loc.boundingBox();
    const x = Math.round(b.x + b.width / 2), y = Math.round(b.y + b.height / 2);
    await page.evaluate(([x, y]) => {
      sessionStorage.setItem("ppCursor", JSON.stringify({ x, y }));
      const c = document.getElementById("pp-cursor");
      if (c) c.style.transform = `translate(${x}px,${y}px)`;
    }, [x, y]);
    await sleep(700);
  };
  const click = async (loc, after = 900) => {
    await moveTo(loc);
    await loc.click();
    await sleep(after);
  };
  const go = async (path, title) => {
    await page.goto(BASE + path);
    if (title) await page.getByRole("heading", { name: title, exact: true }).first().waitFor();
    await sleep(500);
  };
  const scrollTo = async (loc) => {
    await loc.evaluate((e) => e.scrollIntoView({ behavior: "smooth", block: "center" }));
    await sleep(1100);
  };
  const btn = (name) => page.getByRole("button", { name, exact: true });

  // 1. Home
  await go("/", null);
  await caption("Proofpay: charge for what the camera proved, at the friction your history earned");
  await sleep(3500);
  await shot("home");

  // 2. First visit
  await go("/checkout/", "Checkout");
  await caption("Asha's first visit. Vision gives each item a probability that she took it.");
  await click(btn("Start visit"), 1200);
  await page.getByText("Amul milk", { exact: false }).first().waitFor().catch(() => {});
  await scrollTo(page.getByRole("heading", { name: "Basket" }));
  await sleep(2500);
  await shot("first-visit-basket");
  await caption("No history yet, so the score is low: Strict. The hold is the basket plus a 15% buffer.");
  await scrollTo(page.getByRole("heading", { name: "Pay with PayPal" }));
  await sleep(3000);
  await shot("first-visit-policy");

  await caption("PayPal authorizes the hold. Nothing is charged yet.");
  await click(btn("Approve with PayPal (offline stand-in)"), 1200);
  await page.getByText("Walk to the exit").waitFor();
  await sleep(2000);
  await shot("authorized");

  // 3. Staff exit
  await click(page.getByRole("link", { name: "staff exit screen" }), 1200);
  await page.getByRole("heading", { name: /^Visit / }).waitFor();
  await caption("Staff exit. The AI explains the uncertain line; the staff member decides.");
  await click(btn("Explain uncertain lines (AI)"), 1500);
  await page.locator(".ai").first().waitFor();
  await sleep(3000);
  await shot("staff-ai-explainer");
  await click(btn("Taken").first(), 800);
  await caption("Close the visit: capture the verified lines, release the rest.");
  await click(btn("Close visit: capture verified, release the rest"), 1500);
  await page.getByText("captured", { exact: true }).first().waitFor();
  await caption("PayPal captured $3.57 of the $4.10 held. Every call carries an idempotency key.");
  await scrollTo(page.getByRole("heading", { name: "PayPal calls" }));
  await sleep(3500);
  await shot("paypal-calls");

  // 4. Receipt and "Not mine"
  await scrollTo(page.getByRole("link", { name: "Customer receipt" }));
  await click(page.getByRole("link", { name: "Customer receipt" }), 1200);
  await page.getByRole("heading", { name: "Receipt" }).waitFor();
  await caption("Receipt: the shampoo she put back and the buffer were never charged.");
  await scrollTo(page.getByRole("heading", { name: "Receipt" }));
  await sleep(3000);
  await shot("receipt");
  await caption("Back home: “the bread wasn't mine.” AI triage compares the claim with the evidence.");
  await scrollTo(page.getByRole("heading", { name: "Basket" }));
  const bread = page.locator("tr", { hasText: "bread" }).or(page.locator("tr", { hasText: "Bread" })).first();
  await click(bread.getByRole("button", { name: "Not mine" }), 1500);
  await page.locator(".ai", { hasText: "AI triage (" }).waitFor();
  await sleep(2500);
  await shot("not-mine-triage");
  await caption("Staff confirms. PayPal issues a partial refund.");
  await click(btn("Refund"), 1500);
  await page.getByText("Refunded", { exact: true }).first().waitFor();
  await sleep(2500);
  await shot("refunded");

  // 5. History earns Express
  await go("/trust/", "Trust inspector");
  await caption("Months later: 20 verified weekly visits (simulated, and labelled that way).");
  await sleep(1200);
  await click(btn("Add simulated history"), 2000);
  await page.getByText("Added 20 simulated").waitFor();
  await sleep(1500);
  await scrollTo(page.locator("svg").first());
  await caption("Each event's weight and decay is visible. The score is the 10th percentile, so it's earned.");
  await sleep(3500);
  await shot("trust-inspector");

  await go("/checkout/", "Checkout");
  await page.locator("select").selectOption("02-regular-visit");
  await caption("Same shopper, regular basket.");
  await click(btn("Start visit"), 1500);
  await caption("Express: every item clears the auto-capture bar. No exit check, no queue.");
  await scrollTo(page.getByRole("heading", { name: "Basket" }));
  await sleep(3500);
  await shot("express-basket");
  await click(btn("Approve with PayPal (offline stand-in)"), 1200);
  await click(page.getByRole("link", { name: "staff exit screen" }), 1200);
  await page.getByRole("heading", { name: /^Visit / }).waitFor();
  await click(btn("Close visit: capture verified, release the rest"), 1500);
  await page.getByText("captured", { exact: true }).first().waitFor();
  await caption("Captured in full, automatically.");
  await sleep(2500);
  await shot("express-captured");

  // 6. Agent
  await go("/agent/", "Agent console");
  await caption("An AI agent buys store supplies. Proofpay gates every PayPal payment it makes.");
  await sleep(1500);
  await click(btn("Plan purchase"), 1500);
  await page.getByText("Plan (").waitFor();
  await sleep(1500);
  await click(btn("Ask to pay"), 1500);
  await caption("₹1,400 is over its ₹500 limit but under 3×, so it asks a human.");
  await page.getByRole("button", { name: "Approve" }).first().waitFor();
  await sleep(3000);
  await shot("agent-ask-human");
  await click(btn("Approve"), 1500);
  const complete = btn("Payer approved: complete");
  if (await complete.count()) await click(complete.first(), 1500);
  await caption("Purchases confirmed correct raise the agent's limit.");
  await click(btn("Correct").first(), 2000);
  await sleep(1500);
  await caption("A ₹48,000 display fridge is refused outright.");
  await click(btn("SUP-FRIDGE (far over)"), 2000);
  await sleep(3000);
  await shot("agent-deny");

  // 7. Simulator
  await go("/sim/", "Simulator");
  await caption("500 simulated shoppers: learned trust roughly halves loss compared with static rules.");
  await sleep(1500);
  await scrollTo(page.locator("img").first());
  await sleep(3000);
  await shot("simulator");
  await caption("The honest part: our cautious lower bound costs more friction than the plain average.");
  await page.mouse.wheel(0, 500);
  await sleep(4000);
  await caption("");
  await sleep(800);

  const video = page.video();
  await ctx.close();
  await browser.close();
  const raw = await video.path();
  const mp4 = join(OUT, "demo.mp4");
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", raw, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
    "-movflags", "+faststart", mp4]);
  renameSync(raw, join(OUT, "demo.webm"));
  rmSync(join(OUT, "raw"), { recursive: true, force: true });
  console.log(`wrote ${mp4} and ${readdirSync(join(OUT, "shots")).length} screenshots`);
}

main().catch((e) => { console.error(e); process.exit(1); });
