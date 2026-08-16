# Intel OS — Detailed Technical Architecture

## 1. System Decomposition & Module Boundaries

Intel OS is structured as a **Modular Monolith** in Python / FastAPI with an asynchronous background worker layer and a Next.js frontend console.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTEL OS MODULAR MONOLITH                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Ingestion Subsystem (`intel_os.ingestion`)                              │
│     ├── Connector Framework (arXiv, Crossref, Semantic Scholar, Web)        │
│     ├── Fingerprinting & Deduplication Engine (SHA-256, DOI)                │
│     └── Tier-1 Fast Classification & Politeness Dispatcher                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  2. Parsing & Normalization Subsystem (`intel_os.parsing`)                  │
│     ├── Multi-column Academic PDF Parser (Layout-aware)                     │
│     ├── HTML Sanitizer & Clean Markdown Converter                           │
│     └── Document Section Splitter (Abstract, Method, Results, Discussion)   │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. Extraction & Reasoning Subsystem (`intel_os.reasoning`)                 │
│     ├── Replaceable LLM Gateway (Gemini, Claude, OpenAI)                    │
│     ├── Atomic Claim & Empirical Evidence Extractor                         │
│     └── Quote-Bounding Grounding & Verification Verifier                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. Research Memory Subsystem (`intel_os.memory`)                           │
│     ├── PostgreSQL Relational Core (Claims, Evidence, Entities)             │
│     ├── pgvector Semantic Index Manager (HNSW Indexing)                     │
│     ├── Personal Research Memory & Annotation Engine                        │
│     └── S3-Compatible Artifact Storage (Cloudflare R2 / AWS S3)             │
├─────────────────────────────────────────────────────────────────────────────┤
│  5. Opportunity & Lineage Subsystem (`intel_os.opportunity`)                │
│     ├── Research Gap Miner & Limitation Scanner                             │
│     ├── Scientific Contradiction Matrix Engine                              │
│     ├── Emerging Trend Velocity Calculator                                  │
│     └── Idea Lineage Graph & Provenance Tracer                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  6. Retrieval & Synthesis Subsystem (`intel_os.synthesis`)                  │
│     ├── Hybrid Retriever (PostgreSQL BM25 + pgvector Cosine Distance)       │
│     ├── Reciprocal Rank Fusion (RRF) & Cross-Encoder Reranker               │
│     ├── Literature Review & SOTA Matrix Synthesizer                         │
│     └── Research Handbook Generator (Markdown, LaTeX, PDF)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  7. Worker & Task Orchestrator (`intel_os.workers`)                         │
│     ├── Asynchronous Task Queue & Scheduling Engine                         │
│     ├── Idempotency Key Validator & Transaction Boundaries                  │
│     └── Telemetry, Dead-Letter Queue & Retry Policy                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ingestion Subsystem

### 2.1 Connector Framework
* **Abstract Base Connector (`BaseConnector`)**:
  * Enforces rate-limiting via Token Bucket algorithm per domain.
  * Implements exponential backoff on HTTP 429 / 5xx errors.
  * Respects `robots.txt` directives.
* **Specialized Academic Adapters**:
  * `ArxivConnector`: Queries arXiv API via structured search queries (e.g. `cat:cs.AI`, `cat:cs.LG`), parses Atom XML feeds.
  * `CrossrefConnector`: Retrieves metadata, DOIs, publication venues, and bibtex records.
  * `SemanticScholarConnector`: Fetches citation graphs, highly influential citations, and paper embeddings.
  * `WebCrawlerConnector`: Ingests open-access web publications with strict SSRF filtering.

### 2.2 Content Fingerprinting & Deduplication
* Canonical URL normalization (removing tracking parameters, normalizing protocol/trailing slash).
* DOI lowercasing and standard prefix formatting (`10.xxxx/...`).
* SHA-256 hashing of raw content and normalized metadata to eliminate duplicate processing.
* **Idempotency Guarantee**: If a document with matching SHA-256 or DOI already exists, the ingestion pipeline transitions directly to metadata reconciliation without re-downloading or re-extracting.

---

## 3. Parsing & Normalization Subsystem

### 3.1 PDF & Document Processing
* **Layout-Aware Extraction**: Uses specialized PDF parsing (e.g. `pdfplumber` / PyPDF) to detect multi-column layouts, tables, headers, footers, and references.
* **Structured Section Splitting**: Papers are segmented into semantic sections:
  * `TITLE` & `ABSTRACT`
  * `INTRODUCTION` & `BACKGROUND`
  * `METHODOLOGY` / `ARCHITECTURE`
  * `EXPERIMENTAL_SETUP` & `BENCHMARKS`
  * `RESULTS` & `FINDINGS`
  * `LIMITATIONS` & `FUTURE_WORK`
  * `REFERENCES` & `BIBLIOGRAPHY`

### 3.2 HTML Sanitization
* Strips all executable scripts, iframes, styles, and advertising boilerplate using bleach / DOMPurify.
* Converts semantic HTML tags into standard Markdown syntax.

---

## 4. Extraction & Reasoning Subsystem

