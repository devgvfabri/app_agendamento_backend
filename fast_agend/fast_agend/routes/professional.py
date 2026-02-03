from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db, get_current_user, get_scheduling_service, require_role
from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.services.professional_service import ProfessionalService, ProfessionalList
from fast_agend.services.availability_service import AvailabilityService
from fast_agend.schemas import ProfessionalSchema, ProfessionalUpdateSchema, ProfessionalPublic
from fast_agend.core.deps import get_professional_service, get_availability_service
from datetime import datetime, timedelta, time, date
from fast_agend.services.scheduling_service import SchedulingService
from fast_agend.models import User, UserRole

router = APIRouter(prefix="/professionals", tags=["Professionals"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProfessionalSchema)
def create_professional(
    professional: ProfessionalSchema,
    service: ProfessionalService = Depends(get_professional_service),
    current_user: User = Depends(get_current_user),
    admin: User = Depends(require_role(UserRole.ADMIN)),
):
    return service.create_professional(professional, current_user)


@router.get("/", response_model=ProfessionalList)
def list_professionals(service: ProfessionalService = Depends(get_professional_service)):
    return {"professionals": service.list_professionals()}


@router.put("/{professional_id}", response_model=ProfessionalPublic)
def update_professional(
    professional_id: int,
    professional: ProfessionalUpdateSchema,
    service: ProfessionalService = Depends(get_professional_service),
    current_user: User = Depends(get_current_user),
    admin: User = Depends(require_role(UserRole.ADMIN)),
):
    updated = service.update_professional(professional_id, professional, current_user)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado"
        )

    return updated


@router.delete("/{professional_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_professional(
    professional_id: int,
    service: ProfessionalService = Depends(get_professional_service),
    current_user: User = Depends(get_current_user),
    admin: User = Depends(require_role(UserRole.ADMIN)),
):

    deleted = service.delete_professional(professional_id, current_user)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado")

    return deleted

@router.get("/complete", response_model=list[ProfessionalPublic])
def list_professionals_complete(
    service: ProfessionalService = Depends(get_professional_service),
):
    return service.list_professionals_complete()

@router.get("/professional/{professional_id}/slots", status_code=HTTPStatus.OK)
def get_slots(
    professional_id: int,
    date: date,
    service: AvailabilityService = Depends(get_availability_service),
):
    return service.get_available_slots(professional_id, date)

@router.patch("/{scheduling_id}/confirm")
def confirm_scheduling(
    scheduling_id: int,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user),
    pro: User = Depends(require_role(UserRole.PROFESSIONAL)),
):
    return service.confirm(scheduling_id, current_user)