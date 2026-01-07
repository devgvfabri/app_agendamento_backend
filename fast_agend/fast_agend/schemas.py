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

