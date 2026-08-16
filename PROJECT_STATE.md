# Intel OS / NCKH Intelligence Platform — Project State & Safety Checkpoint

## 1. Milestone Tracking

* **Current Milestone**: **Gate 0.2 (G0.2) — Data-Integrity Hardening**
* **Previous Milestones**:
  * **G0 Score: 77/100 | Status: REVISE | G1 Authorization: DENIED**
  * **G0.1 Score: 88/100 | Status: NEAR PASS | G1 Authorization: DENIED**
* **G0.2 Completion Percentage**: **100%**
* **Active Working Branch**: `main`
* **Remote Repository**: `https://github.com/Phuchello/NCKH`
* **Status**: **G0.2 COMPLETED — Awaiting Mentor Re-Audit for G1 Authorization**

---

## 2. What Exists (G0.2 Corrected Deliverables)

1. **Authoritative Specification & Architecture Suite**:
   * [`README.md`](README.md): System executive summary, 3 intellectual assets, snapshot-pinned provenance, storage topology, and 18-table architecture.
   * [`ARCHITECTURE.md`](ARCHITECTURE.md): System architecture, subsystem decomposition, storage topology, mermaid diagrams.
   * [`DECISIONS.md`](DECISIONS.md): Architecture Decision Records (ADR-0001 through ADR-0013) including M:N topic mapping, epistemic separation, snapshot provenance enforcement, confidence-based reconciliation, and gate-staged migrations.
   * [`TODO.md`](TODO.md): Complete engineering task backlog organized from Gate 0 through Gate 10.
   * [`CHANGELOG_AGENT.md`](CHANGELOG_AGENT.md): Full audit trail of AI agent actions and milestone checkpoints.
   * [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md): Target personas, core epics, confidence-based multi-provider reconciliation, multi-topic mapping, and explicit non-goals.
   * [`docs/ARCHITECTURE_DETAILED.md`](docs/ARCHITECTURE_DETAILED.md): Technical specifications for all 7 platform subsystems, 4-tier idempotency, confidence-based reconciliation, and snapshot→source linkage.
   * [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md): Authoritative PostgreSQL 16+ DDL defining **exactly 18 normalized tables** with gate-staged migration matrix, V1 768-dim embedding contract, identity signal classification, provenance invariant summary, and backward lineage query.
   * [`docs/PIPELINE.md`](docs/PIPELINE.md): End-to-end 8-stage intelligence lifecycle with confidence-aware reconciliation workflow (`match_method`, `match_confidence`).
   * [`docs/MILESTONES.md`](docs/MILESTONES.md): G0–G10 roadmap with G1 scoped to 7 foundation tables and explicit migration staging.
   * [`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md): Defense-in-depth threat mitigation, pre-flight SSRF IP-blocking, and XML-delimited prompt injection safeguards.
   * [`docs/SCORING_MODEL.md`](docs/SCORING_MODEL.md): Multi-factor scoring formulations with semantic distinctiveness signals and provisional heuristic labels.
   * [`docs/INTELLIGENCE_MODEL.md`](docs/INTELLIGENCE_MODEL.md): 4-dimensional epistemic ladder and snapshot-pinned Idea Lineage with NOT NULL provenance invariant.

2. **Environment & Configuration Templates**:
   * [`.gitignore`](.gitignore): Multi-language exclusions (Python, Node.js, local data cache, sensitive secrets).
   * [`.env.example`](.env.example): Environment configuration blueprint with explicit V1 768-dim embedding contract documentation.

3. **G0.2 Data-Integrity Hardening Summary**:
   * **Snapshot-Pinned Provenance**: `snapshot_id NOT NULL` on `claims`, `evidence_items`, `idea_provenance`, `document_chunks`. `ON DELETE RESTRICT` on intelligence entities to prevent silent orphaning.
   * **Snapshot → Source Linkage**: `document_source_id` FK on `document_snapshots` completing lineage chain: Source → Observation → Snapshot → Claims.
   * **Confidence-Based Reconciliation**: `match_method` and `match_confidence` on `document_sources`. Hard identity (DOI, arXiv ID) auto-merges; candidate signals (metadata fingerprint) treated as reviewable events. False merge is more dangerous than temporary duplication.
   * **NULLS NOT DISTINCT**: `UNIQUE NULLS NOT DISTINCT (document_id, source_id, provider_doc_id)` on `document_sources` for correct NULL handling.
   * **Snapshot Identity Broadening**: `UNIQUE(document_id, version_identifier, mime_type, content_hash)` on `document_snapshots` supporting multiple representations per version.
   * **Gate-Staged Migrations**: 18 tables split across G1 Foundation (7), G3/G4 Extraction (5), G5 Opportunity (6).
   * **ADR-0011 through ADR-0013**: Recorded all three G0.2 architectural decisions.

---

## 3. What Does NOT Exist (Strict Gate Boundaries)

To ensure disciplined execution, the following components are strictly deferred to subsequent gates and are **not** present in G0.2:

* **No live crawler fleet or connector implementation code** (Deferred to Gate 2).
* **No LLM extraction runners, prompt scripts, or OpenAI/Gemini execution calls** (Deferred to Gate 3).
* **No live database schema migration execution or running database instances** (Deferred to Gate 1).
* **No research gap mining or automated hypothesis generation code** (Deferred to Gate 5).
* **No research handbook compilation or PDF/LaTeX generation code** (Deferred to Gate 7).
* **No Next.js UI frontend code, dashboard components, or chat interfaces** (Deferred to Gate 8).
* **No custom model training or fine-tuning pipelines** (Explicit platform non-goal for G0–V1).

---

## 4. Known Risks & Architectural Mitigations

| Identified Risk | Severity | Architectural Mitigation in G0.2 |
| :--- | :--- | :--- |
| **SSRF via crawler fetch** | CRITICAL | Pre-flight DNS resolution blocking RFC 1918 private subnets and metadata IPs (`169.254.169.254`). See `docs/SECURITY_MODEL.md`. |
| **Indirect Prompt Injection in crawled papers** | HIGH | Strict XML sandboxing delimiters (`<untrusted_document_content>`), Pydantic schema validation, and verbatim quote verification before storing claims. |
| **Unbounded Local Storage Bloat** | HIGH | Multi-tier retention funnel (`DISCOVERED → INDEXED → RELEVANT → RETAINED → ARCHIVED`), metadata-only default intake, and `MAX_LOCAL_CACHE_GB` quota with automated LRU cleanup. |
| **LLM Citation Hallucination & False Truth Attribution** | HIGH | 4D epistemic framework separating Grounding (`VERBATIM_MATCH`) from scientific validity (`epistemic_status = 'UNASSESSED'`). |
| **Document Evolution & Revision Drift** | MEDIUM | Representation snapshot model (`document_snapshots`) pinning claims and chunks to exact version bytes with `NOT NULL` enforcement and `ON DELETE RESTRICT`. |
| **False Document Merges** | HIGH | Tiered identity signal classification. Candidate-only matches (metadata fingerprint without hard identity) do not auto-merge. Reconciliation is auditable via `match_method` and `match_confidence`. |
| **Silent Provenance Destruction** | HIGH | `ON DELETE RESTRICT` on `claims.snapshot_id`, `evidence_items.snapshot_id`, `idea_provenance.snapshot_id`. A snapshot with dependent intelligence cannot be dropped. |

---

## 5. Tests & Consistency Checks Performed

1. **Full Repository Cross-Document Audit**: Verified that all 14+ specification files reference identical table names, column names, constraint types, embedding dimensions (768), and epistemic terms.
2. **Schema Integrity**: Confirmed that `docs/DATA_MODEL.md` DDL contains exactly 18 normalized tables with correct FK references, UNIQUE constraints (including `NULLS NOT DISTINCT`), and provenance invariant annotations.
3. **Provenance Invariant Verification**: Confirmed `snapshot_id NOT NULL` + `ON DELETE RESTRICT` on all machine-extracted intelligence tables (`claims`, `evidence_items`, `idea_provenance`). `ON DELETE CASCADE` confirmed on `document_chunks` (physical derivatives).
4. **Migration Staging Verification**: Confirmed G1 Foundation scope is 7 tables and matches both `docs/DATA_MODEL.md` §5 staging matrix and `docs/MILESTONES.md` G1 section.
5. **No Overbuilding**: Verified that zero application feature code or premature scripts were created.

---

## 6. Last Safe Checkpoint

* **G0 Baseline Checkpoint**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **G0.1 Corrected Checkpoint**: `60abdbe65b88b2dd61e28d5419655b50c5fd94cb`
* **G0.2 Data-Integrity Checkpoint**: `f95ddb8`
* **Working Tree**: Clean.

---

## 7. Exact Next Action

1. Commit G0.2 data-integrity hardening changes and push to `main`.
2. Present G0.2 completion report to the mentor and request formal re-audit for Gate 1 authorization.
3. **DO NOT START GATE 1 BEFORE MENTOR APPROVAL**.
