"""Tests for Health and Status API Endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Validates /api/v1/health response structure and database status."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_status_endpoint(client: AsyncClient):
    """Validates /api/v1/status response structure and telemetry."""
    response = await client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == "Intel OS / NCKH Intelligence Platform"
    assert data["app_version"] == "0.1.0"
    assert data["environment"] == "testing"
    assert data["embedding_dimension"] == 768
    assert "cache" in data
    assert "current_bytes" in data["cache"]
    assert "max_bytes" in data["cache"]
    assert "usage_ratio" in data["cache"]
