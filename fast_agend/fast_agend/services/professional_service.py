from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.repositories.user_repository import UserRepository
from fast_agend.schemas import ProfessionalSchema, ProfessionalUpdateSchema, ProfessionalPublic, ProfessionalList
from fast_agend.models import Professional, User, UserRole
from fastapi import Depends, HTTPException, status

class ProfessionalService:
    def __init__(self, repository: ProfessionalRepository, user_repo: UserRepository):
        self.repository = repository
        self.user_repo = user_repo

    def create_professional(self, professional_data: ProfessionalSchema, current_user: User):
    
        user = self.user_repo.get_by_id(professional_data.id_user)

        if user.role != UserRole.CLIENT:
            raise HTTPException(400, "Usuário já é profissional ou admin")

        professional = Professional(
            id_user=user.id,
            id_establishment=professional_data.id_establishment,
            specialty=professional_data.specialty,
            active=professional_data.active,
        )

        user.role = UserRole.PROFESSIONAL

        return self.repository.create(professional)

    def list_professionals(self) -> list[Professional]:
        return self.repository.get_all()

    def update_professional(
        self, professional_id: int, professional_data: ProfessionalUpdateSchema, user: User
    ) -> Professional | None:

        professional = self.repository.get_by_id(professional_id)
        if not professional:
            return None

        data = professional_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(professional, field, value)

        return self.repository.update(professional)

    def delete_professional(self, professional_id: int, user: User) -> Professional | None:
        professional = self.repository.get_by_id(professional_id)
        if not professional:
            return None

        self.repository.delete(professional)
        return professional

    def list_professionals_complete(self):
        return self.repository.get_with_user_and_services()

    def list_by_establishment(self, establishment_id: int) -> list[Professional]:
        return self.repository.get_by_establishment(establishment_id)