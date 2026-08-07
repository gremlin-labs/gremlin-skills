# Email Lifecycle Audit

Audits an implemented post-signup lifecycle email system against product outcomes, campaign logic, data integrity, consent, deliverability, accessibility, copy, operations, and incremental measurement, then produces a prioritized report and canonical input for Email Lifecycle Strategy.

## When to reach for it

Use when users ask to audit, assess, diagnose, benchmark, optimize, improve, or plan a refactor of existing onboarding, activation, adoption, trial, retention, re-engagement, or win-back email programs; do not use for greenfield strategy, direct implementation, deliverability-only incidents, newsletters, or copy-only rewrites.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `email-lifecycle-strategy`; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/email-lifecycle-audit/`. Required contract artifacts currently include `RESEARCH.md`, `CURRENT-SYSTEM.md`, `CAMPAIGN-INVENTORY.md`, `AUDIT-REPORT.md`, `STRATEGY-INPUT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`email-lifecycle-strategy`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `email-lifecycle-strategy`.
- Optional complements: `goalpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/email-lifecycle-audit/` |
| Required skills | `email-lifecycle-strategy` |
| Optional skills | `goalpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | `python3 skills/growth/email-lifecycle-audit/scripts/test_tools.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

