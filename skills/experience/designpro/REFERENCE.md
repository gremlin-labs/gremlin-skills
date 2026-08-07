# Designpro Reference

Use every applicable section. This reference defines evidence and output contracts; verify external standards and tool behavior against current primary documentation rather than treating version-sensitive details here as frozen.

## Contents

- [Evidence model](#evidence-model)
- [Sampling and runtime inspection](#sampling-and-runtime-inspection)
- [Token and theme audit](#token-and-theme-audit)
- [Consistency matrices](#consistency-matrices)
- [Craft and direction evidence](#craft-and-direction-evidence)
- [Accessibility and contrast](#accessibility-and-contrast)
- [Enforcement selection](#enforcement-selection)
- [Documentation contracts](#documentation-contracts)
- [Artifact schemas](#artifact-schemas)
- [Finding format](#finding-format)
- [Current primary sources](#current-primary-sources)

## Evidence model

Assign one status to every audit check:

- `VERIFIED` — inspected source, configuration, runtime, or test evidence demonstrates the conclusion.
- `FINDING` — evidence demonstrates inconsistency, exclusion, drift, missing governance, or material risk.
- `NOT APPLICABLE` — the capability or risk is demonstrably absent; state why.
- `UNVERIFIED` — evidence or safe access is missing; name what would verify it.

Distinguish:

- **Observed defect** — current evidence violates an established rule or standard.
- **Policy contradiction** — authoritative sources disagree; requires reconciliation, not an invented answer.
- **Risk** — plausible failure with incomplete runtime proof; describe the scenario and missing evidence.
- **Improvement** — stronger consistency or maintainability without a current defect.

For source evidence cite `file:line`. For runtime evidence record route, viewport, theme, state, interaction, inspection date, and sanitized screenshot or measurement path when available. Never cite a scanner match without reading its context.

## Sampling and runtime inspection

Build a route and component inventory before sampling. Include all high-risk or high-frequency surfaces and a representative cross-section of the rest.

Always include where present:

- Global shell, navigation, page header, authentication, onboarding, settings, billing, destructive actions, and the primary product journey.
- Buttons, links, forms, validation, tables or lists, cards, dialogs, menus, tooltips, notifications, empty states, loading states, and error recovery.
- The smallest and largest supported viewports, one intermediate viewport, 200% zoom, keyboard-only navigation, reduced motion, and every supported theme.
- Long localized strings, large user content, zero data, maximal data, slow loading, permission loss, and recoverable failure where applicable.

Record why the sample is representative. Do not claim application-wide compliance from a single route. If the app cannot run, perform static inspection and mark computed style, interaction, and rendered contrast checks `UNVERIFIED`.

## Token and theme audit

### Token layers

Classify tokens into:

1. **Primitive** — raw palette, scale, duration, or dimension values.
2. **Semantic** — product roles such as `surface-raised`, `text-muted`, `border-danger`, or `space-card-inline`.
3. **Component** — narrowly scoped aliases when a component has a stable product role.

Components should normally consume semantic or sanctioned component tokens, not primitive palette values. Avoid component tokens that merely rename a one-off hardcoded value.

For each token record name, kind, source, resolved value per theme, aliases, consumers, status, and notes. Flag alias cycles, unresolved references, unused values, duplicate values with competing meaning, names that misrepresent their role, and missing semantic roles that cause raw-value repetition.

### Theme-ready invariant

A single-theme application is theme-ready when a second complete semantic mapping can be introduced without ordinary components learning the new theme name or receiving design-value rewrites. Validate this by tracing representative component styles to semantic tokens.

### Multi-theme completeness

When themes apply, create a table with semantic roles as rows and themes as columns. Every required cell must resolve. Explicitly model theme inheritance and fallback; a fallback is acceptable only when intentional, documented, and semantically correct.

Audit:

- Surface sequence and allowed nesting.
- Foreground, border, focus, icon, control, selection, and status roles.
- Shadows, glows, overlays, scrims, transparency, images, charts, and syntax.
- Default selection, system preference, persistence, SSR, hydration, first paint, synchronization, and recovery from an invalid stored theme.
- Theme selector semantics, keyboard operation, accessible name, focus, and announcements.
- Addition and deprecation procedure.

Do not require themes to share literal values or visual mood. Require the same semantic coverage, component capability, and accessibility guarantees.

## Consistency matrices

### Contextual spacing taxonomy

Inventory both tokens and usage rules for:

- Page block and inline padding.
- Shell and content gutters.
- Header-to-content and heading-to-description spacing.
- Section separation.
- Card block and inline padding.
- Form, field, label, help, and validation spacing.
- List, row, table, grid, and toolbar spacing.
- Control internal padding and icon gaps.
- Dialog, drawer, popover, menu, and tooltip spacing.
- Empty, loading, error, and recovery composition.
- Responsive and conditional-element adjustments.

The goal is a small vocabulary of intentional contextual recipes, not one universal spacing value.

### Component matrix

Use rows for components or stable variants and columns for:

- Primitive source and owner.
- Sizes and dimensions.
- Typography.
- Spacing.
- Border and radius.
- Icon rules.
- Default, hover, focus, active, selected, disabled, loading, invalid, success, warning, destructive, and read-only states.
- Responsive behavior.
- Theme coverage.
- Accessibility evidence.
- Known drift and planned enforcement.

Classify absent states `NOT APPLICABLE` only with a concrete reason.

### Typography and layout

Check role hierarchy rather than only numeric equality. Confirm semantic headings, readable line length, text reflow, user text-spacing overrides, truncation affordances, numeric alignment, localization, right-to-left behavior where supported, and layout survival under long content.

### Geometry and motion

Define role-based border widths and radii, elevation and z-index ladders, icon sizes and strokes, motion purposes, durations, easing, interruption behavior, and reduced-motion alternatives. Flag values that are individually tokenized but used for the wrong role.

## Craft and direction evidence

Use contextual judgment, then make it inspectable and enforceable.

### Design read

Record product, audience, primary job, personality, density, layout posture, material or imagery posture, and motion posture. Mark each statement `EVIDENCE`, `ASSUMPTION`, or `USER DECISION`, with its source. A reference product is evidence for a quality or relationship, not permission to copy its surface treatment.

### Preservation and change budget

Classify identity-bearing elements and workflows as `PRESERVE`, coherent underdeveloped patterns as `STRENGTHEN`, verified debt as `REPLACE`, and material product or brand changes as `CONFIRM FIRST`. Cite the approved source or runtime evidence behind each classification.

### Craft matrix

For hierarchy, composition, typography, content authenticity, imagery, materiality, interaction feedback, coherence, responsive behavior, localization, and strategic omissions, record the intended quality, evidence, representative routes/states/themes/content, current status, user impact, system landing point, runtime verification, and remaining uncertainty.

### Anti-default method

Do not use a static “AI slop” ban list as findings. Test whether a pattern is repeated without intent, conflicts with the design read, harms comprehension or credibility, or erases product identity. Include counterevidence: when the familiar pattern improves learnability, density, accessibility, or task speed, preserve it.

### Direction-to-system bridge

No approved direction is complete until its qualities map to the design architecture. For example, “calm and precise” must become concrete semantic roles, typography and spacing recipes, component-state behavior, motion posture, asset rules, and verification—not ad hoc muted colors or longer transitions in individual components.

## Accessibility and contrast

Use current WCAG 2.2 Level AA as the minimum conformance target for web applications. Report stronger product standards separately.

### Contrast procedure

For each material pair:

1. Resolve primitive, semantic, component, and theme aliases.
2. Determine the actual bottom-to-top background layer order.
3. Convert each sRGB channel to linear light and alpha-composite layers.
4. Composite a translucent foreground over the final background when necessary.
5. Calculate `(lighter luminance + 0.05) / (darker luminance + 0.05)`.
6. Compare with the criterion appropriate to normal text, large text, or non-text UI.
7. Record token names, final colors, ratio, threshold, theme, component, state, evidence, and outcome.

Do not calculate a translucent token against an assumed white or black background unless that is the proven rendered stack. Gradients, images, video, blur, blend modes, and unknown inherited opacity require representative rendered sampling or an `UNVERIFIED` result.

The bundled contrast script accepts explicit solid and alpha layer models. It does not inspect the DOM or prove the modeled stack matches reality.

### Interaction review

Manually verify keyboard reachability, logical order, visible focus, no focus obstruction, focus restoration, escape and dismissal, labels, descriptions, error association, live status, pointer cancellation, hover/focus content, reduced motion, zoom, reflow, orientation, and target usability. Automated scans complement but do not replace this review.

Prefer 44 by 44 CSS pixel touch targets as a product standard. If the audited product intentionally uses denser controls, distinguish WCAG's minimum and exceptions from the stronger product preference and document the justification.

## Enforcement selection

Choose the smallest reliable mechanism:

| Invariant | Preferred layer | Notes |
|---|---|---|
| Raw CSS colors or forbidden property/value pairs | Stylelint | Exclude canonical token declarations narrowly. |
| Unknown CSS custom properties | Stylelint | Provide reference token files where supported. |
| JSX inline design literals | OXLint or ESLint rule | Permit proven dynamic geometry separately. |
| Forbidden Tailwind arbitrary design values | JS lint rule or scanner | Parse class composition used by the repository. |
| Shared primitive bypass | JS lint rule, type API, or dependency boundary | Avoid regex when component identity matters. |
| Missing variant or state | Component contract test | Test behavior and rendered classes or styles. |
| Missing theme token | Token schema checker | Fail on incomplete semantic mappings. |
| Theme contrast | Contrast matrix plus rendered tests | Evaluate all supported themes and states. |
| Contextual spacing | Component API, visual tests, targeted custom checker | Static lint alone rarely understands layout role. |
| Keyboard and semantics | Component/browser tests plus manual review | Automated evidence is partial. |
| Visual drift | Screenshot or visual regression | Stabilize fonts, data, motion, and viewport. |

### OXLint versus ESLint

Inspect installed versions and plugin compatibility. Prefer the established repository linter when it can express and test the rule. OXLint supports JavaScript plugins with an ESLint-compatible API, but verify current limitations and stability before recommending custom rules. Retain ESLint for rules or processors OXLint cannot safely run rather than forcing a premature replacement.

### Custom tool contract

Every proposed custom checker must define:

- Invariant and rationale.
- Inputs, file types, parser, and generated-file policy.
- Detection and resolution algorithm.
- Configuration and sanctioned source files.
- Violation message with remediation guidance.
- Narrow exception format.
- Fixtures for valid, invalid, boundary, alias, theme, generated, and false-positive cases.
- Exit codes, deterministic output, performance budget, CI command, owner, and versioning.
- Known false positives and false negatives.

Prefer AST or framework-native parsing for semantic rules. Use regex only for candidate inventory or syntax with a demonstrably bounded grammar.

### Rollout

Plan a ratchet when legacy violations are numerous: establish measured baseline; prevent new violations; migrate by vertical slice; reduce baseline monotonically; remove baseline and temporary exceptions. Never call a permanent unowned baseline the final state.

## Documentation contracts

### Style guide

Require product philosophy, source-of-truth paths, token layers and naming, theme architecture, surface nesting, typography, contextual spacing, layout, geometry, elevation, icons, motion, component recipes and states, responsive and localization behavior, accessibility, prohibited patterns, commands, exceptions, and contributor checklist. Include real application examples and exact sanctioned values or token names.

### AGENTS.md

Add or strengthen instructions in the file whose scope owns UI work. Require reading the guide, using semantic tokens and primitives, covering states, running gates, inspecting rendered changes across relevant themes and viewports, documenting exceptions, and updating the guide for new reusable rules. Preserve unrelated user instructions and avoid duplicate blocks.

### README

Add concise links to the style guide, applicable AGENTS instructions, token and component source of truth, and required commands. State strict adherence without duplicating detailed rules.

## Artifact schemas

### DESIGN-AUDIT.md

Include product intent, scope, methodology, evidence coverage, verified strengths, contradictions, prioritized findings, unverified checks, and recommended order.

### CRAFT-MATRIX.md

Include the design read, evidence and assumption labels, preservation and change budget, craft-dimension matrix, anti-default findings and counterevidence, system landing points, runtime coverage, and unverified feel checks.

### VISUAL-DIRECTION.md

When direction is absent, contradictory, or materially changing, include the selected direction, rejected alternatives, approval provenance, identity qualities, hierarchy, composition, typography, content, imagery, material and motion posture, semantic system mapping, preservation rules, prohibited shortcuts, and validation criteria.

### TOKEN-INVENTORY.md

Include source locations, architecture, normalized inventory, alias graph, usage and dead tokens, raw and arbitrary values, semantic gaps, theme readiness, multi-theme completeness when applicable, and recommendations.

### COMPONENT-MATRIX.md

Include inventory and ownership, size and variant matrix, state matrix, contextual spacing, typography and geometry, responsive behavior, theme parity, accessibility, and drift.

### ACCESSIBILITY-MATRIX.md

Include conformance target, sampled journeys, text and non-text contrast, theme/state matrix, keyboard and focus, semantics, targets, zoom/reflow/text spacing, motion, automation, manual evidence, and unverified gaps.

### ENFORCEMENT-STRATEGY.md

Include current tools, rule catalog, rule-to-layer mapping, proposed configuration, custom contracts, exception governance, baseline and rollout, CI gates, ownership, and removal criteria.

### STYLE-GUIDE-SPEC.md

Include current-guide disposition, product philosophy, required sections, exact rules and examples, source-of-truth paths, prohibited patterns, commands, exception process, migration notes, and done criteria.

### MULTI-THEME-SPEC.md

When applicable include product intent, theme catalog, semantic contract, mappings, surfaces and elevation, component/state parity, contrast, assets and integrations, selection and persistence, SSR and hydration, accessible switcher, tests, enforcement, rollout, fallback, and “Done when …” criteria.

## Finding format

```md
## DESIGN-001 — Button sizes diverge outside the shared primitive

- Severity: HIGH
- Status: VERIFIED
- Dimension: Component geometry
- Evidence: `src/features/export/ExportButton.tsx:41`
- Expected rule: Primary compact actions use the shared medium button variant.
- Observed behavior: The feature defines independent size and state classes.
- Scope: Export page and two related dialogs.
- User impact: Equivalent actions have inconsistent targets and visual weight.
- Recommendation: Add the required variant to the shared button and migrate callers.
- Enforcement: A repository-compatible JSX rule rejects design-bearing overrides.
- Done when: Equivalent actions render through the variant and invalid fixtures fail.
- Verification: Component test, lint fixture, and representative visual comparison.
```

Severity:

- `CRITICAL` — blocks essential use, creates serious accessibility exclusion, or makes critical meaning inaccessible.
- `HIGH` — systemic inconsistency, inaccessible common interaction, absent source of truth, or easy recurring bypass.
- `MEDIUM` — bounded drift, incomplete states, documentation gap, or weak enforcement.
- `LOW` — cleanup, clarity, or defense-in-depth.

## Current primary sources

Consult current official sources applicable to the detected stack and record access date and versions:

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WCAG understanding documents: https://www.w3.org/WAI/WCAG22/Understanding/
- WAI contrast guidance: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- WAI non-text contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- WAI focus appearance: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- WAI text spacing: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- WAI target size: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- OXLint documentation: https://oxc.rs/docs/guide/usage/linter
- OXLint JavaScript plugins: https://oxc.rs/docs/guide/usage/linter/js-plugins
- ESLint custom rules: https://eslint.org/docs/latest/extend/custom-rules
- Stylelint rules: https://stylelint.io/user-guide/rules/
- Tailwind theme variables: https://tailwindcss.com/docs/theme
- Playwright accessibility testing: https://playwright.dev/docs/accessibility-testing
- Storybook UI testing: https://storybook.js.org/docs/writing-tests
- Taste Skill by Leonxlnx (inspiration for brief inference, anti-default analysis, and redesign preservation): https://github.com/Leonxlnx/taste-skill
- Emil Kowalski's design engineering skills (inspiration for motion judgment and perceptual review): https://github.com/emilkowalski/skills

Prefer official framework, browser, standards, and tool documentation for additional capabilities. Clearly label inferences and do not treat automated tooling as a conformance certification.
