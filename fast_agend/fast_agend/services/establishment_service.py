from fast_agend.repositories.establishment_repository import Establishment
from fast_agend.schemas import EstablishmentSchema
from fast_agend.models import Establishment
from fastapi import Depends, HTTPException, status

class EstablishmentService:
    def __init__(self, repository: Establishment):
        self.repository = repository

    def create_establishment(self, establishment_data: EstablishmentSchema) -> Establishment:

        establishment = Establishment(
            name=establishment_data.name,
            address=establishment_data.address,
            phone=establishment_data.phone,
            opening_time=establishment_data.opening_time,
            closing_time=establishment_data.closing_time,
        )

        establishment = self.repository.create(establishment)

        return establishment

    def list_establishments(self) -> list[Establishment]:
        return self.repository.get_all()

    def update_establishment(self, establishment_id: int, establishment_data: EstablishmentSchema) -> Establishment | None:
        establishment = self.repository.get_by_id(establishment_id)
        if not establishment:
            return None

        data = establishment_data.model_dump(exclude_unset=True)

        return self.repository.update(establishment)

    def delete_establishment(self, establishment_id: int) -> Establishment | None:
        establishment = self.repository.get_by_id(establishment_id)
        if not establishment:
            return None

        self.repository.delete(establishment)
        return establishment