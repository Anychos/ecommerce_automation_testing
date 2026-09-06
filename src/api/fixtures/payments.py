from typing import Any, Generator

import pytest
from pydantic import BaseModel

from src.api.clients.payments.client import PaymentsAPIClient, get_private_payments_client
from src.api.clients.payments.schemas import CreateOrderPaymentResponseSchema
from src.api.fixtures.deliveries import DeliveryFixture
from src.api.fixtures.user import UserFixture


class PaymentFixture(BaseModel):
    delivery: DeliveryFixture
    response: CreateOrderPaymentResponseSchema

    @property
    def payment_id(self) -> int:
        return self.response.payment_id


@pytest.fixture
def private_payments_client(user: UserFixture) -> Generator[PaymentsAPIClient, None, None]:
    client = get_private_payments_client(user=user.user_schema)

    try:
        yield client
    finally:
        client.close()

@pytest.fixture
def create_payment(private_payments_client: PaymentsAPIClient, create_delivery: DeliveryFixture) -> PaymentFixture:
    order_id = create_delivery.order_id
    response = private_payments_client.create_order_payment(order_id=order_id)
    return PaymentFixture(delivery=create_delivery, response=response)