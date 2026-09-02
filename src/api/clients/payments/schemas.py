from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel


class CreateOrderPaymentResponseSchema(BaseModel):
    payment_id: int
    order_id: int
    status: str
    provider: Literal["fake", "yookassa"]
    attempt_no: int
    external_payment_id: str | None = None
    confirmation_url: str | None = None
    is_test: bool
    amount_value: float
    currency: str
    order_payment_status: str
    created_at: datetime
    updated_at: datetime
    finalized_at: datetime | None = None


class GetPaymentByIdResponseSchema(CreateOrderPaymentResponseSchema):
    error_message: str | None = None


class SyncPaymentResponseSchema(GetPaymentByIdResponseSchema):
    synced: bool = True


class PaymentReturnResponseSchema(SyncPaymentResponseSchema):
    pass


class FakeSucceedPaymentResponseSchema(SyncPaymentResponseSchema):
    pass


class FakeCancelPaymentResponseSchema(SyncPaymentResponseSchema):
    pass


class YooKassaWebhookPayloadSchema(BaseModel):
    type: str | None = None
    event: str | None = None
    object: dict[str, Any] | None = None
