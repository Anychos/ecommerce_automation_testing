from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel

from src.api.clients.product.schemas import ProductInOrderSchema


class CreateOrderRequestSchema(BaseModel):
    cart_id: int


class CreateOrderResponseSchema(BaseModel):
    id: int
    cart_id: int
    created_at: date
    user_id: int
    items_total_amount: float
    delivery_fee_amount: float
    total_amount: float
    payment_status: Literal["unpaid", "pending", "paid", "canceled"]
    delivery_status: Literal[
        "not_requested",
        "selected",
        "activation_failed",
        "pending",
        "assigned",
        "picked_up",
        "delivered",
        "canceled",
    ]
    paid_at: datetime | None = None
    items: list[ProductInOrderSchema]


class GetOrderResponseSchema(CreateOrderResponseSchema):
    pass


GetOrdersResponseSchema = list[GetOrderResponseSchema]
