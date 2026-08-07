# Migratepro — Verification Toolbox & Migration Gotchas

Inherit the cross-cutting execution review from [Goalpro's quality contract](contracts/execution-quality.md). This reference adds migration mechanics and target-stack gates.

## Desk sanity check (every module)

Before running any tool, verify:
- Re-read the diff. Does the new impl reproduce the old module's behavior?
- Are all callers of the old module migrated? Grep for old-module imports/references.
- Did you touch anything outside this module's boundary? Revert unrelated hunks.
- Is there a test for the new impl that covers the old module's behavior?
- Is the app still shippable — builds, runs, smoke works?

## Self-judgment (every module)

State aloud: "I am satisfied this module is migrated because …". Cite what behavior is reproduced, what callers are migrated, whether old code is deleted (per criteria), and any perf delta measured.

## Verification by target stack

Detect source and target stacks from manifests. Run gates for the TARGET stack (the new code is what's being verified):

### TypeScript / JS target
- `npx tsc --noEmit` (or `npm run typecheck`)
- Lint: `npm run lint` (oxlint, fallow, eslint, biome)
- Build: `npm run build`
- Tests: `npm test` (vitest, jest, bun test). Port old tests to new stack.

### Rust target
- `cargo build`
- `cargo clippy -- -D warnings`
- `cargo test`
- Run the binary on a sample input. Port old tests to `#[test]`.

### Go target
- `go build ./...`
- `go vet ./...`
- `go test ./...`
- Run resulting binary. Port old tests to `*_test.go`.

### Python target
- `ruff`
- `mypy`/`pyright` if configured
- `pytest`

### Compiled languages in general
- Compile with warnings (`-Wall -Wextra` for C/C++)
- Run the binary on a sample input
- Run tests

## No configured gate

Run: ported tests (write them if none exist for the module), build/compile if applicable, and the desk sanity check. State in PROGRESS.md what gate was run.

## Failing gates

- Read the actual output. Fix the root cause.
- Re-run the specific failing gate, not the whole suite, while iterating.
- Three-attempts rule: same gate failing 3 substantive fixes in a row → write hypothesis to PROGRESS.md, classify blocker-vs-local, then BLOCK+ask or skip-to-next per SKILL.md.
- "I re-ran and it passed" is not verification — quote the relevant output line.

## Migration-specific gotchas

### Behavior parity
Run both old and new impls side-by-side on the same inputs when feasible. Compare outputs. Drift here is the most common migration bug. If outputs differ, don't mark module done — investigate the diff.

### Test porting
Old tests pin behavior. Port them to the target stack's test framework BEFORE implementing the new module — red tests prove the new code is what the old tests expected. If an old test doesn't make sense in the target stack, note it in PROGRESS.md and confirm the user is OK dropping it.

### Dependency translation
Map old-stack deps to target-stack equivalents. Don't assume parity — check interface, semantics, edge cases (e.g. Ruby's `Time.now` vs Rust's `SystemTime`, JS's `===` vs Python's `is`). Record the mapping in NOTES.md.

### Erasure discipline
After a module's callers are migrated, DELETE the old code in the same step. Don't leave dead old-stack code around — it rots and obscures progress. If the user wants to keep it as a fallback, that's a criteria decision (Phase 3), not a default.

### Performance targets (when perf-driven)
Record before/after numbers in PROGRESS.md for each module that's supposed to improve. If the target stack doesn't improve a given module, say so — don't manufacture wins. Aggregate the deltas to verify the migration meets its perf criteria.

### Paradigm shifts
Some migrations cross paradigms (OO → functional, dynamic → static, GC → manual). Don't force the old paradigm onto the new stack — write idiomatic new-stack code, but verify behavior parity carefully. Note paradigm-bridging decisions in NOTES.md.
