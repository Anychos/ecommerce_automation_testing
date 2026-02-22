from pydantic import BaseModel, EmailStr, Field


class UserData(BaseModel):
    email: EmailStr
    name: str
    phone: str
    password: str
    confirm_password: str
    address: str | None = Field(default=None)

