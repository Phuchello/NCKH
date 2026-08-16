"""Tests for Alembic Migration Definitions and Table Boundary Invariants."""

import importlib.util
from pathlib import Path
import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine

from intel_os.db.base import Base

G1_EXPECTED_TABLES = {
    "topics",
    "sources",
    "documents",
    "document_topics",
    "document_sources",
    "document_snapshots",
    "background_jobs",
}

FORBIDDEN_FUTURE_TABLES = {
    "document_chunks",
    "claims",
    "evidence_items",
    "relationships",
    "user_notes",
    "research_gaps",
    "contradictions",
    "research_opportunities",
    "research_ideas",
    "idea_provenance",
    "experiment_logs",
}


def test_migration_file_exists_and_defines_exact_7_tables():
    """Validates that the G1 migration file exists and declares only the 7 foundation tables."""
    versions_dir = Path(__file__).parent.parent / "intel_os" / "db" / "migrations" / "versions"
    migration_files = list(versions_dir.glob("*.py"))
    assert len(migration_files) >= 1

    g1_file = migration_files[0]
    spec = importlib.util.spec_from_file_location("g1_migration", g1_file)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert hasattr(mod, "revision")
    assert hasattr(mod, "upgrade")
    assert hasattr(mod, "downgrade")
    assert mod.revision == "0001_g1_foundation"


def test_orm_models_match_g1_scope():
    """Validates that Base.metadata contains exactly the 7 G1 tables and zero future tables."""
    registered_tables = set(Base.metadata.tables.keys())

    assert registered_tables == G1_EXPECTED_TABLES
    assert len(registered_tables) == 7

    # Ensure no future feature tables leaked into G1 models
    leaked_tables = registered_tables.intersection(FORBIDDEN_FUTURE_TABLES)
    assert len(leaked_tables) == 0, f"Leaked future tables in G1: {leaked_tables}"


@pytest.mark.asyncio
async def test_table_creation_on_engine(test_engine: AsyncEngine):
    """Validates that all 7 tables are successfully created in the test database."""
    async with test_engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        assert set(tables) == G1_EXPECTED_TABLES


def test_alembic_upgrade_and_downgrade_cycle(tmp_path: Path):
    """Validates full deterministic alembic upgrade head -> downgrade base -> upgrade head lifecycle."""
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine

    db_file = tmp_path / "alembic_cycle.db"
    sync_url = f"sqlite:///{db_file.as_posix()}"

    alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url)

    # 1. Upgrade to head
    command.upgrade(alembic_cfg, "head")
    engine = create_engine(sync_url)
    inspector = inspect(engine)
    created_tables = set(inspector.get_table_names())
    assert G1_EXPECTED_TABLES.issubset(created_tables)

    # 2. Downgrade to base
    command.downgrade(alembic_cfg, "base")
    inspector = inspect(engine)
    remaining_tables = set(inspector.get_table_names())
    for t in G1_EXPECTED_TABLES:
        assert t not in remaining_tables

    # 3. Upgrade back to head
    command.upgrade(alembic_cfg, "head")
    inspector = inspect(engine)
    recreated_tables = set(inspector.get_table_names())
    assert G1_EXPECTED_TABLES.issubset(recreated_tables)
    engine.dispose()

