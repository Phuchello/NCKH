# Intel OS / NCKH Intelligence Platform — Project State & Safety Checkpoint

## 1. Milestone Tracking

* **Current Milestone**: **Gate 2 (G2) — Academic Ingestion & Connector Framework**
* **Previous Milestones**:
  * **Gate 0 (G0)**: Score 77/100 | Status: REVISE
  * **Gate 0.1 (G0.1)**: Score 88/100 | Status: NEAR PASS
  * **Gate 0.2 (G0.2)**: APPROVED by External Mentor
  * **Gate 1 (G1)**: Initial score 82/100 | Revised through G1.1/G1.2
  * **Gate 1 Final**: APPROVED by External Mentor (~96/100)
  * **Gate 1.1**: Local PostgreSQL 16 hardening & URL idempotency completed
  * **Gate 1.2**: GitHub Actions green, unused UUID extension removed, state harmonized
* **G1 Completion Percentage**: **100% — APPROVED**
* **G2 Engineering Authorization**: **AUTHORIZED**
* **G2 Repository Authorization**: **PRIVATE CORE ONLY — PUBLIC REPO HOLD**
* **Active Public Repository**: `https://github.com/Phuchello/NCKH`
* **Public Repository Role**: **Public Showcase / Source-Available Proprietary**
* **Status**: **G2 PAUSED IN PUBLIC REPO UNTIL PRIVATE CORE REPOSITORY IS ESTABLISHED**

---

## 2. Intellectual Property Boundary

Effective 2026-08-16, the project follows a **Public Showcase + Private Core** model.

### Public repository — `Phuchello/NCKH`

Intended for:

- product vision and high-level architecture;
- milestone/status information;
- public research outputs;
- sanitized documentation and demonstrations;
- selected public results and benchmarks;
- intentionally disclosed non-sensitive artifacts.

This repository is **not open source**. See:

- `LICENSE`
- `NOTICE.md`
- `docs/IP_POLICY.md`

### Private core repository

Required for authoritative G2+ proprietary implementation, including:

- ingestion/reconciliation internals;
- proprietary intelligence/scoring/reasoning logic;
- prompt libraries;
- Research Memory / Opportunity Memory private data;
- unpublished research ideas, experiments, and datasets;
- future novel algorithms and commercially sensitive implementation.

**G0/G1 history was already publicly disclosed and must be treated as disclosed. Do not rewrite history to imply otherwise.**

Public Issue #3 is now only the public G2 milestone mirror. Public Issue #5 tracks private-core setup.

---

## 3. What Exists — Approved G1 Baseline

1. **Executable Backend Architecture (`backend/intel_os`)**:
   * FastAPI application foundation and lifecycle management.
   * Strongly typed Pydantic settings and structured logging.
   * Conservative deterministic URL normalization.
   * SQLAlchemy 2.x async engine/session lifecycle.
   * Exactly 7 G1 foundation tables:
     * `topics`
     * `sources`
     * `documents`
     * `document_topics`
     * `document_sources`
     * `document_snapshots`
     * `background_jobs`
   * Provider observation idempotency using normalized URLs and partial unique indexes.
   * Snapshot provenance protection with `ON DELETE RESTRICT`.
   * Alembic migration lifecycle verified on PostgreSQL 16.
   * Bounded local cache manager.
   * `/api/v1/health` and `/api/v1/status`.
   * Docker Compose PostgreSQL 16 + pgvector development environment.
   * GitHub Actions PostgreSQL 16 + pgvector CI pipeline.

2. **Automated Test Suite**:
   * 49 tests passed / 0 failed.
   * 91% backend coverage.
   * SQLite fast unit tests retained where useful.
   * Real PostgreSQL 16 integration/contract tests included.

3. **Architecture Decision Records**:
   * ADR-0014: partial unique indexes for provider observation idempotency.
   * ADR-0015: snapshot-to-observation provenance protection.
   * ADR-0016: PostgreSQL native arrays + `gen_random_uuid()` schema reconciliation.
   * ADR-0017: deterministic URL normalization and observation idempotency keying.

---

## 4. What Does NOT Exist Yet

The following remain intentionally deferred:

* no authoritative G2 academic connector implementation in the public repository;
* no live crawler fleet;
* no LLM extraction runners;
* no vector embedding generation pipeline;
* no R2/object-storage production client;
* no research gap mining or automated hypothesis generation;
* no hybrid search/RRF reranking;
* no research handbook generation engine;
* no frontend product implementation;
* no custom model training/fine-tuning pipeline.

---

## 5. Verification Baseline

### PostgreSQL 16 & Alembic

* PostgreSQL 16 + pgvector verified.
* Exactly 7 application tables + `alembic_version`.
* `alembic upgrade head` succeeded.
* `alembic downgrade base` succeeded with zero enum-type leaks.
* second `alembic upgrade head` succeeded.

### Tests

* **49 passed / 0 failed**.
* **91% backend coverage**.

### GitHub Actions

* Workflow: `Backend CI`
* Verified green run: `31920328660` on final state-update HEAD, with actual PostgreSQL 16 + pgvector job execution.
* Migration lifecycle step: success.
* Full unit + PostgreSQL integration suite: success.

---

## 6. Checkpoints

* **G0 Baseline**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **G0.1 Corrected**: `60abdbe65b88b2dd61e28d5419655b50c5fd94cb`
* **G0.2 Hardened**: `f95ddb8`
* **G1 Implementation**: `e07286b`
* **G1.1 Hardened**: `3f6e771`
* **G1.2 Final Engineering Checkpoint**: `d164b3f`
* **G1 Final State Update**: `52e7300`
* **Public IP Boundary Merge**: `cc0a436`

---

## 7. Exact Next Action

1. Create a **private** repository under `Phuchello` for the authoritative core (recommended working name: `NCKH-core-private`).
2. Verify the repository is PRIVATE before migrating/adding G2 implementation.
3. Seed the private repository from the approved G1 baseline as appropriate.
4. Carry over proprietary license/IP governance and secret exclusions.
5. Move/mirror the detailed G2 engineering task into the private repository.
6. Resume Gemini/Antigravity G2 implementation **only in the private core repository**.
7. Keep `Phuchello/NCKH` as the public showcase/documentation surface.

**DO NOT START G2 CORE IMPLEMENTATION IN THE PUBLIC REPOSITORY.**
