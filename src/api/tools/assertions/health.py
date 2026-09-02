from src.api.clients.health.schema import HealthCheckResponseSchema
from src.api.tools.assertions.base_assertions import assert_field_exists, assert_field_value


def assert_heath_check_response(actual: HealthCheckResponseSchema) -> None:
    assert_field_exists(actual.status, "status")
    assert_field_value(actual.status, "ok", "status")