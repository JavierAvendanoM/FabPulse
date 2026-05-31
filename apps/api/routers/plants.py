import uuid
from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from database import get_db
from config import get_settings
from dependencies import get_current_user_id, get_current_plant
from models.plant import Plant
from schemas.plant import PlantCreate, PlantResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
async def create_plant(
    payload: PlantCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    settings = get_settings()

    plant = Plant(
        name=payload.name,
        company_name=payload.company_name,
        timezone=payload.timezone,
    )
    db.add(plant)
    await db.flush()

    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{settings.supabase_url}/auth/v1/admin/users/{user_id}",
            headers={
                "apikey": settings.supabase_service_role_key,
                "Authorization": f"Bearer {settings.supabase_service_role_key}",
                "Content-Type": "application/json",
            },
            json={"app_metadata": {"plant_id": str(plant.id)}},
        )
        if resp.status_code != 200:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to link plant to user account",
            )

    await db.commit()
    await db.refresh(plant)
    return plant


@router.get("/me", response_model=PlantResponse)
async def get_my_plant(plant: Plant = Depends(get_current_plant)):
    return plant
