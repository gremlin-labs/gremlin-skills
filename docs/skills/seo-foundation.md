# SEO Foundation

Builds an evidence-backed SEO foundation by discovering and confirming business and organic competitors, inspecting representative pages, sampling Google and Bing results, combining first-party queries with Google Ads Keyword Planner demand, and assigning keyword clusters to page owners without prescribing page content.

## When to reach for it

Use when a user asks for SEO competitor research, keyword or search-term research, a competitive search analysis, keyword clustering, cannibalization prevention, or the research foundation for an SEO strategy.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/seo-foundation/`. Required contract artifacts currently include `FOUNDATION-BRIEF.md`, `SITE-BASELINE.md`, `COMPETITORS.md`, `COMPETITOR-ANALYSIS.md`, `EVIDENCE-LEDGER.md`, `SERP-SNAPSHOTS.md`, `KEYWORD-DEMAND.csv`, `KEYWORD-DEMAND.md`, `KEYWORD-CLUSTERS.md`, `PAGE-OWNERSHIP.md`, `SEO-FOUNDATION.md`. Material conclusions are labelled `OBSERVED`, `INFERRED`, `HYPOTHESIS`, or `UNSUPPORTED`; page-level prescriptions remain downstream. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by explicit evidence-strength labels, competitor recurrence is not treated as causal or prescriptive, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Optional complements: `seo-strategy`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/seo-foundation/` |
| Required skills | None |
| Optional skills | `seo-strategy`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->
