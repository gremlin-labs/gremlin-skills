<!-- GENERATED CONTRACT SNAPSHOT
contract: seo-page-quality
source: contracts/seo-page-quality.md
source-version: 1
semantic-owner: seo-content
source-sha256: b88a3ae7b5911d497606b724492fda6adb99463027fa75f97d2201bbc4a7b57c
DO NOT EDIT: run python3 scripts/materialize_contracts.py --write
-->

<!-- contract-metadata
id: seo-page-quality
version: 1
semantic-owner: seo-content
-->

# SEO Page Quality Contract

Apply this contract before approving or implementing a search-targeted page. It separates market evidence, editorial judgment, and technical correctness so a truthful, valid implementation cannot pass when the page itself is strategically weak.

## Contents

- [Evidence boundary](#evidence-boundary)
- [Page-specific benchmark](#page-specific-benchmark)
- [Requirement strength](#requirement-strength)
- [Editorial decision](#editorial-decision)
- [Title and catalogue durability](#title-and-catalogue-durability)
- [Comparative draft review](#comparative-draft-review)
- [Technical verification](#technical-verification)
- [Required outputs](#required-outputs)

## Evidence boundary

Keep these statements distinct:

- `OBSERVED` — directly visible in a dated, scoped source, page, SERP, product, or first-party dataset.
- `INFERRED` — a reasoned interpretation of one or more observations; include the reasoning and plausible alternatives.
- `HYPOTHESIS` — a testable proposition that may guide research but cannot become an implementation requirement.
- `UNSUPPORTED` — not established by available evidence; exclude it from recommendations and acceptance gates.

Competitor recurrence and current rankings show what is present, not why a page ranks or converts. Never turn repeated wording, modules, methodology, testing language, page length, or section order into a causal ranking claim. Search-result snippets are discovery evidence, not a substitute for inspecting the pages.

## Page-specific benchmark

Before shaping a page, inspect the exact proposed owner or current owner plus a representative set of current results and full pages for the target query and intent. Record:

- query and intent;
- market, language, device or context, engine, and retrieval date;
- material SERP features and page roles;
- current owner, protected winners, and overlap exclusions;
- representative competing pages and why each is relevant;
- the user job each page appears to serve;
- title promise, information architecture, catalogue or data model, proof, interaction, and conversion path actually observed;
- table stakes, useful divergences, weaknesses, and unserved needs;
- counterevidence, inaccessible evidence, volatility, and remaining uncertainty.

Continue until the next representative page adds no material page-role, user-job, or competitive evidence, or until a documented limitation prevents a responsible decision. Do not use a universal result count or copy a competitor's distinctive structure or language.

## Requirement strength

Classify every proposed page requirement:

- `MUST` — necessary for the verified user job, product truth, claim integrity, accessibility, or directly evidenced page-role fit.
- `OPTIONAL` — potentially useful, but not required by current evidence.
- `TEST` — a hypothesis with a named validation method, failure signal, and reversible treatment.
- `REJECTED` — copied convention, unsupported claim, brittle structure, or requirement whose cost or risk exceeds its evidenced value.

Every `MUST` cites the evidence and states what would invalidate it. Competitor presence alone cannot produce a `MUST`. Methodology, authorship, firsthand testing, comparison tables, or “tested recommendations” become mandatory only when the page's actual claims require that evidence. If the evidence cannot be produced, narrow the claim, choose another page role, or do not publish.

## Editorial decision

Evaluate truth and competitiveness independently:

| Truth status | Competitive status | Decision |
|---|---|---|
| Unsupported or misleading | Not competitive | `NO PAGE` |
| Unsupported or misleading | Competitive premise | `REVISE` or `BLOCKED`; never publish |
| Truthful | Not competitive | `REVISE` or `NO PAGE` |
| Truthful | Competitive | Eligible for approval and implementation |

A page is competitive only when the evidence supports all applicable statements:

- it satisfies the target user job in a page role compatible with the current SERP;
- it gives the user a concrete reason to choose it over the current owner and representative alternatives;
- its information gain is real, supportable, and substantial enough to justify the page or refresh;
- its title and search promise are specific, compelling, accurate, and fulfilled by the page;
- its structure can hold the planned content or catalogue without immediate rework;
- an experienced editor could defend publishing it now rather than improving the current owner or doing nothing.

Use one verdict: `PUBLISH`, `REVISE`, `NO PAGE`, or `BLOCKED`. `PUBLISH` means editorially eligible for approval; it does not authorize source mutation, deployment, CMS publication, or external actions.

## Title and catalogue durability

Review the proposed title, H1, description, and framing together. They must be truthful without becoming generic, distinguishable without unsupported superlatives, and compelling without clickbait.

Apply an evergreen and catalogue test:

- Would the title still make sense after the next routine inventory, product, or data update?
- Does a count, year, version, or other volatile fact update automatically and atomically everywhere it appears?
- If the page is intentionally a dated snapshot, is that scope useful and unmistakable?
- Can the information architecture accommodate the planned catalogue, filters, comparisons, examples, and future additions?

A mutable inventory count must not be frozen into an evergreen title unless automation keeps it correct or the page is explicitly a dated snapshot. Removing an unsupported “best” or comparative claim is only a truth correction; the replacement must still communicate a differentiated, useful promise.

## Comparative draft review

Before implementation approval and again against the rendered result, compare the proposed page with the benchmark:

1. Does it match the query's actual user job and expected page role?
2. Is its title more useful and compelling while remaining truthful and durable?
3. Does its structure fit the promised catalogue or task?
4. What does it do materially better or differently?
5. Is every advantage visible in the draft rather than asserted in a brief?
6. Would publishing it improve the portfolio, or should the current owner be refreshed instead?
7. What evidence or market change would reverse the verdict?

Record concrete revision requests. “Looks good,” artifact completeness, and internal consistency are not editorial evidence.

## Technical verification

Claims, sources, URL ownership, canonical and index posture, metadata, structured data, links, accessibility, performance, builds, rendering, deployment, receipts, and rollback remain required where applicable. They are necessary safeguards, not substitutes for the page-specific benchmark and editorial verdict.

A technical gate cannot change `REVISE`, `NO PAGE`, or `BLOCKED` into `PUBLISH`.

## Required outputs

The owning page specialist records:

- `PAGE-BENCHMARK.md` — scope, current owner, representative pages, observed page roles, competitive patterns, gaps, limitations, and evidence statuses.
- `PAGE-REQUIREMENTS.md` — `MUST`, `OPTIONAL`, `TEST`, and `REJECTED` requirements with evidence and invalidation conditions.
- `EDITORIAL-REVIEW.md` — title and catalogue tests, comparative review, truth/competitiveness matrix, exact verdict, approval state, and material revisions.

The artifacts may be combined only when every heading and decision remains explicit. Preserve them with the same slug and cite them from implementation and publication receipts.
