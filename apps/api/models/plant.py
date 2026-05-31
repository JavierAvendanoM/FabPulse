import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base

if TYPE_CHECKING:
    from models.division import Division
    from models.station import Station
    from models.worker import Worker
    from models.job import Job
    from models.subscription import Subscription


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    timezone: Mapped[str] = mapped_column(String, nullable=False, default="America/Toronto")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"))

    divisions: Mapped[list["Division"]] = relationship(back_populates="plant", cascade="all, delete-orphan")
    stations: Mapped[list["Station"]] = relationship(back_populates="plant", cascade="all, delete-orphan")
    workers: Mapped[list["Worker"]] = relationship(back_populates="plant", cascade="all, delete-orphan")
    jobs: Mapped[list["Job"]] = relationship(back_populates="plant", cascade="all, delete-orphan")
