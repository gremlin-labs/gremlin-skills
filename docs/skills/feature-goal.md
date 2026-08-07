# Feature Goal

Drive implementation of a feature from a Feature Clone stage using a Plan→Do→Verify loop with Jira-style acceptance criteria, looping until every criterion is met.

## When to reach for it

Use when the user says "build this feature", "implement the cloned feature", "port this spec", "execute the feature-clone stage", or wants a documented feature driven to completion in a target project — typically after running feature-clone.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `goalpro`; optional skills are not assumed to be installed.

## Authority and safety

It may edit the in-scope project when the user’s request authorizes execution. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/feature-goal/`. Required contract artifacts currently include `CRITERIA.md`, `PROGRESS.md`, `QUALITY-REPORT.md`, `spec-link.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

It can, when the user’s request authorizes the execution scope. It must still preserve unrelated work and obey any narrower approval boundary.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`goalpro`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `goalpro`.
- Optional complements: `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `engineering` (promoted) |
| Invocation | `user-only` |
| Authority | `executor`; source mutation `task-scoped`; external actions `none` |
| Output root | `agent-work/{slug}/feature-goal/` |
| Required skills | `goalpro` |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

