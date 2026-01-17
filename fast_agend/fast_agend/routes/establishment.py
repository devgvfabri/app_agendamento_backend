from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.establishment_repository import EstablishmentRepository
from fast_agend.services.establishment_service import EstablishmentService, EstablishmentList
from fast_agend.schemas import EstablishmentSchema, EstablishmentUpdateSchema, EstablishmentPublic
from fast_agend.core.deps import get_establishment_service


router = APIRouter(prefix="/establishments", tags=["Establishments"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=EstablishmentSchema)
def create_establishment(
    establishment: EstablishmentSchema,
    service: EstablishmentService = Depends(get_establishment_service),
):
    return service.create_establishment(establishment)


@router.get("/", response_model=EstablishmentList)
def list_establishments(service: EstablishmentService = Depends(get_establishment_service)):
    return {"establishments": service.list_establishments()}


@router.put("/{establishment_id}", response_model=EstablishmentPublic)
def update_establishment(
    establishment_id: int,
    establishment: EstablishmentUpdateSchema,
    service: EstablishmentService = Depends(get_establishment_service),
):
    updated = service.update_establishment(establishment_id, establishment)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado"
        )

    return updated


@router.delete("/{establishment_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_establishment(
    establishment_id: int,
    service: EstablishmentService = Depends(get_establishment_service),
):

    deleted = service.delete_establishment(establishment_id)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado")

    return deleted
