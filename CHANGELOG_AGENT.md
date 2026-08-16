# AI Agent Activity & Engineering Changelog

This document tracks all engineering actions, gate transitions, and architectural evolutions executed by autonomous AI pair programmers across the **Intel OS / NCKH Intelligence Platform** repository.

---

## Format Standard
Each entry must record:
* **Date & Timestamp**: UTC timestamp
* **Milestone / Gate**: Current gate identifier
* **Agent Role**: Gemini / Antigravity vs Codex
* **Action Summary**: High-level objective completed
* **Files Modified / Created**: Explicit file paths
* **Decisions & Rationale**: Key architectural decisions implemented
* **Verification Performed**: Tests and consistency checks executed

---

## Entries

### [2026-08-16 01:30:00 UTC] — Gate 1 (G1) Database Foundation & Backend Scaffolding
* **Milestone**: Gate 1 (G1)
* **Agent Role**: Antigravity (Gemini)
* **Action Summary**:
  * Built complete, executable Python backend scaffolding under `backend/intel_os`.
  * Configured strongly typed Settings using `pydantic-settings` with safe development defaults and validation.
  * Implemented asynchronous database engine and session management with connection pooling, transaction boundaries, and health check.
  * Authored SQLAlchemy 2.x declarative models for the exact 7 G1 foundation tables (`Topic`, `Source`, `Document`, `DocumentTopic`, `DocumentSource`, `DocumentSnapshot`, `BackgroundJob`).
  * Enforced candidate-only semantics on `metadata_fingerprint` (indexed, NOT unique).
  * Resolved the multi-provider observation NULL `provider_doc_id` edge case via two partial unique indexes (`uq_doc_sources_provider` and `uq_doc_sources_url_null_provider`).
  * Protected snapshot-to-source provenance with `ON DELETE RESTRICT` and ORM `passive_deletes=True`.
  * Supported multi-format snapshots (PDF vs HTML) per version with exact-byte deduplication.
  * Created initial Alembic migration (`0001_g1_foundation`) generating the 7 foundation tables with extensions and enum types.
  * Implemented `LocalCacheManager` with `MAX_LOCAL_CACHE_GB` quota, LRU eviction, and path traversal security guardrails.
  * Created FastAPI service with lifespan lifecycle and endpoints (`GET /api/v1/health`, `GET /api/v1/status`).
  * Created comprehensive pytest test suite (30 tests, 87% coverage).
* **Files Created**:
  * `backend/pyproject.toml`, `backend/alembic.ini`, `backend/README.md`, `docker-compose.yml`
  * `backend/intel_os/__init__.py`, `backend/intel_os/main.py`
  * `backend/intel_os/core/__init__.py`, `backend/intel_os/core/config.py`, `backend/intel_os/core/logging.py`
  * `backend/intel_os/db/__init__.py`, `backend/intel_os/db/base.py`, `backend/intel_os/db/session.py`
  * `backend/intel_os/db/models/__init__.py`, `enums.py`, `topic.py`, `source.py`, `document.py`, `document_topic.py`, `document_source.py`, `document_snapshot.py`, `background_job.py`
  * `backend/intel_os/db/migrations/env.py`, `script.py.mako`, `versions/20260816_0001_g1_foundation.py`
  * `backend/intel_os/api/__init__.py`, `router.py`, `routes/__init__.py`, `routes/health.py`, `routes/status.py`
  * `backend/intel_os/storage/__init__.py`, `storage/local_cache.py`
  * `backend/tests/__init__.py`, `conftest.py`, `test_config.py`, `test_db_lifecycle.py`, `test_models_crud.py`, `test_document_sources_idempotency.py`, `test_snapshot_representations.py`, `test_local_cache.py`, `test_api_health_status.py`, `test_alembic_migration.py`
* **Files Modified**:
  * `docs/DATA_MODEL.md`, `DECISIONS.md` (ADR-0014, ADR-0015), `TODO.md`, `PROJECT_STATE.md`
* **Verification**:
  * 30/30 automated pytest tests passing (100% pass rate, 87% coverage).
  * Alembic migration upgrade / downgrade / upgrade cycle verified.
  * Zero G2+ feature code introduced.
* **Status**: G1 Completed. Checkpoint ready for mentor review.

---

