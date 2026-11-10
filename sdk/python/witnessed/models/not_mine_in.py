from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel


class NotMineIn(SdkBaseModel):
    footage_shows_take: bool


class NotMineInDict(TypedDict):
    footage_shows_take: bool
