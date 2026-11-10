from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypeAlias

from ..core import ErrorMapper, RawError, decode_json
from ..models.http_validation_error import HttpValidationError

AgentPlanErrorBody: TypeAlias = HttpValidationError | RawError


@dataclass(frozen=True, slots=True)
class _AgentPlanError:
    def map(self, status_code: int, content: bytes) -> AgentPlanErrorBody:
        match status_code:
            case 422:
                return decode_json[HttpValidationError](content)
            case _:
                return RawError(status_code, content)


agent_plan_error_mapper: Final[ErrorMapper[AgentPlanErrorBody]] = _AgentPlanError()
