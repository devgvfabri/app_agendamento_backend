from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.services.availability_service import AvailabilityService, AvailabilityList
from fast_agend.schemas import AvailabilitySchema, AvailabilityUpdateSchema, AvailabilityPublic
from fast_agend.core.deps import get_availability_service


router = APIRouter(prefix="/availabilitys", tags=["Availability"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=AvailabilitySchema)
def create_availability(
    availability: AvailabilitySchema,
    service: AvailabilityService = Depends(get_availability_service),
):
    return service.create_availability(availability)


@router.get("/", response_model=AvailabilityList)
def list_availabilitys(service: AvailabilityService = Depends(get_availability_service)):
    return {"availabilitys": service.list_availabilitys()}


@router.put("/{availability_id}", response_model=AvailabilityPublic)
def update_availability(
    availability_id: int,
    availability: AvailabilityUpdateSchema,
    service: AvailabilityService = Depends(get_availability_service),
):
    updated = service.update_availability(availability_id, availability)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Disponibilidade não encontrada"
        )

    return updated


@router.delete("/{availability_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_availabilityt(
    availability_id: int,
    service: AvailabilityService = Depends(get_availability_service),
):

    deleted = service.delete_availabilityt(availability_id)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Disponibilidade não encontrado")

    return deleted