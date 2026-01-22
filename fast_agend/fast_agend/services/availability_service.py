from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.schemas import AvailabilitySchema, AvailabilityList, AvailabilityUpdateSchema, AvailabilityPublic
from fast_agend.models import Availability
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session


class AvailabilityService:
    def __init__(self, repository: AvailabilityRepository):
        self.repository = repository

    def create_availability(
        self,
        db: Session,
        availability_data: AvailabilitySchema
    ) -> Availability:

        if availability_data.start_time >= availability_data.end_time:
            raise HTTPException(
                status_code=400,
                detail="start_time deve ser menor que end_time"
            )

        conflicts = self.repository.find_conflicts(
            db=db,
            professional_id=availability_data.id_professional,
            weekday=availability_data.weekday,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time
        )

        if conflicts:
            raise HTTPException(
                status_code=409,
                detail="Conflito com outra disponibilidade já cadastrada"
            )

        availability = Availability(
            id_professional=availability_data.id_professional,
            weekday=availability_data.weekday,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time
        )

        return self.repository.create(db, availability)

    def list_availabilitys(self) -> list[Availability]:
        return self.repository.get_all()

    def update_availability(self, db: Session, availability_id: int, availability_data: AvailabilityUpdateSchema) -> Availability | None:
        availability = self.repository.get_by_id_db(db, availability_id)
        if not availability:
            return None

        data = availability_data.model_dump(exclude_unset=True)

        start_time = data.get("start_time", availability.start_time)
        end_time = data.get("end_time", availability.end_time)
        weekday = data.get("weekday", availability.weekday)

        if start_time >= end_time:
            raise HTTPException(
                status_code=400,
                detail="start_time deve ser menor que end_time"
            )

        conflicts = self.repository.find_conflicts_excluding_id(
            db=db,
            availability_id=availability.id,
            professional_id=availability.id_professional,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time
        )

        if conflicts:
            raise HTTPException(
                status_code=409,
                detail="Conflito com outra disponibilidade já cadastrada"
            )

        for field, value in data.items():
            setattr(availability, field, value)

        return self.repository.update(db, availability)

    def delete_availability(self, availability_id: int) -> Availability | None:
        availability = self.repository.get_by_id(availability_id)
        if not availability:
            return None

        self.repository.delete(availability)
        return availability
    
    def get_professional_availabilities(
        self,
        db,
        professional_id: int
    ):
        availabilities = self.repository.list_by_professional(
            db=db,
            professional_id=professional_id
        )

        if not availabilities:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma disponibilidade encontrada para este profissional"
            )

        return availabilities