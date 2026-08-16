# Intel OS / NCKH Intelligence Platform — Project State & Safety Checkpoint

## 1. Milestone Tracking

* **Current Milestone**: **Gate 1 (G1) / Gate 1.1 / Gate 1.2 — Database Foundation & Backend Scaffolding**
* **Previous Milestones**:
  * **Gate 0 (G0)**: Score 77/100 | Status: REVISE
  * **Gate 0.1 (G0.1)**: Score 88/100 | Status: NEAR PASS
  * **Gate 0.2 (G0.2)**: APPROVED by External Mentor
  * **Gate 1 (G1)**: Score 82/100 | Status: REVISE (Required Real PostgreSQL 16 & URL Idempotency)
  * **Gate 1.1 (G1.1)**: Local PG16 Hardening & URL Idempotency Completed
  * **Gate 1.2 (G1.2)**: CI Pipeline Green, Unused UUID Extension Removed, State Harmonized
* **G1 Completion Percentage**: **100%**
* **Active Working Branch**: `main`
* **Remote Repository**: `https://github.com/Phuchello/NCKH`
* **Status**: **G1.2 COMPLETED — Ready for Mentor Review & G2 Authorization**

---

## 2. What Exists (G1 Deliverables)

1. **Executable Backend Architecture (`backend/intel_os`)**:
   * [`main.py`](backend/intel_os/main.py): FastAPI application factory, CORS middleware, lifespan lifecycle management with database engine connection & graceful cleanup.
   * [`core/config.py`](backend/intel_os/core/config.py): Strongly typed `Settings` using `pydantic-settings` with safe development defaults and validation.
   * [`core/logging.py`](backend/intel_os/core/logging.py): Structured logging handler.
   * [`core/url.py`](backend/intel_os/core/url.py): Conservative, deterministic URL normalizer for observation deduplication.
   * [`db/base.py`](backend/intel_os/db/base.py): SQLAlchemy 2.0 DeclarativeBase, constraint naming conventions (`ix_`, `uq_`, `ck_`, `fk_`, `pk_`), and platform-independent `GUID` type decorator.
   * [`db/session.py`](backend/intel_os/db/session.py): Async engine creation, `async_sessionmaker`, `get_db` FastAPI dependency with transaction boundaries, `get_db_context` background worker manager, and `check_db_connectivity` health probe.
   * [`db/models/`](backend/intel_os/db/models/): SQLAlchemy 2.x async models for **exactly 7 G1 foundation tables**:
     * `Topic` (`topics`): Domains with unique names/slugs, native `TEXT[]` keywords, and cascade relationships.
     * `Source` (`sources`): Global reusable feeds with unique names, JSON config.
     * `Document` (`documents`): Logical papers with unique DOI/arXiv ID, non-unique `metadata_fingerprint` (candidate signal), native `TEXT[]` authors, retention tier, and cascade relationships.
     * `DocumentTopic` (`document_topics`): M:N junction with `UNIQUE(document_id, topic_id)`.
     * `DocumentSource` (`document_sources`): Provider observation table with `observed_url`, `normalized_observed_url`, and partial unique indexes (`uq_doc_sources_provider` and `uq_doc_sources_url_null_provider`) correctly resolving NULL `provider_doc_id` observation idempotency.
     * `DocumentSnapshot` (`document_snapshots`): Versioned representations with `UNIQUE(document_id, version_identifier, mime_type, content_hash)` and `ON DELETE RESTRICT` on `document_source_id` with ORM `passive_deletes=True`.
     * `BackgroundJob` (`background_jobs`): Execution telemetry with `UNIQUE(idempotency_key)`.
   * [`db/migrations/`](backend/intel_os/db/migrations/): Alembic migration environment with async multi-dialect support and `0001_g1_foundation` initial migration (vector extension active; unused `uuid-ossp` removed).
   * [`storage/local_cache.py`](backend/intel_os/storage/local_cache.py): `LocalCacheManager` enforcing `MAX_LOCAL_CACHE_GB` budget, LRU eviction (`prune()`), path traversal containment security checks, and safe error handling.
   * [`api/routes/`](backend/intel_os/api/routes/):
     * `GET /api/v1/health`: Liveness probe and async database connectivity check (returns 200 `healthy`/`connected` or 503 `degraded`/`disconnected`).
     * `GET /api/v1/status`: Version, environment, embedding dimension (768), and cache utilization metrics.
   * [`docker-compose.yml`](docker-compose.yml): Local PostgreSQL 16 + pgvector environment configuration.
   * [`.github/workflows/backend-ci.yml`](.github/workflows/backend-ci.yml): GitHub Actions CI pipeline running PostgreSQL 16 + pgvector container, full migration lifecycle, and complete 49-test suite.

