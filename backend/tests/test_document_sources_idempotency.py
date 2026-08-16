"""Tests for DocumentSource Multi-Provider Observation Idempotency and NULL provider_doc_id Edge Cases."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.models import Document, DocumentSource, Source


@pytest.mark.asyncio
async def test_case_a_same_doc_same_source_same_provider_id_rejected(db_session: AsyncSession):
    """TEST A: (doc1, source1, provider_doc_id="arxiv:2403.001") inserted twice -> duplicate rejected."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00001",
        metadata_fingerprint="fp1",
        title="Paper A",
        authors=["Author 1"],
    )
    src = Source(
        name="arXiv Ingest Feed",
        source_type="ARXIV",
        base_url="https://arxiv.org",
    )
    db_session.add_all([doc, src])
    await db_session.flush()

    # First observation
    obs1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id="2403.00001",
        observed_url="https://arxiv.org/abs/2403.00001",
        match_method="ARXIV_ID_EXACT",
    )
    db_session.add(obs1)
    await db_session.flush()

    # Second observation with identical (doc, source, provider_doc_id)
    obs2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id="2403.00001",
        observed_url="https://arxiv.org/abs/2403.00001?alt=true",
        match_method="ARXIV_ID_EXACT",
    )
    db_session.add(obs2)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_case_b_same_doc_same_source_null_provider_same_url_rejected(db_session: AsyncSession):
    """TEST B: (doc1, source1, provider_doc_id=NULL, observed_url="http://site.com/p1") inserted twice -> duplicate rejected."""
    doc = Document(
        canonical_url="https://site.com/p1",
        metadata_fingerprint="fp2",
        title="Web Ingested Paper",
        authors=["Author 2"],
    )
    src = Source(
        name="Open Research Web Crawler",
        source_type="WEB",
        base_url="https://site.com",
    )
    db_session.add_all([doc, src])
    await db_session.flush()

    # First observation with provider_doc_id=NULL
    obs1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.com/p1",
        match_method="CANONICAL_URL",
    )
    db_session.add(obs1)
    await db_session.flush()

    # Duplicate observation with same URL and NULL provider_doc_id
    obs2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.com/p1",
        match_method="CANONICAL_URL",
    )
    db_session.add(obs2)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_case_c_same_doc_same_source_null_provider_different_url_allowed(db_session: AsyncSession):
    """TEST C: (doc1, source1, provider_doc_id=NULL, url1) and (doc1, source1, provider_doc_id=NULL, url2) -> ALLOWED as distinct observations."""
    doc = Document(
        canonical_url="https://site.com/main",
        metadata_fingerprint="fp3",
        title="Multi-page Web Report",
        authors=["Author 3"],
    )
    src = Source(
        name="Conference Site Crawler",
        source_type="WEB",
        base_url="https://site.com",
    )
    db_session.add_all([doc, src])
    await db_session.flush()

    obs_page1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.com/paper/overview.html",
        match_method="CANONICAL_URL",
    )
    obs_page2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.com/paper/supplement.html",
        match_method="CANONICAL_URL",
    )

    db_session.add_all([obs_page1, obs_page2])
    await db_session.flush()

    assert obs_page1.id != obs_page2.id
    assert obs_page1.observed_url != obs_page2.observed_url


@pytest.mark.asyncio
async def test_case_d_tracking_url_normalized_to_same_identity_rejected(db_session: AsyncSession):
    """TEST D: URLs differing only in tracking query parameters normalize to the same identity -> rejected."""
    doc = Document(
        canonical_url="https://site.com/p4",
        metadata_fingerprint="fp4",
        title="Tracking Param Paper",
        authors=["Author 4"],
    )
    src = Source(
        name="Tracking Crawler",
        source_type="WEB",
        base_url="https://site.com",
    )
    db_session.add_all([doc, src])
    await db_session.flush()

    obs1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.com/p4",
    )
    db_session.add(obs1)
    await db_session.flush()

    obs2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.com/p4?utm_source=twitter&ref=newsletter",
    )
    db_session.add(obs2)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()

