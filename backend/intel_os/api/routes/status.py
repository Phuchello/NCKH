"""Application Telemetry & Status Endpoint."""

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from intel_os.core.config import get_settings
from intel_os.storage.local_cache import LocalCacheManager

router = APIRouter()


class CacheStatus(BaseModel):
    """Cache usage metrics."""

    current_bytes: int
    max_bytes: int
    usage_ratio: float
    file_count: int
    is_over_budget: bool


class StatusResponse(BaseModel):
    """System status and environment telemetry."""

    app_name: str
    app_version: str
    environment: str
    embedding_dimension: int
    cache: CacheStatus
    timestamp: datetime


@router.get("/status", response_model=StatusResponse, summary="System Status & Telemetry")
async def get_status() -> StatusResponse:
    """Returns platform version, active environment, and bounded cache utilization."""
    settings = get_settings()
    cache_mgr = LocalCacheManager()
    usage = cache_mgr.get_usage()

    return StatusResponse(
        app_name=settings.APP_NAME,
        app_version=settings.APP_VERSION,
        environment=settings.APP_ENV,
        embedding_dimension=settings.EMBEDDING_DIMENSION,
        cache=CacheStatus(
            current_bytes=usage.current_bytes,
            max_bytes=usage.max_bytes,
            usage_ratio=round(usage.usage_ratio, 4),
            file_count=usage.file_count,
            is_over_budget=usage.is_over_budget,
        ),
        timestamp=datetime.now(timezone.utc),
    )
