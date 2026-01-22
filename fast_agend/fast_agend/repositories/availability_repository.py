from sqlalchemy.orm import Session
from fast_agend.models import Availability

class AvailabilityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, avaibility: Availability) -> Availability:
        self.db.add(avaibility)
        self.db.commit()
        self.db.refresh(avaibility)
        return avaibility

    def get_all(self) -> list[Availability]:
        return self.db.query(Availability).all()

    def get_by_id(self, avaibilitys_id: int) -> Availability | None:
        return self.db.query(Availability).filter(Availability.id == avaibilitys_id).first()

    def update(self, avaibility: Availability) -> Availability:
        self.db.add(avaibility)  
        self.db.commit()
        self.db.refresh(avaibility)
        return avaibility

    def delete(self, avaibilitys: Availability) -> None:
        self.db.delete(avaibilitys)
        self.db.commit()

    def list_by_professional(self, db: Session, professional_id: int) -> list[Availability]:
        return (db.query(Availability).filter(Availability.id_professional == professional_id).order_by(Availability.weekday,Availability.start_time).all())