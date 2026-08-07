# Releasepro

Prepare a release by classifying changes, selecting a repository-compatible version, verifying the exact release state, updating release artifacts, committing, tagging, and optionally pushing exact refs.

## When to reach for it

Use when the user says "cut a release", "release v1.X", "bump and tag", "ship a new version", "prepare a release", or wants to package completed work without publishing to a registry.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It executes only after its explicit approval gate and may then edit the in-scope project. External actions retain a separate exact-action approval. It must stop for the separately approved external action even when local preparation is complete. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/release-v{version-slug}/releasepro/`. Required contract artifacts currently include `RELEASE.md`. Conditional files are emitted only when their documented condition applies.

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
| Authority | `executor`; source mutation `after-approval`; external actions `approval-required` |
| Output root | `agent-work/release-v{version-slug}/releasepro/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

