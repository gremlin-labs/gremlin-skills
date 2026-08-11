# SEO Monitor

Runs a read-only SEO learning loop by collecting compatible GA4, Google Search Console, Bing, crawl/index, content-receipt, and page-ownership evidence; comparing approved baselines and mature windows; protecting winners; and routing measured exceptions without reactive rewrites.

## When to reach for it

Use when a user asks to monitor SEO performance, review rankings or organic outcomes, detect crawl/index regressions or content decay, evaluate a launched SEO change, produce recurring SEO reports, or recommend no change, investigation, refresh, consolidation, technical repair, or new strategy.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. It evaluates technical and editorial release layers separately, so a sound canonical or crawl fix cannot self-certify an accompanying copy rewrite. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/seo-monitor/`. Required contract artifacts currently include `MONITOR-BRIEF.md`, `SEO-MONITOR.md`, `MONITOR-HISTORY.md`, `ACTION-QUEUE.md`, `runs/{run-id}/DATA-INVENTORY.md`, `runs/{run-id}/SNAPSHOT.csv`, `runs/{run-id}/MONITOR-REPORT.md`. Evaluated releases are reconciled to approved editorial change IDs or technical classes and their independent rollback boundaries. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, release layers and expected mechanisms are reconciled, terms and persuasion cues gained or lost are visible, technical and editorial rollback remain separable, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Optional complements: `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/seo-monitor/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->
