# Intel OS / NCKH Intelligence Platform

> **A Personal Research & Scientific Intelligence Operating System**

[![Milestone](https://img.shields.io/badge/Milestone-G9%20Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G8](https://img.shields.io/badge/G8-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![G9](https://img.shields.io/badge/G9-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Private Verification](https://img.shields.io/badge/Private%20Verification-564%2F564%20passing-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Database](https://img.shields.io/badge/PostgreSQL-16.15%20%2B%20pgvector-blue?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Security S0](https://img.shields.io/badge/Security%20S0-Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Core](https://img.shields.io/badge/Core-Private-black?style=flat-square)](#public-showcase--private-core)
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
            │
            ▼
 Research Console / Learning Workbench
```

Long-term provenance target:

```text
Idea → Opportunity → Gap / Contradiction → Claim → Evidence → Snapshot → Document → Source
```

---

## Current verified progress

Intel OS has now passed the private engineering gates through **G9 — Reliability, Security, Calibration & Comparative Research-Workflow Benchmark**. The public repository intentionally reports only disclosure-safe milestone outcomes; the authoritative implementation and research memory remain private.

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

Several distinctions remain explicit: contradiction candidates are not scientific refutations, semantic distinctiveness is not proof of novelty, system-inferred gaps are not author-stated limitations, generated ideas are candidates rather than validated conclusions, and automated scores remain provisional until calibrated.

### G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis
**Approved after retrieval, citation, model-input authority and verification-evidence hardening.**

```text
PostgreSQL                       16.15
pgvector                         0.8.6
Alembic                          0001 -> 0009
Upgrade / downgrade / upgrade    PASS
Private automated suite          429 / 429 PASS
Statement coverage               90.3%
Verification categories          17 / 17 PASS
Mentor decision                  APPROVED (~99/100)
```

G6 turns accumulated research memory into a query and synthesis layer with PostgreSQL lexical retrieval, pgvector semantic retrieval, deterministic fusion, bounded provenance-rich context, typed synthesis and deterministic citation validation.

The core rule remains: **retrieval and generation do not create evidence**. Retrieval rank is relevance rather than truth; source text remains untrusted data; model-produced citations must resolve to exact evidence actually supplied in the bounded context.

### Security S0 — Security & Privacy Assurance Baseline
**Approved as a cross-cutting V1 maturity baseline.**

S0 covers data/privacy, identity/access, AI/RAG boundaries, application/API risk, infrastructure/storage, software/AI supply chain, incident/recovery thinking and residual-risk tracking. Public reporting remains intentionally high-level; private threat paths and exploit detail stay in the authoritative core.

S0 is an internal engineering assurance baseline, **not a security certification and not an absolute-security claim**.

### G7 — Living Research Output Engine
**Approved.** G7 turns grounded context into durable research outputs while preserving exact context identity, bibliography hydration, citation validation and output verification.

Disclosure/privacy enforcement occurs before any approved provider gateway boundary; private or unapproved data paths fail closed rather than being repaired after dispatch.

### G8 — Research Console & Learning Workbench
**Approved.** G8 adds the human-facing Next.js research console around the existing provenance and output contracts.

Publicly reportable capabilities include:

- research dashboard and evidence exploration;
- provenance/snapshot inspection;
- research-memory notes;
- Output Studio integration;
- Learning Mode bound to the same authoritative context identity;
- epistemic/provisional-status rendering;
- same-origin BFF and CSRF boundary;
- a synthetic/stateless **PUBLIC_DEMO** mode with no private backend requirement.

The interface remains a workbench rather than the final V1 visual design. UX/UI, bilingual Vietnamese/English support and release polish are part of the remaining V1 hardening work.

### G9 — Reliability, Security, Calibration & Comparative Research-Workflow Benchmark
**Approved after replacing the initial benchmark with a real PostgreSQL-backed system benchmark and independent proof derivation.**

Final disclosure-safe verification summary:

```text
Private backend suite             564 / 564 PASS
Failed / skipped                  0 / 0
Statement coverage                88.7%
PostgreSQL                        16.15
pgvector                          0.8.6
Alembic U/D/U                     PASS
G9 proof                          G9-v1.1
Mandatory G9 categories           13 / 13 PASS
Current-gate security regression  10 / 10 PASS
```

G9 executes bounded real-system tasks across evidence discovery, provenance tracing, contradiction visibility, research-memory reuse, verified brief generation, disclosure/provider policy and restart/recovery. Retrieval calibration, deterministic tamper verification and student-scale resource measurements are included.

The automated conventional-workflow comparison is explicitly labeled **AUTOMATED_PROXY**, not human timing. The system does not claim to beat flat-file operations on raw milliseconds; the value being tested is structured provenance, evidence integrity, reusable research memory, recovery and privacy/security assurance. A real owner-run human benchmark remains a separate future acceptance activity.

---

## Engineering principles

- **Purpose before technology.** A method must solve a real project problem and earn its complexity.
- **Provenance before cleverness.** Important outputs should remain traceable to source evidence.
- **Grounding is not truth.** Source presence and scientific validity remain separate dimensions.
- **Retrieval rank is not truth.** Search scores represent relevance signals only.
- **Semantic similarity is not entailment or novelty.** Vector distance has a deliberately narrow meaning.
- **False merge is worse than temporary duplication.** Scholarly identity reconciliation stays conservative.
- **Metadata first.** Discovering a paper does not imply permanently storing its raw file.
- **Selective retention.** Raw artifacts are retained only when value, provenance, licensing, or research use justifies it.
- **Historical reproducibility.** Model/config changes must not silently reinterpret past research-memory state.
- **Local-first development, portable data boundaries.** V1 remains operable at student scale without enterprise infrastructure.
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
- disclosure-safe test/evaluation summaries;
- sanitized screenshots and demos;
- selected benchmark conclusions;
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
| Security S0 | Security/privacy assurance baseline | ✅ Approved |
| G7 | Living research outputs | ✅ Approved |
| G8 | Research console & learning workbench | ✅ Approved |
| G9 | Reliability, calibration & comparative benchmark | ✅ Approved |
| G10 | V1 release, UX/UI/i18n hardening & archival | ▶ Next |
| V1 Acceptance | End-to-end owner acceptance and freeze | 🔒 After G10 |
| V2 | Distributed / evolution research directions | 🔒 Locked until V1 |

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
