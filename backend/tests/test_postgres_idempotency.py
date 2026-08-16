"""PostgreSQL 16 Idempotency Tests for DocumentSource and Normalized Observed URL."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.models import Document, DocumentSource, Source


@pytest.mark.asyncio
async def test_postgres_case_a_duplicate_provider_id_rejected(pg_session: AsyncSession):
    """TEST A (Postgres): same doc, same source, same provider_doc_id -> rejected by uq_doc_sources_provider."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00010",
        metadata_fingerprint="fp_pg_a",
        title="Postgres Paper A",
        authors=["Author PG 1"],
    )
    src = Source(
        name="arXiv Ingest PG",
        source_type="ARXIV",
        base_url="https://arxiv.org",
    )
    pg_session.add_all([doc, src])
    await pg_session.flush()

    obs1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id="2403.00010",
        observed_url="https://arxiv.org/abs/2403.00010",
    )
    pg_session.add(obs1)
    await pg_session.flush()

    obs2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id="2403.00010",
        observed_url="https://arxiv.org/abs/2403.00010?alt=true",
    )
    pg_session.add(obs2)
    with pytest.raises(IntegrityError) as exc_info:
        await pg_session.flush()
    assert "uq_doc_sources_provider" in str(exc_info.value)
    await pg_session.rollback()


@pytest.mark.asyncio
async def test_postgres_case_b_null_provider_same_normalized_url_rejected(pg_session: AsyncSession):
    """TEST B (Postgres): same doc, same source, NULL provider_doc_id, same normalized URL -> rejected."""
    doc = Document(
        canonical_url="https://site.org/paper_b",
        metadata_fingerprint="fp_pg_b",
        title="Postgres Paper B",
        authors=["Author PG 2"],
    )
    src = Source(
        name="Web Feed PG B",
        source_type="WEB",
        base_url="https://site.org",
    )
    pg_session.add_all([doc, src])
    await pg_session.flush()

    obs1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.org/paper_b",
    )
    pg_session.add(obs1)
    await pg_session.flush()

    obs2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.org/paper_b",
    )
    pg_session.add(obs2)
    with pytest.raises(IntegrityError) as exc_info:
        await pg_session.flush()
    assert "uq_doc_sources_url_null_provider" in str(exc_info.value)
    await pg_session.rollback()


@pytest.mark.asyncio
async def test_postgres_case_c_null_provider_different_normalized_urls_allowed(pg_session: AsyncSession):
    """TEST C (Postgres): same doc, same source, NULL provider_doc_id, different URLs -> allowed."""
    doc = Document(
        canonical_url="https://site.org/paper_c",
        metadata_fingerprint="fp_pg_c",
        title="Postgres Paper C",
        authors=["Author PG 3"],
    )
    src = Source(
        name="Web Feed PG C",
        source_type="WEB",
        base_url="https://site.org",
    )
    pg_session.add_all([doc, src])
    await pg_session.flush()

    obs1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.org/paper_c/main.html",
    )
    obs2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.org/paper_c/supplement.html",
    )
    pg_session.add_all([obs1, obs2])
    await pg_session.flush()

    assert obs1.id != obs2.id
    assert obs1.normalized_observed_url != obs2.normalized_observed_url


@pytest.mark.asyncio
async def test_postgres_case_d_tracking_url_normalized_to_same_identity_rejected(pg_session: AsyncSession):
    """TEST D (Postgres): URLs differing only in tracking parameters normalize to same identity -> rejected."""
    doc = Document(
        canonical_url="https://site.org/paper_d",
        metadata_fingerprint="fp_pg_d",
        title="Postgres Paper D",
        authors=["Author PG 4"],
    )
    src = Source(
        name="Web Feed PG D",
        source_type="WEB",
        base_url="https://site.org",
    )
    pg_session.add_all([doc, src])
    await pg_session.flush()

    # URL without tracking parameters
    obs1 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.org/paper_d",
    )
    pg_session.add(obs1)
    await pg_session.flush()

    # Same URL with UTM tracking parameters
    obs2 = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id=None,
        observed_url="https://site.org/paper_d?utm_source=twitter&utm_medium=feed",
    )
    pg_session.add(obs2)

    with pytest.raises(IntegrityError) as exc_info:
        await pg_session.flush()
    assert "uq_doc_sources_url_null_provider" in str(exc_info.value)
    await pg_session.rollback()
