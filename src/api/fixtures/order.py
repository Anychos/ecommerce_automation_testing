from __future__ import annotations

import pytest
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.api.fixtures.user import UserFixture
    from src.api.fixtures.cart import CartFixture

from src.api.clients.order.client import OrderAPIClient, get_public_order_client, get_private_order_client
from src.api.clients.order.schemas import CreateOrderRequestSchema, CreateOrderResponseSchema


class OrderFixture(BaseModel):
    """
    Хранит данные о созданном заказе
    """

    request: CreateOrderRequestSchema
    response: CreateOrderResponseSchema

    @property
    def order_id(self) -> int:
        return self.response.id


@pytest.fixture
def public_order_client() -> OrderAPIClient:
    """
    Возвращает готовый публичный HTTP клиент для доступа к API заказа

    :return: Публичный HTTP клиент для работы с API заказа
    """

    return get_public_order_client()

@pytest.fixture
def private_order_client(user: UserFixture) -> OrderAPIClient:
    """
    Возвращает готовый приватный HTTP клиент для доступа к API заказов

    :param user: Созданный пользователь
    :return: Приватный HTTP клиент для работы с API заказа
    """

    return get_private_order_client(user=user.user_schema)


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
