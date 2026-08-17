# Intel OS / NCKH — Public Progress & Verified Results

This page is the disclosure-safe public milestone mirror for Intel OS / NCKH. It reports verified engineering outcomes and research-facing progress without publishing the proprietary private-core implementation, private research memory, unpublished ideas, sensitive prompts, or detailed security findings.

---

## Current status

| Gate / Item | Status |
|---|---|
| G0 — Foundation & Architecture | ✅ Approved |
| G1 — Database Foundation & Backend Scaffold | ✅ Approved |
| Private-core transition | ✅ Validated |
| G2 — Academic Ingestion & Connector Framework | ✅ Approved |
| G3 — Full-Text Parsing & Quote-Grounded Extraction | ✅ Approved |
| G4 — Intelligence Lake & Personal Research Memory | ✅ Approved |
| G5 — Opportunity Miner & Snapshot-Pinned Idea Lineage | ✅ Approved (~98/100) |
| G6 — Hybrid Retrieval & Citation-Grounded Synthesis | ✅ Approved (~99/100) |
| Security S0 — Security & Privacy Assurance Baseline | ✅ Approved |
| G7 — Living Research Output Engine | ✅ Approved (~99/100) |
| G8 — Research Console & Learning Workbench | ✅ Approved (~98–99/100) |
| G9 — Reliability, Calibration & Comparative Benchmark | ✅ Approved (~98–99/100) |
| G10 — V1 Release / UX / i18n / Archival | ▶ Next |
| V1 Acceptance | 🔒 After G10 |
| V2 | 🔒 Locked until V1 |

The public repository remains the project showcase, verified-results surface and future publication/demo hub. The authoritative G2+ source implementation remains private.

---

## G0 — Foundation & Architecture

```text
G0 initial review       77/100 — REVISE
G0.1                    88/100 — NEAR PASS
G0.2                    APPROVED
```

Established the modular-monolith direction, provenance-first research data model, epistemic discipline, retention strategy, gate-based engineering process and the long-term separation between replaceable AI models and durable structured research memory.

---

## G1 — Database Foundation & Backend Scaffold

```text
PostgreSQL 16 + pgvector           PASS
Alembic upgrade/downgrade/up       PASS
G1 automated suite                 49 / 49 PASS
Coverage                           91%
Mentor assessment                  ~96/100 — APPROVED
```

---

## G2 — Academic Metadata Ingestion & Connector Framework

**Final decision: APPROVED (~98/100).**

```text
G2.1                     92 / 92 PASS   → REVISE
G2.2                    107 / 107 PASS  → NEAR PASS
G2.3 final              111 / 111 PASS  → APPROVED (~98/100)
```

Verified scope includes scholarly metadata ingestion, conservative identity reconciliation, provider provenance, bounded async networking, explicit job/transaction semantics and real PostgreSQL concurrency testing.

Full public report: **[G2 Final Gate Report](G2_FINAL_REPORT.md)**.

---

## G3 — Full-Text Parsing & Quote-Grounded Extraction

**Final decision: APPROVED (~99/100).**

```text
G3 initial    134 / 134 PASS   → REVISE (~88/100)
G3.1          141 / 141 PASS   → NEAR PASS (~96/100)
G3.2          149 / 149 PASS   → NEAR PASS (~97/100)
G3.3 final    156 / 156 PASS   → APPROVED (~99/100)
```

Verified scope includes streamed representation bounds, immutable snapshots, deterministic parsing, versioned chunks, provider-neutral extraction contracts, character-exact quote grounding, ungrounded-evidence quarantine and reproducible extraction history.

Full public report: **[G3 Final Gate Report](G3_REVIEW_REPORT.md)**.

---

## G4 — Intelligence Lake & Personal Research Memory

**Final decision: APPROVED (~99/100).**

```text
G4 initial   184 / 184 PASS   → REVISE (~84/100)
G4.1         215 / 215 PASS   → NEAR PASS (~95/100)
G4.2         234 / 234 PASS   → NEAR PASS (~98/100)
G4.3 final   243 / 243 PASS   → APPROVED (~99/100)
```

