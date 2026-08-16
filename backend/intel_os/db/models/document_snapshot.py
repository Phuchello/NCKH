"""DocumentSnapshot ORM Model (Fetched Representations & Version Artifacts)."""

from datetime import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from intel_os.db.base import Base, GUID, utc_now
from intel_os.db.models.enums import RetentionTier

if TYPE_CHECKING:
    from intel_os.db.models.document import Document
    from intel_os.db.models.document_source import DocumentSource


class DocumentSnapshot(Base):
    """Represents a specific fetched representation / format of a document version."""

    __tablename__ = "document_snapshots"
    __table_args__ = (
        # Snapshot Identity: permits multiple representations (PDF vs HTML) per version,
        # but rejects duplicate identical bytes for the same representation format.
        UniqueConstraint(
            "document_id",
            "version_identifier",
            "mime_type",
            "content_hash",
            name="uq_snapshots_doc_version_mime_hash",
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
    # Provenance Protection: RESTRICT prevents deleting provider source observation while snapshots depend on it
    document_source_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID,
        ForeignKey("document_sources.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    version_identifier: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="v1",  # e.g., 'arxiv_v1', 'arxiv_v2', 'camera_ready'
    )
    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,  # 'application/pdf', 'text/html'
    )
    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,  # SHA-256 of downloaded representation bytes
    )
    byte_size: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
    )
    raw_s3_key: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    retention_tier: Mapped[RetentionTier] = mapped_column(
        Enum(RetentionTier, native_enum=True, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=RetentionTier.INDEXED,
    )
    parser_version: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    extraction_version: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="document_snapshots",
    )
    document_source: Mapped[Optional["DocumentSource"]] = relationship(
        "DocumentSource",
        back_populates="document_snapshots",
    )

    def __repr__(self) -> str:
        return (
            f"<DocumentSnapshot(id={self.id}, doc_id={self.document_id}, "
            f"ver='{self.version_identifier}', mime='{self.mime_type}')>"
        )
