from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from fast_agend.schemas import Message, UserSchema, UserPublic, UserDB, UserList
from sqlalchemy.orm import Session
from fast_agend.models import User
from fast_agend.core.deps import get_db
from fast_agend.routes.user import router as users_router

app = FastAPI(title='Backend do App de Agendamento')

app.include_router(users_router)


