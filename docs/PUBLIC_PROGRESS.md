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
| G3 — Full-Text Parsing & Quote-Grounded Extraction | 🛠 G3.1 closure after mentor review |
| G4 | 🔒 Locked until G3 final approval |

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
Alembic lifecycle                PASS
Private migration suite          83 / 83 PASS
Coverage                         86%
Original G1 regression surface   PASS
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

**Implementation complete; first mentor decision: REVISE.**

G3 is the first gate that turns selected document representations into source-grounded research objects.

Public pipeline:

```text
Fetched representation
→ immutable snapshot identity
→ deterministic parsing
→ normalized sections/chunks
→ typed claim candidate
→ deterministic quote verification
→ snapshot-pinned evidence
```

### Verified implementation checkpoint

```text
Private CI run                    31925479279
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0002 -> 0003      PASS
Downgrade base / second upgrade   PASS
Full automated suite              134 / 134 PASS
Failed / skipped                  0 / 0
Coverage                          87%
G1/G2 regressions                 PASS
Mentor assessment                 ~88/100 — REVISE
```

### Publicly reportable capability

- bounded-representation retrieval architecture for selected PDF/HTML inputs;
- immutable snapshot identity and content hashing;
- deterministic PDF/HTML parser abstractions;
- section normalization and reference separation;
- deterministic snapshot-pinned chunking;
- dedicated G3 extraction schema for chunks, claims and evidence;
- provider-neutral typed LLM extraction interface with deterministic CI mocks;
- deterministic quote verification;
- new machine-extracted claims default to `UNASSESSED`;
- malformed/encrypted representation failure paths;
- PostgreSQL-backed end-to-end and regression testing.

### Why G3.1 is required

The mentor review deliberately tests stronger invariants than “CI is green.” Closure is focused on:

- true transfer-time representation size bounds;
- strict character-exact `VERBATIM_MATCH` semantics;
- idempotent and version-safe parse/extraction reruns;
- controlled multi-column parser acceptance testing;
- reproducible provider/model/prompt extraction provenance;
- quarantine of ungrounded empirical evidence;
- consistent snapshot/source provenance.

**G4 remains locked.** The existing 134-test suite is the protected G3.1 regression baseline.

Full checkpoint: **[G3 Mentor Review Checkpoint](G3_REVIEW_REPORT.md)**.

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
