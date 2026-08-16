"""Health Check Endpoint."""

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from intel_os.db.session import check_db_connectivity

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check status response payload."""

    status: Literal["healthy", "degraded"]
    database: Literal["connected", "disconnected"]
    timestamp: datetime


@router.get("/health", response_model=HealthResponse, summary="Service Health & DB Connectivity Check")
async def get_health(response: Response) -> HealthResponse:
    """Returns application liveness and database connectivity status."""
    db_connected = await check_db_connectivity()

    if not db_connected:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(
            status="degraded",
            database="disconnected",
            timestamp=datetime.now(timezone.utc),
        )

    return HealthResponse(
        status="healthy",
        database="connected",
        timestamp=datetime.now(timezone.utc),
    )
