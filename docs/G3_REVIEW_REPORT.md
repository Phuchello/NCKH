# G3 Mentor Review Checkpoint

> **Full-Text Parsing, Snapshot Processing & Quote-Grounded Extraction**

G3 is implemented in the private authoritative core. The first review required a focused G3.1 integrity closure; that closure has now passed private PostgreSQL CI and is **NEAR PASS**, with one final micro-closure required before G4.

## Latest verified engineering evidence

```text
G3.1 implementation checkpoint      3fa6711f17f47cb31aac0ddb8d320ac6c787298a
Private CI run                       31926369635
PostgreSQL                           16.15 + pgvector
Alembic 0001 -> 0002 -> 0003 -> 0004 PASS
Downgrade base / second upgrade      PASS
Full automated suite                 141 / 141 PASS
Failed / skipped                     0 / 0
Coverage                             88%
G1/G2 regression surface             PASS
Mentor decision                      NEAR PASS (~96/100)
```

## Publicly reportable G3 capability

The private implementation contains the first end-to-end source-grounding pipeline:

```text
Selected representation
→ immutable snapshot identity
→ deterministic parsing
→ versioned sections/chunks
→ typed claim candidate
→ character-exact quote verification
→ snapshot-pinned claim/evidence
→ extraction-run provenance
```

Verified capability now includes:

- bounded streamed PDF/HTML retrieval with incremental byte counting and SHA-256 hashing;
- hard representation-size limits during transfer;
- immutable `DocumentSnapshot` integration and source-consistency checks;
- deterministic PDF / academic-HTML parsing and section normalization;
- a controlled two-column PDF reading-order fixture;
- parser-version-aware chunk lineage;
- provider-neutral typed LLM extraction schemas with deterministic offline CI mocks;
- persisted extraction-run provenance and same-configuration idempotency;
- deterministic quote grounding independent of the proposing model;
- ungrounded candidate quarantine so failed quotes do not create empirical evidence records;
- all newly machine-extracted claims defaulting to `UNASSESSED`;
- PostgreSQL-backed migration, concurrency and regression validation.

## Flagship epistemic rule

G3 separates **grounding** from **scientific truth**.

A verified quote means only that the source contains the statement. It does **not** establish that the statement is scientifically correct. Newly extracted claims therefore remain `UNASSESSED` until later evidence synthesis or human/scientific evaluation changes that status.

## Why G3 is not approved yet

The remaining G3.2 work is deliberately narrow. Mentor review found several contract-level edge cases that still need closure despite the 141-test green suite:

- leading/trailing whitespace must never allow a stored quote to receive `VERBATIM_MATCH` unless the persisted quote and source slice are character-identical;
- configured LLM wall-clock timeout and output bounds must be enforced, not merely declared in settings;
- forced extraction-rerun semantics must be coherent with same-configuration database idempotency;
- explicit acceptance tests must prove parser-version A survives parser-version B and that model/prompt/extraction-version changes create distinct provenance without rewriting prior runs;
- the legacy snapshot extraction-version field must have an explicit non-authoritative/latest-hint meaning, or stop being mutated.

These are closure items, not a reset of G3.

## Review progression

```text
G3 initial       134 / 134 PASS   → REVISE (~88/100)
G3.1             141 / 141 PASS   → NEAR PASS (~96/100)
G3.2             final micro-closure pending
```

## Current gate state

| Gate | State |
|---|---|
| G0 | ✅ Approved |
| G1 | ✅ Approved |
| G2 | ✅ Approved |
| G3 | 🛠 G3.2 final micro-closure |
| G4 | 🔒 Locked |

Green CI remains necessary but not sufficient for gate approval. G4 will not begin until the remaining contract/provenance edge cases are tested in private PostgreSQL CI and receive final mentor approval.

## Disclosure boundary

This report intentionally publishes verified outcomes, review status and safe architecture only. Proprietary private-core source code, internal research memory, unpublished methods/data and strategically sensitive implementation details are not mirrored into the public repository.

© 2026 Võ Trọng Phúc. All Rights Reserved.
