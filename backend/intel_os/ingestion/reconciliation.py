"""Centralized Multi-Provider Document Reconciliation Engine.

Enforces strict identity precedence for linking provider observations to logical documents:
  DOI_EXACT -> ARXIV_ID_EXACT -> PROVIDER_DOC_ID -> CANONICAL_URL

Candidate-only signals (metadata fingerprint, title similarity) are NEVER auto-merged,
preventing destructive false merges.
"""

from typing import Optional, Tuple
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.models.document import Document
from intel_os.db.models.document_source import DocumentSource
from intel_os.ingestion.dto import NormalizedDiscoveryRecord


class ReconciliationEngine:
    """Centralized identity resolution engine for academic metadata harvest."""

    @staticmethod
    async def resolve(
        session: AsyncSession,
        record: NormalizedDiscoveryRecord,
        source_id: Optional[uuid.UUID] = None,
    ) -> Tuple[Optional[Document], str, float]:
        """Resolves an incoming discovery record to an existing logical Document.

        Returns:
            Tuple of (Document | None, match_method, match_confidence)
            If no hard identity matches, returns (None, 'NEW_DOCUMENT', 1.0).
        """
        # 1. Hard Match: Exact Normalized DOI
        if record.doi:
            stmt = select(Document).where(Document.doi == record.doi)
            res = await session.execute(stmt)
            doc = res.scalar_one_or_none()
            if doc:
                return doc, "DOI_EXACT", 1.0

        # 2. Hard Match: Exact Normalized Logical arXiv ID
        if record.arxiv_id:
            stmt = select(Document).where(Document.arxiv_id == record.arxiv_id)
            res = await session.execute(stmt)
            doc = res.scalar_one_or_none()
            if doc:
                return doc, "ARXIV_ID_EXACT", 1.0

        # 3. Hard Match: Previously Known Provider ID for this Source
        if source_id and record.provider_document_id:
            stmt = (
                select(Document)
                .join(DocumentSource, DocumentSource.document_id == Document.id)
                .where(
                    DocumentSource.source_id == source_id,
                    DocumentSource.provider_doc_id == record.provider_document_id,
                )
            )
            res = await session.execute(stmt)
            doc = res.scalar_one_or_none()
            if doc:
                return doc, "PROVIDER_DOC_ID", 1.0

        # 4. Hard Match: Exact Canonical URL Match
        if record.canonical_url:
            stmt = select(Document).where(Document.canonical_url == record.canonical_url)
            res = await session.execute(stmt)
            doc = res.scalar_one_or_none()
            if doc:
                return doc, "CANONICAL_URL", 1.0

        # 5. Candidate-Only Evidence: Fingerprint Match
        # Invariant: Fingerprint matches are candidate signals and MUST NOT auto-merge.
        # Create as a separate logical document to protect data integrity.
        return None, "NEW_DOCUMENT", 1.0
