# Brag Plan: Proofpay

## What is this app?
A PayPal checkout for camera-tracked stores that holds the whole basket, captures only the items vision (or staff) verified, and uses each payer's history to decide how much checking they get. The same engine gives AI shopping agents an earned spending limit.

## The angle
The receipt is the product. A card hold is normally all-or-nothing; Proofpay's receipt shows two different numbers, what was held and what was charged, and the gap is the point. The film is quiet and exact, like a well-designed receipt: real numbers from the demo ($4.10 held, $3.57 charged; score 0.32 → 0.85; ₹1,400 asks, ₹48,000 denied), no claims the product can't back.

## Hook (first 2-3 seconds)
Two numbers stacked, large: **Held $4.10** then **Charged $3.57**. The second lands, and a small line answers why: "Only what the camera proved."

## Key moments (the middle)
- The first-visit basket from the demo, row by row: milk 99.6% → auto-capture, bread 99.2% → auto-capture, chocolate 63% → staff check → **Taken**, shampoo 11% → released. A PayPal pill closes it: capture $3.57, release the rest.
- Trust earned: the same shopper's score counts from 0.32 to 0.85 while her policy chip changes from **strict** to **express**. "Twenty verified visits later: no exit check."
- The agent guard: two purchase rows arrive. ₹1,400 → **ask human**. ₹48,000 → **deny**.

## Outro / punchline
"Trust changes friction. Never the charge." Then the wordmark: **Proofpay**, with "Pay for what the camera proved" beneath.

## User flow worth showing
Start visit (vision probabilities per item) → staff exit check on the uncertain line → PayPal captures only the verified total. Then history earns Express, and the agent asks before overspending. All three come from the recorded demo (`tools/recorder/out/shots/`).

## Tone
- Preset: polished
- Creative direction: a quiet fintech product film that reads like a well-set receipt
- Interpretation: few scenes with long holds, mixed-case Inter, numbers as heroes, soft crossfades and morphs, two or three subtle sounds, nothing jokey.

## Format: landscape — 1920x1080
## Duration: 24.6s

## Visual identity (from the project)
- Background: #f6f7f9 (panels #ffffff, rules #e2e5ea)
- Accent: #0b57d0
- Text: #14171c (muted #5b6472)
- Status chips: good #137a3c on #e6f4ea, warn #8a5a00 on #fff4dc, bad #b3261e on #fce8e6
- Display font: Inter (the app uses system-ui; Inter is the bundled equivalent)
- Body font: Inter; mono for ids and amounts in the PayPal pill
- Strongest visual element: the basket table with its "Camera: taken?" percentages and the disposition chips

## Share copy (draft)
Proofpay: PayPal holds the basket, and you pay only for what the camera proved. Your history decides how much checking you get, and AI agents earn their spending limits the same way.

## Audio direction
- Role: warm bed with sparse professional accents
- Music: happy-beats-business-moves-vol-12 (steady and clean, 110 BPM)
- Music treatment: 0.3 volume, short fade-in, fade out under the final wordmark
- Music cue guidance: preset `assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json`. Strong cues: 8.74s (the "Taken" click), 17.47s (the deny chip), 22.93s (wordmark lands). Beat grid around 0.55s spacing; table rows are text, so reveal on every other beat (~1.1s).
- Audio-reactive treatment: subtle; the soft accent glow behind the hero numbers and the wordmark may breathe with RMS. No waveform visuals.
- SFX posture: sparse, motion-matched
- Audio-coupled moments: "Charged" landing, the "Taken" click, policy chip switch, the deny row, wordmark landing
- Restraint rule: no SFX on every row; nothing bright or repeated

## Storyboard

### Scene 1 — Held vs charged — 3.4s
"Held $4.10" arrives, then "Charged $3.57" lands below it in ink with "$4.10" dimming to muted. Small line: "Only what the camera proved."
Sequential/interaction: yes — two lines in order, each held ≥1.2s.
Audio intent: a soft, confident first accent.
Audio-coupled idea: soft impact as "Charged" lands.
Music: bed fades in.
Transition mood: soft → Scene 2

### Scene 2 — The basket — 6.4s
A white panel titled "First visit · asha · strict". Four rows from the demo arrive one by one (every other beat): item, price, camera %, disposition chip. The chocolate row's chip "Staff check" gets a cursor click on "Taken". A pill below: `capture $3.57 · release the rest`.
Sequential/interaction: yes — 4 rows, ~1.1s apart; simulated click on "Taken".
Audio intent: precise, procedural.
Audio-coupled idea: one click on "Taken"; a soft drop when the capture pill lands.
Transition mood: morph (panel narrows into the trust card) → Scene 3

### Scene 3 — History earns Express — 4.7s
A trust card: score counts 0.32 → 0.85, the policy chip switches strict → express, caption "Twenty verified visits later: no exit check."
Sequential/interaction: count-up and chip switch.
Audio intent: a small state change.
Audio-coupled idea: switch sound on the chip change.
Transition mood: slide → Scene 4

### Scene 4 — Agents ask first — 3.6s
Title "AI agents earn their limit." Two purchase rows: "Receipt rolls, bags, cleaner · ₹1,400 · ask human", "Display fridge · ₹48,000 · deny".
Sequential/interaction: yes — 2 rows, held.
Audio intent: firm but quiet.
Audio-coupled idea: soft impact on the deny chip.
Transition mood: soft crossfade → Scene 5

### Scene 5 — Outro — 6.5s
"Trust changes friction." / "Never the charge." Then the wordmark "Proofpay" lands on the 22.93s strong cue, with "Pay for what the camera proved" under it. Hold.
Sequential/interaction: two lines, then the logo.
Audio intent: resolution.
Audio-coupled idea: one bell on the wordmark landing; music fades out under it.

**Music mood for this video:** steady, clean, warm
**Audio summary:** a clean bed rises under the receipt, three small motion-matched accents carry the flow, and one bell lands the wordmark as the music fades.
