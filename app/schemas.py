from pydantic import BaseModel, EmailStr
from datetime import date

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_no: str
    dob: date


class UserCreate(UserBase):
    password: str | bytes


class UserOut(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    email: EmailStr