from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fast_agend.core.database import Base
from sqlalchemy import Time, Numeric, ForeignKey, Date


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    cpf: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    is_phone_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    code: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    expires_at : Mapped[datetime] = mapped_column(server_default=func.now())


class Establishment(Base):
    __tablename__ = "establishments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    addres: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    opening_hours: Mapped[datetime] = mapped_column(nullable=True)
    closing_time: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    duration: Mapped[Time] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    service_establishment_id: Mapped[int] = mapped_column(ForeignKey("establishments.id"))


class Professional(Base):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_establishment: Mapped[int] = mapped_column(ForeignKey("establishments.id"))
    specialty: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(nullable=False)

class Scheduling(Base):
    __tablename__ = "schedulings"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=True)
    id_user_client: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_professional: Mapped[int] = mapped_column(ForeignKey("professionals.id"))
    id_establishment: Mapped[int] = mapped_column(ForeignKey("establishments.id"))
    observation: Mapped[str] = mapped_column(nullable=True)

class Service_Scheduling(Base):
    __tablename__ = "service_schedulings"

    id_scheduling: Mapped[int] = relationship(back_populates="schedulings", primary_key=True)
    id_service: Mapped[int] = relationship(back_populates="services", primary_key=True)

class Availability(Base):
    __tablename__ = "availabilitys"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_professional: Mapped[int] = mapped_column(ForeignKey("professionals.id"))
    days: Mapped[int] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(nullable=False)
    end_time: Mapped[datetime] = mapped_column(nullable=False)

class Asessment(Base):
    __tablename__ = "asessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=False)
    id_scheduling: Mapped[int] = mapped_column(ForeignKey("schedulings.id"))

class Professional_Service(Base):

    __tablename__ = "professional_services"
    id_professional: Mapped[int] = mapped_column(ForeignKey("professionals.id"), primary_key=True)
    id_service: Mapped[int] = relationship(back_populates="services", primary_key=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    duration: Mapped[Time] = mapped_column(nullable=False)



