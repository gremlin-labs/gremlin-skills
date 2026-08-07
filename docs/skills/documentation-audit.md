# Documentation Audit

Deeply audits project documentation, verifies it against implementation and history, classifies drift and implementation state, and produces a Goalpro-ready cleanup and restructuring plan.

## When to reach for it

Use when documentation may be stale, plans and tickets need completion classification, docs need consolidation or archiving, a monorepo needs parent-versus-child publication boundaries, or a project needs standardized documentation governance.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/documentation-audit/`. Required contract artifacts currently include `RESEARCH.md`, `INVENTORY.json`, `DOCUMENTATION-CATALOG.md`, `DRIFT-REPORT.md`, `INFORMATION-ARCHITECTURE.md`, `GOVERNANCE.md`, `PLAN.md`, `GOALPRO-INPUT.md`. Conditional files are emitted only when their documented condition applies.

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
| Output root | `agent-work/{slug}/documentation-audit/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `handoff`, `product` |
| Skill-local tests | `python3 skills/engineering/documentation-audit/scripts/test_tools.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

