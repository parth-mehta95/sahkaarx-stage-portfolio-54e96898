"""Automated tests for Task CRUD endpoints and validation."""
import pytest
from fastapi.testclient import TestClient

from main import app
from src.services.task_service import get_task_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_service() -> None:
    """Reset the in-memory task service before each test."""
    service = get_task_service()
    service.clear()


def test_create_task_success() -> None:
    """Test successful task creation with 201 status code."""
    payload = {
        "title": "Setup PostgreSQL Database",
        "description": "Configure connection string and initial migrations",
        "status": "Pending",
    }
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == "Pending"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_default_values() -> None:
    """Test creating task with only required fields uses default status and empty description."""
    payload = {"title": "Minimal Task"}
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["description"] == ""
    assert data["status"] == "Pending"


def test_create_task_validation_error_empty_title() -> None:
    """Test that empty title triggers 422 Unprocessable Entity."""
    response = client.post("/api/v1/tasks", json={"title": ""})
    assert response.status_code == 422


def test_create_task_validation_error_invalid_status() -> None:
    """Test that invalid status string triggers 422 Unprocessable Entity."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test", "status": "Archived"},
    )
    assert response.status_code == 422


def test_get_task_by_id_success() -> None:
    """Test retrieving an existing task by its ID."""
    created = client.post("/api/v1/tasks", json={"title": "Find Me"}).json()
    task_id = created["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


def test_get_task_not_found() -> None:
    """Test retrieving a non-existent task returns 404."""
    response = client.get("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with ID 999 not found"


def test_list_tasks() -> None:
    """Test listing multiple tasks."""
    client.post("/api/v1/tasks", json={"title": "Task 1"})
    client.post("/api/v1/tasks", json={"title": "Task 2"})

    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"


def test_list_tasks_filtered_by_status() -> None:
    """Test filtering tasks by status."""
    client.post("/api/v1/tasks", json={"title": "T1", "status": "Pending"})
    client.post("/api/v1/tasks", json={"title": "T2", "status": "Completed"})
    client.post("/api/v1/tasks", json={"title": "T3", "status": "Pending"})

    res_pending = client.get("/api/v1/tasks?status=Pending")
    assert res_pending.status_code == 200
    assert len(res_pending.json()) == 2

    res_completed = client.get("/api/v1/tasks?status=Completed")
    assert res_completed.status_code == 200
    assert len(res_completed.json()) == 1
    assert res_completed.json()[0]["title"] == "T2"


def test_list_tasks_search() -> None:
    """Test searching tasks by title or description keyword."""
    client.post("/api/v1/tasks", json={"title": "Design REST Schema", "description": "Draft OpenAPI spec"})
    client.post("/api/v1/tasks", json={"title": "Write unit tests", "description": "Cover all endpoints"})

    response = client.get("/api/v1/tasks?search=REST")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "Design REST Schema"


def test_update_task_success() -> None:
    """Test partial and full update of task fields."""
    created = client.post("/api/v1/tasks", json={"title": "Initial Title"}).json()
    task_id = created["id"]

    update_payload = {
        "title": "Updated Title",
        "description": "Now has a description",
        "status": "In Progress",
    }
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Now has a description"
    assert data["status"] == "In Progress"
    assert data["updated_at"] >= created["updated_at"]


def test_update_task_not_found() -> None:
    """Test updating a non-existent task returns 404."""
    response = client.put(
        "/api/v1/tasks/999",
        json={"title": "Updated"},
    )
    assert response.status_code == 404


def test_delete_task_success() -> None:
    """Test deleting an existing task returns 204 No Content."""
    created = client.post("/api/v1/tasks", json={"title": "To Delete"}).json()
    task_id = created["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204

    # Verify task is actually gone
    fetch = client.get(f"/api/v1/tasks/{task_id}")
    assert fetch.status_code == 404


def test_delete_task_not_found() -> None:
    """Test deleting a non-existent task returns 404."""
    response = client.delete("/api/v1/tasks/999")
    assert response.status_code == 404
