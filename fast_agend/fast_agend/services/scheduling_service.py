from fast_agend.repositories.scheduling_repository import SchedulingRepository
from fast_agend.schemas import SchedulingSchema, SchedulingList, SchedulingUpdateSchema, SchedulingPublic
from fast_agend.models import Scheduling
from fastapi import Depends, HTTPException, status
from http import HTTPStatus

class SchedulingService:
    def __init__(self, repository: SchedulingRepository):
        self.repository = repository

    def create_scheduling(self, scheduling_data: SchedulingSchema) -> Scheduling:

        has_conflict = self.repository.exists_conflict(
            professional_id=scheduling_data.id_professional,
            date=scheduling_data.date,
            start_time=scheduling_data.start_time,
            end_time=scheduling_data.end_time,
        )

        if has_conflict:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Horário indisponível para este profissional"
            )

        scheduling = Scheduling(
            date=scheduling_data.date,
            start_time=scheduling_data.start_time,
            end_time=scheduling_data.end_time,
            status=scheduling_data.status,
            id_user_client=scheduling_data.id_user_client,
            id_professional=scheduling_data.id_professional,
            id_establishment=scheduling_data.id_establishment,
            service_id=scheduling_data.service_id,
            observation=scheduling_data.observation,
        )

        return self.repository.create(scheduling)

    def list_schedulings(self) -> list[Scheduling]:
        return self.repository.get_all()

    def update_scheduling(
        self, scheduling_id: int, scheduling_data: SchedulingUpdateSchema
    ) -> Scheduling | None:

        scheduling = self.repository.get_by_id(scheduling_id)
        if not scheduling:
            return None

        data = scheduling_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(scheduling, field, value)

        return self.repository.update(scheduling)

    def delete_scheduling(self, scheduling_id: int) -> Scheduling | None:
        scheduling = self.repository.get_by_id(scheduling_id)
        if not scheduling:
            return None

        self.repository.delete(scheduling)
        return scheduling

    def list_by_professional(self, professional_id: int):
        return self.repository.list_by_professional(professional_id)