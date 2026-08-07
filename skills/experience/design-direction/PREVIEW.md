# Design Direction HTML Preview Contract

## Contents

- [Purpose](#purpose)
- [Preflight inventory](#preflight-inventory)
- [Required comparison](#required-comparison)
- [HTML and interaction contract](#html-and-interaction-contract)
- [Theme and palette exploration](#theme-and-palette-exploration)
- [Iteration loop](#iteration-loop)
- [Validation](#validation)

## Purpose

Build the cheapest credible approximation of the proposed visual systems before expensive implementation. The preview must help the user compare, steer, reject, refine, and approve design logic. It is not production code, a screenshot gallery, or three palette swaps over one generic mockup.

## Preflight inventory

Before writing HTML, inventory the target's real or proposed:

- Shell, navigation, page headers, sidebars, toolbars, and content regions.
- Primitive and compound components, their variants, and ownership.
- High-frequency and high-risk flows.
- Dense data, editorial content, forms, tables/lists/timelines/charts, media, and code where present.
- Loading, empty, validation, error, disabled, success, degraded, and recovery states.
- Small, medium, and large viewport behavior; localization/text expansion; keyboard, pointer, and touch use.
- Existing brand assets, fonts, themes, tokens, and design constraints.

Record which preview elements are `IMPLEMENTED`, `PROPOSED`, or `INFERRED`. Prefer representative content from project fixtures or documentation, sanitized as necessary. Never copy secrets or customer data.

## Required comparison

Every direction panel must render the same representative product slice so differences are comparable. Each panel—not merely the page as a whole—must include these sections with `data-preview-section` attributes:

1. `direction-summary` — name, design read, intended feeling, strongest tradeoff, evidence/assumptions.
2. `typography` — display, page title, section title, body, label, metadata, numeric/code roles where relevant.
3. `palette` — primitive swatches plus semantic surface, foreground, border, accent, focus, success, warning, danger, and info roles.
4. `surfaces` — canvas, shell, base, raised, overlay, nested boundaries, elevation/material behavior.
5. `components` — representative navigation, buttons, links, inputs, controls, cards or project equivalents, and data/content structures.
6. `states` — applicable loading, empty, validation, error, disabled, success, degraded, recovery, hover/focus/active/selected states.
7. `responsive` — a visible narrow-layout specimen or viewport control, with wrapping, ordering, density, and overflow behavior.
8. `motion` — purpose, frequency, durations/curves/springs as hypotheses, reduced-motion alternative, and at least one safe illustrative interaction when motion is applicable.
9. `tradeoffs` — product fit, accessibility/performance risk, system implications, preservation/change budget, and invalidation signal.

Use the project's actual component vocabulary. A marketing site, operations console, editor, and social feed should not share a canned dashboard preview.

## HTML and interaction contract

- One self-contained `DIRECTION-PREVIEW.html`: embedded CSS/JS, local or data-URI assets only, no remote fonts/CDNs/analytics/network calls.
- Include `<!doctype html>`, `<html lang>`, UTF-8 charset, viewport metadata, descriptive title, landmark elements, logical headings, and a visible “planning preview, not production” notice.
- Put revision, slug, evidence timestamp, and option IDs in visible metadata and `data-*` attributes.
- Provide at least two direction controls using buttons with `data-direction-target`, `aria-controls`, and managed `aria-selected`. Panels use matching unique `data-direction-panel` IDs and support keyboard activation.
- When multiple theme families/modes are shown, use a second accessible control group; do not overload the direction switcher.
- Preserve usable focus styles, semantic controls, contrast, zoom/reflow, and text spacing. Never suppress outlines globally.
- Include `@media (prefers-reduced-motion: reduce)` and ensure selection/state changes remain understandable without spatial movement.
- Include responsive CSS and make the comparison usable at 320 CSS pixels without horizontal page scrolling, except inside explicitly scrollable data specimens.
- Use realistic copy and data. No lorem ipsum, Jane Doe, Acme, placeholder gradients, dead `#` links, or fake controls that look actionable without a preview-only explanation.
- Include a feedback tray explaining the three conversational actions: refine an option, request a new set, or approve an option/revision. The HTML must not pretend it can modify artifacts itself.
- Escape or sanitize project-derived content. Do not interpolate untrusted HTML into scripts.

## Theme and palette exploration

When themes are relevant, show semantic parity rather than surface recoloring:

- Same components and states across each mode/family.
- Complete surface/foreground/border/focus/status roles.
- Theme-specific imagery, charts, syntax, shadows, overlays, and browser chrome when relevant.
- Contrast and material risks disclosed next to the option.
- A palette family may inspire primitive colors, but components consume semantic roles only.

Consult the independently discovered `theme-library` skill in embedded mode. Shortlist a few product-fit families, interpret their palette DNA creatively, and disclose evolved or added colors next to the direction; do not dump the full catalog into every preview or copy source role assignments mechanically.

## Iteration loop

For each user turn:

1. Record feedback in `DIRECTION-OPTIONS.md`.
2. Classify it as `REFINE`, `NEW SET`, or `APPROVE`.
3. Increment the revision and update visible preview metadata.
4. Preserve rejected directions and reasons; never silently rewrite history.
5. Write and validate the immutable `previews/DIRECTION-PREVIEW-R{n}.html` snapshot, then refresh `DIRECTION-PREVIEW.html` as the stable latest alias and validate it too.
6. Summarize exactly what changed and present the clickable preview.

If none fit, create a new set from the original product evidence plus rejection reasons. Do not average rejected options into a compromise unless the user explicitly asks for a hybrid.

## Validation

Run:

```bash
python3 {design-direction-skill-root}/scripts/validate_direction_preview.py \
  agent-work/{slug}/design-direction/DIRECTION-PREVIEW.html
```

The validator checks structure, controls, required sections, self-containment, responsive/reduced-motion support, feedback actions, and placeholder leakage. It cannot prove taste, contrast, accessibility, or runtime feel. Manually open the file, exercise every direction/theme control by keyboard, inspect narrow and wide layouts, zoom to 200%, enable reduced motion, and verify representative content and states.
