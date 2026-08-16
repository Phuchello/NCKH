# Intel OS / NCKH — Public Project State

## Current status

- **Public repository**: `Phuchello/NCKH`
- **Role**: public showcase / verified progress mirror / research-publication surface
- **Authoritative implementation**: private core
- **G0**: APPROVED
- **G1**: APPROVED
- **Private-core migration**: VALIDATED
- **G2**: IMPLEMENTED IN PRIVATE CORE — MENTOR AUDIT IN PROGRESS
- **G3**: LOCKED until G2 approval

---

## Verified engineering baseline

### G1

The approved G1 baseline established:

- FastAPI + typed Python backend foundation;
- SQLAlchemy 2.x async + asyncpg;
- PostgreSQL 16 + pgvector;
- staged Alembic migrations;
- 7 foundation tables;
- multi-provider observation provenance;
- normalized URL idempotency;
- document snapshot/version provenance;
- bounded local cache;
- health/status endpoints;
- PostgreSQL integration tests;
- GitHub Actions CI.

Final G1 verification:

```text
PostgreSQL 16 + pgvector     PASS
Alembic upgrade/downgrade    PASS
49 / 49 G1 tests             PASS
Coverage                     91%
G1 final gate                APPROVED (~96/100)
```

### Private-core migration regression

The project was revalidated after moving authoritative G2+ engineering into the private core.

```text
PostgreSQL                    16.15 + pgvector
Alembic lifecycle             PASS
Full suite                    83 / 83 PASS
Failed                        0
Coverage                      86%
Original G1 regression        PASS
Private GitHub Actions        PASS
```

---

## G2 public progress mirror

G2 covers the academic metadata ingestion and source-connector foundation.

Publicly reportable scope:

- arXiv metadata connector;
- Crossref metadata connector;
- OpenAlex metadata connector;
- Semantic Scholar Academic Graph connector;
- provider-neutral normalized discovery representation;
- identifier/URL normalization;
- conservative multi-provider reconciliation;
- provider provenance preservation;
- bounded async ingestion;
- retry/backoff and provider-aware rate control;
- SSRF-oriented network checks;
- background-job telemetry;
- deterministic connector tests;
- real PostgreSQL multi-provider reconciliation test.

G2 implementation is complete but **not yet mentor-approved**. Current review focuses on identity conflicts, concurrency, transaction failure recovery, job idempotency, HTTP/SSRF edge cases, and current provider-policy correctness.

Full public report: [`docs/PUBLIC_PROGRESS.md`](docs/PUBLIC_PROGRESS.md)

---

## Public / private boundary

The public repository remains an active, maintained project front page.

### Public by default

- product vision;
- high-level architecture;
- milestone outcomes;
- verified metrics and test summaries;
- screenshots and demos;
- sanitized examples;
- public research outputs;
- papers, posters, presentations and selected benchmark summaries;
- intentionally released artifacts.

### Private by default

- authoritative G2+ source implementation;
- proprietary reasoning/scoring internals;
- private prompts;
- Research Memory / Opportunity Memory data;
- unpublished research ideas and experiments;
- private datasets/corpora;
- secrets and deployment configuration;
- potentially patent-sensitive methods before disclosure review.

See [`docs/IP_POLICY.md`](docs/IP_POLICY.md).

---

## Next actions

1. Complete G2 mentor/adversarial review in the private core.
2. Publish the resulting **sanitized G2 gate report** here, including final decision, verified metrics, limitations, and safe architecture changes.
3. If G2 passes, update the public roadmap to `G2 APPROVED / G3 AUTHORIZED`.
4. Add screenshots/demos only when real product UI/output exists; do not add fabricated placeholders.
5. Continue updating this public repository at every major gate and research/publication milestone.
