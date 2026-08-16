# Intel OS / NCKH Intelligence Platform — Milestones Roadmap (G0–G10)

This document establishes the authoritative engineering milestones, deliverables, hard acceptance criteria, and agent governance rules across all 11 development gates (G0 to G10).

---

## Milestone Summary Matrix

| Gate | Focus Area | Primary Deliverables | Agent Lead |
| :--- | :--- | :--- | :--- |
| **G0** | **Foundation & Architecture** | Architecture, Data Models, ADRs, Governance | **Antigravity (Gemini)** |
| **G1** | **Database & Backend Scaffolding** | FastAPI core, PostgreSQL 16+ DDL, pgvector, Alembic | **Antigravity** / *Codex* |
| **G2** | **Ingestion & Connectors** | arXiv, Crossref, Semantic Scholar, SSRF guard | **Antigravity** |
| **G3** | **Parsing & Claim Extraction** | Layout-aware PDF parser, LLM quote grounding | **Antigravity** |
| **G4** | **Memory & Object Storage** | PostgreSQL memory core, pgvector HNSW, S3 R2 | **Antigravity** |
| **G5** | **Opportunity Miner & Lineage** | Gap detector, contradiction matrix, idea provenance | **Antigravity** |
| **G6** | **Search, Retrieval & Synthesis** | Hybrid BM25 + Vector retrieval, SOTA matrix | **Antigravity** / *Codex* |
| **G7** | **Handbook & Output Generation** | Research Handbook generator, LaTeX/PDF export | **Antigravity** |
| **G8** | **Next.js Research Console** | Interactive UI, Idea Lineage visualizer, Workbench | **Antigravity** |
| **G9** | **Security & Benchmark Audit** | SSRF/Injection fuzzing, retrieval benchmarks, telemetry | *Codex* / **Antigravity** |
| **G10**| **Production Release & Archival** | Cloudflare R2 migration, cold archive backups | **Antigravity** / *Codex* |

---

## Gate 0: Foundation, Architecture & Specification Baseline [CURRENT]

### Objective
Establish the theoretical, architectural, and data foundation for Intel OS without introducing premature feature code.

### Deliverables
* Complete architectural and specification suite:
  * `README.md`, `PROJECT_STATE.md`, `TODO.md`, `DECISIONS.md`, `ARCHITECTURE.md`, `CHANGELOG_AGENT.md`
  * `docs/PRODUCT_SPEC.md`, `docs/ARCHITECTURE_DETAILED.md`, `docs/DATA_MODEL.md`, `docs/PIPELINE.md`
  * `docs/MILESTONES.md`, `docs/SECURITY_MODEL.md`, `docs/SCORING_MODEL.md`, `docs/INTELLIGENCE_MODEL.md`
* Repository configuration: `.gitignore`, `.env.example`.

### Acceptance Criteria
- [x] Product scope, persona definitions, and explicit non-goals documented.
- [x] Three long-lived assets (Intelligence Lake, Personal Research Memory, Research Opportunity Memory) formally specified.
- [x] Multi-tier retention policy (`DISCOVERED → INDEXED → RELEVANT → RETAINED → ARCHIVED`) defined.
- [x] Complete PostgreSQL 16+ DDL with pgvector and recursive lineage queries specified.
- [x] Idea Lineage provenance chain explicitly formulated.
- [x] Security perimeter against SSRF, prompt injection, and parser exploits defined.
- [x] No premature application feature code introduced.
- [x] G0 committed and pushed to GitHub tracking `Phuchello/NCKH`.
- [x] Mentor review requested before initiating G1.

---

## Gate 1: Database Initialization & Backend Core Scaffolding

### Objective
Create the executable Python backend scaffolding, establish async database connectivity, execute Alembic migrations, and enforce bounded local cache limits.

### Deliverables
* Python 3.11+ project configuration (`pyproject.toml`, `requirements.txt`).
* Async SQLAlchemy / asyncpg engine with connection pooling and health check routes.
* Alembic migration environment generating PostgreSQL tables from `docs/DATA_MODEL.md`.
* `LocalCacheManager` enforcing `MAX_LOCAL_CACHE_GB` quota with automated LRU cleanup.
* Pytest testing harness (`pytest-asyncio`).

### Acceptance Criteria
* `alembic upgrade head` successfully creates all 12 tables and pgvector HNSW indices on clean PostgreSQL.
* Automated tests pass for database CRUD and async connection lifecycle.
* Local cache manager throws quota alerts and successfully prunes temporary files when threshold is breached.

---

## Gate 2: Ingestion Engine & Source Connector Framework

### Objective
Implement polite, rate-limited, SSRF-defended academic connectors and idempotent ingestion.

### Deliverables
* `BaseConnector` abstract interface with Token Bucket rate limiter and retry policy.
* Connectors for arXiv API, Semantic Scholar API, and Crossref API.
* SSRF validation guard resolving DNS and blocking private/loopback IP spaces.
* SHA-256 content deduplication and canonical DOI normalizer.

### Acceptance Criteria
* Ingestion of 100 test preprints from arXiv passes with zero duplicates.
* Re-crawling identical URLs is 100% idempotent and makes zero redundant DB inserts.
* Attempted crawler requests to `127.0.0.1`, `10.0.0.1`, or `169.254.169.254` are immediately blocked.

---

## Gate 3: Text Processing, Normalization & Extraction Pipeline

