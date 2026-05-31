from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from dependencies import get_current_user_id, get_current_plant
from models.plant import Plant
from schemas.plant import PlantResponse

router = APIRouter()


@router.get("/me")
async def get_auth_status(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Plant))
    return {"user_id": user_id, "authenticated": True}


@router.get("/plant", response_model=PlantResponse)
async def get_auth_plant(plant: Plant = Depends(get_current_plant)):
    return plant
