# Intel OS / NCKH Intelligence Platform

> **A Personal Research & Scientific Intelligence Operating System**

[![Milestone](https://img.shields.io/badge/Milestone-G2.3%20Final%20Closure-informational?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G1](https://img.shields.io/badge/G1-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Private CI](https://img.shields.io/badge/Private%20CI-107%2F107%20passing-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Database](https://img.shields.io/badge/PostgreSQL-16.15%20%2B%20pgvector-blue?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G3](https://img.shields.io/badge/G3-Locked-orange?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

---

## What is Intel OS?

**Intel OS** is a long-term research intelligence platform designed to turn large volumes of papers, technical sources, reports, and future research data into a durable, provenance-aware personal research memory.

It is not intended to be another RSS reader, bookmark manager, or one-shot AI summarizer.

```text
Collect → Understand → Filter → Verify → Connect → Analyze → Remember → Synthesize
```

The first application domain is **scientific research / NCKH**, with emphasis on networking, IoT, AIoT, digital twins, AI, cloud/devops, cybersecurity, and adjacent technical research.

---

## Why this project exists

Research discovery is fragmented: papers live in different indexes, evidence is easy to lose, repeated searches waste time, and useful ideas are often disconnected from the sources that inspired them.

Intel OS is being built around three long-lived assets:

- **Intelligence Lake** — discovered sources and selectively retained evidence.
- **Personal Research Memory** — claims, notes, relationships, analyses, and evolving understanding.
- **Research Opportunity Memory** — gaps, contradictions, hypotheses, opportunities, and idea lineage.

AI models are treated as **replaceable reasoning engines**. The durable asset is the structured research memory and its provenance.

---

## System concept

```text
Academic / Technical Sources
            │
            ▼
      Source Collection
            │
            ▼
 Normalize + Reconcile
            │
            ▼
   Evidence / Provenance
            │
            ▼
 Intelligence Analysis
            │
            ▼
 Personal Research Memory
            │
            ▼
 Gaps / Opportunities / Ideas
            │
            ▼
   Living Research Handbook
```

Important conclusions are intended to remain traceable through a lineage such as:

```text
Idea → Opportunity → Gap / Contradiction → Claim → Evidence → Snapshot → Document → Source
```

---

## Current verified progress

### G0 — Foundation & Architecture
**Approved.** Established the modular-monolith direction, provenance-first data model, cloud-first storage model, gate workflow, security/retention principles, and long-lived research-memory concepts.

### G1 — Database Foundation & Backend Scaffold
**Approved after real PostgreSQL hardening.** The verified baseline includes FastAPI, SQLAlchemy 2.x async + asyncpg, PostgreSQL 16 + pgvector, staged Alembic migrations, seven foundation tables, provenance/idempotency constraints, bounded local cache, health/status endpoints, and PostgreSQL-backed CI.

Final G1 checkpoint:

```text
G1 automated suite               49 / 49 PASS
Coverage                         91%
PostgreSQL migration lifecycle   PASS
GitHub Actions                   PASS
Mentor decision                  APPROVED (~96/100)
```

### G2 — Academic Metadata Ingestion
**Implemented in the private core and now at final adversarial closure.**

Publicly reportable scope includes:

- arXiv, Crossref, OpenAlex, and Semantic Scholar ingestion paths;
- provider-neutral discovery records;
- DOI/arXiv/URL normalization;
- conservative multi-provider reconciliation;
- provider-observation provenance;
- resilient async HTTP transport, retry/backoff, rate control, and network-safety checks;
- bounded ingestion jobs and telemetry;
- PostgreSQL-backed concurrency and integration testing;
- provider-identity database invariant;
- whole-ingestion-attempt atomicity and explicit background-job idempotency semantics.

Latest verified G2.2 checkpoint:

```text
PostgreSQL 16.15 + pgvector      PASS
Alembic upgrade/downgrade       PASS
Full private automated suite    107 / 107 PASS
Coverage                        86%
G1 regression surface           PASS
Real PG concurrency suite       PASS
Private GitHub Actions          PASS
Mentor review                   NEAR PASS (~95/100)
```

The remaining closure is deliberately narrow: one provider-identity concurrency artifact must be eliminated and regression-tested before G2 can be formally approved. **G3 remains locked until that final invariant is proven.**

Full public milestone report: **[docs/PUBLIC_PROGRESS.md](docs/PUBLIC_PROGRESS.md)**

---

## Technology direction

| Layer | Direction |
|---|---|
| Web | Next.js + TypeScript |
| API / Intelligence backend | FastAPI + Python |
| Structured memory | PostgreSQL 16+ |
| Semantic retrieval | pgvector |
| Large artifacts | S3-compatible object storage |
| Background execution | Lightweight jobs/workers |
| Local machine | Development + bounded cache |
| Cold backup | Optional external HDD / archive |

The V1 architecture intentionally avoids premature microservices, Kafka, Kubernetes, and unnecessary infrastructure.

---

## Research / engineering principles

- **Provenance before cleverness.** Important AI output should remain traceable to evidence.
- **False merge is worse than temporary duplication.** Scientific identity reconciliation is conservative.
- **Metadata-first ingestion.** Discovering a source does not imply permanent full-text storage.
- **Cloud-first data, local-first development.** A laptop is not the authoritative research-memory store.
- **Strong models only for high-value items.** Cheap deterministic filtering should happen first.
- **No premature custom-LLM training.** Retrieval + structured memory comes first.
- **Gate-based development.** Generated code is not considered a completed milestone until verification and review pass.

---

## Public showcase vs private core

This repository is the **public-facing project surface** and remains actively maintained. It publishes verified progress without exposing proprietary core implementation by default.

```text
PRIVATE CORE
    implement → test → mentor review → disclosure review
                                  │
                                  ▼
PUBLIC SHOWCASE
    progress → metrics → demos → selected results → publications
```

Public releases may include milestone outcomes, safe architecture descriptions, verified metrics, screenshots/demos, selected benchmark results, posters, papers, presentations, and intentionally released artifacts.

Private by default: proprietary implementation, private research memory, unpublished ideas/experiments, sensitive prompts/rules, private datasets, credentials, and strategically sensitive algorithms.

**Public does not mean open source.** See [`LICENSE`](LICENSE), [`NOTICE.md`](NOTICE.md), and [`docs/IP_POLICY.md`](docs/IP_POLICY.md).

---

## Roadmap

| Gate | Focus | Status |
|---|---|---|
| G0 | Product & architecture foundation | ✅ Approved |
| G1 | Database foundation & backend scaffold | ✅ Approved |
| G2 | Academic ingestion & connector framework | 🛠 G2.3 final race-artifact closure |
| G3 | Cleaning, full-text processing & extraction foundation | 🔒 Locked |
| G4 | Intelligence extraction & scoring | Planned |
| G5 | Research gaps / opportunities / idea lineage | Planned |
| G6 | Knowledge memory & retrieval | Planned |
| G7 | Living handbook / synthesis | Planned |
| G8 | Product dashboard / UX | Planned |
| G9 | Reliability, security & performance | Planned |
| G10 | Final release audit | Planned |

---

## Documentation

- [Public Progress & Verified Results](docs/PUBLIC_PROGRESS.md)
- [Product Specification](docs/PRODUCT_SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [Detailed Architecture](docs/ARCHITECTURE_DETAILED.md)
- [Data Model](docs/DATA_MODEL.md)
- [Pipeline](docs/PIPELINE.md)
- [Milestones](docs/MILESTONES.md)
- [Security Model](docs/SECURITY_MODEL.md)
- [Intelligence Model](docs/INTELLIGENCE_MODEL.md)
- [Scoring Model](docs/SCORING_MODEL.md)
- [IP / Disclosure Policy](docs/IP_POLICY.md)

---

## Author

**Võ Trọng Phúc**  
University of Information Technology — VNU-HCM (UIT)

Developed as a long-term personal research-engineering platform and NCKH foundation.

---

© 2026 Võ Trọng Phúc. All Rights Reserved.
