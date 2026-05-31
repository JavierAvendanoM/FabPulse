import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from dependencies import get_current_plant
from models.plant import Plant
from models.division import Division
from schemas.plant import DivisionCreate, DivisionUpdate, DivisionResponse

router = APIRouter()


@router.get("/", response_model=list[DivisionResponse])
async def list_divisions(
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Division).where(Division.plant_id == plant.id).order_by(Division.name)
    )
    return result.scalars().all()


@router.post("/", response_model=DivisionResponse, status_code=status.HTTP_201_CREATED)
async def create_division(
    payload: DivisionCreate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    division = Division(plant_id=plant.id, name=payload.name)
    db.add(division)
    await db.commit()
    await db.refresh(division)
    return division


@router.put("/{division_id}", response_model=DivisionResponse)
async def update_division(
    division_id: uuid.UUID,
    payload: DivisionUpdate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    division = await db.get(Division, division_id)
    if not division or division.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")

    if payload.name is not None:
        division.name = payload.name

    await db.commit()
    await db.refresh(division)
    return division


@router.delete("/{division_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_division(
    division_id: uuid.UUID,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    division = await db.get(Division, division_id)
    if not division or division.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")
    await db.delete(division)
    await db.commit()
