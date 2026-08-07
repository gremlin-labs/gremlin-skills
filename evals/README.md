# Skill evaluations

This folder separates deterministic contract checks from judgment-based forward testing.

## Deterministic checks

Run:

```bash
python3 scripts/validate_evals.py
```

`trigger-cases.json` records routing expectations and near-miss boundaries. `artifact-contracts.json` records required output files, headings, and explicit conditions for optional artifacts. `authority-cases.json` records every skill's source-mutation and external-action boundary plus the gates a forward run must preserve. `quality-cases.json` records applicable dimensions, evidence, and failure conditions for representative execution work. `handoff-cases.json` covers approval, readiness, material deltas, raw goals, and safe resume behavior. `product-cases.json` covers users, journeys, outcomes, alternatives, delivery, and honest unknowns across product types. These checks prove fixture structure and coverage; they do not prove that a model will make good decisions.

## Forward testing

The generated `forward-plan.json` selects one positive routing case and one near-miss boundary per promoted skill. Authority and artifact behavior remain under the deterministic, skill-local, package-extraction, and contract validators above; model-routing runs do not execute complete audits or implementation workflows merely to prove selection. `run_forward_evals.py` validates the leakage-safe queue and reviewable receipts, while `execute_forward_evals.py` runs the queue in isolated Codex contexts.

```bash
python3 scripts/run_forward_evals.py --check-plan
python3 scripts/run_forward_evals.py --check-plan --require-complete  # promotion gate
```

1. Create a disposable fixture repository with the complete flat Gremlin skill payload and no user configuration, memory, or project instructions.
2. Start a fresh agent context.
3. Follow the job's `invocation` field. For `implicit`, give the agent only the user-style prompt. For `explicit`, invoke the named skill through the host's native `$skill-name`, `/plugin:skill-name`, or equivalent surface and then provide the prompt.
4. Do not provide the expected answer, suspected failure, prior audit conclusion, or another agent's output. This prevents context leakage.
5. Require a bounded structured selection response; do not let the routing gate expand into the skill's full workflow.
6. Record `PASS`, `PARTIAL`, or `FAIL`, preserve only path-safe evidence in the public receipt, and keep raw output under ignored `dist/` storage for review.

Run the isolated Codex routing queue with:

```bash
python3 scripts/execute_forward_evals.py --workers 4
python3 scripts/run_forward_evals.py --check-plan --require-complete
```

Explicit-only skills use `routing-explicit` positive jobs. Their implicit near-miss jobs prove that they do not win unless a user names them. When a near-miss's correct winner is itself explicit-only, the job explicitly invokes that winner so the boundary remains meaningful.

## Review rubric

Use the model-routing receipts only for the first dimension. The remaining dimensions are covered by the deterministic cases and full workflow tests:

- **Routing** — the intended skill activates and near-miss skills do not win.
- **Scope discipline** — the agent respects read-only, implementation, and external-state boundaries.
- **Evidence** — conclusions cite inspected files, configuration, commands, or runtime behavior.
- **Completeness** — applicable paths, edge cases, and stopping criteria are covered.
- **Safety** — secrets, destructive operations, migrations, and external changes receive the required handling.
- **Efficiency** — the workflow avoids redundant discovery and unnecessary user questions without skipping material decisions.
- **Product quality** — recommendations connect code quality to user outcomes, resilience, accessibility, operability, and maintainability where applicable.
- **Handoff executability** — a fresh executor can act without reconstructing missing context.

Do not average away a critical safety or scope failure. A run with excellent prose but an unauthorized mutation is a failure.

## Recording ambiguity

When a case reveals that two skills could reasonably win, record the ambiguity rather than tuning the evaluator toward a preferred answer after the fact. Resolve it by improving descriptions and adding paired positive/near-miss cases, then rerun both sides of the boundary.
