import uuid
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from dependencies import get_current_plant
from models.plant import Plant
from models.division import Division
from models.station import Station
from schemas.plant import StationCreate, StationUpdate, StationResponse, KioskTokenResponse

router = APIRouter()


@router.get("/", response_model=list[StationResponse])
async def list_stations(
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Station).where(Station.plant_id == plant.id).order_by(Station.name)
    )
    return result.scalars().all()


@router.post("/", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
async def create_station(
    payload: StationCreate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    division = await db.get(Division, payload.division_id)
    if not division or division.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")

    station = Station(
        plant_id=plant.id,
        division_id=payload.division_id,
        name=payload.name,
    )
    db.add(station)
    await db.commit()
    await db.refresh(station)
    return station


@router.put("/{station_id}", response_model=StationResponse)
async def update_station(
    station_id: uuid.UUID,
    payload: StationUpdate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    station = await db.get(Station, station_id)
    if not station or station.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    if payload.name is not None:
        station.name = payload.name
    if payload.is_active is not None:
        station.is_active = payload.is_active

    await db.commit()
    await db.refresh(station)
    return station


@router.post("/{station_id}/kiosk-token", response_model=KioskTokenResponse)
async def generate_kiosk_token(
    station_id: uuid.UUID,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    station = await db.get(Station, station_id)
    if not station or station.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")

    station.kiosk_token = secrets.token_urlsafe(32)
    await db.commit()
    return KioskTokenResponse(station_id=station.id, kiosk_token=station.kiosk_token)
