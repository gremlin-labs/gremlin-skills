<!-- GENERATED CONTRACT SNAPSHOT
contract: quality
source: contracts/execution-quality.md
source-version: 2
semantic-owner: goalpro
source-sha256: 3c6669de4614ec91d9ce91e374f441984a68cb487a51ab7005becf0877bb25c3
DO NOT EDIT: run python3 scripts/materialize_contracts.py --write
-->

<!-- contract-metadata
id: execution-quality
version: 2
semantic-owner: goalpro
-->

# Goalpro — Execution Quality Contract

Apply this contract proportionally to every execution skill. It sharpens judgment; it is not permission to add ceremony that does not help prove the goal.

## Contents

- [Classify applicability](#classify-applicability)
- [Per-step review](#per-step-review)
- [Final integrated review](#final-integrated-review)
- [Decision validity and validation independence](#decision-validity-and-validation-independence)
- [Evidence statuses](#evidence-statuses)
- [Quality report](#quality-report)
- [Specialized defaults](#specialized-defaults)

## Classify applicability

Before implementation, classify each quality dimension for the goal:

- `APPLICABLE` — the work can materially affect this dimension; define evidence.
- `NOT APPLICABLE` — it cannot materially affect this dimension; record a short reason.
- `UNKNOWN` — inspect before mutation or ask when the answer is a product decision.

Reclassify when the work reveals a new risk. Never silently omit a dimension. A one-line classification is enough for a trivial change.

## Per-step review

Review applicable dimensions before logging a step `DONE`:

### Product intent

- State which acceptance criterion and user or operator outcome the step advances.
- Verify the implementation matches documented product language and decisions.
- Do not optimize a proxy while missing the intended behavior.

### Correctness and resilience

- Cover success, validation, boundary, empty, error, cancellation, retry, and recovery paths that the change can affect.
- Check state transitions, concurrency, idempotency, time, ordering, and partial failure where relevant.
- Prefer invariants and regression tests over examples that only prove the happy path.

### Security, privacy, and abuse

- Recheck authentication, authorization, tenant ownership, input boundaries, secret handling, sensitive data, and dependency exposure.
- Consider economic or resource abuse when the change grants access, money, credits, compute, storage, or external calls.
- Record threat or abuse cases in tests or explicit operational controls.

### Data integrity and compatibility

- Keep multi-write operations atomic where the invariant requires it.
- Define schema/data migration, backfill, mixed-version behavior, rollback, and recovery before irreversible changes.
- Preserve public contracts or document and verify an approved migration path.

### User experience and accessibility

- For user-facing work, verify loading, empty, success, error, degraded, and recovery states.
- Verify keyboard, focus, labels, semantics, contrast, motion, responsive layout, and assistive-technology behavior that the change affects.
- Use the project's design system and interaction conventions.

### Performance and resources

- Identify whether the step touches a hot path, unbounded collection, large payload, cold start, external request, or constrained resource.
- Measure a representative baseline and result when performance is a stated goal or regression risk.
- Avoid claims based only on intuition or microbenchmarks unrelated to production behavior.

### Reliability, observability, and operations

- Define retry, timeout, backpressure, degradation, and recovery behavior for external or asynchronous work.
- Add logs, metrics, traces, health signals, and operator context proportional to the failure cost.
- Verify alerts and runbooks when the change introduces a new operational responsibility.

### Rollout and rollback

- Choose atomic release, feature flag, canary, shadow, dual-run, or staged migration based on risk.
- Define a rollback boundary and evidence that rollback remains safe.
- Remove temporary flags and compatibility paths when their exit criteria are met, or document why they remain.

### Maintainability and documentation

- Match repository naming, module boundaries, error handling, and test style.
- Keep the diff scoped; remove accidental duplication and dead paths introduced by the work.
- Update public, operator, architecture, and contributor documentation affected by the behavior.

### Machine verification

- Run focused regression tests plus the full configured suite, typecheck, lint, build, and executable smoke check that apply.
- Inspect the diff and representative callers after gates pass.
- Treat a narrow green check as evidence only for the behavior it actually covers.

## Decision validity and validation independence

Machine checks can prove implementation behavior, schema conformance, or the absence of a named regression. They cannot establish that a newly invented product, editorial, UX, policy, or SEO decision is desirable.

- Trace every user-facing acceptance criterion to an approved source, observed user/market evidence, protected baseline, or named product policy.
- Label a test authored from the same new decision `CONFORMANCE`; do not cite it as independent validation of that decision.
- Compare representative before/after behavior for user-facing changes, including what information, terminology, action, or persuasive value was lost as well as gained.
- When a diff introduces a material decision outside the approved criteria, stop and expose the delta even if all tests pass.
- Seek independent evidence proportional to risk: owner approval, a separate specialist verdict, a current benchmark, user evidence, canary observation, or production measurement.

Self-judgment is required but is not independent evidence. “I am satisfied” cannot expand authority or turn a proxy metric into the product outcome.

## Final integrated review

Before declaring the goal complete:

1. Exercise a representative end-to-end flow across all completed criteria.
2. Re-run the complete project gate at the final worktree state.
3. Verify the criteria work together, not only in isolated step tests.
4. Inspect for temporary flags, migration debris, debug paths, stale compatibility code, and undocumented manual actions.
5. Verify applicable rollout, rollback, user-visible behavior, and operational signals.
6. Reconcile every quality dimension in `QUALITY-REPORT.md`.
7. Reconcile the final diff against approved scope and label tests by what they actually prove.

Per-step success does not substitute for this integrated gate.

## Evidence statuses

Use one final status per dimension:

- `VERIFIED` — cite the test, command, diff, runtime behavior, document, or operational evidence.
- `NOT APPLICABLE` — give the concrete reason the goal cannot affect it.
- `WAIVED` — cite explicit user approval, the known risk, and the follow-up owner or decision.

`UNKNOWN` is never a completion status. A waiver is a decision, not a convenient substitute for failed verification.

## Quality report

Create `QUALITY-REPORT.md` in the tracking folder:

```md
# Quality report

| Dimension | Status | Evidence or rationale |
|---|---|---|
| Product intent | VERIFIED | `tests/journey.test.ts` proves the approved flow |
| Accessibility | NOT APPLICABLE | No user interface or user-facing output changed |
| Rollback | WAIVED | User approved irreversible backfill in decision D-3 |

## Final integrated verification

- Command or scenario: ...
- Result: ...
- I am satisfied the goal is complete because ...
```

Keep evidence concise and link to detailed logs rather than copying large outputs.

## Specialized defaults

Specialized execution skills add presumptively applicable dimensions:

- **Feature-goal** — product intent, user journey, spec fidelity, errors, target-stack maintainability, and accessibility for user interfaces.
- **Migratepro** — behavior parity, data integrity, compatibility, performance, coexistence, rollout, rollback, and observability.
- **Restructure** — behavior parity, public-interface compatibility, reviewability, and maintainability.
- **Testpro** — critical-path risk, test validity, determinism, suite performance, and maintainability.

“Presumptively applicable” means inspect before marking otherwise; it does not forbid a justified `NOT APPLICABLE` result.
