from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel


class LineIn(SdkBaseModel):
    line_id: str
    name: str
    sku: str
    price: float
    p: float
    evidence: Optional[Any] = UNSET


class LineInDict(TypedDict):
    line_id: str
    name: str
    sku: str
    price: float
    p: float
    evidence: NotRequired[Any]
