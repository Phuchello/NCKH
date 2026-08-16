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

### Epic 1: Multi-Source Ingestion & Politeness (Discovery Layer)
* **FR-1.1**: Multi-channel discovery across academic preprint APIs (arXiv, Crossref, Semantic Scholar, OpenAlex) and user-defined web feeds.
* **FR-1.2**: Automated SHA-256 content hashing, canonical DOI normalization, and URL deduplication.
* **FR-1.3**: Rate-limited crawling with `robots.txt` compliance and SSRF perimeter defense.
* **FR-1.4**: Metadata-first intake (`DISCOVERED` tier) to minimize storage footprint.

### Epic 2: Extraction, Normalization & Claim Verification
* **FR-2.1**: Layout-aware parsing of multi-column academic PDFs and web articles into structured markdown sections (Abstract, Methodology, Results, Discussion).
* **FR-2.2**: Extraction of atomic scientific claims, quantitative metrics, and empirical findings.
* **FR-2.3**: Quote-level grounding: Every extracted claim must record exact source bounding text to prevent hallucinations.
* **FR-2.4**: Automated verification scoring assessing empirical rigor and methodology strength.

### Epic 3: Personal Research Memory (The Long-Lived Asset)
* **FR-3.1**: Persistent storage of verified claims, evidence items, and entity relationships in PostgreSQL.
* **FR-3.2**: User annotations, personal critique notes, experimental logs, and failed hypothesis tracking.
* **FR-3.3**: Entity resolution linking methodologies, datasets, benchmarks, and problem spaces across papers.
* **FR-3.4**: Exportable, LLM-independent knowledge graphs.

### Epic 4: Research Opportunity Mining & Idea Lineage
* **FR-4.1**: Automated identification of research gaps from paper limitation sections and future work notes.
* **FR-4.2**: Detection of scientific contradictions between opposing publication claims.
* **FR-4.3**: Emerging trend velocity analysis tracking keyword acceleration and preprint momentum.
* **FR-4.4**: Idea generation with explicit backward provenance chain:
  `Idea → Opportunity → Gap / Trend / Contradiction → Findings → Claims → Evidence → Documents → Sources`.

### Epic 5: Retrieval, Synthesis & Research Handbooks
* **FR-5.1**: Hybrid retrieval combining PostgreSQL full-text search (BM25) and pgvector cosine similarity.
* **FR-5.2**: Generation of structured State-of-the-Art (SOTA) comparative literature matrices.
* **FR-5.3**: Automated authoring of comprehensive Research Handbooks with verifiable bibliographic citations.
* **FR-5.4**: Multi-format export (Markdown, LaTeX, PDF).

---

## 5. Non-Functional Requirements

| Dimension | Specification |
| :--- | :--- |
| **Data Durability** | Cloud-first authoritative storage with zero data loss guarantee across multi-device usage. |
| **Idempotency** | Ingestion, parsing, and extraction workflows must be 100% idempotent. Re-running jobs produces identical state. |
| **Local Boundary** | Local disk usage is strictly bounded by `MAX_LOCAL_CACHE_GB` (default 10 GB) with automated LRU cleanup. |
| **Security** | Defense-in-depth against SSRF, prompt injection in paper abstracts, and malicious PDF parsers. |
| **Performance** | Hybrid search query latency < 150ms for 50,000+ indexed papers. |
| **Auditability** | Complete telemetry and logging for all background asynchronous tasks. |

---

## 6. End-to-End User Workflows

### Scenario A: Launching a New Research Topic (e.g., "Edge AI Speculative Decoding")
1. Researcher defines Topic in Intel OS with keywords, seed DOIs, and focus criteria.
2. Ingestion engine discovers 500 candidate papers; Tier-1 filter indexes 150 relevant abstracts.
3. System promotes 30 high-impact papers to `RETAINED` tier (PDFs preserved in S3).
4. Extraction engine extracts 180 atomic claims and 45 quantitative benchmarks.
5. Opportunity Miner detects 2 major contradictions and 3 unaddressed hardware gaps.
6. System synthesizes 2 novel research ideas with complete backward lineage graphs.
7. Researcher reviews the Idea Lineage, adds personal experiment notes, and exports a LaTeX blueprint.
