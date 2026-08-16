# Intel OS / NCKH Intelligence Platform — Data Model & Schema Specification

## 1. Entity-Relationship Overview

```mermaid
erDiagram
    TOPICS ||--o{ DOCUMENT_TOPICS : "mapped_via"
    DOCUMENTS ||--o{ DOCUMENT_TOPICS : "categorized_in"
    TOPICS ||--o{ RESEARCH_GAPS : "spans"
    TOPICS ||--o{ RESEARCH_OPPORTUNITIES : "focuses"
    TOPICS ||--o{ USER_NOTES : "annotates"

    SOURCES ||--o{ DOCUMENT_SOURCES : "observes"
    DOCUMENTS ||--o{ DOCUMENT_SOURCES : "discovered_from"
    
    DOCUMENT_SOURCES ||--o{ DOCUMENT_SNAPSHOTS : "fetched_via"
    DOCUMENTS ||--o{ DOCUMENT_SNAPSHOTS : "has_versions"
    DOCUMENT_SNAPSHOTS ||--o{ DOCUMENT_CHUNKS : "splits_into"
    DOCUMENT_SNAPSHOTS ||--o{ CLAIMS : "extracted_from_snapshot"
    
    CLAIMS ||--o{ EVIDENCE_ITEMS : "validated_by"
    CLAIMS ||--o{ RELATIONSHIPS : "source_target"
    CLAIMS ||--o{ CONTRADICTIONS : "conflicts"

    RESEARCH_GAPS ||--o{ RESEARCH_OPPORTUNITIES : "motivates"
    CONTRADICTIONS ||--o{ RESEARCH_OPPORTUNITIES : "informs"

    RESEARCH_OPPORTUNITIES ||--o{ RESEARCH_IDEAS : "spawns"
    RESEARCH_IDEAS ||--o{ IDEA_PROVENANCE : "lineage_root"
    CLAIMS ||--o{ IDEA_PROVENANCE : "grounds"
    DOCUMENTS ||--o{ IDEA_PROVENANCE : "originates"
    DOCUMENT_SNAPSHOTS ||--o{ IDEA_PROVENANCE : "version_pin"

    RESEARCH_IDEAS ||--o{ EXPERIMENT_LOGS : "tests"
```

---

## 2. Enumerations & Status Types

```sql
-- Retention tier for documents & snapshots in Intelligence Lake
CREATE TYPE retention_tier AS ENUM (
    'DISCOVERED',   -- Metadata only (Title, DOI, Authors, Venue, Canonical URL)
    'INDEXED',      -- Metadata + Abstract + Fast topic embeddings
    'RELEVANT',     -- Full parsed text & structural sections
    'RETAINED',     -- Raw PDF/HTML preserved in S3 Object Storage
    'ARCHIVED'      -- Deep cold storage backup
);

-- Grounding status: Verifies text presence in source, NOT scientific validity
CREATE TYPE grounding_status AS ENUM (
    'UNVERIFIED',           -- Extracted claim has not completed quote verification
    'VERBATIM_MATCH',       -- Statement matches exact character substring in source text
    'PARAPHRASE_VERIFIED',  -- Statement semantic meaning verified against bounding quotes
    'FAILED'                -- Quote does not exist in source text (discarded/quarantined)
);

-- Claim type classification
CREATE TYPE claim_type AS ENUM (
    'EMPIRICAL_FINDING',    -- Quantitative/experimental result reported with data
    'AUTHOR_HYPOTHESIS',    -- Proposition formulated by author without full proof
    'BACKGROUND_ASSERTION', -- Stated as prior literature or domain assumption
    'INTERPRETATION',       -- Author qualitative deduction or explanation of results
    'LIMITATION',           -- Explicitly stated boundary condition or failure mode
    'FUTURE_WORK',          -- Suggested research direction or unexplored experiment
    'OTHER'                 -- Uncategorized statement
);

-- Epistemic status: Reflects scientific validity & consensus across literature
CREATE TYPE epistemic_status AS ENUM (
    'UNASSESSED',   -- Default upon extraction; no scientific truth judgment made yet
    'SUPPORTED',    -- Validated by rigorous methodology, empirical evidence, or replication
    'CONTESTED',    -- Direct conflicting finding or contradiction identified in literature
    'REFUTED',      -- Methodologically invalid, retracted, or empirically disproven
    'CONSENSUS',    -- Established scientific consensus across multiple independent studies
    'SPECULATIVE'   -- Untested hypothesis or theoretical conjecture
);

-- Idea status in Opportunity Bank
CREATE TYPE idea_status AS ENUM (
    'CANDIDATE',    -- Automatically generated proposal
    'REVIEWED',     -- Evaluated by human researcher
    'ACCEPTED',     -- Approved for active research / paper authoring
    'REJECTED',     -- Deemed infeasible or duplicate
    'ARCHIVED'      -- Historical reference
);

-- Background job execution status
CREATE TYPE job_status AS ENUM (
    'PENDING',
    'RUNNING',
    'COMPLETED',
    'FAILED',
    'RETRYING'
);
```

