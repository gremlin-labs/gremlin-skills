# Design Review Reference

## Contents

- [Review matrix](#review-matrix)
- [Finding priority](#finding-priority)
- [Verdict rules](#verdict-rules)
- [Output schema](#output-schema)
- [Sources](#sources)

## Review matrix

| Dimension | Inspect when affected |
|---|---|
| Product intent | Approved direction, user goal, hierarchy, preservation rules |
| System integrity | Semantic tokens, themes, recipes, variants, ownership, exceptions |
| Craft | Composition, typography, content, imagery, material, coherence, anti-default rationale |
| States | Loading, empty, validation, error, disabled, success, degraded, recovery |
| Responsive/localization | Small/large/intermediate viewport, zoom, text expansion, wrapping, RTL when supported |
| Accessibility | Semantics, names, focus, keyboard, contrast, targets, non-color cues, assistive technology |
| Motion | Purpose, frequency, response, origin, interruption, reduced motion, input modality, cohesion |
| Performance | Layout/paint/main-thread risk, assets, busy-state behavior, measured evidence |
| Maintainability | Shared primitives, rule location, tests, documentation, exception ownership |

## Finding priority

- `P0` — blocks essential use or creates severe accessibility/safety harm.
- `P1` — material regression in common flow, approved intent, theme/system invariant, accessibility, or motion correctness.
- `P2` — bounded inconsistency or maintainability defect that should be corrected but need not block release when risk is controlled.
- `P3` — optional polish with explicit product rationale; never blocks alone.

Do not report a finding without a governing source or concrete user/system impact. Preference is not evidence.

## Verdict rules

- `BLOCK` for any unresolved P0/P1 or for missing evidence required by approved acceptance criteria.
- `APPROVE WITH FOLLOW-UP` for P2/P3 items with an owner, safe deferral, and verification path.
- `APPROVE` when no material findings remain and applicable checks are verified.
- `UNVERIFIED` when the reviewer cannot resolve material authority or required runtime evidence.

## Output schema

`DESIGN-REVIEW.md` contains:

1. **Scope and revision** — diff/commit/route/component/slice.
2. **Governing intent and system sources** — linked artifacts and precedence.
3. **Evidence coverage** — static, runtime, themes, states, viewports, inputs, content, accessibility, motion, performance.
4. **Verified strengths** — important invariants preserved.
5. **Findings** — priority, status, evidence, governing source, behavior, impact, correction boundary, verification.
6. **Unverified checks** — missing evidence and why it matters.
7. **Verdict** — one contract value and rationale.
8. **Correction routing** — existing Goalpro criteria or recommended systemic audit.
9. **Re-review conditions** — exact evidence needed to change verdict.
10. **Self-judgment** — required satisfaction statement.

## Sources

- [Emil Kowalski's design engineering skills](https://github.com/emilkowalski/skills) inspired the focused motion-review bar and perceptual evidence.
- [Taste Skill by Leonxlnx](https://github.com/Leonxlnx/taste-skill) inspired anti-default and preservation-aware craft review.
- Gremlin's approved product artifacts and system contracts remain authoritative; external inspiration does not define the verdict.
