# Testpro — Frameworks, Coverage Tools & Tautology Prevention

Inherit the cross-cutting execution review from [Goalpro's quality contract](contracts/execution-quality.md). This reference adds test-framework, coverage, harness, and test-validity mechanics.

## Detect test framework + coverage tool

Check manifest files and config. First match wins:

| Ecosystem | Manifest / config | Test runner | Coverage tool |
|---|---|---|---|
| Node/TS | `package.json` with `vitest` | `vitest` | `vitest run --coverage` |
| Node/TS | `package.json` with `jest` | `jest` | `jest --coverage` |
| Node/TS | `package.json` with `bun test` | `bun test` | `bun test --coverage` |
| Node/TS | `package.json` with `mocha` | `mocha` | `nyc` / `c8` |
| Rust | `Cargo.toml` | `cargo test` | `cargo tarpaulin` or `cargo llvm-cov` |
| Python | `pyproject.toml`/`setup.py` with `pytest` | `pytest` | `pytest --cov={pkg}` (pytest-cov) |
| Python | `pyproject.toml` with `unittest` | `python -m unittest` | `coverage run -m unittest && coverage report` |
| Go | `go.mod` | `go test` | `go test -coverprofile=coverage.out && go tool cover -func=coverage.out` |

If no test runner is configured, testpro builds the harness (Phase 4) before doing anything else. Default picks: Node/TS → vitest, Python → pytest, Go → stdlib, Rust → cargo test.

## Coverage reading

Run the coverage tool, then read its report. Record in AUDIT.md:

- **Line coverage** % (basic baseline)
- **Branch coverage** % (better signal — uncovered branches are usually untested edge cases)
- **Function coverage** % (which functions are called by any test)

Branch coverage is the most meaningful signal for gap-finding. Line coverage can be 100% with weak assertions. Always quote the tool's output line in PROGRESS.md, don't paraphrase.

## Harness setup patterns

### Fixtures
- Shared setup data goes in a `fixtures/` or `__fixtures__/` directory next to the tests.
- Each fixture is a plain data file or factory function — no logic that can itself be wrong.
- Prefer factories over static data when tests need variations.

### Fakes vs mocks vs stubs
- **Fake**: working in-memory implementation of a dependency (e.g. in-memory repo). Best for stateful deps.
- **Stub**: returns canned responses. Best for pure I/O deps (HTTP, external APIs).
- **Mock**: records calls and asserts on them. Use sparingly — over-mocking makes tests brittle.
- Default to fakes for data layers, stubs for external services, mocks only for verifying specific call sequences.

### Factories
- A factory builds a valid entity with sensible defaults, overridable per test: `makeUser({ role: 'admin' })`.
- Prevents test coupling to a shared mutable fixture.

## Tautology prevention

A test is a tautology if it can't fail when the code is wrong. After writing each test, sanity-check:

1. **Would this test fail if I deleted the implementation?** If not, it's not testing the behavior.
2. **Does the assertion reference the actual output, or a hardcoded value?** Hardcoded `expect(true).toBe(true)` is useless.
3. **Does the test exercise a path, or just call a function?** Calling a function that returns without asserting on the result is coverage theater.
4. **Would changing the implementation's behavior break this test?** If not, the test doesn't pin behavior.

If a test fails any of these, strengthen it before logging DONE.

## Weak-test signals

Existing tests to flag for strengthening:

- `expect(result).toBeTruthy()` / `toBeDefined()` on functions that always return something
- `expect(() => fn()).not.toThrow()` — only asserts no exception, not correctness
- Tests with no assertions at all (just calling code)
- Tests that mock the thing under test
- Tests that assert on mock call counts instead of on actual output
- Snapshot tests that haven't been reviewed (snapshot size > 50 lines is a smell)

## Flake handling

If a test fails intermittently during the loop:

- Don't mark DONE.
- Run it 5+ times to confirm flake.
- Identify the source: time-dependent, order-dependent, shared state, network, random.
- Fix the root cause (usually a shared-state or order issue), not the symptom.
- Log as `FLAKE-FIXED` in PROGRESS.md with the root cause.
