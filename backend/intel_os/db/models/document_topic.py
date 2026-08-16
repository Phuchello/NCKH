"""DocumentTopic ORM Model (M:N Document <-> Topic)."""

from datetime import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from intel_os.db.base import Base, GUID, utc_now

if TYPE_CHECKING:
    from intel_os.db.models.document import Document
    from intel_os.db.models.topic import Topic


class DocumentTopic(Base):
    """Many-to-many junction linking Documents to Topics."""

    __tablename__ = "document_topics"
    __table_args__ = (
        UniqueConstraint("document_id", "topic_id", name="uq_document_topics_doc_topic"),
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
    topic_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    relevance_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )
    assignment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="MANUAL",  # 'KEYWORD_MATCH', 'SEMANTIC_SIMILARITY', 'MANUAL', 'CLASSIFIER'
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    # Relationships
    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="document_topics",
    )
    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="document_topics",
    )

    def __repr__(self) -> str:
        return f"<DocumentTopic(document_id={self.document_id}, topic_id={self.topic_id})>"
