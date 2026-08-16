"""PostgreSQL 16 Snapshot Multi-Representation and Provenance Invariant Tests."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from intel_os.db.models import Document, DocumentSnapshot, DocumentSource, RetentionTier, Source


@pytest.mark.asyncio
async def test_postgres_snapshot_multi_representation(pg_session: AsyncSession):
    """CONTRACT (Postgres): arXiv v2 PDF and arXiv v2 HTML on same document are both allowed."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00020",
        metadata_fingerprint="fp_pg_snap_1",
        title="Postgres Multi-Format Paper",
        authors=["Author PG Snap 1"],
    )
    pg_session.add(doc)
    await pg_session.flush()

    snap_pdf = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="arxiv_v2",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00020v2.pdf",
        content_hash="hash_pdf_bytes_pg_1",
        byte_size=2048000,
        retention_tier=RetentionTier.RELEVANT,
    )
    snap_html = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="arxiv_v2",
        mime_type="text/html",
        source_url="https://arxiv.org/html/2403.00020v2",
        content_hash="hash_html_bytes_pg_2",
        byte_size=512000,
        retention_tier=RetentionTier.RELEVANT,
    )

    pg_session.add_all([snap_pdf, snap_html])
    await pg_session.flush()

    assert snap_pdf.id != snap_html.id
    assert snap_pdf.version_identifier == snap_html.version_identifier == "arxiv_v2"


@pytest.mark.asyncio
async def test_postgres_duplicate_snapshot_rejected(pg_session: AsyncSession):
    """CONTRACT (Postgres): Duplicate snapshot representation bytes are rejected."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00021",
        metadata_fingerprint="fp_pg_snap_2",
        title="Postgres Duplicate Snap Paper",
        authors=["Author PG Snap 2"],
    )
    pg_session.add(doc)
    await pg_session.flush()

    snap1 = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00021v1.pdf",
        content_hash="identical_hash_pg_abc",
    )
    pg_session.add(snap1)
    await pg_session.flush()

    snap2 = DocumentSnapshot(
        document_id=doc.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00021v1.pdf",
        content_hash="identical_hash_pg_abc",
    )
    pg_session.add(snap2)
    with pytest.raises(IntegrityError) as exc_info:
        await pg_session.flush()
    assert "uq_snapshots_doc_version_mime_hash" in str(exc_info.value)
    await pg_session.rollback()


@pytest.mark.asyncio
async def test_postgres_snapshot_restrict_delete_provenance(pg_session: AsyncSession):
    """CONTRACT (Postgres): Attempting to delete a DocumentSource observation referenced by DocumentSnapshot is rejected with RESTRICT error."""
    doc = Document(
        canonical_url="https://arxiv.org/abs/2403.00022",
        metadata_fingerprint="fp_pg_snap_3",
        title="Postgres Restrict Paper",
        authors=["Author PG Snap 3"],
    )
    src = Source(
        name="arXiv Restrict Feed PG",
        source_type="ARXIV",
        base_url="https://arxiv.org",
    )
    pg_session.add_all([doc, src])
    await pg_session.flush()

    doc_source = DocumentSource(
        document_id=doc.id,
        source_id=src.id,
        provider_doc_id="2403.00022",
        observed_url="https://arxiv.org/abs/2403.00022",
    )
    pg_session.add(doc_source)
    await pg_session.flush()

    snapshot = DocumentSnapshot(
        document_id=doc.id,
        document_source_id=doc_source.id,
        version_identifier="v1",
        mime_type="application/pdf",
        source_url="https://arxiv.org/pdf/2403.00022.pdf",
        content_hash="content_hash_restrict_pg",
    )
    pg_session.add(snapshot)
    await pg_session.flush()

    # Deleting provider observation while snapshot references it must fail on Postgres
    await pg_session.delete(doc_source)
    with pytest.raises(IntegrityError) as exc_info:
        await pg_session.flush()
    assert "foreign key constraint" in str(exc_info.value).lower() or "fk_document_snapshots" in str(exc_info.value)
    await pg_session.rollback()


@pytest.mark.asyncio
async def test_postgres_snapshot_direct_import_allowed(pg_session: AsyncSession):
    """USE CASE: Direct manual/local snapshot import without provider observation is allowed."""
    doc = Document(
        canonical_url="https://manual.local/paper",
        metadata_fingerprint="fp_pg_snap_manual",
        title="Manual Local Import Paper",
        authors=["Local Researcher"],
    )
    pg_session.add(doc)
    await pg_session.flush()

    snapshot = DocumentSnapshot(
        document_id=doc.id,
        document_source_id=None,  # Direct manual import
        version_identifier="camera_ready",
        mime_type="application/pdf",
        source_url="file:///local/paper.pdf",
        content_hash="manual_import_hash_123",
        retention_tier=RetentionTier.RETAINED,
    )
    pg_session.add(snapshot)
    await pg_session.flush()

    assert snapshot.id is not None
    assert snapshot.document_source_id is None
