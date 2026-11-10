from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

RescueHoldErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _RescueHoldError:
    def map(self, status_code: int, content: bytes) -> RescueHoldErrorBody:
        match status_code:
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


rescue_hold_error_mapper: Final[ErrorMapper[RescueHoldErrorBody]] = _RescueHoldError()
