# Intel OS / NCKH Intelligence Platform

> **A Personal Research & Scientific Intelligence Operating System**

[![Milestone](https://img.shields.io/badge/Milestone-G2%20Review-informational?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G1](https://img.shields.io/badge/G1-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Private CI](https://img.shields.io/badge/Private%20CI-83%2F83%20passing-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Database](https://img.shields.io/badge/PostgreSQL-16%20%2B%20pgvector-blue?style=flat-square)](docs/DATA_MODEL.md)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

---

## What is Intel OS?

**Intel OS** is a long-term research intelligence platform designed to turn large volumes of papers, technical sources, reports, and future research data into a durable, provenance-aware personal research memory.

It is not intended to be another RSS reader, bookmark manager, or one-shot AI summarizer.

Its core loop is:

```text
Collect → Understand → Filter → Verify → Connect → Analyze → Remember → Synthesize
```

The first application domain is **scientific research / NCKH**, with a strong focus on networking, IoT, AIoT, digital twins, AI, cloud/devops, cybersecurity, and adjacent technical research.

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
**Approved.**

Established:

- modular-monolith architecture;
- provenance-first data model;
- cloud-first authoritative storage model;
- staged milestone/gate workflow;
- security and retention principles;
- Personal Research Memory / Opportunity Memory concepts.

### G1 — Database Foundation & Backend Scaffold
**Approved after PostgreSQL hardening.**

Verified baseline includes:

- FastAPI + typed Python backend foundation;
- SQLAlchemy 2.x async + asyncpg;
- PostgreSQL 16 + pgvector;
- staged Alembic migrations;
- 7 foundation tables;
- provider-observation idempotency;
- versioned document snapshot provenance;
- bounded local cache;
- PostgreSQL-backed integration tests;
- GitHub Actions CI.

### G2 — Academic Metadata Ingestion
**Implementation complete in the private core; mentor audit in progress.**

The current private implementation covers:

- arXiv;
- Crossref;
- OpenAlex;
- Semantic Scholar Academic Graph;
- provider-neutral discovery records;
- DOI/arXiv/URL normalization;
- centralized reconciliation;
- resilient async HTTP transport;
- retry/backoff and per-provider rate control;
- SSRF-oriented network safety checks;
- multi-provider provenance;
- ingestion job telemetry.

Latest private validation checkpoint:

```text
PostgreSQL 16.15 + pgvector      PASS
Alembic upgrade/downgrade       PASS
Full automated suite            83 / 83 PASS
Coverage                        86%
G1 regression surface           PASS
G2 PG multi-provider test       PASS
```

Passing tests prove the implemented behavior is internally consistent. G2 remains under adversarial review for identity conflicts, concurrency, transaction failure semantics, provider-policy changes, and network edge cases before G3 is authorized.

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

- **Provenance before cleverness.** AI output must be traceable to evidence where meaningful.
- **False merge is worse than temporary duplication.** Scientific identity reconciliation is conservative.
- **Metadata-first ingestion.** Discovering a source does not mean permanently downloading it.
- **Cloud-first data, local-first development.** A laptop is not the authoritative research-memory store.
- **Strong models only for high-value items.** Cheap deterministic filtering should happen first.
- **No premature custom-LLM training.** Retrieval + structured memory comes first.
- **Gate-based development.** A milestone is not considered complete merely because code was generated.

---

## Public showcase vs private core

This repository is the **public-facing project surface**. It is intentionally kept active and will continue to publish:

- milestone outcomes;
- architecture at a safe level of detail;
- verified test/benchmark summaries;
- screenshots and product demos;
- public research outputs;
- posters, papers, presentations, and selected reproducible artifacts;
- release notes and roadmap progress.

The authoritative G2+ implementation lives in a private core repository. Proprietary implementation details, private research memory, unpublished ideas, prompts, datasets, and strategically sensitive logic are not published by default.

```text
PRIVATE CORE
    implement → test → mentor review → disclosure review
                                  │
                                  ▼
PUBLIC SHOWCASE
    progress → metrics → demos → selected results → publications
```

**Public does not mean open source.** This repository is source-available/proprietary. See [`LICENSE`](LICENSE), [`NOTICE.md`](NOTICE.md), and [`docs/IP_POLICY.md`](docs/IP_POLICY.md).

---

## Roadmap

| Gate | Focus | Status |
|---|---|---|
| G0 | Product & architecture foundation | ✅ Approved |
| G1 | Database foundation & backend scaffold | ✅ Approved |
| G2 | Academic ingestion & connector framework | 🔎 Mentor review |
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

This project is developed as a long-term personal research-engineering platform and NCKH foundation.

---

© 2026 Võ Trọng Phúc. All Rights Reserved.
