# Onboarding Direction HTML Preview Contract

## Contents

- [Purpose](#purpose)
- [Preflight](#preflight)
- [Required comparison](#required-comparison)
- [Flow simulation](#flow-simulation)
- [HTML and accessibility](#html-and-accessibility)
- [Iteration](#iteration)
- [Validation](#validation)

## Purpose

Build the cheapest credible simulation of the proposed onboarding systems before implementation. The preview is the primary surface for comparing, steering, rejecting, refining, and approving activation logic. It is not production code, a static mood board, or several palette treatments over the same sequence.

## Preflight

Before writing HTML, inventory the scoped product promise, activation target, platforms, segments, current or proposed states, audit findings and strengths, approved visual language, neighboring copy, auth and permission constraints, data and privacy behavior, accessibility, localization, measurement, and delivery unknowns.

Use sanitized realistic content from current product evidence. Mark preview behavior `IMPLEMENTED`, `PROPOSED`, or `INFERRED`. Never copy secrets, customer data, production identifiers, or unsupported claims.

## Required comparison

Render every option against the same product promise and activation target. Each direction panel must contain these `data-preview-section` values:

1. `direction-summary` — option ID, rationale, intended user response, strongest tradeoff, and evidence status.
2. `activation-path` — entry, steps, system work, commitment, activation moment, and continued success.
3. `screens` — clickable representative sequence for every platform in scope.
4. `states` — loading, validation, permission, denied, error, degraded/offline, interruption, resume, success, and skip where applicable.
5. `copy` — representative titles, actions, helper text, recovery, and success language with voice provenance.
6. `accessibility` — keyboard/touch/assistive technology, focus, targets, text expansion, reduced motion, and localization posture.
7. `measurement` — activation hypothesis, event meanings, guardrail, gaps, and cheapest validation experiment.
8. `tradeoffs` — user success, trust, platform, implementation, performance, reversibility, audit findings, and invalidation signal.

Use the product's real vocabulary. A creator tool, financial workflow, enterprise invitation, health product, and consumer AI app must not share a canned onboarding sequence.

## Flow simulation

- Provide at least two direction controls with `data-direction-target`, `aria-controls`, and managed `aria-selected`.
- Give panels matching unique `data-direction-panel` IDs.
- Include at least one `data-platform-view` per direction and every platform in scope across all directions.
- Use buttons or valid links for simulated actions. Label them as prototype interactions when their behavior is illustrative.
- Mark each material step with `data-flow-step` and the meaningful success with `data-activation-moment`.
- Let users move forward and backward, skip where safe, leave, resume, deny permissions, retry errors, and reach success when those paths apply.
- Preserve comparable starting conditions across options. Do not make one option look better by giving it a stronger generated result, fewer safety requirements, or different product capability.
- Show what continues after first value rather than ending at a completion screen.
- Include a feedback tray with `data-preview-action` values `refine`, `new-set`, and `approve`. The preview explains the conversational action; it does not pretend to edit artifacts itself.

## HTML and accessibility

- Use one self-contained HTML file with embedded CSS and JavaScript, local or data-URI assets only, and no remote fonts, scripts, analytics, or network calls.
- Include document language, UTF-8 charset, viewport metadata, descriptive title, landmarks, logical headings, and a visible “planning preview, not production” notice.
- Put revision, slug, evidence date, option IDs, and platform scope in visible metadata and `data-*` attributes.
- Keep direction and platform controls keyboard-operable with visible focus and accurate ARIA state.
- Include responsive behavior that remains usable at 320 CSS pixels without page-level horizontal scrolling.
- Include reduced-motion behavior. Do not block interaction behind animation.
- Use sufficient semantics, labels, target sizes, ordering, and text wrapping for a planning artifact. Manually test zoom to 200 percent and text expansion.
- Avoid lorem ipsum, generic example companies or people, placeholder gradients, dead links, unsupported metrics, fake consent, and controls that appear to perform real external actions.
- Escape or sanitize project-derived content and never interpolate untrusted markup into scripts.

## Iteration

For each revision:

1. Record feedback and disposition in `DIRECTION-OPTIONS.md`.
2. Classify it as `REFINE`, `NEW SET`, or `APPROVE`.
3. Rerun embedded humanization for changed copy.
4. Increment visible revision metadata.
5. Save and validate immutable `previews/ONBOARDING-PREVIEW-R{n}.html`.
6. Refresh and validate `ONBOARDING-PREVIEW.html` as the latest alias.
7. Summarize exactly what changed and present the clickable file.

If every option is rejected, create a new set from the original evidence and rejection reasons. Do not average rejected directions into a compromise without explicit user direction.

## Validation

Run:

```bash
python3 {onboarding-direction-skill-root}/scripts/validate_onboarding_preview.py \
  agent-work/{slug}/onboarding-direction/ONBOARDING-PREVIEW.html
```

The validator checks required metadata, option controls and panels, platform views, sections, flow and activation markers, feedback actions, responsive and reduced-motion rules, self-containment, and placeholder leakage. It cannot prove activation quality, copy fidelity, consent, accessibility, visual fit, or runtime feel. Manually exercise every option and state with keyboard and pointer or touch simulation, inspect narrow and wide layouts, zoom, enable reduced motion, and compare the preview with source evidence.
