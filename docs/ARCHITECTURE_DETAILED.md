# Intel OS — Detailed Technical Architecture

## 1. System Decomposition & Module Boundaries

Intel OS is structured as a **Modular Monolith** in Python / FastAPI with an asynchronous background worker layer and a Next.js frontend console.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTEL OS MODULAR MONOLITH                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Ingestion Subsystem (`intel_os.ingestion`)                              │
│     ├── Connector Framework (arXiv, Crossref, Semantic Scholar, OpenAlex)   │
│     ├── Deduplication & Multi-Provider Reconciliation Engine                │
│     └── Pre-flight SSRF Guard & Rate-Limited Politeness Dispatcher          │
├─────────────────────────────────────────────────────────────────────────────┤
│  2. Parsing & Normalization Subsystem (`intel_os.parsing`)                  │
│     ├── Multi-column Academic PDF Parser (Layout-aware)                     │
│     ├── HTML Sanitizer & Clean Markdown Converter                           │
│     └── Section Splitter (Abstract, Methodology, Results, Limitations)      │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. Extraction & Epistemic Reasoning Subsystem (`intel_os.reasoning`)       │
│     ├── Replaceable Reasoning LLM Gateway (Gemini, Claude, OpenAI)          │
│     ├── Atomic Claim & Empirical Benchmark Evidence Extractor               │
│     └── Verbatim Quote Grounding Verifier & Epistemic Classifier            │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. Research Memory Subsystem (`intel_os.memory`)                           │
│     ├── PostgreSQL 16+ Relational Core (18 Normalized Tables)               │
│     ├── pgvector Semantic Index Manager (V1 768-dim Embedding Contract)     │
│     ├── Personal Research Memory Engine (Notes, Claims, Experiment Logs)    │
│     └── S3-Compatible Artifact Storage (Cloudflare R2 / AWS S3)             │
├─────────────────────────────────────────────────────────────────────────────┤
│  5. Opportunity & Lineage Subsystem (`intel_os.opportunity`)                │
│     ├── Research Gap Miner & Limitation Scanner                             │
│     ├── Scientific Contradiction Matrix Engine                              │
│     ├── Semantic Distinctiveness Signal Calculator                          │
│     └── Idea Lineage Graph & Snapshot Provenance Tracer                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  6. Retrieval & Synthesis Subsystem (`intel_os.synthesis`)                  │
│     ├── Hybrid Retriever (PostgreSQL Full-Text Lexical + pgvector Cosine)   │
│     ├── Reciprocal Rank Fusion (RRF) & Context Grounding Builder            │
│     ├── SOTA Benchmark Matrix Synthesizer                                   │
│     └── Research Handbook Generator (Markdown, LaTeX, PDF)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  7. Worker & Task Orchestrator (`intel_os.workers`)                         │
│     ├── Asynchronous Task Queue & Scheduling Engine                         │
│     ├── 4-Tier Idempotency Key Validator & Transaction Boundaries           │
│     └── Telemetry, Dead-Letter Queue & Retry Policy                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ingestion & Multi-Provider Reconciliation Subsystem

### 2.1 Connector Framework
* **Abstract Base Connector (`BaseConnector`)**:
  * Enforces rate-limiting via Token Bucket algorithm per domain.
  * Implements exponential backoff on HTTP 429 / 5xx responses.
  * Pre-flight SSRF validation checks hostname and IP address against blocklists before opening connections.
* **Specialized Academic Connectors**:
  * `ArxivConnector`: Queries arXiv API, parses Atom XML feeds.
  * `CrossrefConnector`: Retrieves publication metadata, DOIs, and bibtex records.
  * `SemanticScholarConnector`: Fetches citation counts and paper graphs.
  * `OpenAlexConnector`: Retrieves open scientific metadata and author affiliations.
  * `WebCrawlerConnector`: Ingests open-access web publications.

### 2.2 Deduplication Precedence & Reconciliation
To prevent duplicate logical documents when ingesting from multiple providers, the platform follows an explicit identity precedence:
$$\text{DOI} \longrightarrow \text{arXiv ID} \longrightarrow \text{Canonical URL} \longrightarrow \text{Metadata Fingerprint} \longrightarrow \text{Fetched Content Hash}$$

* `metadata_fingerprint` is a SHA-256 hash of normalized core metadata: `sha256(normalize(title) + normalize(authors) + venue + year)`.
* When a matching document is identified, a new record is added to `document_sources` to record the provider observation without creating redundant documents.
* Documents are mapped to topics via the `document_topics` many-to-many table.

---

## 3. Parsing, Normalization & Snapshot Subsystem

### 3.1 Document Versioning & Snapshots (`document_snapshots`)
A logical scientific document may have multiple representations over time (e.g., arXiv v1 vs v2, PDF vs HTML).
* Every fetched representation is stored as a `document_snapshots` record with:
  * `version_identifier` (e.g. `'arxiv_v1'`, `'arxiv_v2'`)
  * `content_hash` (SHA-256 of downloaded bytes)
  * `mime_type` (`'application/pdf'`, `'text/html'`)
  * `raw_s3_key` (Location in S3/R2 when retained)
  * `parser_version` and `extraction_version`

