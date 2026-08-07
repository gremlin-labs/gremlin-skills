# Onboarding Audit

Audits an existing web or mobile onboarding experience against product evidence, activation goals, platform-specific UX, accessibility, trust, copy, measurement, and user-success principles, then produces a prioritized report and canonical input for Onboarding Direction.

## When to reach for it

Use when users ask to audit, assess, diagnose, benchmark, or improve an implemented signup, first-run, activation, permission, empty-state, or early-lifecycle onboarding flow; do not use for greenfield onboarding design, source implementation, general design-system audits, or copy-only rewrites.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `onboarding-direction`; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/onboarding-audit/`. Required contract artifacts currently include `RESEARCH.md`, `CURRENT-JOURNEY.md`, `AUDIT-REPORT.md`, `DIRECTION-INPUT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`onboarding-direction`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `onboarding-direction`.
- Optional complements: `goalpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `experience` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/onboarding-audit/` |
| Required skills | `onboarding-direction` |
| Optional skills | `goalpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | `python3 skills/experience/onboarding-audit/scripts/test_tools.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

