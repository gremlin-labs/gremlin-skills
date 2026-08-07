# Testpro

Audits an existing test suite and, only when improvement is explicitly requested or approved, builds missing test infrastructure and closes gaps through a Plan→Do→Verify loop.

## When to reach for it

Use when the user says "improve test coverage", "audit our tests", "find untested code", "backfill tests for X", "our coverage is too low", or wants to harden existing behavior rather than write new-feature tests (use tdd for that).

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It begins without project-source mutation. Source mutation is allowed only after the skill’s explicit approval or execution gate. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/testpro/`. Required contract artifacts currently include `AUDIT.md`, `GAPS.md`, `EXECUTION-PLAN.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

Only after its explicit approval or execution boundary has been crossed. Preview, audit, or preparation work does not silently authorize mutation.

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
| Authority | `hybrid`; source mutation `after-approval`; external actions `none` |
| Output root | `agent-work/{slug}/testpro/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

