from datetime import datetime, date
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fast_agend.core.database import Base
from sqlalchemy import Time, Numeric, ForeignKey, Date
from decimal import Decimal



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
    professionals = relationship("Professional", back_populates="user")
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
    address: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    opening_time: Mapped[Time] = mapped_column(Time, nullable=True)
    closing_time: Mapped[Time] = mapped_column(Time, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    professionals = relationship("Professional", back_populates="establishment")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    service_establishment_id: Mapped[int] = mapped_column(ForeignKey("establishments.id"), nullable=False)
    professional_id: Mapped[int] = mapped_column(ForeignKey("professionals.id"), nullable=False)
    professional = relationship("Professional", back_populates="services")

class Professional(Base):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="professionals")
    id_establishment: Mapped[int] = mapped_column(ForeignKey("establishments.id"), nullable=False)
    specialty: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(nullable=True)
    services = relationship("Service", back_populates="professional")
    establishment = relationship("Establishment", back_populates="professionals")


class Scheduling(Base):
    __tablename__ = "schedulings"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[Time] = mapped_column(Time,nullable=False)
    end_time: Mapped[Time] = mapped_column(Time,nullable=False)
    status: Mapped[str] = mapped_column(nullable=True)
    id_user_client: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    id_professional: Mapped[int] = mapped_column(ForeignKey("professionals.id"), nullable=False)
    id_establishment: Mapped[int] = mapped_column(ForeignKey("establishments.id"), nullable=False)
    observation: Mapped[str] = mapped_column(nullable=True)

class Service_Scheduling(Base):
    __tablename__ = "service_schedulings"

    id_scheduling: Mapped[int] = mapped_column(ForeignKey("schedulings.id"), primary_key=True)
    id_service: Mapped[int] = mapped_column(ForeignKey("services.id"), primary_key=True)

class Availability(Base):
    __tablename__ = "availabilitys"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_professional: Mapped[int] = mapped_column(ForeignKey("professionals.id"), nullable=False)
    weekday: Mapped[int] = mapped_column(nullable=False)  
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)

class Asessment(Base):
    __tablename__ = "asessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[int] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    id_scheduling: Mapped[int] = mapped_column(ForeignKey("schedulings.id"), primary_key=True)



