# Intel OS / NCKH — Public Progress & Verified Results

This page is the public milestone mirror for Intel OS / NCKH.

It reports **verified outcomes, engineering milestones, public architecture, and research-facing progress** without publishing proprietary private-core implementation by default.

---

## Current status

| Item | Status |
|---|---|
| G0 — Foundation & Architecture | ✅ Approved |
| G1 — Database Foundation & Backend Scaffold | ✅ Approved |
| Private-core migration | ✅ Validated |
| G2 — Academic Ingestion & Connector Framework | 🔎 Implemented, mentor audit in progress |
| G3 | 🔒 Not authorized |

Current authoritative implementation: private core.  
Current public role: project showcase, milestone mirror, verified-results surface, research/publication hub.

---

## G0 — Foundation & Architecture

### Outcome

G0 established the architectural and research principles used by later gates.

### Publicly reportable deliverables

- modular-monolith V1 architecture;
- web-first product direction;
- provenance-first data model;
- Intelligence Lake concept;
- Personal Research Memory concept;
- Research Opportunity Memory concept;
- idea-lineage requirement;
- cloud-first authoritative storage;
- retention tiers and metadata-first discovery;
- replaceable LLM/reasoning-engine strategy;
- staged database/migration philosophy;
- security and source-provenance model;
- gate-based engineering workflow.

### Review history

- Initial G0 review: **77/100 — revise**.
- G0.1 architecture correction: **88/100 — near pass**.
- G0.2 data-integrity hardening: **approved**.

---

## G1 — Database Foundation & Backend Scaffold

### Outcome

G1 created the first executable engineering foundation and was approved only after real PostgreSQL validation.

### Verified capabilities

- FastAPI application foundation;
- typed configuration with Pydantic;
- SQLAlchemy 2.x async database layer;
- asyncpg PostgreSQL connectivity;
- PostgreSQL 16 + pgvector development environment;
- Alembic migration lifecycle;
- exactly 7 initial foundation tables;
- topic/document many-to-many mapping;
- multi-provider observation provenance;
- normalized observed-URL idempotency;
- document snapshot/version representation;
- `ON DELETE RESTRICT` provenance protection;
- bounded local cache manager;
- health/status API endpoints;
- PostgreSQL integration/contract tests;
- GitHub Actions CI.

### Verification path

G1 was not approved from SQLite-only tests. It underwent an additional PostgreSQL hardening pass to verify production-dialect behavior.

Final validated G1 baseline:

```text
PostgreSQL 16 + pgvector           PASS
Alembic upgrade head              PASS
Alembic downgrade base            PASS
Alembic second upgrade            PASS
G1 automated suite                49 / 49 PASS
Coverage at G1 checkpoint         91%
GitHub Actions                    PASS
```

### G1 review outcome

Final mentor assessment: approximately **96/100 — approved**.

---

## Private-core transition

A Public Showcase + Private Core model was adopted before continuing proprietary G2+ development.

### Why

The project should remain publicly reviewable and portfolio/research friendly without making its complete proprietary implementation, research memory, unpublished ideas, private data, or strategically sensitive reasoning logic public by default.

### Current model

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
    selected benchmark summaries
    screenshots / demos
    papers / posters / presentations
    intentionally released artifacts
```

### Migration validation

After the repository split, the complete backend was revalidated in the private repository rather than assuming the migration preserved behavior.

Private validation checkpoint:

```text
PostgreSQL                         16.15 + pgvector
Alembic upgrade/downgrade/upgrade PASS
Collected tests                   83
Passed                            83
Failed                            0
Coverage                          86%
Original G1 regression surface    PASS
```

The public repository remains an active project surface; it is not an abandoned mirror.

---

## G2 — Academic Metadata Ingestion & Connector Framework

### Current state

**Implementation complete in private core. Mentor audit is in progress. G3 remains locked.**

### Publicly reportable implementation scope

G2 currently integrates metadata acquisition paths for:

- **arXiv**;
- **Crossref**;
- **OpenAlex**;
- **Semantic Scholar Academic Graph**.

The architecture includes, at a public high level:

- provider-neutral normalized discovery records;
- centralized DOI/arXiv/URL normalization;
- conservative multi-provider reconciliation;
- preservation of provider observations/provenance;
- bounded ingestion runs;
- async HTTP transport;
- retry/backoff behavior;
- configurable per-provider rate control;
- redirect/network safety checks;
- ingestion-job telemetry;
- deterministic mock provider fixtures for CI;
- PostgreSQL multi-provider reconciliation integration testing.

### Latest verified private test checkpoint

```text
Full automated suite              83 / 83 PASS
Overall coverage                  86%
PostgreSQL 16.15 + pgvector       PASS
Alembic lifecycle                 PASS
G1 regression behavior            PASS
G2 multi-provider PG test         PASS
Private GitHub Actions            PASS
```

### Why G2 is still under review

Passing tests are necessary but not sufficient for this type of system. The mentor review is deliberately challenging the implementation on:

- conflicting hard scientific identifiers;
- false-merge risk;
- concurrent ingestion races;
- transaction failure recovery;
- background-job idempotency;
- cancellation/retry edge cases;
- SSRF/DNS limitations;
- changing provider API/auth/rate-limit policies.

No G3 implementation is authorized until those issues are resolved or explicitly accepted.

---

## Public reporting policy

For every future gate, this public repository should publish a concise verified report containing, when safe to disclose:

1. milestone objective;
2. capabilities completed;
3. architecture impact at a safe level of detail;
4. tests / evaluation summary;
5. benchmark or experiment results;
6. known limitations;
7. mentor/gate decision;
8. screenshots/demo artifacts when available;
9. public research outputs and publication links;
10. what remains private and why.

Results should be **specific and evidence-based**, but proprietary source code or sensitive research material should not be published merely to make the report look complete.

---

## Planned public showcase evolution

As the product matures, the public repository is expected to gain selected artifacts such as:

- architecture diagrams;
- polished product screenshots;
- short demo recordings / GIFs;
- sanitized topic-intelligence examples;
- performance and reliability summaries;
- research workflow examples;
- release notes;
- posters / slides / papers after disclosure review;
- selected datasets or fixtures when redistribution rights allow.

No placeholder screenshots or fabricated benchmarks should be added before real outputs exist.

---

## Disclosure note

The public repository is **source-available/proprietary, not open source**. Public reporting is intended to make the project assessable, reviewable, and professionally presentable while preserving the project's private core and research/IP boundary.

See [`IP_POLICY.md`](IP_POLICY.md) and the root [`LICENSE`](../LICENSE).
