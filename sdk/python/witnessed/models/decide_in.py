from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class DecideIn(SdkBaseModel):
    approve: bool


class DecideInDict(TypedDict):
    approve: bool
