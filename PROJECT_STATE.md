# Intel OS / NCKH Intelligence Platform — Project State & Safety Checkpoint

## 1. Milestone Tracking

* **Current Milestone**: **Gate 2 (G2) — Academic Metadata Ingestion & Source Connector Framework**
* **Previous Milestones**:
  * **Gate 0 (G0)**: Score 77/100 | Status: REVISE
  * **Gate 0.1 (G0.1)**: Score 88/100 | Status: NEAR PASS
  * **Gate 0.2 (G0.2)**: APPROVED by External Mentor
  * **Gate 1 (G1)**: Score 82/100 | Revised through G1.1/G1.2
  * **Gate 1 Final**: APPROVED by External Mentor (~96/100)
  * **Gate 1.1**: Local PostgreSQL 16 hardening & URL idempotency completed
  * **Gate 1.2**: GitHub Actions green, unused UUID extension removed, state harmonized
  * **Gate 2 (G2)**: Academic Metadata Ingestion & Source Connector Framework Complete
* **G2 Completion Percentage**: **100%**
* **Active Working Branch**: `main`
* **Remote Repository**: `https://github.com/Phuchello/NCKH`
* **Status**: **G2 COMPLETED — Ready for Mentor Review & G3 Authorization**

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

This repository is **source-available proprietary** (see `LICENSE`, `NOTICE.md`, `docs/IP_POLICY.md`).

---

## 3. What Exists (G2 Deliverables)

1. **Academic Repository Connectors (`intel_os/connectors/`)**:
   * [`base.py`](backend/intel_os/connectors/base.py): `BaseConnector` abstract class with async streaming, pagination bounds, and session management.
   * [`arxiv.py`](backend/intel_os/connectors/arxiv.py): Official arXiv Atom 1.0 XML Query API connector with strict 3.0s minimum inter-request delay limiter and logical vs versioned identifier extraction.
   * [`crossref.py`](backend/intel_os/connectors/crossref.py): Official Crossref Works REST API connector with Polite Pool headers (`mailto`), JATS XML tag stripping, and cursor pagination.
   * [`openalex.py`](backend/intel_os/connectors/openalex.py): Official OpenAlex Works REST API connector with inverted-index abstract reconstruction, polite pool headers, and concept metadata.
   * [`semantic_scholar.py`](backend/intel_os/connectors/semantic_scholar.py): Official Semantic Scholar Graph API v1 connector with batch fetching, field projection, `externalIds` extraction, and API key rate limits.
   * [`smoke_test.py`](backend/intel_os/connectors/smoke_test.py): Optional on-demand live smoke test script (disabled by default in CI).
   * [`__init__.py`](backend/intel_os/connectors/__init__.py): Connector registry and `get_connector` factory helper.

2. **Resilient HTTP Transport Layer (`intel_os/http/`)**:
   * [`transport.py`](backend/intel_os/http/transport.py): `ResilientHttpClient` wrapping `httpx.AsyncClient` with bounded concurrency, connect/read/overall timeouts, automatic `Retry-After` header parsing (seconds & HTTP dates), exponential backoff with jitter, and sensitive credential redaction from all log outputs.
   * [`rate_limit.py`](backend/intel_os/http/rate_limit.py): Async token bucket (RPS mode) and minimum inter-request delay `RateLimiter` per provider.
   * [`retry.py`](backend/intel_os/http/retry.py): Exponential backoff delay calculation, status code filtering (429, 502, 503, 504), and `Retry-After` header parser.
   * [`network_safety.py`](backend/intel_os/http/network_safety.py): Pre-flight SSRF mitigation with URL scheme validation (`http`/`https` only, userinfo stripping), IP blocklist checking (loopback `127.0.0.0/8`, `::1`, RFC 1918 private subnets, cloud metadata `169.254.169.254`), and redirect hop validation.

3. **Ingestion & Reconciliation Engine (`intel_os/ingestion/`)**:
   * [`dto.py`](backend/intel_os/ingestion/dto.py): Strongly typed, provider-neutral `NormalizedDiscoveryRecord` Pydantic model.
   * [`identity.py`](backend/intel_os/ingestion/identity.py): Reusable canonical normalizers for DOIs (`normalize_doi`), arXiv logical identifiers (`normalize_arxiv_id`), version tags (`extract_arxiv_version`), and deterministic SHA-256 candidate fingerprints (`compute_metadata_fingerprint`).
   * [`reconciliation.py`](backend/intel_os/ingestion/reconciliation.py): Centralized `ReconciliationEngine` enforcing strict hard identity precedence (`DOI_EXACT` -> `ARXIV_ID_EXACT` -> `PROVIDER_DOC_ID` -> `CANONICAL_URL`). Candidate-only signals are never auto-merged, preventing false merges.
   * [`persistence.py`](backend/intel_os/ingestion/persistence.py): Atomic transactional database persistence linking documents, topics, and discrete `document_sources` observations with full re-ingestion idempotency.
   * [`service.py`](backend/intel_os/ingestion/service.py): `IngestionService` orchestrator executing bounded harvests, updating `BackgroundJob` execution telemetry (`records_seen`, `new_documents`, `matched_documents`, `observations_created`, `duration_seconds`), and recording failure messages.

