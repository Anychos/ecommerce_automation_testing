from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from src.api.tools.data_generator import fake_ru


class QuoteRequestSchema(BaseModel):
    dropoff_address: str = Field(default_factory=fake_ru.dropoff_address)
    dropoff_latitude: float = Field(default_factory=fake_ru.dropoff_latitude)
    dropoff_longitude: float = Field(default_factory=fake_ru.dropoff_longitude)


class QuoteBaseSchema(BaseModel):
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_address: str
    dropoff_latitude: float
    dropoff_longitude: float
    route_distance_meters: float
    route_duration_seconds: float
    fee_amount: float
    currency: str


class QuoteDeliveryResponseSchema(QuoteBaseSchema):
    routing_provider: Literal["osrm", "fake"]


class CreateOrderDeliveryRequestSchema(QuoteRequestSchema):
    pass


class CreateOrderDeliveryResponseSchema(QuoteBaseSchema):
    delivery_id: int
    order_id: int
    status: str
    provider: Literal["fake"]
    external_delivery_id: str | None = None
    order_delivery_status: str
    created_at: datetime
    updated_at: datetime
    assigned_at: datetime | None = None
    picked_up_at: datetime | None = None
    delivered_at: datetime | None = None
    canceled_at: datetime | None = None
    error_message: str | None = None


class GetDeliveryByIdResponseResponseSchema(CreateOrderDeliveryResponseSchema):
    pass


class SyncDeliveryResponseResponseSchema(CreateOrderDeliveryResponseSchema):
    synced: bool = True


class FakeAssignDeliveryResponseSchema(SyncDeliveryResponseResponseSchema):
    pass


class FakePickupDeliveryResponseSchema(SyncDeliveryResponseResponseSchema):
    pass


class FakeDeliverDeliveryResponseSchema(SyncDeliveryResponseResponseSchema):
    pass


class FakeCancelDeliveryResponseSchema(SyncDeliveryResponseResponseSchema):
    pass


class DeliveryWebhookPayloadSchema(BaseModel):
    type: str | None = None
    event: str | None = None
    object: dict[str, Any] | None = None
