from __future__ import annotations

from functools import cached_property
from types import TracebackType
from typing import Any
from uuid import UUID, uuid4

from typing_extensions import Self

from .base_client import DEFAULT_TIMEOUT, BaseWitnessedClient
from .core import (
    OPERATING_SYSTEM,
    PYTHON_RUNTIME,
    ApiResult,
    AsyncHttpClient,
    AsyncHttpx2Client,
    AsyncRawClient,
    BaseRawResponse,
    LoggingOptionsOrDict,
    RawError,
    RequestOptionsOrDict,
    RetryOptionsOrDict,
    async_json_decoder,
    json_body,
    param,
    raw_error_response,
    unwrap,
)
from .errors.agent_complete_error import AgentCompleteErrorBody, agent_complete_error_mapper
from .errors.agent_decide_error import AgentDecideErrorBody, agent_decide_error_mapper
from .errors.agent_outcome_error import AgentOutcomeErrorBody, agent_outcome_error_mapper
from .errors.agent_plan_error import AgentPlanErrorBody, agent_plan_error_mapper
from .errors.agent_purchase_error import AgentPurchaseErrorBody, agent_purchase_error_mapper
from .errors.agent_status_error import AgentStatusErrorBody, agent_status_error_mapper
from .errors.authorize_error import AuthorizeErrorBody, authorize_error_mapper
from .errors.evidence_error import EvidenceErrorBody, evidence_error_mapper
from .errors.exit_check_error import ExitCheckErrorBody, exit_check_error_mapper
from .errors.explain_error import ExplainErrorBody, explain_error_mapper
from .errors.not_mine_error import NotMineErrorBody, not_mine_error_mapper
from .errors.rescue_hold_error import RescueHoldErrorBody, rescue_hold_error_mapper
from .errors.seed_history_error import SeedHistoryErrorBody, seed_history_error_mapper
from .errors.session_error import SessionErrorBody, session_error_mapper
from .errors.start_error import StartErrorBody, start_error_mapper
from .errors.start_from_scenario_error import StartFromScenarioErrorBody, start_from_scenario_error_mapper
from .errors.triage_error import TriageErrorBody, triage_error_mapper
from .errors.trust_error import TrustErrorBody, trust_error_mapper
from .errors.trust_history_error import TrustHistoryErrorBody, trust_history_error_mapper
from .models.decide_in import DecideIn, DecideInDict
from .models.exit_in import ExitIn, ExitInDict
from .models.not_mine_in import NotMineIn, NotMineInDict
from .models.outcome_in import OutcomeIn, OutcomeInDict
from .models.plan_in import PlanIn, PlanInDict
from .models.purchase_in import PurchaseIn, PurchaseInDict
from .models.scenario_in import ScenarioIn, ScenarioInDict
from .models.seed_in import SeedIn, SeedInDict
from .models.start_in import StartIn, StartInDict
from .server.server import Server


