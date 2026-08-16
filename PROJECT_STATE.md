# Intel OS / NCKH Intelligence Platform — Project State & Safety Checkpoint

## 1. Milestone Tracking

* **Current Milestone**: **Gate 1 (G1) — Database Foundation & Backend Scaffolding**
* **Previous Milestones**:
  * **Gate 0 (G0)**: Score 77/100 | Status: REVISE
  * **Gate 0.1 (G0.1)**: Score 88/100 | Status: NEAR PASS
  * **Gate 0.2 (G0.2)**: APPROVED by External Mentor
* **G1 Completion Percentage**: **100%**
* **Active Working Branch**: `main`
* **Remote Repository**: `https://github.com/Phuchello/NCKH`
* **Status**: **G1 COMPLETED — Ready for Mentor Review & G2 Authorization**

---

## 2. What Exists (G1 Deliverables)

1. **Executable Backend Architecture (`backend/intel_os`)**:
   * [`main.py`](backend/intel_os/main.py): FastAPI application factory, CORS middleware, lifespan lifecycle management with database engine connection & graceful cleanup.
   * [`core/config.py`](backend/intel_os/core/config.py): Strongly typed `Settings` using `pydantic-settings` with safe development defaults and validation.
   * [`core/logging.py`](backend/intel_os/core/logging.py): Structured logging handler.
   * [`db/base.py`](backend/intel_os/db/base.py): SQLAlchemy 2.0 DeclarativeBase, constraint naming conventions (`ix_`, `uq_`, `ck_`, `fk_`, `pk_`), and platform-independent `GUID` type decorator.
   * [`db/session.py`](backend/intel_os/db/session.py): Async engine creation, `async_sessionmaker`, `get_db` FastAPI dependency with transaction boundaries, `get_db_context` background worker manager, and `check_db_connectivity` health probe.
   * [`db/models/`](backend/intel_os/db/models/): SQLAlchemy 2.x async models for **exactly 7 G1 foundation tables**:
     * `Topic` (`topics`): Domains with unique names/slugs, JSON keywords, and cascade relationships.
     * `Source` (`sources`): Global reusable feeds with unique names, JSON config.
     * `Document` (`documents`): Logical papers with unique DOI/arXiv ID, non-unique `metadata_fingerprint` (candidate signal), retention tier, and cascade relationships.
     * `DocumentTopic` (`document_topics`): M:N junction with `UNIQUE(document_id, topic_id)`.
     * `DocumentSource` (`document_sources`): Provider observation table with partial unique indexes (`uq_doc_sources_provider` and `uq_doc_sources_url_null_provider`) correctly resolving NULL `provider_doc_id` observation idempotency.
     * `DocumentSnapshot` (`document_snapshots`): Versioned representations with `UNIQUE(document_id, version_identifier, mime_type, content_hash)` and `ON DELETE RESTRICT` on `document_source_id` with ORM `passive_deletes=True`.
     * `BackgroundJob` (`background_jobs`): Execution telemetry with `UNIQUE(idempotency_key)`.
   * [`db/migrations/`](backend/intel_os/db/migrations/): Alembic migration environment with async multi-dialect support and `0001_g1_foundation` initial migration.
   * [`storage/local_cache.py`](backend/intel_os/storage/local_cache.py): `LocalCacheManager` enforcing `MAX_LOCAL_CACHE_GB` budget, LRU eviction (`prune()`), path traversal containment security checks, and safe error handling.
   * [`api/routes/`](backend/intel_os/api/routes/):
     * `GET /api/v1/health`: Liveness probe and async database connectivity check (returns 200 `healthy`/`connected` or 503 `degraded`/`disconnected`).
     * `GET /api/v1/status`: Version, environment, embedding dimension (768), and cache utilization metrics.
   * [`docker-compose.yml`](docker-compose.yml): Local PostgreSQL 16 + pgvector environment configuration.

2. **Automated Test Suite (`backend/tests/`)**:
   * 30 automated unit and integration tests executing across 8 test modules:
     * `test_config.py`: Settings defaults, environment overrides, validation.
     * `test_db_lifecycle.py`: Engine creation, async session lifecycle, rollback on error, connectivity check.
     * `test_models_crud.py`: CRUD, uniqueness constraints, cascade deletion on Topic and Document.
     * `test_document_sources_idempotency.py`: NULL `provider_doc_id` edge cases (Tests A, B, C).
     * `test_snapshot_representations.py`: Multi-format snapshots (PDF vs HTML), duplicate byte rejection, `ON DELETE RESTRICT` provenance protection.
     * `test_local_cache.py`: Cache usage, LRU pruning, path traversal security guardrails, clear.
     * `test_api_health_status.py`: Health and status API endpoint integration.
     * `test_alembic_migration.py`: Exact 7-table schema boundary verification, Alembic upgrade/downgrade/upgrade lifecycle cycle.
   * **Test Result**: **30 passed in 2.84s (100% pass rate, 87% code coverage)**.

