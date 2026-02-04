from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.scheduling_repository import SchedulingRepository
from fast_agend.services.scheduling_service import SchedulingService, SchedulingList
from fast_agend.schemas import SchedulingSchema, SchedulingUpdateSchema, SchedulingPublic, SchedulingProfessionalsResponse, SchedulingCreateSchema, SchedulingUsersResponse
from fast_agend.core.deps import get_scheduling_service, get_current_user
from fast_agend.models import User
from datetime import date

router = APIRouter(prefix="/schedulings", tags=["Schedulings"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=SchedulingCreateSchema)
def create_scheduling(
    scheduling: SchedulingCreateSchema,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_scheduling(scheduling, current_user)


@router.get("/", response_model=SchedulingList)
def list_schedulings(service: SchedulingService = Depends(get_scheduling_service)):
    return {"schedulings": service.list_schedulings()}


@router.put("/{scheduling_id}", response_model=SchedulingPublic)
def update_scheduling(
    scheduling_id: int,
    scheduling: SchedulingUpdateSchema,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user),
):
    updated = service.update_scheduling(scheduling_id, scheduling, current_user)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Agendamento não encontrado"
        )

    return updated


@router.delete("/{scheduling_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_scheduling(
    scheduling_id: int,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user),
):

    deleted = service.delete_scheduling(scheduling_id, current_user)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Agendamento não encontrado")

    return deleted

@router.get("/professionals/{professional_id}/schedulings", response_model=SchedulingProfessionalsResponse)
def get_schedulings_by_professional(
    professional_id: int,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user),
):
    schedulings = service.list_by_professional(current_user, professional_id)

    if not schedulings:
        raise HTTPException(
            status_code=404,
            detail="Nenhum agendamento encontrado para este profissional"
        )

    return {
        "professional_id": professional_id,
        "schedulings": schedulings
    }

@router.get("/professionals/{professional_id}/schedulingsdate", response_model=SchedulingProfessionalsResponse)
def get_schedulings_by_professional_date(
    professional_id: int,
    date: date,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user),
):
    schedulings = service.list_by_professional_date(professional_id, current_user, date)

    if not schedulings:
        raise HTTPException(
            status_code=404,
            detail="Nenhum agendamento encontrado para este profissional"
        )

    return {
        "professional_id": professional_id,
        "schedulings": schedulings,
        "date": date
    }

@router.get("/users/{user_id}/schedulings")
def get_schedulings_by_client(
    user_id: int,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user)
):
    return service.list_by_user_secure(user_id, current_user)

@router.get("/users/{user_id}/schedulingsdate", response_model=SchedulingUsersResponse) 
def get_schedulings_by_users_date( user_id: int, date: date, service: SchedulingService = Depends(get_scheduling_service), current_user: User = Depends(get_current_user)
): 
    schedulings = service.list_by_user_date(user_id, current_user, date) 
    if not schedulings: 
        raise HTTPException( status_code=404, detail="Nenhum agendamento encontrado para este cliente" ) 
        
    return { "user_id": user_id, "schedulings": schedulings, "date": date }


@router.patch("/{scheduling_id}/confirm")
def cancel_scheduling(
    scheduling_id: int,
    service: SchedulingService = Depends(get_scheduling_service),
    current_user: User = Depends(get_current_user),
):
    return service.cancel(scheduling_id, current_user)