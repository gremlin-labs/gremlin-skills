# Landing Page HTML Preview Contract

## Purpose

The preview is a decision surface between product truth and production implementation. It must let the user judge the message, CTA, highlights, persuasion order, visual design, responsive behavior, and intended motion without mistaking the artifact for production code.

## Preflight inventory

Before generating HTML, record:

- approved audience, arrival intent, product callouts, benefit framing, claims, proof, objections, and CTA ladder;
- existing brand assets, tokens, typography, components, imagery, screenshots, demos, and visual-language decisions;
- target routes, navigation context, destination URLs, responsive constraints, localization, and content extremes;
- SEO disposition and traffic intent;
- implementation stack, performance constraints, accessibility requirements, and intended TurbulenceJS roles.

Tag preview content `EVIDENCE`, `USER DECISION`, `ASSUMPTION`, or `UNKNOWN`. Use visible “proof unavailable” or “decision pending” treatments instead of invented testimonials, numbers, or logos.

## Adaptive comparison

Set `data-preview-mode="single"` when an approved direction exists. Render one implementation-fidelity direction and only the targeted variants needed for unresolved sections.

Set `data-preview-mode="comparison"` when no approved direction exists. Render two or three directions with the same approved message, product truth, and CTA goal so differences are meaningful. Options must differ in persuasion and design logic, not just palette.

Every direction panel must expose these annotated aspects using `data-preview-aspect` values. They may appear in the page itself or an adjacent decision tray; they do not prescribe section order:

- `message` — audience, arrival intent, value proposition, headline hierarchy, and strongest assumption.
- `cta` — primary and secondary action, outcome labels, destination/behavior, commitment, and friction.
- `product` — prioritized callouts, feature-benefit relationship, demonstration, and differentiation.
- `proof` — approved evidence or an explicit statement that proof is unavailable.
- `objections` — important concerns, risk reversal, and information needed before commitment.
- `responsive` — narrow-layout specimen or control plus ordering, wrapping, touch, and content behavior.
- `motion` — purpose, semantic role, TurbulenceJS implementation hypothesis, intensity, interruption, and reduced endpoint.
- `seo` — index posture, title/description hypothesis, heading structure, entity/structured-data implications.
- `tradeoffs` — conversion, brand, accessibility, performance, implementation, and invalidation risks.

Mark actionable specimens with `data-cta`. Preview-only actions must explain their intended destination or behavior and must not use dead `href="#"` links.

## HTML and interaction contract

- Produce one self-contained HTML file with embedded CSS and JavaScript, local/data-URI assets only, and no network calls, tracking, remote fonts, remote media, or CDNs.
- Include doctype, language, UTF-8 charset, viewport metadata, descriptive title, landmarks, logical headings, and a visible “planning preview, not production” notice.
- Put slug, revision, evidence date, preview mode, and option IDs in visible metadata and `data-*` attributes.
- For comparison mode, provide at least two keyboard-operable buttons using `data-direction-target`, `aria-controls`, and managed `aria-selected`. Panels use matching unique IDs and `data-direction-panel`.
- For single mode, one visible panel is sufficient. Targeted section variants need accessible controls when interactive.
- Use realistic approved content. Do not use lorem ipsum, Acme, Jane Doe, fake logos, unsupported metrics, fabricated testimonials, placeholder gradients, empty images, or controls that pretend to work.
- Preserve focus visibility, semantic controls, contrast, zoom/reflow, text spacing, and keyboard/pointer/touch parity. Never globally suppress outlines.
- Include responsive CSS that works at 320 CSS pixels without page-level horizontal scrolling, except explicitly scrollable specimens.
- Include `@media (prefers-reduced-motion: reduce)` and ensure every animation has an understandable reduced endpoint.
- Illustrative preview motion may use embedded CSS/JavaScript. Do not pull TurbulenceJS from a CDN or claim the preview proves its production integration.
- Include a feedback tray explaining `REFINE`, `NEW SET`, and `APPROVE`. The artifact cannot approve itself or modify project files.
- Escape project-derived content and never interpolate untrusted HTML into scripts.

## Revision loop

For every user response:

1. Record the feedback and classify it `REFINE`, `NEW SET`, or `APPROVE` in `PAGE-DIRECTIONS.md`.
2. Increment the revision for any content or design change.
3. Update visible metadata and option IDs.
4. Preserve rejected options and reasons.
5. Validate the immutable `previews/LANDING-PAGE-PREVIEW-R{n}.html` file.
6. Refresh and validate `LANDING-PAGE-PREVIEW.html` as the stable current alias.
7. Present the clickable alias and summarize the material delta.

Approval names the exact revision and scope. A later material change to message, CTA, product callouts, page logic, visual direction, motion posture, or proof invalidates approval until the delta is confirmed.

## Validation

Run:

```bash
python3 {landing-page-skill-root}/scripts/validate_landing_page_preview.py \
  agent-work/{slug}/landing-page/LANDING-PAGE-PREVIEW.html
```

Then manually inspect direction/variant controls, CTA descriptions, narrow and wide layouts, keyboard use, 200% zoom, reduced motion, content extremes, contrast, visual hierarchy, and claim provenance. The validator proves structure and self-containment only.
