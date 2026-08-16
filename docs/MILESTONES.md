# Intel OS / NCKH Intelligence Platform — Milestones Roadmap (G0–G10)

This document establishes the authoritative engineering milestones, deliverables, hard acceptance criteria, and agent governance rules across all development gates (G0 to G10).

---

## Milestone Summary Matrix

| Gate | Focus Area | Primary Deliverables | Agent Lead |
| :--- | :--- | :--- | :--- |
| **G0 / G0.1 / G0.2** | **Foundation & Architecture** | Architecture, 18-Table DDL, Epistemic Model, ADRs, Governance | **Antigravity (Gemini)** |
| **G1** | **Database & Backend Scaffolding** | FastAPI core, PostgreSQL 16+ DDL (7 G1 tables), pgvector, Alembic | **Antigravity** / *Codex* |
| **G2** | **Ingestion & Connectors** | arXiv, Crossref, Semantic Scholar, SSRF guard, Reconciliation | **Antigravity** |
| **G3** | **Parsing & Claim Extraction** | Layout PDF parser, Snapshot model, LLM quote grounding | **Antigravity** |
| **G4** | **Memory & Object Storage** | PostgreSQL memory core, pgvector HNSW, S3 R2 store | **Antigravity** |
| **G5** | **Opportunity Miner & Lineage** | Gap detector, contradiction matrix, snapshot-pinned lineage | **Antigravity** |
| **G6** | **Search, Retrieval & Synthesis** | Hybrid Lexical + Vector retrieval, SOTA matrix | **Antigravity** / *Codex* |
| **G7** | **Handbook & Output Generation** | Research Handbook generator, LaTeX/PDF export | **Antigravity** |
| **G8** | **Next.js Research Console** | Interactive UI, Idea Lineage visualizer, Workbench | **Antigravity** |
| **G9** | **Security & Benchmark Audit** | SSRF/Injection fuzzing, retrieval benchmarks, scoring calibration | *Codex* / **Antigravity** |
| **G10**| **Production Release & Archival** | Cloudflare R2 migration, cold archive backups | **Antigravity** / *Codex* |

---

## Gate 0 / Gate 0.1 / Gate 0.2: Foundation, Architecture & Specification Baseline [CURRENT]

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
- [x] Topic cardinality modeled as Many-to-Many (`document_topics`).
- [x] Document version snapshot model (`document_snapshots`) specified.
- [x] Epistemic dimensions (Grounding vs Claim Type vs Epistemic Status vs Evidence Quality) decoupled.
- [x] Deduplication precedence (`DOI → arXiv ID → Canonical URL → Metadata Fingerprint → Content Hash`) defined.
- [x] Versioned V1 Embedding Model Contract (768 dimensions) established.
- [x] Complete PostgreSQL 16+ DDL specifying exactly 18 normalized tables and recursive snapshot-pinned lineage queries.
- [x] Defense-in-depth security model with pre-flight SSRF IP blocking and prompt injection fencing.
- [x] Calibrated scoring definitions with provisional heuristic labels.
- [x] No premature application feature code introduced.
- [x] Committed and pushed to GitHub tracking `Phuchello/NCKH`.
- [x] Mentor review requested before initiating G1.

---

## Gate 1: Database Initialization & Backend Core Scaffolding

### Objective
Create the executable Python backend scaffolding, establish async database connectivity, execute the **G1 Foundation** Alembic migration (7 tables), and enforce bounded local cache limits.

### Deliverables
* Python 3.11+ project configuration (`pyproject.toml`, `requirements.txt`).
* Async SQLAlchemy / asyncpg engine with connection pooling and health check routes.
* **G1 Foundation Alembic migration** generating 7 tables: `topics`, `sources`, `documents`, `document_topics`, `document_sources`, `document_snapshots`, `background_jobs`.
* `LocalCacheManager` enforcing `MAX_LOCAL_CACHE_GB` quota with automated LRU cleanup.
* Pytest testing harness (`pytest-asyncio`).

### Migration Staging Note
> G1 creates only the 7 foundation tables. Extraction tables (`document_chunks`, `claims`, `evidence_items`, `relationships`, `user_notes`) are introduced in G3/G4. Opportunity tables (`research_gaps`, `contradictions`, `research_opportunities`, `research_ideas`, `idea_provenance`, `experiment_logs`) are introduced in G5. See `docs/DATA_MODEL.md` §5 for the full staging matrix.

### Acceptance Criteria
* `alembic upgrade head` successfully creates the 7 G1 foundation tables and associated indices on clean PostgreSQL 16+.
* Automated tests pass for database CRUD and async connection lifecycle.
* Local cache manager throws quota alerts and successfully prunes temporary files when threshold is breached.
* Schema matches `docs/DATA_MODEL.md` §6 DDL for the 7 G1 tables exactly.

---

## Gate 2: Ingestion Engine & Source Connector Framework

### Objective
Implement polite, rate-limited, SSRF-defended academic connectors and idempotent multi-provider ingestion reconciliation.

