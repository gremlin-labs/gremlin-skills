# Planpro

Take a simple feature request, do a deep dive on the existing codebase, and write a detailed phased plan with project-specific implementation notes.

## When to reach for it

Use when the user says "plan this", "write a plan for X", "how should I build X in this repo", "scope this feature", "I want to do X but need a plan first", or asks for a phased/broken-down implementation plan grounded in the actual codebase rather than from scratch.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/planpro/`. Required contract artifacts currently include `PLAN.md`, `RESEARCH.md`, `GOALPRO-INPUT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

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
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/planpro/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `handoff`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

