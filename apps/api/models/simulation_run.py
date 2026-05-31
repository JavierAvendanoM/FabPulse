import uuid
from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from models.base import Base

if TYPE_CHECKING:
    from models.plant import Plant
    from models.job import Job


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("plants.id"), nullable=False)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    input_params: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    output_p50: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    output_p70: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    output_p95: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    iterations: Mapped[int] = mapped_column(Integer, default=1000)
    vertex_ai_request_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("NOW()"))

    plant: Mapped["Plant"] = relationship()
    job: Mapped["Job"] = relationship(back_populates="simulation_runs")