### Deliverables
* `BaseConnector` abstract interface with Token Bucket rate limiter and retry policy.
* Connectors for arXiv API, Semantic Scholar API, Crossref API, and OpenAlex API.
* SSRF validation guard resolving DNS and blocking private/loopback IP spaces.
* Multi-provider document reconciliation engine using canonical identity precedence.

### Acceptance Criteria
* Ingestion of test preprints from arXiv and Crossref reconciles matching documents into single logical records with distinct `document_sources` observations.
* Re-crawling identical URLs is 100% idempotent and makes zero redundant DB inserts.
* Attempted crawler requests to private subnets or cloud metadata IPs (`169.254.169.254`) are immediately blocked.

---

## Gate 3: Text Processing, Normalization & Extraction Pipeline

### Objective
Implement layout-aware academic PDF extraction, representation versioning (`document_snapshots`), LLM gateway adapters, and quote-grounded claim extraction.

### Deliverables
* PDF parser handling multi-column layouts, tables, and reference sections.
* Section splitter identifying Abstract, Methodology, Results, Limitations, and Future Work.
* Versioned representation manager populating `document_snapshots`.
* Replaceable `LLMGateway` supporting Gemini, Claude, and OpenAI via Pydantic schemas.
* Claim & evidence extractor enforcing verbatim quote bounding and setting `epistemic_status = 'UNASSESSED'`.

### Acceptance Criteria
* PDF parsing achieves clean section extraction on diverse academic papers.
* 100% of extracted claims achieve `grounding_status = 'VERBATIM_MATCH'` matching source text within character offset bounds; failed quotes are quarantined.
* Newly extracted claims default to `UNASSESSED`.

---

## Gate 4: Intelligence Lake & Personal Research Memory Storage

### Objective
Implement S3-compatible artifact retention for high-value papers, pgvector embedding indexing (768 dimensions), and user memory CRUD.

### Deliverables
* S3 storage client (`S3ArtifactStore`) supporting upload, download, and URL generation for Cloudflare R2 / AWS S3.
* Retention tier promotion manager (`DISCOVERED → INDEXED → RELEVANT → RETAINED`).
* Embedding generation pipeline storing 768-dim vectors in `claims`, `document_chunks`, and `research_ideas`.
* REST API endpoints for user notes, experiment logs, and claim exploration.

### Acceptance Criteria
* High-value papers promote to `RETAINED` and store raw PDFs in S3 with matching snapshot records.
* HNSW cosine distance search on pgvector returns top-K semantically relevant claims in <50ms.
* User notes link transactionally to claims and documents.

---

## Gate 5: Research Opportunity Miner (Gaps, Contradictions, Lineage)

### Objective
Implement algorithmic detection of research gaps, scientific contradictions, semantic distinctiveness scoring, and snapshot-pinned Idea Lineage construction.

### Deliverables
* Gap detector analyzing paper limitation sections.
* Scientific contradiction engine cross-evaluating opposing empirical claims.
* Semantic distinctiveness signal calculator comparing candidate ideas against retrieved prior art.
* Idea proposal generator producing hypotheses with full `idea_provenance` records pinned to specific `document_snapshots`.

### Acceptance Criteria
* Contradiction engine flags conflicting benchmark claims on synthetic test fixtures.
* Every generated research idea contains a valid backward lineage graph linking to at least one gap, claim, source document, and snapshot version.
* Recursive SQL lineage query executes and outputs complete provenance tree.

---

## Gate 6: Core Search, Retrieval & Synthesis API

### Objective
Build hybrid search engine (PostgreSQL lexical search + pgvector cosine distance) and provenance-constrained literature review synthesis.

### Deliverables
* Hybrid retriever combining PostgreSQL full-text lexical search (`tsvector`/`tsquery`) with pgvector cosine distance.
* Reciprocal Rank Fusion (RRF) and reranking pipeline.
* SOTA comparison matrix generator.
* Provenance-constrained Q&A endpoint with verified citations.

### Acceptance Criteria
* Hybrid search achieves higher retrieval recall than lexical search or vector search alone.
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
* Interactive Idea Lineage graph visualizer with snapshot provenance inspection.
* Research Memory workbench for notes, claims, and hypothesis management.
* Crawler and storage quota monitoring dashboard.

### Acceptance Criteria
* UI renders smoothly with responsive layouts across desktop and mobile.
* Idea Lineage visualizer allows interactive graph navigation back to original paper quotes and snapshot versions.
* Fast API integration with <200ms roundtrip UI updates.

---

## Gate 9: Security Hardening, Observability & Benchmark Audit

### Objective
Perform end-to-end security penetration testing, prompt injection fuzzing, retrieval benchmarks, scoring calibration, and Codex engineering audit.

### Deliverables
* Automated SSRF and prompt injection test suite.
* Retrieval accuracy benchmarks (MRR@10, NDCG@10).
* Empirical calibration of scoring model parameters (\(w_v, w_c, \alpha, \beta, \gamma\)).
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
