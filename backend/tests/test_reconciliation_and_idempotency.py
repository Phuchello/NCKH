"""Integration and Acceptance Tests for Multi-Provider Reconciliation and Idempotency.

Verifies:
1. Cross-provider same-DOI reconciliation (Crossref + OpenAlex + Semantic Scholar -> 1 Document, 3 Sources)
2. Re-ingestion idempotency (re-running identical records creates 0 duplicate rows)
3. arXiv version coalescence (v1 and v2 map to same logical Document)
4. Candidate-only non-merge preservation (same title/authors with different or missing DOIs are NOT auto-merged)
"""

from datetime import date
import uuid
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
async def test_cross_provider_same_doi_reconciliation_and_idempotency(db_session: AsyncSession):
    """Critical Acceptance Test:

    1. Crossref, OpenAlex, and Semantic Scholar return records with the same DOI.
       Database MUST have exactly 1 Document and 3 DocumentSource rows.
    2. Re-running the exact same ingestion MUST result in still 1 Document and 3 DocumentSource rows.
    """
    # 1. Create Source feeds for all 3 providers
    src_crossref = Source(
        name="Crossref Feed",
        source_type="doi_registry",
        base_url="https://api.crossref.org/works",
    )
    src_openalex = Source(
        name="OpenAlex Feed",
        source_type="open_index",
        base_url="https://api.openalex.org/works",
    )
    src_s2 = Source(
        name="Semantic Scholar Feed",
        source_type="graph_index",
        base_url="https://api.semanticscholar.org/graph/v1",
    )
    db_session.add_all([src_crossref, src_openalex, src_s2])
    await db_session.flush()

    # Create active research topic
    topic = Topic(name="Research Gap Mining", slug="gap-mining")
    db_session.add(topic)
    await db_session.flush()

    target_doi = "10.1145/3372278.3390678"

    rec_crossref = NormalizedDiscoveryRecord(
        provider="crossref",
        provider_document_id=target_doi,
        title="A Graph-Based Framework for Research Gap Detection",
        authors=["Jane Doe", "John Smith"],
        doi=target_doi,
        canonical_url=f"https://doi.org/{target_doi}",
        observed_url=f"http://dx.doi.org/{target_doi}",
        publication_date=date(2020, 6, 15),
        publication_year=2020,
        venue="ACM Transactions on Information Systems",
        abstract="We propose a novel framework for detecting research gaps.",
        provider_metadata={"source": "crossref_raw"},
    )

    rec_openalex = NormalizedDiscoveryRecord(
        provider="openalex",
        provider_document_id="W2741809807",
        title="A Graph-Based Framework for Research Gap Detection",
        authors=["Jane Doe", "John Smith"],
        doi=target_doi,
        canonical_url=f"https://doi.org/{target_doi}",
        observed_url="https://openalex.org/W2741809807",
        publication_date=date(2020, 6, 15),
        publication_year=2020,
        venue="ACM Transactions on Information Systems",
        abstract="We propose a novel graph-based framework for gap detection.",
        provider_metadata={"source": "openalex_raw"},
    )

    rec_s2 = NormalizedDiscoveryRecord(
        provider="semantic_scholar",
        provider_document_id="649def34f8be52c8b66281af98ae772c99cf93e5",
        title="A Graph-Based Framework for Research Gap Detection",
        authors=["Jane Doe", "John Smith"],
        doi=target_doi,
        canonical_url=f"https://doi.org/{target_doi}",
        observed_url="https://www.semanticscholar.org/paper/649def34f8be52c8b66281af98ae772c99cf93e5",
        publication_date=date(2020, 6, 15),
        publication_year=2020,
        venue="ACM Trans. Inf. Syst.",
        abstract="We propose a novel framework for detecting research gaps in scientific literature.",
        provider_metadata={"source": "s2_raw"},
    )

    # --- Phase 1: Ingest from Crossref ---
    doc1, src_obs1, is_new1, is_obs_new1 = await persist_discovery_record(
        db_session, rec_crossref, source_id=src_crossref.id, topic_id=topic.id
    )
    assert is_new1 is True
    assert is_obs_new1 is True
    assert doc1.doi == target_doi

    # --- Phase 2: Ingest from OpenAlex (Same DOI) ---
    doc2, src_obs2, is_new2, is_obs_new2 = await persist_discovery_record(
        db_session, rec_openalex, source_id=src_openalex.id, topic_id=topic.id
    )
    assert is_new2 is False  # Reconciled to doc1!
    assert is_obs_new2 is True
    assert doc2.id == doc1.id

    # --- Phase 3: Ingest from Semantic Scholar (Same DOI) ---
    doc3, src_obs3, is_new3, is_obs_new3 = await persist_discovery_record(
        db_session, rec_s2, source_id=src_s2.id, topic_id=topic.id
    )
    assert is_new3 is False  # Reconciled to doc1!
    assert is_obs_new3 is True
    assert doc3.id == doc1.id

    await db_session.commit()

    # Query DB to assert exact counts
    docs_stmt = select(Document).where(Document.doi == target_doi)
    docs = (await db_session.execute(docs_stmt)).scalars().all()
    assert len(docs) == 1, f"Expected exactly 1 Document, got {len(docs)}"

    sources_stmt = select(DocumentSource).where(DocumentSource.document_id == doc1.id)
    sources = (await db_session.execute(sources_stmt)).scalars().all()
    assert len(sources) == 3, f"Expected exactly 3 DocumentSources, got {len(sources)}"

    # --- Phase 4: Re-run the ENTIRE Ingestion Pipeline (Idempotency Test) ---
    doc1_re, _, is_new1_re, is_obs1_re = await persist_discovery_record(
        db_session, rec_crossref, source_id=src_crossref.id, topic_id=topic.id
    )
    doc2_re, _, is_new2_re, is_obs2_re = await persist_discovery_record(
        db_session, rec_openalex, source_id=src_openalex.id, topic_id=topic.id
    )
    doc3_re, _, is_new3_re, is_obs3_re = await persist_discovery_record(
        db_session, rec_s2, source_id=src_s2.id, topic_id=topic.id
    )

    assert is_new1_re is False and is_obs1_re is False
    assert is_new2_re is False and is_obs2_re is False
    assert is_new3_re is False and is_obs3_re is False

    await db_session.commit()

    # Verify counts remain unchanged
    docs_after = (await db_session.execute(docs_stmt)).scalars().all()
    sources_after = (await db_session.execute(sources_stmt)).scalars().all()
    assert len(docs_after) == 1
    assert len(sources_after) == 3


