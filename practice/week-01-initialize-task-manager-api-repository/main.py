"""Main entrypoint for Task Manager REST API application."""
import sys
from pathlib import Path

# Ensure project root is in Python sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from config.settings import get_settings
from src.main import app, create_app

__all__ = ["app", "create_app"]

if __name__ == "__main__":
    settings = get_settings()
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