class AsyncWitnessedClient(BaseWitnessedClient[AsyncRawClient]):
    def __init__(
        self,
        *,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        retry_options: int | RetryOptionsOrDict | None = None,
        logging_options: LoggingOptionsOrDict | None = None,
        custom_async_http_client: AsyncHttpClient | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url, timeout=timeout, retry_options=retry_options, logging_options=logging_options
        )
        self._raw_client = AsyncRawClient(
            http_client=(
                custom_async_http_client if custom_async_http_client is not None else AsyncHttpx2Client(timeout=timeout)
            ),
            retry_options=self._retry_options,
            logging_options=self._logging_options,
            global_headers=[
                param[str]("User-Agent", "WitnessedClient/1.0.0 Python"),
                param[str]("X-APIMatic-Lang", "Python"),
                param[str]("X-APIMatic-Package-Version", "1.0.0"),
                param[str]("X-APIMatic-Gen-Version", "4.0.0"),
                param[str]("X-APIMatic-OS", OPERATING_SYSTEM),
                param[str]("X-APIMatic-Runtime", PYTHON_RUNTIME),
            ],
        )

    @cached_property
    def with_raw_response(self) -> AsyncApiWithRawResponse:
        return AsyncApiWithRawResponse(self._raw_client, self._server)

    async def agent_complete(self, purchase_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``POST`` request.

        Args:
            purchase_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.agent_complete(purchase_id, request_options=request_options))

    async def agent_decide(
        self, purchase_id: str, body: DecideIn | DecideInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            purchase_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.agent_decide(purchase_id, body, request_options=request_options))

    async def agent_outcome(
        self, purchase_id: str, body: OutcomeIn | OutcomeInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            purchase_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.agent_outcome(purchase_id, body, request_options=request_options))

    async def agent_plan(
        self, agent_id: str, body: PlanIn | PlanInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            agent_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.agent_plan(agent_id, body, request_options=request_options))

    async def agent_purchase(
        self, agent_id: str, body: PurchaseIn | PurchaseInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            agent_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.agent_purchase(agent_id, body, request_options=request_options))

    async def agent_status(self, agent_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            agent_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.agent_status(agent_id, request_options=request_options))

    async def agreement(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """How often staff agreed with the AI. "check_bag" / "review_footage" defer to staff, so they're counted
        separately rather than as agreement.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.agreement(request_options=request_options))

    async def authorize(self, session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.authorize(session_id, request_options=request_options))

    async def config(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.config(request_options=request_options))

    async def evidence(self, session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.evidence(session_id, request_options=request_options))

    async def exit_check(
        self, session_id: str, body: ExitIn | ExitInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.exit_check(session_id, body, request_options=request_options))

    async def explain(self, session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.explain(session_id, request_options=request_options))

    async def list_holds(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.list_holds(request_options=request_options))

    async def not_mine(
        self,
        session_id: str,
        line_id: str,
        body: NotMineIn | NotMineInDict,
        *,
        request_options: RequestOptionsOrDict | None = None,
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            line_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.not_mine(session_id, line_id, body, request_options=request_options))

    async def paypal_webhook(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``POST`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.paypal_webhook(request_options=request_options))

    async def rescue_hold(self, session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.rescue_hold(session_id, request_options=request_options))

    async def scenarios(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.scenarios(request_options=request_options))

    async def seed_history(
        self, body: SeedIn | SeedInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Add SIMULATED weekly verified visits for a demo customer (labelled simulated).

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.seed_history(body, request_options=request_options))

    async def seed_holds(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Add SIMULATED holds of different ages (offline stand-in) to the timeline.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.seed_holds(request_options=request_options))

    async def session(self, session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.session(session_id, request_options=request_options))

    async def sessions(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.sessions(request_options=request_options))

    async def sim_results(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.sim_results(request_options=request_options))

    async def start(self, body: StartIn | StartInDict, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``POST`` request.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.start(body, request_options=request_options))

    async def start_from_scenario(
        self, body: ScenarioIn | ScenarioInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.start_from_scenario(body, request_options=request_options))

    async def subjects(self, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: If the API responds with an error status code. ``error`` is ``RawError``."""
        return unwrap(await self.with_raw_response.subjects(request_options=request_options))

    async def triage(
        self, session_id: str, line_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> Any:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            line_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.triage(session_id, line_id, request_options=request_options))

    async def trust(self, subject: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Send a ``GET`` request.

        Args:
            subject: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.trust(subject, request_options=request_options))

    async def trust_history(self, subject: str, *, request_options: RequestOptionsOrDict | None = None) -> Any:
        """Score just after each event, plus now: the trust inspector's line chart.

        Args:
            subject: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            Successful Response

        Raises:
            ApiError: Validation Error ``error`` is ``HttpValidationError | RawError``."""
        return unwrap(await self.with_raw_response.trust_history(subject, request_options=request_options))

    async def aclose(self) -> None:
        await self._raw_client.http_client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        await self.aclose()


class AsyncApiWithRawResponse(BaseRawResponse[AsyncRawClient, Server]):
    async def agent_complete(
        self, purchase_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, AgentCompleteErrorBody]:
        """Send a ``POST`` request.

        Args:
            purchase_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/agents/purchases/{purchase_id}/complete"),
            path_params=[param[str]("purchase_id", purchase_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=agent_complete_error_mapper,
            request_options=request_options,
        )

    async def agent_decide(
        self, purchase_id: str, body: DecideIn | DecideInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, AgentDecideErrorBody]:
        """Send a ``POST`` request.

        Args:
            purchase_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/agents/purchases/{purchase_id}/decide"),
            path_params=[param[str]("purchase_id", purchase_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[DecideIn | DecideInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=agent_decide_error_mapper,
            request_options=request_options,
        )

    async def agent_outcome(
        self, purchase_id: str, body: OutcomeIn | OutcomeInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, AgentOutcomeErrorBody]:
        """Send a ``POST`` request.

        Args:
            purchase_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/agents/purchases/{purchase_id}/outcome"),
            path_params=[param[str]("purchase_id", purchase_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[OutcomeIn | OutcomeInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=agent_outcome_error_mapper,
            request_options=request_options,
        )

    async def agent_plan(
        self, agent_id: str, body: PlanIn | PlanInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, AgentPlanErrorBody]:
        """Send a ``POST`` request.

        Args:
            agent_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/agents/{agent_id}/plan"),
            path_params=[param[str]("agent_id", agent_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[PlanIn | PlanInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=agent_plan_error_mapper,
            request_options=request_options,
        )

    async def agent_purchase(
        self, agent_id: str, body: PurchaseIn | PurchaseInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, AgentPurchaseErrorBody]:
        """Send a ``POST`` request.

        Args:
            agent_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/agents/{agent_id}/purchases"),
            path_params=[param[str]("agent_id", agent_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[PurchaseIn | PurchaseInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=agent_purchase_error_mapper,
            request_options=request_options,
        )

    async def agent_status(
        self, agent_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, AgentStatusErrorBody]:
        """Send a ``GET`` request.

        Args:
            agent_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/agents/{agent_id}"),
            path_params=[param[str]("agent_id", agent_id)],
            decoder=async_json_decoder[Any],
            error_mapper=agent_status_error_mapper,
            request_options=request_options,
        )

    async def agreement(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """How often staff agreed with the AI. "check_bag" / "review_footage" defer to staff, so they're counted
        separately rather than as agreement.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/ai/agreement"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def authorize(
        self, session_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, AuthorizeErrorBody]:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/sessions/{session_id}/authorize"),
            path_params=[param[str]("session_id", session_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=authorize_error_mapper,
            request_options=request_options,
        )

    async def config(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/config"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def evidence(
        self, session_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, EvidenceErrorBody]:
        """Send a ``GET`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/sessions/{session_id}/evidence"),
            path_params=[param[str]("session_id", session_id)],
            decoder=async_json_decoder[Any],
            error_mapper=evidence_error_mapper,
            request_options=request_options,
        )

    async def exit_check(
        self, session_id: str, body: ExitIn | ExitInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, ExitCheckErrorBody]:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/sessions/{session_id}/exit"),
            path_params=[param[str]("session_id", session_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[ExitIn | ExitInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=exit_check_error_mapper,
            request_options=request_options,
        )

    async def explain(
        self, session_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, ExplainErrorBody]:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/sessions/{session_id}/explain"),
            path_params=[param[str]("session_id", session_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=explain_error_mapper,
            request_options=request_options,
        )

    async def list_holds(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/holds"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def not_mine(
        self,
        session_id: str,
        line_id: str,
        body: NotMineIn | NotMineInDict,
        *,
        request_options: RequestOptionsOrDict | None = None,
    ) -> ApiResult[Any, NotMineErrorBody]:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            line_id: Value sent with the request.
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/sessions/{session_id}/lines/{line_id}/not-mine"),
            path_params=[param[str]("session_id", session_id), param[str]("line_id", line_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[NotMineIn | NotMineInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=not_mine_error_mapper,
            request_options=request_options,
        )

    async def paypal_webhook(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Send a ``POST`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/webhooks/paypal"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def rescue_hold(
        self, session_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, RescueHoldErrorBody]:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/holds/{session_id}/rescue"),
            path_params=[param[str]("session_id", session_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=rescue_hold_error_mapper,
            request_options=request_options,
        )

    async def scenarios(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/scenarios"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def seed_history(
        self, body: SeedIn | SeedInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, SeedHistoryErrorBody]:
        """Add SIMULATED weekly verified visits for a demo customer (labelled simulated).

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/seed-history"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[SeedIn | SeedInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=seed_history_error_mapper,
            request_options=request_options,
        )

    async def seed_holds(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Add SIMULATED holds of different ages (offline stand-in) to the timeline.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/demo/seed-holds"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def session(
        self, session_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, SessionErrorBody]:
        """Send a ``GET`` request.

        Args:
            session_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/sessions/{session_id}"),
            path_params=[param[str]("session_id", session_id)],
            decoder=async_json_decoder[Any],
            error_mapper=session_error_mapper,
            request_options=request_options,
        )

    async def sessions(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/sessions"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def sim_results(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/sim"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def start(
        self, body: StartIn | StartInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, StartErrorBody]:
        """Send a ``POST`` request.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/sessions"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[StartIn | StartInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=start_error_mapper,
            request_options=request_options,
        )

    async def start_from_scenario(
        self, body: ScenarioIn | ScenarioInDict, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, StartFromScenarioErrorBody]:
        """Send a ``POST`` request.

        Args:
            body: The request body.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/sessions/from-scenario"),
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            body=json_body[ScenarioIn | ScenarioInDict](body),
            decoder=async_json_decoder[Any],
            error_mapper=start_from_scenario_error_mapper,
            request_options=request_options,
        )

    async def subjects(self, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]:
        """Send a ``GET`` request.

        Args:
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/subjects"),
            decoder=async_json_decoder[Any],
            error_mapper=raw_error_response,
            request_options=request_options,
        )

    async def triage(
        self, session_id: str, line_id: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, TriageErrorBody]:
        """Send a ``POST`` request.

        Args:
            session_id: Value sent with the request.
            line_id: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="POST",
            url_template=self._server.default("/api/sessions/{session_id}/lines/{line_id}/triage"),
            path_params=[param[str]("session_id", session_id), param[str]("line_id", line_id)],
            headers=[param[UUID]("Idempotency-Key", uuid4())],
            decoder=async_json_decoder[Any],
            error_mapper=triage_error_mapper,
            request_options=request_options,
        )

    async def trust(
        self, subject: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, TrustErrorBody]:
        """Send a ``GET`` request.

        Args:
            subject: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/trust/{subject}"),
            path_params=[param[str]("subject", subject)],
            decoder=async_json_decoder[Any],
            error_mapper=trust_error_mapper,
            request_options=request_options,
        )

    async def trust_history(
        self, subject: str, *, request_options: RequestOptionsOrDict | None = None
    ) -> ApiResult[Any, TrustHistoryErrorBody]:
        """Score just after each event, plus now: the trust inspector's line chart.

        Args:
            subject: Value sent with the request.
            request_options: Per-call overrides for this one request, such as a timeout, extra headers, or its retry
                count and statuses.

        Returns:
            An ``ApiResult`` holding the deserialized response or the error body."""
        return await self._client.execute(
            http_method="GET",
            url_template=self._server.default("/api/trust/{subject}/history"),
            path_params=[param[str]("subject", subject)],
            decoder=async_json_decoder[Any],
            error_mapper=trust_history_error_mapper,
            request_options=request_options,
        )


AsyncClient = AsyncWitnessedClient
