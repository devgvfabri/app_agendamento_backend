from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.repositories.scheduling_repository import SchedulingRepository
from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.schemas import AvailabilitySchema, AvailabilityList, AvailabilityUpdateSchema, AvailabilityPublic
from fast_agend.models import Availability, User
from fast_agend.services.slot_service import generate_time_slots, generate_slots, has_conflict
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time, date
from datetime import date as DateType
from fast_agend.utils import normalize_time


class AvailabilityService:
    def __init__(self, repository: AvailabilityRepository, scheduling_repo: SchedulingRepository, professional_repo: ProfessionalRepository):
        self.repository = repository
        self.scheduling_repo = scheduling_repo
        self.professional_repo = professional_repo

    def create_availability(
        self,
        db: Session,
        availability_data: AvailabilitySchema,
        user: User
    ) -> Availability:

        professional = self.professional_repo.get_by_id(
            availability_data.id_professional
        )

        if not professional:
            raise HTTPException(
                status_code=404,
                detail="Profissional não encontrado"
            )

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

    def update_availability(self, db: Session, availability_id: int, availability_data: AvailabilityUpdateSchema, user: User) -> Availability | None:
        availability = self.repository.get_by_id_db(db, availability_id)
        if not availability:
            return None

        data = availability_data.model_dump(exclude_unset=True)

        start_time = data.get("start_time", availability.start_time)
        end_time = data.get("end_time", availability.end_time)
        weekday = data.get("weekday", availability.weekday)

        start_time = normalize_time(start_time)
        end_time = normalize_time(end_time)


        if start_time is not None:
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

    def delete_availability(self, availability_id: int, user: User) -> Availability | None:
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
            professional_id=professional_id
        )

        if not availabilities:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma disponibilidade encontrada para este profissional"
            )

        return availabilities

    def get_available_slots(
        self,
        professional_id: int,
        target_date: DateType,
        slot_minutes: int = 30
    ):
        weekday = target_date.weekday()

        availabilities = self.repository.list_by_professional(
            professional_id
        )

        day_availabilities = [
            a for a in availabilities if a.weekday == weekday
        ]

        if not day_availabilities:
            return []

        schedulings = self.scheduling_repo.list_by_professional_and_date(
            professional_id,
            target_date
        )

        free_slots = []

        for availability in day_availabilities:
            slots = generate_slots(
                availability.start_time,
                availability.end_time,
                slot_minutes,
                target_date
            )

            for slot in slots:
                if not has_conflict(
                    slot["start"],
                    slot["end"],
                    schedulings
                ):
                    free_slots.append(slot["start"].strftime("%H:%M"))

        return {
            "date": target_date,
            "weekday": weekday,
            "slots": free_slots
        }