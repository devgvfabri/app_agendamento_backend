from fast_agend.repositories.establishment_repository import EstablishmentRepository
from fast_agend.schemas import EstablishmentSchema, EstablishmentList, EstablishmentUpdateSchema, EstablishmentPublic
from fast_agend.models import Establishment, User
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

class EstablishmentService:
    def __init__(self, repository: EstablishmentRepository):
        self.repository = repository

    def create_establishment(self, establishment_data: EstablishmentSchema, user: User) -> Establishment:
        establishment = Establishment(
            name=establishment_data.name,
            address=establishment_data.address,
            phone=establishment_data.phone,
            opening_time=establishment_data.opening_time,
            closing_time=establishment_data.closing_time,
        )

        try:
            return self.repository.create(establishment)

        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um estabelecimento com esse nome ou telefone."
            )

    def list_establishments(self) -> list[Establishment]:
        return self.repository.get_all()

    def update_establishment(
        self, establishment_id: int, establishment_data: EstablishmentUpdateSchema, user: User
    ) -> Establishment | None:

        establishment = self.repository.get_by_id(establishment_id)
        if not establishment:
            return None

        data = establishment_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(establishment, field, value)
        try:
            return self.repository.update(establishment)

        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um estabelecimento com esse nome ou telefone."
            )

    def delete_establishment(self, establishment_id: int, user: User) -> Establishment | None:
        establishment = self.repository.get_by_id(establishment_id)
        if not establishment:
            return None

        self.repository.delete(establishment)
        return establishment