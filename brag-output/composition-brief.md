# Hyperframes Composition Brief: Proofpay

## Objective
Create a short launch-style brag video for Proofpay.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080, 30 fps
- Duration: 24.6 seconds

## Source Material
- Project root: `C:\Development\proofpay`
- Primary files read: `README.md`, `web/app/globals.css`, `web/app/checkout/page.tsx`, `web/app/staff/page.tsx`, `web/app/agent/page.tsx`, `demo/scenarios/01-first-visit.json`, recorded screenshots in `tools/recorder/out/shots/`
- Product name: Proofpay
- Tagline / strongest claim: "Pay for what the camera proved, at the friction your history earned."
- Key UI moment to recreate: the first-visit basket table (camera probability + disposition chip per line) and the trust card (score with lower-bound label, policy chip)
- Copy that must appear verbatim:
  - Held $4.10
  - Charged $3.57
  - Trust changes friction. Never the charge.
  - Proofpay

## Creative Direction
- Tone preset: polished
- Creative direction: a quiet fintech product film that reads like a well-set receipt
- Interpretation: long holds, numbers as the heroes, mixed-case Inter, morphs and soft crossfades, sparse audio.
- Angle: the receipt is the product: two numbers, held and charged, and the gap between them is what Proofpay does.
- Hook: "Held $4.10" → "Charged $3.57" → "Only what the camera proved."
- Outro / punchline: "Trust changes friction. Never the charge." then the Proofpay wordmark.
- Avoid: generic SaaS language, abstract filler, redesigning the product UI, any claim beyond the demo's numbers.

## Visual Identity
- Background: #f6f7f9; panels #ffffff with #e2e5ea rules and 12px radius
- Text: #14171c; muted #5b6472
- Accent: #0b57d0
- Chips: auto-capture/express #137a3c on #e6f4ea; staff check #8a5a00 on #fff4dc; strict/deny #b3261e on #fce8e6; released/neutral #5b6472 on #eef1f5
- Display and body font: Inter; IBM Plex Mono for the PayPal pill
- Visual references: basket table, disposition chips, trust card, agent purchases table

## Storyboard
Use the storyboard in `brag-output/brag-plan.md` as the creative contract.

1. Held vs charged — 0.0–3.4s — the two amounts and "Only what the camera proved."
2. The basket — 3.4–9.8s — four demo rows, the "Taken" click, the capture pill
3. History earns Express — 9.8–14.5s — 0.32 → 0.85, strict → express
4. Agents ask first — 14.5–18.1s — ₹1,400 ask human, ₹48,000 deny
5. Outro — 18.1–24.6s — the punchline, then the wordmark on the 22.93s cue

## Audio
- Audio role: warm bed with sparse professional accents
- Audio arc: fade in under the hook, steady through the flow, fade out under the wordmark
- Music: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` at 0.3
- Music cue guidance: bundled preset (110 BPM); strong cues 8.74s, 17.47s, 22.93s
- Audio-reactive treatment: none in this cut (Hyperframes 0.8 exposes no extraction helper in the bundled skills); recorded as a skip, not a blocker
- Audio-coupled moments: "Charged" lands (soft impact), "Taken" click, chip switch, deny row (soft impact), wordmark (bell)
- SFX selection guidance: low HF-risk picks from `sfx-analysis.md`
- Audio files: copied into `brag-output/composition/assets/`

## Hyperframes Instructions
Follow the Hyperframes contract (bundled `hyperframes` and `hyperframes-cli` skills in v0.8.221). Show real UI from the project, keep every text readable, stay within 15-25 s, run `npx hyperframes check` before render.
