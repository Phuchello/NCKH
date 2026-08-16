"""Tests for Settings and Configuration Module."""

from pathlib import Path
import pytest
from pydantic import ValidationError

from intel_os.core.config import Settings


def test_default_settings():
    """Validates default settings values and properties."""
    settings = Settings(
        DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/intel_os",
        MAX_LOCAL_CACHE_GB=10.0,
    )
    assert settings.APP_NAME == "Intel OS / NCKH Intelligence Platform"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.MAX_LOCAL_CACHE_GB == 10.0
    assert settings.EMBEDDING_DIMENSION == 768
    assert settings.max_cache_bytes == 10 * 1024 * 1024 * 1024


def test_database_url_validation():
    """Validates automatic postgresql+asyncpg prefix adjustment."""
    settings = Settings(DATABASE_URL="postgresql://user:pass@localhost:5432/mydb")
    assert settings.DATABASE_URL.startswith("postgresql+asyncpg://")

    with pytest.raises(ValidationError):
        Settings(DATABASE_URL="")


def test_custom_settings():
    """Validates custom environment variable overrides."""
    settings = Settings(
        APP_ENV="testing",
        LOG_LEVEL="DEBUG",
        MAX_LOCAL_CACHE_GB=5.0,
        LOCAL_TEMP_DIR=Path("/tmp/intel_os_cache"),
        DATABASE_URL="postgresql+asyncpg://user:secret@db.local:5432/intel_db",
    )
    assert settings.is_testing is True
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.MAX_LOCAL_CACHE_GB == 5.0
    assert settings.max_cache_bytes == 5 * 1024 * 1024 * 1024
    assert settings.LOCAL_TEMP_DIR.as_posix() == "/tmp/intel_os_cache"
