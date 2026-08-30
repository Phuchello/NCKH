# Intel OS — Research Intelligence Operating System

> **A provenance-aware research intelligence platform for building durable, reusable research memory.**  
> *Hệ thống trí tuệ nghiên cứu giúp biến tài liệu rời rạc thành nền tri thức có nguồn gốc, có thể kiểm tra và tái sử dụng lâu dài.*

[![Public Milestone](https://img.shields.io/badge/Public%20Milestone-V1.0.3-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![V1](https://img.shields.io/badge/V1-Frozen%20%2B%20Verified-blue?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Demo](https://img.shields.io/badge/PUBLIC__DEMO-Live-orange?style=flat-square)](https://intel-os-eight.vercel.app/)
[![Private Core](https://img.shields.io/badge/Core-Private-black?style=flat-square)](#public-showcase--private-core)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

**Live PUBLIC_DEMO:** https://intel-os-eight.vercel.app/

> The hosted demo is **synthetic and stateless**. It does not expose the private research database, unpublished research memory, credentials, proprietary implementation, or private evaluation artifacts.

---

## What is Intel OS?

Intel OS is a long-term personal research system for turning fragmented papers, technical sources, notes, evidence, and future research artifacts into a structured knowledge foundation that can be searched, inspected, reused, and synthesized **without losing provenance**.

```text
fragmented research assets
        ↓
collect + normalize + verify
        ↓
versioned evidence + provenance
        ↓
durable research memory
        ↓
connect claims, contradictions, gaps and ideas
        ↓
retrieve + synthesize with traceable context
        ↓
reusable research outputs and future projects
```

Intel OS is **not** a generic chatbot, bookmark manager, one-shot paper summarizer, or an excuse to train a custom model when structured memory and retrieval solve the problem better.

---

## Current public milestone — V1.0.3

V1 is frozen and verified. The current disclosure-safe public milestone mirrors the approved **V1.0.3 Design Level 2 UI Patch** running in production PUBLIC_DEMO.

### What V1 establishes

- provenance-aware ingestion and immutable source snapshots;
- character-exact evidence grounding and structured claims;
- durable Personal Research Memory;
- contradiction, gap, opportunity and idea lineage;
- hybrid lexical + semantic retrieval;
- citation-grounded synthesis;
- Living Research Output Engine;
- Research Console / Learning Workbench;
- explicit `PUBLIC_DEMO` / `PRIVATE_LOCAL` boundaries;
- security, recovery, reproducibility and release verification;
- Vietnamese-first owner UI with coherent English mode.

### V1.0.3 interface refinement

The latest public UI adds a warm beige–orange **Research Intelligence command center** with:

- a Knowledge Landscape / Provenance canvas;
- truthful `Document → Snapshot → Claim` provenance emphasis;
- research gaps displayed separately as provisional intelligence signals;
- contextual inspection on desktop;
- an accessible contextual bottom sheet on mobile;
- keyboard focus management and `Ctrl/Cmd + K` actions;
- bilingual VI/EN presentation without changing research identity or epistemic state.

The visible product generation label remains **V1.0**. `v1.0.3` is a post-freeze interface/release patch, not a new research-core generation.

---

## Why this project exists

Research work tends to fragment across PDFs, browser tabs, notes, spreadsheets, chat histories and temporary AI summaries. The difficult part is not only finding information; it is preserving:

- what source a statement came from;
- which version of the source was used;
- what exact evidence supports it;
- what is still uncertain, provisional or contested;
- what ideas, gaps and experiments were derived from that context;
- how a future output can be traced back to the research state that produced it.

Intel OS treats that accumulated structure as the durable asset. AI models remain replaceable reasoning engines rather than the system of record.

---

## Three product layers

### 1. Gold Knowledge Core

The long-lived research foundation: source identity, immutable/versioned snapshots, evidence, claims, notes, contradictions, gaps, opportunities, ideas and provenance relationships.

### 2. Research Intelligence Layer

Retrieval, comparison, contradiction visibility, gap/opportunity surfacing and grounded synthesis operate on the knowledge core.

> **Grounding is not truth.** A source containing a statement does not automatically make that statement scientifically correct.

### 3. Research Workbench

The human-facing layer for exploring evidence, inspecting provenance, reusing research memory, learning from selected context and creating research outputs.

---

## Research flow

```text
Academic / Technical Sources
            │
            ▼
      Discovery & Ingestion
            │
            ▼
   Versioned Source Snapshots
            │
            ▼
   Parsing + Evidence Grounding
            │
            ▼
      Gold Knowledge Core
            │
      ┌─────┴───────────────┐
      ▼                     ▼
Retrieval / Synthesis   Gaps / Contradictions
      │                     │
      └──────────┬──────────┘
                 ▼
        Research Workbench
                 │
                 ▼
       Reusable Research Outputs
```

The system also preserves longer research lineage where available, while keeping inferred relationships distinct from source-grounded provenance.

---

## Public demo

The public deployment demonstrates the owner-facing Research Console with **synthetic data only**.

Publicly demonstrable surfaces include:

- Research Intelligence command center;
- evidence exploration;
- document and immutable-snapshot inspection;
- provenance / lineage views;
- demo-safe research-memory interaction;
- controlled research-output generation;
- Learning Mode;
- Research Intelligence views;
- Vietnamese / English interface support.

The public demo is intentionally separated from `PRIVATE_LOCAL`, the authoritative private owner workflow backed by persistent research memory.

---

## Verified engineering progress

All V1 gates are now approved and the release path is complete.

| Gate | Focus | Public status |
|---|---|---|
| G0 | Product & architecture foundation | ✅ Approved |
| G1 | Database foundation & backend scaffold | ✅ Approved |
| G2 | Academic ingestion & connector framework | ✅ Approved |
| G3 | Parsing, snapshots & quote-grounded extraction | ✅ Approved |
| G4 | Intelligence Lake & Personal Research Memory | ✅ Approved |
| G5 | Research gaps, opportunities & idea lineage | ✅ Approved |
| G6 | Hybrid retrieval & citation-grounded synthesis | ✅ Approved |
| Security S0 | Security/privacy assurance baseline | ✅ Approved |
| G7 | Living Research Output Engine | ✅ Approved |
| G8 | Research Console & Learning Workbench | ✅ Approved |
| G9 | Reliability, calibration & workflow benchmark | ✅ Approved |
| G10 | V1 release / UX / i18n / recovery / archival | ✅ Approved |
| V1 Acceptance | Owner end-to-end acceptance | ✅ Approved |
| V1 Final Verification | Release evidence + identity closure | ✅ Approved |
| V1.0 | Canonical application freeze | ✅ Released |
| V1.0.3 | Design Level 2 UI patch | ✅ Released / Production |
| V2 | Distributed Research Data Fabric direction | 🔒 Planned, not started |

Disclosure-safe verification snapshot for the current V1 release line:

```text
Private backend suite              589 / 589 PASS
PostgreSQL                         16.15
pgvector                           0.8.6
Alembic upgrade/downgrade/upgrade  PASS
Frontend unit suite                PASS
Owner Playwright journey           PASS
Security regression                PASS
G10 recovery / startup proof       PASS
V1 Acceptance evidence             PASS
V1 Final Verification evidence     PASS
Post-merge release CI              33315205533 — SUCCESS
Production PUBLIC_DEMO health      200 OK
```

These numbers are engineering verification results, **not claims of scientific correctness, production-scale usage, or universal model quality**.

See **[Public Progress & Verified Results](docs/PUBLIC_PROGRESS.md)** for the full gate history and interpretation.

---

## Engineering principles

- **Purpose before technology.** Complexity must solve an actual project problem.
- **Provenance before cleverness.** Important outputs should remain traceable to evidence.
- **Grounding is not truth.** Source presence and scientific validity are separate.
- **Retrieval rank is not truth.** Search scores represent relevance, not correctness.
- **Semantic similarity is not novelty.** Vector distance has a deliberately narrow meaning.
- **False merge is worse than temporary duplication.** Scholarly identity remains conservative.
- **Selective retention.** Discovery does not imply permanently storing every raw file.
- **Historical reproducibility.** Model/config changes should not silently reinterpret past research state.
- **Green CI is necessary, not sufficient.** Gate approval requires review of what the evidence actually proves.

---

## Public showcase + private core

This repository is intentionally a **public showcase**, not the authoritative implementation repository.

```text
PRIVATE CORE
implementation → tests → evidence → mentor review → disclosure review
                                                   │
                                                   ▼
PUBLIC SHOWCASE
vision → architecture → verified progress → demo → selected results
```

### Public by design

- project vision and motivation;
- disclosure-safe architecture;
- verified milestone outcomes;
- safe CI/test/benchmark summaries;
- synthetic demo behavior;
- intentionally released publications and research artifacts.

### Private by design

- authoritative G2+ implementation;
- live schemas/migrations and production internals not intentionally released;
- proprietary ranking, scoring, reconciliation and reasoning logic;
- detailed security/threat paths;
- private research memory, datasets and retained artifacts;
- unpublished gaps, experiments, hypotheses and ideas;
- credentials, prompts and operational configuration.

The earlier public Git history contains foundational implementation that was disclosed before the private-core transition. The current public branch intentionally does **not** mirror the live proprietary codebase.

**Public does not mean open source.** See [LICENSE](LICENSE), [NOTICE.md](NOTICE.md) and [IP / Disclosure Policy](docs/IP_POLICY.md).

---

## Documentation

- **[Architecture Overview](ARCHITECTURE.md)** — disclosure-safe system architecture.
- **[Public Progress & Verified Results](docs/PUBLIC_PROGRESS.md)** — milestone history and verified metrics.
- **[IP / Disclosure Policy](docs/IP_POLICY.md)** — public/private repository boundary.
- **[License](LICENSE)** — proprietary source-available terms.
- **[Notice](NOTICE.md)** — ownership and public-access notice.

The repository is deliberately compact. Detailed engineering state, agent logs, TODOs, migrations, security internals, prompts, private evidence and scoring implementation remain in the private authoritative core.

---

## Author

**Võ Trọng Phúc**  
University of Information Technology — VNU-HCM (UIT)

Developed as a long-term personal research-engineering platform and foundation for future scientific research.

© 2026 Võ Trọng Phúc. All Rights Reserved.
