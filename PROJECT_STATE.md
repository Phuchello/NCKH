# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** APPROVED (~98/100)
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** APPROVED (~99/100)
- **G4 — Intelligence Lake & Personal Research Memory:** IMPLEMENTED; first mentor decision **REVISE (~84/100)**
- **Current engineering action:** **G4.1 — Storage Consistency & Embedding Provenance Closure**
- **G5 authorization:** **DENIED until G4 final approval**

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation remains in the private authoritative core and is disclosed here only at a safe level of detail.

---

## Latest verified engineering evidence

### G3 final

```text
Private CI run                    31927755688
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0004              PASS
Full automated suite              156 / 156 PASS
Coverage                          88%
Mentor decision                   APPROVED (~99/100)
```

### G4 implementation / first mentor review

```text
Private CI run                    31936122041
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0005              PASS
Downgrade base / second upgrade   PASS
Full automated suite              184 / 184 PASS
Failed / skipped                  0 / 0
Coverage                          87%
G1/G2/G3 regression surface       PASS
Mentor decision                   REVISE (~84/100)
```

The green G4 suite is valid evidence for the behaviors it exercises, but final approval is intentionally withheld until cross-store durability and embedding-history provenance are proven under failure/version-change cases.

---

## Publicly reportable G4 capability

At a disclosure-safe level, the private G4 implementation currently includes:

- 768-dimensional semantic-vector storage for document chunks and claims;
- PostgreSQL pgvector + HNSW cosine indexing with controlled integration tests;
- deterministic offline embedding mocks for CI;
- Personal Research Memory user-note persistence with bounded content and optional-link preservation;
- conservative claim-to-claim relationship storage without automatic epistemic-status mutation;
- artifact key safety, deterministic retained-artifact naming and signed-URL redaction;
- retention promotion happy-path/idempotency plus hash/size/upload-failure checks;
- full regression of approved G1–G3 behavior.

The active G4.1 closure focuses on:

1. concrete S3-compatible deployment adapter;
2. upload-success / DB-commit-failure compensation or reconciliation semantics;
3. version-preserving embedding provenance across model/config changes;
4. exact source-text identity for every vector;
5. response-cardinality and resource-bound enforcement;
6. missing adversarial PostgreSQL/storage tests.

See:
- [`docs/G4_REVIEW_REPORT.md`](docs/G4_REVIEW_REPORT.md)
- [`docs/PUBLIC_PROGRESS.md`](docs/PUBLIC_PROGRESS.md)

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

The public repository remains actively maintained at every major gate. Verified metrics, sanitized architecture updates, demos/screenshots, selected benchmarks, release notes, posters, papers and presentations are published only when they genuinely exist and pass disclosure review.

---

## Exact next action

Complete **G4.1** in the private authoritative core while preserving the 184-test regression baseline, run PostgreSQL 16 + pgvector CI, and return for final G4 mentor review. **Do not begin G5 before G4 approval.**
