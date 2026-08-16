"""Intel OS Main Application Entry Point."""

from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from intel_os.api.router import api_router
from intel_os.core.config import get_settings
from intel_os.core.logging import setup_logging
from intel_os.db.session import close_db, get_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and graceful shutdown lifecycle."""
    settings = get_settings()
    setup_logging(settings.LOG_LEVEL)
    logger.info("Starting %s (%s) in %s mode...", settings.APP_NAME, settings.APP_VERSION, settings.APP_ENV)

    # Initialize async database engine
    get_engine()

    yield

    # Clean shutdown
    logger.info("Shutting down %s...", settings.APP_NAME)
    await close_db()
    logger.info("Shutdown complete.")


def create_app() -> FastAPI:
    """Factory function for FastAPI application instance."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Backend platform core for Intel OS / NCKH Intelligence Platform",
        lifespan=lifespan,
        docs_url="/docs" if settings.APP_ENV != "production" else None,
        redoc_url="/redoc" if settings.APP_ENV != "production" else None,
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.APP_ENV == "development" else [],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()
