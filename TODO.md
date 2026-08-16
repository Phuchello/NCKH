# Intel OS / NCKH Intelligence Platform — Engineering Task Backlog

## Gate 0 / Gate 0.1: Foundation, Architecture & Specification Baseline [COMPLETED]
- [x] Initial G0 repository initialization and remote connection (`Phuchello/NCKH`).
- [x] G0.1 Architectural Corrections based on Mentor Audit:
  - [x] Fix Topic Cardinality: Replaced 1:N with Many-to-Many `document_topics` table.
  - [x] Separate Identity Fingerprint from Content Hash: `metadata_fingerprint` for DISCOVERED tier; `content_hash` on snapshots only.
  - [x] Document Version / Snapshot Model: Created `document_snapshots` with version identifiers and S3 keys.
  - [x] Multi-Provider Reconciliation: Introduced `document_sources` for provider observations with canonical identity precedence.
  - [x] Repair Embedding Model Contract: Established versioned 768-dim contract for V1 schema and migration protocol.
  - [x] Reconcile Schema References: Standardized exact 18-table normalized DDL across all documents.
  - [x] Fix Scientific Epistemology: Decoupled Grounding (`VERBATIM_MATCH`), Claim Type, Epistemic Status (default `UNASSESSED`), and Evidence Quality.
  - [x] Fix Scoring Language: Renamed novelty to Semantic Distinctiveness Signal and marked all formulas PROVISIONAL.
  - [x] Fix Search Terminology: Standardized on "PostgreSQL full-text lexical retrieval" (`tsvector`/`tsquery`).
  - [x] Calibrate Security Language: Replaced absolute claims with defense-in-depth and threat mitigation framing.
- [x] Full Cross-Document Consistency Audit across all 14 specification files.
- [x] Commit and push G0.1 checkpoint to GitHub.
- [x] Request mentor review before starting Gate 1.

---

## Gate 1: Database Foundation & Backend Scaffolding [COMPLETED]
- [x] Backend Scaffolding:
  - [x] Python project structure with `pyproject.toml` (Python 3.11+, FastAPI, SQLAlchemy 2.x async, asyncpg, Alembic, Pydantic v2, pydantic-settings).
  - [x] Asynchronous database engine setup (`intel_os.db.session`) with connection pooling, transaction boundaries, and health connectivity check.
  - [x] Alembic migration environment configured for PostgreSQL 16+, extensions (`vector`), and async/sync multi-dialect support.
  - [x] Initial database migration (`0001_g1_foundation`) generating the 7 G1 foundation tables (`topics`, `sources`, `documents`, `document_topics`, `document_sources`, `document_snapshots`, `background_jobs`).
  - [x] Partial unique index strategy for `document_sources` resolving NULL `provider_doc_id` observation idempotency.
  - [x] Snapshot-to-observation provenance protection with `ON DELETE RESTRICT` and `passive_deletes=True`.
  - [x] Snapshot multi-format representation support (PDF vs HTML) and byte-level deduplication.
  - [x] Bounded local cache manager (`LocalCacheManager`) enforcing `MAX_LOCAL_CACHE_GB` quota with LRU eviction and path traversal security guardrails.
  - [x] Basic health check and telemetry API routes (`GET /api/v1/health`, `GET /api/v1/status`).
  - [x] Comprehensive pytest test suite (30 unit/integration tests with 87% coverage across settings, DB lifecycle, CRUD, idempotency, representations, cache, and API).

---

## Gate 1.1: PostgreSQL Reality Check & Schema Alignment [COMPLETED]
- [x] Real PostgreSQL 16 Testing:
  - [x] Boots PostgreSQL 16 + pgvector container via standard `docker compose up -d`.
  - [x] Created isolated test database (`intel_os_test`) with safety guard refusing execution against non-test databases.
  - [x] Executed and verified real PostgreSQL Alembic upgrade/downgrade/upgrade cycle (`upgrade head` -> `downgrade base` -> `upgrade head`).
- [x] Enum Lifecycle Fix:
  - [x] Controlled ENUM type creation on PostgreSQL for `retention_tier` and `job_status` with zero duplicate type collisions or leaks.
- [x] Schema & Docs Reconciliation:
  - [x] Standardized `topics.keywords` and `documents.authors` as native PostgreSQL `TEXT[]` (`ARRAY(String)`) with SQLite `JSON` fallback.
  - [x] Adopted built-in `gen_random_uuid()` database server defaults and application-level `uuid.uuid4`.
  - [x] Guaranteed complete alignment: `DOCS == ORM == ALEMBIC == ACTUAL POSTGRES SCHEMA`.