Publicly reportable capability includes a bounded S3-compatible retained-artifact boundary, explicit cross-store compensation/reconciliation, immutable embedding provenance, pgvector/HNSW active projections, Personal Research Memory notes and conservative claim relationships.

Full report: **[G4 Final Gate Report](G4_REVIEW_REPORT.md)**.

---

## G5 — Research Opportunity Miner & Snapshot-Pinned Idea Lineage

**Final decision: APPROVED (~98/100).**

```text
G5 initial     286 / 286 PASS   → REVISE (~91/100)
G5.1 final     297 / 297 PASS   → APPROVED (~98/100)
```

G5 establishes the first Research Opportunity Memory layer with source-grounded gap candidates, separately labeled system-inferred gaps, conservative contradiction candidates, research opportunities, candidate ideas and exact snapshot-pinned backward lineage.

Important public epistemic boundaries remain explicit:

- contradiction candidate ≠ scientific refutation;
- semantic distinctiveness ≠ novelty proof;
- system-inferred gap ≠ author-stated limitation;
- generated idea ≠ validated research conclusion;
- provisional score ≠ calibrated scientific truth.

Private unpublished opportunities, idea text and experiment notes remain private by design.

---

## G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis

**Final decision: APPROVED (~99/100).**

```text
PostgreSQL                        16.15
pgvector                          0.8.6
Alembic                           0001 -> 0009
Upgrade / downgrade / upgrade     PASS
Private automated suite           429 / 429 PASS
Statement coverage                90.3%
Verification categories           17 / 17 PASS
```

Verified public flow:

```text
Research Query
→ PostgreSQL lexical retrieval + pgvector semantic retrieval
→ deterministic normalization / deduplication / hybrid fusion
→ provenance-rich bounded context
→ typed synthesis
→ deterministic citation validation
→ source-traceable answer
```

G6 preserves the rule that retrieval and generation do not create evidence. Retrieval rank is relevance, not truth; semantic similarity is not entailment; source text is untrusted data; and model-produced citations must resolve to exact evidence actually present in the bounded context.

---

## Security S0 — Security & Privacy Assurance Baseline

**Final decision: APPROVED as a cross-cutting V1 engineering baseline.**

Publicly reportable coverage includes data/privacy, identity/access, AI/RAG boundaries, application/API risk, infrastructure/storage, software/AI supply chain, recovery/incident thinking and explicit residual-risk tracking.

The project does **not** claim security certification, perfect security or elimination of all residual risk. Detailed attack paths and private security evidence remain in the private core.

---

## G7 — Living Research Output Engine

**Final decision: APPROVED (~99/100).**

G7 converts authoritative bounded research context into durable research outputs while preserving exact context identity, bibliography hydration, deterministic citation validation and output verification.

The provider-data privacy boundary was hardened so classification and provider authorization occur before dispatch. Private or unapproved research context fails closed rather than being repaired after provider access.

Public capability summary:

```text
Authoritative research context
→ verified context identity
→ output planning
→ bounded synthesis
→ citation / bibliography validation
→ output verification
→ durable research artifact
```

---

## G8 — Research Console & Learning Workbench

**Final decision: APPROVED (~98–99/100).**

G8 adds a human-facing Next.js workbench while preserving the already-approved data/provenance contracts.

Disclosure-safe capabilities include:

- dashboard and research health/status views;
- search/evidence exploration;
- exact document/snapshot/source provenance inspection;
- research-memory notes;
- Output Studio;
- Learning Mode bound to the same authoritative context identity;
- provisional/epistemic labels surfaced in the UI;
- same-origin BFF + CSRF boundary;
- server-only private bearer handling;
- synthetic, stateless `PUBLIC_DEMO` mode with no private database/backend requirement.

The current interface is functional but is not treated as the final visual design. G10 owns release UX/UI hardening and bilingual Vietnamese/English support.

---

