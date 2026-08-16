"""Intel OS Core Configuration Module.

Provides strongly typed application settings loaded from environment variables
or .env files with safe development defaults.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation and safe defaults."""

    # Application metadata
    APP_NAME: str = "Intel OS / NCKH Intelligence Platform"
    APP_ENV: Literal["development", "testing", "production"] = "development"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API configuration
    API_V1_STR: str = "/api/v1"

    # Database configuration
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/intel_os",
        description="Async PostgreSQL connection URI",
    )
    DATABASE_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DATABASE_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    DATABASE_POOL_TIMEOUT: float = Field(default=30.0, ge=1.0)
    DATABASE_POOL_RECYCLE: int = Field(default=1800, ge=60)
    DATABASE_ECHO: bool = False

    # Local Cache Configuration (Bounded laptop storage)
    MAX_LOCAL_CACHE_GB: float = Field(
        default=10.0,
        ge=0.1,
        description="Maximum local storage cache budget in gigabytes",
    )
    LOCAL_TEMP_DIR: Path = Field(
        default=Path("./cache/temp"),
        description="Local root directory for transient buffers and caches",
    )

    # Embedding Contract (V1)
    EMBEDDING_DIMENSION: int = Field(
        default=768,
        description="Strict vector dimension for V1 schema",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure DATABASE_URL is non-empty and has proper async dialect for asyncpg."""
        if not v:
            raise ValueError("DATABASE_URL cannot be empty")
        # Automatically adjust postgresql:// to postgresql+asyncpg:// if standard postgresql uri passed
        if v.startswith("postgresql://") and not v.startswith("postgresql+asyncpg://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    @property
    def max_cache_bytes(self) -> int:
        """Returns max cache budget in bytes."""
        return int(self.MAX_LOCAL_CACHE_GB * 1024 * 1024 * 1024)

    @property
    def is_testing(self) -> bool:
        """Returns True if running in testing environment."""
        return self.APP_ENV == "testing"


@lru_cache
def get_settings() -> Settings:
    """Cached singleton for application settings."""
    return Settings()
