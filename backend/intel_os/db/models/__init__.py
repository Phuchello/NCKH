"""Intel OS Database Models Package."""

from intel_os.db.base import Base
from intel_os.db.models.background_job import BackgroundJob
from intel_os.db.models.document import Document
from intel_os.db.models.document_snapshot import DocumentSnapshot
from intel_os.db.models.document_source import DocumentSource
from intel_os.db.models.document_topic import DocumentTopic
from intel_os.db.models.enums import (
    ClaimType,
    EpistemicStatus,
    GroundingStatus,
    IdeaStatus,
    JobStatus,
    RetentionTier,
)
from intel_os.db.models.source import Source
from intel_os.db.models.topic import Topic

__all__ = [
    "Base",
    # Enums
    "RetentionTier",
    "GroundingStatus",
    "ClaimType",
    "EpistemicStatus",
    "IdeaStatus",
    "JobStatus",
    # G1 Foundation Models (7 Tables)
    "Topic",
    "Source",
    "Document",
    "DocumentTopic",
    "DocumentSource",
    "DocumentSnapshot",
    "BackgroundJob",
]