## G9 — Reliability, Security, Calibration & Comparative Research-Workflow Benchmark

**Final decision: APPROVED (~98–99/100).**

G9 was not accepted on its first green CI. The initial benchmark was rejected because the proof did not sufficiently demonstrate the actual Intel OS system path. The final accepted G9.1 benchmark uses real PostgreSQL-backed system paths and independent evidence derivation.

Disclosure-safe final verification:

```text
Private backend suite             564 / 564 PASS
Failed / skipped                  0 / 0
Statement coverage                88.7%
PostgreSQL                        16.15
pgvector                          0.8.6
Alembic U/D/U                     PASS
G9 proof                          G9-v1.1
Mandatory G9 categories           13 / 13 PASS
Current-gate security regression  10 / 10 PASS
```

Real-system benchmark tasks cover:

- evidence discovery;
- provenance tracing;
- contradiction visibility without automatic truth adjudication;
- research-memory reuse;
- verified Evidence Brief generation;
- disclosure/provider-policy enforcement;
- restart/recovery/reseed/tamper behavior.

Retrieval calibration on the bounded sanitized fixture recorded Recall@1/3/5 = `1.0/1.0/1.0`, MRR = `1.0`, duplicate-result rate = `0.0`, effective-context survival = `1.0`, and contradiction endpoint preservation = `1.0`. These values describe the deterministic G9 fixture only and are not claimed as universal model quality.

### Comparative-workflow interpretation

A small machine-measured `AUTOMATED_PROXY` baseline was used for selected A/B/E operations. Flat conventional operations are naturally much faster on raw milliseconds than Intel OS database/provenance processing. The project therefore does **not** claim that Intel OS exists to beat flat files on primitive lookup latency.

The research value under evaluation is instead:

- exact provenance reconstruction;
- citation and bibliography integrity;
- reusable structured research memory;
- explicit epistemic state;
- controlled contradiction handling;
- recovery/reproducibility;
- privacy/security boundaries.

A true owner-run human workflow benchmark remains intentionally separate from machine CI evidence and will not overwrite or relabel the machine results.

### Student-scale practicality

The accepted G9 fixture remained within a lightweight local PostgreSQL + pgvector stack. No Redis, Kafka, microservice mesh, new model training or enterprise orchestration was introduced merely to satisfy the gate.

---

## Next: G10 — V1 Release & UX Hardening

G10 is the next gate. Planned disclosure-safe focus includes:

- release/reproducibility cleanup;
- final local run and recovery experience;
- UI/UX refinement through iterative review;
- responsive/layout/typography/empty/loading/error-state cleanup;
- **Vietnamese + English first-class interface support**;
- preservation of source titles, quotes, citations, hashes and research data without unsafe automatic translation;
- release/archive bookkeeping and V1 handoff preparation.

G10 approval will still be followed by an owner-facing V1 end-to-end acceptance pass before an Intel OS V1.0 freeze.

---

## Review philosophy

A gate is evaluated on more than implementation completeness:

1. purpose fit and measurable usefulness;
2. deterministic tests;
3. production-dialect behavior;
4. provenance/data-integrity invariants;
5. concurrency/failure/recovery semantics;
6. provider/model reproducibility;
7. epistemic correctness;
8. privacy/security boundaries;
9. safe public disclosure.

**Green CI is necessary, but not sufficient, for gate approval.**

---

## Public reporting policy

The public repository reports milestone objective, safe architecture, verified test/evaluation summaries, known limitations, mentor decision, sanitized demos/screenshots, selected benchmark conclusions and research outputs when disclosure permits.

No fabricated benchmark, placeholder screenshot, unpublished research memory, credential, sensitive threat detail or private-core implementation is published merely for appearance.

Public progress is synchronized after verified gate approval rather than after every private implementation commit.

---

## Disclosure note

This repository is **source-available/proprietary, not open source**. Public reporting keeps the project assessable while preserving its private core and research/IP boundary.

See [`IP_POLICY.md`](IP_POLICY.md) and the root [`LICENSE`](../LICENSE).
