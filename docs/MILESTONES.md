# Intel OS / NCKH — Milestones Roadmap (G0–G10)

This document is the public, disclosure-safe roadmap for Intel OS / NCKH. Detailed implementation plans, private security evidence, unpublished research memory and proprietary internals remain in the authoritative private core.

A green CI run alone does not approve a gate; approval requires evidence review against purpose, integrity, security and reproducibility criteria.

---

## Milestone summary

| Gate | Focus | Public status |
|---|---|---|
| G0 | Product & architecture foundation | ✅ Approved |
| G1 | PostgreSQL database foundation & backend scaffold | ✅ Approved |
| G2 | Academic ingestion & connector framework | ✅ Approved |
| G3 | Parsing, snapshots & quote-grounded extraction | ✅ Approved |
| G4 | Intelligence Lake, embeddings & Personal Research Memory | ✅ Approved |
| G5 | Research gaps, contradictions, opportunities & idea lineage | ✅ Approved |
| G6 | Hybrid retrieval & citation-grounded synthesis | ✅ Approved |
| Security S0 | Cross-cutting security/privacy assurance baseline | ✅ Approved |
| G7 | Living Research Output Engine | ✅ Approved |
| G8 | Research Console & Learning Workbench | ✅ Approved |
| G9 | Reliability, calibration & comparative workflow benchmark | ✅ Approved |
| G10 | V1 release, UX/UI, VI/EN i18n, recovery & archival | ▶ Next |
| V1 Acceptance | Owner end-to-end acceptance & V1.0 freeze readiness | 🔒 After G10 |
| V2 | Distributed/evolution research directions | 🔒 After V1 |

---

## G0 — Foundation & Architecture

Established the product philosophy, provenance-first data model, epistemic boundaries, durable research-memory assets, retention strategy, replaceable model boundaries and gate-based engineering rules.

**Status: ✅ Approved.**

## G1 — Database Foundation & Backend Scaffold

Established the executable PostgreSQL/pgvector foundation, async backend contracts, migration lifecycle and bounded local-development behavior.

**Status: ✅ Approved (~96/100).**

## G2 — Academic Ingestion & Connector Framework

Added bounded provider-aware ingestion, SSRF defenses, provider provenance, conservative scholarly identity reconciliation, idempotency and real PostgreSQL concurrency verification.

**Status: ✅ Approved (~98/100).**

## G3 — Parsing & Quote-Grounded Extraction

Added immutable snapshots, deterministic parsing/chunking, extraction provenance, exact quote grounding, bounded model output and quarantine of unsupported evidence.

> Grounding proves source presence; it does not prove scientific truth.

**Status: ✅ Approved (~99/100).**

## G4 — Intelligence Lake & Personal Research Memory

Added disclosure-safe artifact retention boundaries, compensation/reconciliation, immutable embedding provenance, pgvector/HNSW projections, user notes and conservative claim relationships.

**Status: ✅ Approved (~99/100).**

## G5 — Research Opportunity Memory & Idea Lineage

Added gap/contradiction candidates, research opportunities and candidate ideas with exact snapshot-pinned backward lineage. Semantic distinctiveness remains distinctiveness, not novelty proof.

**Status: ✅ Approved (~98/100).**

## G6 — Hybrid Retrieval & Citation-Grounded Synthesis

Added PostgreSQL lexical retrieval, pgvector semantic retrieval, deterministic fusion, bounded provenance-rich context, typed synthesis and deterministic citation validation.

Core rule: **retrieval and generation do not create evidence**.

**Status: ✅ Approved (~99/100).**

## Security S0 — Cross-Cutting Assurance Baseline

Established evidence-oriented security/privacy coverage across data, identity, AI/RAG, application/API, infrastructure/storage, supply-chain and recovery/residual-risk domains.

S0 is an engineering maturity baseline, not a security certification or perfect-security claim.

**Status: ✅ Approved.**

## G7 — Living Research Output Engine

Added authoritative context identity, output planning, bounded synthesis, citation/bibliography validation, durable output verification and pre-dispatch provider/privacy enforcement.

**Status: ✅ Approved (~99/100).**

## G8 — Research Console & Learning Workbench

Added the human-facing Next.js workbench while preserving approved provenance/security contracts: dashboard, evidence exploration, snapshot/source inspection, research-memory notes, Output Studio, Learning Mode, epistemic labels, same-origin BFF/CSRF and a synthetic/stateless PUBLIC_DEMO mode.

The current UI is functional but intentionally not considered the final V1 visual design.

**Status: ✅ Approved (~98–99/100).**

## G9 — Reliability, Security, Calibration & Comparative Workflow Benchmark

G9 was not accepted on its first green CI. The final G9.1 closure uses a real PostgreSQL-backed system benchmark and independent proof derivation.

```text
Private backend suite             564 / 564 PASS
Failed / skipped                  0 / 0
Statement coverage                88.7%
PostgreSQL                        16.15
pgvector                          0.8.6
Alembic U/D/U                     PASS
G9 proof                          G9-v1.1
Mandatory categories              13 / 13 PASS
Current-gate security regression  10 / 10 PASS
```

Real-system task coverage includes evidence discovery, exact provenance, contradiction visibility, research-memory reuse, verified Evidence Brief generation, disclosure/provider policy and restart/recovery/reseed/tamper behavior.

The CI comparison uses an explicitly labeled **AUTOMATED_PROXY**, not human timing. Flat operations are faster in raw milliseconds; Intel OS is evaluated for provenance, integrity, reuse, reproducibility and controlled research context rather than universal lookup latency.

**Status: ✅ Approved (~98–99/100).**

---

## G10 — V1 Release, UX/UI + VI/EN i18n Hardening & Archival

### Purpose
Turn the approved G0–G9 system into a coherent V1 release candidate without weakening provenance, security or reproducibility.

### Planned public-safe focus

- release/reproducibility cleanup;
- reliable local startup/shutdown and recovery guidance;
- workspace/artifact hygiene;
- responsive UI hardening;
- typography, spacing, visual hierarchy and navigation refinement;
- loading/error/empty/degraded-state UX;
- iterative screenshot/local review instead of one-shot cosmetic polish;
- **Vietnamese + English first-class interface support**;
- persisted language preference;
- no automatic translation of source titles, quotes, citations, IDs, hashes or user research data;
- final documentation and archive bookkeeping;
- preparation for owner-facing V1 Acceptance.

### Non-goals

G10 does not introduce unrelated enterprise infrastructure, new model training, microservices, federated learning, RL or speculative V2 architecture merely for novelty.

**Status: ▶ Next.**

---

## V1 Acceptance after G10

G10 approval does not automatically equal V1.0 release. A separate owner-facing acceptance flow must exercise:

```text
source / paper
→ ingest
→ parse + claims/evidence
→ research memory
→ gap/contradiction/opportunity
→ retrieval
→ grounded synthesis
→ verified research output
→ exact citation/provenance inspection
```

Acceptance also covers error states, privacy boundaries, restart/recovery and practical local operation. Only then should V1 be frozen/tagged.

---

## Public synchronization rule

The public repository is synchronized **after verified gate approval**, not after every private implementation commit.

```text
PRIVATE CORE
implement → test → evidence → mentor review → disclosure review
                                             │
                                             ▼
PUBLIC SHOWCASE
verified status → safe metrics → demos → selected results → publications
```

This keeps public progress current while preserving proprietary implementation and unpublished research/IP boundaries.