3. **Architecture Decision Records (ADRs)**:
   * `ADR-0014`: Partial Unique Index Strategy for Multi-Provider Observation Idempotency with NULL Identifiers.
   * `ADR-0015`: Snapshot-to-Observation Provenance Protection via ON DELETE RESTRICT and ORM Passive Deletes.

---

## 3. What Does NOT Exist (Strict Gate Boundaries)

To ensure disciplined execution, the following components are strictly deferred to subsequent gates and are **not** present in G1:

* **No live crawler fleet or connector implementation code** (Deferred to Gate 2).
* **No LLM extraction runners, prompt scripts, or OpenAI/Gemini execution calls** (Deferred to Gate 3).
* **No vector embedding generation or R2 object storage client** (Deferred to Gate 4).
* **No research gap mining or automated hypothesis generation code** (Deferred to Gate 5).
* **No hybrid search or RRF reranking** (Deferred to Gate 6).
* **No research handbook compilation or PDF/LaTeX generation code** (Deferred to Gate 7).
* **No Next.js UI frontend code or web components** (Deferred to Gate 8).
* **No custom model training or fine-tuning pipelines** (Explicit platform non-goal for G0–V1).

---

## 4. Architecture & Spec Amendments Documented in G1

1. **DocumentSource Idempotency Strategy (ADR-0014)**:
   * Replaced single `UNIQUE NULLS NOT DISTINCT` with two partial unique indexes:
     * `uq_doc_sources_provider`: `UNIQUE (document_id, source_id, provider_doc_id) WHERE provider_doc_id IS NOT NULL`
     * `uq_doc_sources_url_null_provider`: `UNIQUE (document_id, source_id, observed_url) WHERE provider_doc_id IS NULL`
   * Solves the edge case where web crawls without provider IDs have multiple distinct pages for the same document.
2. **Snapshot-to-Observation Provenance (ADR-0015)**:
   * Configured `ON DELETE RESTRICT` on `document_snapshots.document_source_id` with `passive_deletes=True` on ORM relationship to guarantee source observations cannot be deleted while dependent snapshots exist.

---

## 5. Tests Executed & Results

### 5.2 Test & Migration Verification Results (G1.1 Reality Check)

#### A. PostgreSQL 16 & Alembic Lifecycle
* **Container**: `pgvector/pgvector:pg16` on PostgreSQL 16.15 (healthy).
* **Extensions**: `vector` and `uuid-ossp` active.
* **Alembic Upgrade Head**: Created exactly 7 application tables (`topics`, `sources`, `documents`, `document_topics`, `document_sources`, `document_snapshots`, `background_jobs`) + `alembic_version`.
* **Alembic Downgrade Base**: Cleanly dropped all 7 tables and custom ENUM types (`retention_tier`, `job_status`) with zero type leaks.
* **Second Alembic Upgrade Head**: Recreated tables and types flawlessly.

#### B. Test Suite Execution (49 Passed / 0 Failed, 91% Coverage)
```text
tests/test_alembic_migration.py ..................... [4 passed - SQLite & DDL boundaries]
tests/test_api_health_status.py ..................... [2 passed - FastAPI /health & /status]
tests/test_config.py ................................ [3 passed - Pydantic settings & validation]
tests/test_db_lifecycle.py .......................... [3 passed - Engine lifecycle & transactions]
tests/test_document_sources_idempotency.py .......... [4 passed - Observation idempotency Scenarios A-D]
tests/test_local_cache.py ........................... [4 passed - LRU pruning, quota & path containment]
tests/test_models_crud.py ........................... [7 passed - 7 G1 tables CRUD & cascade delete]
tests/test_postgres_contract.py ..................... [4 passed - Real PG16 table inventory, enums, column types, alembic lifecycle]
tests/test_postgres_idempotency.py .................. [4 passed - Real PG16 Scenarios A-D with normalized URLs]
tests/test_postgres_snapshots.py .................... [4 passed - Real PG16 multi-format, byte dedup, RESTRICT delete, manual import]
tests/test_snapshot_representations.py .............. [4 passed - Snapshot SQLite unit representation invariants]
tests/test_url_normalization.py ..................... [6 passed - Conservative deterministic URL normalizer]

TOTAL: 49 passed in 5.44s
CODE COVERAGE: 91% (724 statements, 68 missed)
```

---

## 6. Last Safe Checkpoint

* **G0 Baseline Checkpoint**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **G0.1 Corrected Checkpoint**: `60abdbe65b88b2dd61e28d5419655b50c5fd94cb`
* **G0.2 Hardened Checkpoint**: `f95ddb8`
* **G1 Implementation Checkpoint**: `e07286b`
* **G1.1 Hardened Checkpoint**: `86a9175`
* **Working Tree**: Clean.

---

## 7. Exact Next Action

1. Commit G1.1 implementation deliverables and push to `origin/main`.
2. Present G1.1 completion report to mentor for Gate 2 authorization.
3. **DO NOT START GATE 2 BEFORE MENTOR APPROVAL**.
