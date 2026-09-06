import allure

from src.api.clients.deliveries.schemas import (
    CreateOrderDeliveryRequestSchema,
    CreateOrderDeliveryResponseSchema,
    FakeAssignDeliveryResponseSchema,
    FakeCancelDeliveryResponseSchema,
    FakeDeliverDeliveryResponseSchema,
    FakePickupDeliveryResponseSchema,
    GetDeliveryByIdResponseResponseSchema,
    QuoteBaseSchema,
    QuoteDeliveryResponseSchema,
    QuoteRequestSchema,
    SyncDeliveryResponseResponseSchema,
)
from src.api.clients.error_schemas import InputValidationErrorResponseSchema
from src.api.tools.assertions.base_assertions import assert_field_exists, assert_field_value
from src.api.tools.assertions.error import assert_input_validation_error_response


def _assert_quote_response(
        *,
        actual: QuoteBaseSchema,
        expected: QuoteRequestSchema
) -> None:
    """Проверяет поля маршрута, полученные из запроса доставки."""
    assert_field_exists(actual.pickup_address, "pickup_address")
    assert_field_exists(actual.pickup_latitude, "pickup_latitude")
    assert_field_exists(actual.pickup_longitude, "pickup_longitude")
    assert_field_value(actual.dropoff_address, expected.dropoff_address, "dropoff_address")
    assert_field_value(actual.dropoff_latitude, expected.dropoff_latitude, "dropoff_latitude")
    assert_field_value(actual.dropoff_longitude, expected.dropoff_longitude, "dropoff_longitude")
    assert_field_exists(actual.route_distance_meters, "route_distance_meters")
    assert_field_exists(actual.route_duration_seconds, "route_duration_seconds")
    assert_field_exists(actual.fee_amount, "fee_amount")
    assert_field_value(actual.currency, "RUB", "currency")


@allure.step("Проверка ответа на запрос котировки доставки")
def assert_quote_delivery_response(
        *,
        actual: QuoteDeliveryResponseSchema,
        expected: QuoteRequestSchema
) -> None:
    """Проверяет успешный ответ запроса котировки доставки."""
    _assert_quote_response(actual=actual, expected=expected)
    assert_field_value(actual.routing_provider, "fake", "routing_provider")


def _assert_delivery_entity(
        *,
        actual: CreateOrderDeliveryResponseSchema,
        expected: CreateOrderDeliveryResponseSchema,
        status: str | None = None,
        order_delivery_status: str | None = None
) -> None:
    """Проверяет неизменяемые поля и lifecycle-статусы delivery-сущности."""
    assert_field_value(actual.delivery_id, expected.delivery_id, "delivery_id")
    assert_field_value(actual.order_id, expected.order_id, "order_id")
    assert_field_value(actual.provider, expected.provider, "provider")
    assert_field_value(actual.pickup_address, expected.pickup_address, "pickup_address")
    assert_field_value(actual.pickup_latitude, expected.pickup_latitude, "pickup_latitude")
    assert_field_value(actual.pickup_longitude, expected.pickup_longitude, "pickup_longitude")
    assert_field_value(actual.dropoff_address, expected.dropoff_address, "dropoff_address")
    assert_field_value(actual.dropoff_latitude, expected.dropoff_latitude, "dropoff_latitude")
    assert_field_value(actual.dropoff_longitude, expected.dropoff_longitude, "dropoff_longitude")
    assert_field_value(actual.route_distance_meters, expected.route_distance_meters, "route_distance_meters")
    assert_field_value(actual.route_duration_seconds, expected.route_duration_seconds, "route_duration_seconds")
    assert_field_value(actual.fee_amount, expected.fee_amount, "fee_amount")
    assert_field_value(actual.currency, expected.currency, "currency")
    assert_field_value(actual.created_at, expected.created_at, "created_at")
    assert_field_exists(actual.updated_at, "updated_at")
    assert_field_value(actual.status, status if status is not None else expected.status, "status")
    assert_field_value(
        actual.order_delivery_status,
        order_delivery_status if order_delivery_status is not None else expected.order_delivery_status,
        "order_delivery_status"
    )
    assert_field_value(actual.error_message, None, "error_message")


@allure.step("Проверка ответа на запрос создания доставки")
def assert_create_order_delivery_response(
        *,
        actual: CreateOrderDeliveryResponseSchema,
        expected: CreateOrderDeliveryRequestSchema,
        order_id: int
) -> None:
    """Проверяет создание fake-доставки для указанного заказа."""
    _assert_quote_response(actual=actual, expected=expected)
    assert_field_exists(actual.delivery_id, "delivery_id")
    assert_field_value(actual.order_id, order_id, "order_id")
    assert_field_value(actual.status, "selected", "status")
    assert_field_value(actual.provider, "fake", "provider")
    assert_field_value(actual.order_delivery_status, "selected", "order_delivery_status")
    assert_field_value(actual.external_delivery_id, None, "external_delivery_id")
    assert_field_exists(actual.created_at, "created_at")
    assert_field_exists(actual.updated_at, "updated_at")
    assert_field_value(actual.assigned_at, None, "assigned_at")
    assert_field_value(actual.picked_up_at, None, "picked_up_at")
    assert_field_value(actual.delivered_at, None, "delivered_at")
    assert_field_value(actual.canceled_at, None, "canceled_at")
    assert_field_value(actual.error_message, None, "error_message")


