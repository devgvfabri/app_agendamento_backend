from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fast_agend.core.deps import get_db
from fast_agend.repositories.service_repository import ServiceRepository
from fast_agend.services.services_service import ServicesService, ServiceList
from fast_agend.schemas import ServiceSchema, ServiceUpdateSchema, ServicePublic
from fast_agend.core.deps import get_service


router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=ServiceSchema)
def create_service(
    services: ServiceSchema,
    service: ServicesService = Depends(get_service),
):
    return service.create_service(services)


@router.get("/", response_model=ServiceList)
def list_services(service: ServicesService = Depends(get_service)):
    return {"services": service.list_services()}


@router.put("/{service_id}", response_model=ServicePublic)
def update_service(
    service_id: int,
    services: ServiceUpdateSchema,
    service: ServicesService = Depends(get_service),
):
    updated = service.update_service(service_id, services)
    if not updated:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado"
        )

    return updated


@router.delete("/{service_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_service(
    service_id: int,
    service: ServicesService = Depends(get_service),
):

    deleted = service.delete_service(service_id)
    if not deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Estabelecimento não encontrado")

    return deleted
