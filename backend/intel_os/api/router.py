"""API V1 Router Assembly."""

from fastapi import APIRouter

from intel_os.api.routes import health, status

api_router = APIRouter()

api_router.include_router(health.router, tags=["system"])
api_router.include_router(status.router, tags=["system"])
