import allure

from src.api.clients.cart.schemas import AddItemCartResponseSchema, AddItemCartRequestSchema, DeleteCartResponseSchema, \
    DeleteCartItemResponseSchema, UpdateCartItemResponseSchema, UpdateCartItemRequestSchema, GetCartResponseSchema
from src.api.clients.error_shemas import HTTPValidationErrorResponseSchema
from src.api.tools.assertions.base_assertions import assert_value, assert_field_exists
from src.api.tools.assertions.error import assert_http_validation_error_response


@allure.step("Проверка ответа на запрос добавления продукта в корзину")
def assert_add_item_to_cart_response(
        *,
        actual: AddItemCartResponseSchema,
        expected: AddItemCartRequestSchema
) -> None:
    """
    Проверяет ответ на запрос добавления продукта в корзину

    :param actual: Фактический ответ на запрос добавления продукта в корзину
    :param expected: Ожидаемый ответ на запрос добавления продукта в корзину
    """

    assert_field_exists(actual.product_id, "item_id")
    assert_value(actual.product_id, expected.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")


def assert_product_in_cart(
        *,
        actual: GetCartResponseSchema,
        index: int
) -> None:
    """
    Проверяет наличие продукта в корзине

    :param actual: Фактический ответ на запрос получения корзины
    :param index: Индекс продукта в корзине
    """

    assert_value(actual.items[index].product_id, actual.items[index].product_id, "product_id")
    assert_value(actual.items[index].quantity, actual.items[index].quantity, "quantity")
    assert_value(actual.items[index].product_name, actual.items[index].product_name, "price")
    assert_value(actual.items[index].product_price, actual.items[index].product_price, "product_price")
    assert_value(actual.items[index].product_image_url, actual.items[index].product_image_url, "product_image_url")
    assert_value(actual.items[index].is_available, actual.items[index].is_available, "is_available")
    assert_value(actual.items[index].has_enough_stock, actual.items[index].has_enough_stock, "has_enough_stock")
    assert_value(actual.items[index].available_quantity, actual.items[index].available_quantity, "available_quantity")


@allure.step("Проверка ответа на запрос получения корзины")
def assert_get_cart_response(actual: GetCartResponseSchema):
    """
    Проверяет ответ на запрос получения корзины

    :param actual: Фактический ответ на запрос получения корзины
    """

    assert_field_exists(actual.id, "id")
    assert_field_exists(actual.user_id, "user_id")
    assert_field_exists(actual.total_quantity, "total_quantity")
    assert_field_exists(actual.total_price, "total_price")
    assert_field_exists(actual.items, "items")

    assert_product_in_cart(actual=actual, index=0)


@allure.step("Проверка ответа на запрос обновления продукта в корзине")
def assert_update_cart_response(
        *,
        actual: UpdateCartItemResponseSchema,
        expected: UpdateCartItemRequestSchema
) -> None:
    """
    Проверяет ответ на запрос обновления продукта в корзине

    :param actual: Фактический ответ на запрос обновления продукта в корзине
    :param expected: Ожидаемый ответ на запрос обновления продукта в корзине
    """

    assert_field_exists(actual.product_id, "item_id")
    assert_field_exists(actual.product_id, "product_id")
    assert_value(actual.quantity, expected.quantity, "quantity")


@allure.step("Проверка ответа на запрос удаления корзины")
def assert_delete_cart_response(actual: DeleteCartResponseSchema) -> None:
    """
    Проверяет ответ на запрос удаления корзины

    :param actual: Фактический ответ на запрос удаления корзины
    """

    expected = DeleteCartResponseSchema(
        message="Корзина очищена"
    )
    assert_value(actual.message, expected.message, "message")


@allure.step("Проверка ответа на запрос удаления продукта из корзины")
def assert_delete_item_cart_response(actual: DeleteCartItemResponseSchema) -> None:
    """
    Проверяет ответ на запрос удаления продукта из корзины

    :param actual: Фактический ответ на запрос удаления продукта из корзины
    """

    expected = DeleteCartItemResponseSchema(
        message="Продукт удален из корзины"
    )
    assert_value(actual.message, expected.message, "message")


@allure.step("Проверка ответа на запрос с добавлением несуществующего продукта в корзину")
def assert_not_found_product_response(actual: HTTPValidationErrorResponseSchema) -> None:
    """
    Проверяет ответ на запрос с добавлением несуществующего продукта в корзину

    :param actual: Фактический ответ на запрос с добавлением несуществующего продукта в корзину
    """

    expected = HTTPValidationErrorResponseSchema(
        detail="Продукт не найден или недоступен"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)


@allure.step("Проверка ответа на запрос с добавлением в корзину больше чем имеется в наличии")
def assert_not_enough_product_response(actual: HTTPValidationErrorResponseSchema) -> None:
    """
    Проверяет ответ на запрос с добавлением в корзину больше чем имеется в наличии

    :param actual: Фактический ответ на запрос с добавлением в корзину больше чем имеется в наличии
    """

    expected = HTTPValidationErrorResponseSchema(
        detail="Недостаточно товара в наличии"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)