- [x] Normalized Observed URL & Idempotency:
  - [x] Implemented conservative deterministic URL normalizer (`intel_os.core.url.normalize_url`).
  - [x] Separated verbatim `observed_url` from canonical `normalized_observed_url`.
  - [x] Verified partial unique index `uq_doc_sources_url_null_provider` on real PostgreSQL with scenarios A, B, C, D.
- [x] Contract & Provenance Test Suite:
  - [x] Added PostgreSQL database introspection and contract tests (`test_postgres_contract.py`).
  - [x] Added PostgreSQL idempotency tests (`test_postgres_idempotency.py`).
  - [x] Added PostgreSQL snapshot provenance and representation tests (`test_postgres_snapshots.py`).
  - [x] Added URL normalizer unit tests (`test_url_normalization.py`).

---

## Gate 1.2: CI Green & Final Cleanup [COMPLETED]
- [x] CI Pipeline Reliability:
  - [x] Eliminated external action policy risk by replacing `astral-sh/setup-uv@v2` with official `actions/checkout@v4` and `actions/setup-python@v5`.
  - [x] Installed `uv` directly via `pip` on standard Python 3.11 runner.
  - [x] Added automated PostgreSQL 16 service container (`pgvector/pgvector:pg16`) with health checks.
  - [x] Automated full Alembic migration verification (`upgrade head` -> `downgrade base` -> `upgrade head`) in CI.
  - [x] Automated full 49-test suite (Unit + PostgreSQL 16 Integration) in CI.
- [x] Cleanup & Hardening:
  - [x] Removed unused `uuid-ossp` extension creation from migrations, tests, and target DDL.
  - [x] Aligned `test_postgres_alembic_lifecycle` to run without optional `psycopg2` driver dependency.
  - [x] Refreshed `PROJECT_STATE.md` with internally consistent Gate 1.2 deliverables and test metrics.

---

## Gate 2: Ingestion Engine & Source Connector Framework [COMPLETED]
- [x] Ingestion Architecture:
  - [x] Base connector interface (`BaseConnector`) with rate limiting, async streaming, and bounded pagination.
  - [x] 4 Academic connectors implemented and verified against official API policies:
    - [x] arXiv: Atom XML query API, 3-second politeness limiter, canonical logical vs versioned ID handling.
    - [x] Crossref: Works REST API, polite pool identification headers, JATS XML abstract cleaning, cursor paging.
    - [x] OpenAlex: Works REST API, polite pool headers, inverted-index abstract reconstruction, concepts.
    - [x] Semantic Scholar: Academic Graph API v1, batch fetching, externalIds mapping, 429 Retry-After handling.
  - [x] Shared HTTP Transport & Resilience (`intel_os.http`):
    - [x] `ResilientHttpClient` with timeouts, exponential backoff, jitter, and Retry-After header parsing (numeric & HTTP dates).
    - [x] Token bucket and minimum delay `RateLimiter` per provider.
    - [x] Sensitive header/key redaction in all logging outputs.
  - [x] Network Safety & SSRF Mitigation (`intel_os.http.network_safety`):
    - [x] Pre-flight URL scheme validation (`http`/`https` only, userinfo rejection).
    - [x] IP blocklist checking (loopback `127.0.0.0/8`, `::1`, RFC 1918 private networks, link-local `169.254.169.254`).
    - [x] Redirect hop validation with maximum hop cap (3 hops).
  - [x] Normalized Discovery DTO (`NormalizedDiscoveryRecord`) provider-neutral Pydantic model.
  - [x] Centralized Identity Normalization (`intel_os.ingestion.identity`):
    - [x] `normalize_doi` canonical lowercasing and URL stripping.
    - [x] `normalize_arxiv_id` logical identifier coalescence.
    - [x] `extract_arxiv_version` version extraction.
    - [x] `compute_metadata_fingerprint` deterministic SHA-256 computation.
  - [x] Multi-Provider Reconciliation & Idempotency:
    - [x] Hard identity matching (DOI, logical arXiv ID, provider doc ID, canonical URL).
    - [x] Candidate-only non-merge preservation (metadata fingerprints NEVER silently merge).
    - [x] Cross-provider same-DOI 3-source test passes (1 Document, 3 Sources).
    - [x] Re-ingestion idempotency test passes (0 duplicate rows created).
  - [x] Ingestion Service & Telemetry:
    - [x] `IngestionService` coordinating harvest runs, bounds (`max_records`), and `BackgroundJob` telemetry.
  - [x] Comprehensive Automated Test Suite (83 total unit, mock HTTP, and PostgreSQL integration tests).

