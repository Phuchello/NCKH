# G3 Mentor Review Checkpoint

> **Full-Text Parsing, Snapshot Processing & Quote-Grounded Extraction**

G3 is implemented in the private authoritative core. G3.2 has passed full private PostgreSQL CI and is now **NEAR PASS (~97/100)**. One final bounded-output/reproducibility contract closure remains before G4.

## Latest verified engineering evidence

```text
G3.2 implementation checkpoint      28200e96ecf360f6a0046f1d71b584ce7960afd2
Private CI run                       31927144568
PostgreSQL                           16.15 + pgvector
Alembic 0001 -> 0002 -> 0003 -> 0004 PASS
Downgrade base / second upgrade      PASS
Full automated suite                 149 / 149 PASS
Failed / skipped                     0 / 0
Coverage                             87%
G1/G2 regression surface             PASS
Mentor decision                      NEAR PASS (~97/100)
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

Verified capability includes:

- bounded streamed PDF/HTML retrieval with incremental byte counting and SHA-256 hashing;
- hard representation-size limits during transfer;
- immutable `DocumentSnapshot` integration and source-consistency checks;
- deterministic PDF / academic-HTML parsing and section normalization;
- a controlled two-column PDF reading-order fixture;
- parser-version-aware chunk lineage;
- provider-neutral typed LLM extraction schemas with deterministic offline CI mocks;
- persisted extraction-run provenance and same-configuration idempotency;
- character-exact deterministic quote grounding independent of the proposing model;
- typed wall-clock extraction timeouts;
- explicit separation between prompt version and extraction-pipeline version;
- parser-version and extraction-configuration history coexistence tested on PostgreSQL;
- ungrounded candidate quarantine so failed quotes do not create empirical evidence records;
- all newly machine-extracted claims defaulting to `UNASSESSED`;
- PostgreSQL-backed migration, concurrency and regression validation.

## Flagship epistemic rule

G3 separates **grounding** from **scientific truth**. A verified quote means only that the source contains the statement; it does not establish that the statement is scientifically correct. Newly extracted claims therefore remain `UNASSESSED` until later evidence synthesis or human/scientific evaluation changes that status.

## Why G3 is not approved yet

The remaining work is deliberately narrow and concerns the provider-neutral LLM contract rather than the source-grounding pipeline itself.

Although G3.2 now enforces a maximum claim count, the configured maximum output-token budget is not yet propagated through the gateway request contract, and aggregate parsed response size is not independently bounded. Effective input/output bounds also need to participate in the extraction configuration fingerprint so a material limits change cannot silently reuse a result produced under different execution constraints.

The final closure therefore requires:

- an explicit provider-neutral maximum output budget in the extraction request contract;
- a service-side aggregate response-size guard independent of claim count;
- bounded/discarded raw response text;
- effective extraction bounds included in the reproducibility fingerprint;
- deterministic tests for oversized single-claim/raw-response output and fingerprint changes.

No new subsystem is required and G4 remains out of scope.

## Review progression

```text
G3 initial       134 / 134 PASS   → REVISE (~88/100)
G3.1             141 / 141 PASS   → NEAR PASS (~96/100)
G3.2             149 / 149 PASS   → NEAR PASS (~97/100)
Final closure    bounded-output/reproducibility contract pending
```

## Current gate state

| Gate | State |
|---|---|
| G0 | ✅ Approved |
| G1 | ✅ Approved |
| G2 | ✅ Approved |
| G3 | 🛠 Final output-contract closure |
| G4 | 🔒 Locked |

Green CI remains necessary but not sufficient for gate approval. G4 will not begin until the final contract closure is re-tested in private PostgreSQL CI and receives mentor sign-off.

## Disclosure boundary

This report intentionally publishes verified outcomes, review status and safe architecture only. Proprietary private-core source code, internal research memory, unpublished methods/data and strategically sensitive implementation details are not mirrored into the public repository.

© 2026 Võ Trọng Phúc. All Rights Reserved.
