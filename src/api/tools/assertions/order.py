from typing import List

import allure

from src.api.clients.error_schemas import HTTPValidationErrorResponseSchema
from src.api.clients.order.schemas import CreateOrderResponseSchema, GetOrderResponseSchema, CreateOrderRequestSchema, \
    GetOrdersResponseSchema
from src.api.fixtures.cart import CartFixture
from src.api.tools.assertions.base_assertions import assert_field_value, assert_field_exists, assert_length
from src.api.tools.assertions.error import assert_http_validation_error_response


@allure.step("Проверка продукта в заказе")
def assert_product_in_order(
        *,
        actual: CreateOrderResponseSchema,
        cart: CartFixture,
        index: int
) -> None:
    """
    Проверяет соответствие позиции заказа ожидаемому продукту

    :param actual: Фактический ответ на запрос создания заказа
    :param cart: Корзина с ожидаемым продуктом
    :param index: Индекс позиции продукта в заказе
    """
    item = actual.items[index]
    product = cart.product

    assert_field_value(item.product_id, cart.product_id, "product_id")
    assert_field_value(item.product_name, product.request.name, "product_name")
    assert_field_value(item.product_image_url, product.request.image_url, "product_image_url")
    assert_field_value(item.unit_price, product.request.price, "unit_price")
    assert_field_value(item.quantity, cart.request.quantity, "quantity")
    assert_field_value(item.line_total, product.request.price * cart.request.quantity, "line_total")

@allure.step("Проверка ответа на запрос создания заказа")
def assert_create_order_response(
        *,
        actual: CreateOrderResponseSchema,
        expected: CreateOrderRequestSchema,
        cart: CartFixture,
        product_index: int = 0
) -> None:
    """
    Проверяет ответ на запрос создания заказа

    :param actual: Фактический ответ на запрос создания заказа
    :param expected: Ожидаемый ответ на запрос создания заказа
    :param cart: Корзина с ожидаемым продуктом
    :param product_index: Индекс позиции продукта в заказе
    """
    product = cart.product

    assert_field_value(actual.cart_id, expected.cart_id, "cart_id")
    assert_field_exists(actual.id, "order_id")
    assert_field_exists(actual.user_id, "user_id")
    assert_field_exists(actual.created_at, "created_at")

    expected_items_total = product.request.price * cart.request.quantity
    assert_field_value(actual.items_total_amount, expected_items_total, "items_total_amount")
    assert_field_exists(actual.delivery_fee_amount, "delivery_fee_amount")
    assert_field_value(actual.total_amount, actual.items_total_amount + actual.delivery_fee_amount, "total_amount")
    assert_field_value(actual.payment_status, "unpaid", "payment_status")
    assert_field_value(actual.delivery_status, "not_requested", "delivery_status")
    assert_field_value(actual.paid_at, None, "paid_at")
    assert_field_exists(actual.items, "items")

    assert_product_in_order(actual=actual, cart=cart, index=product_index)

@allure.step("Проверка ответа на запрос получения заказа")
def assert_get_order_response(
        *,
        actual: GetOrderResponseSchema,
        expected: CreateOrderResponseSchema
) -> None:
    """
    Проверяет ответ на запрос получения заказа

    :param actual: Фактический ответ на запрос получения заказа
    :param expected: Ожидаемый ответ на запрос создания заказа
    """
    assert_field_value(actual.id, expected.id, "id")
    assert_field_value(actual.cart_id, expected.cart_id, "cart_id")
    assert_field_value(actual.created_at, expected.created_at, "created_at")
    assert_field_value(actual.user_id, expected.user_id, "user_id")
    assert_field_value(actual.items_total_amount, expected.items_total_amount, "items_total_amount")
    assert_field_value(actual.delivery_fee_amount, expected.delivery_fee_amount, "delivery_fee_amount")
    assert_field_value(actual.total_amount, expected.total_amount, "total_amount")
    assert_field_value(actual.payment_status, expected.payment_status, "payment_status")
    assert_field_value(actual.delivery_status, expected.delivery_status, "delivery_status")
    assert_field_value(actual.paid_at, expected.paid_at, "paid_at")
    assert_length(actual.items, expected.items, "items")

    for actual_item, expected_item in zip(actual.items, expected.items):
        assert_field_value(actual_item.product_id, expected_item.product_id, "product_id")
        assert_field_value(actual_item.product_name, expected_item.product_name, "product_name")
        assert_field_value(actual_item.product_image_url, expected_item.product_image_url, "product_image_url")
        assert_field_value(actual_item.unit_price, expected_item.unit_price, "unit_price")
        assert_field_value(actual_item.quantity, expected_item.quantity, "quantity")
        assert_field_value(actual_item.line_total, expected_item.line_total, "line_total")

@allure.step("Проверка ответа на запрос получения списка заказов")
def assert_get_orders_response(
        *,
        get_orders_response: GetOrdersResponseSchema,
        create_order_responses: List[CreateOrderResponseSchema]
) -> None:
    """
    Проверяет ответ на запрос получения списка заказов

    :param get_orders_response: Фактический ответ на запрос получения списка заказов
    :param create_order_responses: Ожидаемый ответ на запрос получения списка заказов
    """
    assert get_orders_response, "Список заказов пуст"

    orders_by_id = {
        order.id: order for order in get_orders_response
    }

    for created_order in create_order_responses:
        assert created_order.id in orders_by_id, (
            f"Заказ с id {created_order.id} отсутствует в ответе"
        )

        actual_order = orders_by_id[created_order.id]
        assert_get_order_response(actual=actual_order, expected=created_order)

@allure.step("Проверка ответа на запрос создания заказа с пустой корзиной")
def assert_empty_cart_order_response(actual: HTTPValidationErrorResponseSchema) -> None:
    """
    Проверяет ответ на запрос создания заказа с пустой корзиной

    :param actual: Фактический ответ на запрос создания заказа с пустой корзиной
    """
    expected = HTTPValidationErrorResponseSchema(
        detail="Нельзя создать заказ с пустой корзиной"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)

@allure.step("Проверка ответа на запрос создания заказа с недоступным продуктом")
def assert_unavailable_product_order_response(actual: HTTPValidationErrorResponseSchema) -> None:
    """
    Проверяет ответ на запрос создания заказа с недоступным продуктом

    :param actual: Фактический ответ на запрос создания заказа с недоступным продуктом
    """
    expected = HTTPValidationErrorResponseSchema(
        detail="В корзине есть недоступные для заказа товары"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)

