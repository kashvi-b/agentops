from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas import RunRequest, RunResponse, RunStatus


class RunRepository:
    def __init__(self):
        self._runs: dict[UUID, RunResponse] = {}

    def create(self, request: RunRequest) -> RunResponse:
        run = RunResponse(
            run_id=uuid4(),
            task=request.task,
            status=RunStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )
        self._runs[run.run_id] = run
        return run

    def get(self, run_id: UUID) -> RunResponse | None:
        return self._runs.get(run_id)

    def list_all(self) -> list[RunResponse]:
        return list(self._runs.values())
