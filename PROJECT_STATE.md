# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100 final mentor assessment)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** IMPLEMENTED; G2.1 adversarial hardening completed; mentor decision **REVISE**
- **Current engineering action:** **G2.2 — concurrency, identity-agreement & job-semantics closure**
- **G3 authorization:** **DENIED until G2 final approval**

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation is maintained in the private authoritative core and is disclosed here only at a safe level of detail.

---

## Latest verified engineering evidence

### G1 final checkpoint

```text
PostgreSQL 16 + pgvector           PASS
Alembic lifecycle                 PASS
G1 automated suite                49 / 49 PASS
Coverage                          91%
GitHub Actions                    PASS
Mentor decision                   APPROVED
```

### Private-core migration checkpoint

```text
PostgreSQL 16.15 + pgvector       PASS
Alembic upgrade/downgrade/upgrade PASS
Full suite                        83 / 83 PASS
Original G1 regressions           PASS
Coverage                          86%
```

### G2.1 checkpoint

```text
PostgreSQL 16.15 + pgvector       PASS
Alembic upgrade/downgrade/upgrade PASS
Full automated suite              92 / 92 PASS
Failed tests                      0
Coverage                          86%
Original G1 regressions           PASS
Private GitHub Actions            PASS
Mentor decision                   REVISE
```

The G2.1 REVISE verdict reflects missing adversarial proof/semantics around concurrency and idempotency, not a regression of G1.

---

## Publicly reportable G2 capability

The private implementation currently includes high-level support for:

- academic metadata acquisition from arXiv, Crossref, OpenAlex, and Semantic Scholar;
- provider-neutral discovery records;
- DOI/arXiv/URL normalization;
- conservative scholarly-document reconciliation;
- provider-observation provenance;
- bounded ingestion jobs and telemetry;
- async HTTP transport, retry/backoff and rate control;
- network-safety / SSRF-oriented checks;
- deterministic CI fixtures and PostgreSQL integration tests.

Detailed proprietary implementation is intentionally not mirrored here.

---

## G2.2 public closure themes

Before G2 can be approved, the private core must close and verify:

1. real concurrent-ingestion/idempotency behavior on PostgreSQL;
2. complete agreement across trusted scholarly identities;
3. safe duplicate-running background-job behavior;
4. explicit transaction/failure accounting;
5. final provider authentication/policy alignment;
6. remaining HTTP timeout/cancellation/redirect edge cases.

No G3 work is authorized before those items pass mentor re-review.

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

The public repository remains actively maintained. Future gate approvals, verified metrics, demos/screenshots, selected benchmarks, posters, papers, presentations, and safe research outputs should be reported here.

See:

- [`README.md`](README.md)
- [`docs/PUBLIC_PROGRESS.md`](docs/PUBLIC_PROGRESS.md)
- [`docs/IP_POLICY.md`](docs/IP_POLICY.md)
- [`LICENSE`](LICENSE)
- [`NOTICE.md`](NOTICE.md)

---

## Exact next action

Complete **G2.2** in the private authoritative core, run real PostgreSQL concurrency/failure tests and full CI, then return for mentor review. If approved, update this public surface to **G2 APPROVED / G3 AUTHORIZED** with verified final metrics.
