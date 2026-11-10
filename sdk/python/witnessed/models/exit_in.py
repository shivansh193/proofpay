from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import UNSET, Optional, SdkBaseModel
from .line_in import LineIn, LineInDict


class ExitIn(SdkBaseModel):
    staff_verdicts: Optional[dict[str, bool]] = UNSET
    found: Optional[list[LineIn]] = UNSET


class ExitInDict(TypedDict):
    staff_verdicts: NotRequired[dict[str, bool]]
    found: NotRequired[list[LineInDict]]
