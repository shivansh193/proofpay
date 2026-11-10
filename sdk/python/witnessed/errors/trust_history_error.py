from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

TrustHistoryErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _TrustHistoryError:
    def map(self, status_code: int, content: bytes) -> TrustHistoryErrorBody:
        match status_code:
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


trust_history_error_mapper: Final[ErrorMapper[TrustHistoryErrorBody]] = _TrustHistoryError()
