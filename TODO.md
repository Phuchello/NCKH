# Intel OS / NCKH Intelligence Platform — Engineering Task Backlog

## Gate 0: Foundation, Architecture & Specification Baseline [COMPLETED]
- [x] Initialize Git repository cleanly tracking `Phuchello/NCKH`.
- [x] Authoritative G0 architectural specifications:
  - [x] `README.md` (System overview, 3 assets, provenance chain)
  - [x] `PROJECT_STATE.md` (State checkpoint, metrics, safety boundaries)
  - [x] `TODO.md` (Engineering backlog G0–G10)
  - [x] `DECISIONS.md` (ADRs 0001–0008)
  - [x] `ARCHITECTURE.md` (System architecture, topology, retention funnel)
  - [x] `CHANGELOG_AGENT.md` (Agent audit trail)
  - [x] `docs/PRODUCT_SPEC.md` (Vision, user personas, epics, non-goals)
  - [x] `docs/ARCHITECTURE_DETAILED.md` (Subsystems, connectors, worker model)
  - [x] `docs/DATA_MODEL.md` (SQL DDL schema, pgvector definitions, lineage queries)
  - [x] `docs/PIPELINE.md` (End-to-end 8-stage data pipeline & retention tiers)
  - [x] `docs/MILESTONES.md` (Comprehensive G0–G10 roadmap & acceptance criteria)
  - [x] `docs/SECURITY_MODEL.md` (Threat matrix, SSRF defenses, prompt injection guards)
  - [x] `docs/SCORING_MODEL.md` (Mathematical scoring formulations & weighting)
  - [x] `docs/INTELLIGENCE_MODEL.md` (Epistemic states, opportunity mechanics, lineage)
- [x] Environment configuration template (`.env.example`) & `.gitignore`.
- [x] Commit and push G0 checkpoint to GitHub.
- [x] Request mentor review before starting Gate 1.

---

## Gate 1: Environment Setup, Database & Backend Core Scaffolding [UPCOMING]
- [ ] Backend Scaffolding:
  - [ ] Python project structure with `pyproject.toml` / `requirements.txt` (FastAPI, SQLAlchemy, asyncpg, pgvector, Pydantic v2, Alembic).
  - [ ] Asynchronous database engine setup with connection pooling.
  - [ ] Alembic migration environment configured for PostgreSQL 16+ and pgvector.
  - [ ] Initial database migration generating tables defined in `docs/DATA_MODEL.md`.
  - [ ] Bounded local cache manager enforcing `MAX_LOCAL_CACHE_GB` quota.
  - [ ] Basic health check and telemetry API routes (`/api/v1/health`, `/api/v1/status`).
  - [ ] Unit testing harness with `pytest` and `pytest-asyncio`.

---

## Gate 2: Ingestion Engine & Source Connector Framework
- [ ] Ingestion Architecture:
  - [ ] Base connector interface (`BaseConnector`) with rate limiting and retry logic.
  - [ ] Academic connectors: arXiv API / RSS, Semantic Scholar API, Crossref API, OpenAlex.
  - [ ] Web & General crawler connector with `robots.txt` compliance and SSRF validation.
  - [ ] Content fingerprinting and deduplication engine using SHA-256 and DOI normalization.
  - [ ] Tier 1 Filter: Fast metadata classification to assign initial retention tier (`DISCOVERED` vs `INDEXED`).
  - [ ] Asynchronous ingestion job queue with transactional state logging.

---

## Gate 3: Text Processing, Normalization & Extraction Pipeline
- [ ] Processing Subsystem:
  - [ ] Robust PDF parser supporting multi-column layouts, tables, and references (pdfplumber/PyPDF).
  - [ ] HTML article cleaner and markdown converter with boilerplate removal.
  - [ ] Structural section splitter (Abstract, Background, Methodology, Results, Discussion, Limitations).
  - [ ] LLM Provider Gateway supporting Gemini, Claude, and OpenAI with structured JSON schemas.
  - [ ] Atomic claim and empirical evidence extractor with verbatim quote bounding.
  - [ ] Claim verification engine comparing extracted statements against source text.

---

## Gate 4: Intelligence Lake & Personal Research Memory Storage
- [ ] Memory Engine:
  - [ ] S3-compatible Object Storage manager for high-value raw artifact retention (`RETAINED` tier).
  - [ ] Topic and Domain taxonomy manager with hierarchical tagging.
  - [ ] Structured persistence for verified claims, evidence items, and entity relationships.
  - [ ] pgvector chunk and claim embedding generator with cosine similarity index.
  - [ ] Personal Research Memory CRUD APIs for user notes, observation logs, and experiment notes.
  - [ ] Entity resolution engine linking identical concepts across multiple papers.

---

## Gate 5: Research Opportunity Miner (Gaps, Contradictions, Lineage)
- [ ] Opportunity Subsystem:
  - [ ] Research gap detection algorithm analyzing unaddressed limitations and open questions.
  - [ ] Scientific contradiction detector identifying opposing claims across publications.
  - [ ] Emerging trend analyzer calculating velocity across topics and preprint keywords.
  - [ ] Candidate research idea and hypothesis generator with feasibility and novelty scoring.
  - [ ] Provenance graph builder establishing full backward and forward Idea Lineage links.

---

## Gate 6: Core Search, Retrieval & Synthesis API
- [ ] Retrieval Subsystem:
  - [ ] Hybrid search engine combining PostgreSQL full-text search (BM25) and pgvector semantic retrieval.
  - [ ] Reciprocal Rank Fusion (RRF) and cross-encoder reranking.
  - [ ] Provenance-constrained synthesis engine producing literature review matrices and state-of-the-art summaries.
  - [ ] Citation-backed Q&A endpoint guaranteeing zero-hallucination factual grounding.

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
  - [ ] Idea Lineage Visualizer: Interactive node-link graph of ideas, gaps, claims, and papers.
  - [ ] Research Memory Workbench: Personal notes, claim verification explorer, hypothesis tracker.
  - [ ] Ingestion & Job Monitor: Real-time crawl logs, storage quota gauges, retention metrics.

---

## Gate 9: Security Hardening, Observability & Evaluation
- [ ] Enterprise Hardening:
  - [ ] SSRF defense test suite against private IP spaces and metadata services.
  - [ ] Prompt injection fuzz testing across malicious academic PDF test fixtures.
  - [ ] End-to-end telemetry and structured JSON audit logging.
  - [ ] Retrieval accuracy benchmark (Precision@K, Recall@K, Grounding Faithfulness).
  - [ ] Codex engineering audit for concurrency, idempotency, and database performance.

---

## Gate 10: Production Release, Cold Archival & Gate 10 Sign-off
- [ ] Production Readiness:
  - [ ] Cloudflare R2 migration & production deployment runbooks.
  - [ ] Automated database backup & cold archival export scripts to external storage.
  - [ ] Complete developer documentation and user manual.
  - [ ] Final architecture sign-off and mentor review.
