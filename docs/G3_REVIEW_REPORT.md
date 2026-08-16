# G3 Mentor Review Checkpoint

> **Full-Text Parsing, Snapshot Processing & Quote-Grounded Extraction**

G3 is implemented in the private authoritative core and has completed its first mentor review. The implementation passed the complete private CI suite, but the gate is **not yet approved**: a narrow G3.1 integrity closure is required before G4.

## Verified engineering evidence

```text
Private implementation checkpoint    97ddd615742182c846dd11c07bd16c1168e4dcc1
Private CI run                       31925479279
PostgreSQL                           16.15 + pgvector
Alembic upgrade/downgrade/upgrade   PASS
Full automated suite                134 / 134 PASS
Failed / skipped                    0 / 0
Coverage                            87%
G1/G2 regression surface            PASS
Mentor decision                     REVISE (~88/100)
```

## Publicly reportable G3 capability

The private implementation now contains the first complete source-grounding pipeline prototype:

```text
Selected representation
→ immutable snapshot identity
→ deterministic parsing
→ normalized sections/chunks
→ typed claim candidate
→ deterministic quote verification
→ snapshot-pinned claim/evidence persistence
```

Implemented capability includes:

- bounded PDF/HTML representation-retrieval architecture;
- SHA-256 representation identity and local temporary caching;
- immutable `DocumentSnapshot` integration;
- deterministic PDF and academic-HTML parser abstractions;
- section normalization and reference separation;
- deterministic snapshot-pinned chunking;
- a dedicated G3 extraction migration for chunks, claims and evidence;
- provider-neutral typed LLM extraction schemas with deterministic CI mocks;
- claim categories aligned to the project epistemic model;
- deterministic quote-grounding logic;
- all new machine-extracted claims defaulting to `UNASSESSED`;
- malformed/encrypted representation handling;
- PostgreSQL-backed regression validation.

## Flagship epistemic rule

G3 explicitly separates **grounding** from **scientific truth**.

A verified quote means:

> the source contains this statement.

It does **not** mean:

> the statement is scientifically correct.

Therefore newly extracted claims remain `UNASSESSED` until later evidence synthesis or human/scientific evaluation changes that status.

## Why G3 is still REVISE

Green CI is necessary but not sufficient for this gate. The mentor review identified a focused set of integrity requirements that need stronger proof before approval:

- representation-size enforcement must be truly bounded during transfer, not only after content is available;
- `VERBATIM_MATCH` must remain character-exact;
- parsing/extraction reruns must preserve historical provenance and avoid duplicate intelligence;
- parser limitations, especially multi-column academic layouts, need a controlled acceptance fixture;
- extraction provider/model/prompt configuration must remain reproducible in persisted provenance;
- ungrounded candidates must not become grounded empirical evidence;
- snapshot/source provenance must remain internally consistent.

These are closure items, not a reset of G3.

## Current gate state

| Gate | State |
|---|---|
| G0 | ✅ Approved |
| G1 | ✅ Approved |
| G2 | ✅ Approved |
| G3 | 🛠 G3.1 integrity closure |
| G4 | 🔒 Locked |

The existing **134-test passing suite is now the protected G3.1 regression baseline**. G4 will not begin until the closure is re-tested in private PostgreSQL CI and receives final mentor approval.

## Disclosure boundary

This report intentionally publishes verified outcomes, review status and safe architecture only. Proprietary private-core source code, internal research memory, unpublished methods/data and strategically sensitive implementation details are not mirrored into the public repository.

© 2026 Võ Trọng Phúc. All Rights Reserved.
