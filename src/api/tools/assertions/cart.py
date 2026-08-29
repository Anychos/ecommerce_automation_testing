import allure

from src.api.clients.cart.schemas import AddItemCartResponseSchema, AddItemCartRequestSchema, DeleteCartResponseSchema, \
    DeleteCartItemResponseSchema, UpdateCartItemResponseSchema, UpdateCartItemRequestSchema, GetCartResponseSchema
from src.api.clients.error_schemas import HTTPValidationErrorResponseSchema
from src.api.fixtures.cart import CartFixture
from src.api.tools.assertions.base_assertions import assert_field_value, assert_field_exists
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
    assert_field_exists(actual.product_id, "product_id")
    assert_field_value(actual.product_id, expected.product_id, "product_id")
    assert_field_value(actual.quantity, expected.quantity, "quantity")

@allure.step("Проверка наличия продукта в корзине")
def assert_product_in_cart(
        *,
        actual: GetCartResponseSchema,
        cart: CartFixture,
        index: int
) -> None:
    """
    Проверяет соответствие позиции корзины ожидаемому продукту

    :param actual: Фактический ответ на запрос получения корзины
    :param cart: Созданная корзина с ожидаемым продуктом
    :param index: Индекс продукта в корзине
    """
    item = actual.items[index]
    product = cart.product

    assert_field_value(item.product_id, cart.product_id, "product_id")
    assert_field_value(item.quantity, cart.request.quantity, "quantity")
    assert_field_value(item.product_name, product.request.name, "product_name")
    assert_field_value(item.product_price, product.request.price, "product_price")
    assert_field_value(item.product_image_url, product.request.image_url, "product_image_url")
    assert_field_value(item.is_available, product.request.is_available, "is_available")
    assert_field_value(item.has_enough_stock, product.request.stock_quantity >= cart.request.quantity, "has_enough_stock")
    assert_field_value(item.available_quantity, product.request.stock_quantity, "available_quantity")

@allure.step("Проверка ответа на запрос получения корзины")
def assert_get_cart_response(
        *,
        actual: GetCartResponseSchema,
        cart: CartFixture,
        product_index: int = 0
) -> None:
    """
    Проверяет ответ на запрос получения корзины

    :param actual: Фактический ответ на запрос получения корзины
    :param cart: Созданная корзина с ожидаемым продуктом
    :param product_index: Индекс позиции продукта в корзине
    """
    product = cart.product

    assert_field_exists(actual.id, "id")
    assert_field_value(actual.id, cart.cart_id, "id")
    assert_field_exists(actual.user_id, "user_id")
    assert_field_value(actual.total_quantity, cart.request.quantity, "total_quantity")
    assert_field_value(actual.total_price, product.request.price * cart.request.quantity, "total_price")
    assert_field_exists(actual.items, "items")
    assert_product_in_cart(actual=actual, cart=cart, index=product_index)

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
    assert_field_value(actual.quantity, expected.quantity, "quantity")

@allure.step("Проверка ответа на запрос удаления корзины")
def assert_delete_cart_response(actual: DeleteCartResponseSchema) -> None:
    """
    Проверяет ответ на запрос удаления корзины

    :param actual: Фактический ответ на запрос удаления корзины
    """
    expected = DeleteCartResponseSchema(
        message="Корзина очищена"
    )
    assert_field_value(actual.message, expected.message, "message")

@allure.step("Проверка ответа на запрос удаления продукта из корзины")
def assert_delete_item_cart_response(actual: DeleteCartItemResponseSchema) -> None:
    """
    Проверяет ответ на запрос удаления продукта из корзины

    :param actual: Фактический ответ на запрос удаления продукта из корзины
    """
    expected = DeleteCartItemResponseSchema(
        message="Продукт удален из корзины"
    )
    assert_field_value(actual.message, expected.message, "message")

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

@allure.step("Проверка ответа на запрос с добавлением в корзину одного товара больше чем имеется в наличии")
def assert_not_enough_product_response(actual: HTTPValidationErrorResponseSchema) -> None:
    """
    Проверяет ответ на запрос с добавлением в корзину больше чем имеется в наличии

    :param actual: Фактический ответ на запрос с добавлением в корзину больше чем имеется в наличии
    """
    expected = HTTPValidationErrorResponseSchema(
        detail="Недостаточно товара в наличии"
    )
    assert_http_validation_error_response(actual=actual, expected=expected)

