# G4 Mentor Review Checkpoint

> **Intelligence Lake, Personal Research Memory & Embedding Storage**

G4 has a substantial private implementation and a fully green PostgreSQL CI checkpoint, but the first mentor audit returned **REVISE (~84/100)**. The current closure milestone is **G4.1 — Storage Consistency & Embedding Provenance**.

## Latest verified engineering evidence

```text
Private CI run                       31936122041
PostgreSQL                           16.15 + pgvector
Alembic 0001 -> 0005                 PASS
Downgrade base / second upgrade      PASS
Full automated suite                 184 / 184 PASS
Failed / skipped                     0 / 0
Coverage                             87%
G1/G2/G3 regression surface          PASS
Mentor decision                      REVISE (~84/100)
```

## Publicly reportable G4 capability

The private core now includes a first storage/memory/vector foundation:

```text
Grounded snapshot / chunk / claim
→ selective retained-artifact workflow
→ 768-dimension semantic vectors
→ pgvector / HNSW indexing
→ user-authored research notes
→ conservative claim relationships
```

Verified capability includes:

- PostgreSQL 16 + pgvector vector storage for existing G4 entities (`document_chunks`, `claims`);
- 768-dimension database contract and deterministic offline embedding mock;
- HNSW cosine indexes with controlled PostgreSQL query/index validation;
- Personal Research Memory `user_notes` storage with bounded content and link-preservation semantics;
- generic claim-to-claim relationship storage with self-link prevention and no automatic epistemic-status mutation;
- deterministic artifact-object key generation, path-safety checks and signed-URL redaction;
- retention promotion happy path, idempotency, upload-failure, hash-mismatch and size-mismatch tests;
- complete regression of the approved G1–G3 surface.

## Why G4 is not approved yet

The review found several storage/provenance contracts that green CI does not yet prove:

1. The private docs describe a concrete S3-compatible adapter, but the current reviewed code surface only contains the provider-neutral interface and deterministic mock. A narrow real S3-compatible adapter is still required for eventual R2/AWS-compatible deployment while CI remains offline.
2. Cross-system retention is not one ACID transaction. The current compensation path covers an error during database flush, but the required **upload succeeds → database commit fails** case still needs explicit compensation/recovery proof.
3. Embedding configuration changes currently replace the active vector metadata rather than preserving historical embedding provenance. G4.1 must make vector history reproducible across model/config changes.
4. Embedding provenance must pin the exact source-text identity used to generate the vector and reject provider response-cardinality mismatches.
5. Additional adversarial tests are required for commit-failure recovery, embedding timeout/partial-failure cleanup, bounded embedding input/batch behavior and note-link preservation.

These are closure items around durability and reproducibility, not a reset of G4.

## Gate state

| Gate | State |
|---|---|
| G0 | ✅ Approved |
| G1 | ✅ Approved |
| G2 | ✅ Approved |
| G3 | ✅ Approved |
| G4 | 🛠 G4.1 integrity closure |
| G5 | 🔒 Locked |

## Review principle

A green suite proves the tested behaviors, not every architectural invariant. For cross-system durability and scientific-memory provenance, **failure semantics and historical reproducibility are gate criteria**, not optional hardening.

## Disclosure boundary

This report publishes only verified outcomes and high-level review conclusions. Private-core source, private research memory/data, credentials, retained raw artifacts and strategically sensitive implementation details are not mirrored into the public repository.

© 2026 Võ Trọng Phúc. All Rights Reserved.
