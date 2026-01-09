from fast_agend.core.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Depends
from sqlalchemy.orm import Session

from fast_agend.repositories.user_repository import UserRepository
from fast_agend.services.auth_service import AuthService
from fast_agend.core.deps import get_db


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)
