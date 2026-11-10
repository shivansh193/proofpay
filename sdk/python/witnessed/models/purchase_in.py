from __future__ import annotations

from typing import Any

from typing_extensions import NotRequired, TypedDict

from ..core import SdkBaseModel


class PurchaseIn(SdkBaseModel):
    items: list[Any]
    task: str = ""


class PurchaseInDict(TypedDict):
    items: list[Any]
    task: NotRequired[str]
