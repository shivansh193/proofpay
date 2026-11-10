from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class ScenarioIn(SdkBaseModel):
    scenario: str


class ScenarioInDict(TypedDict):
    scenario: str
