# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** APPROVED (~98/100)
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** APPROVED (~99/100)
- **G4 — Intelligence Lake & Personal Research Memory:** G4.1 **NEAR PASS (~95/100)**
- **Current engineering action:** **G4.2 — Storage Read Bounds & Provenance Integrity Micro-Closure**
- **G5 authorization:** **DENIED until G4 final approval**

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation remains in the private authoritative core and is disclosed here only at a safe level of detail.

---

## Latest verified engineering evidence

### G3 final

```text
Private CI run                    31927755688
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0004              PASS
Full automated suite              156 / 156 PASS
Coverage                          88%
Mentor decision                   APPROVED (~99/100)
```

### G4.1 reviewed checkpoint

```text
Private CI run                    31941431543
PostgreSQL 16.15 + pgvector       PASS
Alembic 0001 -> 0006              PASS
Downgrade base / second upgrade   PASS
Full automated suite              215 / 215 PASS
Failed / skipped                  0 / 0
Coverage                          88%
Protected regression surface      PASS
Mentor decision                   NEAR PASS (~95/100)
```

G4.1 resolved the major G4 storage/provenance blockers, including a concrete S3-compatible boundary, explicit cross-store compensation/reconciliation, immutable embedding history, exact source-text identity and adversarial PostgreSQL/storage testing.

Final G4 approval is intentionally withheld for a small G4.2 integrity closure covering true bounded object reads, stronger durable post-upload verification/reconciliation, and database-level consistency between embedding-provenance entity type and foreign-key target.

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

Complete **G4.2** in the private authoritative core while preserving the 215-test regression baseline, run PostgreSQL 16 + pgvector CI and return for final G4 mentor sign-off. **Do not begin G5 before G4 approval.**
