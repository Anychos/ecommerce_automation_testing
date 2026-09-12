from collections.abc import Generator

import pytest
from pydantic import BaseModel

from src.api.clients.deliveries.client import (
    DeliveriesAPIClient,
    get_private_deliveries_client,
)
from src.api.clients.deliveries.schemas import (
    CreateOrderDeliveryRequestSchema,
    CreateOrderDeliveryResponseSchema,
)
from src.api.fixtures.order import OrderFixture
from src.api.fixtures.user import UserFixture


class DeliveryFixture(BaseModel):
    request: CreateOrderDeliveryRequestSchema
    response: CreateOrderDeliveryResponseSchema

    @property
    def delivery_id(self) -> int:
        return self.response.delivery_id

    @property
    def order_id(self) -> int:
        return self.response.order_id


@pytest.fixture
def private_delivery_client(
    user: UserFixture,
) -> Generator[DeliveriesAPIClient, None, None]:
    """
    Возвращает готовый HTTP клиент для доступа к приватному API доставки

    :param user: Созданный пользователь
    """
    client = get_private_deliveries_client(user=user.user_schema)

    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def create_delivery(
    private_delivery_client: DeliveriesAPIClient, create_order: OrderFixture
) -> DeliveryFixture:
    order_id = create_order.order_id
    request = CreateOrderDeliveryRequestSchema()
    response = private_delivery_client.create_order_delivery(
        order_id=order_id, request=request
    )
    return DeliveryFixture(request=request, response=response)
