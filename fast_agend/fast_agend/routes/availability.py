from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db, require_role
from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.services.availability_service import AvailabilityService, AvailabilityList
from fast_agend.schemas import AvailabilitySchema, AvailabilityUpdateSchema, AvailabilityPublic
from fast_agend.core.deps import get_availability_service, get_current_user
from fast_agend.models import User, UserRole


router = APIRouter(prefix="/availabilitys", tags=["Availability"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=AvailabilitySchema)
def create_availability(
    availability: AvailabilitySchema,
    db: Session = Depends(get_db),
    service: AvailabilityService = Depends(get_availability_service),
    current_user: User = Depends(get_current_user),
    pro: User = Depends(require_role(UserRole.PROFESSIONAL)),
):
    return service.create_availability(db, availability, current_user)

@router.get("/", response_model=AvailabilityList)
def list_availabilitys(service: AvailabilityService = Depends(get_availability_service)):
    return {"availabilitys": service.list_availabilitys()}


@router.put("/{availability_id}", response_model=AvailabilityPublic)
def update_availability(
    availability_id: int,
    availability: AvailabilityUpdateSchema,
    db: Session = Depends(get_db),
    service: AvailabilityService = Depends(get_availability_service),
    current_user: User = Depends(get_current_user),
    pro: User = Depends(require_role(UserRole.PROFESSIONAL)),
):
    updated = service.update_availability(
        db,
        availability_id,
        availability,
        current_user,
    )

    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            "Disponibilidade não encontrada"
        )

    return updated


@router.delete("/{availability_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_availabilityt(
    availability_id: int,
    service: AvailabilityService = Depends(get_availability_service),
    current_user: User = Depends(get_current_user),
    pro: User = Depends(require_role(UserRole.PROFESSIONAL)),
):

    deleted = service.delete_availability(availability_id, current_user)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Disponibilidade não encontrado")

    return deleted

@router.get("/{professional_id}/availabilities", response_model=list[AvailabilityPublic])
def list_professional_availabilities(
    professional_id: int,
    db: Session = Depends(get_db),
    service: AvailabilityService = Depends(get_availability_service)
):
    return service.get_professional_availabilities(
        db=db,
        professional_id=professional_id
    )