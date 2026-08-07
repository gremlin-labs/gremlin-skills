# Migratepro

Rewrite an existing codebase in a new stack one module at a time, keeping the app shippable throughout.

## When to reach for it

Use when the user says "rewrite X in Y", "port this to TypeScript/Rust/Go", "migrate this codebase to a new stack", "incrementally rewrite this app", or wants an in-place stack migration where the app stays working between steps. Differs from audit-plan (greenfield proposals) by migrating in place.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may edit the in-scope project when the user’s request authorizes execution. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/migratepro/`. Required contract artifacts currently include `MAP.md`, `CRITERIA.md`, `PLAN.md`, `PROGRESS.md`, `QUALITY-REPORT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

It can, when the user’s request authorizes the execution scope. It must still preserve unrelated work and obey any narrower approval boundary.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Optional complements: `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `engineering` (promoted) |
| Invocation | `user-only` |
| Authority | `executor`; source mutation `task-scoped`; external actions `none` |
| Output root | `agent-work/{slug}/migratepro/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

