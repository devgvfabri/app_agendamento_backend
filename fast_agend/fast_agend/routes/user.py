from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.user_repository import UserRepository
from fast_agend.services.user_service import UserService
from fast_agend.schemas import UserSchema, UserPublic, UserList, UserCreate, UserResponse, UserUpdateSchema
from fastapi import Depends
from fast_agend.security.password import oauth2_scheme
from fast_agend.core.deps import get_auth_service
from fast_agend.services.auth_service import AuthService
from fast_agend.utils import send_verification_email, generate_code
from fast_agend.core.deps import get_current_user
from fast_agend.models import User, VerificationToken

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(
    user: UserSchema,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(user)


@router.get("/", response_model=UserList)
def list_users(service: UserService = Depends(get_user_service)):
    return {"users": service.list_users()}


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserUpdateSchema,
    service: UserService = Depends(get_user_service),
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Você não pode alterar outro usuário",
        )

    updated = service.update_user(user_id, user)
    if not updated:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

    return updated


@router.delete("/{user_id}", response_model=UserPublic)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Você não pode excluir outro usuário",
        )

    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

    return deleted

@router.get("/me", response_model=UserResponse)
def read_users_me(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.get_current_user(token)

@router.post("/verify/email/request")
def request_email_verification(
    email: str,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    code = generate_code()
    token = VerificationToken(
        user_id=user.id,
        code=code,
        type="email",
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )

    db.add(token)
    db.commit()

    send_verification_email(user.email, code)
    return {"message": "Código enviado para seu e-mail"}


@router.post("/verify/email/confirm")
def confirm_email_verification(
    email: str,
    code: str,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    token = db.query(VerificationToken).filter_by(
        user_id=user.id,
        code=code,
        type="email"
    ).first()

    if not token:
        raise HTTPException(400, "Código inválido")

    if token.expires_at < datetime.utcnow():
        raise HTTPException(400, "Código expirado")

    user.is_email_verified = True
    db.delete(token)
    db.commit()

    return {"message": "E-mail verificado com sucesso"}
