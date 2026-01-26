from fast_agend.core.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from fast_agend.services.user_service import UserService
from fast_agend.services.establishment_service import EstablishmentService
from fast_agend.services.scheduling_service import SchedulingService
from fast_agend.services.services_service import ServicesService
from fast_agend.services.availability_service import AvailabilityService
from fast_agend.services.professional_service import ProfessionalService
from fast_agend.repositories.verification_token_repository import VerificationTokenRepository
from fast_agend.repositories.user_repository import UserRepository
from fast_agend.repositories.scheduling_repository import SchedulingRepository
from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.repositories.service_repository import ServiceRepository
from fast_agend.repositories.establishment_repository import EstablishmentRepository
from fast_agend.services.auth_service import AuthService
from fast_agend.core.deps import get_db
from fast_agend.security.password import oauth2_scheme, SECRET_KEY, ALGORITHM
from fast_agend.models import User
from jose import JWTError, jwt

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = UserRepository(db).get_by_username(username)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user

def get_user_service(db: Session = Depends(get_db)):
    return UserService(
        repository=UserRepository(db),
        verification_token_repository=VerificationTokenRepository(db)
    )

def get_establishment_service(db: Session = Depends(get_db)):
    return EstablishmentService(
        repository=EstablishmentRepository(db),
    )

def get_service(db: Session = Depends(get_db)):
    return ServicesService(
        repository=ServiceRepository(db),
    )

def get_professional_service(db: Session = Depends(get_db)):
    return ProfessionalService(
        repository=ProfessionalRepository(db),
    )

def get_availability_service(db: Session = Depends(get_db)):
    return AvailabilityService(
        AvailabilityRepository(db),
        SchedulingRepository(db),
    )

def get_scheduling_service(
    db: Session = Depends(get_db),
):
    return SchedulingService(
        SchedulingRepository(db),
        ServiceRepository(db),
    )
