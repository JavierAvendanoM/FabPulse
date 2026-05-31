from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from dependencies import get_kiosk_station, get_current_plant
from models.plant import Plant
from models.station import Station
from models.job import Job
from models.task_log import TaskLog
from schemas.task import TaskCreate, TaskResponse

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_from_kiosk(
    payload: TaskCreate,
    station: Station = Depends(get_kiosk_station),
    db: AsyncSession = Depends(get_db),
):
    job = await db.get(Job, payload.job_id)
    if not job or job.plant_id != station.plant_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    task_log = TaskLog(
        plant_id=station.plant_id,
        job_id=payload.job_id,
        station_id=station.id,
        worker_id=payload.worker_id,
        started_at=payload.started_at,
        completed_at=payload.completed_at,
        notes=payload.notes,
        offline_created=payload.offline_created,
    )
    db.add(task_log)
    await db.commit()
    await db.refresh(task_log)
    return task_log


@router.post("/manual", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_manual(
    payload: TaskCreate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    job = await db.get(Job, payload.job_id)
    if not job or job.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    task_log = TaskLog(
        plant_id=plant.id,
        job_id=payload.job_id,
        worker_id=payload.worker_id,
        started_at=payload.started_at,
        completed_at=payload.completed_at,
        notes=payload.notes,
        offline_created=False,
    )
    db.add(task_log)
    await db.commit()
    await db.refresh(task_log)
    return task_log


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TaskLog)
        .where(TaskLog.plant_id == plant.id)
        .order_by(TaskLog.started_at.desc())
        .limit(500)
    )
    return result.scalars().all()
