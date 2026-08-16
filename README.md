# Intel OS / NCKH Intelligence Platform

> **A Personal Research & Scientific Intelligence Operating System**

[![Milestone](https://img.shields.io/badge/Milestone-G4.1%20Integrity%20Closure-informational?style=flat-square)](docs/G4_REVIEW_REPORT.md)
[![G1](https://img.shields.io/badge/G1-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G2](https://img.shields.io/badge/G2-Approved-success?style=flat-square)](docs/G2_FINAL_REPORT.md)
[![G3](https://img.shields.io/badge/G3-Approved-success?style=flat-square)](docs/G3_REVIEW_REPORT.md)
[![Private CI](https://img.shields.io/badge/Private%20CI-184%2F184%20passing-success?style=flat-square)](docs/G4_REVIEW_REPORT.md)
[![Database](https://img.shields.io/badge/PostgreSQL-16.15%20%2B%20pgvector-blue?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G5](https://img.shields.io/badge/G5-Locked-orange?style=flat-square)](docs/G4_REVIEW_REPORT.md)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

---

## What is Intel OS?

**Intel OS** is a long-term research intelligence platform for turning papers, technical sources, reports, and future research data into durable, provenance-aware research memory.

It is not intended to be another RSS reader, bookmark manager, one-shot AI summarizer, or generic LLM wrapper.

```text
Collect → Filter → Verify → Connect → Analyze → Remember → Synthesize → Act
```

The first application domain is scientific research / NCKH, with emphasis on networking, IoT, AIoT, digital twins, AI, cloud/devops, cybersecurity, and adjacent technical research.

---

## Core idea

Intel OS is built around three long-lived assets:

- **Intelligence Lake** — discovered sources and selectively retained evidence/artifacts.
- **Personal Research Memory** — claims, notes, relationships, analyses, and evolving understanding.
- **Research Opportunity Memory** — gaps, contradictions, hypotheses, opportunities, and idea lineage.

AI models are treated as **replaceable reasoning engines**. The durable asset is the structured memory and its provenance.

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
 Parse + Ground Evidence
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

Long-term provenance target:

```text
Idea → Opportunity → Gap / Contradiction → Claim → Evidence → Snapshot → Document → Source
```

---

## Current verified progress

### G0 — Foundation & Architecture
**Approved.** Established the modular-monolith direction, provenance-first data model, epistemic model, security principles, retention strategy, and gate-based engineering workflow.

### G1 — Database Foundation & Backend Scaffold
**Approved after real PostgreSQL hardening.**

```text
G1 automated suite               49 / 49 PASS
Coverage                         91%
PostgreSQL migration lifecycle   PASS
Mentor decision                  APPROVED (~96/100)
```

### G2 — Academic Metadata Ingestion & Connector Framework
**Approved after adversarial concurrency, transaction and provider-policy hardening.**

```text
PostgreSQL 16.15 + pgvector      PASS
Private automated suite          111 / 111 PASS
Coverage                         86%
Real PG concurrency suite        PASS
Mentor decision                  APPROVED (~98/100)
```

Publicly reportable capability includes arXiv, Crossref, OpenAlex and Semantic Scholar metadata ingestion; conservative scholarly identity reconciliation; multi-provider provenance; bounded async networking; job idempotency; whole-attempt transactions; and PostgreSQL concurrency testing.

See **[G2 Final Gate Report](docs/G2_FINAL_REPORT.md)**.

### G3 — Full-Text Parsing & Quote-Grounded Extraction
**Approved after progressive integrity hardening.**

```text
PostgreSQL 16.15 + pgvector      PASS
Private automated suite          156 / 156 PASS
Coverage                         88%
Mentor decision                  APPROVED (~99/100)
```

G3 provides streamed representation bounds, immutable snapshot/version provenance, deterministic parsing, versioned chunks, character-exact quote verification, ungrounded-evidence quarantine, immutable extraction-run provenance and bounded provider-neutral extraction contracts.

> **Grounding is not truth.** A verified quote proves that a source contains a statement; it does not prove the statement is scientifically correct.

See **[G3 Final Gate Report](docs/G3_REVIEW_REPORT.md)**.

### G4 — Intelligence Lake & Personal Research Memory
**Implemented; first mentor review = REVISE. G4.1 integrity closure is active.**

Latest verified checkpoint:

```text
PostgreSQL 16.15 + pgvector      PASS
Alembic upgrade/downgrade/up     PASS
Private automated suite          184 / 184 PASS
Failed / skipped                 0 / 0
Coverage                         87%
G1/G2/G3 regression surface      PASS
Mentor decision                  REVISE (~84/100)
```

The private core now contains the first memory/vector foundation:

```text
Grounded snapshot / chunk / claim
→ selective retained-artifact workflow
→ 768-dimension semantic vectors
→ pgvector / HNSW indexing
→ user-authored research notes
→ conservative claim relationships
```

The remaining G4.1 closure is focused on cross-store durability and historical reproducibility: concrete S3-compatible deployment adapter, commit-failure compensation/recovery, version-preserving embedding provenance, source-text identity, and missing adversarial tests.

See **[G4 Mentor Review Checkpoint](docs/G4_REVIEW_REPORT.md)**.

**G5 remains locked until G4 receives final mentor approval.**

---

## Engineering principles

- **Provenance before cleverness.** Important outputs should remain traceable to source evidence.
- **Grounding is not truth.** Source presence and scientific validity remain separate dimensions.
- **False merge is worse than temporary duplication.** Scholarly identity reconciliation stays conservative.
- **Metadata first.** Discovering a paper does not imply permanently storing its raw file.
- **Selective retention.** Raw artifacts are retained only when value, provenance, licensing, or research use justifies it.
- **Historical reproducibility.** Model/config changes must not silently reinterpret past research-memory state.
- **Cloud-first data, local-first development.** The laptop is not the authoritative research-memory store.
- **No premature custom-LLM training.** Retrieval and structured memory come first.
- **Gate-based development.** Green CI is necessary, but not sufficient, for approval.

---

## Public showcase + private core

This repository is the **public-facing project surface** and remains actively maintained.

```text
PRIVATE CORE
    implement → test → mentor review → disclosure review
                                  │
                                  ▼
PUBLIC SHOWCASE
    progress → metrics → demos → selected results → publications
```

### Public by design
- product vision and safe architecture;
- verified milestone outcomes;
- test/evaluation summaries;
- sanitized screenshots and demos;
- selected benchmarks;
- papers, posters, presentations and intentionally released artifacts.

### Private by design
- authoritative G2+ source implementation;
- proprietary reasoning/scoring internals;
- private research memory and datasets;
- raw retained artifacts not licensed for redistribution;
- unpublished experiments and ideas;
- sensitive prompts/rules and credentials.

**Public does not mean open source.** See [`LICENSE`](LICENSE), [`NOTICE.md`](NOTICE.md), and [`docs/IP_POLICY.md`](docs/IP_POLICY.md).

---

## Roadmap

| Gate | Focus | Status |
|---|---|---|
| G0 | Product & architecture foundation | ✅ Approved |
| G1 | Database foundation & backend scaffold | ✅ Approved |
| G2 | Academic ingestion & connector framework | ✅ Approved |
| G3 | Full-text parsing & quote-grounded extraction | ✅ Approved |
| G4 | Intelligence Lake / memory storage & embeddings | 🛠 G4.1 integrity closure |
| G5 | Research gaps / opportunities / idea lineage | 🔒 Locked |
| G6 | Hybrid search, retrieval & synthesis | Planned |
| G7 | Living handbook / research outputs | Planned |
| G8 | Research console / UX | Planned |
| G9 | Reliability, security & benchmark audit | Planned |
| G10 | Production release & archival | Planned |

---

## Documentation

- [Public Progress & Verified Results](docs/PUBLIC_PROGRESS.md)
- [G2 Final Gate Report](docs/G2_FINAL_REPORT.md)
- [G3 Final Gate Report](docs/G3_REVIEW_REPORT.md)
- [G4 Mentor Review Checkpoint](docs/G4_REVIEW_REPORT.md)
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

© 2026 Võ Trọng Phúc. All Rights Reserved.