---

## 3. Versioned Embedding Model Contract for V1

* **V1 Embedding Contract**: All vector columns in the V1 schema (`document_chunks.embedding`, `claims.embedding`, `research_ideas.embedding`) strictly enforce **768 dimensions** (matching `text-embedding-004` / Gemini Embeddings / standard 768-dim models).
* **LLM Provider Independence**: Reasoning LLMs (Gemini, Claude, GPT) remain dynamically interchangeable via prompt adapters. Vector embeddings, however, conform to the active database contract dimension.
* **Future Embedding Migration Protocol**: Upgrading embedding models (e.g., to 1536-dim or 3072-dim) requires:
  1. Creating a versioned column or table (e.g., `document_chunks_v2` or `embedding_v2 vector(1536)`).
  2. Running an asynchronous backfill migration to compute new embeddings.
  3. Building new HNSW indexes.
  4. Swapping the active search query configuration.
  *(pgvector strictly rejects inserting vectors whose dimension does not match the column definition).*

---

## 4. Identity Signal Classification & Reconciliation Policy

Document identity is resolved via a tiered confidence model. **False merges are more dangerous than temporary duplication.**

### 4.1 Identity Signal Tiers

| Tier | Signal Type | Examples | Reconciliation Behavior |
| :--- | :--- | :--- | :--- |
| **HARD / TRUSTED** | Exact match on globally unique identifier | DOI exact match, arXiv ID exact match | Auto-merge into single logical `documents` record. No review required. |
| **STRONG** | Canonical URL after normalization | Same URL with tracking parameters stripped | Auto-merge with logged match method. |
| **CANDIDATE** | Metadata fingerprint, title/author overlap | `metadata_fingerprint` match, fuzzy title similarity \(\ge 0.95\) | Create `document_sources` observation; flag for reconciliation review if no hard identity exists. |

### 4.2 Reconciliation Metadata

The `document_sources` table carries lightweight reconciliation tracking:
* `match_method`: How this observation was linked to a logical document (e.g., `'DOI_EXACT'`, `'ARXIV_ID_EXACT'`, `'CANONICAL_URL'`, `'METADATA_FINGERPRINT'`, `'MANUAL'`).
* `match_confidence`: Confidence score (`1.0` for hard identity; `0.7–0.9` for candidate signals).

### 4.3 Reconciliation Invariants
1. **Hard identity matches** (DOI, arXiv ID) are trusted and auto-merged.
2. **Metadata fingerprint matches** without a hard identity create a provider observation linked to the best-matching document, but the system MUST NOT silently merge two logical works on fingerprint alone if titles differ significantly.
3. **When in doubt, preserve as separate documents**. A human or future reconciliation pass can merge them.
4. **Provider provenance is never discarded**: Every observation is recorded in `document_sources` regardless of merge outcome.

---

## 5. V1 Target Schema vs Gate-Staged Migrations

The DDL below defines the **complete V1 Target Schema** (18 normalized tables). However, Alembic migrations are introduced incrementally by gate:

| Migration Stage | Tables Created | Gate |
| :--- | :--- | :--- |
| **G1 Foundation** | `topics`, `sources`, `documents`, `document_topics`, `document_sources`, `document_snapshots`, `background_jobs` | G1 |
| **G3/G4 Extraction & Memory** | `document_chunks`, `claims`, `evidence_items`, `relationships`, `user_notes` | G3/G4 |
| **G5 Opportunity & Lineage** | `research_gaps`, `contradictions`, `research_opportunities`, `research_ideas`, `idea_provenance`, `experiment_logs` | G5 |

