# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** APPROVED (~98/100)
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** APPROVED (~99/100)
- **G4 — Intelligence Lake & Personal Research Memory:** APPROVED (~99/100)
- **G5 — Research Opportunity Miner & Snapshot-Pinned Idea Lineage:** **APPROVED (~98/100)**
- **Current engineering action:** **G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis**
- **G6 authorization:** **ACTIVE**
- **G7 authorization:** LOCKED until G6 mentor approval

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation remains in the private authoritative core and is disclosed here only at a safe level of detail.

---

## Latest verified engineering evidence

### G5 final

```text
Private implementation CI         31952247007
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0008              PASS
Downgrade base / second upgrade   PASS
Full automated suite              297 / 297 PASS
Failed / skipped                  0 / 0
Coverage                          90%
Mentor decision                   APPROVED (~98/100)
```

G5 progressed from an initial 286/286 green implementation that received a REVISE decision to a 297/297 final suite after a dedicated snapshot-lineage integrity closure.

At a disclosure-safe level, G5 now provides:

```text
Grounded claims / limitations / future work
→ explicit + inferred gap candidates
→ conservative contradiction candidates
→ provisionally scored research opportunities
→ candidate research ideas
→ exact snapshot-pinned backward lineage
→ lightweight experiment / human-review records
```

Important calibration remains explicit: grounding is not truth; contradiction candidates are not refutations; semantic distinctiveness is not proof of novelty; generated ideas are not validated research conclusions; automated scoring remains provisional until later calibration.

The flagship G5 integrity property is that a persisted generated idea must remain traceable through its opportunity and supporting gap/contradiction to a valid grounded claim and the exact immutable source snapshot/version used at generation time. Model-produced references are treated as untrusted input and must pass deterministic database validation.

---

## G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis

G6 is now authorized to build the first trustworthy query/retrieval/synthesis layer:

```text
Research query
→ PostgreSQL lexical retrieval + pgvector semantic retrieval
→ deterministic deduplication / hybrid fusion
→ bounded provenance-rich context
→ typed citation-grounded synthesis
→ deterministic citation validation
→ answer with exact source paths
```

The public-facing G6 safety boundary is deliberately strict:

- retrieval rank means relevance, not truth;
- semantic similarity is not entailment;
- source text is untrusted data and cannot issue system instructions;
- a model citation is accepted only if it resolves to an exact retrieved context item and its true snapshot/document provenance;
- a real database entity that was not supplied to the synthesis context is still an invalid citation;
- conflicting evidence can be surfaced without automatic scientific adjudication.

Private query data, research memory, unpublished opportunities/ideas and proprietary retrieval/synthesis implementation remain outside the public repository by default.

---

## Public / private rule

```text
PRIVATE CORE
    implementation → test → mentor review → disclosure review
                                      │
                                      ▼
PUBLIC NCKH
    verified progress → metrics → demos → selected results → publications
```

The public repository remains actively maintained. Verified metrics, sanitized architecture updates, demos/screenshots, selected benchmarks, release notes, posters, papers and presentations are published only when those artifacts genuinely exist and pass disclosure review.

---

## Exact next action

Implement **G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis** in the private authoritative core against the protected 297-test G5 baseline. **Do not begin G7 before G6 approval.**
