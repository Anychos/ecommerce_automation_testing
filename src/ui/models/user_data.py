from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    email: EmailStr
    name: str
    phone: str
    password: str
    confirm_password: str
