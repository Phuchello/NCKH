# Intel OS — Public Progress & Verified Results

This is the disclosure-safe milestone record for Intel OS. It reports verified outcomes without mirroring the proprietary private-core implementation, private research memory, unpublished ideas, sensitive prompts or detailed security findings.

**Public demo preview:** https://intel-os-eight.vercel.app/

The hosted demo uses synthetic/stateless public data and should not be interpreted as access to the private owner research environment.

---

## Current status

| Gate / Item | Public status |
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
| G10 — V1 Release / UX / i18n / Recovery / Archival | 🔄 Private hardening / review |
| V1 Acceptance | 🔒 After G10 approval |
| V2 | 🔒 After V1 freeze |

The authoritative implementation and research state live in the private core. Public synchronization occurs only after disclosure review; an implementation commit or green CI run is not automatically a public milestone.

---

## G0 — Foundation & Architecture

```text
G0 initial review       77/100 — REVISE
G0.1                    88/100 — NEAR PASS
G0.2                    APPROVED
```

Established the modular-monolith direction, provenance-first data model, epistemic boundaries, retention strategy, gate-based engineering process and the separation between replaceable AI models and durable structured research memory.

---

## G1 — Database Foundation & Backend Scaffold

```text
PostgreSQL 16 + pgvector           PASS
Alembic upgrade/downgrade/up       PASS
G1 automated suite                 49 / 49 PASS
Coverage                           91%
Mentor assessment                  ~96/100 — APPROVED
```

The foundational public implementation was created before the project moved its authoritative G2+ engineering into the private core. Historical Git commits remain part of the already-disclosed project history, but the current public branch no longer mirrors the live backend codebase.

---

## G2 — Academic Metadata Ingestion & Connector Framework

**Final decision: APPROVED (~98/100).**

```text
G2.1                     92 / 92 PASS   → REVISE
G2.2                    107 / 107 PASS  → NEAR PASS
G2.3 final              111 / 111 PASS  → APPROVED (~98/100)
```

Disclosure-safe scope includes scholarly metadata ingestion, conservative identity reconciliation, provider provenance, bounded async networking, explicit job/transaction semantics and real PostgreSQL concurrency testing.

The gate history matters: green tests were not enough when a concurrency/provenance edge case still survived review.

---

## G3 — Full-Text Parsing & Quote-Grounded Extraction

**Final decision: APPROVED (~99/100).**

```text
G3 initial    134 / 134 PASS   → REVISE (~88/100)
G3.1          141 / 141 PASS   → NEAR PASS (~96/100)
G3.2          149 / 149 PASS   → NEAR PASS (~97/100)
G3.3 final    156 / 156 PASS   → APPROVED (~99/100)
```

Verified scope includes streamed representation bounds, versioned source snapshots, deterministic parsing, versioned chunks, provider-neutral extraction contracts, character-exact quote grounding, unsupported-evidence quarantine and reproducible extraction history.

> **Grounding is not truth.** A verified quote proves that a source contains a statement; it does not prove the statement is scientifically correct.

---

## G4 — Intelligence Lake & Personal Research Memory

**Final decision: APPROVED (~99/100).**

```text
G4 initial   184 / 184 PASS   → REVISE (~84/100)
G4.1         215 / 215 PASS   → NEAR PASS (~95/100)
G4.2         234 / 234 PASS   → NEAR PASS (~98/100)
G4.3 final   243 / 243 PASS   → APPROVED (~99/100)
```

Publicly reportable capabilities include bounded retained-artifact storage, explicit cross-store compensation/reconciliation, versioned embedding provenance, pgvector/HNSW projections, Personal Research Memory notes and conservative claim relationships.

G4 is another example of the project rule that a large passing test suite does not automatically prove the intended semantics.

---

## G5 — Research Opportunity Miner & Idea Lineage

**Final decision: APPROVED (~98/100).**

```text
G5 initial     286 / 286 PASS   → REVISE (~91/100)
G5.1 final     297 / 297 PASS   → APPROVED (~98/100)
```

G5 establishes the Research Opportunity Memory layer with source-grounded gap candidates, separately labeled system-inferred gaps, conservative contradiction candidates, research opportunities, candidate ideas and exact snapshot-pinned backward lineage.

Public epistemic boundaries remain explicit:

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
Alembic                           0001 → 0009
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

