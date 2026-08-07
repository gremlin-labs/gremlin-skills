# Onboarding Direction

Defines and documents an evidence-backed onboarding direction for web, native mobile, or cross-platform products, optimizing activation, time-to-value, user success, trust, and progressive mastery before implementation.

## When to reach for it

Use when users ask to design or redesign onboarding, explore first-run or activation flows, compare onboarding concepts, turn an Onboarding Audit into an improved direction, or approve a realistic onboarding prototype before Planpro or Goalpro implementation; do not use for source implementation, audit-only work, general visual art direction, or copy-only rewriting.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `prose-humanizer`; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/onboarding-direction/`. Required contract artifacts currently include `RESEARCH.md`, `DIRECTION-OPTIONS.md`, `ONBOARDING-PREVIEW.html`, `previews/ONBOARDING-PREVIEW-R{n}.html`, `ONBOARDING-BLUEPRINT.md`, `EXPERIENCE-MATRIX.md`, `COPY-DECK.md`, `MEASUREMENT-PLAN.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`prose-humanizer`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `prose-humanizer`.
- Optional complements: `goalpro`, `planpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `experience` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/onboarding-direction/` |
| Required skills | `prose-humanizer` |
| Optional skills | `goalpro`, `planpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `handoff`, `product` |
| Skill-local tests | `python3 skills/experience/onboarding-direction/scripts/test_tools.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

