from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict

JobStatus = Literal["pending", "in_progress", "completed", "on_hold"]


class JobCreate(BaseModel):
    job_number: str
    division_id: Optional[UUID] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None
    engineering_hours: Optional[Decimal] = None
    priority: int = 0
    due_date: Optional[date] = None


class JobUpdate(BaseModel):
    job_number: Optional[str] = None
    division_id: Optional[UUID] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None
    engineering_hours: Optional[Decimal] = None
    priority: Optional[int] = None
    due_date: Optional[date] = None


class JobStatusUpdate(BaseModel):
    status: JobStatus


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    plant_id: UUID
    division_id: Optional[UUID]
    job_number: str
    customer_name: Optional[str]
    description: Optional[str]
    engineering_hours: Optional[Decimal]
    status: str
    priority: int
    due_date: Optional[date]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
