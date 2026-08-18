# Intel OS — Public / Private Repository Policy

## 1. Purpose

Intel OS uses a **Public Showcase + Private Core** repository model.

The goal is to keep the project visible and assessable for lecturers, researchers, recruiters, collaborators and future publications without turning the proprietary implementation, private research memory or unpublished research work into an open-source codebase.

This is a repository-governance policy, not legal advice for patents, commercialization, university ownership or funding agreements.

---

## 2. Repository roles

### Public Showcase — `Phuchello/NCKH`

The public repository is the project's active front page and verified-results surface.

It may contain intentionally released material such as:

- project vision and motivation;
- disclosure-safe architecture;
- verified milestone/gate history;
- sanitized test and benchmark summaries;
- synthetic screenshots and public demos;
- known limitations that are safe to disclose;
- public papers, posters, presentations and research outputs;
- selected interface documentation or implementation samples when explicitly approved.

The public repository should remain substantive and current, but it is **not an installable mirror of the private core**.

### Private Core — `Phuchello/NCKH-core-private`

The private repository is the authoritative engineering workspace and source of truth for proprietary G2+ development.

Private by default:

- current implementation and production internals;
- schemas and migrations not intentionally released;
- ingestion/reconciliation implementation;
- proprietary ranking, scoring and reasoning logic;
- prompt/orchestration rules;
- private evaluation fixtures and detailed evidence;
- detailed security attack paths and countermeasure implementation;
- production/operational configuration;
- Personal Research Memory and Research Opportunity Memory;
- private datasets and derived corpora;
- unpublished gaps, hypotheses, ideas, experiments and negative results;
- credentials, tokens and secrets.

---

## 3. Publication flow

```text
PRIVATE CORE
implement
   ↓
test
   ↓
evidence
   ↓
mentor / technical review
   ↓
disclosure review
   ↓
sanitize
   ↓
PUBLIC SHOWCASE
verified progress
architecture summary
demo / screenshots
selected results
publications
```

A feature being private does **not** mean its existence or verified high-level outcome should disappear from the public project narrative.

Conversely, a polished public repository does not justify publishing proprietary internals.

---

## 4. Disclosure classes

### PUBLIC

Safe/intended for release, for example:

- README/product description;
- high-level diagrams;
- roadmap and milestone status;
- sanitized CI/test summaries;
- synthetic screenshots/demos;
- published research outputs;
- disclosure-safe benchmark conclusions;
- selected examples that do not reveal proprietary core logic.

### PRIVATE

Keep private by default:

- user/research memory;
- unpublished gaps, ideas, hypotheses and experiments;
- proprietary prompts and orchestration;
- scoring weights/rules and competitive implementation logic;
- credentials/secrets;
- private datasets or licensed corpora;
- internal evaluation data exposing proprietary decision logic;
- production operational details.

### REVIEW BEFORE PUBLICATION

Requires explicit review:

- potentially novel or patentable methods;
- detailed methodology before publication/IP decisions;
- unpublished experimental results;
- model-training datasets;
- data-source licensing edge cases;
- architecture detail that would materially reveal private implementation.

If publication safety is uncertain, keep the artifact private until reviewed.

---

## 5. Public milestone standard

For each major approved gate or release, the public showcase should publish as much of the following as is safe and meaningful:

1. milestone purpose;
2. capabilities completed;
3. high-level architecture impact;
4. verified test/CI results;
5. benchmark or experiment results where appropriate;
6. known limitations;
7. Mentor/gate decision;
8. synthetic screenshots/demo artifacts where available;
9. public research/publication links;
10. a disclosure note for intentionally private implementation.

Do not publish vague claims such as “advanced AI system complete” without evidence.

Do not fabricate screenshots, benchmarks, user counts, production-scale claims or research results to improve presentation.

The current disclosure-safe milestone record is [Public Progress & Verified Results](PUBLIC_PROGRESS.md).

---

## 6. Data and research safety

Never commit to the public showcase:

- API keys, passwords or tokens;
- production `.env` files;
- database dumps containing private research memory;
- private notes or user history;
- unpublished experiment datasets unless explicitly approved;
- licensed full-text corpora without redistribution rights;
- private embeddings/derived datasets when strategically sensitive;
- local caches or production operational artifacts.

Any dataset intentionally released publicly should have provenance, redistribution-rights review, privacy review where applicable and a deliberate versioned release.

---

## 7. Research / IP precaution

Before publishing a potentially novel technical contribution, ask:

1. Is it already intentionally published in a paper, preprint or thesis?
2. Could it be patentable or commercially valuable?
3. Is a university, supervisor, sponsor, competition or funding agreement relevant?
4. Would disclosure destroy useful trade-secret value?
5. Are third-party data/code/licensing obligations involved?
6. Is detailed release necessary, or is a high-level result sufficient?

If patent/commercialization potential is material, detailed disclosure should pause for appropriate IP review.

---

## 8. Historical disclosure rule

G0/G1 and an early G2 implementation were previously visible in the public repository.

That history is treated as already disclosed and is **not rewritten or falsely described as never public**. The current branch may remove old working-tree files for clarity and boundary hygiene while Git history remains intact.

---

## 9. Current operating rule

As of the current V1 hardening phase:

- `Phuchello/NCKH-core-private` remains the authoritative implementation repository;
- `Phuchello/NCKH` remains the active public showcase;
- public milestone status remains at the last actually approved/disclosed gate until the next disclosure review;
- G10/V1 hardening work is not automatically public just because a deployment or CI run exists;
- the public repository is proprietary and **not open source**.

See [LICENSE](../LICENSE), [NOTICE.md](../NOTICE.md), [Architecture Overview](../ARCHITECTURE.md) and [Public Progress & Verified Results](PUBLIC_PROGRESS.md).
