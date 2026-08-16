# G2 Final Gate Report — Academic Ingestion & Connector Framework

## Decision

**G2 APPROVED**  
Final mentor assessment: **~98/100**

G2 established the academic metadata ingestion and reconciliation foundation for Intel OS while preserving a strict public-showcase/private-core IP boundary.

---

## Publicly reportable scope

G2 integrates metadata acquisition paths for:

- arXiv;
- Crossref;
- OpenAlex;
- Semantic Scholar Academic Graph.

The private implementation includes, at a safe architectural level:

- provider-neutral normalized discovery records;
- DOI and logical arXiv normalization;
- provider-level identity tracking;
- conservative multi-provider reconciliation;
- explicit identity-conflict handling;
- provider-observation provenance;
- bounded ingestion jobs;
- async HTTP transport;
- retry/backoff and per-provider rate control;
- redirect and network-safety checks;
- background-job telemetry and idempotency;
- PostgreSQL-backed concurrency recovery.

---

## Why G2 required multiple review passes

The gate was intentionally not approved from a happy-path implementation alone.

### Initial implementation

The connector framework and metadata ingestion path were functional, but mentor review identified risks around:

- provider-policy drift;
- scientific identity conflicts;
- false merges;
- PostgreSQL uniqueness races;
- transaction-failure recovery;
- duplicate background jobs;
- cancellation/redirect edge cases.

### G2.1

Provider-policy and identity semantics were hardened. The automated suite reached **92/92 passing**, but mentor review still returned **REVISE** because concurrency invariants were not yet proven with real PostgreSQL races.

### G2.2

Real two-session PostgreSQL concurrency tests, provider-ID database uniqueness, whole-attempt atomicity, job idempotency, and HTTP edge cases were added. The suite reached **107/107 passing**.

Mentor review then caught one final race artifact: the observation could deduplicate correctly while a losing concurrent candidate Document survived as an orphan.

### G2.3

The final closure re-rooted the losing worker to the winning logical Document, removed only transient concurrency duplicates, preserved genuine scientific identity-conflict evidence, and strengthened the persistence return invariant.

The final private CI result was **111/111 passing**.

---

## Final verified evidence

```text
PostgreSQL                       16.15 + pgvector
Alembic upgrade head             PASS
Alembic downgrade base           PASS
Alembic second upgrade           PASS
Full automated suite             111 / 111 PASS
Failed tests                     0
Skipped tests                    0
Coverage                         86%
Original G1 regression surface   PASS
Private GitHub Actions           PASS
Mentor decision                  APPROVED
```

Private CI run ID: `31924223739`.

---

## Verified integrity properties

The final gate verifies, among other cases:

- concurrent workers ingesting the same DOI converge to one logical Document;
- a provider identifier is unique within its source namespace;
- concurrent same-provider-ID ingestion does not leave an orphan logical duplicate;
- concurrent normalized-URL observations remain idempotent;
- duplicate background-job keys do not start uncontrolled parallel execution;
- failed ingestion attempts roll back their data mutations while FAILED telemetry persists;
- the returned Document and DocumentSource always agree on document ownership in normal successful paths;
- contradictory hard scholarly identities are preserved as explicit conflicts rather than silently merged;
- canonical URL equality does not override hard identity safeguards;
- redirect state preserves the current HTTP method/body semantics across multi-hop redirects;
- rate limiter resources are released under cancellation;
- retry delays are bounded.

---

## Epistemic / research significance

G2 is not only an API integration milestone. Its main contribution to the architecture is protecting the future Research Memory from bad identity decisions.

The project follows the principle:

> **False merge is worse than temporary duplication.**

Provider disagreement is retained as provenance instead of being erased. This is important because later stages will build claims, evidence, contradictions, gaps, and ideas on top of these logical works.

---

## Known residual risks

Accepted for later gates:

- DNS validation remains subject to TOCTOU / rebinding limitations; the current network layer is defense-in-depth, not a claim of total SSRF elimination.
- A crashed RUNNING background job does not yet have lease/heartbeat-based automatic recovery; G2 safely rejects duplicate RUNNING execution.
- Provider API/auth/rate policies can change and must be re-verified when connectors are materially modified.

These are documented limitations, not hidden assumptions.

---

## Gate transition

**G2 is complete. G3 is authorized.**

G3 focuses on:

```text
Fetched representation
→ immutable snapshot
→ layout-aware parse
→ normalized sections/chunks
→ claim candidate
→ exact quote verification
→ evidence record
```

Embeddings, S3/R2 durable artifact storage, opportunity mining, handbook generation, and frontend work remain deferred to later gates.

---

## Disclosure boundary

This report publishes verified outcomes and safe architecture only. The authoritative G2+ implementation remains proprietary/private.

See:

- [`PUBLIC_PROGRESS.md`](PUBLIC_PROGRESS.md)
- [`IP_POLICY.md`](IP_POLICY.md)
- root [`LICENSE`](../LICENSE)

© 2026 Võ Trọng Phúc. All Rights Reserved.
