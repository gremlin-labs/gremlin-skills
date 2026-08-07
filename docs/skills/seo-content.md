# SEO Content

Executes one approved SEO content brief at a time by validating upstream ownership, researching primary sources, locking claims, drafting and humanizing copy, implementing it through project conventions, and verifying search, accessibility, build, rendering, and published behavior.

## When to reach for it

Use when a user asks to write, refresh, implement, or publish one SEO-targeted article, guide, comparison, use-case, or other content page from an approved SEO Strategy brief; route material landing-page persuasion or visual design through landing-page instead.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `prose-humanizer`; optional skills are not assumed to be installed.

## Authority and safety

It may edit the in-scope project when the user’s request authorizes execution. External actions retain a separate exact-action approval. It must stop for the separately approved external action even when local preparation is complete. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/seo-content/`. Required contract artifacts currently include `BRIEF-VALIDATION.md`, `CONTENT-PLAN.md`, `SOURCE-LEDGER.md`, `CLAIM-LEDGER.md`, `PROGRESS.md`, `CONTENT-RECEIPT.md`, `QUALITY-REPORT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

It can, when the user’s request authorizes the execution scope. It must still preserve unrelated work and obey any narrower approval boundary.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`prose-humanizer`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `prose-humanizer`.
- Optional complements: `seo-indexing`, `seo-monitor`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `user-only` |
| Authority | `executor`; source mutation `task-scoped`; external actions `approval-required` |
| Output root | `agent-work/{slug}/seo-content/` |
| Required skills | `prose-humanizer` |
| Optional skills | `seo-indexing`, `seo-monitor`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

