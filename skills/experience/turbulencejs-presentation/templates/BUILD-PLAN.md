# Build plan: {title}

## Outcome

{Executable definition of done.}

## Scope and exclusions

- Included: {items}
- Excluded: {items}

## Target architecture

- Semantic deck model: {path/shape}
- Rendering: {path/ownership}
- Presentation state and URL: {path/contract}
- Motion ownership: {path/diagnostics}
- Readiness/export: {path/signal}
- Browser verification: {path/matrix}

## Implementation slices

1. {Representative vertical slice and focused gate.}
2. {Semantic layout/aspect system and focused gate.}
3. {Full narrative and focused gate.}
4. {Documentation/package integration and final gate.}

## Approval gates

- Direction gate: brief, storyboard, and style contract approved before production.
- Sample gate: exact-size 16:9 and 9:16 representative slide approved before the full build.

## Verification

- Structural: {validation, unit, build, lint, typecheck}
- Browser: every slide × both viewports × full/reduced motion
- Accessibility: {semantics, keyboard, focus, contrast, minimum type, reduced endpoints}
- Lifecycle: {interrupt, cleanup, zero idle work, surface teardown}
- Visual: full-size capture locations and named reviewer observations
- Packaging/delivery: {commands}

## Dependencies and risks

- {Dependency or risk, mitigation, owner.}

## Rollback

- {Additive or phase-local rollback path; no destructive command placeholders.}