@pytest.mark.asyncio
async def test_arxiv_version_coalescence_to_logical_work(db_session: AsyncSession):
    """Verify arXiv v1 and v2 observations coalesce into the same logical Document."""
    source = Source(name="arXiv Feed", source_type="academic_repo", base_url="https://export.arxiv.org/api/query")
    db_session.add(source)
    await db_session.flush()

    rec_v1 = NormalizedDiscoveryRecord(
        provider="arxiv",
        provider_document_id="2301.12345",
        title="Deep Residual Learning",
        authors=["Kaiming He"],
        doi=None,
        arxiv_id="2301.12345",
        canonical_url="https://arxiv.org/abs/2301.12345",
        observed_url="http://arxiv.org/abs/2301.12345v1",
        external_ids={"arxiv": "2301.12345", "arxiv_version": "v1"},
        provider_metadata={"version": "v1"},
    )

    rec_v2 = NormalizedDiscoveryRecord(
        provider="arxiv",
        provider_document_id="2301.12345",
        title="Deep Residual Learning for Image Recognition",
        authors=["Kaiming He", "Xiangyu Zhang"],
        doi="10.1109/cvpr.2016.90",
        arxiv_id="2301.12345",
        canonical_url="https://arxiv.org/abs/2301.12345",
        observed_url="http://arxiv.org/abs/2301.12345v2",
        external_ids={"arxiv": "2301.12345", "arxiv_version": "v2"},
        provider_metadata={"version": "v2"},
    )

    doc_v1, _, is_new_v1, _ = await persist_discovery_record(db_session, rec_v1, source_id=source.id)
    doc_v2, _, is_new_v2, _ = await persist_discovery_record(db_session, rec_v2, source_id=source.id)

    assert is_new_v1 is True
    assert is_new_v2 is False  # Auto-merged onto same logical work
    assert doc_v2.id == doc_v1.id
    assert doc_v2.arxiv_id == "2301.12345"
    assert doc_v2.doi == "10.1109/cvpr.2016.90"  # Enriched from v2


@pytest.mark.asyncio
async def test_candidate_only_evidence_does_not_auto_merge(db_session: AsyncSession):
    """Verify identical title & author fingerprint with distinct DOIs are NOT merged."""
    source = Source(name="Generic Index", source_type="academic_api", base_url="https://example.com")
    db_session.add(source)
    await db_session.flush()

    rec_a = NormalizedDiscoveryRecord(
        provider="crossref",
        provider_document_id="10.5555/paper1",
        title="Attention Is All You Need",
        authors=["Ashish Vaswani", "Noam Shazeer"],
        doi="10.5555/paper1",
        canonical_url="https://doi.org/10.5555/paper1",
        observed_url="https://doi.org/10.5555/paper1",
    )

    rec_b = NormalizedDiscoveryRecord(
        provider="crossref",
        provider_document_id="10.5555/paper2",
        title="Attention Is All You Need",
        authors=["Ashish Vaswani", "Noam Shazeer"],
        doi="10.5555/paper2",  # Different DOI (e.g. workshop vs main conf)
        canonical_url="https://doi.org/10.5555/paper2",
        observed_url="https://doi.org/10.5555/paper2",
    )

    doc_a, _, is_new_a, _ = await persist_discovery_record(db_session, rec_a, source_id=source.id)
    doc_b, _, is_new_b, _ = await persist_discovery_record(db_session, rec_b, source_id=source.id)

    assert is_new_a is True
    assert is_new_b is True  # Maintained as separate documents
    assert doc_a.id != doc_b.id
