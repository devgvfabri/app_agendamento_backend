from fast_agend.repositories.service_repository import ServiceRepository
from fast_agend.schemas import ServiceSchema, ServiceList, ServiceUpdateSchema, ServicePublic
from fast_agend.models import Service
from fastapi import Depends, HTTPException, status

class ServicesService:
    def __init__(self, repository: ServiceRepository):
        self.repository = repository

    def create_service(self, service_data: ServiceSchema) -> Service:

        service = Service(
            name=service_data.name,
            description=service_data.description,
            duration_minutes=service_data.duration_minutes,
            price=service_data.price,
            service_establishment_id=service_data.service_establishment_id,
        )

        service = self.repository.create(service)

        return service

    def list_services(self) -> list[Service]:
        return self.repository.get_all()

    def update_service(
        self, service_id: int, service_data: ServiceUpdateSchema
    ) -> Service | None:

        service = self.repository.get_by_id(service_id)
        if not service:
            return None

        data = service_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(service, field, value)

        return self.repository.update(service)

    def delete_service(self, service_id: int) -> Service | None:
        service = self.repository.get_by_id(service_id)
        if not service:
            return None

        self.repository.delete(service)
        return service
    
    def list_services_by_establishment(
        self, establishment_id: int
    ) -> list[Service]:
        return self.repository.get_by_establishment(establishment_id)