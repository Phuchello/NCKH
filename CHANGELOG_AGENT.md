# AI Agent Activity & Engineering Changelog

This document tracks all engineering actions, gate transitions, and architectural evolutions executed by autonomous AI pair programmers across the **Intel OS / NCKH Intelligence Platform** repository.

---

## Format Standard
Each entry must record:
* **Date & Timestamp**: UTC timestamp
* **Milestone / Gate**: Current gate identifier
* **Agent Role**: Gemini / Antigravity vs Codex
* **Action Summary**: High-level objective completed
* **Files Modified / Created**: Explicit file paths
* **Decisions & Rationale**: Key architectural decisions implemented
* **Verification Performed**: Tests and consistency checks executed

---

## Entries

### [2026-08-16 01:05:00 UTC] — Gate 0.1 (G0.1) Architecture Correction Pass
* **Milestone**: Gate 0.1 (G0.1)
* **Agent Role**: Antigravity (Gemini)
* **Action Summary**:
  * Performed comprehensive architectural repair and specification hardening following the external mentor G0 audit (Score: 77/100, Status: REVISE).
  * **Topic Cardinality**: Replaced 1:N topic ownership with many-to-many junction `document_topics` and made sources globally reusable.
  * **Identity vs Content Hash**: Separated `metadata_fingerprint` (for `DISCOVERED` tier) from `content_hash` (for fetched `document_snapshots` representations).
  * **Document Snapshot Model**: Introduced `document_snapshots` table to track representation versions (e.g. arXiv revisions) and pin claims to exact source versions.
  * **Multi-Provider Reconciliation**: Introduced `document_sources` to track multi-provider discovery provenance while reconciling into a single logical `Document`.
  * **Embedding Model Contract**: Established fixed 768-dimensional vector contract for V1 schema, decoupled from replaceable reasoning LLM providers, with a documented migration protocol.
  * **Schema Reconciliation**: Harmonized all documentation to reference the exact 18 normalized PostgreSQL tables.
  * **Scientific Epistemology**: Decoupled Grounding Status (`VERBATIM_MATCH`), Claim Type, Epistemic Status (default `UNASSESSED`), and Evidence Quality. Verbatim quotes validate presence, not scientific truth.
  * **Scoring Model Calibration**: Renamed novelty to Semantic Distinctiveness Signal and marked all scoring formulas/weights as PROVISIONAL pending G9 calibration.
  * **Search Terminology**: Corrected "BM25" references to "PostgreSQL full-text lexical retrieval (`tsvector`/`tsquery`)".
  * **Security Wording**: Calibrated security claims to defense-in-depth and risk reduction framing.
* **Files Modified**:
  * `README.md`
  * `ARCHITECTURE.md`
  * `DECISIONS.md`
  * `TODO.md`
  * `CHANGELOG_AGENT.md`
  * `PROJECT_STATE.md`
  * `.env.example`
  * `docs/PRODUCT_SPEC.md`
  * `docs/ARCHITECTURE_DETAILED.md`
  * `docs/DATA_MODEL.md`
  * `docs/PIPELINE.md`
  * `docs/MILESTONES.md`
  * `docs/SECURITY_MODEL.md`
  * `docs/SCORING_MODEL.md`
  * `docs/INTELLIGENCE_MODEL.md`
* **Verification**:
  * Full cross-document audit confirming 100% internal consistency across all 14 specification files and `.env.example`.
  * Zero application feature code introduced.
* **Status**: G0.1 Completed. Checkpoint ready for mentor re-audit.

---

### [2026-08-16 00:50:00 UTC] — Gate 0 (G0) Foundation & Architecture Baseline
* **Milestone**: Gate 0 (G0)
* **Agent Role**: Antigravity (Gemini)
* **Action Summary**:
  * Initialized local git repository, connected cleanly to remote `Phuchello/NCKH` on branch `main`.
  * Authored initial G0 architectural specification suite covering all 14 foundational documents.
  * Modeled three durable intellectual assets: Intelligence Lake, Personal Research Memory, and Research Opportunity Memory.
* **Commit**: `dbb55ac148771a80c565f544fe229dd9cd618fc6`
* **Status**: G0 Initial Submission (Scored 77/100, Proceeded to G0.1).
