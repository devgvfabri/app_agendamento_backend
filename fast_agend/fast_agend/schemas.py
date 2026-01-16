from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import time


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    cpf: str
    phone: str

class UserPublic(BaseModel):
    username: str
    email: EmailStr
    phone: str
    id: int

class UserDB(UserSchema):
    id: int

class UserList(BaseModel):
    users: list[UserPublic]

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    cpf: str
    phone: str


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str | None = None
    cpf: str
    phone: str


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    cpf: str
    phone: str

    class Config:
        from_attributes = True

class EstablishmentSchema(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    opening_time: time
    closing_time: time

class EstablishmentList(BaseModel):
    establishments: list[EstablishmentSchema]