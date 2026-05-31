import uuid
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from database import get_db
from config import get_settings

security = HTTPBearer()


def _decode_jwt(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    payload = _decode_jwt(credentials.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")
    return user_id


async def get_current_plant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    from models.plant import Plant

    payload = _decode_jwt(credentials.credentials)
    plant_id = (payload.get("app_metadata") or {}).get("plant_id")
    if not plant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No plant associated with this account. Create a plant first.",
        )

    plant = await db.get(Plant, uuid.UUID(plant_id))
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")
    return plant


async def get_kiosk_station(
    x_kiosk_token: str = Header(..., alias="X-Kiosk-Token"),
    db: AsyncSession = Depends(get_db),
):
    from models.station import Station

    result = await db.execute(
        select(Station).where(
            Station.kiosk_token == x_kiosk_token,
            Station.is_active == True,
        )
    )
    station = result.scalar_one_or_none()
    if not station:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid kiosk token")
    return station
