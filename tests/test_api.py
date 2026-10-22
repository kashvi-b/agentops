from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api import app, repository


@pytest.fixture(autouse=True)
def reset_repository():
    repository._runs.clear()
    yield
    repository._runs.clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["version"] == "0.2.0"


def test_create_run(client):
    response = client.post(
        "/runs",
        json={"task": "Calculate 125 * 48"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["task"] == "Calculate 125 * 48"
    assert data["run_id"]


def test_get_run(client):
    created = client.post(
        "/runs",
        json={"task": "Analyze sales data"},
    ).json()

    response = client.get(f"/runs/{created['run_id']}")

    assert response.status_code == 200
    assert response.json()["run_id"] == created["run_id"]


def test_list_runs(client):
    client.post("/runs", json={"task": "First task"})
    client.post("/runs", json={"task": "Second task"})

    response = client.get("/runs")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_reject_short_task(client):
    response = client.post("/runs", json={"task": "Hi"})

    assert response.status_code == 422


def test_reject_missing_task(client):
    response = client.post("/runs", json={})

    assert response.status_code == 422


def test_reject_unknown_fields(client):
    response = client.post(
        "/runs",
        json={"task": "Valid task", "unexpected": True},
    )

    assert response.status_code == 422


def test_unknown_run(client):
    response = client.get(f"/runs/{uuid4()}")

    assert response.status_code == 404


def test_invalid_run_id(client):
    response = client.get("/runs/not-a-uuid")

    assert response.status_code == 422
