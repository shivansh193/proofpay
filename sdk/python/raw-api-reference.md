# Raw Reference

**Raw** endpoints, reached through `with_raw_response`, return `ApiResult[T, E]` and never raise for an API error. For the parsed endpoints, see [API Reference](api-reference.md).

> Source: [WitnessedClient](witnessed/client.py)

<details>
<summary><code>def agent_complete(purchase_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, AgentCompleteErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.agent_complete("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentCompleteErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.agent_complete("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentCompleteErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>purchase_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [AgentCompleteErrorBody](witnessed/errors/agent_complete_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[AgentCompleteErrorBody](witnessed/errors/agent_complete_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def agent_decide(purchase_id: str, body: DecideIn | DecideInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, AgentDecideErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.agent_decide("some example string", DecideIn(approve=True))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentDecideErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.agent_decide("some example string", DecideIn(approve=True))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentDecideErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>purchase_id</code> | <code>str</code> | Value sent with the request. |
| <code>body</code> | <code>[DecideIn](witnessed/models/decide_in.py) \| [DecideInDict](witnessed/models/decide_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [AgentDecideErrorBody](witnessed/errors/agent_decide_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[AgentDecideErrorBody](witnessed/errors/agent_decide_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def agent_outcome(purchase_id: str, body: OutcomeIn | OutcomeInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, AgentOutcomeErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.agent_outcome("some example string", OutcomeIn(outcome="some example string"))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentOutcomeErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.agent_outcome(
    "some example string", OutcomeIn(outcome="some example string")
)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentOutcomeErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>purchase_id</code> | <code>str</code> | Value sent with the request. |
| <code>body</code> | <code>[OutcomeIn](witnessed/models/outcome_in.py) \| [OutcomeInDict](witnessed/models/outcome_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [AgentOutcomeErrorBody](witnessed/errors/agent_outcome_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[AgentOutcomeErrorBody](witnessed/errors/agent_outcome_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def agent_plan(agent_id: str, body: PlanIn | PlanInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, AgentPlanErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.agent_plan("some example string", PlanIn(task="some example string"))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentPlanErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.agent_plan("some example string", PlanIn(task="some example string"))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentPlanErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>agent_id</code> | <code>str</code> | Value sent with the request. |
| <code>body</code> | <code>[PlanIn](witnessed/models/plan_in.py) \| [PlanInDict](witnessed/models/plan_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [AgentPlanErrorBody](witnessed/errors/agent_plan_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[AgentPlanErrorBody](witnessed/errors/agent_plan_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def agent_purchase(agent_id: str, body: PurchaseIn | PurchaseInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, AgentPurchaseErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.agent_purchase("some example string", PurchaseIn(items=[{}]))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentPurchaseErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.agent_purchase("some example string", PurchaseIn(items=[{}]))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentPurchaseErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>agent_id</code> | <code>str</code> | Value sent with the request. |
| <code>body</code> | <code>[PurchaseIn](witnessed/models/purchase_in.py) \| [PurchaseInDict](witnessed/models/purchase_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [AgentPurchaseErrorBody](witnessed/errors/agent_purchase_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[AgentPurchaseErrorBody](witnessed/errors/agent_purchase_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def agent_status(agent_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, AgentStatusErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.agent_status("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentStatusErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.agent_status("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AgentStatusErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>agent_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [AgentStatusErrorBody](witnessed/errors/agent_status_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[AgentStatusErrorBody](witnessed/errors/agent_status_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def agreement(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

How often staff agreed with the AI. "check_bag" / "review_footage" defer to
staff, so they're counted separately rather than as agreement.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.agreement()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.agreement()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def authorize(session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, AuthorizeErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.authorize("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AuthorizeErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.authorize("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type AuthorizeErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [AuthorizeErrorBody](witnessed/errors/authorize_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[AuthorizeErrorBody](witnessed/errors/authorize_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def config(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.config()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.config()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def evidence(session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, EvidenceErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.evidence("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type EvidenceErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.evidence("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type EvidenceErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [EvidenceErrorBody](witnessed/errors/evidence_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[EvidenceErrorBody](witnessed/errors/evidence_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def exit_check(session_id: str, body: ExitIn | ExitInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, ExitCheckErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.exit_check("some example string", ExitIn())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ExitCheckErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.exit_check("some example string", ExitIn())
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ExitCheckErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>body</code> | <code>[ExitIn](witnessed/models/exit_in.py) \| [ExitInDict](witnessed/models/exit_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [ExitCheckErrorBody](witnessed/errors/exit_check_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[ExitCheckErrorBody](witnessed/errors/exit_check_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def explain(session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, ExplainErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.explain("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ExplainErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.explain("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type ExplainErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [ExplainErrorBody](witnessed/errors/explain_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[ExplainErrorBody](witnessed/errors/explain_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def list_holds(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.list_holds()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.list_holds()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def not_mine(session_id: str, line_id: str, body: NotMineIn | NotMineInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, NotMineErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.not_mine(
    "some example string", "some example string", NotMineIn(footage_shows_take=True)
)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type NotMineErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.not_mine(
    "some example string", "some example string", NotMineIn(footage_shows_take=True)
)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type NotMineErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>line_id</code> | <code>str</code> | Value sent with the request. |
| <code>body</code> | <code>[NotMineIn](witnessed/models/not_mine_in.py) \| [NotMineInDict](witnessed/models/not_mine_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [NotMineErrorBody](witnessed/errors/not_mine_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[NotMineErrorBody](witnessed/errors/not_mine_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def paypal_webhook(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.paypal_webhook()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.paypal_webhook()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def rescue_hold(session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RescueHoldErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.rescue_hold("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RescueHoldErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.rescue_hold("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RescueHoldErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RescueHoldErrorBody](witnessed/errors/rescue_hold_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RescueHoldErrorBody](witnessed/errors/rescue_hold_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def scenarios(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.scenarios()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.scenarios()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def seed_history(body: SeedIn | SeedInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, SeedHistoryErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Add SIMULATED weekly verified visits for a demo customer (labelled simulated).

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.seed_history(SeedIn(customer_id="some example string"))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type SeedHistoryErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.seed_history(SeedIn(customer_id="some example string"))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type SeedHistoryErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[SeedIn](witnessed/models/seed_in.py) \| [SeedInDict](witnessed/models/seed_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [SeedHistoryErrorBody](witnessed/errors/seed_history_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[SeedHistoryErrorBody](witnessed/errors/seed_history_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def seed_holds(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Add SIMULATED holds of different ages (offline stand-in) to the timeline.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.seed_holds()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.seed_holds()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def session(session_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, SessionErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.session("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type SessionErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.session("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type SessionErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [SessionErrorBody](witnessed/errors/session_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[SessionErrorBody](witnessed/errors/session_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def sessions(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.sessions()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.sessions()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def sim_results(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.sim_results()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.sim_results()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def start(body: StartIn | StartInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, StartErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.start(
    StartIn(
        customer_id="some example string",
        lines=[
            LineIn(
                line_id="some example string", name="some example string", sku="some example string", price=1.5, p=1.5
            ),
        ],
    ),
)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type StartErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.start(
    StartIn(
        customer_id="some example string",
        lines=[
            LineIn(
                line_id="some example string", name="some example string", sku="some example string", price=1.5, p=1.5
            ),
        ],
    ),
)
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type StartErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[StartIn](witnessed/models/start_in.py) \| [StartInDict](witnessed/models/start_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [StartErrorBody](witnessed/errors/start_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[StartErrorBody](witnessed/errors/start_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def start_from_scenario(body: ScenarioIn | ScenarioInDict, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, StartFromScenarioErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.start_from_scenario(ScenarioIn(scenario="some example string"))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type StartFromScenarioErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.start_from_scenario(ScenarioIn(scenario="some example string"))
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type StartFromScenarioErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>body</code> | <code>[ScenarioIn](witnessed/models/scenario_in.py) \| [ScenarioInDict](witnessed/models/scenario_in.py)</code> | The request body. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [StartFromScenarioErrorBody](witnessed/errors/start_from_scenario_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[StartFromScenarioErrorBody](witnessed/errors/start_from_scenario_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def subjects(*, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, RawError]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.subjects()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

**Async**

```python
result = await async_client.with_raw_response.subjects()
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type RawError
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [RawError](witnessed/core/results.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[RawError](witnessed/core/results.py)</code>

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def triage(session_id: str, line_id: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, TriageErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `POST` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.triage("some example string", "some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type TriageErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.triage("some example string", "some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type TriageErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>session_id</code> | <code>str</code> | Value sent with the request. |
| <code>line_id</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [TriageErrorBody](witnessed/errors/triage_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[TriageErrorBody](witnessed/errors/triage_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def trust(subject: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, TrustErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Send a `GET` request.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.trust("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type TrustErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.trust("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type TrustErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>subject</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [TrustErrorBody](witnessed/errors/trust_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[TrustErrorBody](witnessed/errors/trust_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

<details>
<summary><code>def trust_history(subject: str, *, request_options: RequestOptionsOrDict | None = None) -> ApiResult[Any, TrustHistoryErrorBody]</code></summary>

<dl>
<dd>

### Description

<dl>
<dd>

Score just after each event, plus now: the trust inspector's line chart.

</dd>
</dl>

### Usage

<dl>
<dd>

**Sync**

```python
result = client.with_raw_response.trust_history("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type TrustHistoryErrorBody
```

**Async**

```python
result = await async_client.with_raw_response.trust_history("some example string")
match result:
    case Success(payload=payload):
        ...  # TODO: Handle 'payload' of type Any
    case Failure(error=error):
        ...  # TODO: Handle 'error' of type TrustHistoryErrorBody
```

</dd>
</dl>

### Parameters

<dl>
<dd>

| Name | Type | Description |
| --- | --- | --- |
| <code>subject</code> | <code>str</code> | Value sent with the request. |
| <code>request_options</code> | <code>[RequestOptionsOrDict](witnessed/core/request_options.py) \| None</code> | Per-call overrides for this one request, such as a timeout, extra headers, or its retry count and statuses. |

</dd>
</dl>

### Response

<dl>
<dd>

**Returns**: <code>[ApiResult](witnessed/core/results.py)&#91;Any, [TrustHistoryErrorBody](witnessed/errors/trust_history_error.py)&#93;</code>

**On `Success`**: `payload` is <code>Any</code> -- Successful Response

**On `Failure`**: `error` is <code>[TrustHistoryErrorBody](witnessed/errors/trust_history_error.py)</code>

Mapped in first-match order -- an earlier row wins over a later range that also covers the status:

| Status | `error` is |
| --- | --- |
| 422 | <code>[HttpValidationError](witnessed/models/http_validation_error.py)</code> |
| anything unmapped | <code>[RawError](witnessed/core/results.py)</code> |

</dd>
</dl>

</dd>
</dl>

</details>

