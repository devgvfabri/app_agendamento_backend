from pydantic import BaseModel, EmailStr


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


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    cpf: str
    phone: str

    class Config:
        from_attributes = True


