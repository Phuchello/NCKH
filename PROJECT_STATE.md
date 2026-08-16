# Intel OS / NCKH Intelligence Platform — Project State & Safety Checkpoint

## 1. Milestone Tracking

* **Current Milestone**: **Gate 0 (G0) — Foundation & Architecture Kickoff**
* **G0 Completion Percentage**: **100%**
* **Active Working Branch**: `main`
* **Remote Repository**: `https://github.com/Phuchello/NCKH`
* **Status**: **G0 COMPLETED — Awaiting Mentor Review**

---

## 2. What Exists (G0 Deliverables)

1. **Authoritative Specification & Architecture Suite**:
   * [`README.md`](README.md): System executive summary, 3 intellectual assets, provenance requirements, storage topology.
   * [`ARCHITECTURE.md`](ARCHITECTURE.md): System architecture, subsystem decomposition, storage tiers, mermaid topology.
   * [`DECISIONS.md`](DECISIONS.md): Architecture Decision Records (ADRs 0001 through 0008).
   * [`TODO.md`](TODO.md): Complete engineering task backlog organized from Gate 0 through Gate 10.
   * [`CHANGELOG_AGENT.md`](CHANGELOG_AGENT.md): Full audit trail of AI agent actions and architectural milestones.
   * [`docs/PRODUCT_SPEC.md`](docs/PRODUCT_SPEC.md): Target personas, core epics, functional/non-functional requirements, explicit non-goals.
   * [`docs/ARCHITECTURE_DETAILED.md`](docs/ARCHITECTURE_DETAILED.md): Granular technical specifications for all 7 platform subsystems.
   * [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md): PostgreSQL 16+ DDL schema, pgvector vector column configurations, constraints, and recursive SQL lineage queries.
   * [`docs/PIPELINE.md`](docs/PIPELINE.md): End-to-end 8-stage intelligence lifecycle (`Collect → Filter → Verify → Connect → Analyze → Remember → Synthesize → Act`) and multi-tier retention funnel.
   * [`docs/MILESTONES.md`](docs/MILESTONES.md): Comprehensive Gate 0 to Gate 10 roadmap with hard deliverables and acceptance criteria.
   * [`docs/SECURITY_MODEL.md`](docs/SECURITY_MODEL.md): Defense-in-depth threat matrix, SSRF IP-blocking perimeter, and XML-delimited prompt injection safeguards.
   * [`docs/SCORING_MODEL.md`](docs/SCORING_MODEL.md): Mathematical scoring formulations for source credibility, claim relevance, evidence rigor, gap potential, and candidate idea priority.
   * [`docs/INTELLIGENCE_MODEL.md`](docs/INTELLIGENCE_MODEL.md): Epistemic status ladder, asset ontology, and bidirectional Idea Lineage mechanics.

2. **Environment & Configuration Templates**:
   * [`.gitignore`](.gitignore): Python, Node.js, local data cache, and sensitive secret exclusions.
   * [`.env.example`](.env.example): Comprehensive configuration blueprint for PostgreSQL, pgvector, S3/R2 storage, AI reasoning APIs, and crawler limits.

3. **Repository Cleanliness**:
   * Safe git initialization on `main` branch synchronized with remote `origin/main` without rewriting remote history.

---

## 3. What Does NOT Exist (Strict Gate Boundaries)

To ensure disciplined execution, the following components are strictly deferred to subsequent gates and are **not** present in G0:

* **No live crawler fleet or connector implementation code** (Deferred to Gate 2).
* **No LLM extraction runners, prompt scripts, or OpenAI/Gemini execution calls** (Deferred to Gate 3).
* **No live database schema migration execution or running database instances** (Deferred to Gate 1).
* **No research gap mining or automated hypothesis generation code** (Deferred to Gate 5).
* **No research handbook compilation or PDF/LaTeX generation code** (Deferred to Gate 7).
* **No Next.js UI frontend code, dashboard components, or chat interfaces** (Deferred to Gate 8).
* **No custom model training or fine-tuning pipelines** (Explicit platform non-goal for G0–V1).

---

## 4. Known Risks & Architectural Mitigations

| Identified Risk | Severity | Architectural Mitigation in G0 |
| :--- | :--- | :--- |
| **SSRF via crawler fetch** | CRITICAL | Pre-flight DNS resolution blocking RFC 1918 private subnets and metadata IPs (`169.254.169.254`). See `docs/SECURITY_MODEL.md`. |
| **Indirect Prompt Injection in crawled papers** | HIGH | Strict XML sandboxing delimiters (`<untrusted_document_content>`), Pydantic schema validation, and verbatim quote verification before storing claims. |
| **Unbounded Local Storage Bloat** | HIGH | Multi-tier retention funnel (`DISCOVERED → INDEXED → RELEVANT → RETAINED → ARCHIVED`), metadata-only default intake, and `MAX_LOCAL_CACHE_GB` quota with automated LRU cleanup. |
| **LLM Citation Hallucination** | HIGH | Verbatim quote grounding requirement; claims failing exact substring verification against source text are discarded. |
| **Opaque Research Idea Genesis** | MEDIUM | Explicit relational Idea Lineage records (`Idea → Opportunity → Gap → Claim → Document → Source`) instead of opaque vector-only similarity. |

---

## 5. Tests & Consistency Checks Performed

1. **Document Completeness & Cross-Referencing**: Verified that all 14 required files exist, have consistent naming, and reference uniform table schemas and ontological terms.
2. **Data Model Integrity**: Verified that `docs/DATA_MODEL.md` DDL includes all necessary foreign keys, indexes, pgvector column definitions, and recursive CTE query syntax.
3. **Storage Tiering Validation**: Confirmed that storage topologies across `README.md`, `ARCHITECTURE.md`, `docs/ARCHITECTURE_DETAILED.md`, and `docs/PIPELINE.md` uniformly respect cloud-first principles and retention funnel tiers.
4. **Git Repository Status**: Confirmed clean git tracking on branch `main` ready for commit and push.

---

## 6. Last Safe Checkpoint

* **Checkpoint Tag**: `G0-COMPLETED`
* **Commit**: `ac0d88817ee56a75b8e26f3918c05e87bd0d8b41` (G0 Specification Baseline)
* **Working Tree**: Clean.

---

## 7. Exact Next Action

1. Submit G0 baseline commit and push to `origin/main`.
2. Present G0 completion report to the mentor/user and request explicit review and approval.
3. **Await mentor approval before initiating Gate 1 (Backend Core & Database Initialization)**.
