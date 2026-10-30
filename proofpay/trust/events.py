"""Trust events: the append-only evidence the engine scores."""

from __future__ import annotations

from dataclasses import dataclass, field

KINDS = frozenset(
    {
        "capture_verified",
        "line_disputed_upheld",
        "line_disputed_rejected",
        "exit_mismatch",
        "refund",
        "dispute_opened",
        "chargeback",
        "agent_purchase_ok",
        "agent_purchase_returned",
        "agent_purchase_overridden",
    }
)


@dataclass(frozen=True)
class Event:
    subject: str
    kind: str
    t: float  # days since epoch
    # capture_verified: vision probability of each captured line.
    line_p: tuple[float, ...] = ()
    # Money involved (basket captured, refund amount, ...). Used for value at risk.
    value: float = 0.0
    # Free-form provenance: PayPal ids, "simulated", footage links.
    meta: dict = field(default_factory=dict, compare=False, hash=False)

    def __post_init__(self) -> None:
        if self.kind not in KINDS:
            raise ValueError(f"unknown event kind {self.kind!r}")
        if self.kind == "capture_verified" and not self.line_p:
            raise ValueError("capture_verified needs line_p")
        if any(not 0.0 <= p <= 1.0 for p in self.line_p):
            raise ValueError("line_p must be probabilities")