---

## Gate 3: Text Processing, Normalization & Extraction Pipeline
- [ ] Processing Subsystem:
  - [ ] Robust PDF parser supporting multi-column layouts, tables, and references (pdfplumber/PyPDF).
  - [ ] HTML article cleaner and markdown converter with boilerplate removal.
  - [ ] Section splitter (Abstract, Methodology, Results, Limitations, Future Work).
  - [ ] Representation snapshot manager populating `document_snapshots`.
  - [ ] Replaceable LLM Provider Gateway supporting Gemini, Claude, and OpenAI with structured Pydantic schemas.
  - [ ] Atomic claim and empirical evidence extractor with verbatim quote bounding and default `epistemic_status = 'UNASSESSED'`.

---

## Gate 4: Intelligence Lake & Personal Research Memory Storage
- [ ] Memory Engine:
  - [ ] S3-compatible Object Storage manager for high-value raw artifact retention (`RETAINED` tier).
  - [ ] Multi-topic mapping manager with relevance scoring (`document_topics`).
  - [ ] Structured persistence for verified claims, evidence items, and claim relationships.
  - [ ] pgvector chunk and claim embedding generator (768-dim contract) with HNSW cosine index.
  - [ ] Personal Research Memory CRUD APIs for user notes, observation logs, and experiment notes.

---

## Gate 5: Research Opportunity Miner (Gaps, Contradictions, Lineage)
- [ ] Opportunity Subsystem:
  - [ ] Research gap detection algorithm analyzing unaddressed limitations and open questions.
  - [ ] Scientific contradiction detector identifying opposing claims across publications.
  - [ ] Semantic distinctiveness signal calculator comparing candidate ideas against retrieved prior art.
  - [ ] Candidate research idea and hypothesis generator with feasibility scoring.
  - [ ] Provenance graph builder establishing snapshot-pinned backward and forward Idea Lineage links.

---

## Gate 6: Core Search, Retrieval & Synthesis API
- [ ] Retrieval Subsystem:
  - [ ] Hybrid search engine combining PostgreSQL full-text lexical search and pgvector semantic retrieval.
  - [ ] Reciprocal Rank Fusion (RRF) and context grounding builder.
  - [ ] Provenance-constrained synthesis engine producing literature review matrices and state-of-the-art summaries.
  - [ ] Citation-backed Q&A endpoint with snapshot verification.

---

## Gate 7: Research Handbook & Output Generation
- [ ] Output Subsystem:
  - [ ] Automated Scientific Research Handbook generator synthesizing topic intelligence.
  - [ ] Markdown, LaTeX, and PDF export engines with verified bibliographic citations.
  - [ ] Research project blueprint generator (Hypothesis, Methodology, Resource Requirements, Timeline).
  - [ ] Export verification suite auditing citation integrity.

---

## Gate 8: Web UI / Next.js Research Console
- [ ] Frontend Workbench:
  - [ ] Next.js 15+ App Router application with responsive research-centric interface.
  - [ ] Intelligence Dashboard: Topic feeds, recent discoveries, opportunity alerts.
  - [ ] Idea Lineage Visualizer: Interactive node-link graph of ideas, gaps, claims, and paper snapshots.
  - [ ] Research Memory Workbench: Personal notes, claim verification explorer, hypothesis tracker.
  - [ ] Ingestion & Job Monitor: Real-time crawl logs, storage quota gauges, retention metrics.

---

## Gate 9: Security Hardening, Observability & Evaluation
- [ ] Enterprise Hardening:
  - [ ] SSRF defense test suite against private IP spaces and metadata services.
  - [ ] Prompt injection fuzz testing across malicious academic PDF test fixtures.
  - [ ] Empirical calibration of multi-factor scoring model weights.
  - [ ] Retrieval accuracy benchmark (MRR@10, NDCG@10).
  - [ ] Codex engineering audit for concurrency, idempotency, and database performance.

---

## Gate 10: Production Release, Cold Archival & Gate 10 Sign-off
- [ ] Production Readiness:
  - [ ] Cloudflare R2 migration & production deployment runbooks.
  - [ ] Automated database backup & cold archival export scripts to external storage.
  - [ ] Complete developer documentation and user manual.
  - [ ] Final architecture sign-off and mentor review.
