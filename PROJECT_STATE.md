# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** APPROVED (~98/100)
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** IMPLEMENTED; mentor decision **REVISE (~88/100)**
- **Current engineering action:** **G3.1 — integrity/provenance closure**
- **G4 authorization:** **DENIED until G3 final approval**

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation remains in the private authoritative core and is disclosed here only at a safe level of detail.

---

## Latest verified engineering evidence

### G1 final

```text
PostgreSQL 16 + pgvector           PASS
Alembic lifecycle                  PASS
G1 automated suite                 49 / 49 PASS
Coverage                           91%
Mentor decision                    APPROVED
```

### G2 final

```text
Private CI run                    31924223739
PostgreSQL 16.15 + pgvector       PASS
Alembic lifecycle                 PASS
Full automated suite              111 / 111 PASS
Coverage                          86%
Real PostgreSQL concurrency       PASS
Mentor decision                   APPROVED (~98/100)
```

### G3 implementation / first mentor review

```text
Private CI run                    31925479279
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0002 -> 0003      PASS
Full automated suite              134 / 134 PASS
Failed / skipped                  0 / 0
Coverage                          87%
G1/G2 regression surface          PASS
Mentor decision                   REVISE (~88/100)
```

G3 green CI is valid engineering evidence, but final approval is intentionally withheld until the stricter grounding/provenance acceptance criteria are closed.

---

## Publicly reportable G3 capability

The private G3 implementation currently includes, at a high level:

- selected PDF/HTML representation retrieval architecture;
- immutable snapshot identity and SHA-256 content hashing;
- deterministic PDF/HTML parser abstractions;
- section normalization and snapshot-pinned chunks;
- dedicated extraction persistence for chunks, claims and evidence;
- typed provider-neutral LLM extraction interface with deterministic mocks;
- deterministic quote verification;
- `UNASSESSED` default for newly extracted claims;
- malformed/encrypted input handling;
- PostgreSQL-backed CI and regression tests.

The active G3.1 closure focuses on true transfer-time resource bounds, character-exact quote grounding, version-safe/idempotent reruns, controlled multi-column evaluation, reproducible extraction metadata, ungrounded-evidence quarantine and source/snapshot consistency.

See:
- [`docs/G3_REVIEW_REPORT.md`](docs/G3_REVIEW_REPORT.md)
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

The public repository remains actively maintained at every major gate. Verified metrics, sanitized architecture updates, demos/screenshots, selected benchmarks, release notes, posters, papers and presentations should be published when those artifacts genuinely exist and pass disclosure review.

---

## Exact next action

Complete **G3.1** in the private authoritative core while preserving the 134-test regression baseline, run PostgreSQL 16 private CI, and return for final G3 mentor review. **Do not begin G4 before G3 approval.**
