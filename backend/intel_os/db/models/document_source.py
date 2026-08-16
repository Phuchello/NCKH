"""DocumentSource ORM Model (Multi-Provider Discovery Provenance)."""

from datetime import datetime
import uuid
from typing import TYPE_CHECKING, Any, List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from intel_os.core.url import normalize_url
from intel_os.db.base import Base, GUID, utc_now

if TYPE_CHECKING:
    from intel_os.db.models.document import Document
    from intel_os.db.models.document_snapshot import DocumentSnapshot
    from intel_os.db.models.source import Source


class DocumentSource(Base):
    """Represents a discrete provider observation of a document.

    Handles idempotency across both provider-assigned identifiers and normalized web URLs.
    """

    __tablename__ = "document_sources"
    __table_args__ = (
        # Idempotency Rule 1: When provider_doc_id is present, (document_id, source_id, provider_doc_id) is unique
        Index(
            "uq_doc_sources_provider",
            "document_id",
            "source_id",
            "provider_doc_id",
            unique=True,
            postgresql_where=text("provider_doc_id IS NOT NULL"),
            sqlite_where=text("provider_doc_id IS NOT NULL"),
        ),
        # Idempotency Rule 2: When provider_doc_id is NULL, (document_id, source_id, normalized_observed_url) is unique
        Index(
            "uq_doc_sources_url_null_provider",
            "document_id",
            "source_id",
            "normalized_observed_url",
            unique=True,
            postgresql_where=text("provider_doc_id IS NULL"),
            sqlite_where=text("provider_doc_id IS NULL"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider_doc_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    observed_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    normalized_observed_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    observed_metadata: Mapped[dict] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
    )
    match_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="MANUAL",
    )
    match_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
        server_default=text("1.0"),
    )
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )

    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="document_sources",
    )
    source: Mapped["Source"] = relationship(
        "Source",
        back_populates="document_sources",
    )
    document_snapshots: Mapped[List["DocumentSnapshot"]] = relationship(
        "DocumentSnapshot",
        back_populates="document_source",
        passive_deletes=True,
    )

    def __init__(self, **kwargs: Any) -> None:
        if "observed_url" in kwargs and "normalized_observed_url" not in kwargs:
            kwargs["normalized_observed_url"] = normalize_url(kwargs["observed_url"])
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<DocumentSource(id={self.id}, doc_id={self.document_id}, source_id={self.source_id}, provider_id='{self.provider_doc_id}')>"