@allure.step("Проверка ответа на запрос получения доставки")
def assert_get_delivery_response(
        *,
        actual: GetDeliveryByIdResponseResponseSchema,
        expected: CreateOrderDeliveryResponseSchema
) -> None:
    """Проверяет чтение доставки без изменения её состояния."""
    _assert_delivery_entity(actual=actual, expected=expected)
    assert_field_value(actual.external_delivery_id, expected.external_delivery_id, "external_delivery_id")
    assert_field_value(actual.assigned_at, expected.assigned_at, "assigned_at")
    assert_field_value(actual.picked_up_at, expected.picked_up_at, "picked_up_at")
    assert_field_value(actual.delivered_at, expected.delivered_at, "delivered_at")
    assert_field_value(actual.canceled_at, expected.canceled_at, "canceled_at")


@allure.step("Проверка ответа на запрос синхронизации доставки")
def assert_sync_delivery_response(
        *,
        actual: SyncDeliveryResponseResponseSchema,
        expected: CreateOrderDeliveryResponseSchema
) -> None:
    """Проверяет синхронизацию доставки без ожидаемого lifecycle-перехода."""
    _assert_delivery_entity(actual=actual, expected=expected)
    assert_field_value(actual.external_delivery_id, expected.external_delivery_id, "external_delivery_id")
    assert_field_value(actual.assigned_at, expected.assigned_at, "assigned_at")
    assert_field_value(actual.picked_up_at, expected.picked_up_at, "picked_up_at")
    assert_field_value(actual.delivered_at, expected.delivered_at, "delivered_at")
    assert_field_value(actual.canceled_at, expected.canceled_at, "canceled_at")
    assert_field_value(actual.synced, True, "synced")


def _assert_fake_transition(
        *,
        actual: SyncDeliveryResponseResponseSchema,
        expected: CreateOrderDeliveryResponseSchema,
        status: str
) -> None:
    _assert_delivery_entity(
        actual=actual,
        expected=expected,
        status=status,
        order_delivery_status=status
    )
    assert_field_value(actual.synced, True, "synced")


@allure.step("Проверка ответа fake assign доставки")
def assert_assigned_delivery(
        *,
        actual: FakeAssignDeliveryResponseSchema,
        expected: CreateOrderDeliveryResponseSchema
) -> None:
    """Проверяет назначение курьера для fake-доставки."""
    _assert_fake_transition(actual=actual, expected=expected, status="assigned")
    assert_field_exists(actual.external_delivery_id, "external_delivery_id")
    assert_field_exists(actual.assigned_at, "assigned_at")
    assert_field_value(actual.picked_up_at, None, "picked_up_at")
    assert_field_value(actual.delivered_at, None, "delivered_at")
    assert_field_value(actual.canceled_at, None, "canceled_at")


@allure.step("Проверка ответа fake pickup доставки")
def assert_picked_delivery(
        *,
        actual: FakePickupDeliveryResponseSchema,
        expected: CreateOrderDeliveryResponseSchema
) -> None:
    """Проверяет получение доставки курьером."""
    _assert_fake_transition(actual=actual, expected=expected, status="picked_up")
    assert_field_exists(actual.external_delivery_id, "external_delivery_id")
    assert_field_exists(actual.assigned_at, "assigned_at")
    assert_field_exists(actual.picked_up_at, "picked_up_at")
    assert_field_value(actual.delivered_at, None, "delivered_at")
    assert_field_value(actual.canceled_at, None, "canceled_at")


@allure.step("Проверка ответа fake deliver доставки")
def assert_delivered_delivery(
        *,
        actual: FakeDeliverDeliveryResponseSchema,
        expected: CreateOrderDeliveryResponseSchema
) -> None:
    """Проверяет успешную доставку заказа."""
    _assert_fake_transition(actual=actual, expected=expected, status="delivered")
    assert_field_exists(actual.external_delivery_id, "external_delivery_id")
    assert_field_exists(actual.assigned_at, "assigned_at")
    assert_field_exists(actual.picked_up_at, "picked_up_at")
    assert_field_exists(actual.delivered_at, "delivered_at")
    assert_field_value(actual.canceled_at, None, "canceled_at")


@allure.step("Проверка ответа fake cancel доставки")
def assert_canceled_delivery(
        *,
        actual: FakeCancelDeliveryResponseSchema,
        expected: CreateOrderDeliveryResponseSchema
) -> None:
    """Проверяет отмену fake-доставки."""
    _assert_fake_transition(actual=actual, expected=expected, status="canceled")
    assert_field_exists(actual.external_delivery_id, "external_delivery_id")
    assert_field_exists(actual.canceled_at, "canceled_at")
    assert_field_value(actual.delivered_at, None, "delivered_at")


@allure.step("Проверка validation error ответа delivery")
def assert_delivery_validation_error_response(
        *,
        actual: InputValidationErrorResponseSchema,
        expected: InputValidationErrorResponseSchema
) -> None:
    """Проверяет стандартный FastAPI 422-ответ delivery-маршрута."""
    assert_input_validation_error_response(actual=actual, expected=expected)
