# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** APPROVED (~98/100)
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** APPROVED (~99/100)
- **G4 — Intelligence Lake & Personal Research Memory:** **APPROVED (~99/100)**
- **Current engineering action:** **G5 — Research Opportunity Miner & Snapshot-Pinned Idea Lineage**
- **G5 authorization:** **ACTIVE**
- **G6 authorization:** LOCKED until G5 mentor approval

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation remains in the private authoritative core and is disclosed here only at a safe level of detail.

---

## Latest verified engineering evidence

### G4 final

```text
Private CI run                    31945476008
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0007              PASS
Downgrade base / second upgrade   PASS
Full automated suite              243 / 243 PASS
Failed / skipped                  0 / 0
Coverage                          88%
Mentor decision                   APPROVED (~99/100)
```

The G4 closure progressed from 184/184 green but REVISE, through storage/provenance hardening, to a final 243/243 verified suite. Publicly reportable capability now includes bounded S3-compatible artifact retention, explicit PostgreSQL/object-store compensation and reconciliation semantics, immutable embedding provenance, pgvector/HNSW active projections, Personal Research Memory notes and conservative claim relationships.

Important calibration remains explicit: PostgreSQL + S3 are not one ACID transaction; semantic vectors are retrieval infrastructure rather than proof of scientific novelty; note privacy metadata is not an authorization boundary; formal retrieval-quality benchmarking remains later work.

---

## G5 — Research Opportunity Memory

G5 is authorized to build the first structured opportunity/idea layer:

```text
Grounded claims / limitations / future work
→ gap candidates
→ contradiction candidates
→ research opportunities
→ candidate research ideas
→ snapshot-pinned backward lineage
```

The flagship invariant is explainability back to exact source versions: generated ideas must retain a valid path to grounded claims and the exact `DocumentSnapshot` that produced them. Automated contradiction, gap, feasibility and semantic-distinctiveness signals remain provisional and must not be presented as scientific truth or proven novelty.

Private unpublished ideas, opportunity memory, experiment notes and implementation remain outside the public repository by default.

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

Implement **G5 — Research Opportunity Miner & Snapshot-Pinned Idea Lineage** in the private authoritative core against the protected 243-test G4 baseline. **Do not begin G6 before G5 approval.**
