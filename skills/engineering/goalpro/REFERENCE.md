# Goalpro — Verification Toolbox

Pick gates that apply. Detect from manifest files (`package.json`, `tsconfig.json`, `Cargo.toml`, `go.mod`, etc.). Every iteration must end with all *applicable* gates green **and** an explicit self-judgment of satisfaction before logging `DONE`.

Use [QUALITY.md](contracts/execution-quality.md) for cross-cutting product, correctness, security, data, accessibility, performance, reliability, rollout, and maintainability review. This file remains the toolchain and mechanical-verification toolbox.

## Desk sanity check (always)

Before any tool, logically verify:
- Re-read the diff. Does it actually achieve the step's stated intent?
- Did you touch anything the step didn't ask for? Revert unrelated hunks.
- Does every user-facing or authority-sensitive hunk map to an approved criterion and conditional change-control ID? Stop on an unmatched delta.
- Does the change interact with neighbors? Mental-trace one representative call site.
- Is there a test for the new behavior?
- Does the test prove approved behavior, or merely enforce a decision you just invented? Label the latter conformance-only and obtain independent evidence.

## Self-judgment (always)

State aloud (in PROGRESS.md or your reasoning): "I am satisfied that this step is completed because …". Be specific — cite what behavior works, what criteria it satisfies. "Looks good" is not judgment.

## TypeScript / JS

- `npx tsc --noEmit` (or `npm run typecheck`)
- Lint: `npm run lint` — detect `oxlint`, `fallow`, `eslint`, `biome`
- Build: `npm run build`
- Tests: `npm test` (detect: `vitest`, `jest`, `bun test`). Write a test for the new behavior first.

## Compiled languages

- **Rust**: `cargo build`, `cargo clippy -- -D warnings`, `cargo test`, run the binary on a sample input
- **Go**: `go build ./...`, `go vet ./...`, `go test ./...`, run the resulting binary
- **C/C++**: compile with `-Wall -Wextra`, run the binary, run tests
- **Elixir**: `mix compile --warnings-as-errors`, `mix test`
- **Python**: `ruff`, `mypy`/`pyright` if configured, `pytest`

## No configured gate

Run: tests (write one if none exist), build/compile if applicable, and the desk sanity check. State in PROGRESS.md what gate was run.

## Failing gates

- Read the actual output. Fix the root cause.
- Re-run the specific failing gate, not the whole suite, while iterating.
- **Three-attempts rule**: same gate failing 3 substantive fixes in a row → write hypothesis to PROGRESS.md, classify blocker-vs-local, then either BLOCK+ask or skip-to-next per SKILL.md.
- "I re-ran and it passed" is not verification — quote the relevant output line.

## Cross-cutting changes

When a step touches public interfaces, also:
- Grep for callers; skim each for breakage.
- Update docstrings/README where behavior changed.
- Add/adjust a regression test for the most-used caller.

## Final gate

At the final worktree state, rerun every configured project gate and the representative end-to-end scenario recorded in `QUALITY-REPORT.md`. Compare the final diff with exact approved criteria and conditional change-control artifacts. A collection of earlier per-step green outputs is not proof that the integrated result remains green or that the underlying product/editorial decision was valid.