> [!IMPORTANT]
> **G1 creates only the 7 foundation tables.** Later gate tables are defined here for architectural completeness but MUST NOT be instantiated in the first migration. Each gate introduces its own migration when the feature becomes real.

---

## 6. PostgreSQL 16+ Authoritative V1 Target DDL (18 Normalized Tables)

```sql
-- Ensure extensions are enabled
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- 1. Topics (Research Areas & Domains)                           [G1 MIGRATION]
-- =============================================================================
CREATE TABLE topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    keywords TEXT[] NOT NULL DEFAULT '{}',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =============================================================================
-- 2. Sources (Globally Reusable Ingestion Providers)             [G1 MIGRATION]
-- =============================================================================
CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    source_type VARCHAR(50) NOT NULL, -- 'ARXIV', 'CROSSREF', 'SEMANTIC_SCHOLAR', 'OPENALEX', 'WEB'
    base_url TEXT NOT NULL,
    feed_url TEXT,
    config JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_crawled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =============================================================================
-- 3. Documents (Logical Scientific Works / Papers)               [G1 MIGRATION]
-- =============================================================================
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doi VARCHAR(255) UNIQUE,
    arxiv_id VARCHAR(100) UNIQUE,
    canonical_url TEXT NOT NULL,
    metadata_fingerprint VARCHAR(64) NOT NULL, -- SHA-256 of normalized (title + authors + venue + year)
    title TEXT NOT NULL,
    authors TEXT[] NOT NULL DEFAULT '{}',
    publication_venue VARCHAR(255),
    publication_date DATE,
    abstract TEXT,
    retention_tier retention_tier NOT NULL DEFAULT 'DISCOVERED',
    relevance_score FLOAT NOT NULL DEFAULT 0.0,
    credibility_prior FLOAT NOT NULL DEFAULT 0.0, -- Heuristic source prior, NOT proof of claim truth
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_documents_doi ON documents(doi);
CREATE INDEX idx_documents_arxiv_id ON documents(arxiv_id);
CREATE INDEX idx_documents_metadata_fingerprint ON documents(metadata_fingerprint);
CREATE INDEX idx_documents_retention_tier ON documents(retention_tier);

-- =============================================================================
-- 4. Document Topics (M:N Document <-> Topic)                    [G1 MIGRATION]
-- =============================================================================
CREATE TABLE document_topics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    relevance_score FLOAT NOT NULL DEFAULT 0.0,
    assignment_method VARCHAR(50) NOT NULL DEFAULT 'MANUAL',
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, topic_id)
);

CREATE INDEX idx_document_topics_doc ON document_topics(document_id);
CREATE INDEX idx_document_topics_topic ON document_topics(topic_id);

-- =============================================================================
-- 5. Document Sources (Multi-Provider Observation Provenance)    [G1 MIGRATION]
-- =============================================================================
CREATE TABLE document_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    provider_doc_id VARCHAR(255), -- ID in the provider system (may be NULL for web crawls)
    observed_url TEXT NOT NULL,
    observed_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    match_method VARCHAR(50) NOT NULL DEFAULT 'MANUAL', -- 'DOI_EXACT', 'ARXIV_ID_EXACT', 'CANONICAL_URL', 'METADATA_FINGERPRINT', 'MANUAL'
    match_confidence FLOAT NOT NULL DEFAULT 1.0, -- 1.0 for hard identity, 0.7-0.9 for candidate signals
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_document_sources_doc ON document_sources(document_id);
CREATE INDEX idx_document_sources_source ON document_sources(source_id);

-- Idempotency Rule 1: Non-NULL provider_doc_id uniqueness per (document, source)
CREATE UNIQUE INDEX uq_doc_sources_provider ON document_sources (document_id, source_id, provider_doc_id)
WHERE provider_doc_id IS NOT NULL;

-- Idempotency Rule 2: NULL provider_doc_id uniqueness per (document, source, observed_url)
CREATE UNIQUE INDEX uq_doc_sources_url_null_provider ON document_sources (document_id, source_id, observed_url)
WHERE provider_doc_id IS NULL;

-- =============================================================================
-- 6. Document Snapshots (Fetched Representations / Versions)     [G1 MIGRATION]
-- =============================================================================
CREATE TABLE document_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    document_source_id UUID REFERENCES document_sources(id) ON DELETE RESTRICT, -- Provenance protected: cannot drop source observation while snapshots depend on it
    version_identifier VARCHAR(50) NOT NULL DEFAULT 'v1', -- e.g. 'arxiv_v1', 'arxiv_v2'
    mime_type VARCHAR(100) NOT NULL, -- 'application/pdf', 'text/html'
    source_url TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL, -- SHA-256 of downloaded representation bytes
    byte_size BIGINT,
    raw_s3_key TEXT, -- Location in S3/R2 when retained
    retention_tier retention_tier NOT NULL DEFAULT 'INDEXED',
    parser_version VARCHAR(50),
    extraction_version VARCHAR(50),
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- Snapshot identity: same document + version + representation format + identical bytes
    UNIQUE(document_id, version_identifier, mime_type, content_hash)
);

CREATE INDEX idx_snapshots_document_id ON document_snapshots(document_id);
CREATE INDEX idx_snapshots_content_hash ON document_snapshots(content_hash);
CREATE INDEX idx_snapshots_document_source ON document_snapshots(document_source_id);

-- =============================================================================
-- 7. Background Jobs (Async Task Execution & Telemetry)          [G1 MIGRATION]
-- =============================================================================
CREATE TABLE background_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_type VARCHAR(100) NOT NULL,
    idempotency_key VARCHAR(128) NOT NULL UNIQUE,
    status job_status NOT NULL DEFAULT 'PENDING',
    progress_percentage FLOAT NOT NULL DEFAULT 0.0,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    result JSONB,
    error_message TEXT,
    attempts INT NOT NULL DEFAULT 0,
    max_attempts INT NOT NULL DEFAULT 3,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_background_jobs_idempotency_key ON background_jobs(idempotency_key);
CREATE INDEX idx_background_jobs_status ON background_jobs(status);

-- =============================================================================
-- 8. Document Chunks & Vector Index                          [G3/G4 MIGRATION]
-- =============================================================================
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    snapshot_id UUID NOT NULL REFERENCES document_snapshots(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    section_name VARCHAR(100),
    content TEXT NOT NULL,
    token_count INT NOT NULL,
    embedding vector(768), -- V1 Embedding Contract (768 dimensions)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(snapshot_id, chunk_index)
);

CREATE INDEX idx_document_chunks_document_id ON document_chunks(document_id);
CREATE INDEX idx_document_chunks_snapshot_id ON document_chunks(snapshot_id);
CREATE INDEX idx_document_chunks_embedding_hnsw ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- =============================================================================
-- 9. Claims (Personal Research Memory Core)                  [G3/G4 MIGRATION]
-- =============================================================================
-- PROVENANCE INVARIANT: Machine-extracted claims MUST have a NOT NULL snapshot_id.
-- ON DELETE RESTRICT on snapshot_id prevents silently orphaning extracted intelligence.
CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    snapshot_id UUID NOT NULL REFERENCES document_snapshots(id) ON DELETE RESTRICT,
    claim_text TEXT NOT NULL,
    normalized_statement TEXT NOT NULL,
    claim_type claim_type NOT NULL DEFAULT 'OTHER',
    grounding_status grounding_status NOT NULL DEFAULT 'UNVERIFIED',
    quote_verbatim TEXT NOT NULL,
    quote_start_char INT,
    quote_end_char INT,
    epistemic_status epistemic_status NOT NULL DEFAULT 'UNASSESSED',
    grounding_confidence FLOAT NOT NULL DEFAULT 0.0,
    embedding vector(768), -- V1 Embedding Contract (768 dimensions)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_claims_document_id ON claims(document_id);
CREATE INDEX idx_claims_snapshot_id ON claims(snapshot_id);
CREATE INDEX idx_claims_claim_type ON claims(claim_type);
CREATE INDEX idx_claims_grounding_status ON claims(grounding_status);
CREATE INDEX idx_claims_epistemic_status ON claims(epistemic_status);
CREATE INDEX idx_claims_embedding_hnsw ON claims USING hnsw (embedding vector_cosine_ops);

-- =============================================================================
-- 10. Evidence Items (Empirical Grounding)                   [G3/G4 MIGRATION]
-- =============================================================================
-- PROVENANCE INVARIANT: Machine-extracted evidence MUST have a NOT NULL snapshot_id.
CREATE TABLE evidence_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    snapshot_id UUID NOT NULL REFERENCES document_snapshots(id) ON DELETE RESTRICT,
    evidence_type VARCHAR(50) NOT NULL, -- 'BENCHMARK', 'STATISTICAL_RESULT', 'QUALITATIVE', 'ABLATION'
    dataset_name VARCHAR(255),
    hardware_setup VARCHAR(255),
    sample_size INT,
    metric_name VARCHAR(100),
    metric_value FLOAT,
    baseline_value FLOAT,
    statistical_significance VARCHAR(50),
    table_figure_ref VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_evidence_claim_id ON evidence_items(claim_id);
CREATE INDEX idx_evidence_document_id ON evidence_items(document_id);
CREATE INDEX idx_evidence_snapshot_id ON evidence_items(snapshot_id);

-- =============================================================================
-- 11. Relationships (Claim-to-Claim Logic Graph)             [G3/G4 MIGRATION]
-- =============================================================================
CREATE TABLE relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    target_claim_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    relation_type VARCHAR(50) NOT NULL,
    explanation TEXT,
    weight FLOAT NOT NULL DEFAULT 1.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(source_claim_id, target_claim_id, relation_type)
);

CREATE INDEX idx_relationships_source_claim ON relationships(source_claim_id);
CREATE INDEX idx_relationships_target_claim ON relationships(target_claim_id);
CREATE INDEX idx_relationships_type ON relationships(relation_type);

-- =============================================================================
-- 12. User Notes (Personal Research Memory Annotations)      [G3/G4 MIGRATION]
-- =============================================================================
-- User-authored notes are loosely linked; NULLable FKs are appropriate.
CREATE TABLE user_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    claim_id UUID REFERENCES claims(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    tags TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_notes_topic_id ON user_notes(topic_id);
CREATE INDEX idx_user_notes_document_id ON user_notes(document_id);

-- =============================================================================
-- 13. Research Gaps (Limitations & Missing Evaluations)         [G5 MIGRATION]
-- =============================================================================
CREATE TABLE research_gaps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    primary_limitation TEXT NOT NULL,
    gap_score FLOAT NOT NULL DEFAULT 0.0,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_research_gaps_topic_id ON research_gaps(topic_id);

-- =============================================================================
-- 14. Contradictions (Conflicting Empirical Claims)             [G5 MIGRATION]
-- =============================================================================
CREATE TABLE contradictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    claim_a_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    claim_b_id UUID NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
    contradiction_summary TEXT NOT NULL,
    severity_score FLOAT NOT NULL DEFAULT 0.0,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contradictions_topic_id ON contradictions(topic_id);
CREATE INDEX idx_contradictions_claims ON contradictions(claim_a_id, claim_b_id);

-- =============================================================================
-- 15. Research Opportunities                                    [G5 MIGRATION]
-- =============================================================================
CREATE TABLE research_opportunities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    research_gap_id UUID REFERENCES research_gaps(id) ON DELETE SET NULL,
    contradiction_id UUID REFERENCES contradictions(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    opportunity_statement TEXT NOT NULL,
    semantic_distinctiveness_score FLOAT NOT NULL DEFAULT 0.0,
    feasibility_score FLOAT NOT NULL DEFAULT 0.0,
    priority_score FLOAT NOT NULL DEFAULT 0.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_opportunities_topic_id ON research_opportunities(topic_id);

-- =============================================================================
-- 16. Research Ideas (Candidate Hypotheses & Blueprints)        [G5 MIGRATION]
-- =============================================================================
CREATE TABLE research_ideas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    opportunity_id UUID NOT NULL REFERENCES research_opportunities(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    hypothesis TEXT NOT NULL,
    proposed_methodology TEXT NOT NULL,
    estimated_resource_cost TEXT,
    status idea_status NOT NULL DEFAULT 'CANDIDATE',
    embedding vector(768), -- V1 Embedding Contract (768 dimensions)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_research_ideas_topic_id ON research_ideas(topic_id);
CREATE INDEX idx_research_ideas_opportunity_id ON research_ideas(opportunity_id);
CREATE INDEX idx_research_ideas_embedding_hnsw ON research_ideas USING hnsw (embedding vector_cosine_ops);

-- =============================================================================
-- 17. Idea Provenance (Snapshot-Pinned Backward Lineage)        [G5 MIGRATION]
-- =============================================================================
-- PROVENANCE INVARIANT: snapshot_id is NOT NULL — lineage must reach exact bytes.
CREATE TABLE idea_provenance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idea_id UUID NOT NULL REFERENCES research_ideas(id) ON DELETE CASCADE,
    opportunity_id UUID REFERENCES research_opportunities(id) ON DELETE SET NULL,
    gap_id UUID REFERENCES research_gaps(id) ON DELETE SET NULL,
    claim_id UUID REFERENCES claims(id) ON DELETE SET NULL,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    snapshot_id UUID NOT NULL REFERENCES document_snapshots(id) ON DELETE RESTRICT,
    provenance_role VARCHAR(50) NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_idea_provenance_idea_id ON idea_provenance(idea_id);
CREATE INDEX idx_idea_provenance_document_id ON idea_provenance(document_id);
CREATE INDEX idx_idea_provenance_snapshot_id ON idea_provenance(snapshot_id);
CREATE INDEX idx_idea_provenance_claim_id ON idea_provenance(claim_id);

-- =============================================================================
-- 18. Experiment Logs (Empirical Trials & Lessons)              [G5 MIGRATION]
-- =============================================================================
CREATE TABLE experiment_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idea_id UUID NOT NULL REFERENCES research_ideas(id) ON DELETE CASCADE,
    experiment_name VARCHAR(255) NOT NULL,
    setup_description TEXT NOT NULL,
    results_summary TEXT NOT NULL,
    did_succeed BOOLEAN NOT NULL,
    lessons_learned TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_experiment_logs_idea_id ON experiment_logs(idea_id);
```

