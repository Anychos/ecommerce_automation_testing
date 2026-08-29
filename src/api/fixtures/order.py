from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

import pytest
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.api.fixtures.user import UserFixture
    from src.api.fixtures.cart import CartFixture

from src.api.clients.order.client import OrderAPIClient, get_public_order_client, get_private_order_client
from src.api.clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema


class OrderFixture(BaseModel):
    """Хранит данные о созданном заказе"""
    request: CreateOrderRequestSchema
    response: CreateOrderResponseSchema

    @property
    def order_id(self) -> int:
        return self.response.id


@pytest.fixture
def public_order_client() -> Generator[OrderAPIClient, None, None]:
    """Возвращает готовый HTTP клиент для доступа к публичному API заказа"""
    client = get_public_order_client()

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def private_order_client(user: UserFixture) -> Generator[OrderAPIClient, None, None]:
    """
    Возвращает готовый HTTP клиент для доступа к приватному API заказов

    :param user: Созданный пользователь
    """
    client = get_private_order_client(user=user.user_schema)

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def create_order(
        private_order_client: OrderAPIClient,
        create_cart: CartFixture
) -> OrderFixture:
    """
    Создает заказ

    :param private_order_client: Приватный HTTP клиент для доступа к API заказов
    :param create_cart: Созданная корзина
    :return: Информация о созданном заказе
    """
    request = CreateOrderRequestSchema(cart_id=create_cart.cart_id)
    response = private_order_client.create_order(request=request)
    return OrderFixture(request=request, response=response)