Retrieval and generation do not create evidence. Retrieval rank is relevance rather than truth; semantic similarity is not entailment; source text is untrusted data; and generated citations must resolve to evidence that was actually supplied to the synthesis context.

---

## Security S0 — Security & Privacy Assurance Baseline

**Final decision: APPROVED as a cross-cutting V1 engineering baseline.**

Disclosure-safe coverage includes data/privacy, identity/access, AI/RAG boundaries, application/API risk, infrastructure/storage, software/AI supply chain, recovery/incident thinking and explicit residual-risk tracking.

S0 is an engineering assurance baseline, **not a security certification and not an absolute-security claim**. Detailed threat paths and private security evidence stay in the authoritative core.

---

## G7 — Living Research Output Engine

**Final decision: APPROVED (~99/100).**

G7 converts bounded research context into durable research outputs while preserving context identity, bibliography hydration, citation validation and output verification.

Disclosure/privacy enforcement occurs before approved provider boundaries; private or unapproved research context fails closed rather than being repaired after dispatch.

---

## G8 — Research Console & Learning Workbench

**Final decision: APPROVED (~98–99/100).**

G8 adds the human-facing Next.js workbench while preserving approved provenance and security contracts.

Disclosure-safe capabilities include:

- dashboard and research health/status views;
- evidence search/exploration;
- document, version and source-provenance inspection;
- research-memory notes;
- research output generation;
- Learning Mode bound to the selected research context;
- provisional/epistemic labels surfaced in the UI;
- same-origin application boundary for private operation;
- synthetic/stateless `PUBLIC_DEMO` mode with no private database requirement.

G10 owns the V1 release polish, bilingual VI/EN UX, reproducibility, recovery and archival readiness.

---

## G9 — Reliability, Security, Calibration & Comparative Workflow Benchmark

**Final decision: APPROVED (~98–99/100).**

G9 was not accepted on its first green CI. The initial benchmark was rejected because the proof did not sufficiently demonstrate the actual Intel OS system path. The final G9.1 closure uses a real PostgreSQL-backed system benchmark and independently derived evidence.

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

Real-system benchmark tasks cover evidence discovery, provenance tracing, contradiction visibility without automatic truth adjudication, research-memory reuse, verified brief generation, disclosure/provider policy and restart/recovery/reseed/tamper behavior.

The bounded sanitized retrieval fixture recorded Recall@1/3/5 = `1.0/1.0/1.0`, MRR = `1.0`, duplicate-result rate = `0.0`, effective-context survival = `1.0` and contradiction endpoint preservation = `1.0`. These values describe that deterministic fixture only and are **not** claimed as universal model quality.

### Comparative-workflow interpretation

A machine-measured `AUTOMATED_PROXY` baseline was used for selected operations. Flat conventional operations are naturally faster on raw milliseconds than Intel OS database/provenance processing.

The project therefore does not claim that Intel OS exists to win primitive lookup latency. The research value under evaluation is instead:

- exact provenance reconstruction;
- citation/bibliography integrity;
- reusable structured research memory;
- explicit epistemic state;
- controlled contradiction handling;
- recovery/reproducibility;
- privacy/security boundaries.

A true owner-run human workflow benchmark remains a separate acceptance activity and will not be relabeled as machine evidence.

---

## G10 — V1 Release Hardening

G10 is currently being completed in the private authoritative core. Public status remains **in progress** until Mentor review actually approves the gate.

Disclosure-safe focus includes:

- responsive VI/EN owner experience;
- clearer research terminology;
- loading/empty/error states;
- explicit `PUBLIC_DEMO` / `PRIVATE_LOCAL` mode boundaries;
- startup/runbook reproducibility;
- dependency/release hardening;
- backup/restore verification;
- archival and release-candidate evidence.

No G10 result should be treated as approved merely because a deployment exists or CI is green.

After G10 approval, a separate owner-facing V1 Acceptance flow must be completed before V1.0 freeze/tag.

---

## Public / private synchronization rule

```text
PRIVATE CORE
implementation → test → evidence → mentor review → disclosure review
                                             │
                                             ▼
PUBLIC SHOWCASE
verified progress → safe metrics → demo → selected results → publications
```

The public repository stays substantive, but it is intentionally not an installable mirror of the proprietary core.
