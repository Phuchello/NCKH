"""Database Engine and Async Session Management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from intel_os.core.config import get_settings

logger = logging.getLogger(__name__)

# Global engine and sessionmaker instances
_engine: Optional[AsyncEngine] = None
_async_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_engine() -> AsyncEngine:
    """Returns or creates the shared async SQLAlchemy engine."""
    global _engine
    if _engine is None:
        settings = get_settings()
        is_sqlite = settings.DATABASE_URL.startswith("sqlite")

        engine_kwargs = {
            "echo": settings.DATABASE_ECHO,
        }

        # PostgreSQL-specific pool tuning
        if not is_sqlite:
            engine_kwargs.update(
                {
                    "pool_size": settings.DATABASE_POOL_SIZE,
                    "max_overflow": settings.DATABASE_MAX_OVERFLOW,
                    "pool_timeout": settings.DATABASE_POOL_TIMEOUT,
                    "pool_recycle": settings.DATABASE_POOL_RECYCLE,
                    "pool_pre_ping": True,
                }
            )

        _engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)
        logger.info("Initialized async database engine for %s", settings.DATABASE_URL.split("@")[-1])
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Returns or creates the async session factory."""
    global _async_session_factory
    if _async_session_factory is None:
        engine = get_engine()
        _async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
    return _async_session_factory


async def close_db() -> None:
    """Closes and disposes of the database engine."""
    global _engine, _async_session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_factory = None
        logger.info("Disposed async database engine.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session with transaction management."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """Async context manager for background jobs and tasks."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_connectivity() -> bool:
    """Performs a lightweight connectivity check against the database."""
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.warning("Database health check failed: %s", exc)
        return False
