# Restructure — Stack Layouts & Move Mechanics

Inherit the cross-cutting execution review from [Goalpro's quality contract](contracts/execution-quality.md). This reference adds layout, move, and import-update mechanics.

## Best-practice layouts by stack

Use these as the comparison baseline in Phase 1. The project's *own* dominant conventions win when they conflict with these — but flag the conflict in AUDIT.md.

### TypeScript / Node
- `src/` for source, `test/` or `__tests__/` colocated or top-level
- Framework-specific: Next.js (app/ or pages/), NestJS (modules), Express (routes/ + controllers/ + services/)
- Files: kebab-case for modules, PascalCase for React components, camelCase for utilities
- Colocate component + test + styles (`.tsx` / `.test.tsx` / `.module.css`)

### Python
- `src/{package}/` layout (preferred over flat) per PyPA
- `tests/` top-level, mirror the package structure
- `__init__.py` in every package dir
- snake_case files, PascalCase classes, UPPER_CASE constants

### Rust
- `src/lib.rs` for library, `src/bin/` for binaries, `src/main.rs` for the primary binary
- Module-as-directory: `src/foo/mod.rs` or `src/foo.rs` + `src/foo/` (modern style)
- snake_case files

### Go
- `cmd/{binary}/main.go` for binaries, `internal/` for private packages, `pkg/` for public (contested — some teams skip `pkg/`)
- Test files colocated: `foo.go` + `foo_test.go`

### Ruby / Rails
- Convention over configuration: `app/models/`, `app/controllers/`, `app/services/`, `app/jobs/`
- snake_case files, CamelCase classes

## Import-path update patterns

When a file moves, every importer needs updating. Patterns by stack:

### TypeScript / ES modules
- Use `grep` for the old relative path (`from './old/path'` or `from '../old/path'`) and the bare specifier if it's a package internal
- Path-alias imports (`@/foo`) need both the alias resolution AND the source path updated
- After moving, run `tsc --noEmit` to catch any missed import

### Python
- Update `from old.path import x` → `from new.path import x`
- If the moved module had relative imports (`from . import sibling`), re-derive them — the relative graph changed
- `__init__.py` re-exports need updating if the moved module was part of a package's public API

### Rust
- `mod foo;` declarations follow the file move automatically when using the `src/foo.rs` + `src/foo/` pattern
- `use crate::old::path` → `use crate::new::path` for explicit paths
- Run `cargo check` to catch missed `use` statements

### Go
- Move the file, update the `package` declaration if the directory name changed
- Update all `import "github.com/x/old/path"` → `"github.com/x/new/path"` across the repo
- `go build ./...` catches missed imports

## Gate commands by stack

After every move, run the project's gate. Detect from manifest:

| Stack | Build | Typecheck | Lint | Tests |
|---|---|---|---|---|
| TS/Node | `npm run build` | `npx tsc --noEmit` | `npm run lint` (oxlint/fallow/eslint/biome) | `npm test` |
| Python | (n/a) | `mypy` / `pyright` if configured | `ruff` | `pytest` |
| Rust | `cargo build` | (cargo check) | `cargo clippy -- -D warnings` | `cargo test` |
| Go | `go build ./...` | (go vet) | `golangci-lint run` if configured | `go test ./...` |

If no test suite exists, the gate is build+typecheck+lint. Note the missing test suite in AUDIT.md — it's a refactor candidate (suggest running testpro after restructure).

## Move safety

- Use `git mv` (or the VCS equivalent) so history follows the file. Plain `mv` loses renames in `git log --follow`.
- One move per commit when feasible — makes `git bisect` useful if something breaks later.
- Don't move and edit in the same commit if you can help it — move first, commit, then edit. Easier to review.
- If a move would conflict with uncommitted changes, ask the user to commit or stash first (same as releasepro's dirty-tree abort).

## Opportunistic split signals

A move surfaces a split opportunity when:

- The file being moved has ≥2 unrelated concerns (grep for `//` section dividers, multiple unrelated exports, functions with no shared dependencies)
- The file being moved exceeds ~300 lines and isn't a single coherent module (e.g. a router with all handlers inline)
- A function in the moved file is only used by code in a different directory than the file's new home — re-home it

A split is NOT warranted when:

- The file is large but cohesive (e.g. a single parser with many rules)
- The "concerns" are actually all used together by every caller
- Splitting would create files smaller than ~50 lines each

When in doubt, don't split. Note it in REFACTOR-CANDIDATES.md instead.
