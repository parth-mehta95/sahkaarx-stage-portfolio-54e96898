"""Application configuration settings."""
import os
from typing import List, Optional
from pydantic import BaseModel


class Settings(BaseModel):
    """Application configuration settings loaded from environment or defaults."""

    APP_NAME: str = "Task Manager REST API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A production-ready Task Manager REST API built with FastAPI, "
        "featuring validated Pydantic schemas, modular layering, and comprehensive tests."
    )
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    ALLOWED_ORIGINS: List[str] = ["*"]


_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """Retrieve or initialize the cached application settings instance."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
