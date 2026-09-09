from typing import Literal

from pydantic import BaseModel


class HealthCheckResponseSchema(BaseModel):
    status: Literal["ok"]
