import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from dependencies import get_current_plant
from models.plant import Plant
from models.job import Job
from schemas.job import JobCreate, JobUpdate, JobStatusUpdate, JobResponse

router = APIRouter()


@router.get("/", response_model=list[JobResponse])
async def list_jobs(
    job_status: Optional[str] = Query(None, alias="status"),
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    query = select(Job).where(Job.plant_id == plant.id)
    if job_status:
        query = query.where(Job.status == job_status)
    query = query.order_by(Job.priority.desc(), Job.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: JobCreate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    job = Job(
        plant_id=plant.id,
        **payload.model_dump(),
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: uuid.UUID,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    job = await db.get(Job, job_id)
    if not job or job.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: uuid.UUID,
    payload: JobUpdate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    job = await db.get(Job, job_id)
    if not job or job.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, value)

    await db.commit()
    await db.refresh(job)
    return job


@router.patch("/{job_id}/status", response_model=JobResponse)
async def update_job_status(
    job_id: uuid.UUID,
    payload: JobStatusUpdate,
    plant: Plant = Depends(get_current_plant),
    db: AsyncSession = Depends(get_db),
):
    job = await db.get(Job, job_id)
    if not job or job.plant_id != plant.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    job.status = payload.status
    if payload.status == "in_progress" and not job.started_at:
        job.started_at = datetime.now(timezone.utc)
    if payload.status == "completed" and not job.completed_at:
        job.completed_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(job)
    return job
