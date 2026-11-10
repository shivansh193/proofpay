from __future__ import annotations

from typing_extensions import TypedDict

from ..core import SdkBaseModel
from .line_in import LineIn, LineInDict


class StartIn(SdkBaseModel):
    customer_id: str
    lines: list[LineIn]


class StartInDict(TypedDict):
    customer_id: str
    lines: list[LineInDict]
