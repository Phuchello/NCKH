# Intel OS / NCKH Intelligence Platform

> **A Long-Term Personal Research & Scientific Intelligence Operating System**

[![Status: Gate 0 Completed](https://img.shields.io/badge/Milestone-Gate%200%20Completed-success?style=flat-square)](docs/MILESTONES.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Architecture: Cloud-First Modular Monolith](https://img.shields.io/badge/Architecture-Cloud--First%20Modular%20Monolith-orange?style=flat-square)](ARCHITECTURE.md)
[![PostgreSQL + pgvector](https://img.shields.io/badge/Database-PostgreSQL%20%2B%20pgvector-blue?style=flat-square)](docs/DATA_MODEL.md)

---

## 1. Executive Overview

**Intel OS / NCKH Intelligence Platform** is a dedicated research operating system designed to automate, structure, and accelerate scientific inquiry (Nghiên cứu Khoa học - NCKH).

Unlike standard RSS feed readers, generic news scrapers, or ephemeral chat wrappers, Intel OS functions as a **durable intelligence multiplier**. It systematically discovers, ingests, verifies, connects, and synthesizes scientific discoveries into an evolving, permanent research memory.

### The Core Intelligence Loop

```text
Collect ──► Filter ──► Verify ──► Connect ──► Analyze ──► Remember ──► Synthesize ──► Act
```

1. **Collect**: Multi-source discovery across arXiv, Crossref, Semantic Scholar, open access repositories, and web sources.
2. **Filter**: Aggressive multi-tiered filtering to suppress noise before high-cost extraction.
3. **Verify**: Rigorous evidence-to-claim validation, provenance extraction, and methodology checks.
4. **Connect**: Graph entity resolution, contradiction detection, and research gap mapping.
5. **Analyze**: Multi-factor scoring (relevance, credibility, novelty, feasibility, actionability).
6. **Remember**: Structured persistence into long-lived personal research memory and opportunity banks.
7. **Synthesize**: Provenance-constrained briefing generation, state-of-the-art literature matrices, and research handbooks.
8. **Act**: Generating concrete, actionable research proposals, experimental designs, and paper blueprints.

---

## 2. Three Durable Intellectual Assets

Intel OS explicitly decouples transient AI models from three permanent, high-value intellectual assets:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      INTEL OS INTELLECTUAL ASSETS                       │
├──────────────────────────┬───────────────────────┬──────────────────────┤
│    Intelligence Lake     │   Personal Research   │ Research Opportunity │
│                          │        Memory         │        Memory        │
├──────────────────────────┼───────────────────────┼──────────────────────┤
│ • Discovered metadata    │ • Verified claims     │ • Research gaps      │
│ • Filtered documents     │ • Empirical evidence  │ • Contradictions     │
│ • Full-text indices      │ • Entity relations    │ • Emerging trends    │
│ • Selectively retained   │ • User notes & logs   │ • Idea lineage       │
│   raw evidence (PDF/HTML)│ • Hypotheses state    │ • Feasibility & cost │
└──────────────────────────┴───────────────────────┴──────────────────────┘
```

1. **Intelligence Lake**: Indexes discovered source material and selectively retains raw evidence under a strict multi-tier retention policy.
2. **Personal Research Memory**: The most valuable long-lived user asset. Contains verified claims, empirical evidence, relationships, analyses, topic states, personal notes, experiment logs, and evolving scientific understanding—preserved independently of any specific LLM provider.
3. **Research Opportunity Memory**: A first-class architectural engine managing research gaps, contradictions, emerging trends, candidate opportunities, hypotheses, feasibility evaluations, and complete **Idea Lineage**.

---

## 3. Flagship Requirement: Idea Lineage & Provenance Chain

A research idea must never exist in an opaque vacuum. Intel OS enforces a strict backward and forward provenance chain:

```text
Idea ──► Opportunity ──► Gap / Trend / Contradiction ──► Findings ──► Claims ──► Evidence ──► Documents ──► Sources
```

```text
Research Idea: "Adaptive Multi-Token Speculation for Resource-Constrained Edge LLMs"
  ├── Research Gap: "Speculative decoding fails on latency-variable mobile NPU backends"
  │     ├── Claim: "Draft model verification overhead exceeds speedup on heterogeneous NPUs"
  │     │     └── Paper: "Latency Dynamics of Edge Speculation" (arXiv:2403.xxxxx)
  │     └── Claim: "Fixed lookahead lengths cause pipeline stall under dynamic thermal throttling"
  │           └── Paper: "Thermal-Aware On-Device Inference" (ACM MobileSys 2024)
  ├── Emerging Trend: "Sub-2B parameter compact models with linear attention"
  │     └── Report: "State of Mobile AI 2025"
  └── Contradiction:
        ├── Source A: Claims memory bandwidth is primary bottleneck (IEEE Micro 2024)
        └── Source B: Claims compute kernel dispatch latency dominates (MLSys 2024)
```

---

## 4. Storage Principles & Tiering

The authoritative system is **Cloud-First**. The developer's laptop is never treated as durable storage.

| Tier | Storage Technology | Role & Content |
| :--- | :--- | :--- |
| **Relational Core** | **PostgreSQL 16+** | Topics, sources, documents, claims, evidence, scores, relationships, gaps, opportunities, ideas, user notes, background job telemetry. |
| **Vector Engine** | **pgvector** | Embeddings & semantic retrieval colocated with relational memory for unified transactional queries. |
| **Object Storage** | **S3-Compatible (Cloudflare R2)** | Selectively retained PDFs, HTML snapshots, extracted evidence figures, full raw source artifacts. |
| **Local Laptop** | **Bounded Local Cache** | Source code, test fixtures, temporary parser buffers, bounded working sets (`MAX_LOCAL_CACHE_GB`). |
| **External HDD** | **Cold Backup / Archive** | Periodic database dumps, cold archive datasets, historical raw dumps. *Never run active DB directly from USB.* |

### Multi-Tier Retention Funnel

```text
1,000,000 Discovered (Metadata / Index only in DB)
       ↓
  100,000 Relevant (Extracted clean text & metadata)
       ↓
   10,000 High Value (Retain raw PDF/HTML evidence in S3)
       ↓
    1,000 Core Research Items (Deep archival & continuous synthesis)
```

---

## 5. Model Strategy & Decoupling

* **No Custom Model Training in Early Gates**: The platform prioritizes high-fidelity structured intelligence and reliable retrieval over premature model fine-tuning.
* **LLMs as Replaceable Reasoning Engines**: Claude, Gemini, and OpenAI models are leveraged via structured input/output adapters.
* **Durable Intelligence Asset**: The accumulated relational data, claims, evidence graph, and opportunity lineage form the permanent system value.

---

## 6. Architecture & Tech Stack

* **Backend**: Python 3.11+, FastAPI, SQLAlchemy / asyncpg, Pydantic v2, pgvector.
* **Frontend**: Next.js 15+ (App Router), TypeScript, Vanilla CSS design tokens.
* **Database**: PostgreSQL 16+ with `pgvector` extension.
* **Storage**: AWS S3 / Cloudflare R2 / MinIO (S3-compatible API).
* **Job Execution**: Asynchronous idempotent worker tasks with structured telemetry.

---

## 7. Documentation Index

Detailed architectural specifications and engineering standards are organized under `/docs`:

* [System Architecture Overview](ARCHITECTURE.md)
* [Detailed Technical Architecture](docs/ARCHITECTURE_DETAILED.md)
* [Relational & Vector Data Model](docs/DATA_MODEL.md)
* [Product Specification & Epics](docs/PRODUCT_SPEC.md)
* [Ingestion & Processing Pipeline](docs/PIPELINE.md)
* [Milestones Roadmap (G0–G10)](docs/MILESTONES.md)
* [Security, SSRF & Sandboxing Model](docs/SECURITY_MODEL.md)
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

* **Current Milestone**: **Gate 0 (G0) — Foundation & Architecture Kickoff**
* **Completion Status**: **100% (Ready for Mentor Review)**
* **Active Branch**: `main`