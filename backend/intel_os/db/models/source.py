"""Source ORM Model."""

from datetime import datetime
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from intel_os.db.base import Base, GUID, utc_now

if TYPE_CHECKING:
    from intel_os.db.models.document_source import DocumentSource


class Source(Base):
    """Represents a globally reusable ingestion feed or provider (arXiv, Crossref, etc.)."""

    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # e.g., 'ARXIV', 'CROSSREF', 'SEMANTIC_SCHOLAR', 'OPENALEX', 'WEB'
    base_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    feed_url: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    config: Mapped[dict] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    last_crawled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    # Relationships
    document_sources: Mapped[List["DocumentSource"]] = relationship(
        "DocumentSource",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Source(id={self.id}, name='{self.name}', type='{self.source_type}')>"
