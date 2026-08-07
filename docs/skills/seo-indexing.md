# SEO Indexing

Runs a guarded post-publication indexing-assistance loop that discovers new or materially updated canonical pages, verifies live crawl and index readiness, prioritizes an approved batch, requests Google indexing through supported signed-in computer use or an eligible restricted API, and records immutable receipts.

## When to reach for it

Use when a user asks to submit URLs to Google Search Console, request indexing or recrawling, process a daily indexing queue, create an indexing reminder or recurring agent job, or verify and submit newly published SEO pages.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It executes within its artifact or external-operation boundary without editing project source. External actions retain a separate exact-action approval. It must stop for the separately approved external action even when local preparation is complete. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/seo-indexing/`. Required contract artifacts currently include `INDEXING-BRIEF.md`, `INDEXING-STATUS.md`, `URL-QUEUE.csv`, `SUBMISSION-HISTORY.md`, `runs/{run-id}/DISCOVERY.md`, `runs/{run-id}/URL-VERIFICATION.csv`, `runs/{run-id}/RUN-REPORT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Optional complements: `seo-monitor`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `user-only` |
| Authority | `executor`; source mutation `never`; external actions `approval-required` |
| Output root | `agent-work/{slug}/seo-indexing/` |
| Required skills | None |
| Optional skills | `seo-monitor`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

