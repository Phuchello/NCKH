# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100 final mentor assessment)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** **APPROVED (~98/100)**
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** **ACTIVE**
- **G4 authorization:** **DENIED until G3 mentor approval**

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation remains in the private authoritative core and is disclosed here only at a safe level of detail.

---

## Latest verified engineering evidence

### G1 final checkpoint

```text
PostgreSQL 16 + pgvector           PASS
Alembic lifecycle                  PASS
G1 automated suite                 49 / 49 PASS
Coverage                           91%
GitHub Actions                     PASS
Mentor decision                    APPROVED
```

### G2 final checkpoint

```text
PostgreSQL 16.15 + pgvector       PASS
Alembic upgrade/downgrade/up      PASS
Full automated suite              111 / 111 PASS
Failed / skipped                  0 / 0
Coverage                          86%
Real PostgreSQL concurrency       PASS
Original G1 regressions           PASS
Private GitHub Actions            PASS
Mentor decision                   APPROVED (~98/100)
```

Private CI run ID for the final G2 checkpoint: `31924223739`.

See [`docs/G2_FINAL_REPORT.md`](docs/G2_FINAL_REPORT.md) for the sanitized final gate report.

---

## Publicly reportable G2 capability

The private implementation includes, at a high level:

- academic metadata acquisition from arXiv, Crossref, OpenAlex, and Semantic Scholar;
- provider-neutral discovery records;
- DOI/arXiv/provider identity normalization and reconciliation;
- conservative scholarly-document identity handling;
- explicit identity-conflict preservation;
- provider-observation provenance;
- bounded ingestion jobs and telemetry;
- async HTTP transport, retry/backoff and provider-aware rate control;
- network-safety / SSRF-oriented protections;
- real PostgreSQL concurrency/idempotency tests;
- whole-ingestion-attempt transaction semantics;
- background-job idempotency.

Detailed proprietary implementation is intentionally not mirrored here.

---

## G3 public objective

G3 builds the first source-grounded full-text pipeline:

```text
Fetched representation
→ immutable snapshot
→ layout-aware parse
→ normalized sections/chunks
→ claim candidate
→ exact quote verification
→ evidence record
```

Publicly reportable design principles:

- every parsed/grounded object remains tied to a specific snapshot/version;
- grounding status is separate from scientific truth;
- newly extracted claims default to `UNASSESSED`;
- exact quote verification is deterministic and independent of the model that proposed the claim;
- malformed or ungrounded output is quarantined/rejected;
- embeddings, S3/R2 durable object storage, opportunity mining and frontend work remain deferred.

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

The public repository remains actively maintained at every major gate. It should continue to receive verified metrics, sanitized architecture updates, demos/screenshots, selected benchmarks, release notes, posters, papers and presentations when those artifacts genuinely exist and pass disclosure review.

---

## Exact next action

Complete G3 in the private authoritative core, preserve all G1/G2 invariants, run private PostgreSQL CI, then return for mentor review. **Do not begin G4 before G3 approval.**
