"""PostgreSQL 16 Multi-Provider Ingestion Integration Test.

Executes end-to-end ingestion, multi-provider same-DOI reconciliation,
and re-ingestion idempotency on real PostgreSQL 16 with JSONB and TEXT[] types.
"""

from datetime import date
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.models.document import Document
from intel_os.db.models.document_source import DocumentSource
from intel_os.db.models.source import Source
from intel_os.db.models.topic import Topic
from intel_os.ingestion.dto import NormalizedDiscoveryRecord
from intel_os.ingestion.persistence import persist_discovery_record


@pytest.mark.asyncio
async def test_postgres_real_multi_provider_reconciliation(pg_session: AsyncSession):
    """Verifies end-to-end reconciliation on real PostgreSQL 16."""
    # 1. Seed Sources
    s_crossref = Source(name="PG Crossref", source_type="doi_registry", base_url="https://api.crossref.org")
    s_openalex = Source(name="PG OpenAlex", source_type="open_index", base_url="https://api.openalex.org")
    s_s2 = Source(name="PG Semantic Scholar", source_type="graph_index", base_url="https://api.semanticscholar.org")
    pg_session.add_all([s_crossref, s_openalex, s_s2])
    await pg_session.flush()

    topic = Topic(name="PostgreSQL AI Architecture", slug="pg-ai-arch")
    pg_session.add(topic)
    await pg_session.flush()

    test_doi = "10.1000/182"

    rec1 = NormalizedDiscoveryRecord(
        provider="crossref",
        provider_document_id=test_doi,
        title="Scalable Multi-Provider Architecture",
        authors=["Alice Johnson", "Bob Lee"],
        doi=test_doi,
        canonical_url=f"https://doi.org/{test_doi}",
        observed_url=f"http://dx.doi.org/{test_doi}",
        publication_date=date(2024, 1, 15),
        publication_year=2024,
        venue="IEEE Transactions on Software Engineering",
        abstract="Architecture for robust scholarly indexing.",
        provider_metadata={"crossref_id": 123},
    )

    rec2 = NormalizedDiscoveryRecord(
        provider="openalex",
        provider_document_id="W9999999",
        title="Scalable Multi-Provider Architecture",
        authors=["Alice Johnson", "Bob Lee"],
        doi=test_doi,
        canonical_url=f"https://doi.org/{test_doi}",
        observed_url="https://openalex.org/W9999999",
        publication_date=date(2024, 1, 15),
        publication_year=2024,
        venue="IEEE Transactions on Software Engineering",
        abstract="Architecture for robust scholarly indexing.",
        provider_metadata={"openalex_score": 9.5},
    )

    rec3 = NormalizedDiscoveryRecord(
        provider="semantic_scholar",
        provider_document_id="s2_sha_abcdef",
        title="Scalable Multi-Provider Architecture",
        authors=["Alice Johnson", "Bob Lee"],
        doi=test_doi,
        canonical_url=f"https://doi.org/{test_doi}",
        observed_url="https://semanticscholar.org/paper/s2_sha_abcdef",
        publication_date=date(2024, 1, 15),
        publication_year=2024,
        venue="IEEE TSE",
        abstract="Architecture for robust scholarly indexing with full graphs.",
        provider_metadata={"citations": 100},
    )

    # Ingest all 3 provider records
    doc1, _, is_new1, is_obs1 = await persist_discovery_record(pg_session, rec1, s_crossref.id, topic.id)
    doc2, _, is_new2, is_obs2 = await persist_discovery_record(pg_session, rec2, s_openalex.id, topic.id)
    doc3, _, is_new3, is_obs3 = await persist_discovery_record(pg_session, rec3, s_s2.id, topic.id)

    assert is_new1 is True and is_obs1 is True
    assert is_new2 is False and is_obs2 is True
    assert is_new3 is False and is_obs3 is True

    await pg_session.commit()

    # Query PG16 directly
    doc_res = await pg_session.execute(select(Document).where(Document.doi == test_doi))
    all_docs = doc_res.scalars().all()
    assert len(all_docs) == 1

    sources_res = await pg_session.execute(select(DocumentSource).where(DocumentSource.document_id == doc1.id))
    all_sources = sources_res.scalars().all()
    assert len(all_sources) == 3

    # Re-run for PG idempotency verification
    doc1_re, _, is_new1_re, is_obs1_re = await persist_discovery_record(pg_session, rec1, s_crossref.id, topic.id)
    doc2_re, _, is_new2_re, is_obs2_re = await persist_discovery_record(pg_session, rec2, s_openalex.id, topic.id)
    doc3_re, _, is_new3_re, is_obs3_re = await persist_discovery_record(pg_session, rec3, s_s2.id, topic.id)

    assert not is_new1_re and not is_obs1_re
    assert not is_new2_re and not is_obs2_re
    assert not is_new3_re and not is_obs3_re

    await pg_session.commit()

    # Assert counts remain unchanged
    doc_res_after = await pg_session.execute(select(Document).where(Document.doi == test_doi))
    assert len(doc_res_after.scalars().all()) == 1

    sources_res_after = await pg_session.execute(select(DocumentSource).where(DocumentSource.document_id == doc1.id))
    assert len(sources_res_after.scalars().all()) == 3
