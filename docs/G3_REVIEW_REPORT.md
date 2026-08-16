# G3 Final Gate Report

> **Full-Text Parsing, Snapshot Processing & Quote-Grounded Extraction**

G3 is formally **APPROVED** after three focused hardening passes beyond the initial implementation. The authoritative implementation remains in the private core; this report publishes only verified results, safe architecture, review progression, and non-sensitive limitations.

## Final verified engineering evidence

```text
Final private checkpoint              f1379a909d24832446893f1f54afbaae8da288ab
Private CI run                        31927755688
PostgreSQL                            16.15 + pgvector
Alembic 0001 -> 0002 -> 0003 -> 0004 PASS
Downgrade base / second upgrade       PASS
Full automated suite                  156 / 156 PASS
Failed / skipped                      0 / 0
Coverage                              88%
G1/G2 regression surface              PASS
Mentor decision                       APPROVED (~99/100)
```

## Publicly reportable G3 capability

```text
Selected representation
→ immutable snapshot identity
→ deterministic parsing
→ versioned sections / chunks
→ typed claim candidate
→ character-exact quote verification
→ snapshot-pinned claim / evidence
→ immutable extraction-run provenance
```

Verified capability includes:

- bounded streamed PDF/HTML retrieval with incremental byte counting and SHA-256 hashing;
- hard representation-size limits during transfer;
- immutable `DocumentSnapshot` integration with source/document consistency guards;
- deterministic PDF / academic-HTML parser abstractions and section normalization;
- controlled two-column PDF reading-order acceptance fixture;
- parser-version-aware chunk history;
- provider-neutral typed extraction gateway with deterministic offline CI mocks;
- bounded LLM input, wall-clock timeout, claim count, requested output tokens, aggregate response characters, and reported token usage;
- prompt-version and extraction-version separation;
- configuration fingerprints covering provider/model/parser/version and material execution bounds;
- same-configuration extraction idempotency and changed-configuration provenance coexistence;
- character-exact deterministic quote grounding independent of the proposing model;
- ungrounded candidate quarantine so failed quotes create no grounded empirical evidence rows;
- all newly machine-extracted claims defaulting to `UNASSESSED`;
- PostgreSQL-backed migration, concurrency, version-history and regression validation.

## Flagship epistemic rule

G3 deliberately separates **grounding** from **scientific truth**.

A `VERBATIM_MATCH` proves only that the exact quoted text exists in the pinned source representation. It does **not** prove that the scientific statement is correct, reproducible, or consensus. Newly extracted claims therefore remain `UNASSESSED` until later evidence synthesis or human/scientific evaluation changes that status.

## Review progression

```text
G3 initial    134 / 134 PASS   → REVISE (~88/100)
G3.1          141 / 141 PASS   → NEAR PASS (~96/100)
G3.2          149 / 149 PASS   → NEAR PASS (~97/100)
G3.3 final    156 / 156 PASS   → APPROVED (~99/100)
```

The extra review passes closed transfer-time resource bounds, exact-quote edge cases, version-safe reruns, extraction-run reproducibility, multi-column parser proof, output-budget enforcement, and configuration-sensitive provenance.

## Remaining non-blocking limitations

- Academic PDF reconstruction is a bounded baseline, not universal layout recovery.
- Future live LLM adapters must map the provider-neutral output-budget field into their native API configuration; normal CI remains offline and deterministic.
- G3 establishes auditable source grounding, not scientific consensus or automated truth assessment.

## Gate state

| Gate | State |
|---|---|
| G0 | ✅ Approved |
| G1 | ✅ Approved |
| G2 | ✅ Approved |
| G3 | ✅ Approved |
| G4 | 🚧 Authorized / Active |

G4 now moves from source-grounded extraction into durable Intelligence Lake / Personal Research Memory storage, controlled artifact retention, and versioned semantic embeddings.

## Disclosure boundary

This report intentionally publishes verified outcomes and safe architecture only. Proprietary private-core source, private research memory, raw retained artifacts, unpublished methods/data, prompts, credentials, and strategically sensitive implementation details are not mirrored here.

© 2026 Võ Trọng Phúc. All Rights Reserved.
