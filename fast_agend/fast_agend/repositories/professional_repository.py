from sqlalchemy.orm import Session
from fast_agend.models import Professional
from sqlalchemy.orm import joinedload

class ProfessionalRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, professinal: Professional) -> Professional:
        self.db.add(professinal)
        self.db.commit()
        self.db.refresh(professinal)
        return professinal

    def get_all(self) -> list[Professional]:
        return self.db.query(Professional).all()

    def get_by_id(self, professinals_id: int) -> Professional | None:
        return self.db.query(Professional).filter(Professional.id == professinals_id).first()

    def update(self, professinal: Professional) -> Professional:
        self.db.add(professinal)  
        self.db.commit()
        self.db.refresh(professinal)
        return professinal

    def delete(self, professinals: Professional) -> None:
        self.db.delete(professinals)
        self.db.commit()

    def get_with_user_and_services(self):
        return (
            self.db.query(Professional)
            .options(
                joinedload(Professional.user),
                joinedload(Professional.services)
            )
            .all()
        )

    def get_by_establishment(self, establishment_id: int):
        return (
            self.db.query(Professional)
            .options(joinedload(Professional.services))
            .filter(Professional.id_establishment == establishment_id)
            .all()
        )

    def get_by_user_id(self, user_id: int) -> Professional | None:
        return (
            self.db
            .query(Professional)
            .filter(Professional.id_user == user_id)
            .first()
        )

    