### [2026-08-16 01:15:00 UTC] — Gate 0.2 (G0.2) Data-Integrity Hardening Pass
* **Milestone**: Gate 0.2 (G0.2)
* **Agent Role**: Antigravity (Gemini)
* **Action Summary**:
  * Performed final data-integrity hardening following mentor re-audit (G0: 77/100, G0.1: 88/100, Status: NEAR PASS).
  * **Snapshot-Pinned Provenance**: Enforced `snapshot_id NOT NULL` on `claims`, `evidence_items`, `idea_provenance`, `document_chunks`. Changed `ON DELETE SET NULL` to `ON DELETE RESTRICT` on `claims`, `evidence_items`, and `idea_provenance` to prevent silent provenance destruction.
  * **Snapshot → Source Linkage**: Added `document_source_id` FK on `document_snapshots` to record which provider observation triggered the fetch, completing the lineage chain Source → Observation → Snapshot → Claims.
  * **Confidence-Based Reconciliation**: Added `match_method` and `match_confidence` columns to `document_sources`. Classified identity signals into Hard (DOI, arXiv ID), Strong (Canonical URL), and Candidate (Metadata Fingerprint) tiers with explicit reconciliation policy: false merge > temporary duplication.
  * **NULLS NOT DISTINCT**: Changed `document_sources` unique constraint to `UNIQUE NULLS NOT DISTINCT (document_id, source_id, provider_doc_id)` for correct NULL handling on PostgreSQL 16+.
  * **Snapshot Identity Broadening**: Changed `document_snapshots` unique constraint from `(document_id, version_identifier)` to `(document_id, version_identifier, mime_type, content_hash)` to support multiple representations of the same version.
  * **Gate-Staged Migrations**: Formally split 18 tables across G1 Foundation (7 tables), G3/G4 Extraction (5 tables), G5 Opportunity (6 tables) with explicit staging matrix.
  * **ADR-0011 through ADR-0013**: Recorded architectural decisions for snapshot provenance enforcement, confidence-based reconciliation, and staged migrations.
* **Files Modified**:
  * `README.md`
  * `DECISIONS.md` (ADR-0011, ADR-0012, ADR-0013)
  * `CHANGELOG_AGENT.md`
  * `PROJECT_STATE.md`
  * `docs/DATA_MODEL.md` (primary rewrite)
  * `docs/PIPELINE.md`
  * `docs/MILESTONES.md`
  * `docs/ARCHITECTURE_DETAILED.md`
  * `docs/INTELLIGENCE_MODEL.md`
  * `docs/PRODUCT_SPEC.md`
* **Verification**:
  * Full cross-document audit confirming schema, column names, constraint types, and provenance invariants are consistent across all 14+ specification files.
  * Zero application feature code introduced.
* **Status**: G0.2 Completed. Checkpoint ready for mentor re-audit.

---

### [2026-08-16 01:05:00 UTC] — Gate 0.1 (G0.1) Architecture Correction Pass
* **Milestone**: Gate 0.1 (G0.1)
* **Agent Role**: Antigravity (Gemini)
* **Action Summary**:
  * Performed comprehensive architectural repair and specification hardening following the external mentor G0 audit (Score: 77/100, Status: REVISE).
  * **Topic Cardinality**: Replaced 1:N topic ownership with many-to-many junction `document_topics` and made sources globally reusable.
  * **Identity vs Content Hash**: Separated `metadata_fingerprint` (for `DISCOVERED` tier) from `content_hash` (for fetched `document_snapshots` representations).
  * **Document Snapshot Model**: Introduced `document_snapshots` table to track representation versions (e.g. arXiv revisions) and pin claims to exact source versions.
  * **Multi-Provider Reconciliation**: Introduced `document_sources` to track multi-provider discovery provenance while reconciling into a single logical `Document`.
  * **Embedding Model Contract**: Established fixed 768-dimensional vector contract for V1 schema, decoupled from replaceable reasoning LLM providers, with a documented migration protocol.
  * **Schema Reconciliation**: Harmonized all documentation to reference the exact 18 normalized PostgreSQL tables.
  * **Scientific Epistemology**: Decoupled Grounding Status (`VERBATIM_MATCH`), Claim Type, Epistemic Status (default `UNASSESSED`), and Evidence Quality. Verbatim quotes validate presence, not scientific truth.
  * **Scoring Model Calibration**: Renamed novelty to Semantic Distinctiveness Signal and marked all scoring formulas/weights as PROVISIONAL pending G9 calibration.
  * **Search Terminology**: Corrected "BM25" references to "PostgreSQL full-text lexical retrieval (`tsvector`/`tsquery`)".
  * **Security Wording**: Calibrated security claims to defense-in-depth and risk reduction framing.
* **Files Modified**:
  * `README.md`
  * `ARCHITECTURE.md`
  * `DECISIONS.md`
  * `TODO.md`
  * `CHANGELOG_AGENT.md`
  * `PROJECT_STATE.md`
  * `.env.example`
  * `docs/PRODUCT_SPEC.md`
  * `docs/ARCHITECTURE_DETAILED.md`
  * `docs/DATA_MODEL.md`
  * `docs/PIPELINE.md`
  * `docs/MILESTONES.md`
  * `docs/SECURITY_MODEL.md`
  * `docs/SCORING_MODEL.md`
  * `docs/INTELLIGENCE_MODEL.md`
* **Verification**:
  * Full cross-document audit confirming 100% internal consistency across all 14 specification files and `.env.example`.
  * Zero application feature code introduced.
* **Status**: G0.1 Completed. Checkpoint ready for mentor re-audit.

---

### [2026-08-16 00:50:00 UTC] — Gate 0 (G0) Foundation & Architecture Baseline
* **Milestone**: Gate 0 (G0)
* **Agent Role**: Antigravity (Gemini)
* **Action Summary**:
  * Initialized local git repository, connected cleanly to remote `Phuchello/NCKH` on branch `main`.
  * Authored initial G0 architectural specification suite covering all 14 foundational documents.
  * Modeled three durable intellectual assets: Intelligence Lake, Personal Research Memory, and Research Opportunity Memory.
* **Commit**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **Status**: G0 Initial Submission (Scored 77/100, Proceeded to G0.1).
