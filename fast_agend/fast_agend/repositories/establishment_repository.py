from sqlalchemy.orm import Session
from fast_agend.models import Establishment

class Establishment:
    def __init__(self, db: Session):
        self.db = db

    def create(self, establishments: Establishment) -> Establishment:
        self.db.add(establishments)
        self.db.commit()
        self.db.refresh(establishments)
        return establishments

    def get_all(self) -> list[Establishment]:
        return self.db.query(Establishment).all()

    def get_by_id(self, establishments_id: int) -> Establishment | None:
        return self.db.query(Establishment).filter(Establishment.id == establishments_id).first()

    def update(self, establishments: Establishment) -> Establishment:
        self.db.commit()
        self.db.refresh(establishments)
        return establishments

    def delete(self, establishments: Establishment) -> None:
        self.db.delete(establishments)
        self.db.commit()