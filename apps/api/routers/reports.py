from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from dependencies import get_current_plant
from models.plant import Plant

router = APIRouter()


@router.post("/monthly")
async def generate_monthly_report(plant: Plant = Depends(get_current_plant)):
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={"error": "Not implemented", "detail": "AI reports (Vertex AI) is Week 4 scope", "code": "NOT_IMPLEMENTED"},
    )