2. **Automated Test Suite (`backend/tests/`)**:
   * 49 automated unit and integration tests executing across 12 test modules:
     * `test_config.py`: Settings defaults, environment overrides, validation (3 tests).
     * `test_db_lifecycle.py`: Engine creation, async session lifecycle, rollback on error, connectivity check (3 tests).
     * `test_models_crud.py`: CRUD, uniqueness constraints, cascade deletion on Topic and Document (7 tests).
     * `test_document_sources_idempotency.py`: NULL `provider_doc_id` edge cases (Tests A, B, C, D) (4 tests).
     * `test_snapshot_representations.py`: Multi-format snapshots (PDF vs HTML), duplicate byte rejection, `ON DELETE RESTRICT` provenance protection (4 tests).
     * `test_local_cache.py`: Cache usage, LRU pruning, path traversal security guardrails, clear (4 tests).
     * `test_api_health_status.py`: Health and status API endpoint integration (2 tests).
     * `test_alembic_migration.py`: Exact 7-table schema boundary verification, Alembic upgrade/downgrade/upgrade lifecycle cycle (4 tests).
     * `test_url_normalization.py`: Conservative, deterministic URL normalizer unit tests (6 tests).
     * `test_postgres_contract.py`: Real PostgreSQL 16 schema contract and DB introspection (4 tests).
     * `test_postgres_idempotency.py`: Real PostgreSQL 16 Scenarios A, B, C, D (4 tests).
     * `test_postgres_snapshots.py`: Real PostgreSQL 16 snapshot multi-format representations and provenance (4 tests).
   * **Test Result**: **49 passed in 5.42s (100% pass rate, 91% code coverage)**.

3. **Architecture Decision Records (ADRs)**:
   * `ADR-0014`: Partial Unique Index Strategy for Multi-Provider Observation Idempotency with NULL Identifiers.
   * `ADR-0015`: Snapshot-to-Observation Provenance Protection via ON DELETE RESTRICT and ORM Passive Deletes.
   * `ADR-0016`: PostgreSQL Native TEXT[] Arrays and Built-in gen_random_uuid() Schema Reconciliation.
   * `ADR-0017`: Deterministic URL Normalization & Idempotency Keying for Document Sources.

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

## 4. Tests Executed & Verification Results

### A. PostgreSQL 16 & Alembic Lifecycle
* **Container Service**: `pgvector/pgvector:pg16` on PostgreSQL 16.15.
* **Extensions**: `vector` active (`uuid-ossp` removed).
* **Alembic Upgrade Head**: Created exactly 7 application tables (`topics`, `sources`, `documents`, `document_topics`, `document_sources`, `document_snapshots`, `background_jobs`) + `alembic_version`.
* **Alembic Downgrade Base**: Cleanly dropped all 7 tables and custom ENUM types (`retention_tier`, `job_status`) with zero type leaks.
* **Second Alembic Upgrade Head**: Recreated tables and types flawlessly.

### B. Test Suite Metrics
* **Total Tests**: 49 passed / 0 failed.
* **Code Coverage**: 91% total backend coverage (723 statements, 68 missed).
* **Passing Test Modules**: 12/12 modules green.

---

## 5. Checkpoints

* **G0 Baseline Checkpoint**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **G0.1 Corrected Checkpoint**: `60abdbe65b88b2dd61e28d5419655b50c5fd94cb`
* **G0.2 Hardened Checkpoint**: `f95ddb8`
* **G1 Implementation Checkpoint**: `e07286b`
* **G1.1 Hardened Checkpoint**: `3f6e771`
* **G1.2 Final Checkpoint**: *(Tracked via Git commit)*
* **Working Tree**: Clean.

---

## 6. Exact Next Action

1. Await external mentor review for Gate 1 / Gate 1.1 / Gate 1.2 final evaluation.
2. Upon authorization, proceed to Gate 2: Ingestion Engine & Source Connector Framework.
3. **DO NOT START GATE 2 BEFORE MENTOR APPROVAL**.
