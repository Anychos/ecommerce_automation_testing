import allure

from src.api.clients.deliveries.schemas import CreateOrderDeliveryResponseSchema
from src.api.clients.error_schemas import InputValidationErrorResponseSchema
from src.api.clients.order.schemas import CreateOrderResponseSchema
from src.api.clients.payments.schemas import (
    CreateOrderPaymentResponseSchema,
    FakeCancelPaymentResponseSchema,
    FakeSucceedPaymentResponseSchema,
    GetPaymentByIdResponseSchema,
    PaymentReturnResponseSchema,
    SyncPaymentResponseSchema,
)
from src.api.tools.assertions.base_assertions import (
    assert_field_exists,
    assert_field_value,
)
from src.api.tools.assertions.error import assert_input_validation_error_response


def _assert_payment_entity(
    *,
    actual: CreateOrderPaymentResponseSchema,
    expected: CreateOrderPaymentResponseSchema,
    status: str | None = None,
    order_payment_status: str | None = None,
    finalized: bool | None = None,
) -> None:
    """Проверяет общие поля ответа payment и его согласованность с expected."""
    assert_field_exists(actual.payment_id, "payment_id")
    assert_field_value(actual.payment_id, expected.payment_id, "payment_id")
    assert_field_value(actual.order_id, expected.order_id, "order_id")
    assert_field_value(
        actual.status, status if status is not None else expected.status, "status"
    )
    assert_field_value(actual.provider, expected.provider, "provider")
    assert_field_value(actual.attempt_no, expected.attempt_no, "attempt_no")
    assert_field_value(
        actual.external_payment_id, expected.external_payment_id, "external_payment_id"
    )
    assert_field_value(
        actual.confirmation_url, expected.confirmation_url, "confirmation_url"
    )
    assert_field_value(actual.is_test, expected.is_test, "is_test")
    assert_field_value(actual.amount_value, expected.amount_value, "amount_value")
    assert_field_value(actual.currency, expected.currency, "currency")
    assert_field_value(
        actual.order_payment_status,
        order_payment_status
        if order_payment_status is not None
        else expected.order_payment_status,
        "order_payment_status",
    )
    assert_field_exists(actual.created_at, "created_at")
    assert_field_exists(actual.updated_at, "updated_at")
    assert_field_value(actual.created_at, expected.created_at, "created_at")
    assert_field_value(
        getattr(actual, "error_message", None),
        getattr(expected, "error_message", None),
        "error_message",
    )

    if finalized is True:
        assert_field_exists(actual.finalized_at, "finalized_at")
    elif finalized is False:
        assert_field_value(actual.finalized_at, None, "finalized_at")
    else:
        assert_field_value(actual.finalized_at, expected.finalized_at, "finalized_at")


@allure.step("Проверка ответа на запрос создания оплаты")
def assert_create_payment_response(
    *,
    actual: CreateOrderPaymentResponseSchema,
    order: CreateOrderResponseSchema,
    delivery: CreateOrderDeliveryResponseSchema,
) -> None:
    """Проверяет создание fake-оплаты после расчёта и выбора доставки."""
    assert_field_exists(actual.payment_id, "payment_id")
    assert_field_exists(actual.attempt_no, "attempt_no")
    assert_field_value(actual.order_id, order.id, "order_id")
    assert_field_value(actual.order_id, delivery.order_id, "order_id")
    assert_field_value(actual.status, "pending", "status")
    assert_field_value(actual.provider, "fake", "provider")
    assert_field_value(actual.attempt_no, 1, "attempt_no")
    assert_field_exists(actual.external_payment_id, "external_payment_id")
    assert_field_exists(actual.confirmation_url, "confirmation_url")
    assert_field_value(actual.is_test, True, "is_test")
    assert_field_value(
        actual.amount_value,
        order.items_total_amount + delivery.fee_amount,
        "amount_value",
    )
    assert_field_value(actual.currency, "RUB", "currency")
    assert_field_value(actual.order_payment_status, "pending", "order_payment_status")
    assert_field_exists(actual.created_at, "created_at")
    assert_field_exists(actual.updated_at, "updated_at")
    assert_field_value(actual.finalized_at, None, "finalized_at")
    assert_field_value(getattr(actual, "error_message", None), None, "error_message")


@allure.step("Проверка ответа на запрос получения оплаты")
def assert_get_payment_response(
    *, actual: GetPaymentByIdResponseSchema, expected: CreateOrderPaymentResponseSchema
) -> None:
    """Проверяет ответ получения оплаты по идентификатору."""
    _assert_payment_entity(actual=actual, expected=expected)


@allure.step("Проверка ответа на запрос синхронизации оплаты")
def assert_sync_payment_response(
    *, actual: SyncPaymentResponseSchema, expected: CreateOrderPaymentResponseSchema
) -> None:
    """Проверяет ответ синхронизации оплаты."""
    _assert_payment_entity(actual=actual, expected=expected)
    assert_field_value(actual.synced, True, "synced")


@allure.step("Проверка ответа на возврат оплаты")
def assert_return_payment_response(
    *, actual: PaymentReturnResponseSchema, expected: CreateOrderPaymentResponseSchema
) -> None:
    """Проверяет ответ endpoint возврата оплаты."""
    assert_sync_payment_response(actual=actual, expected=expected)


@allure.step("Проверка ответа fake checkout оплаты")
def assert_fake_checkout_payment_response(*, actual: str) -> None:
    """Проверяет непустой HTML-ответ fake checkout."""
    assert isinstance(actual, str), "Ответ fake checkout не является строкой"
    assert actual.strip(), "Ответ fake checkout пуст"


def _assert_fake_transition(
    *,
    actual: SyncPaymentResponseSchema,
    expected: CreateOrderPaymentResponseSchema,
    status: str,
    order_payment_status: str,
    finalized: bool,
) -> None:
    _assert_payment_entity(
        actual=actual,
        expected=expected,
        status=status,
        order_payment_status=order_payment_status,
        finalized=finalized,
    )
    assert_field_value(actual.synced, True, "synced")


@allure.step("Проверка ответа fake succeed оплаты")
def assert_succeed_payment_response(
    *,
    actual: FakeSucceedPaymentResponseSchema,
    expected: CreateOrderPaymentResponseSchema,
) -> None:
    """Проверяет успешную финализацию fake-оплаты."""
    _assert_fake_transition(
        actual=actual,
        expected=expected,
        status="succeeded",
        order_payment_status="paid",
        finalized=True,
    )


@allure.step("Проверка ответа fake cancel оплаты")
def assert_cancel_payment_response(
    *,
    actual: FakeCancelPaymentResponseSchema,
    expected: CreateOrderPaymentResponseSchema,
) -> None:
    """Проверяет отмену fake-оплаты."""
    _assert_fake_transition(
        actual=actual,
        expected=expected,
        status="canceled",
        order_payment_status="canceled",
        finalized=True,
    )


@allure.step("Проверка validation error ответа payment")
def assert_payment_validation_error_response(
    *,
    actual: InputValidationErrorResponseSchema,
    expected: InputValidationErrorResponseSchema,
) -> None:
    """Проверяет стандартный FastAPI 422-ответ payment-маршрута."""
    assert_input_validation_error_response(actual=actual, expected=expected)
