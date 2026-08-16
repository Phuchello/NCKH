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
| G3 — Full-Text Parsing & Quote-Grounded Extraction | 🚧 Active |
| G4 | 🔒 Locked until G3 approval |

The public repository remains an active showcase, verified-results surface, and research/publication hub. The authoritative G2+ implementation remains private.

---

## G0 — Foundation & Architecture

G0 established the architectural and research principles used by later gates:

- modular-monolith V1 architecture;
- provenance-first data model;
- Intelligence Lake / Personal Research Memory / Research Opportunity Memory concepts;
- idea-lineage requirement;
- cloud-first authoritative storage direction;
- metadata-first retention policy;
- replaceable reasoning-model strategy;
- security, epistemic and gate-review principles.

Review history:

```text
G0 initial review       77/100 — REVISE
G0.1                    88/100 — NEAR PASS
G0.2                    APPROVED
```

---

## G1 — Database Foundation & Backend Scaffold

G1 created the executable backend foundation and was approved only after real PostgreSQL verification.

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

Publicly reportable scope:

- arXiv, Crossref, OpenAlex, and Semantic Scholar metadata ingestion;
- provider-neutral discovery records;
- DOI/arXiv/provider identity normalization and reconciliation;
- explicit hard-identity conflict handling;
- conservative false-merge policy;
- provider-observation provenance;
- bounded ingestion jobs;
- resilient async HTTP transport;
- bounded retries and provider-aware rate control;
- network-safety / SSRF-oriented defenses;
- whole-attempt transaction semantics;
- background-job idempotency;
- real PostgreSQL concurrency testing.

### Review progression

```text
Private split baseline   83 / 83 PASS
G2.1                     92 / 92 PASS   → REVISE
G2.2                    107 / 107 PASS  → NEAR PASS
G2.3 final              111 / 111 PASS  → APPROVED
```

G2 was not approved merely because CI was green. Review passes specifically challenged scientific identity conflicts, database race conditions, transaction failure recovery, job idempotency, provider-policy changes, and HTTP edge cases.

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

**Status: Active.**

G3 is the first gate that turns selected document representations into source-grounded research objects.

Public architectural target:

```text
Fetched representation
→ immutable snapshot identity
→ layout-aware parsing
→ normalized sections/chunks
→ claim candidate
→ deterministic exact-quote verification
→ evidence record
```

Key G3 principles:

- parsed content remains pinned to a specific snapshot/version;
- quote grounding is deterministic and independent of the LLM that proposed the claim;
- `VERBATIM_MATCH` means the quote exists in the source text — it does **not** mean the scientific claim is true;
- newly extracted claims default to `UNASSESSED`;
- malformed or ungrounded extraction is quarantined/rejected rather than silently accepted;
- embeddings, S3/R2 storage, opportunity mining and frontend work remain out of scope for G3.

G3 results will be mirrored publicly after mentor/disclosure review.

---

## Review philosophy

A gate is evaluated on more than implementation completeness:

1. deterministic tests;
2. production-dialect behavior;
3. provenance/data-integrity invariants;
4. concurrency and failure semantics;
5. external-provider policy correctness;
6. epistemic correctness;
7. safe public disclosure.

Green CI is necessary, but not sufficient, for gate approval.

---

## Public reporting policy

For future gates, this repository publishes a concise verified report containing, when safe:

- milestone objective and completed capability;
- safe architecture impact;
- test/evaluation evidence;
- benchmark/experiment results;
- known limitations;
- mentor/gate decision;
- screenshots/demos when real outputs exist;
- public papers/posters/presentations;
- explicit disclosure boundary.

No fabricated benchmark, placeholder screenshot, or private-core implementation is published merely for appearance.

---

## Disclosure note

This repository is **source-available/proprietary, not open source**. Public reporting keeps the project assessable and professionally presentable while preserving its private core and research/IP boundary.

See [`IP_POLICY.md`](IP_POLICY.md) and the root [`LICENSE`](../LICENSE).
