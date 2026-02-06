from fast_agend.repositories.scheduling_repository import SchedulingRepository
from fast_agend.repositories.professional_repository import ProfessionalRepository
from fast_agend.repositories.service_repository import ServiceRepository
from fast_agend.repositories.availability_repository import AvailabilityRepository
from fast_agend.schemas import SchedulingSchema, SchedulingList, SchedulingUpdateSchema, SchedulingPublic, SchedulingCreateSchema, SchedulingStatus
from fast_agend.models import Scheduling, User, UserRole
from fast_agend.services.slot_service import normalize_time
from fastapi import Depends, HTTPException, status
from http import HTTPStatus
from datetime import datetime, timedelta, date
from datetime import date as DateType
import logging

logger = logging.getLogger("Scheduling")


ALLOWED_TRANSITIONS = {
    SchedulingStatus.PENDING: {
        SchedulingStatus.CONFIRMED,
        SchedulingStatus.CANCELLED,
    },
    SchedulingStatus.CONFIRMED: {
        SchedulingStatus.CANCELLED,
        SchedulingStatus.FINISHED,
    },
    SchedulingStatus.FINISHED: set(),
    SchedulingStatus.CANCELLED: set(),
}

class SchedulingService:
    def __init__(self, repository: SchedulingRepository, service_repo: ServiceRepository, availability_repo: AvailabilityRepository, professional_repo: ProfessionalRepository ):
        self.repository = repository
        self.service_repo = service_repo
        self.availability_repo = availability_repo
        self.professional_repo = professional_repo

    def create_scheduling(self, scheduling_data: SchedulingCreateSchema, user: User) -> Scheduling:

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

        if scheduling_data.date < date.today():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Não é possível realizar o agendamento em dias já ocorridos."
            )

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

        service = self.service_repo.get_by_id(scheduling_data.service_id)

        if not service:
            logger.warning(
                "Serviço não encontrado | service_id=%s user=%s",
                scheduling_data.service_id,
                user.id
            )
            raise HTTPException(404, "Serviço não encontrado")

        if service.professional_id != scheduling_data.id_professional:
            logger.warning(
                "Serviço não pertence ao profissional | service=%s professional=%s user=%s",
                service.id,
                scheduling_data.id_professional,
                user.id
            )
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Este serviço não pertence ao profissional informado"
            )

        professional = self.professional_repo.get_by_id_and_establishment(
            scheduling_data.id_professional,
            scheduling_data.id_establishment
        )

        if not professional:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Profissional não pertence a este estabelecimento"
            )

        scheduling = Scheduling(
            date=scheduling_data.date,
            start_time=start_times,
            end_time=end_time,
            status=SchedulingStatus.PENDING,
            id_user_client=user.id,
            id_professional=scheduling_data.id_professional,
            id_establishment=scheduling_data.id_establishment,
            service_id=scheduling_data.service_id,
            observation=scheduling_data.observation,
        )
        logger.info(
            "Criando agendamento | user=%s professional=%s service=%s date=%s",
            user.id,
            scheduling_data.id_professional,
            scheduling_data.service_id,
            scheduling_data.date
        )

        return self.repository.create(scheduling)

    def list_schedulings(self) -> list[Scheduling]:
        return self.repository.get_all()

    def update_scheduling(
        self,
        scheduling_id: int,
        scheduling_data: SchedulingUpdateSchema,
        user: User,
    ) -> Scheduling | None:

        scheduling = self.repository.get_by_id(scheduling_id)

        if scheduling.status in {
            SchedulingStatus.CANCELLED,
            SchedulingStatus.FINISHED,
        }:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Agendamento cancelado ou finalizado não pode ser alterado"
            )

        schedule_date = scheduling_data.date

        if scheduling_data.date is not None:
            if scheduling_data.date < DateType.today():
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Agendamento não pode ser no passado"
                )

        if not scheduling:
            return None

        if scheduling_data.observation is not None:
            scheduling.observation = scheduling_data.observation

        current = scheduling.status
        new = SchedulingStatus.PENDING

        if scheduling_data.status is not None:
            current = scheduling.status
            new = scheduling_data.status

            if new not in ALLOWED_TRANSITIONS[current]:
                raise HTTPException(
                    HTTPStatus.BAD_REQUEST,
                    f"Transição inválida: {current} → {new}"
                )

        if (
            scheduling_data.date is None
            and scheduling_data.start_time is None
        ):
            return self.repository.update(scheduling)

        date = scheduling_data.date or scheduling.date
        start_time = scheduling_data.start_time or scheduling.start_time

        service = self.service_repo.get_by_id(scheduling.service_id)
        if not service:
            raise HTTPException(404, "Serviço não encontrado")

        start_dt = datetime.combine(date, start_time)
        start_dt += timedelta(minutes=1)
        end_dt = start_dt + timedelta(minutes=service.duration_minutes)
        end_dt -= timedelta(minutes=2)
        start_times = start_dt.time()
        end_time = end_dt.time()

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

        has_conflict = self.repository.exists_conflict(
            professional_id=scheduling.id_professional,
            date=date,
            start_time=start_times,
            end_time=end_time,
            ignore_scheduling_id=scheduling.id
        )

        if has_conflict:
            raise HTTPException(
                HTTPStatus.CONFLICT,
                "Horário indisponível para este profissional"
            )
        
        scheduling.status = SchedulingStatus.PENDING

        scheduling.date = date
        scheduling.start_time = start_times
        scheduling.end_time = end_time

        return self.repository.update(scheduling)

    def delete_scheduling(self, scheduling_id: int, user: User) -> Scheduling | None:
        scheduling = self.repository.get_by_id(scheduling_id)
        if not scheduling:
            return None

        self.repository.delete(scheduling)
        return scheduling

    def list_by_professional(self, current_user: User,  professional_id: int):

        if current_user.role == UserRole.ADMIN:
            return self.repository.list_all(date)

        if current_user.role != UserRole.PROFESSIONAL:
            raise HTTPException(403, "Apenas profissionais")

        professional = self.professional_repo.get_by_user_id(current_user.id)

        if not professional:
            raise HTTPException(404, "Profissional não encontrado")

        if professional.id != professional_id:
            raise HTTPException(403, "Você só pode acessar seus próprios agendamentos")

        return self.repository.list_by_professional(professional_id)

    def confirm(self, scheduling_id: int, user: User):
        scheduling = self.repository.get_by_id(scheduling_id)
        professional = self.professional_repo.get_by_user_id(user.id)

        if not scheduling:
            raise HTTPException(404, "Agendamento não encontrado")

        if not professional:
            raise HTTPException(403, "Usuário não é um profissional")

        if scheduling.id_professional != professional.id:
            raise HTTPException(403, "Você não pode confirmar este agendamento")

        if scheduling.status != SchedulingStatus.PENDING:
            raise HTTPException(
                400,
                "Somente agendamentos pendentes podem ser confirmados"
            )

        scheduling.status = SchedulingStatus.CONFIRMED
        return self.repository.update(scheduling)

    def cancel(self, scheduling_id: int, user: User):
        scheduling = self.repository.get_by_id(scheduling_id)
        professional = self.professional_repo.get_by_user_id(user.id)


        if scheduling.status in [
            SchedulingStatus.CANCELLED,
            SchedulingStatus.FINISHED
        ]:
            raise HTTPException(400, "Agendamento não pode ser cancelado")

        if user.id == scheduling.id_user_client:
            pass

        elif professional and professional.id == scheduling.id_professional:
            pass

        else:
            raise HTTPException(403, "Você não pode cancelar este agendamento")

        scheduling.status = SchedulingStatus.CANCELLED
        return self.repository.update(scheduling)

    def list_by_professional_date(self, professional_id: int, current_user: User, target_date: date):
        if current_user.role == UserRole.ADMIN:
            return self.repository.list_all(date)

        if current_user.role != UserRole.PROFESSIONAL:
            raise HTTPException(403, "Apenas profissionais")

        professional = self.professional_repo.get_by_user_id(current_user.id)

        if not professional:
            raise HTTPException(404, "Profissional não encontrado")

        if professional.id != professional_id:
            raise HTTPException(403, "Você só pode acessar seus próprios agendamentos")

        return self.repository.list_by_professional_and_date(professional_id, target_date)

    def list_by_user(self, user_id: int):
        return self.repository.list_by_user(user_id)

    def list_by_user_secure(self, user_id: int, user: User):

        if user.role != UserRole.ADMIN and user.id != user_id:
            raise HTTPException(403, "Sem permissão")

        return self.repository.list_by_user(user_id)

    def list_by_user_date(self, user_id: int, user: User, target_date: date):
        if user.role != UserRole.ADMIN and user.id != user_id:
            raise HTTPException(403, "Sem permissão")

        return self.repository.list_by_user_and_date(user_id, target_date)
