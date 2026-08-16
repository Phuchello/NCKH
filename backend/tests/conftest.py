"""Pytest Configuration and Shared Test Fixtures."""

import os
from pathlib import Path
from typing import AsyncGenerator
from urllib.parse import urlparse

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

# Set testing environment variables before importing app modules
os.environ["APP_ENV"] = "testing"
os.environ["LOG_LEVEL"] = "WARNING"
os.environ["MAX_LOCAL_CACHE_GB"] = "1.0"
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from intel_os.core.config import Settings, get_settings
from intel_os.db.base import Base
import intel_os.db.models  # Registers all 7 models
from intel_os.db.session import get_db
from intel_os.main import app
from intel_os.storage.local_cache import LocalCacheManager

POSTGRES_TEST_URL = os.getenv(
    "POSTGRES_TEST_URL",
    "postgresql+asyncpg://postgres:postgrespassword@localhost:5432/intel_os_test",
)


def assert_safe_test_db(db_url: str) -> None:
    """CRITICAL SAFETY GUARD: Refuses execution if target database is not a local test instance."""
    parsed = urlparse(db_url)
    hostname = parsed.hostname or ""
    path = parsed.path.lstrip("/")

    is_local = hostname in ("localhost", "127.0.0.1", "::1", "")
    is_test_named = "test" in path.lower()

    if not (is_local and is_test_named):
        raise RuntimeError(
            f"SAFETY VIOLATION: Refusing to run destructive tests against non-test database: {db_url} "
            f"(Must be local host and contain 'test' in DB name)"
        )


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Returns application settings configured for test environment."""
    return get_settings()


@pytest.fixture
async def test_engine(tmp_path: Path):
    """Creates an isolated in-memory SQLite async engine for fast unit tests."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

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
    """Yields an isolated async session for SQLite unit testing."""
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
    return LocalCacheManager(cache_dir=temp_cache_dir, max_cache_gb=0.001)


# =============================================================================
# PostgreSQL 16 Integration Test Fixtures
# =============================================================================


@pytest.fixture(scope="session")
def postgres_url() -> str:
    """Returns verified safe PostgreSQL test URL."""
    assert_safe_test_db(POSTGRES_TEST_URL)
    return POSTGRES_TEST_URL


@pytest.fixture
async def postgres_engine(postgres_url: str) -> AsyncGenerator[AsyncEngine, None]:
    """Yields an async engine connected to real PostgreSQL 16 test database."""
    assert_safe_test_db(postgres_url)
    engine = create_async_engine(postgres_url, echo=False)

    yield engine

    await engine.dispose()


@pytest.fixture
async def pg_session(postgres_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Yields an async session connected to real PostgreSQL 16 with automatic rollback."""
    session_factory = async_sessionmaker(
        bind=postgres_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with session_factory() as session:
        yield session
        await session.rollback()
