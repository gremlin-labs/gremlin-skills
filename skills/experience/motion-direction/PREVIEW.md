# Motion Direction Studio preview contract

## Contents

- [Purpose](#purpose)
- [Preflight inventory](#preflight-inventory)
- [Required comparison](#required-comparison)
- [Interaction contract](#interaction-contract)
- [Evidence and diagnostics](#evidence-and-diagnostics)
- [Iteration](#iteration)
- [Validation](#validation)

## Purpose

Build the cheapest credible comparison of complete motion systems before implementation. The Studio helps the user compare, steer, reject, refine, and approve motion logic. It is not production code, a generic component gallery, or an intensity selector.

## Preflight inventory

Inventory the target's actual page families, shell/navigation, component vocabulary, state model, input methods, responsive behavior, visual direction, content density, existing animation ownership, public TurbulenceJS version/exports, accessibility constraints, performance constraints, and runtime gates.

Record every specimen as `IMPLEMENTED`, `PROPOSED`, or `INFERRED`, with evidence. Use realistic sanitized product content; never copy secrets, credentials, private customer material, or untrusted HTML.

## Required comparison

Each direction panel must render the same representative synthetic product slices. Globally cover or explicitly mark not applicable:

- direction summary and trade-offs;
- page/route entry and navigation;
- menu/sidebar/drawer behavior;
- overlay/dialog/popover behavior;
- form/control feedback;
- list/data/content update;
- loading, spinner, skeleton, and progress behavior;
- empty, error, degraded, recovery, and success behavior;
- toast/notification behavior;
- one rare Signature delight opportunity.

Every specimen identifies purpose, frequency, semantic role, delight tier, public Turbulence family hypothesis, evidence status, reduced endpoint, and primary risk. Put its machine-checkable evidence label in `data-evidence-status="SIMULATED|PUBLIC-RUNTIME|UNVERIFIED"` on the element carrying `data-motion-category`.

Directions must differ across at least three consequential relationships from `REFERENCE.md`. The same DOM may be reused for comparability, but the spatial model, rhythm, choreography, material/effect vocabulary, and delight placement cannot collapse into a common implementation with different speed variables.

## Interaction contract

- Use one self-contained `MOTION-DIRECTION-PREVIEW.html` with embedded CSS/JS and local or data-URI assets only.
- Include `<!doctype html>`, `<html lang>`, UTF-8 charset, viewport metadata, descriptive title, logical headings, and a `main` landmark.
- Put slug, revision, option IDs, and evidence timestamp in visible metadata and `data-*` attributes.
- Provide at least two direction buttons with `data-direction-target`, `aria-controls`, and managed `aria-selected`; panels use matching `data-direction-panel` IDs.
- Provide page/surface controls, `data-replay-motion`, full/reduced-motion controls, and `data-stress-motion` interruption controls.
- Include `@media (prefers-reduced-motion: reduce)` and make the explicit reduced mode independently usable.
- Support keyboard activation, visible focus, 320 CSS-pixel reflow, 200% zoom, and no horizontal page scrolling outside explicit data specimens.
- Include a visible “planning preview, not production” notice and feedback tray offering `REFINE`, `NEW SET`, and `APPROVE`.
- Do not use remote scripts, styles, fonts, analytics, tracking, dead controls, lorem ipsum, generic fake people/companies, or unlabeled simulations.

## Evidence and diagnostics

Label every motion specimen:

- `SIMULATED` — inline CSS/JS approximates the intended feel only.
- `PUBLIC-RUNTIME` — verified installed public TurbulenceJS behavior executes.
- `UNVERIFIED` — exact feel or public capability still needs proof.

When public runtime behavior executes, expose active owned work, interruption/retargeting result, and settled cleanup diagnostics. A simulated preview must not show fake runtime counters.

View all directions at normal speed before using slow motion or frame-by-frame diagnosis. Replay repeated flows and use the stress control to test open-close-open, route replacement, progress cancellation, or the target's equivalent interruption.

## Iteration

For every user turn:

1. Record feedback as `REFINE`, `NEW SET`, or `APPROVE`.
2. Increment the revision and visible metadata.
3. Preserve rejected options and reasons.
4. Write `previews/MOTION-DIRECTION-PREVIEW-R{n}.html` as an immutable snapshot.
5. Refresh and validate the stable `MOTION-DIRECTION-PREVIEW.html` alias.
6. Present the clickable preview and describe exact changes.

Approval names the option and validated revision. Prose approval without a matching Studio revision is incomplete.

## Validation

Run:

```bash
python3 {motion-direction-skill-root}/scripts/validate_motion_direction_preview.py \
  agent-work/{slug}/motion-direction/MOTION-DIRECTION-PREVIEW.html
```

Then manually exercise every direction/page/motion/replay/stress control by keyboard, inspect normal and reduced motion, test narrow and wide layouts plus 200% zoom, verify realistic content and evidence labels, and inspect any runtime diagnostics. The validator proves structure and self-containment; it cannot prove taste, feel, contrast, performance, or lifecycle correctness.

Open the artifact directly when the available browser supports local files. If it does not, serve only the skill-stage directory over a loopback address with a bounded local preview server or host preview utility, keep it unavailable to the LAN, make no application-source copy, and stop the server after review. Never upload the Studio or weaken browser security to obtain a preview. If no rendered browser surface is available after those safe options, record the manual gate `BLOCKED` and do not ask for direction approval.
