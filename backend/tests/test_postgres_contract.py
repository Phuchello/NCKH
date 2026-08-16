"""PostgreSQL 16 Schema Contract and Database Introspection Tests."""

from pathlib import Path
import pytest
from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncEngine

from tests.conftest import assert_safe_test_db

G1_TABLES = {
    "topics",
    "sources",
    "documents",
    "document_topics",
    "document_sources",
    "document_snapshots",
    "background_jobs",
}


@pytest.mark.asyncio
async def test_postgres_table_inventory_and_extensions(postgres_engine: AsyncEngine):
    """CONTRACT: Real PostgreSQL 16 contains exactly 7 application tables + alembic_version and required extensions."""
    async with postgres_engine.connect() as conn:
        # Check tables
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        app_tables = set(tables) - {"alembic_version"}
        assert app_tables == G1_TABLES
        assert "alembic_version" in tables

        # Check installed extensions (only vector and plpgsql are required)
        res = await conn.execute(text("SELECT extname FROM pg_extension;"))
        extensions = {row[0] for row in res.fetchall()}
        assert "vector" in extensions
        assert "plpgsql" in extensions


@pytest.mark.asyncio
async def test_postgres_enum_types_and_values(postgres_engine: AsyncEngine):
    """CONTRACT: PostgreSQL contains retention_tier and job_status with exact enum values."""
    async with postgres_engine.connect() as conn:
        res = await conn.execute(
            text(
                """
                SELECT t.typname, e.enumlabel
                FROM pg_type t
                JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE t.typname IN ('retention_tier', 'job_status')
                ORDER BY t.typname, e.enumsortorder;
                """
            )
        )
        rows = res.fetchall()
        enums_by_type = {}
        for typname, label in rows:
            enums_by_type.setdefault(typname, []).append(label)

        assert "retention_tier" in enums_by_type
        assert enums_by_type["retention_tier"] == [
            "DISCOVERED",
            "INDEXED",
            "RELEVANT",
            "RETAINED",
            "ARCHIVED",
        ]

        assert "job_status" in enums_by_type
        assert enums_by_type["job_status"] == [
            "PENDING",
            "RUNNING",
            "COMPLETED",
            "FAILED",
            "RETRYING",
        ]


@pytest.mark.asyncio
async def test_postgres_column_data_types(postgres_engine: AsyncEngine):
    """CONTRACT: Important column data types on PostgreSQL match the exact authoritative schema."""
    async with postgres_engine.connect() as conn:
        # Check topics.keywords and documents.authors are PostgreSQL text[] arrays
        res = await conn.execute(
            text(
                """
                SELECT table_name, column_name, udt_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND (
                    (table_name = 'topics' AND column_name IN ('id', 'keywords'))
                    OR (table_name = 'documents' AND column_name IN ('id', 'authors', 'metadata', 'retention_tier'))
                    OR (table_name = 'document_sources' AND column_name IN ('observed_url', 'normalized_observed_url', 'observed_metadata'))
                    OR (table_name = 'document_snapshots' AND column_name IN ('byte_size', 'retention_tier'))
                    OR (table_name = 'background_jobs' AND column_name IN ('idempotency_key', 'payload', 'status'))
                  );
                """
            )
        )
        cols = {(r[0], r[1]): (r[2], r[3]) for r in res.fetchall()}

        # Verify PostgreSQL native ARRAY types
        assert cols[("topics", "keywords")][0] in ("_varchar", "_text", "ARRAY")
        assert cols[("documents", "authors")][0] in ("_varchar", "_text", "ARRAY")

        # Verify JSONB types
        assert cols[("documents", "metadata")][0] == "jsonb"
        assert cols[("document_sources", "observed_metadata")][0] == "jsonb"
        assert cols[("background_jobs", "payload")][0] == "jsonb"

        # Verify UUID primary keys
        assert cols[("topics", "id")][0] == "uuid"
        assert cols[("documents", "id")][0] == "uuid"

        # Verify BIGINT
        assert cols[("document_snapshots", "byte_size")][0] == "int8"

        # Verify normalized_observed_url exists
        assert ("document_sources", "normalized_observed_url") in cols


def test_postgres_alembic_lifecycle(postgres_url: str):
    """CONTRACT: Real PostgreSQL 16 full upgrade -> downgrade -> upgrade cycle succeeds without enum leaks."""
    from alembic import command
    from alembic.config import Config

    assert_safe_test_db(postgres_url)

    alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)

    # 1. Downgrade to base (drops all tables and custom enums)
    command.downgrade(alembic_cfg, "base")

    # 2. Upgrade back to head (re-creates extensions, enums, tables, and partial indexes)
    command.upgrade(alembic_cfg, "head")

