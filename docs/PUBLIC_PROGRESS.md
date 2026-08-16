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
| G4 — Intelligence Lake & Personal Research Memory | 🚧 Active |

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

Verified baseline:

```text
PostgreSQL 16 + pgvector           PASS
Alembic upgrade/downgrade/up       PASS
G1 automated suite                 49 / 49 PASS
Coverage                           91%
GitHub Actions                     PASS
Mentor assessment                  ~96/100 — APPROVED
```

Publicly reportable capabilities include FastAPI, SQLAlchemy 2 async + asyncpg, seven foundation tables, multi-provider provenance, normalized URL idempotency, versioned snapshots, bounded local cache, and PostgreSQL-backed CI.

---

## Private-core transition

The project uses a **Public Showcase + Private Core** model.

```text
PRIVATE CORE
    authoritative implementation
    proprietary logic
    private data / research memory
    unpublished methods & experiments

PUBLIC SHOWCASE
    architecture overview
    verified progress
    milestone outcomes
    demos / screenshots
    selected benchmark summaries
    papers / posters / presentations
```

After the split, the backend was revalidated rather than assuming migration preserved behavior:

```text
PostgreSQL 16.15 + pgvector       PASS
Alembic lifecycle                 PASS
Private migration suite           83 / 83 PASS
Coverage                           86%
Original G1 regression surface     PASS
```

---

## G2 — Academic Metadata Ingestion & Connector Framework

**Final decision: APPROVED.**

Publicly reportable scope includes arXiv, Crossref, OpenAlex and Semantic Scholar metadata ingestion; provider-neutral discovery; conservative scholarly identity reconciliation; provider provenance; async HTTP resilience; job idempotency; whole-attempt transaction semantics; and real PostgreSQL concurrency testing.

### Review progression

```text
Private split baseline   83 / 83 PASS
G2.1                     92 / 92 PASS   → REVISE
G2.2                    107 / 107 PASS  → NEAR PASS
G2.3 final              111 / 111 PASS  → APPROVED
```

### Final verified G2 evidence

```text
PostgreSQL 16.15 + pgvector       PASS
Alembic upgrade/downgrade/up      PASS
Full automated suite              111 / 111 PASS
Failed / skipped                  0 / 0
Coverage                          86%
Real PostgreSQL concurrency       PASS
Original G1 regression surface    PASS
Private GitHub Actions            PASS
Mentor assessment                 ~98/100 — APPROVED
```

Full public report: **[G2 Final Gate Report](G2_FINAL_REPORT.md)**.

---

## G3 — Full-Text Parsing & Quote-Grounded Extraction

**Final decision: APPROVED.**

G3 turns selected document representations into versioned, source-grounded research objects while keeping grounding separate from scientific truth.

Public pipeline:

```text
Fetched representation
→ immutable snapshot identity
→ deterministic parsing
→ versioned sections/chunks
→ typed claim candidate
→ character-exact quote verification
→ snapshot-pinned evidence
→ immutable extraction-run provenance
```

### Review progression

```text
G3 initial    134 / 134 PASS   → REVISE (~88/100)
G3.1          141 / 141 PASS   → NEAR PASS (~96/100)
G3.2          149 / 149 PASS   → NEAR PASS (~97/100)
G3.3 final    156 / 156 PASS   → APPROVED (~99/100)
```

### Final verified G3 evidence

```text
Private checkpoint                f1379a909d24832446893f1f54afbaae8da288ab
Private CI run                    31927755688
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0004              PASS
Downgrade base / second upgrade   PASS
Full automated suite              156 / 156 PASS
Failed / skipped                  0 / 0
Coverage                          88%
G1/G2 regression surface          PASS
Mentor assessment                 ~99/100 — APPROVED
```

### Publicly reportable capability

- true streamed PDF/HTML representation bounds and content hashing;
- immutable snapshot/source provenance;
- deterministic parser and controlled two-column fixture;
- parser-version-aware chunk history;
- provider-neutral typed extraction interface with deterministic CI mocks;
- character-exact `VERBATIM_MATCH` quote grounding;
- ungrounded-evidence quarantine;
- immutable extraction-run provenance and same-config idempotency;
- bounded extraction input, timeout, claim count, token budget, aggregate response size and reported token usage;
- configuration-sensitive extraction fingerprints and PostgreSQL history coexistence;
- all machine-extracted claims default to `UNASSESSED`.

Full public report: **[G3 Final Gate Report](G3_REVIEW_REPORT.md)**.

---

## G4 — Intelligence Lake & Personal Research Memory

**Status: AUTHORIZED / ACTIVE.**

G4 moves the project from grounded extraction into durable memory/storage primitives. Publicly reportable target architecture is:

```text
Retained artifact bytes
→ immutable snapshot storage pointer
→ versioned semantic embeddings
→ pgvector claim/chunk index
→ user-authored research notes
→ conservative claim relationships
```

G4 implementation remains private. Public updates will report only reviewed outcomes such as storage semantics, vector/index validation, deterministic test metrics, sanitized diagrams/screenshots, and known limitations.

G4 explicitly does **not** yet implement research-gap mining, contradiction detection, opportunity/idea generation, idea lineage, final hybrid retrieval/RRF, synthesis, or frontend work.

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