---

## 7. Provenance Invariant Summary

The following invariants are enforced by schema constraints:

| Entity | `snapshot_id` | `ON DELETE` | Rationale |
| :--- | :--- | :--- | :--- |
| `document_chunks` | `NOT NULL` | `CASCADE` | Chunks are physical derivatives of a snapshot; deleting the snapshot deletes chunks. |
| `claims` | `NOT NULL` | `RESTRICT` | Machine-extracted claims must always trace to the exact snapshot. Deleting a snapshot with live claims is blocked. |
| `evidence_items` | `NOT NULL` | `RESTRICT` | Evidence is extracted from a snapshot. Provenance must not be silently destroyed. |
| `idea_provenance` | `NOT NULL` | `RESTRICT` | Lineage graph must always reach exact source bytes. |
| `user_notes` | N/A (no `snapshot_id`) | N/A | User-authored content is loosely linked. NULLable FKs to `document_id`, `claim_id`, and `topic_id` are appropriate. |

---

## 8. Backward Provenance Traversal Query

This query reconstructs the full backward provenance tree for any given `research_idea`, traversing from idea through snapshot to the originating source provider:

```sql
SELECT 
    ri.id AS idea_id,
    ri.title AS idea_title,
    ro.id AS opportunity_id,
    ro.title AS opportunity_title,
    rg.id AS gap_id,
    rg.title AS gap_title,
    c.id AS claim_id,
    c.claim_text AS claim_text,
    c.quote_verbatim AS evidence_quote,
    c.grounding_status AS claim_grounding,
    c.epistemic_status AS claim_epistemic_status,
    d.id AS document_id,
    d.title AS document_title,
    d.doi AS document_doi,
    ds.version_identifier AS snapshot_version,
    ds.mime_type AS snapshot_mime_type,
    ds.content_hash AS snapshot_content_hash,
    -- Relational path to originating Source (not inferred from URL strings)
    dsrc.observed_url AS provider_observed_url,
    dsrc.match_method AS provider_match_method,
    src.name AS source_name,
    src.source_type AS source_type,
    ip.provenance_role AS role
FROM research_ideas ri
JOIN idea_provenance ip ON ri.id = ip.idea_id
LEFT JOIN research_opportunities ro ON ip.opportunity_id = ro.id
LEFT JOIN research_gaps rg ON ip.gap_id = rg.id
LEFT JOIN claims c ON ip.claim_id = c.id
JOIN documents d ON ip.document_id = d.id
JOIN document_snapshots ds ON ip.snapshot_id = ds.id
LEFT JOIN document_sources dsrc ON ds.document_source_id = dsrc.id
LEFT JOIN sources src ON dsrc.source_id = src.id
WHERE ri.id = 'YOUR_RESEARCH_IDEA_UUID';
```
