from sqlalchemy.orm import Session
from fast_agend.models import Availability

class AvailabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Availability]:
        return self.db.query(Availability).all()

    def get_by_id(self, avaibilitys_id: int) -> Availability | None:
        return self.db.query(Availability).filter(Availability.id == avaibilitys_id).first()

    def get_by_id_db(
        self,
        db: Session,
        availability_id: int
    ) -> Availability | None:
        return db.get(Availability, availability_id)

    def update(self, db: Session, availability: Availability) -> Availability:
        db.add(availability)
        db.commit()
        db.refresh(availability)
        return availability

    def delete(self, avaibilitys: Availability) -> None:
        self.db.delete(avaibilitys)
        self.db.commit()

    def list_by_professional(self, db: Session, professional_id: int) -> list[Availability]:
        return (db.query(Availability).filter(Availability.id_professional == professional_id).order_by(Availability.weekday,Availability.start_time).all())

    def create(
        self,
        db: Session,
        availability: Availability
    ) -> Availability:
        db.add(availability)
        db.commit()
        db.refresh(availability)
        return availability

    def find_conflicts(
        self,
        db: Session,
        professional_id: int,
        weekday: int,
        start_time,
        end_time
    ):
        return (
            db.query(Availability)
            .filter(
                Availability.id_professional == professional_id,
                Availability.weekday == weekday,
                Availability.start_time < end_time,
                Availability.end_time > start_time
            )
            .all()
        )

    def find_conflicts_excluding_id(
        self,
        db: Session,
        availability_id: int,
        professional_id: int,
        weekday: int,
        start_time,
        end_time
    ):
        return (
            db.query(Availability)
            .filter(
                Availability.id != availability_id,
                Availability.id_professional == professional_id,
                Availability.weekday == weekday,
                Availability.start_time < end_time,
                Availability.end_time > start_time
            )
            .all()
        )