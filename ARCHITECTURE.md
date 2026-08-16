# Intel OS Architecture Overview

## 1. Architectural Philosophy

**Intel OS / NCKH Intelligence Platform** is built as a **Cloud-First Modular Monolith** designed for long-term personal research acceleration and scientific intelligence management.

The architectural design is governed by five non-negotiable principles:

1. **Durable Assets over Ephemeral Models**: Large Language Models are treated as replaceable computational reasoning engines. The true enduring value is the structured relational graph of verified claims, empirical evidence, research gaps, opportunities, and user insights.
2. **Strict Snapshot-Pinned Provenance & Lineage**: Every derived insight, hypothesis, research gap, or paper idea traces backward to its underlying claims, supporting evidence, originating document snapshot version, and discovery source.
3. **Cloud-First Authoritative Truth**: The developer laptop is never the system of record. Local storage is strictly bounded (`MAX_LOCAL_CACHE_GB`) as a transient execution cache. The authoritative repository of intelligence resides in a cloud-hosted PostgreSQL database and S3-compatible object storage.
4. **Selective Tiered Retention**: Ingestion distinguishes discovery from deep retention. Not every discovered item requires permanent raw document storage. Raw evidence is retained only when passing value, relevance, and reproducibility thresholds.
5. **Idempotency & Observability by Default**: All background ingestion, normalization, and analysis jobs are governed by a 4-tier idempotency model, trackable and verifiable through transactional telemetry.

---

## 2. High-Level System Architecture

```mermaid
flowchart TB
    subgraph DiscoveryLayer["1. Discovery & Ingestion Layer"]
        Sources["Discovery Connectors\n(arXiv, Crossref, Semantic Scholar, OpenAlex, Web)"]
        Crawler["Polite Crawler / Ingest Service\n(Rate-limited, Pre-flight SSRF Guard)"]
        Reconcile["Multi-Provider Reconciler\n(Canonical Identity Precedence)"]
        DocTopics["Many-to-Many Topic Mapper\n(document_topics)"]
    end

    subgraph StorageLayer["2. Storage & Memory Subsystem"]
        subgraph CloudStorage["Authoritative Cloud Core"]
            Postgres[("PostgreSQL 16+\n(18 Normalized Tables:\nTopics, Sources, Documents, Snapshots,\nClaims, Evidence, Gaps, Ideas)")]
            PgVector[("pgvector Extension\n(V1 768-dim Embedding Contract)")]
            S3Store[("S3 Object Storage (Cloudflare R2)\n(Retained Snapshot PDFs, HTML, Artifacts)")]
        end
        subgraph LocalTier["Developer Local Workspace"]
            LocalCache["Bounded Local Cache\n(MAX_LOCAL_CACHE_GB = 10G)"]
        end
    end

    subgraph ProcessingLayer["3. Intelligence Processing & Reasoning"]
        Snapshots["Versioned Representation Manager\n(document_snapshots)"]
        Parser["Layout-Aware Document Parser\n(PDF structure, Clean Markdown)"]
        Extractor["4D Extraction Engine\n(Grounding, Claim Type, Epistemic Status, Evidence)"]
        Scorer["Multi-Factor Scoring Engine\n(Relevance, Evidence Rigor, Semantic Distinctiveness)"]
        OpportunityMiner["Research Opportunity Miner\n(Gap Detector, Contradiction Engine)"]
        LineageGraph["Snapshot-Pinned Provenance & Lineage Engine"]
    end

    subgraph LLMAdapters["4. Replaceable AI Reasoning Layer"]
        Adapter["Provider-Agnostic LLM Gateway"]
        Gemini["Google Gemini"]
        Claude["Anthropic Claude"]
        OpenAI["OpenAI GPT"]
    end

    subgraph ApplicationLayer["5. Application & Interaction Layer"]
        FastAPI["FastAPI Modular Monolith API"]
        NextJS["Next.js Research Console (UI)"]
        ExportEngine["Handbook & Synthesis Generator"]
    end

    Sources --> Crawler --> Reconcile --> DocTopics
    DocTopics -->|"Discovered / Indexed"| Postgres
    DocTopics --> Snapshots
    Snapshots -->|"Retained Raw Files"| S3Store
    Snapshots --> Parser --> Extractor
    Extractor <--> Adapter
    Adapter --> Gemini & Claude & OpenAI
    Extractor --> Scorer --> OpportunityMiner --> LineageGraph
    LineageGraph --> Postgres & PgVector
    Postgres <--> FastAPI
    PgVector <--> FastAPI
    S3Store <--> FastAPI
    FastAPI <--> NextJS
    FastAPI --> ExportEngine
```

