from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import time
from decimal import Decimal


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
    name: str
    address: str
    phone: str
    opening_time: time
    closing_time: time

class EstablishmentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
    phone: str
    opening_time: time
    closing_time: time

class EstablishmentList(BaseModel):
    establishments: list[EstablishmentPublic]

class EstablishmentUpdateSchema(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class ServiceSchema(BaseModel):
    name: str
    description: str
    duration_minutes: int
    price: Decimal
    service_establishment_id: int
    professional_id: int

class ServicePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    duration_minutes: int
    price: Decimal

class ServiceList(BaseModel):
    services: list[ServicePublic]

class ServiceUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[Decimal] = None

class ProfessionalSchema(BaseModel):
    id_user: int
    id_establishment: int
    specialty: str
    active: bool

class ProfessionalPublic(BaseModel):
    id: int
    specialty: str | None
    active: bool | None
    user: UserPublic
    services: list[ServicePublic]

    model_config = ConfigDict(from_attributes=True)

class ProfessionalList(BaseModel):
    professionals: list[ProfessionalPublic]

class ProfessionalUpdateSchema(BaseModel):
    specialty: Optional[str] = None
    active: Optional[bool] = None
    id_establishment: Optional[int] = None

