"""Automated tests for service health check endpoints."""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Test GET / returns 200 and expected metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"
    assert data["version"] == "1.0.0"


def test_health_endpoint() -> None:
    """Test GET /health returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"


def test_api_v1_health_endpoint() -> None:
    """Test GET /api/v1/health returns 200 and healthy status."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
