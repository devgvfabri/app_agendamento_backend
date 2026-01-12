from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import timedelta
from fast_agend.security.password import oauth2_scheme, SECRET_KEY, ALGORITHM, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fast_agend.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

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
