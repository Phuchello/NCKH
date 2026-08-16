# Intel OS / NCKH — Intellectual Property & Repository Boundary Policy

## 1. Purpose

Intel OS / NCKH is intended to be publicly presentable while preserving ownership and control over its implementation, private research memory, proprietary reasoning workflows, and future novel research contributions.

The project therefore follows a **Public Showcase + Private Core** model.

This policy is an engineering/repository governance rule. It is not a substitute for professional legal advice for patents, commercialization, university IP agreements, or other high-value intellectual-property decisions.

---

## 2. Repository Model

### Public Showcase Repository

`Phuchello/NCKH` remains the public-facing project repository.

Its role is to communicate:

- project vision and motivation;
- high-level architecture;
- milestone history;
- public research notes that are intentionally released;
- screenshots and product demonstrations;
- sanitized examples;
- public benchmarks and reproducible results selected for release;
- public API/interface documentation where disclosure is safe;
- papers, posters, presentations, and research outputs after publication review;
- selected non-sensitive implementation material explicitly approved for disclosure.

The public repository is **source-available/proprietary**, not open source.

### Private Core Repository

From Gate 2 onward, the authoritative implementation of proprietary core functionality should live in a private repository.

The private core includes, by default:

- ingestion and reconciliation engine implementation;
- proprietary ranking/scoring logic;
- intelligence extraction orchestration;
- prompt libraries and internal reasoning policies;
- Research Gap / Opportunity mining implementation;
- idea-generation and idea-lineage internals;
- private evaluation harnesses that reveal proprietary decision logic;
- production deployment configuration;
- private connectors/configuration when disclosure would expose operational details;
- unreleased algorithms and research methods;
- internal experiments and failed hypotheses;
- private datasets and derived corpora;
- Personal Research Memory and user-specific intelligence data.

The private repository is the authoritative engineering source for these components.

---

## 3. Gate Boundary

### Already Public

G0 and G1 material has already been published in the public repository. That history should be treated as disclosed and should not be relied upon as a trade secret.

Do not rewrite public Git history merely to create the appearance that prior disclosure did not happen.

### From G2 Forward

Before implementing proprietary G2+ functionality, agents must verify the target repository.

**Default rule:**

```text
PUBLIC NCKH REPO
    documentation / showcase / intentionally released material

PRIVATE CORE REPO
    authoritative proprietary implementation
```

No agent may place new proprietary-core implementation into the public repository merely because an earlier milestone was developed there.

---

## 4. Public Disclosure Classification

Every substantial artifact should be classified before publication.

### PUBLIC

Safe/intended for release, for example:

- README/product description;
- high-level diagrams;
- screenshots;
- public research outputs;
- sanitized benchmark summaries;
- published methodology already intentionally disclosed;
- public-facing API contracts;
- selected examples that do not expose proprietary core logic.

### PRIVATE

Not intended for public release, including:

- Research Memory;
- user notes;
- unpublished research gaps and hypotheses;
- proprietary prompt chains;
- internal scoring weights/rules when strategically sensitive;
- unreleased algorithms;
- credentials and secrets;
- private datasets;
- licensed/copyrighted source corpora that cannot be redistributed;
- internal evaluation data;
- deployment secrets;
- commercial strategy.

### REVIEW BEFORE PUBLICATION

Artifacts requiring an explicit disclosure review:

- novel algorithms;
- potentially patentable methods;
- detailed research methodology before filing/publication decisions;
- unpublished experimental results;
- model-training datasets;
- competitive product logic;
- data-source licensing edge cases;
- architecture details that would reveal the private implementation substantially.

---

## 5. Research Publication / Patent-Safety Gate

Before publicly releasing a potentially novel technical contribution, ask:

1. Is this already intentionally published in a paper/preprint/thesis?
2. Could this be a patentable invention or part of one?
3. Is there a university, supervisor, sponsor, competition, or funding agreement affecting ownership?
4. Would disclosure destroy trade-secret value?
5. Are third-party datasets, papers, code, or licenses involved?
6. Is public release necessary now, or can a high-level description be published instead?

If patent or commercialization potential is material, pause detailed public disclosure until an appropriate IP review is completed.

---

## 6. Research Data Policy

The public repository must not contain the authoritative research dataset or intelligence memory.

### Never commit

- API keys/tokens/passwords;
- database dumps containing personal research memory;
- private notes;
- licensed PDFs or bulk copyrighted corpora without redistribution rights;
- unpublished experiment datasets unless explicitly approved;
- production environment files;
- local caches;
- private embeddings or derived datasets when strategically sensitive.

### Public release datasets

Any dataset intentionally released publicly should have:

- a clear provenance record;
- redistribution-rights review;
- privacy review if applicable;
- a dedicated dataset license/terms where appropriate;
- a versioned release rather than an accidental working-directory dump.

---

## 7. Agent Governance

All AI development agents must follow this rule:

> **Never infer that a file is safe to publish simply because the repository is currently public.**

Before substantial G2+ work, the agent must identify whether the task belongs to the public showcase or private core.

### Gemini / Antigravity

Primary builder. Must implement proprietary G2+ core only in the private repository once created.

### Claude Opus

May review private architecture, reconciliation logic, scientific reasoning, and disclosure boundaries.

### Codex

May work on private core for difficult engineering tasks when explicitly authorized. Do not publish private-core fixes into the public showcase unless intentionally sanitized.

### Mentor / Gate Review

Every gate review should include an **IP disclosure check** in addition to engineering quality.

---

## 8. Public Release Workflow

Preferred flow:

```text
PRIVATE CORE
    ↓
implement + test + internal review
    ↓
classify disclosure
    ↓
sanitize / remove secrets & proprietary internals
    ↓
PUBLIC SHOWCASE
    ↓
README / demo / benchmark / docs / paper links
```

The public repository should communicate capability without becoming the authoritative copy of proprietary implementation.

---

## 9. Third-Party Rights

Project ownership does not override third-party licenses or copyrights.

Before redistributing code, papers, datasets, figures, standards text, or model artifacts, verify the applicable terms.

A proprietary repository may still contain dependencies under open-source licenses, provided their license obligations are followed. Those third-party components remain under their original licenses.

---

## 10. Current Decision

Effective from 2026-08-16:

- `Phuchello/NCKH` is the **public showcase / source-available proprietary repository**.
- It is **not an open-source project**.
- New proprietary-core implementation from **Gate 2 onward is paused in this public repository** until the private core repository is established.
- The public repository may continue to receive sanitized documentation, demos, research outputs, and deliberately disclosed artifacts.

See the root [`LICENSE`](../LICENSE) and [`NOTICE.md`](../NOTICE.md).
