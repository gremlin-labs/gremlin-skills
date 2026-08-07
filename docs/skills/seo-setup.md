# SEO Setup

Establishes and verifies the technical, analytics, search-console, and keyword-research prerequisites required by an SEO program through guarded source changes, APIs, or signed-in computer use.

## When to reach for it

Use when a project needs initial SEO setup, GA4, Google Search Console, Google Ads Keyword Planner, Bing Webmaster Tools, a working crawl/index foundation, or a trustworthy setup status before SEO research or strategy.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It executes only after its explicit approval gate and may then edit the in-scope project. External actions retain a separate exact-action approval. It must stop for the separately approved external action even when local preparation is complete. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/seo-setup/`. Required contract artifacts currently include `AUDIT.md`, `SEO-SETUP-STATUS.json`, `QUALITY-REPORT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

Only after its explicit approval or execution boundary has been crossed. Preview, audit, or preparation work does not silently authorize mutation.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Optional complements: `seo-foundation`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `user-only` |
| Authority | `executor`; source mutation `after-approval`; external actions `approval-required` |
| Output root | `agent-work/{slug}/seo-setup/` |
| Required skills | None |
| Optional skills | `seo-foundation`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | `python3 skills/growth/seo-setup/scripts/tests/test_seo_stack.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

