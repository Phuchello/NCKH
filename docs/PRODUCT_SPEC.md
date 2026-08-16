# Intel OS / NCKH Intelligence Platform — Product Specification

## 1. Product Vision & Mission

### 1.1 Vision
**Intel OS** is an intelligent, long-term scientific research and intelligence operating system. It transforms scientific discovery (Nghiên cứu Khoa học - NCKH) from fragmented, manual literature browsing into an automated, structured, and compounding intellectual asset.

### 1.2 Mission
To empower researchers and intelligence analysts to continuously discover, critically verify, semantically connect, and proactively synthesize scientific literature into durable personal research memory and breakthrough research opportunities.

---

## 2. Target Personas & Use Cases

### 2.1 Personas
1. **The NCKH Lead Researcher / Principal Investigator**:
   * *Goal*: Identify high-impact research gaps, map competing methodologies, and generate defensible research grant proposals.
   * *Pain Points*: Overwhelmed by 100+ weekly preprint publications, struggling to trace why a specific hypothesis is novel, losing track of historical notes and failed experiments.
2. **The Scientific Intelligence Analyst**:
   * *Goal*: Track technological frontiers, detect emerging trends across disparate disciplines, and surface scientific contradictions between peer-reviewed publications.
   * *Pain Points*: Information silos, lack of evidence-level provenance, opaque AI summaries that hallucinate citations.
3. **The Graduate Student / Research Fellow**:
   * *Goal*: Build an authoritative State-of-the-Art (SOTA) literature matrix and author structured scientific survey handbooks.
   * *Pain Points*: Disorganized PDFs on local laptop storage, tedious manual citation management, inability to query past read papers semantically.

---

## 3. Core Differentiation: What Intel OS Is and Is NOT

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CORE DIFFERENTIATION                             │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ What Intel OS IS                     │ What Intel OS IS NOT                 │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • A Durable Research Memory System   │ • A Generic RSS Reader / News Feed   │
│ • Provenance-Enforced Claim Engine   │ • A Shallow AI Chat Wrapper          │
│ • Proactive Research Gap Miner       │ • A Generic PDF Summarizer           │
│ • Multi-Tiered Retention Lake        │ • A Brittle Local-Only File Folder   │
│ • Graph of Contradictions & Lineage  │ • A Black-Box LLM Fine-Tuning Project│
│ • Cloud-First Long-Term Asset        │ • An Unbounded Disk-Exhausting Scraper│
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 3.1 Non-Goals (Explicit Boundaries)
* **Not a Generic Chatbot**: Intel OS does not prioritize unstructured casual conversation. All interactions are grounded in structured research entities, verified claims, and evidence links.
* **Not an Unbounded Web Scraper**: The platform does not permanently download the entire internet. It employs a strict filtering funnel to retain raw documents only when their research value is proven.
* **Not an In-House LLM Training Platform**: The platform does not attempt to train custom foundation models from scratch in early versions. Foundation models are interchangeable reasoning engines; the structured data is the system of record.
* **Not a Pure Local-Only Tool**: Intel OS rejects the fragility of storing the primary research database on a personal laptop drive.

---

## 4. Functional Requirements & Core Epics

### Epic 1: Multi-Source Discovery & Reconciliation (Discovery Layer)
* **FR-1.1**: Multi-channel discovery across academic preprint APIs (arXiv, Crossref, Semantic Scholar, OpenAlex) and web feeds.
* **FR-1.2**: Multi-provider document reconciliation: Reconciles records from multiple sources into a single logical `Document` via canonical identity precedence (`DOI → arXiv ID → URL → Metadata Fingerprint`).
* **FR-1.3**: Many-to-Many Topic Assignment: Maps documents to multiple research topics via `document_topics`.
* **FR-1.4**: Rate-limited crawling with `robots.txt` compliance and pre-flight SSRF perimeter defense.
* **FR-1.5**: Metadata-first intake (`DISCOVERED` tier) to prevent storage bloat.

