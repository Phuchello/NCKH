# Intel OS — Research Intelligence Operating System

> **A provenance-aware research intelligence platform for building durable, reusable research memory.**

[![Public Milestone](https://img.shields.io/badge/Public%20Milestone-G9%20Approved-success?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![V1](https://img.shields.io/badge/V1-Hardening%20in%20Progress-blue?style=flat-square)](docs/PUBLIC_PROGRESS.md)
[![Private Core](https://img.shields.io/badge/Core-Private-black?style=flat-square)](#public-showcase--private-core)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

**PUBLIC_DEMO preview:** https://intel-os-eight.vercel.app/

> The hosted demo is a synthetic/stateless public preview. It does not expose the private research database, credentials, unpublished research memory, or proprietary core implementation.

---

## What is Intel OS?

Intel OS is a long-term personal research system for turning fragmented papers, technical sources, notes, evidence, and future research artifacts into a structured knowledge foundation that can be searched, inspected, reused, and synthesized without losing provenance.

It is designed around one core idea:

```text
fragmented research assets
        ↓
collect + normalize + verify
        ↓
source-grounded research memory
        ↓
connect claims, evidence, gaps and ideas
        ↓
retrieve + synthesize with provenance
        ↓
reusable research outputs and future projects
```

Intel OS is **not** intended to be a generic chatbot, bookmark manager, one-shot paper summarizer, or an excuse to train a custom model when structured memory and retrieval solve the problem better.

---

## Why this project exists

Research work tends to fragment across PDFs, browser tabs, notes, spreadsheets, chat histories and temporary AI summaries. The difficult part is not only finding information; it is preserving:

- what source a statement came from;
- which version of the source was used;
- what evidence supports the statement;
- what is still uncertain or contested;
- what ideas, gaps and experiments were derived from that evidence;
- how a future output can be traced back to its research context.

Intel OS treats that accumulated structure as the durable asset. AI models remain replaceable reasoning engines rather than the system of record.

---

## Three product layers

### 1. Gold Knowledge Core

The long-lived research foundation: source identity, document versions/snapshots, evidence, claims, notes, contradictions, gaps, opportunities, ideas and provenance relationships.

### 2. Research Intelligence Layer

Retrieval, comparison, contradiction visibility, gap/opportunity surfacing and grounded synthesis operate on the knowledge core.

**Grounding is not truth.** A source containing a statement does not automatically make that statement scientifically correct.

### 3. Research Workbench

The human-facing layer for exploring evidence, inspecting provenance, managing research memory, learning from selected evidence and creating research outputs.

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

Long-term provenance target:

```text
Idea → Opportunity → Gap / Contradiction → Claim → Evidence → Snapshot → Document → Source
```

---

## Public demo

The public deployment demonstrates the owner-facing Research Console with synthetic data only.

Publicly demonstrable surfaces include:

- research dashboard;
- evidence exploration;
- document/version inspection;
- provenance and idea-lineage views;
- research-memory interaction in demo-safe form;
- research output generation with disclosure boundaries;
- Learning Mode;
- Research Intelligence views;
- Vietnamese / English interface support.

The public demo is intentionally separated from `PRIVATE_LOCAL`, which is the private owner workflow backed by the authoritative research environment.

---

## Verified engineering progress

The public milestone mirror currently reports verified private-core outcomes through **G9**. G10/V1 hardening is still under private review and is **not** presented here as approved until the gate is actually closed.

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
| G10 | V1 release / UX / i18n / recovery / archival | 🔄 Private hardening |
| V1 Acceptance | Owner end-to-end acceptance | 🔒 After G10 |
| V2 | Evolution / distributed research directions | 🔒 After V1 |

Disclosure-safe G9 verification snapshot:

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

See **[Public Progress & Verified Results](docs/PUBLIC_PROGRESS.md)** for the gate history and interpretation of these numbers.

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
- high-level architecture;
- verified milestone outcomes;
- disclosure-safe metrics and benchmark summaries;
- synthetic screenshots and demos;
- selected public research outputs and publications.

### Private by design

- authoritative G2+ implementation;
- schemas/migrations and production internals not intentionally released;
- proprietary ranking, scoring, reconciliation and reasoning logic;
- detailed security/threat paths;
- private research memory, datasets and raw retained artifacts;
- unpublished gaps, experiments, hypotheses and ideas;
- credentials, prompts and operational configuration.

The earlier public Git history contains foundational implementation that was already disclosed before the private-core transition. The current public branch intentionally does not mirror the live proprietary codebase.

**Public does not mean open source.** See [LICENSE](LICENSE), [NOTICE.md](NOTICE.md) and [IP / Disclosure Policy](docs/IP_POLICY.md).

---

## Documentation

- **[Architecture Overview](ARCHITECTURE.md)** — disclosure-safe system architecture.
- **[Public Progress & Verified Results](docs/PUBLIC_PROGRESS.md)** — milestone history and verified metrics.
- **[IP / Disclosure Policy](docs/IP_POLICY.md)** — public/private repository boundary.
- **[License](LICENSE)** — proprietary source-available terms.
- **[Notice](NOTICE.md)** — ownership and public-access notice.

The repository is deliberately kept compact. Detailed engineering state, agent logs, TODOs, migrations, security internals and scoring implementation live only in the private authoritative core.

---

## Author

**Võ Trọng Phúc**  
University of Information Technology — VNU-HCM (UIT)

Developed as a long-term personal research-engineering platform and foundation for future scientific research.

© 2026 Võ Trọng Phúc. All Rights Reserved.
