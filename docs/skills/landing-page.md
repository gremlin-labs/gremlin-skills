# Landing Page

Designs conversion-focused landing pages and optionally implements an approved preview through product-truth discovery, messaging approval, adaptive HTML previews, humanized copy, SEO, purposeful TurbulenceJS motion, and integrated verification.

## When to reach for it

Use when a user asks to create, redesign, optimize, preview, or implement a product, campaign, launch, signup, or marketing landing page; do not use for broad product art direction, a site-wide design-system audit, or copy-only editing.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `prose-humanizer`, `seo-strategy`; optional skills are not assumed to be installed.

## Authority and safety

It begins without project-source mutation. Source mutation is allowed only after the skill’s explicit approval or execution gate. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/landing-page/`. Required contract artifacts currently include `RESEARCH.md`, `MESSAGE-MAP.md`, `COPY-DECK.md`, `SEO-PLAN.md`, `PAGE-DIRECTIONS.md`, `LANDING-PAGE-PREVIEW.html`, `previews/LANDING-PAGE-PREVIEW-R{n}.html`, `PROGRESS.md`, `QUALITY-REPORT.md`. Search-targeted work also requires `PAGE-BENCHMARK.md`, `PAGE-REQUIREMENTS.md`, and `EDITORIAL-REVIEW.md` before message approval. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

Only after its explicit approval or execution boundary has been crossed. Preview, audit, or preparation work does not silently authorize mutation.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`prose-humanizer`, `seo-strategy`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, search-targeted pages pass page-specific competitive, title, catalogue, and editorial gates, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `prose-humanizer`, `seo-strategy`.
- Optional complements: `theme-library`, `turbulencejs-integration`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `experience` (promoted) |
| Invocation | `model-visible` |
| Authority | `hybrid`; source mutation `after-approval`; external actions `none` |
| Output root | `agent-work/{slug}/landing-page/` |
| Required skills | `prose-humanizer`, `seo-strategy` |
| Optional skills | `theme-library`, `turbulencejs-integration` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->
