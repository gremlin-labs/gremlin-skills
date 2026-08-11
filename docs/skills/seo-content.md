# SEO Content

Benchmarks, challenges, briefs, and executes one SEO-targeted editorial page at a time by combining page-specific competitive research, editorial judgment, primary-source truth, approval, implementation, and comparative verification.

## When to reach for it

Use when a user asks to evaluate, write, refresh, implement, or publish one search-targeted article, guide, comparison, use-case, catalogue, or other editorial page from an SEO Strategy opportunity; route material landing-page persuasion or visual design through landing-page instead.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `prose-humanizer`, `seo-strategy`; optional skills are not assumed to be installed.

## Authority and safety

It begins with read-only page benchmarking and editorial judgment. It may edit the in-scope project only after the exact specialist brief and `PUBLISH` verdict are approved. User-facing SEO changes also require a digest-matching `SEO-CHANGE-LEDGER.json` and `SEO-CHANGE-APPROVAL.json`; shared templates require a canary and separate editorial rollback. External actions retain a separate exact-action approval. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/seo-content/`. Required contract artifacts currently include `BRIEF-VALIDATION.md`, `PAGE-BENCHMARK.md`, `PAGE-REQUIREMENTS.md`, `EDITORIAL-BRIEF.md`, `EDITORIAL-REVIEW.md`, `CONTENT-PLAN.md`, `SOURCE-LEDGER.md`, `CLAIM-LEDGER.md`, `PROGRESS.md`, `CONTENT-RECEIPT.md`, `QUALITY-REPORT.md`. `SEO-CHANGE-LEDGER.json` and `SEO-CHANGE-APPROVAL.json` are conditional implementation artifacts for user-facing changes. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

Only after its editorial approval boundary has been crossed. Opportunity or Strategy approval alone does not authorize source mutation.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`prose-humanizer`, `seo-strategy`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, the exact query and representative pages were benchmarked, truth and competitiveness passed independently, useful persuasive and navigational language was not neutralized mechanically, FAQ utility remains separate from schema eligibility, the title is compelling and durable, the planned catalogue fits, exact approved changes match rendered output, applicable verification gates pass, and the skill stops at its documented authority boundary.

## Adjacent Gremlin skills

- Required package relationships: `prose-humanizer`, `seo-strategy`.
- Optional complements: `seo-indexing`, `seo-monitor`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `model-visible` |
| Authority | `hybrid`; source mutation `after-approval`; external actions `approval-required` |
| Output root | `agent-work/{slug}/seo-content/` |
| Required skills | `prose-humanizer`, `seo-strategy` |
| Optional skills | `seo-indexing`, `seo-monitor`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->
