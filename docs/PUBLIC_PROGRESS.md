# Intel OS / NCKH — Public Progress & Verified Results

This page is the public milestone mirror for Intel OS / NCKH. It reports verified engineering outcomes and research-facing progress without publishing proprietary private-core implementation by default.

---

## Current status

| Gate / Item | Status |
|---|---|
| G0 — Foundation & Architecture | ✅ Approved |
| G1 — Database Foundation & Backend Scaffold | ✅ Approved |
| Private-core transition | ✅ Validated |
| G2 — Academic Ingestion & Connector Framework | ✅ Approved |
| G3 — Full-Text Parsing & Quote-Grounded Extraction | ✅ Approved |
| G4 — Intelligence Lake & Personal Research Memory | 🛠 G4.2 micro-closure |
| G5 — Opportunity / Idea Lineage | 🔒 Locked |

The public repository remains an active showcase, verified-results surface, and research/publication hub. The authoritative G2+ implementation remains private.

---

## G0 — Foundation & Architecture

```text
G0 initial review       77/100 — REVISE
G0.1                    88/100 — NEAR PASS
G0.2                    APPROVED
```

---

## G1 — Database Foundation & Backend Scaffold

```text
PostgreSQL 16 + pgvector           PASS
Alembic upgrade/downgrade/up       PASS
G1 automated suite                 49 / 49 PASS
Coverage                           91%
Mentor assessment                  ~96/100 — APPROVED
```

---

## G2 — Academic Metadata Ingestion & Connector Framework

**Final decision: APPROVED.**

```text
G2.1                     92 / 92 PASS   → REVISE
G2.2                    107 / 107 PASS  → NEAR PASS
G2.3 final              111 / 111 PASS  → APPROVED (~98/100)
```

Verified scope includes scholarly metadata ingestion, conservative identity reconciliation, provider provenance, bounded async networking, explicit job/transaction semantics and real PostgreSQL concurrency testing.

Full public report: **[G2 Final Gate Report](G2_FINAL_REPORT.md)**.

---

## G3 — Full-Text Parsing & Quote-Grounded Extraction

**Final decision: APPROVED.**

```text
G3 initial    134 / 134 PASS   → REVISE (~88/100)
G3.1          141 / 141 PASS   → NEAR PASS (~96/100)
G3.2          149 / 149 PASS   → NEAR PASS (~97/100)
G3.3 final    156 / 156 PASS   → APPROVED (~99/100)
```

Verified scope includes streamed representation bounds, immutable snapshots, deterministic parsing, versioned chunks, provider-neutral extraction contracts, character-exact quote grounding, ungrounded-evidence quarantine and reproducible extraction history.

Full public report: **[G3 Final Gate Report](G3_REVIEW_REPORT.md)**.

---

## G4 — Intelligence Lake & Personal Research Memory

### Review progression

```text
G4 initial   184 / 184 PASS   → REVISE (~84/100)
G4.1         215 / 215 PASS   → NEAR PASS (~95/100)
G4.2         active           → final sign-off pending
```

### Latest verified G4.1 evidence

```text
Private CI run                    31941431543
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0006              PASS
Downgrade base / second upgrade   PASS
Full automated suite              215 / 215 PASS
Failed / skipped                  0 / 0
Coverage                          88%
Protected regression surface      PASS
Mentor assessment                 NEAR PASS (~95/100)
```

### Publicly reportable capability

- S3-compatible retained-artifact storage boundary with offline adapter validation;
- explicit compensation/reconciliation semantics for cross-store retention rather than distributed-atomicity claims;
- immutable historical embedding provenance plus a separate active pgvector/HNSW projection;
- exact source-text identity and version-sensitive embedding history;
- embedding dimension/cardinality/input/batch/partial-failure protections;
- Personal Research Memory notes with optional-link preservation semantics;
- conservative claim relationships without automatic scientific-status mutation;
- all approved G1–G3 regression behavior preserved.

### G4.2 final micro-closure

The remaining reviewed work is deliberately narrow:

- enforce object-download limits while bytes are being read rather than after full buffering;
- strengthen durable post-upload object verification/reconciliation before the database claims retention success;
- enforce at the database layer that an immutable embedding-provenance row's declared entity type matches its actual foreign-key target.

**G5 remains locked until final G4 approval.**

Full checkpoint: **[G4 Mentor Review Checkpoint](G4_REVIEW_REPORT.md)**.

---

## Review philosophy

A gate is evaluated on more than implementation completeness:

1. deterministic tests;
2. production-dialect behavior;
3. provenance/data-integrity invariants;
4. concurrency and failure semantics;
5. provider/model reproducibility;
6. epistemic correctness;
7. safe public disclosure.

Green CI is necessary, but not sufficient, for gate approval.

---

## Public reporting policy

The public repository reports milestone objective, safe architecture, verified test/evaluation evidence, known limitations, mentor decision, real demos/screenshots, selected benchmarks and research outputs when disclosure permits.

No fabricated benchmark, placeholder screenshot or private-core implementation is published merely for appearance.

---

## Disclosure note

This repository is **source-available/proprietary, not open source**. Public reporting keeps the project assessable while preserving its private core and research/IP boundary.

See [`IP_POLICY.md`](IP_POLICY.md) and the root [`LICENSE`](../LICENSE).
