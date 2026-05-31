from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    job_id: UUID
    worker_id: Optional[UUID] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    offline_created: bool = False


class TaskComplete(BaseModel):
    completed_at: datetime
    notes: Optional[str] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    plant_id: UUID
    job_id: UUID
    station_id: Optional[UUID]
    worker_id: Optional[UUID]
    started_at: datetime
    completed_at: Optional[datetime]
    duration_minutes: Optional[Decimal]
    offline_created: bool
    notes: Optional[str]
    created_at: datetime
