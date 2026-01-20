from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.schemas import ProfessionalSchema, ProfessionalUpdateSchema, ProfessionalPublic, ProfessionalList
from fast_agend.models import Professional
from fastapi import Depends, HTTPException, status

class ProfessionalService:
    def __init__(self, repository: ProfessionalRepository):
        self.repository = repository

    def create_professional(self, professional_data: ProfessionalSchema) -> Professional:

        professional = Professional(
            id_user=professional_data.id_user,
            id_establishment=professional_data.id_establishment,
            specialty=professional_data.specialty,
            active=professional_data.active,
        )

        professional = self.repository.create(professional)

        return professional

    def list_professionals(self) -> list[Professional]:
        return self.repository.get_all()

    def update_professional(
        self, professional_id: int, professional_data: ProfessionalUpdateSchema
    ) -> Professional | None:

        professional = self.repository.get_by_id(professional_id)
        if not professional:
            return None

        data = professional_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(professional, field, value)

        return self.repository.update(professional)

    def delete_professional(self, professional_id: int) -> Professional | None:
        professional = self.repository.get_by_id(professional_id)
        if not professional:
            return None

        self.repository.delete(professional)
        return professional