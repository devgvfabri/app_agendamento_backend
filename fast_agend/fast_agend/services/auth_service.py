from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import timedelta
from fast_agend.security.password import oauth2_scheme, SECRET_KEY, ALGORITHM, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, hash_password
from fast_agend.repositories.user_repository import UserRepository
from fast_agend.core.config import settings
from fast_agend.services.email_service import EmailService


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.email_service = EmailService()

    def login(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha inválidos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_email_verified: 
            raise HTTPException(
                status_code=403,
                detail="Confirme seu e-mail antes de fazer login",
            )

        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def get_current_user(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")

            if not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        user = self.user_repo.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
            )

        return user
    
    def forgot_password(self, email: str):
        user = self.user_repo.get_by_email(email)

        # IMPORTANTE: não informar se o e-mail existe
        if not user:
            return

        token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=15),
        )

        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        self.email_service.send_reset_password_email(email, reset_link)

    def reset_password(self, token: str, new_password: str) -> None:
        # 1️⃣ Decodificar token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str | None = payload.get("sub")
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido ou expirado",
            )

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido",
            )

        # 2️⃣ Buscar usuário
        user = self.user_repo.get_by_id(int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        # 3️⃣ Atualizar senha
        user.password = hash_password(new_password)
        self.user_repo.update(user)

