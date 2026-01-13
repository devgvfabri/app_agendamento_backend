from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fast_agend.security.password import verify_password, create_access_token
from fast_agend.schemas import Token, ForgotPasswordRequest
from fastapi.security import OAuth2PasswordRequestForm
from fast_agend.repositories.user_repository import UserRepository
from fast_agend.core.deps import get_auth_service
from fast_agend.services.auth_service import AuthService


router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    return auth_service.login(
        form_data.username,
        form_data.password,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/forgot-password", status_code=status.HTTP_204_NO_CONTENT)
def forgot_password(
    data: ForgotPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    auth_service.forgot_password(data.email)