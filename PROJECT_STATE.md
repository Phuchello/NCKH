# Intel OS / NCKH — Public Project State

## Current verified gate state

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** APPROVED (~98/100)
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** APPROVED (~99/100)
- **G4 — Intelligence Lake & Personal Research Memory:** APPROVED (~99/100)
- **G5 — Research Opportunity Miner & Snapshot-Pinned Idea Lineage:** APPROVED (~98/100)
- **G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis:** APPROVED (~99/100)
- **Security S0 — Security/Privacy Assurance Baseline:** APPROVED
- **G7 — Living Research Output Engine:** APPROVED (~99/100)
- **G8 — Research Console & Learning Workbench:** APPROVED (~98–99/100)
- **G9 — Reliability, Security, Calibration & Comparative Research-Workflow Benchmark:** APPROVED (~98–99/100)
- **Current engineering action:** **G10 — V1 Release, UX/UI + Vietnamese/English i18n Hardening & Archival**
- **V1 Acceptance:** LOCKED until G10 approval
- **V2:** LOCKED until V1 acceptance/freeze

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation, private research memory, unpublished opportunities/ideas, sensitive prompts/rules, exploit details and credentials remain in the private authoritative core.

---

## Latest disclosure-safe verification snapshot

The latest accepted G9/G9.1 closure verifies the V1 private core through the reliability/calibration gate:

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

The accepted G9 benchmark is a bounded **real PostgreSQL-backed system benchmark**, not a standalone toy script. Publicly reportable task coverage includes:

```text
Evidence discovery
→ exact provenance tracing
→ contradiction visibility without truth adjudication
→ research-memory reuse
→ verified Evidence Brief generation
→ disclosure/provider-policy enforcement
→ restart / recovery / reseed / tamper verification
```

The benchmark runner records raw results only and the verification layer derives proof independently. A small conventional-workflow comparison is explicitly labeled `AUTOMATED_PROXY`; it is not presented as human timing. Owner-run human acceptance remains separate.

---

## Human-facing V1 status

G8 established the functional Research Console / Learning Workbench. The current interface is intentionally **not considered visually final**.

G10 will harden the release experience with:

- iterative UI/UX review rather than one-shot cosmetic polish;
- responsive layout, visual hierarchy, typography and spacing cleanup;
- loading, empty, error and degraded-state UX;
- beginner-readable onboarding and research-flow clarity;
- **Vietnamese + English first-class interface support** with persisted language choice;
- no automatic translation of paper titles, source quotes, citations, hashes, IDs or user research data;
- preservation of G0–G9 provenance, citation and security invariants during UI work;
- release/recovery/reproducibility and archival cleanup.

---

## Public / private rule

```text
PRIVATE CORE
    implementation → test → mentor review → disclosure review
                                      │
                                      ▼
PUBLIC NCKH
    verified progress → metrics → demos → selected results → publications
```

Public synchronization happens **after a gate is verified/approved**, not after every private implementation commit. This keeps the showcase current without leaking proprietary or unreviewed material.

---

## Exact next action

Proceed to **G10 — V1 Release, UX/UI + VI/EN i18n Hardening & Archival** in the private authoritative core while preserving all approved G0–G9/S0 evidence and invariants.

After G10 mentor approval, run the owner-facing V1 end-to-end acceptance flow before any V1.0 freeze/tag. V2 remains locked until that V1 acceptance is complete.
