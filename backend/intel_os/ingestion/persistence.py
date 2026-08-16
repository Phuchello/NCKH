"""Database Persistence for Discovered Academic Metadata.

Handles transactional document creation/enrichment, topic mapping,
and idempotent multi-provider observation recording.
"""

from typing import Optional, Tuple
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.core.url import normalize_url
from intel_os.db.models.document import Document
from intel_os.db.models.document_source import DocumentSource
from intel_os.db.models.document_topic import DocumentTopic
from intel_os.db.models.enums import RetentionTier
from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.identity import compute_metadata_fingerprint
from intel_os.ingestion.reconciliation import ReconciliationEngine


async def persist_discovery_record(
    session: AsyncSession,
    record: NormalizedDiscoveryRecord,
    source_id: uuid.UUID,
    topic_id: Optional[uuid.UUID] = None,
) -> Tuple[Document, DocumentSource, bool, bool]:
    """Persists a normalized discovery record into PostgreSQL.

    Returns:
        Tuple of:
            - Document (the resolved or newly created document entity)
            - DocumentSource (the resolved or newly created observation)
            - is_new_document (True if a new Document was inserted)
            - is_new_observation (True if a new DocumentSource was inserted)
    """
    # 1. Resolve Document match via strict identity rules
    existing_doc, match_method, match_confidence = await ReconciliationEngine.resolve(
        session,
        record,
        source_id=source_id,
    )

    if existing_doc is None:
        # Create a new logical document
        fingerprint = compute_metadata_fingerprint(
            title=record.title,
            authors=record.authors,
            venue=record.venue,
            year=record.publication_year,
        )
        doc = Document(
            doi=record.doi,
            arxiv_id=record.arxiv_id,
            canonical_url=record.canonical_url,
            metadata_fingerprint=fingerprint,
            title=record.title,
            authors=record.authors,
            publication_venue=record.venue,
            publication_date=record.publication_date,
            abstract=record.abstract,
            retention_tier=RetentionTier.DISCOVERED,
            relevance_score=0.0,
            credibility_prior=0.0,
            doc_metadata=record.provider_metadata,
        )
        session.add(doc)
        await session.flush()
        is_new_doc = True
    else:
        doc = existing_doc
        is_new_doc = False

        # Non-destructive metadata enrichment on matched document
        if not doc.abstract and record.abstract:
            doc.abstract = record.abstract
        if not doc.doi and record.doi:
            doc.doi = record.doi
        if not doc.arxiv_id and record.arxiv_id:
            doc.arxiv_id = record.arxiv_id
        if not doc.publication_venue and record.venue:
            doc.publication_venue = record.venue
        if not doc.publication_date and record.publication_date:
            doc.publication_date = record.publication_date
        await session.flush()

    # 2. Link Document to Topic if topic_id provided
    if topic_id:
        topic_stmt = select(DocumentTopic).where(
            DocumentTopic.document_id == doc.id,
            DocumentTopic.topic_id == topic_id,
        )
        res = await session.execute(topic_stmt)
        if not res.scalar_one_or_none():
            doc_topic = DocumentTopic(
                document_id=doc.id,
                topic_id=topic_id,
                relevance_score=0.0,
                assignment_method="HARVEST",
            )
            session.add(doc_topic)
            await session.flush()

    # 3. Check for existing DocumentSource observation (Idempotency check)
    norm_url = normalize_url(record.observed_url)
    if record.provider_document_id is not None:
        source_stmt = select(DocumentSource).where(
            DocumentSource.document_id == doc.id,
            DocumentSource.source_id == source_id,
            DocumentSource.provider_doc_id == record.provider_document_id,
        )
    else:
        source_stmt = select(DocumentSource).where(
            DocumentSource.document_id == doc.id,
            DocumentSource.source_id == source_id,
            DocumentSource.normalized_observed_url == norm_url,
            DocumentSource.provider_doc_id.is_(None),
        )

    res = await session.execute(source_stmt)
    existing_source = res.scalar_one_or_none()

    if existing_source:
        return doc, existing_source, is_new_doc, False

    # 4. Insert discrete observation record
    doc_source = DocumentSource(
        document_id=doc.id,
        source_id=source_id,
        provider_doc_id=record.provider_document_id,
        observed_url=record.observed_url,
        normalized_observed_url=norm_url,
        observed_metadata=record.provider_metadata,
        match_method=match_method,
        match_confidence=match_confidence,
        observed_at=record.observed_at,
    )
    session.add(doc_source)
    await session.flush()

    return doc, doc_source, is_new_doc, True
