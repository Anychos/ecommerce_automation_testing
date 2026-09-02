from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class QuoteRequestSchema(BaseModel):
    dropoff_address: str
    dropoff_latitude: float = Field(..., ge=-90, le=90)
    dropoff_longitude: float = Field(..., ge=-180, le=180)


class QuoteResponseSchema(BaseModel):
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
    routing_provider: Literal["osrm", "fake"]


class CreateOrderDeliveryRequestSchema(QuoteRequestSchema):
    pass


class CreateOrderDeliveryResponseSchema(BaseModel):
    delivery_id: int
    order_id: int
    status: str
    provider: Literal["fake"]
    external_delivery_id: str | None = None
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
    order_delivery_status: str
    created_at: datetime
    updated_at: datetime
    assigned_at: datetime | None = None
    picked_up_at: datetime | None = None
    delivered_at: datetime | None = None
    canceled_at: datetime | None = None
    error_message: str | None = None


class GetDeliveryByIdResponseSchema(CreateOrderDeliveryResponseSchema):
    pass


class SyncDeliveryResponseSchema(CreateOrderDeliveryResponseSchema):
    synced: bool = True


class FakeAssignDeliveryResponseSchema(SyncDeliveryResponseSchema):
    pass


class FakePickupDeliveryResponseSchema(SyncDeliveryResponseSchema):
    pass


class FakeDeliverDeliveryResponseSchema(SyncDeliveryResponseSchema):
    pass


class FakeCancelDeliveryResponseSchema(SyncDeliveryResponseSchema):
    pass


class DeliveryWebhookPayloadSchema(BaseModel):
    type: str | None = None
    event: str | None = None
    object: dict[str, Any] | None = None