### 4.1 Replaceable LLM Gateway
* Implements a vendor-neutral interface (`LLMGateway`):
  * Input: Structured prompt template, input text, and target Pydantic schema.
  * Output: Validated Pydantic model instance.
  * Supported Adapters: Google Gemini, Anthropic Claude, OpenAI.
* Zero proprietary vendor lock-in: Prompt templates and JSON schemas remain identical across providers.

### 4.2 Claim & Evidence Extraction
* Extracts **Atomic Claims**: Single, independently verifiable assertions (e.g. *"Quantization to INT4 reduces memory bandwidth by 3.2x with <0.5% accuracy loss"*).
* Extracts **Empirical Evidence**: Dataset names, sample sizes, hardware testbeds, baseline models, performance metrics, and statistical confidence values.
* **Verbatim Quote Grounding**: Every claim and evidence item stores exact string offsets (`start_char`, `end_char`) matching the source text. Any extracted claim without matching source text is rejected as a hallucination.

---

## 5. Storage Topology & Memory Subsystem

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AUTHORITATIVE STORAGE CORE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PostgreSQL 16+ Database (ACID / Relational / Graph Queries)                │
│  ├── `topics` & `topic_taxonomies`                                          │
│  ├── `sources` & `source_connectors`                                        │
│  ├── `documents` & `document_chunks`                                        │
│  ├── `claims` & `evidence_items`                                            │
│  ├── `relationships` (Entity & Claim Graph)                                 │
│  ├── `research_gaps`, `contradictions`, `emerging_trends`                   │
│  ├── `research_opportunities` & `research_ideas`                            │
│  ├── `idea_provenance` (Explicit Lineage Graph)                             │
│  ├── `user_notes` & `experiment_logs` (Personal Research Memory)            │
│  └── `background_jobs` & `job_telemetry`                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  pgvector Extension (Colocated Semantic Vectors)                            │
│  ├── `document_chunks.embedding` (vector(768) / HNSW Index)                 │
│  ├── `claims.embedding` (vector(768) / HNSW Index)                          │
│  └── `research_ideas.embedding` (vector(768) / HNSW Index)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  S3-Compatible Object Store (Cloudflare R2 / AWS S3)                        │
│  ├── `retained-artifacts/pdfs/{doc_id}.pdf`                                 │
│  ├── `retained-artifacts/html/{doc_id}.html`                                │
│  └── `retained-artifacts/figures/{doc_id}_{fig_id}.png`                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  Local Developer Environment (Transient & Bounded)                          │
│  ├── Source Code (`/backend`, `/frontend`, `/docs`)                         │
│  └── Bounded Local Cache (`/cache/temp`, quota: `MAX_LOCAL_CACHE_GB`)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Opportunity & Idea Lineage Subsystem

### 6.1 Research Gap Mining
* Analyzes `LIMITATIONS` and `FUTURE_WORK` sections across papers grouped by topic.
* Clusters recurring unsolved challenges and correlates them with hardware or theoretical constraints.

### 6.2 Scientific Contradiction Matrix
* Cross-compares claims sharing identical entities or metrics (e.g. *Latency of Method X on Hardware Y*).
* Flags claims with opposing conclusions and calculates contradiction severity scores.

### 6.3 Backward & Forward Lineage Traversal
* **Backward Lineage**: Given a generated research proposal, traverses relational edges back through opportunities, gaps, claims, evidence items, and original source documents.
* **Forward Impact**: When a new paper is ingested, the system calculates which existing hypotheses or ideas are supported, challenged, or superseded.

---

## 7. Retrieval & Synthesis Subsystem

### 7.1 Hybrid Retrieval Architecture
```
Query Text
  │
  ├──► [BM25 Full-Text Search on PostgreSQL tsvector] ──► Top KBM25 (Ranked)
  │                                                            │
  └──► [pgvector Cosine Distance Search (<=>)] ────────► Top KVec (Ranked)
                                                               │
                                                               ▼
                                                  [Reciprocal Rank Fusion (RRF)]
                                                               │
                                                               ▼
                                                  [Cross-Encoder Reranker]
                                                               │
                                                               ▼
                                                  [Grounding Context Builder]
```

### 7.2 Research Handbook Synthesizer
* Formats curated intelligence into structured chapters:
  1. Executive Summary & Problem Formulation
  2. Taxonomy & Methodological Landscape
  3. Empirical Benchmark Matrix & Comparative Analysis
  4. Active Contradictions & Unresolved Research Gaps
  5. High-Impact Research Proposals & Experimental Blueprints
  6. Verified Bibliographic Index

---

## 8. Worker Orchestration & Asynchronous Processing

* **Idempotent Job Dispatch**: Every task receives a deterministic `job_id` based on `hash(task_type, payload_hash)`.
* **State Machine**: `PENDING → RUNNING → COMPLETED / FAILED / RETRYING`.
* **Dead-Letter Queue (DLQ)**: Tasks failing after 3 retries are moved to DLQ with full stack traces for forensic analysis.
* **Local Cache Janitor**: Background routine monitoring `/cache/temp` and evicting least-recently-used files when total usage exceeds `MAX_LOCAL_CACHE_GB`.