### Objective
Implement layout-aware academic PDF extraction, LLM gateway adapters, and quote-grounded claim extraction.

### Deliverables
* PDF parser handling multi-column layouts, tables, and reference sections.
* Section splitter identifying Abstract, Methodology, Results, Discussion, and Limitations.
* Replaceable `LLMGateway` supporting Gemini, Claude, and OpenAI via Pydantic schemas.
* Claim & evidence extractor with verbatim quote bounding and offset calculation.

### Acceptance Criteria
* PDF parsing achieves clean section extraction on 10 diverse academic papers.
* 100% of extracted claims match verbatim text in source documents within character offset bounds.
* Extracted claims failing verbatim verification are rejected.

---

## Gate 4: Intelligence Lake & Personal Research Memory Storage

### Objective
Implement S3-compatible artifact retention for high-value papers, pgvector embedding indexing, and user memory CRUD.

### Deliverables
* S3 storage client (`S3ArtifactStore`) supporting upload, download, and URL generation for Cloudflare R2 / AWS S3.
* Retention tier promotion manager (`DISCOVERED → INDEXED → RELEVANT → RETAINED`).
* Embedding generation pipeline storing 768-dim vectors in `claims` and `document_chunks`.
* REST API endpoints for user notes, experiment logs, and claim exploration.

### Acceptance Criteria
* High-value papers promote to `RETAINED` and store raw PDFs in S3 with matching DB keys.
* HNSW cosine distance search on pgvector returns top-K semantically relevant claims in <50ms.
* User notes link transactionally to claims and documents.

---

## Gate 5: Research Opportunity Miner (Gaps, Contradictions, Lineage)

### Objective
Implement algorithmic detection of research gaps, scientific contradictions, and automated Idea Lineage construction.

### Deliverables
* Gap detector analyzing paper limitation sections.
* Scientific contradiction engine cross-evaluating opposing empirical claims.
* Emerging trend velocity calculator tracking keyword momentum.
* Idea proposal generator producing hypotheses with full `idea_provenance` records.

### Acceptance Criteria
* Contradiction engine flags conflicting benchmark claims on synthetic test fixtures.
* Every generated research idea contains a valid backward lineage graph linking to at least one gap, claim, and source document.
* Recursive SQL lineage query executes and outputs complete provenance tree.

---

## Gate 6: Core Search, Retrieval & Synthesis API

### Objective
Build hybrid search engine and provenance-constrained literature review synthesis.

### Deliverables
* Hybrid retriever combining PostgreSQL BM25 full-text search with pgvector cosine distance.
* Reciprocal Rank Fusion (RRF) and reranking pipeline.
* SOTA comparison matrix generator.
* Provenance-constrained Q&A endpoint with verified citations.

### Acceptance Criteria
* Hybrid search achieves higher retrieval recall than BM25 or vector search alone.
* Synthesized literature reviews contain zero unverified citations.

---

## Gate 7: Research Handbook & Output Generation

### Objective
Implement automated scientific handbook and paper blueprint synthesis.

### Deliverables
* Research Handbook compiler organizing topic intelligence into structured chapters.
* Export pipelines for Markdown, LaTeX, and PDF.
* BibTeX reference generator with verified DOIs.

### Acceptance Criteria
* Generated LaTeX document compiles cleanly with `pdflatex` or standard LaTeX engines.
* All citations in generated handbooks match valid database records.

---

## Gate 8: Web UI / Next.js Research Console

### Objective
Deliver a responsive, modern web interface for research exploration, idea lineage inspection, and intelligence monitoring.

### Deliverables
* Next.js 15+ App Router frontend with custom Vanilla CSS design tokens.
* Topic overview and intelligence feed.
* Interactive Idea Lineage graph visualizer.
* Research Memory workbench for notes, claims, and hypothesis management.
* Crawler and storage quota monitoring dashboard.

### Acceptance Criteria
* UI renders smoothly with responsive layouts across desktop and mobile.
* Idea Lineage visualizer allows interactive graph navigation back to original paper quotes.
* Fast API integration with <200ms roundtrip UI updates.

---

## Gate 9: Security Hardening, Observability & Benchmark Audit

### Objective
Perform end-to-end security penetration testing, prompt injection fuzzing, retrieval benchmarks, and Codex engineering audit.

### Deliverables
* Automated SSRF and prompt injection test suite.
* Retrieval accuracy benchmarks (MRR@10, NDCG@10).
* Structured JSON logging and Prometheus telemetry metrics.
* Codex audit report on concurrency, idempotency, and database locks.

### Acceptance Criteria
* Zero high-severity vulnerabilities identified in security audit.
* Retrieval benchmark meets target accuracy thresholds.
* Background workers withstand simulated network disconnects and concurrent job restarts without race conditions.

---

## Gate 10: Production Release, Cold Archival & Gate 10 Sign-off

### Objective
Finalize production deployment configuration, establish automated cold backup protocols, and achieve formal project sign-off.

### Deliverables
* Cloudflare R2 production bucket configuration.
* Automated cold database and artifact export script targeting external storage.
* Comprehensive user handbook and API documentation.
* Final Gate 10 review and repository tag.

### Acceptance Criteria
* Production deployment boots cleanly and passes end-to-end smoke tests.
* Cold backup export successfully produces restorable PostgreSQL dump and S3 archive bundle.
* Formal mentor approval and sign-off.