---

## 3. The Three Long-Lived Intellectual Assets

Intel OS manages three primary intellectual assets, designed to persist across decades of research:

### Asset 1: The Intelligence Lake
* **Function**: Indexes and organizes all discovered source material across multiple providers, filtering raw data into curated knowledge tiers.
* **Retention Hierarchy**:
  1. `DISCOVERED`: Canonical identity (DOI, arXiv ID, canonical URL), `metadata_fingerprint`, authors, publication venue (stored in PostgreSQL).
  2. `INDEXED`: Extracted abstract, normalized keywords, fast topic embeddings.
  3. `RELEVANT`: Full parsed clean text and structural sections tied to a `document_snapshots` record.
  4. `RETAINED`: Original raw artifact (PDF, HTML snapshot) preserved in S3-compatible storage with `raw_s3_key`.
  5. `ARCHIVED`: Cold storage tier for reproducible long-term project checkpoints.
* **Key Invariant**: Discovery does not imply raw file retention. Metadata-only intake prevents storage bloat.

### Asset 2: Personal Research Memory
* **Function**: The user's accumulated, verified scientific knowledge base and experimental narrative.
* **Key Components**:
  * **Verified Claims**: Atomic statements of fact, empirical findings, or theoretical assertions with verbatim quote grounding and explicit epistemic status (`UNASSESSED`, `SUPPORTED`, `CONTESTED`, etc.).
  * **Evidence Items**: Quantitative metrics, experimental setups, sample sizes, and statistical confidence levels linked to claims and document snapshots.
  * **Entity & Claim Relationships**: Cross-publication graph links connecting methods, benchmarks, and problem spaces (`SUPPORTS`, `CONTESTS`, `EXTENDS`, `REFUTES`).
  * **Personal Research Notes**: User observations, critique notes, brainstorms, and evolving mental models.
  * **Experiment Logs & Failure Analysis**: Detailed records of empirical trials, negative results, and design lessons.

### Asset 3: Research Opportunity Memory
* **Function**: A proactive scientific discovery engine that uncovers, structures, and refines high-potential research directions.
* **Key Components**:
  * **Research Gaps**: Underexplored domains, missing evaluations, hardware bottlenecks, or methodological limitations.
  * **Scientific Contradictions**: Explicit discrepancies between empirical findings across different publications.
  * **Candidate Ideas & Hypotheses**: Novel solution proposals evaluated for semantic distinctiveness, feasibility, and resource cost.
  * **Idea Lineage**: Complete backward provenance graph explaining *why* an idea was proposed, pinned to exact source snapshots.

---

## 4. Flagship Provenance: Idea Lineage Graph

Intel OS guarantees complete traceability for all generated insights and proposals:

$$\text{Idea} \longrightarrow \text{Opportunity} \longrightarrow \text{Gap / Contradiction} \longrightarrow \text{Claims} \longrightarrow \text{Evidence} \longrightarrow \text{Snapshots} \longrightarrow \text{Documents} \longrightarrow \text{Sources}$$

```mermaid
graph TD
    subgraph Idea["Research Idea Level"]
        I1["Idea: Efficient On-Device Speculative Decoding for Mobile NPUs"]
    end

    subgraph Opportunity["Opportunity & Gap Level"]
        O1["Opportunity: Sub-2B Linear Attention Speculator"]
        G1["Gap: Verification overhead bottlenecks heterogeneous NPUs"]
        C1["Contradiction: Kernel latency vs Memory bandwidth bottleneck"]
    end

    subgraph Claims["Verified Claims Level"]
        CL1["Claim: Fixed lookahead yields 38% stall on Apple A17 NPU\n[Epistemic: SUPPORTED, Grounding: VERBATIM_MATCH]"]
        CL2["Claim: Dynamic speculative windowing reduces thermal throttle by 4x\n[Epistemic: SUPPORTED, Grounding: VERBATIM_MATCH]"]
        CL3["Claim: Memory bus saturates before compute utilization reaches 50%\n[Epistemic: SUPPORTED, Grounding: VERBATIM_MATCH]"]
    end

    subgraph Evidence["Evidence & Snapshot Level"]
        E1["Evidence: Table 3 - Runtime latency across 500 prompts"]
        E2["Evidence: Figure 4 - Power vs Token throughput curves"]
        SN1["Snapshot: arXiv v2 PDF (Hash: e3b0c442...)"]
        SN2["Snapshot: Camera-Ready PDF (Hash: 9f83ac12...)"]
        D1["Paper: 'Latency Dynamics of Edge Speculation' (arXiv:2403.11111)"]
        D2["Paper: 'Thermal Characterization of Edge NPUs' (ACM MobileSys 2024)"]
    end

    subgraph Sources["Source Origin Level"]
        S1["Source: arXiv cs.AI Feed"]
        S2["Source: ACM Digital Library"]
    end

    I1 --> O1
    I1 --> G1
    I1 --> C1
    G1 --> CL1
    G1 --> CL2
    C1 --> CL1
    C1 --> CL3
    CL1 --> E1 --> SN1 --> D1 --> S1
    CL2 --> E2 --> SN2 --> D2 --> S2
    CL3 --> E1 --> SN1
```

