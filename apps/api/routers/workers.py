import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from database import get_db
from dependencies import get_current_plant
from models.plant import Plant
from models.worker import Worker
from schemas.worker import WorkerCreate, WorkerUpdate, WorkerResponse, WorkerPinVerify

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=list[WorkerResponse])
async def list_workers(
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Worker)
        .where(Worker.plant_id == plant.id, Worker.is_active == True)
        .order_by(Worker.name)
    )
    return result.scalars().all()


@router.post("/", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def create_worker(
    payload: WorkerCreate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    worker = Worker(
        plant_id=plant.id,
        name=payload.name,
        employee_id=payload.employee_id,
        pin_hash=pwd_context.hash(payload.pin) if payload.pin else None,
    )
    db.add(worker)
    await db.commit()
    await db.refresh(worker)
    return worker


@router.put("/{worker_id}", response_model=WorkerResponse)
async def update_worker(
    worker_id: uuid.UUID,
    payload: WorkerUpdate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    worker = await db.get(Worker, worker_id)
    if not worker or worker.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    if payload.name is not None:
        worker.name = payload.name
    if payload.employee_id is not None:
        worker.employee_id = payload.employee_id
    if payload.pin is not None:
        worker.pin_hash = pwd_context.hash(payload.pin)
    if payload.is_active is not None:
        worker.is_active = payload.is_active

    await db.commit()
    await db.refresh(worker)
    return worker


@router.post("/verify-pin")
async def verify_worker_pin(
    payload: WorkerPinVerify,
    db: AsyncSession = Depends(get_db),
):
    worker = await db.get(Worker, payload.worker_id)
    if not worker or not worker.pin_hash:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    if not pwd_context.verify(payload.pin, worker.pin_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid PIN")

    return {"verified": True, "worker_id": str(worker.id), "name": worker.name}
