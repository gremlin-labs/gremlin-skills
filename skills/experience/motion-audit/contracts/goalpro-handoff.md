<!-- GENERATED CONTRACT SNAPSHOT
contract: goalpro-handoff
source: contracts/goalpro-handoff.md
source-version: 1
semantic-owner: goalpro
source-sha256: 998cde01cbadf582ca2055774e663d66dbe852ead8e33a31b603f855bdb00843
DO NOT EDIT: run python3 scripts/materialize_contracts.py --write
-->

<!-- contract-metadata
id: goalpro-handoff
version: 1
semantic-owner: goalpro
-->

# Goalpro — Direct Handoff Contract

Use this contract whenever another skill hands implementation directly to Goalpro. The handoff must preserve enough approved context that Goalpro can create criteria without repeating the upstream investigation.

## Contents

- [Required sections](#required-sections)
- [Readiness states](#readiness-states)
- [Approval provenance](#approval-provenance)
- [Goalpro consumption](#goalpro-consumption)
- [Template](#template)
- [Examples](#examples)

## Required sections

A direct `GOALPRO-INPUT.md` includes:

1. **Goal and product outcome** — what will be true for users, operators, or the system.
2. **Slug** — the same kebab-case slug used by the upstream artifact.
3. **Source artifacts and evidence** — repository-relative paths to plans, audits, research, specs, and decisions.
4. **Approval provenance** — what the user approved, when, and whether the handoff changed afterward.
5. **Implementation slices** — ordered, reversible tracer bullets with dependencies.
6. **Acceptance criteria** — independently verifiable “Done when …” items.
7. **Non-goals and boundaries** — source, data, external-state, and authority limits.
8. **Quality applicability** — dimensions from [the execution-quality contract](execution-quality.md), expected evidence, and known waivers.
9. **Project gates** — exact commands and expected success results discovered upstream.
10. **Delivery requirements** — applicable migration, compatibility, rollout, rollback, and observability.
11. **Manual and external actions** — separate operator steps from code changes; state what Goalpro may not do.
12. **Unverified assumptions** — identify the owner and whether each is discoverable or a user decision.
13. **Sensitive-data constraints** — secrets, customer data, production access, and sanitization rules.

Link detailed source artifacts instead of copying them wholesale. The handoff is an execution index, not a second audit or plan.

## Readiness states

Classify before Goalpro mutates anything:

- `READY` — every required section is present; criteria and decisions are approved; remaining unknowns are safely discoverable and cannot materially change scope or risk.
- `NEEDS DELTA CONFIRMATION` — Goalpro discovered or added a material criterion, product decision, destructive operation, external action, data/security constraint, or scope change after upstream approval.
- `BLOCKED` — a required decision or evidence source is missing and cannot be discovered safely.

Formatting gaps alone do not force another user round when the underlying approved source unambiguously supplies the information. Fill and cite the source. Never convert silence into approval.

## Approval provenance

Record:

- Approval status: `APPROVED`, `NOT APPROVED`, or `PARTIAL`.
- Approved artifact and revision or timestamp.
- Approved scope and explicit exclusions.
- Changes made after approval.

Completion of an audit or plan is not automatically approval to implement it. An explicit user request to execute an unchanged approved artifact is approval. If the handoff changes materially afterward, classify it `NEEDS DELTA CONFIRMATION`.

## Goalpro consumption

1. Read `GOALPRO-INPUT.md` and every source artifact it marks required.
2. Validate all required sections and classify readiness.
3. Derive `agent-work/{slug}/goalpro/CRITERIA.md` with source links and approval provenance.
4. If `agent-work/{slug}/goalpro/` exists, inspect its criteria and progress:
   - Resume when it represents the same goal and sources.
   - Reconcile approved source changes into a visible delta.
   - Stop on a conflicting or unrelated goal; never overwrite or silently suffix.
5. For `READY`, begin without re-asking the user to approve unchanged criteria.
6. For `NEEDS DELTA CONFIRMATION`, show only the material delta and ask one focused question.
7. For `BLOCKED`, state the missing decision or evidence and stop before mutation.
8. For a raw goal or unapproved plan, use Goalpro's full criteria-confirmation gate.

## Template

```md
# Goalpro input

## Goal and product outcome

## Slug

## Source artifacts and evidence

## Approval provenance

- Status: APPROVED | NOT APPROVED | PARTIAL
- Approved artifact:
- Approved scope:
- Changes after approval:

## Implementation slices

## Acceptance criteria

- [ ] Done when ...

## Non-goals and boundaries

## Quality applicability

## Project gates

| Gate | Command | Expected result |
|---|---|---|

## Delivery requirements

## Manual and external actions

## Unverified assumptions

## Sensitive-data constraints

## Readiness

- State: READY | NEEDS DELTA CONFIRMATION | BLOCKED
- Rationale:
```

## Examples

### Complete

An approved audit links its evidence, orders two implementation slices, defines database and integration gates, marks production configuration as a manual action, records no post-approval change, and has only a discoverable package-manager assumption. Classify `READY`; Goalpro creates criteria and begins without repeating approval.

### Incomplete

A proposal says “migrate customer data” but does not define compatibility, rollback, ownership, or whether production mutation is authorized. Classify `BLOCKED`. If Goalpro discovers a safe migration design but it adds destructive behavior not previously approved, reclassify `NEEDS DELTA CONFIRMATION` and present only that decision.
