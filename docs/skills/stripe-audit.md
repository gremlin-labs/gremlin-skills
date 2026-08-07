# Stripe Audit

Audits Stripe Billing and subscription implementations in Next.js applications and produces a goalpro-ready remediation package.

## When to reach for it

Use when the user asks to audit, investigate, optimize, or refactor Stripe; fix subscription synchronization or renewal credits; review Stripe products and pricing; or identify billing security, reliability, and abuse risks.

## Prerequisites

Start with the project, evidence, approval state, and same-slug artifacts named by the request. Required package relationships are none; optional skills are not assumed to be installed.

## Authority and safety

It may inspect project and external evidence and write only its skill-scoped work artifacts. It does not edit project source or mutate external systems. The canonical skill instructions remain authoritative when a request has narrower limits.

## Outputs

Work is owned at `agent-work/{slug}/stripe-audit/`. Required contract artifacts currently include `AUDIT.md`, `INVARIANTS.md`, `EVENT-MATRIX.md`, `TEST-SCENARIOS.md`, `GOALPRO-INPUT.md`. Conditional files are emitted only when their documented condition applies.

## Common questions

### Does it change my project?

No. It may write its reviewable `agent-work` artifacts, but project-source mutation is outside this skill’s authority.

### Can it be installed alone?

Yes. Its archive has no required sibling-skill dependency; optional integrations are discovered rather than assumed.

## Visible success

The required artifacts exist at the declared output root, claims are backed by the evidence level the skill requires, applicable verification gates pass, and the skill stops at its documented authority boundary. Structural validation alone is not treated as proof of product judgment.

## Adjacent Gremlin skills

- Optional complements: `goalpro`, `theme-library`.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `growth` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/stripe-audit/` |
| Required skills | None |
| Optional skills | `goalpro`, `theme-library` |
| Evaluation families | `trigger`, `artifact`, `handoff`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->

