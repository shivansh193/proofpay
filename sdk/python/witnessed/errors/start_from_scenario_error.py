from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

StartFromScenarioErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _StartFromScenarioError:
    def map(self, status_code: int, content: bytes) -> StartFromScenarioErrorBody:
        match status_code:
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


start_from_scenario_error_mapper: Final[ErrorMapper[StartFromScenarioErrorBody]] = _StartFromScenarioError()
