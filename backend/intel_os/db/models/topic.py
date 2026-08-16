"""Topic ORM Model."""

from datetime import datetime
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ARRAY, Boolean, DateTime, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from intel_os.db.base import Base, GUID, utc_now

if TYPE_CHECKING:
    from intel_os.db.models.document_topic import DocumentTopic


class Topic(Base):
    """Represents a research domain or topic (e.g. Edge AI, Speculative Decoding)."""

    __tablename__ = "topics"

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
    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    keywords: Mapped[list[str]] = mapped_column(
        ARRAY(String).with_variant(JSON, "sqlite"),
        nullable=False,
        default=list,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
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
        back_populates="topic",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Topic(id={self.id}, name='{self.name}', slug='{self.slug}')>"
