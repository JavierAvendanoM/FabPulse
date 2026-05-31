import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base

if TYPE_CHECKING:
    from models.plant import Plant
    from models.division import Division
    from models.task_log import TaskLog
    from models.simulation_run import SimulationRun


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("plants.id", ondelete="CASCADE"), nullable=False
    )
    division_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("divisions.id"), nullable=True
    )
    job_number: Mapped[str] = mapped_column(String, nullable=False)
    customer_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    engineering_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending")
    priority: Mapped[int] = mapped_column(Integer, default=0)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"))

    plant: Mapped["Plant"] = relationship(back_populates="jobs")
    division: Mapped[Optional["Division"]] = relationship(back_populates="jobs")
    task_logs: Mapped[list["TaskLog"]] = relationship(back_populates="job", cascade="all, delete-orphan")
    simulation_runs: Mapped[list["SimulationRun"]] = relationship(back_populates="job")
