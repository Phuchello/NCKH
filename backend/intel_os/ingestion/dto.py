"""Normalized Discovery Record Data Transfer Object (DTO).

Provides a typed, provider-neutral model representing a discovered academic paper
across all scholarly connector feeds.
"""

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from intel_os.db.base import utc_now


class NormalizedDiscoveryRecord(BaseModel):
    """Provider-neutral scholarly metadata record produced by connectors."""

    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True)

    provider: str = Field(
        ...,
        description="Source provider identifier ('arxiv', 'crossref', 'openalex', 'semantic_scholar')",
    )
    provider_document_id: Optional[str] = Field(
        default=None,
        description="Provider-specific primary document ID (e.g. arXiv ID, OpenAlex work ID, S2 paperId)",
    )
    title: str = Field(
        ...,
        description="Cleaned title of the scientific work",
    )
    authors: list[str] = Field(
        default_factory=list,
        description="Ordered list of author full names",
    )
    doi: Optional[str] = Field(
        default=None,
        description="Normalized Digital Object Identifier (e.g. '10.1145/1234567.89')",
    )
    arxiv_id: Optional[str] = Field(
        default=None,
        description="Normalized logical arXiv identifier without version suffix (e.g. '2301.12345')",
    )
    canonical_url: str = Field(
        ...,
        description="Authoritative/publisher landing page URL",
    )
    observed_url: str = Field(
        ...,
        description="Verbatim provider URL observed during harvest",
    )
    publication_date: Optional[date] = Field(
        default=None,
        description="Exact publication date if available",
    )
    publication_year: Optional[int] = Field(
        default=None,
        description="Publication calendar year",
    )
    venue: Optional[str] = Field(
        default=None,
        description="Journal, conference, or repository venue name",
    )
    abstract: Optional[str] = Field(
        default=None,
        description="Full text abstract if provided by harvest feed",
    )
    external_ids: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of auxiliary identifiers (e.g. {'mag': '123', 'corpusId': '456'})",
    )
    provider_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Verbatim provider JSON payload preserved for full provenance",
    )
    observed_at: datetime = Field(
        default_factory=utc_now,
        description="Timestamp when observation was captured",
    )
