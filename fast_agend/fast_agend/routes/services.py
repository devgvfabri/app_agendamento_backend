from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.service_repository import ServiceRepository
from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.services.services_service import ServicesService, ServiceList
from fast_agend.schemas import ServiceSchema, ServiceUpdateSchema, ServicePublic
from fast_agend.core.deps import get_service, get_current_user
from fast_agend.models import User


router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ServiceSchema)
def create_service(
    services: ServiceSchema,
    service: ServicesService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_service(services, current_user)


@router.get("/", response_model=ServiceList)
def list_services(service: ServicesService = Depends(get_service)):
    return {"services": service.list_services()}


@router.put("/{service_id}", response_model=ServicePublic)
def update_service(
    service_id: int,
    services: ServiceUpdateSchema,
    service: ServicesService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):
    updated = service.update_service(service_id, services, current_user)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado"
        )

    return updated


@router.delete("/{service_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_service(
    service_id: int,
    service: ServicesService = Depends(get_service),
    current_user: User = Depends(get_current_user),
):

    deleted = service.delete_service(service_id, current_user)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado")

    return deleted

@router.get(
    "/establishment/{establishment_id}",
    response_model=list[ServicePublic]
)
def list_services_by_establishment(
    establishment_id: int,
    db: Session = Depends(get_db),
):
    repository = ServiceRepository(db)
    professional_repo = ProfessionalRepository(db)
    service = ServicesService(repository, professional_repo)

    services = service.list_services_by_establishment(establishment_id)

    if not services:
        return []

    return services

@router.get(
    "/professional/{professional_id}",
    response_model=list[ServicePublic]
)
def list_services_by_professional(
    professional_id: int,
    db: Session = Depends(get_db),
):
    repository = ServiceRepository(db)
    professional_repo = ProfessionalRepository(db)
    service = ServicesService(repository, professional_repo)

    services = service.list_services_by_establishment(professional_id)

    if not services:
        return []

    return services
