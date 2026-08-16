"""G1 Foundation Schema (7 Tables).

Revision ID: 0001_g1_foundation
Revises: 
Create Date: 2026-08-16 01:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001_g1_foundation"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    is_postgres = conn.dialect.name == "postgresql"

    # 0. PostgreSQL Extensions and Controlled ENUM Lifecycle
    if is_postgres:
        op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        op.execute('CREATE EXTENSION IF NOT EXISTS vector')
        op.execute("CREATE TYPE retention_tier AS ENUM ('DISCOVERED', 'INDEXED', 'RELEVANT', 'RETAINED', 'ARCHIVED')")
        op.execute("CREATE TYPE job_status AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'RETRYING')")

    retention_tier_type = (
        postgresql.ENUM(
            "DISCOVERED",
            "INDEXED",
            "RELEVANT",
            "RETAINED",
            "ARCHIVED",
            name="retention_tier",
            create_type=False,
        )
        if is_postgres
        else sa.Enum(
            "DISCOVERED",
            "INDEXED",
            "RELEVANT",
            "RETAINED",
            "ARCHIVED",
            name="retention_tier",
            native_enum=False,
        )
    )

    job_status_type = (
        postgresql.ENUM(
            "PENDING",
            "RUNNING",
            "COMPLETED",
            "FAILED",
            "RETRYING",
            name="job_status",
            create_type=False,
        )
        if is_postgres
        else sa.Enum(
            "PENDING",
            "RUNNING",
            "COMPLETED",
            "FAILED",
            "RETRYING",
            name="job_status",
            native_enum=False,
        )
    )

    uuid_col = (
        lambda: sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        )
        if is_postgres
        else sa.Column("id", sa.CHAR(36), primary_key=True)
    )

    # 1. Topics Table
    op.create_table(
        "topics",
        uuid_col(),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "keywords",
            postgresql.ARRAY(sa.String()) if is_postgres else sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::text[]") if is_postgres else "[]",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("name", name="uq_topics_name"),
        sa.UniqueConstraint("slug", name="uq_topics_slug"),
    )
    op.create_index("ix_topics_name", "topics", ["name"])
    op.create_index("ix_topics_slug", "topics", ["slug"])

    # 2. Sources Table
    op.create_table(
        "sources",
        uuid_col(),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False),
        sa.Column("base_url", sa.Text(), nullable=False),
        sa.Column("feed_url", sa.Text(), nullable=True),
        sa.Column(
            "config",
            postgresql.JSONB() if is_postgres else sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb") if is_postgres else "{}",
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("last_crawled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("name", name="uq_sources_name"),
    )
    op.create_index("ix_sources_name", "sources", ["name"])

    # 3. Documents Table
    op.create_table(
        "documents",
        uuid_col(),
        sa.Column("doi", sa.String(255), nullable=True),
        sa.Column("arxiv_id", sa.String(100), nullable=True),
        sa.Column("canonical_url", sa.Text(), nullable=False),
        sa.Column("metadata_fingerprint", sa.String(64), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column(
            "authors",
            postgresql.ARRAY(sa.String()) if is_postgres else sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::text[]") if is_postgres else "[]",
        ),
        sa.Column("publication_venue", sa.String(255), nullable=True),
        sa.Column("publication_date", sa.Date(), nullable=True),
        sa.Column("abstract", sa.Text(), nullable=True),
        sa.Column("retention_tier", retention_tier_type, nullable=False, server_default="DISCOVERED"),
        sa.Column("relevance_score", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("credibility_prior", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column(
            "metadata",
            postgresql.JSONB() if is_postgres else sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb") if is_postgres else "{}",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("doi", name="uq_documents_doi"),
        sa.UniqueConstraint("arxiv_id", name="uq_documents_arxiv_id"),
    )
    op.create_index("ix_documents_doi", "documents", ["doi"])
    op.create_index("ix_documents_arxiv_id", "documents", ["arxiv_id"])
    op.create_index("ix_documents_metadata_fingerprint", "documents", ["metadata_fingerprint"])
    op.create_index("ix_documents_retention_tier", "documents", ["retention_tier"])

    # 4. Document Topics (M:N Junction Table)
    op.create_table(
        "document_topics",
        uuid_col(),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "topic_id",
            postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36),
            sa.ForeignKey("topics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("relevance_score", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column("assignment_method", sa.String(50), nullable=False, server_default="MANUAL"),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("document_id", "topic_id", name="uq_document_topics_doc_topic"),
    )
    op.create_index("ix_document_topics_document_id", "document_topics", ["document_id"])
    op.create_index("ix_document_topics_topic_id", "document_topics", ["topic_id"])

    # 5. Document Sources (Multi-Provider Observation Table)
    op.create_table(
        "document_sources",
        uuid_col(),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36),
            sa.ForeignKey("sources.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("provider_doc_id", sa.String(255), nullable=True),
        sa.Column("observed_url", sa.Text(), nullable=False),
        sa.Column("normalized_observed_url", sa.Text(), nullable=False),
        sa.Column(
            "observed_metadata",
            postgresql.JSONB() if is_postgres else sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb") if is_postgres else "{}",
        ),
        sa.Column("match_method", sa.String(50), nullable=False, server_default="MANUAL"),
        sa.Column("match_confidence", sa.Float(), nullable=False, server_default=sa.text("1.0")),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_document_sources_document_id", "document_sources", ["document_id"])
    op.create_index("ix_document_sources_source_id", "document_sources", ["source_id"])

    # Partial unique index for non-NULL provider_doc_id
    op.create_index(
        "uq_doc_sources_provider",
        "document_sources",
        ["document_id", "source_id", "provider_doc_id"],
        unique=True,
        postgresql_where=sa.text("provider_doc_id IS NOT NULL"),
        sqlite_where=sa.text("provider_doc_id IS NOT NULL"),
    )
    # Partial unique index for NULL provider_doc_id (using normalized_observed_url)
    op.create_index(
        "uq_doc_sources_url_null_provider",
        "document_sources",
        ["document_id", "source_id", "normalized_observed_url"],
        unique=True,
        postgresql_where=sa.text("provider_doc_id IS NULL"),
        sqlite_where=sa.text("provider_doc_id IS NULL"),
    )

    # 6. Document Snapshots Table
    op.create_table(
        "document_snapshots",
        uuid_col(),
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "document_source_id",
            postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36),
            sa.ForeignKey("document_sources.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("version_identifier", sa.String(50), nullable=False, server_default="v1"),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("byte_size", sa.BigInteger(), nullable=True),
        sa.Column("raw_s3_key", sa.Text(), nullable=True),
        sa.Column("retention_tier", retention_tier_type, nullable=False, server_default="INDEXED"),
        sa.Column("parser_version", sa.String(50), nullable=True),
        sa.Column("extraction_version", sa.String(50), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint(
            "document_id",
            "version_identifier",
            "mime_type",
            "content_hash",
            name="uq_snapshots_doc_version_mime_hash",
        ),
    )
    op.create_index("ix_document_snapshots_document_id", "document_snapshots", ["document_id"])
    op.create_index("ix_document_snapshots_document_source_id", "document_snapshots", ["document_source_id"])
    op.create_index("ix_document_snapshots_content_hash", "document_snapshots", ["content_hash"])

    # 7. Background Jobs Table
    op.create_table(
        "background_jobs",
        uuid_col(),
        sa.Column("job_type", sa.String(100), nullable=False),
        sa.Column("idempotency_key", sa.String(128), nullable=False),
        sa.Column("status", job_status_type, nullable=False, server_default="PENDING"),
        sa.Column("progress_percentage", sa.Float(), nullable=False, server_default=sa.text("0.0")),
        sa.Column(
            "payload",
            postgresql.JSONB() if is_postgres else sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb") if is_postgres else "{}",
        ),
        sa.Column("result", postgresql.JSONB() if is_postgres else sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default=sa.text("3")),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("idempotency_key", name="uq_background_jobs_idempotency_key"),
    )
    op.create_index("ix_background_jobs_idempotency_key", "background_jobs", ["idempotency_key"])
    op.create_index("ix_background_jobs_status", "background_jobs", ["status"])


def downgrade() -> None:
    conn = op.get_bind()
    is_postgres = conn.dialect.name == "postgresql"

    # Drop tables in reverse dependency order
    op.drop_table("background_jobs")
    op.drop_table("document_snapshots")
    op.drop_table("document_sources")
    op.drop_table("document_topics")
    op.drop_table("documents")
    op.drop_table("sources")
    op.drop_table("topics")

    if is_postgres:
        op.execute("DROP TYPE IF EXISTS job_status CASCADE")
        op.execute("DROP TYPE IF EXISTS retention_tier CASCADE")
