from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routers import health, auth, plants, divisions, stations, workers, jobs, tasks, analytics, simulator, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="FabPulse API",
    version="1.0.0",
    description="Real-time production intelligence for off-site fabrication plants",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fabpulse.io",
        "https://app.fabpulse.io",
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "detail": str(exc.errors()), "code": "VALIDATION_ERROR"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "detail": exc.detail, "code": "HTTP_ERROR"},
    )


app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(plants.router, prefix="/plants", tags=["plants"])
app.include_router(divisions.router, prefix="/divisions", tags=["divisions"])
app.include_router(stations.router, prefix="/stations", tags=["stations"])
app.include_router(workers.router, prefix="/workers", tags=["workers"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(simulator.router, prefix="/simulator", tags=["simulator"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
