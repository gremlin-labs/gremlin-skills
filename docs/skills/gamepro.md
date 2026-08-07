# Gamepro

Builds or resumes a game through visible playable milestones, from First Playable to MVP, V1, and an optional Release Candidate, using a persistent Plan→Do→Verify loop.

## When to reach for it

Use when a user asks to build, finish, continue, or drive a game to a playable milestone; do not use for idea-only brainstorming, plan-only work, art direction alone, a bounded bug fix, or release-only operations.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may edit the in-scope project when the user’s request authorizes execution. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/gamepro/`. Required contract artifacts currently include `GAME.md`, `PROGRESS.md`, `QUALITY-REPORT.md`. Conditional files are emitted only when their documented condition applies.

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
| Category | `experience` (promoted) |
| Invocation | `user-only` |
| Authority | `executor`; source mutation `task-scoped`; external actions `none` |
| Output root | `agent-work/{slug}/gamepro/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

