"""Document ORM Model."""

from datetime import date, datetime
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ARRAY, Date, DateTime, Enum, Float, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from intel_os.db.base import Base, GUID, utc_now
from intel_os.db.models.enums import RetentionTier

if TYPE_CHECKING:
    from intel_os.db.models.document_snapshot import DocumentSnapshot
    from intel_os.db.models.document_source import DocumentSource
    from intel_os.db.models.document_topic import DocumentTopic


class Document(Base):
    """Represents a logical scientific work or paper."""

    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    doi: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )
    arxiv_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
        index=True,
    )
    canonical_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    metadata_fingerprint: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    authors: Mapped[list[str]] = mapped_column(
        ARRAY(String).with_variant(JSON, "sqlite"),
        nullable=False,
        default=list,
    )
    publication_venue: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    publication_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    abstract: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    retention_tier: Mapped[RetentionTier] = mapped_column(
        Enum(
            RetentionTier,
            name="retention_tier",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=RetentionTier.DISCOVERED,
        index=True,
    )
    relevance_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
        server_default=text("0.0"),
    )
    credibility_prior: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
        server_default=text("0.0"),
    )
    doc_metadata: Mapped[dict] = mapped_column(
        "metadata",
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )

    # Relationships
    document_topics: Mapped[List["DocumentTopic"]] = relationship(
        "DocumentTopic",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    document_sources: Mapped[List["DocumentSource"]] = relationship(
        "DocumentSource",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    document_snapshots: Mapped[List["DocumentSnapshot"]] = relationship(
        "DocumentSnapshot",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, title='{self.title[:40]}...', tier={self.retention_tier.value})>"
