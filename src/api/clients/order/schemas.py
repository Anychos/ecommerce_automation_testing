from pydantic import BaseModel, Field

from src.api.clients.product.schemas import ProductInOrderSchema


class CreateOrderRequestSchema(BaseModel):
    cart_id: int


class CreateOrderResponseSchema(BaseModel):
    id: int
    cart_id: int
    created_at: str
    user_id: int
    items_total_amount: float
    delivery_fee_amount: float
    total_amount: float
    payment_status: str
    delivery_status: str
    paid_at: str | None = Field(default=None)
    items: list[ProductInOrderSchema]


class GetOrderResponseSchema(CreateOrderResponseSchema):
    pass


GetOrdersResponseSchema = list[GetOrderResponseSchema]
