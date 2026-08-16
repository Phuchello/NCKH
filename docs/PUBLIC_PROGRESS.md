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
| G4 — Intelligence Lake & Personal Research Memory | 🛠 G4.1 integrity closure |
| G5 — Opportunity / Idea Lineage | 🔒 Locked |

The public repository remains an active showcase, verified-results surface, and research/publication hub. The authoritative G2+ implementation remains private.

---

## G0 — Foundation & Architecture

G0 established the architectural and research principles used by later gates: modular-monolith V1 architecture, provenance-first data model, Intelligence Lake / Personal Research Memory / Research Opportunity Memory concepts, cloud-first authoritative storage, metadata-first retention, replaceable reasoning models, and gate-based engineering.

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

Publicly reportable capabilities include FastAPI, SQLAlchemy 2 async + asyncpg, seven foundation tables, multi-provider provenance, normalized URL idempotency, versioned snapshots, bounded local cache, and PostgreSQL-backed CI.

---

## G2 — Academic Metadata Ingestion & Connector Framework

**Final decision: APPROVED.**

```text
G2.1                     92 / 92 PASS   → REVISE
G2.2                    107 / 107 PASS  → NEAR PASS
G2.3 final              111 / 111 PASS  → APPROVED (~98/100)
```

Verified scope includes arXiv, Crossref, OpenAlex and Semantic Scholar metadata ingestion; conservative identity reconciliation; provider provenance; bounded async networking; explicit job/transaction semantics; and real PostgreSQL concurrency testing.

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

Verified scope includes streamed representation bounds, immutable snapshots, deterministic PDF/HTML parsing, versioned chunks, provider-neutral extraction contracts, character-exact quote grounding, ungrounded-evidence quarantine, extraction-run provenance/idempotency and PostgreSQL history-preservation tests.

Full public report: **[G3 Final Gate Report](G3_REVIEW_REPORT.md)**.

---

## G4 — Intelligence Lake & Personal Research Memory

**Implementation checkpoint verified; first mentor decision: REVISE (~84/100).**

### Verified G4 checkpoint

```text
Private CI run                    31936122041
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0005              PASS
Downgrade base / second upgrade   PASS
Full automated suite              184 / 184 PASS
Failed / skipped                  0 / 0
Coverage                          87%
G1/G2/G3 regression surface       PASS
Mentor assessment                 REVISE (~84/100)
```

### Publicly reportable capability

- 768-dimensional vector storage for existing G4 entities (`document_chunks`, `claims`);
- PostgreSQL pgvector + HNSW cosine index validation;
- deterministic offline embedding gateway used in CI;
- Personal Research Memory `user_notes` storage with bounded content and optional-link preservation;
- generic claim relationships with self-link rejection, duplicate-edge idempotency and no automatic scientific-status mutation;
- artifact key safety, deterministic retained-object naming and signed-URL redaction;
- retention promotion happy path/idempotency and hash/size/upload-failure checks;
- all approved G1–G3 regressions preserved.

### Why G4.1 is required

The first mentor audit found several contracts that the 184-test suite does not yet prove:

- a concrete deployment-ready S3-compatible adapter is still missing from the reviewed code surface;
- cross-store compensation must cover the real **upload succeeds → DB commit fails** boundary, not only an earlier flush error;
- embedding model/config changes must preserve historical vector provenance rather than overwrite it;
- embedding provenance must pin the exact source-text identity used to produce each vector;
- provider response cardinality and storage/embedding resource bounds need stronger adversarial validation;
- missing tests include commit-failure recovery, changed-config embedding history, embedding timeout/no-partial-corruption and linked-claim note preservation.

This is an integrity closure, not a reset of G4. **G5 remains locked.**

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

For future gates, this repository publishes milestone objective, safe architecture, verified test/evaluation evidence, known limitations, mentor decision, real demos/screenshots, selected benchmarks, and public research outputs when disclosure permits.

No fabricated benchmark, placeholder screenshot, or private-core implementation is published merely for appearance.

---

## Disclosure note

This repository is **source-available/proprietary, not open source**. Public reporting keeps the project assessable and professionally presentable while preserving its private core and research/IP boundary.

See [`IP_POLICY.md`](IP_POLICY.md) and the root [`LICENSE`](../LICENSE).
