# Intel OS / NCKH Intelligence Platform — Project State & Safety Checkpoint

## 1. Milestone Tracking

* **Current Milestone**: **Gate 0.1 (G0.1) — Architecture Correction & Specification Hardening**
* **Previous Milestone Audit**: **G0 Score: 77/100 | Status: REVISE | G1 Authorization: DENIED**
* **G0.1 Completion Percentage**: **100%**
* **Active Working Branch**: `main`
* **Remote Repository**: `https://github.com/Phuchello/NCKH`
* **Status**: **G0.1 COMPLETED — Awaiting Mentor Re-Audit for G1 Authorization**

---

## 2. What Exists (G0.1 Corrected Deliverables)

1. **Authoritative Specification & Architecture Suite**:
   * [`README.md`](README.md): System executive summary, 3 intellectual assets, snapshot-pinned provenance, storage topology, and 18-table architecture.
   * [`ARCHITECTURE.md`](ARCHITECTURE.md): System architecture, subsystem decomposition, storage topology, mermaid diagrams.
   * [`DECISIONS.md`](DECISIONS.md): Architecture Decision Records (ADR-0001 through ADR-0010) including M:N topic mapping and epistemic separation.
   * [`TODO.md`](TODO.md): Complete engineering task backlog organized from Gate 0 through Gate 10.
   * [`CHANGELOG_AGENT.md`](CHANGELOG_AGENT.md): Full audit trail of AI agent actions and milestone checkpoints.
   * [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md): Target personas, core epics, multi-topic mapping, multi-provider reconciliation, and explicit non-goals.
   * [`docs/ARCHITECTURE_DETAILED.md`](docs/ARCHITECTURE_DETAILED.md): Technical specifications for all 7 platform subsystems, 4-tier idempotency, and 18 normalized tables.
   * [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md): Authoritative PostgreSQL 16+ DDL defining **exactly 18 normalized tables**, V1 768-dim embedding contract, and recursive snapshot-pinned SQL lineage queries.
   * [`docs/PIPELINE.md`](docs/PIPELINE.md): End-to-end 8-stage intelligence lifecycle (`Collect → Filter → Verify → Connect → Analyze → Remember → Synthesize → Act`), canonical deduplication precedence, and multi-provider reconciliation.
   * [`docs/MILESTONES.md`](docs/MILESTONES.md): Comprehensive Gate 0 to Gate 10 roadmap with hard deliverables and acceptance criteria.
   * [`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md): Defense-in-depth threat mitigation, pre-flight SSRF IP-blocking, and XML-delimited prompt injection safeguards.
   * [`docs/SCORING_MODEL.md`](docs/SCORING_MODEL.md): Multi-factor scoring formulations with semantic distinctiveness signals and provisional heuristic labels.
   * [`docs/INTELLIGENCE_MODEL.md`](docs/INTELLIGENCE_MODEL.md): 4-dimensional epistemic ladder (Grounding vs Claim Type vs Epistemic Status vs Evidence Quality) and snapshot-pinned Idea Lineage.

2. **Environment & Configuration Templates**:
   * [`.gitignore`](.gitignore): Multi-language exclusions (Python, Node.js, local data cache, sensitive secrets).
   * [`.env.example`](.env.example): Environment configuration blueprint with explicit V1 768-dim embedding contract documentation.

3. **G0.1 Architectural Corrections Summary**:
   * **Topic Cardinality**: Converted 1:N to Many-to-Many via `document_topics`.
   * **Identity Separation**: `metadata_fingerprint` used for `DISCOVERED` tier; `content_hash` isolated to fetched `document_snapshots`.
   * **Document Snapshots**: Created `document_snapshots` to model representation versions (e.g. arXiv v1 vs v2) and pin claim provenance.
   * **Multi-Provider Reconciliation**: Introduced `document_sources` for provider observation provenance with canonical deduplication precedence (`DOI → arXiv ID → Canonical URL → Metadata Fingerprint → Content Hash`).
   * **Embedding Model Contract**: Versioned 768-dim contract for V1 schema, decoupled from replaceable reasoning LLM providers.
   * **Schema Reconciliation**: Eliminated all phantom entity references, standardizing on exactly 18 normalized tables across all documents.
   * **Scientific Epistemology**: Decoupled Grounding Status (`VERBATIM_MATCH`), Claim Type, Epistemic Status (default `UNASSESSED`), and Evidence Quality. Verbatim quotes validate text presence, not scientific truth.
   * **Scoring Recalibration**: Renamed novelty to Semantic Distinctiveness Signal ($S_{dist}$) and marked all formulas PROVISIONAL pending G9 empirical calibration.
   * **Search Terminology**: Standardized on "PostgreSQL full-text lexical retrieval (`tsvector`/`tsquery`)".
   * **Security Language**: Replaced absolute claims with calibrated defense-in-depth terminology.

---

## 3. What Does NOT Exist (Strict Gate Boundaries)

To ensure disciplined execution, the following components are strictly deferred to subsequent gates and are **not** present in G0.1:

* **No live crawler fleet or connector implementation code** (Deferred to Gate 2).
* **No LLM extraction runners, prompt scripts, or OpenAI/Gemini execution calls** (Deferred to Gate 3).
* **No live database schema migration execution or running database instances** (Deferred to Gate 1).
* **No research gap mining or automated hypothesis generation code** (Deferred to Gate 5).
* **No research handbook compilation or PDF/LaTeX generation code** (Deferred to Gate 7).
* **No Next.js UI frontend code, dashboard components, or chat interfaces** (Deferred to Gate 8).
* **No custom model training or fine-tuning pipelines** (Explicit platform non-goal for G0–V1).

---

## 4. Known Risks & Architectural Mitigations

| Identified Risk | Severity | Architectural Mitigation in G0.1 |
| :--- | :--- | :--- |
| **SSRF via crawler fetch** | CRITICAL | Pre-flight DNS resolution blocking RFC 1918 private subnets and metadata IPs (`169.254.169.254`). See `docs/SECURITY_MODEL.md`. |
| **Indirect Prompt Injection in crawled papers** | HIGH | Strict XML sandboxing delimiters (`<untrusted_document_content>`), Pydantic schema validation, and verbatim quote verification before storing claims. |
| **Unbounded Local Storage Bloat** | HIGH | Multi-tier retention funnel (`DISCOVERED → INDEXED → RELEVANT → RETAINED → ARCHIVED`), metadata-only default intake, and `MAX_LOCAL_CACHE_GB` quota with automated LRU cleanup. |
| **LLM Citation Hallucination & False Truth Attribution** | HIGH | 4D epistemic framework separating Grounding (`VERBATIM_MATCH`) from scientific validity (`epistemic_status = 'UNASSESSED'`). |
| **Document Evolution & Revision Drift** | MEDIUM | Representation snapshot model (`document_snapshots`) pinning claims and chunks to exact version bytes. |

---

## 5. Tests & Consistency Checks Performed

1. **Full Repository Cross-Document Audit**: Verified that all 14 specification files, `README.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `TODO.md`, `CHANGELOG_AGENT.md`, and `.env.example` reference identical 18 table names, embedding dimensions (768), and epistemic terms.
2. **Schema Integrity**: Confirmed that `docs/DATA_MODEL.md` DDL contains exactly 18 normalized tables with all foreign keys, unique constraints, and indexes.
3. **No Overbuilding**: Verified that zero application feature code or premature scripts were created.

---

## 6. Last Safe Checkpoint

* **Previous Checkpoint (G0 Baseline)**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **Current Checkpoint (G0.1 Corrected)**: Will be registered upon git commit of G0.1.
* **Working Tree**: Clean.

---

## 7. Exact Next Action

1. Commit G0.1 corrected specification suite and push to `origin/main`.
2. Present G0.1 completion report to the mentor and request formal re-audit for Gate 1 authorization.
3. **DO NOT START GATE 1 BEFORE MENTOR APPROVAL**.
