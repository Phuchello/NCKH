"""Pytest Configuration and Shared Test Fixtures."""

import os
from pathlib import Path
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Set testing environment variables before importing app modules
os.environ["APP_ENV"] = "testing"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["LOG_LEVEL"] = "WARNING"
os.environ["MAX_LOCAL_CACHE_GB"] = "1.0"

from intel_os.core.config import Settings, get_settings
from intel_os.db.base import Base
import intel_os.db.models  # Registers all 7 models
from intel_os.db.session import get_db
from intel_os.main import app
from intel_os.storage.local_cache import LocalCacheManager


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Returns application settings configured for test environment."""
    return get_settings()


@pytest.fixture
async def test_engine(tmp_path: Path):
    """Creates an isolated in-memory or SQLite async engine for tests."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    # Enable SQLite foreign key enforcement for tests
    from sqlalchemy import event

    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Yields an isolated async session for database testing."""
    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(test_engine) -> AsyncGenerator[AsyncClient, None]:
    """Yields an HTTP async test client with database dependency override."""
    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def cache_manager(tmp_path: Path) -> LocalCacheManager:
    """Yields an isolated LocalCacheManager with a temporary directory."""
    temp_cache_dir = tmp_path / "cache_test"
    return LocalCacheManager(cache_dir=temp_cache_dir, max_cache_gb=0.001)  # ~1MB budget for testing
