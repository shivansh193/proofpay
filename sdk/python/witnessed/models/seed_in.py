from __future__ import annotations

from typing_extensions import NotRequired, TypedDict

from ..core import SdkBaseModel


class SeedIn(SdkBaseModel):
    customer_id: str
    visits: int = 12
    basket_inr: float = 250.0


class SeedInDict(TypedDict):
    customer_id: str
    visits: NotRequired[int]
    basket_inr: NotRequired[float]
