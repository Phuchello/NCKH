# Intel OS / NCKH — Intellectual Property & Repository Boundary Policy

## 1. Purpose

Intel OS / NCKH is intended to remain **publicly assessable and professionally presentable** while preserving ownership and control over proprietary implementation, private research memory, unpublished research work, and strategically sensitive logic.

The project follows a **Public Showcase + Private Core** model.

This policy is an engineering/repository governance rule. It is not a substitute for professional legal advice for patents, commercialization, university IP agreements, competitions, funding, or other high-value intellectual-property decisions.

---

## 2. Repository model

### Public Showcase — `Phuchello/NCKH`

This repository is the project's **active public front page**, not an abandoned mirror.

Its role is to communicate:

- project vision and motivation;
- high-level architecture;
- milestone history and gate decisions;
- verified test / reliability summaries;
- public benchmarks and selected results;
- screenshots and product demonstrations;
- sanitized examples;
- public API/interface documentation where disclosure is safe;
- public research notes intentionally released;
- papers, posters, presentations, preprints and published research outputs after disclosure review;
- selected implementation artifacts explicitly approved for release.

The public repository should stay current as the private product evolves.

At every major gate, the public repository should receive a **sanitized but substantive progress report** describing what was achieved, how it was verified, known limitations, and the current project status.

The public repository is **source-available/proprietary, not open source**.

### Private Core — `Phuchello/NCKH-core-private`

This repository is the authoritative implementation workspace for proprietary G2+ engineering.

It includes by default:

- authoritative ingestion/reconciliation implementation;
- proprietary ranking/scoring logic;
- intelligence extraction orchestration;
- private prompt libraries and internal reasoning policies;
- Research Gap / Opportunity mining implementation;
- idea-generation and idea-lineage internals;
- private evaluation harnesses that expose decision logic;
- production deployment configuration;
- unreleased algorithms and research methods;
- internal experiments and failed hypotheses;
- private datasets and derived corpora;
- Personal Research Memory and user-specific intelligence data.

The private repository is the engineering source of truth. The public repository is the communication/research showcase source of truth.

---

## 3. Core publication principle

The project must not choose between **visibility** and **ownership**. Instead:

```text
PRIVATE CORE
    implement
       ↓
    test
       ↓
    mentor / technical review
       ↓
    disclosure classification
       ↓
    sanitize where required
       ↓
PUBLIC SHOWCASE
    milestone report
    verified metrics
    architecture overview
    screenshots / demo
    selected benchmark results
    publication artifacts
```

A feature being private does **not** mean its existence, capability, evaluation result, or safe high-level architecture should disappear from the public project narrative.

Conversely, a desire for a polished public repository does not justify publishing proprietary internals.

---

## 4. Disclosure classification

Every substantial artifact should be classified before publication.

### PUBLIC

Safe/intended for release, for example:

- README/product description;
- high-level diagrams;
- roadmap and milestone status;
- sanitized test/CI summaries;
- screenshots and demos;
- public research outputs;
- sanitized benchmark summaries;
- published methodology already intentionally disclosed;
- public-facing API contracts;
- selected examples that do not expose proprietary core logic.

### PRIVATE

Not intended for public release by default:

- Research Memory;
- user notes;
- unpublished research gaps and hypotheses;
- proprietary prompt chains;
- internal scoring weights/rules when strategically sensitive;
- unreleased algorithms;
- credentials and secrets;
- private datasets;
- licensed/copyrighted source corpora that cannot be redistributed;
- internal evaluation data that exposes proprietary logic;
- production deployment details;
- commercial strategy.

### REVIEW BEFORE PUBLICATION

Artifacts requiring explicit disclosure review:

- novel algorithms;
- potentially patentable methods;
- detailed research methodology before filing/publication decisions;
- unpublished experimental results;
- model-training datasets;
- competitive product logic;
- data-source licensing edge cases;
- architecture details that substantially reveal private implementation.

---

## 5. Public milestone reporting standard

For each major Gate / release, the public showcase should publish, when safe:

1. milestone objective;
2. capabilities completed;
3. high-level architecture impact;
4. verified test / CI result;
5. benchmark or experiment result where meaningful;
6. known limitations;
7. mentor/gate decision;
8. screenshots or demo artifacts when real output exists;
9. public research outputs / publication links;
10. disclosure note for intentionally private implementation.

Reports should be specific enough for lecturers, researchers, recruiters, collaborators, or reviewers to evaluate the work.

Do not use vague claims such as "advanced AI system complete" without verifiable supporting results.

Do not fabricate screenshots, benchmarks, user numbers, production-scale claims, or research results merely to make the public repository look polished.

Public progress is maintained in [`PUBLIC_PROGRESS.md`](PUBLIC_PROGRESS.md).

---

## 6. Research publication / patent-safety gate

Before publicly releasing a potentially novel technical contribution, ask:

1. Is this already intentionally published in a paper/preprint/thesis?
2. Could this be patentable or commercially valuable?
3. Is there a university, supervisor, sponsor, competition, or funding agreement affecting ownership?
4. Would disclosure destroy trade-secret value?
5. Are third-party datasets, papers, code, or licenses involved?
6. Is detailed release necessary now, or can a high-level result be published instead?

If patent or commercialization potential is material, detailed public disclosure should pause for appropriate IP review.

---

## 7. Research data policy

The public repository must not contain the authoritative research dataset or intelligence memory.

### Never commit

- API keys/tokens/passwords;
- database dumps containing research memory;
- private notes;
- licensed PDFs or bulk copyrighted corpora without redistribution rights;
- unpublished experiment datasets unless explicitly approved;
- production environment files;
- local caches;
- private embeddings or derived datasets when strategically sensitive.

### Public datasets

Any dataset intentionally released publicly should have:

- clear provenance;
- redistribution-rights review;
- privacy review where applicable;
- dedicated dataset terms/license where appropriate;
- a versioned release rather than an accidental working-directory dump.

---

## 8. Agent governance

All development/review agents must follow:

> **Never infer that a file is safe to publish merely because the public showcase exists.**

For G2+ work, agents must identify whether a task belongs to private engineering or public reporting before writing files.

### Private engineering

Gemini / Antigravity, Claude Opus, Codex, or other development agents work in the private core when implementing proprietary functionality.

### Public reporting

After a gate or meaningful milestone, an explicit disclosure/reporting step updates `Phuchello/NCKH` with safe:

- status;
- verified metrics;
- architecture summary;
- demo/research artifacts;
- known limitations.

No agent should allow the public showcase to drift several gates behind the private implementation.

---

## 9. Third-party rights

Project ownership does not override third-party licenses or copyrights.

Before redistributing code, papers, datasets, figures, standards text, or model artifacts, verify the applicable terms.

A proprietary project may use open-source dependencies while those components remain governed by their original licenses and obligations.

---

## 10. Current decision

Effective 2026-08-16:

- `Phuchello/NCKH` is the **active public showcase / verified-results / research-publication repository**.
- `Phuchello/NCKH-core-private` is the **authoritative private implementation repository**.
- The public repository is **not open source**.
- G0/G1 and an earlier accidentally public G2 commit must be treated as historically disclosed; history is not rewritten to imply otherwise.
- Current G2 implementation lives in the private core and is under mentor review.
- The public repository must continue to receive professional, substantive milestone reports as private development progresses.

See the root [`LICENSE`](../LICENSE), [`NOTICE.md`](../NOTICE.md), and [`PUBLIC_PROGRESS.md`](PUBLIC_PROGRESS.md).
