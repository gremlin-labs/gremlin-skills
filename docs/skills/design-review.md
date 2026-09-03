# Design Review

Reviews a bounded UI or motion change—such as a diff, pull request, route, component, or completed implementation slice—against approved design intent, semantic tokens, component recipes, accessibility, responsive behavior, and perceptual motion quality, then returns an evidence-backed verdict.

## When to reach for it

- Review a bounded UI or motion change against approved intent and return an approve or block verdict.
- Check cognitive load, first-timer task completion, or copy against an approved direction contract.
- Validate a completed Designpro or Motion Audit slice before release.
- Do not use for whole-app audits, new visual direction, or implementing fixes.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/design-review/`. Required contract artifacts currently include `DESIGN-REVIEW.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- `designpro` owns whole-app generic-feel and token/craft audits.
- `prose-humanizer` owns rewriting the copy that review only critiques.
- Optional complements: `goalpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `experience` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/design-review/` |
| Required skills | None |
| Optional skills | `goalpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