### Epic 2: Parsing, Snapshots & Epistemic Verification
* **FR-2.1**: Layout-aware parsing of multi-column academic PDFs and web articles into structured markdown sections.
* **FR-2.2**: Representation versioning: Creates immutable `document_snapshots` for each fetched representation (e.g. arXiv v1 vs v2).
* **FR-2.3**: Four-dimensional claim extraction separating Grounding Status (`VERBATIM_MATCH`), Claim Type, Epistemic Status (default `UNASSESSED`), and Evidence Items.
* **FR-2.4**: Quote-level grounding: Validates verbatim substring matching against source text to prevent hallucinations.

### Epic 3: Personal Research Memory (The Long-Lived Asset)
* **FR-3.1**: Persistent storage of verified claims, empirical evidence items, and claim relationships in PostgreSQL.
* **FR-3.2**: User annotations, personal critique notes, experimental logs, and failed hypothesis tracking.
* **FR-3.3**: Exportable, LLM-independent knowledge graphs.

### Epic 4: Research Opportunity Mining & Idea Lineage
* **FR-4.1**: Automated identification of research gaps from paper limitation sections and future work notes.
* **FR-4.2**: Detection of scientific contradictions between opposing publication claims.
* **FR-4.3**: Semantic distinctiveness estimation comparing candidate ideas against retrieved prior art.
* **FR-4.4**: Candidate idea generation with explicit backward Idea Lineage pinned to exact document snapshots:
  $$\text{Idea} \longrightarrow \text{Opportunity} \longrightarrow \text{Gap / Trend / Contradiction} \longrightarrow \text{Claims} \longrightarrow \text{Evidence} \longrightarrow \text{Snapshots} \longrightarrow \text{Documents} \longrightarrow \text{Sources}$$

### Epic 5: Retrieval, Synthesis & Research Handbooks
* **FR-5.1**: Hybrid retrieval combining PostgreSQL full-text lexical search and pgvector cosine similarity (V1 768-dim contract).
* **FR-5.2**: Generation of structured State-of-the-Art (SOTA) comparative literature matrices.
* **FR-5.3**: Automated authoring of comprehensive Research Handbooks with verifiable bibliographic citations.
* **FR-5.4**: Multi-format export (Markdown, LaTeX, PDF).

---

## 5. Non-Functional Requirements

| Dimension | Specification |
| :--- | :--- |
| **Data Durability** | Cloud-first authoritative storage with zero data loss guarantee across multi-device usage. |
| **Idempotency** | 4-tier idempotency architecture guaranteeing safe, non-duplicating pipeline re-runs. |
| **Local Boundary** | Local disk usage is strictly bounded by `MAX_LOCAL_CACHE_GB` (default 10 GB) with automated LRU cleanup. |
| **Security** | Defense-in-depth against SSRF, prompt injection in paper abstracts, and parser resource exhaustion. |
| **Performance** | Hybrid search query latency < 150ms for 50,000+ indexed papers. |
| **Auditability** | Complete telemetry and logging for all background asynchronous tasks. |

---

## 6. End-to-End User Workflows

### Scenario A: Launching a Multi-Topic Research Track (e.g., "Edge AI & Speculative Decoding")
1. Researcher defines Topics in Intel OS with keywords and seed DOIs.
2. Ingestion engine discovers candidate preprints; metadata is reconciled across arXiv and Crossref without duplication.
3. System assigns papers to multiple topics via `document_topics` and promotes high-impact papers to `RETAINED` tier.
4. Parsing engine creates versioned `document_snapshots` and extracts claims with verbatim quote grounding.
5. Opportunity Miner surfaces scientific contradictions and unaddressed hardware limitations.
6. System synthesizes candidate research ideas with complete backward Idea Lineage pinned to exact snapshot versions.
7. Researcher reviews the Idea Lineage, adds personal experiment notes, and exports a LaTeX blueprint.
