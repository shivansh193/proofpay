"""Vision adapter: shelf detections -> basket lines with a probability per item.

Any backend that implements `VisionEngine` can plug in. `ReplayEngine` replays a
recorded detection trace (demo/scenarios/*.json), so the demo runs with no GPU
and no model API. Traces record what a detector reported for each item: the
pick-up and put-back events it saw and its final probability that the item
left with the shopper.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from proofpay.checkout import BasketLine

SCENARIOS = Path(__file__).resolve().parent.parent / "demo" / "scenarios"


@dataclass(frozen=True)
class Detection:
    item_id: str
    name: str
    sku: str
    price: float  # INR
    p_taken: float
    events: tuple[dict, ...] = ()  # e.g. {"t": 3.2, "type": "pick", "conf": 0.97}
    crops: tuple[str, ...] = ()  # evidence image paths/URLs
    notes: str = ""


@dataclass(frozen=True)
class Trace:
    scenario: str
    title: str
    customer_id: str
    detections: tuple[Detection, ...]
    hidden: tuple[dict, ...] = field(default=())  # untracked items staff can "find" at exit
    clip: str | None = None


class VisionEngine(Protocol):
    name: str

    def basket(self, session_key: str) -> Trace: ...


class ReplayEngine:
    name = "replay"

    def __init__(self, folder: Path = SCENARIOS):
        self.folder = folder

    def scenarios(self) -> list[dict]:
        out = []
        for f in sorted(self.folder.glob("*.json")):
            j = json.loads(f.read_text(encoding="utf-8"))
            out.append({"scenario": f.stem, "title": j["title"], "customer_id": j["customer_id"],
                        "hidden": j.get("hidden", [])})
        return out

    def basket(self, session_key: str) -> Trace:
        j = json.loads((self.folder / f"{session_key}.json").read_text(encoding="utf-8"))
        dets = tuple(
            Detection(
                d["item_id"], d["name"], d["sku"], float(d["price"]), float(d["p_taken"]),
                tuple(d.get("events", ())), tuple(d.get("crops", ())), d.get("notes", ""),
            )
            for d in j["detections"]
        )
        return Trace(session_key, j["title"], j["customer_id"], dets, tuple(j.get("hidden", ())), j.get("clip"))


def to_lines(trace: Trace) -> list[BasketLine]:
    return [
        BasketLine(
            d.item_id, d.name, d.sku, d.price, d.p_taken,
            {"events": list(d.events), "crops": list(d.crops), "notes": d.notes, "engine": "replay"},
        )
        for d in trace.detections
    ]
