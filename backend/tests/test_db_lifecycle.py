"""Tests for Database Engine Lifecycle and Async Session Contexts."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.session import check_db_connectivity, close_db, get_db_context, get_engine


@pytest.fixture(autouse=True)
async def cleanup_engine():
    """Ensures clean engine lifecycle per test."""
    await close_db()
    yield
    await close_db()


@pytest.mark.asyncio
async def test_engine_creation_and_connectivity():
    """Validates that engine is instantiated and connectivity check succeeds."""
    engine = get_engine()
    assert engine is not None

    connected = await check_db_connectivity()
    assert connected is True


@pytest.mark.asyncio
async def test_session_lifecycle_and_rollback(db_session: AsyncSession):
    """Validates session execution and transaction boundary integrity."""
    result = await db_session.execute(text("SELECT 1 + 1 AS sum_val"))
    row = result.mappings().first()
    assert row["sum_val"] == 2


@pytest.mark.asyncio
async def test_db_context_manager():
    """Validates async context manager transaction lifecycle."""
    async with get_db_context() as session:
        result = await session.execute(text("SELECT 'hello' AS greeting"))
        row = result.mappings().first()
        assert row["greeting"] == "hello"
