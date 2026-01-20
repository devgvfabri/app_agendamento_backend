from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.services.professional_service import ProfessionalService, ProfessionalList
from fast_agend.schemas import ProfessionalSchema, ProfessionalUpdateSchema, ProfessionalPublic
from fast_agend.core.deps import get_professional_service


router = APIRouter(prefix="/professionals", tags=["Professionals"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ProfessionalSchema)
def create_professional(
    professional: ProfessionalSchema,
    service: ProfessionalService = Depends(get_professional_service),
):
    return service.create_professional(professional)


@router.get("/", response_model=ProfessionalList)
def list_professionals(service: ProfessionalService = Depends(get_professional_service)):
    return {"professionals": service.list_professionals()}


@router.put("/{professional_id}", response_model=ProfessionalPublic)
def update_professional(
    professional_id: int,
    professional: ProfessionalUpdateSchema,
    service: ProfessionalService = Depends(get_professional_service),
):
    updated = service.update_professional(professional_id, professional)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado"
        )

    return updated


@router.delete("/{professional_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_professional(
    professional_id: int,
    service: ProfessionalService = Depends(get_professional_service),
):

    deleted = service.delete_professional(professional_id)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado")

    return deleted