### 3.2 Layout-Aware Parsing & Section Splitting
* Uses layout-aware parsers (e.g. `pdfplumber` / PyPDF) to detect multi-column text, tables, and references.
* Segments papers into semantic sections: `ABSTRACT`, `METHODOLOGY`, `RESULTS`, `LIMITATIONS`, `FUTURE_WORK`.

---

## 4. Extraction & Epistemic Reasoning Subsystem

### 4.1 Replaceable Reasoning LLM Gateway vs Embedding Contract
* **Reasoning LLM Gateway**: Vendor-neutral adapter interface (`LLMGateway`) supporting Gemini, Claude, and OpenAI via Pydantic JSON schemas. Prompts and output schemas are decoupled from model providers.
* **V1 Embedding Model Contract**: All vector columns in PostgreSQL enforce **768 dimensions** (matching `text-embedding-004` / Gemini Embeddings). Future dimension upgrades follow a versioned migration protocol.

### 4.2 Four-Dimensional Epistemic Extraction
Every extracted assertion is decomposed into:
1. **Grounding Status (`grounding_status`)**: Verified via verbatim quote substring matching.
2. **Claim Type (`claim_type`)**: Categorized as `EMPIRICAL_FINDING`, `AUTHOR_HYPOTHESIS`, `BACKGROUND_ASSERTION`, `LIMITATION`, `FUTURE_WORK`, etc.
3. **Epistemic Status (`epistemic_status`)**: Initialized to `UNASSESSED`. Promoted to `SUPPORTED` only when verified against empirical evidence and methodology rigor.
4. **Evidence Items (`evidence_items`)**: Quantitative benchmarks, datasets, sample sizes, and p-values.

---

## 5. Storage Topology & Memory Subsystem

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AUTHORITATIVE STORAGE CORE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PostgreSQL 16+ Database (18 Normalized Tables)                             │
│  ├── `topics` & `document_topics` (M:N Topic Taxonomy)                      │
│  ├── `sources` & `document_sources` (Global Connectors & Provider Observ.)  │
│  ├── `documents` & `document_snapshots` (Logical Works & Version Snapshots) │
│  ├── `document_chunks` (Parsed Sections with 768-dim Vector Embeddings)     │
│  ├── `claims` & `evidence_items` (Grounded Claims & Empirical Metrics)      │
│  ├── `relationships` (Claim-to-Claim Graph Edges)                           │
│  ├── `research_gaps` & `contradictions` (Limitations & Scientific Conflicts)│
│  ├── `research_opportunities` & `research_ideas` (Opportunity Vectors)      │
│  ├── `idea_provenance` (Snapshot-Pinned Backward Lineage Graph)             │
│  ├── `user_notes` & `experiment_logs` (Personal Research Memory)            │
│  └── `background_jobs` (Asynchronous Job State & Telemetry)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  pgvector Extension (Colocated Semantic Vectors)                            │
│  ├── `document_chunks.embedding` (vector(768) / HNSW Index)                 │
│  ├── `claims.embedding` (vector(768) / HNSW Index)                          │
│  └── `research_ideas.embedding` (vector(768) / HNSW Index)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  S3-Compatible Object Store (Cloudflare R2 / AWS S3)                        │
│  └── `retained-artifacts/snapshots/{snapshot_id}.pdf`                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  Local Developer Environment (Transient & Bounded)                          │
│  └── Bounded Local Cache (`/cache/temp`, quota: `MAX_LOCAL_CACHE_GB = 10G`) │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Opportunity & Idea Lineage Subsystem

* **Research Gap Mining**: Aggregates limitation and future work sections across papers grouped by topic.
* **Scientific Contradiction Engine**: Identifies opposing empirical claims sharing identical entity or metric contexts.
* **Idea Lineage Engine**: Assembles recursive backward provenance trees linking candidate research ideas to specific research gaps, verified claims, supporting evidence items, and originating document snapshot versions.

---

## 7. Retrieval & Synthesis Subsystem

### 7.1 Hybrid Retrieval Architecture
```
Query Text
  │
  ├──► [PostgreSQL Full-Text Lexical Search (tsvector/tsquery)] ──► Top K_Lex (Ranked)
  │                                                                     │
  └──► [pgvector Cosine Distance Search (<=>)] ─────────────────► Top K_Vec (Ranked)
                                                                        │
                                                                        ▼
                                                           [Reciprocal Rank Fusion (RRF)]
                                                                        │
                                                                        ▼
                                                           [Grounding Context Builder]
```

* Retrieval utilizes standard PostgreSQL full-text lexical search and pgvector cosine similarity. Dedicated BM25 extensions (e.g. `pg_search`) will be evaluated in Gate 6/9 benchmarks.

---

## 8. Four-Tier Idempotency & Worker Architecture

* **Tier 1 (Document)**: Deduplicated via DOI, arXiv ID, or `metadata_fingerprint`.
* **Tier 2 (Provider Observation)**: Unique `(document_id, source_id, provider_doc_id)`.
* **Tier 3 (Snapshot)**: Unique `(document_id, version_identifier)` with SHA-256 byte hash.
* **Tier 4 (Worker Job)**: Task dispatch with `idempotency_key = sha256(job_type + payload_hash)`.
* **Local Cache Janitor**: Enforces `MAX_LOCAL_CACHE_GB` quota with automated LRU eviction.
