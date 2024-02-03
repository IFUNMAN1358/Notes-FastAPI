from pydantic import BaseModel
from pydantic import UUID4, EmailStr


class FullUser(BaseModel):
    id: UUID4
    username: str
    email: EmailStr
    hashed_password: str
    role: str


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class LoginUser(BaseModel):
    email_username: str
    password: str


class ReturnIdUser(BaseModel):
    id: UUID4

    class Config:
        from_attributes = True
