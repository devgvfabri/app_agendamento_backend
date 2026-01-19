from sqlalchemy.orm import Session
from fast_agend.models import Service

class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, service: Service) -> Service:
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return service

    def get_all(self) -> list[Service]:
        return self.db.query(Service).all()

    def get_by_id(self, services_id: int) -> Service | None:
        return self.db.query(Service).filter(Service.id == services_id).first()

    def update(self, service: Service) -> Service:
        self.db.add(service)  
        self.db.commit()
        self.db.refresh(service)
        return service

    def delete(self, services: Service) -> None:
        self.db.delete(services)
        self.db.commit()

    def get_by_establishment(self, establishment_id: int) -> list[Service]:
        return (
            self.db
            .query(Service)
            .filter(Service.service_establishment_id == establishment_id)
            .all()
        )