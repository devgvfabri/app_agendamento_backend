from fast_agend.repositories.scheduling_repository import SchedulingRepository
from fast_agend.repositories.service_repository import ServiceRepository
from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.schemas import SchedulingSchema, SchedulingList, SchedulingUpdateSchema, SchedulingPublic, SchedulingCreateSchema
from fast_agend.models import Scheduling
from fast_agend.services.slot_service import normalize_time
from fastapi import Depends, HTTPException, status
from http import HTTPStatus
from datetime import datetime, timedelta

class SchedulingService:
    def __init__(self, repository: SchedulingRepository, service_repo: ServiceRepository, availability_repo: AvailabilityRepository ):
        self.repository = repository
        self.service_repo = service_repo
        self.availability_repo = availability_repo

    def create_scheduling(self, scheduling_data: SchedulingCreateSchema) -> Scheduling:

        service = self.service_repo.get_by_id(scheduling_data.service_id)

        weekday = scheduling_data.date.weekday()

        availabilities = self.availability_repo.list_by_professional(
            scheduling_data.id_professional
        )

        day_availabilities = [
            a for a in availabilities if a.weekday == weekday
        ]

        if not day_availabilities:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Profissional não atende neste dia"
            )

        if not service:
            raise HTTPException(404, "Serviço não encontrado")

        start_dt = datetime.combine(
            scheduling_data.date,
            scheduling_data.start_time
        )
        start_dt += timedelta(minutes=1)

        end_dt = start_dt + timedelta(minutes=service.duration_minutes)
        end_dt -= timedelta(minutes=2)

        start_times = start_dt.time()
        end_time = end_dt.time()

        fits_in_availability = any(
            start_times >= a.start_time and end_time <= a.end_time
            for a in day_availabilities
        )

        if not fits_in_availability:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Horário fora da disponibilidade do profissional"
            )



        has_conflict = self.repository.exists_conflict(
            professional_id=scheduling_data.id_professional,
            date=scheduling_data.date,
            start_time=start_times,
            end_time=end_time,
        )

        if has_conflict:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Horário indisponível para este profissional"
            )

        scheduling = Scheduling(
            date=scheduling_data.date,
            start_time=start_times,
            end_time=end_time,
            status="Marcado",
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
        self,
        scheduling_id: int,
        scheduling_data: SchedulingUpdateSchema
    ) -> Scheduling | None:

        scheduling = self.repository.get_by_id(scheduling_id)
        if not scheduling:
            return None

        # 1️⃣ Atualizações simples
        if scheduling_data.status is not None:
            scheduling.status = scheduling_data.status

        if scheduling_data.observation is not None:
            scheduling.observation = scheduling_data.observation

        # 2️⃣ Se NÃO alterou data nem horário, pode salvar direto
        if (
            scheduling_data.date is None
            and scheduling_data.start_time is None
        ):
            return self.repository.update(scheduling)

        # 3️⃣ Resolver valores finais
        date = scheduling_data.date or scheduling.date
        start_time = scheduling_data.start_time or scheduling.start_time

        service = self.service_repo.get_by_id(scheduling.service_id)
        if not service:
            raise HTTPException(404, "Serviço não encontrado")

        # 4️⃣ Calcular end_time
        start_dt = datetime.combine(date, start_time)
        end_dt = start_dt + timedelta(minutes=service.duration_minutes)
        end_time = end_dt.time()

        # 5️⃣ Validar availability
        weekday = date.weekday()

        availabilities = self.availability_repo.list_by_professional(
            scheduling.id_professional
        )

        day_availabilities = [
            a for a in availabilities if a.weekday == weekday
        ]

        if not day_availabilities:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Profissional não atende neste dia"
            )

        fits_in_availability = any(
            normalize_time(start_time) >= normalize_time(a.start_time)
            and normalize_time(end_time) <= normalize_time(a.end_time)
            for a in day_availabilities
        )

        if not fits_in_availability:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Horário fora da disponibilidade do profissional"
            )

        # 6️⃣ Verificar conflito ignorando ele mesmo
        has_conflict = self.repository.exists_conflict(
            professional_id=scheduling.id_professional,
            date=date,
            start_time=start_time,
            end_time=end_time,
            ignore_scheduling_id=scheduling.id
        )

        if has_conflict:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                "Horário indisponível para este profissional"
            )

        # 7️⃣ Aplicar mudanças finais
        scheduling.date = date
        scheduling.start_time = start_time
        scheduling.end_time = end_time

        return self.repository.update(scheduling)

    def delete_scheduling(self, scheduling_id: int) -> Scheduling | None:
        scheduling = self.repository.get_by_id(scheduling_id)
        if not scheduling:
            return None

        self.repository.delete(scheduling)
        return scheduling

    def list_by_professional(self, professional_id: int):
        return self.repository.list_by_professional(professional_id)