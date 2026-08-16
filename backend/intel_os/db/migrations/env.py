"""Alembic environment configuration supporting both sync and async engines."""

import asyncio
from logging.config import fileConfig
import os
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parents[3]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from intel_os.core.config import get_settings
from intel_os.db.base import Base
import intel_os.db.models  # Ensure all 7 models are registered

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support
target_metadata = Base.metadata

# Resolve effective database URL
configured_url = config.get_main_option("sqlalchemy.url")
if not configured_url:
    settings = get_settings()
    configured_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    config.set_main_option("sqlalchemy.url", configured_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Configures migration context and runs pending migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(db_url: str) -> None:
    """Runs migrations using asyncpg / aiosqlite connection."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = db_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (handles sync and async dialects)."""
    db_url = config.get_main_option("sqlalchemy.url") or ""

    if "+asyncpg" in db_url or "+aiosqlite" in db_url:
        asyncio.run(run_async_migrations(db_url))
    else:
        configuration = config.get_section(config.config_ini_section) or {}
        configuration["sqlalchemy.url"] = db_url
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            do_run_migrations(connection)

        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
