from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fast_agend.schemas import Message, UserSchema, UserPublic, UserDB, UserList
from sqlalchemy.orm import Session
from fast_agend.models import User
from fast_agend.core.deps import get_db
from fast_agend.routes.user import router as users_router
from fast_agend.routes.auth import router as auth_router
from fast_agend.routes.establishment import router as establishments_router 
from fast_agend.exceptions.user_exceptions import InvalidCPFException, ExistingNumberException, UsernameAlreadyExistsException
from fast_agend.exceptions.user_exceptions import CPFAlreadyExistsException, EmailAlreadyExistsException, InvalidPasswordException
from dotenv import load_dotenv
import os


app = FastAPI(title='Backend do App de Agendamento')

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(establishments_router)

@app.exception_handler(InvalidCPFException)
async def invalid_cpf_exception_handler(
    request: Request,
    exc: InvalidCPFException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

@app.exception_handler(UsernameAlreadyExistsException)
async def existing_username_exception_handler(
    request: Request,
    exc: UsernameAlreadyExistsException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

@app.exception_handler(CPFAlreadyExistsException)
async def existing_cpf_exception_handler(
    request: Request,
    exc: CPFAlreadyExistsException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

@app.exception_handler(EmailAlreadyExistsException)
async def existing_email_exception_handler(
    request: Request,
    exc: EmailAlreadyExistsException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

@app.exception_handler(ExistingNumberException)
async def existing_number_exception_handler(
    request: Request,
    exc: ExistingNumberException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

@app.exception_handler(InvalidPasswordException)
async def invalid_password(
    request: Request,
    exc: InvalidPasswordException
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )
