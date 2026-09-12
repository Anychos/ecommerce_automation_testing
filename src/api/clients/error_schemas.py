from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: str
    location: list[str | int] = Field(alias="loc")
    message: str = Field(alias="msg")
    input: Any | None = Field(default=None)
    context: dict[str, Any] | None = Field(alias="ctx", default=None)


class InputValidationErrorResponseSchema(BaseModel):
    detail: list[ErrorSchema]


class HTTPValidationErrorResponseSchema(BaseModel):
    detail: str
