"""Tests for G1 Core Models CRUD and Relational Constraints."""

from datetime import date
import uuid
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.models import (
    BackgroundJob,
    Document,
    DocumentSnapshot,
    DocumentSource,
    DocumentTopic,
    JobStatus,
    RetentionTier,
    Source,
    Topic,
)


@pytest.mark.asyncio
async def test_topic_crud_and_uniqueness(db_session: AsyncSession):
    """Validates Topic model creation, query, and unique constraints."""
    topic = Topic(
        name="Edge AI & Speculative Decoding",
        slug="edge-ai-speculative-decoding",
        description="Accelerating LLMs on edge devices using speculation",
        keywords=["edge", "speculative-decoding", "npu", "latency"],
    )
    db_session.add(topic)
    await db_session.flush()

    assert topic.id is not None
    assert topic.is_active is True

    # Query back
    stmt = select(Topic).where(Topic.slug == "edge-ai-speculative-decoding")
    result = await db_session.execute(stmt)
    fetched = result.scalar_one()
    assert fetched.name == "Edge AI & Speculative Decoding"

    # Duplicate name should raise IntegrityError
    dup_topic = Topic(
        name="Edge AI & Speculative Decoding",
        slug="different-slug",
    )
    db_session.add(dup_topic)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_source_crud(db_session: AsyncSession):
    """Validates Source model creation and uniqueness."""
    source = Source(
        name="arXiv cs.AI Feed",
        source_type="ARXIV",
        base_url="https://arxiv.org",
        feed_url="http://export.arxiv.org/rss/cs.AI",
        config={"rate_limit_per_second": 3},
    )
    db_session.add(source)
    await db_session.flush()

    assert source.id is not None
    assert source.source_type == "ARXIV"

    # Duplicate source name rejected
    dup_source = Source(
        name="arXiv cs.AI Feed",
        source_type="ARXIV",
        base_url="https://arxiv.org/alt",
    )
    db_session.add(dup_source)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_document_metadata_fingerprint_non_uniqueness(db_session: AsyncSession):
    """CRITICAL GUARDRAIL: metadata_fingerprint is NOT globally unique.

    Two distinct papers sharing a fingerprint must both be insertable without a DB constraint error.
    """
    shared_fingerprint = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    doc1 = Document(
        doi="10.1000/182",
        canonical_url="https://example.com/paper1",
        metadata_fingerprint=shared_fingerprint,
        title="Edge Speculation v1",
        authors=["Alice", "Bob"],
        retention_tier=RetentionTier.DISCOVERED,
    )
    doc2 = Document(
        doi="10.1000/183",
        canonical_url="https://example.com/paper2",
        metadata_fingerprint=shared_fingerprint,
        title="Edge Speculation v2 (Separate logical work)",
        authors=["Charlie", "Dave"],
        retention_tier=RetentionTier.DISCOVERED,
    )

    db_session.add_all([doc1, doc2])
    await db_session.flush()

    assert doc1.id != doc2.id
    assert doc1.metadata_fingerprint == doc2.metadata_fingerprint


@pytest.mark.asyncio
async def test_document_topics_many_to_many(db_session: AsyncSession):
    """Validates M:N Document <-> Topic association and uniqueness."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00001",
        metadata_fingerprint="fp12345",
        title="Multi-Topic Research Paper",
        authors=["Author A"],
    )
    topic_a = Topic(name="Topic Alpha", slug="topic-alpha")
    topic_b = Topic(name="Topic Beta", slug="topic-beta")

    db_session.add_all([doc, topic_a, topic_b])
    await db_session.flush()

    # Link to both topics
    dt_a = DocumentTopic(document_id=doc.id, topic_id=topic_a.id, relevance_score=0.95)
    dt_b = DocumentTopic(document_id=doc.id, topic_id=topic_b.id, relevance_score=0.80)
    db_session.add_all([dt_a, dt_b])
    await db_session.flush()

    # Duplicate link to same topic should fail
    dt_dup = DocumentTopic(document_id=doc.id, topic_id=topic_a.id, relevance_score=0.50)
    db_session.add(dt_dup)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_background_job_crud_and_idempotency(db_session: AsyncSession):
    """Validates BackgroundJob execution tracking and idempotency_key uniqueness."""
    job = BackgroundJob(
        job_type="INGEST_ARXIV_FEED",
        idempotency_key="job_key_feed_2026_08_16_01",
        status=JobStatus.PENDING,
        payload={"feed": "cs.AI", "batch_size": 50},
    )
    db_session.add(job)
    await db_session.flush()

    assert job.id is not None
    assert job.status == JobStatus.PENDING

    # Attempting duplicate job key fails
    dup_job = BackgroundJob(
        job_type="INGEST_ARXIV_FEED",
        idempotency_key="job_key_feed_2026_08_16_01",
        status=JobStatus.PENDING,
    )
    db_session.add(dup_job)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_topic_cascade_delete(db_session: AsyncSession):
    """Validates that deleting a Topic cascades and removes associated DocumentTopic records."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00099",
        metadata_fingerprint="fp_cascade_1",
        title="Cascade Paper",
        authors=["Author Cascade"],
    )
    topic = Topic(name="Cascade Topic", slug="cascade-topic")
    db_session.add_all([doc, topic])
    await db_session.flush()

    dt = DocumentTopic(document_id=doc.id, topic_id=topic.id)
    db_session.add(dt)
    await db_session.flush()

    # Delete topic
    await db_session.delete(topic)
    await db_session.flush()

    # Verify junction row was removed
    stmt = select(DocumentTopic).where(DocumentTopic.document_id == doc.id)
    result = await db_session.execute(stmt)
    assert result.scalars().first() is None


@pytest.mark.asyncio
async def test_document_cascade_delete(db_session: AsyncSession):
    """Validates that deleting a Document cascades to document_topics, document_sources, and document_snapshots."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00100",
        metadata_fingerprint="fp_cascade_2",
        title="Full Cascade Paper",
        authors=["Author Full"],
    )
    topic = Topic(name="Full Cascade Topic", slug="full-cascade-topic")
    src = Source(name="Cascade Source", source_type="ARXIV", base_url="https://arxiv.org")
    db_session.add_all([doc, topic, src])
    await db_session.flush()

    dt = DocumentTopic(document_id=doc.id, topic_id=topic.id)
    dsrc = DocumentSource(document_id=doc.id, source_id=src.id, provider_doc_id="2403.00100", observed_url="http://arxiv.org")
    db_session.add_all([dt, dsrc])
    await db_session.flush()

    snap = DocumentSnapshot(
        document_id=doc.id,
        document_source_id=dsrc.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="http://arxiv.org/pdf",
        content_hash="full_cascade_hash",
    )
    db_session.add(snap)
    await db_session.flush()

    # Delete document
    await db_session.delete(doc)
    await db_session.flush()

    # Verify all child rows removed
    assert (await db_session.execute(select(DocumentTopic).where(DocumentTopic.document_id == doc.id))).scalars().first() is None
    assert (await db_session.execute(select(DocumentSource).where(DocumentSource.document_id == doc.id))).scalars().first() is None
    assert (await db_session.execute(select(DocumentSnapshot).where(DocumentSnapshot.document_id == doc.id))).scalars().first() is None

