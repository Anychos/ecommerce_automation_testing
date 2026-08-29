from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Any, Generator

import pytest
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.api.fixtures.user import UserFixture, private_admin_client

from src.api.clients.cart.client import CartAPIClient, get_public_cart_client, get_private_cart_client
from src.api.clients.cart.schemas import AddItemCartRequestSchema, AddItemCartResponseSchema
from src.api.fixtures.product import CreateProductFixture


class CartFixture(BaseModel):
    """Хранит данные о созданной корзине"""
    request: AddItemCartRequestSchema
    response: AddItemCartResponseSchema
    product: CreateProductFixture

    @property
    def cart_id(self) -> int:
        return self.response.cart_id

    @property
    def product_id(self) -> int:
        return self.response.product_id


@pytest.fixture
def public_cart_client() -> Generator[CartAPIClient, None, None]:
    """Возвращает готовый HTTP клиент для доступа к публичному API корзины"""
    client = get_public_cart_client()

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def private_cart_client(user: UserFixture) -> Generator[CartAPIClient, None, None]:
    """
    Возвращает готовый HTTP клиент для доступа к приватному API корзины

    :param user: Созданный пользователь
    """
    client = get_private_cart_client(user=user.user_schema)

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def create_cart(
        private_cart_client: CartAPIClient,
        create_available_product: CreateProductFixture
) -> Generator[CartFixture, None, None]:
    """
    Создает корзину с продуктом

    :param private_cart_client: Приватный HTTP клиент для доступа к API корзины
    :param create_available_product: Созданный продукт
    :return: Объект CartFixture с информацией о корзине
    """
    request = AddItemCartRequestSchema(product_id=create_available_product.product_id)

    response = private_cart_client.add_item_cart(request=request)
    cart = CartFixture(request=request, response=response, product=create_available_product)

    yield cart

    private_cart_client.clear_cart_api()

@pytest.fixture
def empty_cart(
    private_cart_client: CartAPIClient,
    create_cart: CartFixture
) -> CartFixture:
    """
    Создает корзину и очищает ее

    :param private_cart_client: Приватный HTTP клиент для доступа к API корзины
    :param create_cart: Созданная корзина
    :return: Объект CartFixture с информацией о корзине
    """
    private_cart_client.clear_cart_api()
    return create_cart
