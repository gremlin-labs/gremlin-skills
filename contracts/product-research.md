<!-- contract-metadata
id: product-research
version: 1
semantic-owner: planpro
-->

# Planpro — Product Research Lens

Use this lens before recommending or planning changes. Connect technical work to real user, operator, and business outcomes without inventing evidence or forcing product ceremony onto irrelevant work.

## Contents

- [Classify the dimensions](#classify-the-dimensions)
- [Intent sources](#intent-sources)
- [User and problem](#user-and-problem)
- [Current journey](#current-journey)
- [Desired outcome](#desired-outcome)
- [Quality attributes](#quality-attributes)
- [Delivery](#delivery)
- [Alternatives](#alternatives)
- [Unknowns and questions](#unknowns-and-questions)
- [Current external guidance](#current-external-guidance)
- [Research output](#research-output)

## Classify the dimensions

Record each section as:

- `RELEVANT` — investigate it and cite evidence.
- `NOT APPLICABLE` — give a short concrete reason.
- `UNKNOWN` — state what evidence or decision is missing and who can resolve it.

Do not silently skip a dimension. Keep classifications proportional: a one-line internal refactor needs far less product research than a new onboarding flow or billing migration.

## Intent sources

Read what exists before inferring intent:

- README, contributor and agent instructions.
- `CONTEXT.md`, `PRODUCT.md`, PRDs, specifications, roadmap, and design-system guidance.
- ADRs and decision records, especially rejected alternatives.
- Relevant issues, support notes, analytics definitions, and recent git history.
- Existing user-facing copy, workflows, tests, and operational runbooks.

Treat these as evidence, not infallible instructions. Record contradictions and prefer explicit current decisions over guesses.

## User and problem

Identify:

- Primary user or operator and any materially affected secondary actor.
- Job-to-be-done and current pain or risk.
- Why the change matters now.
- Existing workaround and its cost.
- Who could be harmed or excluded by the change.

If the request is internal infrastructure, the “user” may be a developer, operator, support agent, or downstream system.

## Current journey

Trace the current path from entry to outcome:

- Entry point and prerequisites.
- Happy path.
- Loading, empty, validation, permission, error, degraded, cancellation, retry, and recovery states.
- Cross-device, responsive, keyboard, assistive-technology, or offline behavior when relevant.
- Support and operator path when automation fails.

Cite code, tests, screenshots, documentation, or runtime inspection. Do not design the desired journey until the current one is understood.

## Desired outcome

Define:

- Observable user or operator result.
- Success signal that would show improvement.
- Guardrail that must not regress.
- Failure signal that would invalidate the approach.
- Time horizon and population when evidence supports them.

Do not invent numeric targets. When no metric exists, define an observable qualitative or testable signal and mark quantitative targets `UNKNOWN`.

## Quality attributes

Classify the attributes that shape the design:

- Accessibility and inclusive interaction.
- Security, privacy, authorization, and abuse resistance.
- Correctness, reliability, availability, and recovery.
- Latency, throughput, scale, memory, cost, and resource limits.
- Data integrity, retention, auditability, and compliance.
- Compatibility, extensibility, localization, and maintainability.

Carry applicable attributes into acceptance criteria and [the execution-quality contract](execution-quality.md).

## Delivery

Investigate:

- Data migration, backfill, and mixed-version behavior.
- API, schema, and client compatibility.
- Feature flags, canary, shadow, dual-run, or staged rollout.
- Observability, alerting, support, and manual recovery.
- Rollback boundary and irreversible operations.
- Documentation, training, and external coordination.

Separate code changes from manual and external actions in the handoff.

## Alternatives

Include credible alternatives, including “do nothing” when useful. For each, state:

- Mechanism and evidence.
- User/product benefit.
- Cost, complexity, and operational burden.
- Risks and reversibility.
- Why it was selected, rejected, or deferred.

Do not recommend a reference pattern merely because it is sophisticated. Adoption fit and outcome matter more than novelty.

## Unknowns and questions

Classify each unknown:

- `DISCOVERABLE` — resolve from code, configuration, primary documentation, or runtime evidence.
- `ASSUMPTION` — proceed only when low-risk; record rationale and verification.
- `USER DECISION` — material product, risk, data, scope, or external-state choice; ask one focused question.
- `VALIDATION EXPERIMENT` — cheapest test that would reduce meaningful uncertainty.

Resolve discoverable facts before asking. Never turn missing evidence into confident product prose.

## Current external guidance

Browse current primary documentation when the plan depends on an external API, framework, regulation, security recommendation, product capability, or version-sensitive behavior. Record the source, access date, applicable version, and any inference. Prefer official documentation and specifications over secondary summaries.

## Research output

Add a compact matrix to the research artifact:

```md
## Product context

| Dimension | Status | Evidence, outcome, or unknown |
|---|---|---|
| User and problem | RELEVANT | Operators cannot recover failed imports without support |
| User journey | RELEVANT | `app/import/page.tsx` and journey test |
| Accessibility | NOT APPLICABLE | No user interface or user-facing output changes |
| Success signal | UNKNOWN | Product owner must choose acceptable recovery time |

## Alternatives

## Delivery constraints

## Decisions and validation experiments
```

The matrix is an index. Put detailed evidence in the surrounding research, not in oversized table cells.
