"""Places the Kokoro lines on the video, writes the fit report and the subtitles.

    python mix.py   # needs out/proofpay-demo.mp4 (make-video.mjs) and out/vo/*.wav (Kaggle kernel output)
Writes out/proofpay-demo-voiceover.mp4, out/voice-fit.md and out/proofpay-demo.srt.
No music bed: the repo has no track it is licensed to use; add one with a sidechain duck if that changes.
"""
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "out"
MAX_TEMPO = 1.18
GAP = 0.15  # seconds of air kept before the next line


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def chunks(text, width=42):
    """Split at sentence ends, then commas, into cues of at most two ~42-char lines."""
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text) if p.strip()]
    out = []
    for p in parts:
        if len(p) <= 2 * width:
            out.append(p)
            continue
        pieces, cur = [], ""
        for c in re.split(r"(?<=,)\s+", p):
            if cur and len(cur) + 1 + len(c) > 2 * width:
                pieces.append(cur)
                cur = c
            else:
                cur = f"{cur} {c}".strip()
        pieces.append(cur)
        out.extend(pieces)
    return out


def wrap(text, width=42):
    if len(text) <= width:
        return text
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best[0]:
            best = (score, a, b)
    return f"{best[1]}\n{best[2]}"


def main():
    lines = json.loads((HERE / "narration.json").read_text(encoding="utf-8"))["lines"]
    lengths = json.loads((OUT / "vo" / "lengths.json").read_text())
    video = OUT / "proofpay-demo.mp4"
    duration = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                                    capture_output=True, text=True, check=True).stdout)

    rows, placed, inputs, filters = [], [], ["-i", str(video)], []
    for i, l in enumerate(lines):
        length = lengths[l["id"]]
        room = l["until"] - l["at"] - GAP
        tempo = 1.0 if length <= room else min(MAX_TEMPO, length / room)
        spoken = length / tempo
        fits = spoken <= room + 1e-6
        rows.append((l["id"], length, room, tempo, fits))
        placed.append((l, l["at"], l["at"] + spoken))
        inputs += ["-i", str(OUT / "vo" / f"{l['id']}.wav")]
        chain = f"[{i + 1}:a]aresample=48000"
        if tempo > 1.0:
            chain += f",atempo={tempo:.3f}"
        chain += f",adelay={int(l['at'] * 1000)}:all=1[v{i}]"
        filters.append(chain)
    mix = "".join(f"[v{i}]" for i in range(len(lines)))
    filters.append(f"{mix}amix=inputs={len(lines)}:normalize=0:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad[a]")

    final = OUT / "proofpay-demo-voiceover.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters),
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-t", f"{duration:.3f}", "-movflags", "+faststart", str(final)], check=True)

    # Subtitles from the placed timings, split by characters within each line.
    cues = []
    for l, start, end in placed:
        parts = chunks(l["written"])
        total = sum(len(p) for p in parts)
        t = start
        for p in parts:
            d = (end - start) * len(p) / total
            cues.append([t, t + d, wrap(p)])
            t += d
    for a, b in zip(cues, cues[1:]):
        a[1] = min(a[1], b[0] - 0.04)
    (OUT / "proofpay-demo.srt").write_text(
        "\n".join(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{txt}\n" for i, (s, e, txt) in enumerate(cues, 1)),
        encoding="utf-8")

    report = ["| Line | Voice s | Room s | Tempo | Fits |", "|---|---|---|---|---|"]
    report += [f"| {i} | {n:.2f} | {r:.2f} | {t:.3f}x | {'yes' if f else 'NO, shorten text'} |" for i, n, r, t, f in rows]
    (OUT / "voice-fit.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"wrote {final}, {len(cues)} subtitle cues")


if __name__ == "__main__":
    main()
