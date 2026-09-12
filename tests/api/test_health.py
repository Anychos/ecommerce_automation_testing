from http import HTTPStatus

from src.api.clients.health.client import HealthCheckAPIClient
from src.api.clients.health.schema import HealthCheckResponseSchema
from src.api.tools.assertions.base_assertions import (
    assert_json_schema,
    assert_status_code,
)
from src.api.tools.assertions.health import assert_heath_check_response


def test_health_check(check_health_client: HealthCheckAPIClient) -> None:
    response = check_health_client.health_check_api()
    assert_status_code(response.status_code, HTTPStatus.OK)

    response_data = HealthCheckResponseSchema.model_validate_json(response.text)
    assert_heath_check_response(response_data)
    assert_json_schema(response.json(), response_data.model_json_schema())