---

## 5. Storage Topology & Cloud-First Principles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          STORAGE TOPOLOGY & ROLES                           │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Storage Tier                   │ Authoritative Responsibility               │
├────────────────────────────────┼────────────────────────────────────────────┤
│ PostgreSQL 16+ (Primary DB)    │ Authoritative source of truth for:         │
│                                │ • 18 Normalized Tables                     │
│                                │ • Multi-Topic Mappings (`document_topics`) │
│                                │ • Document Snapshots (`document_snapshots`)│
│                                │ • Claims, Evidence, Relationships          │
│                                │ • Research Gaps, Opportunities, Ideas      │
│                                │ • User Notes, Experiments, Job Logs        │
├────────────────────────────────┼────────────────────────────────────────────┤
│ pgvector (Extension)           │ Colocated semantic retrieval vectors for:  │
│                                │ • V1 Contract: Fixed 768 Dimensions        │
│                                │ • Document chunks, Claim embeddings        │
│                                │ • Research Idea embeddings (HNSW Index)    │
├────────────────────────────────┼────────────────────────────────────────────┤
│ S3 Object Storage (R2/MinIO)   │ Durable artifact storage for:              │
│                                │ • High-value raw snapshot PDFs and HTML    │
│                                │ • Extracted tables, charts, figures        │
│                                │ • Cold dataset dumps and exports           │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Developer Laptop (Local)       │ Transient execution environment:           │
│                                │ • Source code & test fixtures              │
│                                │ • Temporary parsing buffer                 │
│                                │ • Bounded cache (MAX_LOCAL_CACHE_GB = 10G) │
├────────────────────────────────┼────────────────────────────────────────────┤
│ External HDD (Cold Archive)    │ Disaster recovery & offline archives:      │
│                                │ • Monthly database dump archives           │
│                                │ • Large historical benchmark datasets      │
│                                │ (Never used as the active PostgreSQL host) │
└────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 6. Technology Stack Justification

| Component | Selected Technology | Architectural Justification |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI (Python 3.11+)** | High-performance asynchronous REST endpoints, native Pydantic schema validation, mature ecosystem for scientific document parsing. |
| **ORM / Data Access** | **SQLAlchemy 2.0 (Async) + asyncpg** | Robust relational mapping, explicit transaction boundaries, async query execution, direct compatibility with pgvector. |
| **Database** | **PostgreSQL 16+** | Industry standard for relational integrity, JSONB support for flexible metadata, ACID compliance for research memory. |
| **Vector Engine** | **pgvector** | Colocates vector embeddings inside PostgreSQL under a versioned 768-dim contract. Eliminates dual-database synchronization complexity. |
| **Object Store** | **S3-Compatible (Cloudflare R2)** | Standard S3 API, zero egress fees with Cloudflare R2, multi-region redundancy for raw research artifacts. |
| **Frontend UI** | **Next.js 15+ (App Router)** | High-performance server-rendered UI, TypeScript type safety, fluid responsive design for research exploration. |
| **Styling** | **Modern Vanilla CSS & Tokens** | Clean, fast, zero-runtime overhead, fully custom research console aesthetics. |
| **Queue & Workers** | **Asynchronous Job Worker** | Background scraping, parsing, and LLM extraction with 4-tier idempotency ensuring non-duplicating executions. |

---

## 7. Next Steps & Detailed Architecture

For granular technical specifications, refer to:
* [Detailed Architecture](docs/ARCHITECTURE_DETAILED.md)
* [Relational & Vector Data Model](docs/DATA_MODEL.md)
* [Ingestion & Processing Pipeline](docs/PIPELINE.md)
* [Security & Sandboxing Model](docs/SECURITY_MODEL.md)
* [Multi-Factor Scoring Model](docs/SCORING_MODEL.md)
* [Intelligence & Epistemic Ontology](docs/INTELLIGENCE_MODEL.md)
