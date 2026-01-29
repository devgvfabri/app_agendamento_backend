from sqlalchemy.orm import Session, joinedload
from fast_agend.models import Scheduling
from datetime import datetime, timedelta, time, date
from fast_agend.schemas import  SchedulingStatus


BLOCKING_STATUSES = [
    SchedulingStatus.PENDING,
    SchedulingStatus.CONFIRMED,
]

class SchedulingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, scheduling: Scheduling) -> Scheduling:
        self.db.add(scheduling)
        self.db.commit()
        self.db.refresh(scheduling)
        return scheduling

    def get_all(self) -> list[Scheduling]:
        return self.db.query(Scheduling).all()

    def get_by_id(self, schedulings_id: int) -> Scheduling | None:
        return self.db.query(Scheduling).filter(Scheduling.id == schedulings_id).first()

    def update(self, scheduling: Scheduling) -> Scheduling:
        self.db.add(scheduling)  
        self.db.commit()
        self.db.refresh(scheduling)
        return scheduling

    def delete(self, schedulings: Scheduling) -> None:
        self.db.delete(schedulings)
        self.db.commit()

    def list_by_professional(self, professional_id: int):
        return (
            self.db.query(Scheduling)
            .options(
                joinedload(Scheduling.service),
                joinedload(Scheduling.user),
            )
            .filter(Scheduling.id_professional == professional_id)
            .all()
        )

    def list_by_professional_and_date(
        self,
        professional_id: int,
        target_date: date,
    ):
        return (
            self.db.query(Scheduling)
            .filter(
                Scheduling.id_professional == professional_id,
                Scheduling.date == target_date
            )
            .all()
        )

    def exists_conflict(
        self,
        professional_id: int,
        date: date,
        start_time: time,
        end_time: time,
        ignore_scheduling_id: int | None = None,
    ) -> bool:

        query = self.db.query(Scheduling).filter(
            Scheduling.id_professional == professional_id,
            Scheduling.date == date,
            Scheduling.start_time < end_time,
            Scheduling.end_time > start_time,
            Scheduling.status.in_(BLOCKING_STATUSES),
        )

        if ignore_scheduling_id is not None:
            query = query.filter(Scheduling.id != ignore_scheduling_id)

        return self.db.query(query.exists()).scalar()