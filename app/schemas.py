from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task: str = Field(
        min_length=3,
        max_length=5000,
        description="Task the AI agent should perform",
    )


class RunResponse(BaseModel):
    run_id: UUID
    task: str
    status: RunStatus
    created_at: datetime
    result: str | None = None


class HealthResponse(BaseModel):
    status: str
    version: str
