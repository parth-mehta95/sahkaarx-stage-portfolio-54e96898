"""Health check and status API endpoints."""
from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Payload schema for health check responses."""
    status: str
    timestamp: datetime
    version: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service Health Check",
    description="Returns the current operational status, API version, and timestamp.",
)
def get_health() -> HealthResponse:
    """Return 200 OK if service is running properly."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
    )
