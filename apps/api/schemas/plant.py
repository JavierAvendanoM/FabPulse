from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PlantCreate(BaseModel):
    name: str
    company_name: str
    timezone: str = "America/Toronto"


class PlantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    company_name: str
    timezone: str
    created_at: datetime


class DivisionCreate(BaseModel):
    name: str


class DivisionUpdate(BaseModel):
    name: Optional[str] = None


class DivisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    plant_id: UUID
    name: str
    created_at: datetime


class StationCreate(BaseModel):
    division_id: UUID
    name: str


class StationUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class StationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    division_id: UUID
    plant_id: UUID
    name: str
    kiosk_token: Optional[str]
    is_active: bool


class KioskTokenResponse(BaseModel):
    station_id: UUID
    kiosk_token: str
