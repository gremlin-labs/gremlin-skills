# Brainstormpro

Audit a codebase through the lens of a user's outcome, propose distinct evidence-grounded ideas with trade-offs and validation experiments, let the user choose, and hand the approved proposal to Planpro or Goalpro.

## When to reach for it

Use when the user knows what should improve but does not know the solution — "brainstorm how to consolidate redundant screens", "propose ways to make sync more efficient", or "we need to reduce API costs but don't know how".

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `planpro`; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/brainstormpro/`. Required contract artifacts currently include `AUDIT.md`, `IDEAS.md`, `PROPOSAL.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`planpro`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `planpro`.
- Optional complements: `goalpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `engineering` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/brainstormpro/` |
| Required skills | `planpro` |
| Optional skills | `goalpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

