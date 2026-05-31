from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class WorkerCreate(BaseModel):
    name: str
    employee_id: Optional[str] = None
    pin: Optional[str] = None


class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    employee_id: Optional[str] = None
    pin: Optional[str] = None
    is_active: Optional[bool] = None


class WorkerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    plant_id: UUID
    name: str
    employee_id: Optional[str]
    is_active: bool
    created_at: datetime


class WorkerPinVerify(BaseModel):
    worker_id: UUID
    pin: str
