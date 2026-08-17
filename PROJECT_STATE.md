# Intel OS / NCKH — Public Project State

## Current gate

- **G0 — Foundation & Architecture:** APPROVED
- **G1 — Database Foundation & Backend Scaffold:** APPROVED (~96/100)
- **Private-core transition:** VALIDATED
- **G2 — Academic Ingestion & Connector Framework:** APPROVED (~98/100)
- **G3 — Full-Text Parsing & Quote-Grounded Extraction:** APPROVED (~99/100)
- **G4 — Intelligence Lake & Personal Research Memory:** APPROVED (~99/100)
- **G5 — Research Opportunity Miner & Snapshot-Pinned Idea Lineage:** APPROVED (~98/100)
- **G6 — Hybrid Retrieval & Citation-Grounded Research Synthesis:** **APPROVED (~99/100)**
- **Current engineering action:** **Security S0 — Threat-Model & Security/Privacy Assurance Baseline**
- **Security S0 authorization:** **ACTIVE**
- **G7 authorization:** LOCKED until Security S0 mentor approval

This repository is the **public showcase / verified-results surface**. Proprietary G2+ implementation, private research memory, unpublished opportunities/ideas, exploit details, prompts/rules and credentials remain in the private authoritative core. Public reporting is intentionally limited to disclosure-safe architecture, verified outcomes, metrics, demos and research outputs.

---

## Latest verified engineering evidence

### G6 final

```text
Private implementation CI         31994684252
PostgreSQL                        16.15
pgvector                          0.8.6
Alembic head                      0009_g6_retrieval_indices
Upgrade / downgrade / upgrade    PASS
Full automated suite              429 / 429 PASS
Failed / skipped                  0 / 0
Statement coverage                90.3%
Verification proof manifest       v1.2
Declared verification categories 17 / 17 PASS
Mentor decision                   APPROVED (~99/100)
```

At a disclosure-safe level, G6 now provides:

```text
Research query
→ PostgreSQL lexical retrieval + pgvector semantic retrieval
→ deterministic normalization / hybrid fusion
→ bounded provenance-rich context
→ typed citation-grounded synthesis
→ deterministic citation validation
→ exact backward source paths
```

Key verified G6 properties include:

- retrieval rank is treated as relevance, not scientific truth;
- semantic similarity is not treated as entailment;
- source content remains passive untrusted data rather than control instructions;
- model-visible Claim/Chunk provenance is checked against authoritative document/snapshot state before synthesis;
- fabricated citations and real-but-non-retrieved citations are rejected;
- model-visible title/truncation/contradiction metadata is validated fail-closed before provider dispatch;
- conflicting evidence can be surfaced only from the exact effective context without automatic epistemic adjudication;
- material retrieval/synthesis behavior is versioned/fingerprinted;
- verification evidence uses explicit typed proof references rather than loose substring matching.

The verification pack is machine-derived from private CI and intentionally sanitized. Raw private tests, source code, research memory, unpublished ideas and credentials are not published through this showcase surface.

---

## Security S0 — active pre-G7 baseline

Security is being treated as a cross-cutting engineering constraint rather than an end-of-project add-on. Before G7 output-generation work begins, the private core is establishing a focused threat-model and assurance baseline covering data/privacy, identity/access, AI/RAG boundaries, application/API risks, infrastructure/storage, software/AI supply chain, and operational recovery.

Public reporting will expose only high-level verified security outcomes and residual-risk language where safe. Detailed threat paths, private architecture attack surfaces and exploit material remain private by default.

Security S0 is **not** a claim of certification or absolute security. It is the baseline from which later deterministic security tests, CI assurance, adversarial benchmarks and independent review can be built.

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

Complete **Security S0 — Threat-Model & Security/Privacy Assurance Baseline** in the private authoritative core. **Do not begin G7 until Security S0 receives mentor approval.**
