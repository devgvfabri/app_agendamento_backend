from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.schemas import AvailabilitySchema, AvailabilityList, AvailabilityUpdateSchema, AvailabilityPublic
from fast_agend.models import Availability
from fastapi import Depends, HTTPException, status

class AvailabilityService:
    def __init__(self, repository: AvailabilityRepository):
        self.repository = repository

    def create_availability(self, availability_data: AvailabilitySchema) -> Availability:

        availability = Availability(
            id_professional=availability_data.id_professional,
            weekday=availability_data.weekday,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time,
        )

        availability = self.repository.create(availability)

        return availability

    def list_availabilitys(self) -> list[Availability]:
        return self.repository.get_all()

    def update_availability(
        self, availability_id: int, availability_data: AvailabilityUpdateSchema
    ) -> Availability | None:

        availability = self.repository.get_by_id(availability_id)
        if not availability:
            return None

        data = availability_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(availability, field, value)

        return self.repository.update(availability)

    def delete_availability(self, availability_id: int) -> Availability | None:
        availability = self.repository.get_by_id(availability_id)
        if not availability:
            return None

        self.repository.delete(availability)
        return availability