from src.api.clients.error_schemas import InputValidationErrorResponseSchema, HTTPValidationErrorResponseSchema, ErrorSchema
from src.api.tools.assertions.base_assertions import assert_field_value, assert_length


def assert_error(
        *,
        actual: ErrorSchema,
        expected: ErrorSchema
) -> None:
    """
    Проверяет соответствие ошибки в ответе

    :param actual: Фактическая ошибка
    :param expected: Ожидаемая ошибка
    """
    assert_field_value(actual.type, expected.type, "type")
    assert_field_value(actual.location, expected.location, "location")
    assert_field_value(actual.message, expected.message, "message")
    assert_field_value(actual.input, expected.input, "input")
    assert_field_value(actual.context, expected.context, "context")

def assert_input_validation_error_response(
        *,
        actual: InputValidationErrorResponseSchema,
        expected: InputValidationErrorResponseSchema
) -> None:
    assert_length(actual.detail, expected.detail, "detail")

    for index, expected_error in enumerate(expected.detail):
        assert_error(actual=actual.detail[index], expected=expected_error)

def assert_http_validation_error_response(
        *,
        actual: HTTPValidationErrorResponseSchema,
        expected: HTTPValidationErrorResponseSchema
) -> None:
    assert_field_value(actual.detail, expected.detail, "detail")
