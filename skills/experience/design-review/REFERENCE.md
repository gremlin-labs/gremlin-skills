# Design Review Reference

## Contents

- [Review matrix](#review-matrix)
- [Direction contract and visitor mode](#direction-contract-and-visitor-mode)
- [Copy checks](#copy-checks)
- [Task critique](#task-critique)
- [Browser chrome and first viewport](#browser-chrome-and-first-viewport)
- [Finding priority](#finding-priority)
- [Verdict rules](#verdict-rules)
- [Output schema](#output-schema)
- [Sources](#sources)

## Review matrix

| Dimension | Inspect when affected |
|---|---|
| Product intent | Approved direction contract, user goal, hierarchy, preservation rules |
| Visitor mode | Persuade / Operate / Read / Experience from the contract, or an `ASSUMPTION` from the surface |
| System integrity | Semantic tokens, themes, recipes, variants, ownership, exceptions |
| Craft | Composition, typography, content, imagery, material, coherence, anti-default rationale |
| Copy | Labels, actions, errors, empty states, placeholders against the message hierarchy |
| States | Loading, empty, validation, error, disabled, success, degraded, recovery |
| Responsive/localization | Small/large/intermediate viewport, zoom, text expansion, wrapping, RTL when supported |
| Accessibility | Semantics, names, focus, keyboard, contrast, targets, non-color cues, assistive technology |
| Motion | Purpose, frequency, response, origin, interruption, reduced motion, input modality, cohesion |
| Performance | Layout/paint/main-thread risk, assets, busy-state behavior, measured evidence |
| Maintainability | Shared primitives, rule location, tests, documentation, exception ownership |

## Direction contract and visitor mode

Cite `DIRECTION-CONTRACT.md` (or an equivalent six-block contract) before taste. If it is missing or contradictory with another authority source, mark contract checks `UNVERIFIED`. Do not invent Thesis, Own-world, Story, First viewport, Form, or Finish.

Record visitor mode from the contract. If only the surface is known, infer Persuade, Operate, Read, or Experience and label `ASSUMPTION`. Do not fail an Operate settings route for missing Persuade spectacle.

## Copy checks

Use the same hierarchy as Designpro: one fact the user needs now, the next action, supporting context, then tone. Actions are verb plus object. Errors answer what failed, why when useful, and how to recover. Empty states distinguish first-use, no results, filters, permissions, and failure. Placeholders are examples, not labels.

Report a copy finding only when it harms comprehension or task completion. Do not rewrite strings here; route rewrites to `prose-humanizer`.

## Task critique

Run only when the bounded surface has a primary user task. Do not expand into a whole-app critique. Cap personas at two.

### Design specificity

Verdict: authored for this product, or interchangeable with a category sibling if the logo were swapped. Category-interchangeable UI is a finding only when an approved contract promised an own-world.

### Cognitive-load checklist

Mark each item `pass`, `fail`, or `n/a` with one evidence line:

1. At a decision point the visitor holds at most four working-memory chunks.
2. One primary action is visually and verbally first.
3. Labels use the visitor's words, not internal schema names.
4. Errors are recoverable without restarting the task.
5. Location and remaining work stay visible through the flow.
6. Defaults are safe; destructive choices are not pre-selected.
7. Irreversible actions require an explicit confirm that names the object.
8. A first-timer can finish without tribal knowledge or a hidden shortcut.

### Personas

Prefer two personas already evidenced in the product or direction package. If none exist, use a first-timer plus the mode-relevant specialist: a power user for Operate, a mobile-interrupted visitor for Persuade, a skimming reader for Read, or an immersed participant for Experience. Do not require stock names.

### Optional Nielsen scoring

A 0–4 table is optional. On Persuade or Experience surfaces, heuristics 7 (flexibility and efficiency of use) and 10 (help and documentation) may be `n/a`; renormalize the denominator. Never fail a landing page for missing power-user shortcuts.

## Browser chrome and first viewport

When the change touches theming, inspect selection, caret, scrollbar, focus ring, underline offset, and tabular numerals against the approved palette. When the change is a marketing or first-run surface, the first viewport must still state the thesis after copy is stripped.

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

Invalid, blank, or mislabeled captures do not bind a verdict. One batched rendered pass is the ceiling unless later fixes are claimed, in which case one confirm pass is enough.

## Output schema

`DESIGN-REVIEW.md` contains:

1. **Scope and revision** — diff/commit/route/component/slice.
2. **Governing intent and system sources** — linked artifacts and precedence.
3. **Visitor mode** — contract value or surface `ASSUMPTION`.
4. **Direction contract** — citation, or `UNVERIFIED` if missing.
5. **Evidence coverage** — static, runtime, themes, states, viewports, inputs, content, accessibility, motion, performance.
6. **Verified strengths** — important invariants preserved.
7. **Task critique** — specificity, checklist, personas; or `Not applicable` with reason.
8. **Findings** — priority, status, evidence, governing source, behavior, impact, correction boundary, verification.
9. **Unverified checks** — missing evidence and why it matters.
10. **Verdict** — one contract value and rationale.
11. **Correction routing** — existing Goalpro criteria or recommended systemic audit.
12. **Re-review conditions** — exact evidence needed to change verdict.
13. **Self-judgment** — required satisfaction statement.

## Sources

- [Emil Kowalski's design engineering skills](https://github.com/emilkowalski/skills) inspired the focused motion-review bar and perceptual evidence.
- [Taste Skill by Leonxlnx](https://github.com/Leonxlnx/taste-skill) inspired anti-default and preservation-aware craft review.
- [Impeccable](https://github.com/pbakaus/impeccable) inspired visitor-mode judgment, compact direction-contract citation, UX copy checks, and bounded task critique. Use original, product-specific reasoning; do not copy detector rules or command names. These sources do not define the verdict and do not imply endorsement.
- Gremlin's approved product artifacts and system contracts remain authoritative.
