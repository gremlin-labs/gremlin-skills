# Compact History

Audits, verifies, summarizes, and archives accumulated agent-work history while preserving unfinished initiatives and extracting actionable follow-up work.

## When to reach for it

Use when an agent-work folder has become difficult to navigate, completed initiatives need archival, implementation history needs project-specific changelogs, unfinished plans need status reporting, or deferred and out-of-scope work needs consolidation into future planning prompts.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It executes within its artifact or external-operation boundary without editing project source. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/• compact-history/`. Required contract artifacts currently include `changelog/{project-key}.md`, `in-progress/{project-key}.md`, `todo/{project-key}.md`, `runs/{run-id}/INVENTORY.json`, `runs/{run-id}/PREVIEW.md`, `runs/{run-id}/MANIFEST.json`, `runs/{run-id}/ROLLBACK.json`. Conditional files are emitted only when their documented condition applies.

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
| Invocation | `user-only` |
| Authority | `executor`; source mutation `never`; external actions `none` |
| Output root | `agent-work/• compact-history/` |
| Required skills | None |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality` |
| Skill-local tests | `python3 skills/engineering/compact-history/scripts/test_tools.py` |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

