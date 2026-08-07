# Motion Audit

Audits an existing application's motion and interaction system for purpose, frequency, response, spatial continuity, interruption, gesture physics, performance, accessibility, cohesion, tokens, missed opportunities, and TurbulenceJS migration, then produces an evidence-backed remediation handoff.

## When to reach for it

Use when the user asks to audit or improve implemented animations across a codebase, diagnose jank or inconsistency, establish motion tokens and enforcement, find performance or reduced-motion defects, identify purposeful missing motion, or plan systemic adoption of TurbulenceJS; do not use to art-direct a future motion language, review one bounded diff, or directly implement motion.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/motion-audit/`. Required contract artifacts currently include `RESEARCH.md`, `MOTION-AUDIT.md`, `MOTION-INVENTORY.md`, `INTERACTION-MATRIX.md`, `PERFORMANCE-MATRIX.md`, `ACCESSIBILITY-MATRIX.md`, `MOTION-SYSTEM-SPEC.md`, `ENFORCEMENT-STRATEGY.md`, `PLAN.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Optional complements: `goalpro`, `motion-direction`, `planpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `experience` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/motion-audit/` |
| Required skills | None |
| Optional skills | `goalpro`, `motion-direction`, `planpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `handoff`, `product` |
| Skill-local tests | `python3 skills/experience/motion-audit/scripts/test_tools.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

