# Intel OS / NCKH Intelligence Platform

> **A Personal Research & Scientific Intelligence Operating System**

[![Milestone](https://img.shields.io/badge/Milestone-Security%20S0-informational?style=flat-square)](PROJECT_STATE.md)
[![G1](https://img.shields.io/badge/G1-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G2](https://img.shields.io/badge/G2-Approved-success?style=flat-square)](docs/G2_FINAL_REPORT.md)
[![G3](https://img.shields.io/badge/G3-Approved-success?style=flat-square)](docs/G3_REVIEW_REPORT.md)
[![G4](https://img.shields.io/badge/G4-Approved-success?style=flat-square)](docs/G4_REVIEW_REPORT.md)
[![G5](https://img.shields.io/badge/G5-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G6](https://img.shields.io/badge/G6-Approved-success?style=flat-square)](PROJECT_STATE.md)
[![Private CI](https://img.shields.io/badge/Private%20CI-429%2F429%20passing-success?style=flat-square)](PROJECT_STATE.md)
[![Database](https://img.shields.io/badge/PostgreSQL-16.15%20%2B%20pgvector-blue?style=flat-square)](PROJECT_STATE.md)
[![Security S0](https://img.shields.io/badge/Security%20S0-Active-blue?style=flat-square)](PROJECT_STATE.md)
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
 Retrieval + Grounded Synthesis
            │
            ▼
   Living Research Outputs
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

```text
PostgreSQL 16.15 + pgvector      PASS
Alembic 0001 -> 0007             PASS
Upgrade / downgrade / upgrade    PASS
Private automated suite          243 / 243 PASS
Failed / skipped                 0 / 0
Coverage                         88%
Mentor decision                  APPROVED (~99/100)
```

At a disclosure-safe level, G4 establishes selectively retained artifacts, an S3-compatible storage boundary, compensation/reconciliation semantics, immutable embedding provenance, active pgvector/HNSW semantic projections, user-authored notes and conservative claim relationships.

See **[G4 Final Gate Report](docs/G4_REVIEW_REPORT.md)**.

### G5 — Research Opportunity Miner & Snapshot-Pinned Idea Lineage
**Approved after a dedicated semantic-lineage integrity closure.**

```text
G5 initial                       286 / 286 PASS → REVISE (~91/100)
G5.1 final                       297 / 297 PASS → APPROVED (~98/100)
PostgreSQL 16.15 + pgvector      PASS
Alembic 0001 -> 0008             PASS
Upgrade / downgrade / upgrade    PASS
Failed / skipped                 0 / 0
Coverage                         90%
```

G5 establishes the first **Research Opportunity Memory** layer:

```text
Grounded claims / limitations / future work
→ explicit + inferred gap candidates
→ conservative contradiction candidates
→ research opportunities
→ candidate ideas
→ exact snapshot-pinned backward lineage
```

The final integrity boundary rejects semantically incorrect references even when individual UUIDs are real database objects. Idea lineage must remain tied to its true opportunity, supporting gap/contradiction, grounded claim, document and exact immutable snapshot. Provider attribution follows the source observation of that exact snapshot.

Several distinctions remain explicit: contradiction candidates are not scientific refutations, semantic distinctiveness is not proof of novelty, system-inferred gaps are not author-stated limitations, generated ideas are candidates rather than validated conclusions, and automated scores remain provisional until later calibration.

### G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis
**Approved after progressive retrieval, citation, model-input authority and verification-evidence hardening.**

```text
PostgreSQL                       16.15
pgvector                         0.8.6
Alembic                          0001 -> 0009
Upgrade / downgrade / upgrade    PASS
Private automated suite          429 / 429 PASS
Failed / skipped                 0 / 0
Statement coverage               90.3%
Verification proof manifest      v1.2
Verification categories          17 / 17 PASS
Mentor decision                  APPROVED (~99/100)
```

G6 turns the accumulated research memory into a trustworthy query and synthesis layer:

```text
Research Query
→ PostgreSQL lexical retrieval + pgvector semantic retrieval
→ deterministic normalization / deduplication
→ hybrid fusion
→ provenance-rich bounded context
→ typed synthesis
→ deterministic citation validation
→ source-traceable answer
```

The flagship G6 rule is that **retrieval and generation do not create evidence**. Retrieval rank is relevance rather than truth, semantic similarity is not entailment, source text is untrusted data, and every model-produced source citation must resolve to an exact item that was actually supplied in the bounded retrieval context with matching snapshot/document provenance.

The final G6 authority boundary additionally validates model-visible title, truncation state and contradiction-participant metadata before synthesis. Verification evidence uses explicit typed proof references rather than loose substring matching, preventing decoy test names from satisfying proof requirements.

### Security S0 — Threat-Model & Security/Privacy Assurance Baseline
**Active before G7.** Security is being treated as a cross-cutting engineering constraint rather than an end-of-project add-on.

S0 establishes a private, evidence-oriented baseline for data/privacy, identity/access, AI/RAG boundaries, application/API risk, infrastructure/storage, software/AI supply chain, incident response and residual-risk tracking. Public reporting remains intentionally high-level; private threat paths and exploit detail stay in the authoritative core.

S0 is an internal maturity baseline, not a security certification or an absolute-security claim.

---

## Engineering principles

- **Provenance before cleverness.** Important outputs should remain traceable to source evidence.
- **Grounding is not truth.** Source presence and scientific validity remain separate dimensions.
- **Retrieval rank is not truth.** Search scores represent relevance signals only.
- **Semantic similarity is not entailment or novelty.** Vector distance has a deliberately narrow meaning.
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
- sensitive prompts/rules and credentials;
- detailed threat paths, exploit notes and private security findings.

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
| G5 | Research gaps / opportunities / idea lineage | ✅ Approved |
| G6 | Hybrid retrieval & citation-grounded synthesis | ✅ Approved |
| Security S0 | Threat-model & security/privacy assurance baseline | 🛠 Active |
| G7 | Living handbook / research outputs | 🔒 Locked until Security S0 approval |
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
