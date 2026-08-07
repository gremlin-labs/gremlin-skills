# Audit Plan

Audit one or more reference projects and create a proposal for a new project implementation — rewrites, ports, or combinations of features from multiple projects into one new codebase.

## When to reach for it

Use when the user says "rewrite X in Y", "port this to a new stack", "combine features from A, B, C into one project", "rebuild this in a faster language", or wants an audit-driven proposal for new-project greenfield or target-repo work.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `audit-compare`; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/audit-plan/`. Required contract artifacts currently include `PROPOSAL.md`, `SYNTHESIS.md`, `ARCHITECTURE.md`, `PLANPRO-INPUT.md`, `REFERENCE-IDS.md`, `refs/{ref-slug}-AUDIT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`audit-compare`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `audit-compare`.
- Optional complements: `goalpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `engineering` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/audit-plan/` |
| Required skills | `audit-compare` |
| Optional skills | `goalpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

