# Intel OS / NCKH Intelligence Platform

> **A Personal Research & Scientific Intelligence Operating System**

[![Milestone](https://img.shields.io/badge/Milestone-G5%20Opportunity%20Miner-informational?style=flat-square)](PROJECT_STATE.md)
[![G1](https://img.shields.io/badge/G1-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G2](https://img.shields.io/badge/G2-Approved-success?style=flat-square)](docs/G2_FINAL_REPORT.md)
[![G3](https://img.shields.io/badge/G3-Approved-success?style=flat-square)](docs/G3_REVIEW_REPORT.md)
[![G4](https://img.shields.io/badge/G4-Approved-success?style=flat-square)](docs/G4_REVIEW_REPORT.md)
[![Private CI](https://img.shields.io/badge/Private%20CI-243%2F243%20passing-success?style=flat-square)](docs/G4_REVIEW_REPORT.md)
[![Database](https://img.shields.io/badge/PostgreSQL-16.15%20%2B%20pgvector-blue?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G5](https://img.shields.io/badge/G5-Active-blue?style=flat-square)](PROJECT_STATE.md)
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

See **[G2 Final Gate Report](docs/G2_FINAL_REPORT.md)**.

### G3 — Full-Text Parsing & Quote-Grounded Extraction
**Approved after progressive integrity hardening.**

```text
PostgreSQL 16.15 + pgvector      PASS
Private automated suite          156 / 156 PASS
Coverage                         88%
Mentor decision                  APPROVED (~99/100)
```

G3 provides immutable snapshot/version provenance, deterministic parsing, versioned chunks, character-exact quote grounding, ungrounded-evidence quarantine and reproducible extraction runs.

> **Grounding is not truth.** A verified quote proves that a source contains a statement; it does not prove the statement is scientifically correct.

See **[G3 Final Gate Report](docs/G3_REVIEW_REPORT.md)**.

### G4 — Intelligence Lake & Personal Research Memory
**Approved after three integrity-closure passes.**

Final verified checkpoint:

```text
PostgreSQL 16.15 + pgvector      PASS
Alembic 0001 -> 0007             PASS
Upgrade / downgrade / upgrade    PASS
Private automated suite          243 / 243 PASS
Failed / skipped                 0 / 0
Coverage                         88%
Mentor decision                  APPROVED (~99/100)
```

At a disclosure-safe level, G4 establishes:

```text
Grounded research objects
→ selectively retained artifacts
→ S3-compatible storage boundary
→ compensated/reconcilable retention
→ immutable embedding provenance
→ active pgvector/HNSW semantic index
→ user-authored notes
→ conservative claim relationships
```

The final closure verifies transfer-time bounded S3 reads, post-upload durable metadata checks, commit-failure compensation/reconciliation, version-preserving embedding history, exact source-text identity, provider cardinality/bounds, DB-level embedding-provenance integrity, and strict already-RETAINED idempotency checks.

See **[G4 Final Gate Report](docs/G4_REVIEW_REPORT.md)**.

### G5 — Research Opportunity Miner & Idea Lineage
**Active.** G5 begins the Research Opportunity Memory layer.

```text
Grounded claims / limitations / future work
→ gap candidates
→ contradiction candidates
→ research opportunities
→ candidate ideas
→ snapshot-pinned backward lineage
```

G5 keeps several distinctions explicit: contradiction candidates are not scientific refutations, semantic distinctiveness is not proof of novelty, system-inferred gaps are not author-stated limitations, and generated ideas are candidates rather than validated research conclusions.

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
| G4 | Intelligence Lake / memory storage & embeddings | ✅ Approved |
| G5 | Research gaps / opportunities / idea lineage | 🛠 Active |
| G6 | Hybrid search, retrieval & synthesis | 🔒 Locked until G5 approval |
| G7 | Living handbook / research outputs | Planned |
| G8 | Research console / UX | Planned |
| G9 | Reliability, security & benchmark audit | Planned |
| G10 | Production release & archival | Planned |

---

## Documentation

- [Public Progress & Verified Results](docs/PUBLIC_PROGRESS.md)
- [G2 Final Gate Report](docs/G2_FINAL_REPORT.md)
- [G3 Final Gate Report](docs/G3_REVIEW_REPORT.md)
- [G4 Final Gate Report](docs/G4_REVIEW_REPORT.md)
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
