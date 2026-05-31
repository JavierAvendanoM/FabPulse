from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from dependencies import get_current_plant
from models.plant import Plant

router = APIRouter()


@router.get("/lei")
async def get_lei(plant: Plant = Depends(get_current_plant)):
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={"error": "Not implemented", "detail": "LEI analytics is Week 3 scope", "code": "NOT_IMPLEMENTED"},
    )


@router.get("/yield")
async def get_yield(plant: Plant = Depends(get_current_plant)):
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={"error": "Not implemented", "detail": "Yield analytics is Week 3 scope", "code": "NOT_IMPLEMENTED"},
    )
