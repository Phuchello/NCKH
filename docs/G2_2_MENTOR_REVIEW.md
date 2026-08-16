# G2.2 — Public Mentor Review Summary

## Decision

**NEAR PASS (~95/100). G3 remains locked pending one narrow concurrency closure.**

## Verified checkpoint

```text
PostgreSQL 16.15 + pgvector      PASS
Alembic upgrade/downgrade       PASS
Full private automated suite    107 / 107 PASS
Coverage                        86%
Original G1 regression surface  PASS
Real PostgreSQL concurrency     PASS
Private GitHub Actions          PASS
```

## What G2.2 strengthened

At a public, non-proprietary level, G2.2 added or verified:

- hard-identity agreement across scholarly provider signals;
- a provider-level identifier database invariant;
- real PostgreSQL two-session concurrency testing;
- SAVEPOINT-based race recovery;
- whole-ingestion-attempt transaction atomicity;
- explicit background-job idempotency semantics;
- production-oriented OpenAlex authentication behavior;
- optional provider contact identity rather than a placeholder identity;
- bounded HTTP wall-clock timeout;
- redirect-method/body behavior tests;
- cancellation-safe rate-limit concurrency accounting.

## Why G2 is not approved yet

The mentor review found one remaining edge case in concurrent provider-identity ingestion where the database can correctly deduplicate the provider observation while still allowing a transient duplicate logical document to survive. The private implementation must eliminate that artifact and prove the invariant with a focused real-PostgreSQL regression test.

Implementation details of the race and its fix remain private by design.

## Gate status

| Gate | Status |
|---|---|
| G0 | ✅ Approved |
| G1 | ✅ Approved |
| G2 | 🟡 Near pass — final concurrency closure |
| G3 | 🔒 Locked |

This report intentionally publishes verified outcomes and review status without exposing proprietary private-core implementation.
