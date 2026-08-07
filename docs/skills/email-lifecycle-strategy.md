# Email Lifecycle Strategy

Defines and documents an evidence-backed post-signup lifecycle email strategy that advances activation, repeated value, adoption, retention, and respectful re-engagement while protecting consent, deliverability, accessibility, and inbox trust before implementation.

## When to reach for it

Use when users ask to create, design, map, compare, improve, replace, or approve onboarding, activation, adoption, trial, retention, re-engagement, win-back, or sunset email programs, including turning an Email Lifecycle Audit into a refactored strategy; do not use for audit-only work, direct implementation or sending, deliverability incidents, newsletters, or one-off copy rewrites.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `prose-humanizer`; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/email-lifecycle-strategy/`. Required contract artifacts currently include `RESEARCH.md`, `STRATEGY-OPTIONS.md`, `MESSAGE-SAMPLES.md`, `EMAIL-LIFECYCLE-PREVIEW.html`, `previews/EMAIL-LIFECYCLE-PREVIEW-R{n}.html`, `LIFECYCLE-STRATEGY.md`, `CAMPAIGN-MAP.md`, `STATE-AND-DECISION-MODEL.md`, `MESSAGE-BRIEFS.md`, `COPY-DECK.md`, `DELIVERABILITY-AND-CONSENT-GUARDRAILS.md`, `MEASUREMENT-PLAN.md`. Conditional files are emitted only when their documented condition applies.

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
| Category | `growth` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/email-lifecycle-strategy/` |
| Required skills | `prose-humanizer` |
| Optional skills | `goalpro`, `planpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `handoff`, `product` |
| Skill-local tests | `python3 skills/growth/email-lifecycle-strategy/scripts/test_tools.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

