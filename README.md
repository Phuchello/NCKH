# Intel OS / NCKH Intelligence Platform

> **A Personal Research & Scientific Intelligence Operating System**

[![Status: G1 Approved](https://img.shields.io/badge/Milestone-G1%20Approved-success?style=flat-square)](PROJECT_STATE.md)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)
[![Repository: Public Showcase](https://img.shields.io/badge/Repository-Public%20Showcase-blueviolet?style=flat-square)](docs/IP_POLICY.md)
[![PostgreSQL + pgvector](https://img.shields.io/badge/Database-PostgreSQL%2016%2B%20%2B%20pgvector-blue?style=flat-square)](docs/DATA_MODEL.md)

---

## Licensing & Intellectual Property

**This repository is publicly viewable but is not open source.**

Intel OS / NCKH is **source-available and proprietary**. Copyright © 2026 Võ Trọng Phúc. All Rights Reserved.

Public visibility is intended for portfolio presentation, academic review, research discussion, evaluation, and demonstration. No open-source license is granted. Rights provided by GitHub's Terms of Service for public repositories remain unaffected; broader reuse, modification, redistribution, deployment, commercialization, or derivative development requires prior written permission from the copyright owner.

See:

- [`LICENSE`](LICENSE) — controlling proprietary source-available license.
- [`NOTICE.md`](NOTICE.md) — ownership and data notice.
- [`docs/IP_POLICY.md`](docs/IP_POLICY.md) — public showcase / private core boundary.

### Repository boundary

```text
PUBLIC: Phuchello/NCKH
    vision • high-level architecture • public docs • demos • selected results

PRIVATE CORE
    proprietary G2+ implementation • research memory • scoring/reasoning internals
    opportunity mining • private prompts • unpublished experiments • private data
```

G0/G1 history was already publicly disclosed. From **Gate 2 onward, new proprietary-core implementation is not to be developed in this public repository** until the private core repository is established.

---

## 1. Executive Overview

**Intel OS / NCKH Intelligence Platform** is a long-term research operating system for discovering, organizing, validating, connecting, and synthesizing scientific and technical knowledge into durable research memory.

It is designed to go beyond an RSS reader, bookmark manager, or disposable chatbot session. The product vision is a continuously evolving intelligence environment that supports research discovery, evidence-grounded analysis, longitudinal knowledge memory, and research-opportunity exploration.

### Core intelligence loop

```text
Collect → Understand → Filter → Verify → Connect → Analyze → Remember → Synthesize
```

The first application domain is scientific research / NCKH, with future support for technology intelligence, networking, AIoT, cloud/devops, cybersecurity, tools, and learning intelligence.

---

## 2. Durable Research Assets

The system treats AI models as replaceable reasoning engines. Long-lived value comes from structured, provenance-aware research assets:

- **Intelligence Lake** — indexed source material and selectively retained evidence.
- **Personal Research Memory** — claims, evidence, relationships, notes, analyses, and evolving understanding.
- **Research Opportunity Memory** — gaps, contradictions, unresolved questions, hypotheses, opportunities, and idea lineage.

Private/user-specific instances of these assets are **not public-repository content**.

---

## 3. Provenance-First Principle

A key product requirement is that important conclusions and research ideas remain traceable to evidence rather than existing as opaque AI output.

Conceptually:

```text
Idea
  ↓
Opportunity / Gap / Contradiction
  ↓
Finding / Claim
  ↓
Evidence
  ↓
Document Snapshot
  ↓
Logical Document
  ↓
Source / Provider Observation
```

The exact private implementation may evolve independently of this public architectural description.

---

## 4. Storage Principles

The authoritative system is **cloud-first**. A developer laptop is treated as a working environment and bounded cache, not the authoritative research-memory store.

| Layer | Intended role |
| :--- | :--- |
| **PostgreSQL 16+** | Structured metadata, provenance, jobs, and research-memory records |
| **pgvector** | Semantic retrieval alongside relational data |
| **S3-compatible object storage** | Selectively retained raw/large artifacts where redistribution/storage rights permit |
| **Local SSD** | Code, fixtures, temporary processing, bounded cache |
| **External HDD** | Optional cold backup/archive; never the live authoritative database |

The system follows a retention funnel: discovery does not imply permanent full-text storage.

---

## 5. Model Strategy

- No premature custom-LLM training.
- External reasoning models remain replaceable.
- Retrieval, structured memory, provenance, and evidence remain independent from any one model provider.
- Specialized small models may be considered later only when enough high-quality labelled data exists for narrow repeatable tasks.

---

## 6. Current Engineering Baseline

**Gate 1 is formally approved.** The verified public baseline includes:

- Python / FastAPI backend foundation
- SQLAlchemy 2.x async + asyncpg
- PostgreSQL 16 + pgvector
- gate-staged Alembic migrations
- seven G1 foundation tables
- provider-observation and snapshot provenance constraints
- bounded local cache manager
- health/status endpoints
- PostgreSQL-backed integration tests
- GitHub Actions CI with PostgreSQL 16 + pgvector

The final G1 CI validation executed the PostgreSQL migration lifecycle and complete test suite successfully.

**Gate 2 implementation is IP-gated:** the academic ingestion/reconciliation core will continue in a private repository, while this repository remains the public project/showcase surface.

---

## 7. Public Documentation Index

- [Architecture Overview](ARCHITECTURE.md)
- [Detailed Architecture](docs/ARCHITECTURE_DETAILED.md)
- [Data Model](docs/DATA_MODEL.md)
- [Product Specification](docs/PRODUCT_SPEC.md)
- [Pipeline](docs/PIPELINE.md)
- [Milestones](docs/MILESTONES.md)
- [Security Model](docs/SECURITY_MODEL.md)
- [Scoring Model](docs/SCORING_MODEL.md)
- [Intelligence Model](docs/INTELLIGENCE_MODEL.md)
- [Architecture Decisions](DECISIONS.md)
- [Project State](PROJECT_STATE.md)
- [Agent Changelog](CHANGELOG_AGENT.md)
- [Backlog](TODO.md)
- [IP & Repository Boundary Policy](docs/IP_POLICY.md)

Some currently public architecture documents originated before the public/private boundary was adopted. Future public updates may intentionally become more abstract than the private implementation.

---

## 8. AI-Assisted Engineering Governance

AI tools may assist development and review, but repository classification rules take precedence over convenience.

- Routine implementation and iteration may be performed by general coding agents.
- Deep architecture/scientific review may use stronger reasoning reviewers.
- Security-, transaction-, migration-, and concurrency-critical work receives additional review when required.
- **No development agent may publish private-core implementation merely because this showcase repository is public.**

---

## 9. Current Status

```text
G0  Foundation & Architecture                  APPROVED
G1  Database Foundation & Backend Scaffold    APPROVED
G2  Academic Ingestion & Connector Framework  AUTHORIZED, PRIVATE-CORE HOLD
```

Next action: establish the private authoritative core repository, then resume G2 there. Public `Phuchello/NCKH` continues as the showcase/documentation surface.
