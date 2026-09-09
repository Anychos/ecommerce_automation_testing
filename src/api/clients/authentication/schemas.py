from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from src.api.clients.user.schemas import CreateUserResponseSchema
from src.api.tools.data_generator import fake_ru


class AuthenticationResponseSchema(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    user: CreateUserResponseSchema


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(AuthenticationResponseSchema):
    pass


class RegistrationRequestSchema(BaseModel):
    email: EmailStr = Field(default_factory=fake_ru.email)
    password: str = Field(default_factory=fake_ru.password)
    name: str = Field(default_factory=fake_ru.first_name)
    phone: str = Field(default_factory=fake_ru.phone)


class RegistrationResponseSchema(AuthenticationResponseSchema):
    pass
