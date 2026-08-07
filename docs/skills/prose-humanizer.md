# Prose Humanizer

Rewrites user-facing prose to sound natural, specific, and human while preserving facts, meaning, voice, markup, and code behavior.

## When to reach for it

Use when a user asks to humanize, de-AI, polish, or rewrite pasted text, documentation, web copy, HTML, Markdown/MDX, JSX/TSX, templates, or other user-visible strings; do not use for code semantics, data, legal truth validation, translation, or conversion-strategy design.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are `seo-strategy`; optional skills are not assumed to be installed.

## Authority and safety

It may edit the in-scope project when the user’s request authorizes execution. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/prose-humanizer/`. Required contract artifacts currently include `SCOPE.md`, `PROGRESS.md`, `REWRITE-REPORT.md`, `QUALITY-REPORT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

It can, when the user’s request authorizes the execution scope. It must still preserve unrelated work and obey any narrower approval boundary.

### Can it be installed alone?

Its standalone package must include the declared dependency closure (`seo-strategy`). Running those skills first is required only when the workflow or handoff says so.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Required package relationships: `seo-strategy`.
- Optional complements: `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `experience` (promoted) |
| Invocation | `model-visible` |
| Authority | `executor`; source mutation `task-scoped`; external actions `none` |
| Output root | `agent-work/{slug}/prose-humanizer/` |
| Required skills | `seo-strategy` |
| Optional skills | `theme-library` |
| Evaluation families | `trigger`, `artifact`, `quality` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