4. **Automated Test Suite (`backend/tests/`)**:
   * 83 automated unit, mock HTTP, and PostgreSQL integration tests across 20 test modules:
     * `test_config.py`: Settings defaults, environment overrides, validation (3 tests).
     * `test_db_lifecycle.py`: Engine creation, async session lifecycle, rollback on error, connectivity check (3 tests).
     * `test_models_crud.py`: CRUD, uniqueness constraints, cascade deletion on Topic and Document (7 tests).
     * `test_document_sources_idempotency.py`: NULL `provider_doc_id` edge cases (4 tests).
     * `test_snapshot_representations.py`: Multi-format snapshots, duplicate byte rejection, ON DELETE RESTRICT (4 tests).
     * `test_local_cache.py`: Cache usage, LRU pruning, path traversal security guardrails (4 tests).
     * `test_api_health_status.py`: Health and status API endpoint integration (2 tests).
     * `test_alembic_migration.py`: Schema boundary verification, Alembic upgrade/downgrade/upgrade lifecycle (4 tests).
     * `test_url_normalization.py`: URL normalizer unit tests (6 tests).
     * `test_network_safety.py`: SSRF IP blocklist, URL syntax, userinfo rejection, literal IP URLs, redirect validation (6 tests).
     * `test_http_resilience.py`: Delay limiter, token bucket, Retry-After header parsing, backoff jitter, secret redaction, 429 retry, 404 immediate return (7 tests).
     * `test_identity_normalization.py`: DOI normalizer, arXiv ID coalescing, version extractor, metadata fingerprint (4 tests).
     * `test_connectors_arxiv.py`: Mock Atom XML feed parser, single ID fetch, malformed XML handling (3 tests).
     * `test_connectors_crossref.py`: JATS abstract cleaning, JSON parser, single DOI fetch (3 tests).
     * `test_connectors_openalex.py`: Inverted-index abstract reconstruction, search parser, single work fetch (3 tests).
     * `test_connectors_semantic_scholar.py`: S2 Graph API search, batch endpoint, externalIds extraction (2 tests).
     * `test_reconciliation_and_idempotency.py`: 3-provider same-DOI reconciliation, re-ingestion idempotency, arXiv version coalescence, candidate non-merge (3 tests).
     * `test_ingestion_service.py`: Service orchestration, bounds, telemetry tracking, error handling (2 tests).
     * `test_postgres_contract.py`: PostgreSQL 16 schema contract and DB introspection (4 tests).
     * `test_postgres_idempotency.py`: PostgreSQL 16 Scenarios A, B, C, D (4 tests).
     * `test_postgres_snapshots.py`: PostgreSQL 16 snapshot representations and provenance (4 tests).
     * `test_postgres_ingestion_integration.py`: Live multi-provider reconciliation and idempotency on PG16 (1 test).
   * **Test Result**: **83 passed / skipped cleanly when offline (100% pass rate, 87% code coverage)**.

5. **Architecture Decision Records (ADRs)**:
   * `ADR-0018`: Resilient Asynchronous HTTP Layer with Per-Provider Rate Limiting and SSRF Defense.
   * `ADR-0019`: Provider-Neutral Discovery DTO and Canonical Identifier Normalization.
   * `ADR-0020`: Hard Identity vs Candidate-Only Non-Merge Policy for Scholarly Document Deduplication.

---

## 4. What Does NOT Exist Yet (Strict Gate Boundaries)

To ensure disciplined execution, the following components are strictly deferred to subsequent gates:

* **No PDF extraction, full-text parsing, or section chunking** (Deferred to Gate 3).
* **No LLM extraction runners, prompt scripts, or OpenAI/Gemini execution calls** (Deferred to Gate 3).
* **No vector embedding generation or R2 object storage client** (Deferred to Gate 4).
* **No research gap mining or automated hypothesis generation code** (Deferred to Gate 5).
* **No hybrid search or RRF reranking** (Deferred to Gate 6).
* **No research handbook compilation or PDF/LaTeX generation code** (Deferred to Gate 7).
* **No Next.js UI frontend code or web components** (Deferred to Gate 8).
* **No message brokers (Celery/Redis/Kafka)** (Strictly avoided; uses lightweight `background_jobs` table).

---

## 5. Checkpoints

* **G0 Baseline**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **G0.1 Corrected**: `60abdbe65b88b2dd61e28d5419655b50c5fd94cb`
* **G0.2 Hardened**: `f95ddb8`
* **G1 Implementation**: `e07286b`
* **G1.1 Hardened**: `3f6e771`
* **G1.2 Final Engineering Checkpoint**: `d164b3f`
* **Public IP Boundary Merge**: `a4cf623`
* **G2 Implementation Checkpoint**: `6223fc0`

---

## 6. Exact Next Action

1. Commit and push Gate 2 deliverables to GitHub (`origin/main`).
2. Verify GitHub Actions CI run completes **GREEN** (`conclusion: success`).
3. Present final Gate 2 implementation report to user/mentor.
4. Await external mentor review for Gate 3 authorization.
5. **DO NOT START GATE 3 BEFORE MENTOR APPROVAL**.
