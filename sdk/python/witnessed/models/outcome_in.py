from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class OutcomeIn(SdkBaseModel):
    outcome: str


class OutcomeInDict(TypedDict):
    outcome: str
