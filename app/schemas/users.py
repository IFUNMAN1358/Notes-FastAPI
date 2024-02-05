from pydantic import BaseModel
from pydantic import UUID4, EmailStr


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    email_username: str
    password: str


class ReturnIdUser(BaseModel):
    id: UUID4
