from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from app.repository import RunRepository
from app.schemas import (
    HealthResponse,
    RunRequest,
    RunResponse,
)

app = FastAPI(
    title="AgentOps API",
    description="Reliable AI agent execution and evaluation platform",
    version="0.2.0",
)

repository = RunRepository()


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        version=app.version,
    )


@app.post(
    "/runs",
    response_model=RunResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_run(request: RunRequest):
    return repository.create(request)


@app.get("/runs", response_model=list[RunResponse])
def list_runs():
    return repository.list_all()


@app.get("/runs/{run_id}", response_model=RunResponse)
def get_run(run_id: UUID):
    run = repository.get(run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found",
        )

    return run
