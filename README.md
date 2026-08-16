# Intel OS / NCKH Intelligence Platform

> **A Long-Term Personal Research & Scientific Intelligence Operating System**

[![Status: Gate 0.2 Completed](https://img.shields.io/badge/Milestone-Gate%200.2%20Completed-success?style=flat-square)](docs/MILESTONES.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Architecture: Cloud-First Modular Monolith](https://img.shields.io/badge/Architecture-Cloud--First%20Modular%20Monolith-orange?style=flat-square)](ARCHITECTURE.md)
[![PostgreSQL + pgvector](https://img.shields.io/badge/Database-PostgreSQL%2016%2B%20%2B%20pgvector-blue?style=flat-square)](docs/DATA_MODEL.md)

---

## 1. Executive Overview

**Intel OS / NCKH Intelligence Platform** is a dedicated research operating system designed to automate, structure, and accelerate scientific inquiry (Nghiên cứu Khoa học - NCKH).

Unlike standard RSS feed readers, generic news scrapers, or ephemeral chat wrappers, Intel OS functions as a **durable intelligence multiplier**. It systematically discovers, ingests, verifies, connects, and synthesizes scientific discoveries into an evolving, permanent research memory.

### The Core Intelligence Loop

```text
Collect ──► Filter ──► Verify ──► Connect ──► Analyze ──► Remember ──► Synthesize ──► Act
```

1. **Collect**: Multi-provider discovery across arXiv, Crossref, Semantic Scholar, OpenAlex, and web feeds with canonical deduplication.
2. **Filter**: Aggressive multi-tiered retention funnel (`DISCOVERED → INDEXED → RELEVANT → RETAINED → ARCHIVED`) to prevent storage bloat.
3. **Verify**: Rigorous 4D epistemic extraction separating Grounding Status (`VERBATIM_MATCH`), Claim Type, Epistemic Status (default `UNASSESSED`), and Evidence Quality.
4. **Connect**: Cross-paper entity resolution, claim-to-claim logic relationships, and scientific contradiction detection.
5. **Analyze**: Multi-factor scoring (relevance, source credibility prior, evidence rigor, semantic distinctiveness).
6. **Remember**: Structured persistence into long-lived personal research memory and opportunity banks.
7. **Synthesize**: Provenance-constrained literature matrices, state-of-the-art briefings, and research handbooks.
8. **Act**: Generating actionable research proposals and blueprints with snapshot-pinned Idea Lineage.

---

## 2. Three Durable Intellectual Assets

Intel OS explicitly decouples transient AI reasoning models from three permanent, high-value intellectual assets:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      INTEL OS INTELLECTUAL ASSETS                       │
├──────────────────────────┬───────────────────────┬──────────────────────┤
│    Intelligence Lake     │   Personal Research   │ Research Opportunity │
│                          │        Memory         │        Memory        │
├──────────────────────────┼───────────────────────┼──────────────────────┤
│ • Discovered metadata    │ • Verified claims     │ • Research gaps      │
│ • Multi-topic mappings   │ • Empirical evidence  │ • Contradictions     │
│ • Versioned snapshots    │ • Claim relationships │ • Semantic distance  │
│ • Selectively retained   │ • User notes & logs   │ • Idea lineage       │
│   raw files (PDF/HTML)   │ • Hypotheses state    │ • Feasibility & cost │
└──────────────────────────┴───────────────────────┴──────────────────────┘
```

1. **Intelligence Lake**: Indexes discovered source material across providers, manages many-to-many topic mappings (`document_topics`), representation versions (`document_snapshots`), and selectively retains raw evidence under a strict multi-tier retention policy.
2. **Personal Research Memory**: The most valuable long-lived user asset. Contains grounded atomic claims, empirical evidence items, logic relationships, personal notes, experiment logs, and evolving scientific understanding—preserved independently of any specific LLM provider.
3. **Research Opportunity Memory**: A first-class architectural engine managing research gaps, scientific contradictions, semantic distinctiveness signals, candidate hypotheses, feasibility evaluations, and complete **Idea Lineage**.

---

## 3. Flagship Requirement: Snapshot-Pinned Idea Lineage

A research idea must never exist in an opaque vacuum. Intel OS enforces a strict backward and forward provenance chain:

$$\text{Idea} \longrightarrow \text{Opportunity} \longrightarrow \text{Gap / Contradiction} \longrightarrow \text{Claims} \longrightarrow \text{Evidence} \longrightarrow \text{Snapshots} \longrightarrow \text{Documents} \longrightarrow \text{Sources}$$

```text
Research Idea: "Adaptive Multi-Token Speculation for Resource-Constrained Edge LLMs"
  ├── Research Gap: "Speculative decoding fails on latency-variable mobile NPU backends"
  │     ├── Claim: "Draft model verification overhead exceeds speedup on heterogeneous NPUs"
  │     │     └── Evidence: Table 2 - Latency Breakdown
  │     │           └── Snapshot: arXiv v2 PDF (arXiv:2403.xxxxx)
  │     └── Claim: "Fixed lookahead lengths cause pipeline stall under dynamic thermal throttling"
  │           └── Evidence: Figure 5 - Thermal Profiles
  │                 └── Snapshot: Camera-Ready PDF (ACM MobileSys 2024)
  └── Contradiction:
        ├── Source A Claim: Memory bandwidth is primary bottleneck (Snapshot: IEEE Micro 2024)
        └── Source B Claim: Compute kernel dispatch latency dominates (Snapshot: MLSys 2024)
```

---

## 4. Storage Principles & Tiering

The authoritative system is **Cloud-First**. The developer's laptop is never treated as durable storage.

| Tier | Storage Technology | Role & Content |
| :--- | :--- | :--- |
| **Relational Core** | **PostgreSQL 16+** | 18 normalized tables: topics, sources, documents, snapshots, claims, evidence, relationships, gaps, opportunities, ideas, user notes, background job telemetry. |
| **Vector Engine** | **pgvector** | Embeddings & semantic retrieval colocated with relational memory under a fixed **V1 768-dim Embedding Contract**. |
| **Object Storage** | **S3-Compatible (Cloudflare R2)** | Selectively retained snapshot PDFs, HTML snapshots, extracted evidence figures, full raw source artifacts. |
| **Local Laptop** | **Bounded Local Cache** | Source code, test fixtures, temporary parser buffers, bounded working sets (`MAX_LOCAL_CACHE_GB = 10G`). |
| **External HDD** | **Cold Backup / Archive** | Periodic database dumps, cold archive datasets, historical raw dumps. *Never run active DB directly from USB.* |

### Multi-Tier Retention Funnel

```text
1,000,000 Discovered (Metadata / Fingerprint in PostgreSQL)
       ↓
  100,000 Indexed (Abstract, keywords, fast embeddings)
       ↓
   10,000 Relevant (Parsed clean text & document_snapshots)
       ↓
    1,000 Retained (Raw PDF/HTML evidence in S3 Object Storage)
       ↓
      100 Deep Archival (Periodic long-term backup)
```

---

## 5. Model Strategy & Decoupling

* **No Custom Model Training in Early Gates**: The platform prioritizes high-fidelity structured intelligence and reliable retrieval over premature model fine-tuning.
* **LLMs as Replaceable Reasoning Engines**: Claude, Gemini, and OpenAI models are leveraged via structured input/output adapters.
* **Versioned Embedding Contract**: Vector dimensions are fixed at 768 in V1 for schema consistency; upgrading dimensions follows an explicit table migration protocol.

---

## 6. Architecture & Tech Stack

* **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0 / asyncpg, Pydantic v2, pgvector.
* **Frontend**: Next.js 15+ (App Router), TypeScript, Vanilla CSS design tokens.
* **Database**: PostgreSQL 16+ with `pgvector` extension (18 normalized tables).
* **Storage**: AWS S3 / Cloudflare R2 / MinIO (S3-compatible API).
* **Job Execution**: Asynchronous idempotent worker tasks with 4-tier idempotency.

---

## 7. Documentation Index

Detailed architectural specifications and engineering standards are organized under `/docs`:

* [System Architecture Overview](ARCHITECTURE.md)
* [Detailed Technical Architecture](docs/ARCHITECTURE_DETAILED.md)
* [Relational & Vector Data Model (18 Tables)](docs/DATA_MODEL.md)
* [Product Specification & Epics](docs/PRODUCT_SPEC.md)
* [Ingestion & Processing Pipeline](docs/PIPELINE.md)
* [Milestones Roadmap (G0–G10)](docs/MILESTONES.md)
* [Security & Threat Mitigation Model](docs/SECURITY_MODEL.md)
* [Multi-Factor Scoring Model](docs/SCORING_MODEL.md)
* [Intelligence & Epistemic Ontology](docs/INTELLIGENCE_MODEL.md)
* [Architecture Decision Records (ADRs)](DECISIONS.md)
* [Project State & Safety Checkpoint](PROJECT_STATE.md)
* [Agent Development Changelog](CHANGELOG_AGENT.md)
* [Engineering Task Backlog](TODO.md)

---

## 8. AI Agent Governance Policy

Engineering tasks on Intel OS are divided across specialized AI roles:
* **Gemini / Antigravity**: Primary agent for architecture exploration, comprehensive documentation, scaffolding, routine backend/frontend development, unit/integration testing, API integrations, and UI workflows.
* **Codex**: Reserved strictly for high-concurrency debugging, idempotency verification, transaction isolation audits, complex migrations, security-critical implementations, and final engineering audits.

---

## 9. Current Status

* **Current Milestone**: **Gate 0.2 (G0.2) — Data-Integrity Hardening**
* **Status**: **100% Completed (Ready for Mentor Re-Audit)**
* **Active Branch**: `main`