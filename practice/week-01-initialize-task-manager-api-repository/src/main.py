"""FastAPI application factory and route registration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import get_settings
from src.api.health import router as health_router
from src.api.routes import router as tasks_router


def create_app() -> FastAPI:
    """Initialize and configure the FastAPI application instance."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register Routers
    app.include_router(health_router, prefix="", tags=["Health"])
    app.include_router(health_router, prefix=settings.API_V1_PREFIX, tags=["Health"])
    app.include_router(tasks_router, prefix=settings.API_V1_PREFIX, tags=["Tasks"])

    @app.get("/", tags=["Root"])
    def root() -> dict[str, str]:
        """Root welcome endpoint with API documentation links."""
        return {
            "message": "Welcome to the Task Manager REST API",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_V1_PREFIX}/health",
        }

    return app


app = create_app()
