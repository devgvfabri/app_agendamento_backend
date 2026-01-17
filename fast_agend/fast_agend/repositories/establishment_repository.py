from sqlalchemy.orm import Session
from fast_agend.models import Establishment

class EstablishmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, establishment: Establishment) -> Establishment:
        self.db.add(establishment)
        self.db.commit()
        self.db.refresh(establishment)
        return establishment

    def get_all(self) -> list[Establishment]:
        return self.db.query(Establishment).all()

    def get_by_id(self, establishments_id: int) -> Establishment | None:
        return self.db.query(Establishment).filter(Establishment.id == establishments_id).first()

    def update(self, establishment: Establishment) -> Establishment:
        self.db.add(establishment)  
        self.db.commit()
        self.db.refresh(establishment)
        return establishment

    def delete(self, establishments: Establishment) -> None:
        self.db.delete(establishments)
        self.db.commit()