from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.scheduling_repository import SchedulingRepository
from fast_agend.services.scheduling_service import SchedulingService, SchedulingList
from fast_agend.schemas import SchedulingSchema, SchedulingUpdateSchema, SchedulingPublic, SchedulingProfessionalsResponse, SchedulingCreateSchema
from fast_agend.core.deps import get_scheduling_service


router = APIRouter(prefix="/schedulings", tags=["Schedulings"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=SchedulingCreateSchema)
def create_scheduling(
    scheduling: SchedulingCreateSchema,
    service: SchedulingService = Depends(get_scheduling_service),
):
    return service.create_scheduling(scheduling)


@router.get("/", response_model=SchedulingList)
def list_schedulings(service: SchedulingService = Depends(get_scheduling_service)):
    return {"schedulings": service.list_schedulings()}


@router.put("/{scheduling_id}", response_model=SchedulingPublic)
def update_scheduling(
    scheduling_id: int,
    scheduling: SchedulingUpdateSchema,
    service: SchedulingService = Depends(get_scheduling_service),
):
    updated = service.update_scheduling(scheduling_id, scheduling)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Agendamento não encontrado"
        )

    return updated


@router.delete("/{scheduling_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_scheduling(
    scheduling_id: int,
    service: SchedulingService = Depends(get_scheduling_service),
):

    deleted = service.delete_scheduling(scheduling_id)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Agendamento não encontrado")

    return deleted

@router.get(
    "/professionals/{professional_id}/schedulings",
    response_model=SchedulingProfessionalsResponse
)
def get_schedulings_by_professional(
    professional_id: int,
    service: SchedulingService = Depends(get_scheduling_service),
):
    schedulings = service.list_by_professional(professional_id)

    if not schedulings:
        raise HTTPException(
            status_code=404,
            detail="Nenhum agendamento encontrado para este profissional"
        )

    return {
        "professional_id": professional_id,
        "schedulings": schedulings
    }