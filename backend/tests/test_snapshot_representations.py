"""Tests for DocumentSnapshot Multi-Representation Support and Provenance Invariants."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.models import Document, DocumentSnapshot, DocumentSource, RetentionTier, Source


@pytest.mark.asyncio
async def test_multi_representation_pdf_and_html_allowed(db_session: AsyncSession):
    """Validates that PDF and HTML representations of the same document version are both allowed."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00001",
        metadata_fingerprint="fp_snap_1",
        title="Multi-format Document",
        authors=["Author 1"],
    )
    db_session.add(doc)
    await db_session.flush()

    # Snapshot 1: arXiv v2 PDF
    snap_pdf = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="arxiv_v2",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00001v2.pdf",
        content_hash="hash_pdf_bytes_12345",
        byte_size=1048576,
        retention_tier=RetentionTier.RELEVANT,
    )

    # Snapshot 2: arXiv v2 HTML
    snap_html = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="arxiv_v2",
        mime_type="text/html",
        source_url="https://arxiv.org/html/2403.00001v2",
        content_hash="hash_html_bytes_67890",
        byte_size=524288,
        retention_tier=RetentionTier.RELEVANT,
    )

    db_session.add_all([snap_pdf, snap_html])
    await db_session.flush()

    assert snap_pdf.id != snap_html.id
    assert snap_pdf.version_identifier == snap_html.version_identifier == "arxiv_v2"


@pytest.mark.asyncio
async def test_duplicate_snapshot_representation_bytes_rejected(db_session: AsyncSession):
    """Validates that re-fetching identical bytes for the same version and format is rejected."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00002",
        metadata_fingerprint="fp_snap_2",
        title="Duplicate Snapshot Test",
        authors=["Author 2"],
    )
    db_session.add(doc)
    await db_session.flush()

    snap1 = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00002v1.pdf",
        content_hash="identical_hash_abc",
    )
    db_session.add(snap1)
    await db_session.flush()

    # Exact duplicate representation bytes
    snap2 = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00002v1.pdf",
        content_hash="identical_hash_abc",
    )
    db_session.add(snap2)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_snapshot_source_provenance_linkage(db_session: AsyncSession):
    """Validates snapshot linkage to originating provider observation."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00003",
        metadata_fingerprint="fp_snap_3",
        title="Provenance Test Paper",
        authors=["Author 3"],
    )
    src = Source(
        name="arXiv Feed Provenance",
        source_type="ARXIV",
        base_url="https://arxiv.org",
    )
    db_session.add_all([doc, src])
    await db_session.flush()

    doc_source = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id="2403.00003",
        observed_url="https://arxiv.org/abs/2403.00003",
    )
    db_session.add(doc_source)
    await db_session.flush()

    snapshot = DocumentSnapshot(
        document_id=doc.id,
        document_source_id=doc_source.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00003.pdf",
        content_hash="content_hash_prov_test",
    )
    db_session.add(snapshot)
    await db_session.flush()

    assert snapshot.document_source_id == doc_source.id
    assert snapshot.document_source.source.name == "arXiv Feed Provenance"


@pytest.mark.asyncio
async def test_snapshot_restrict_delete_on_document_source(db_session: AsyncSession):
    """Validates that deleting DocumentSource is blocked when a DocumentSnapshot references it."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00004",
        metadata_fingerprint="fp_snap_4",
        title="Restrict Delete Test Paper",
        authors=["Author 4"],
    )
    src = Source(
        name="arXiv Restrict Feed",
        source_type="ARXIV",
        base_url="https://arxiv.org",
    )
    db_session.add_all([doc, src])
    await db_session.flush()

    doc_source = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id="2403.00004",
        observed_url="https://arxiv.org/abs/2403.00004",
    )
    db_session.add(doc_source)
    await db_session.flush()

    snapshot = DocumentSnapshot(
        document_id=doc.id,
        document_source_id=doc_source.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00004.pdf",
        content_hash="content_hash_restrict_test",
    )
    db_session.add(snapshot)
    await db_session.flush()

    # Deleting the parent DocumentSource while snapshot is attached must be rejected
    await db_session.delete(doc_source)
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()

