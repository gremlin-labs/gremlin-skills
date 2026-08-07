# Motion Direction reference

## Contents

- [Evidence and disposition](#evidence-and-disposition)
- [Direction quality test](#direction-quality-test)
- [Delight tiers](#delight-tiers)
- [Category coverage](#category-coverage)
- [Policy schemas](#policy-schemas)
- [Capability gaps](#capability-gaps)
- [Handoff readiness](#handoff-readiness)

## Evidence and disposition

- `EVIDENCE` — current product, code, runtime, public package, or approved artifact supports the claim.
- `ASSUMPTION` — a reversible hypothesis with owner and validation experiment.
- `USER DECISION` — an explicit product or creative choice.
- `SIMULATED` — a Studio approximation demonstrates intended feel but not exact runtime behavior.
- `PUBLIC-RUNTIME` — the preview or inspected target executes a verified public TurbulenceJS capability.
- `UNVERIFIED` — exact public capability, runtime feel, device behavior, or measurement remains unknown.
- `NOT APPLICABLE` — the category is absent or irrelevant, with reason.

Never convert `SIMULATED` into an API or performance claim. Never call an uninspected package export unsupported.

## Direction quality test

A direction is coherent only when it defines one relationship among product intent, interaction frequency, spatial model, rhythm, choreography, and delight. A direction is distinct from its peers only when at least three consequential relationships change:

1. response rhythm or asymmetry;
2. spatial model, origin, path, or depth;
3. transition choreography or sequencing;
4. material/effect vocabulary;
5. delight placement and escalation.

Duration, easing, palette, or intensity changes over the same system are variants, not directions.

For each option record:

| Dimension | Required evidence |
| --- | --- |
| Product fit | User/job/emotion rationale and invalidation signal |
| Frequency | Continuous, frequent, occasional, and rare posture |
| Spatial model | Origins, paths, continuity, depth, and responsive behavior |
| Rhythm | Response, duration, asymmetry, sequencing, and interruption |
| Turbulence vocabulary | Public family hypotheses, intensity ceiling, and verification status |
| Delight | Essential, Expressive, and Signature allocation |
| Access and input | Reduced endpoint, focus, keyboard, pointer, and touch behavior |
| Performance/lifecycle | Resource limits, ownership, teardown, and settled state |
| Migration | Existing ownership, replaced schedulers, rollout, and rollback |
| Experiment | Cheapest preview or runtime evidence that could reject the option |

## Delight tiers

### Essential

Use for immediate acknowledgement, selection, focus-supporting state, continuity, and frequent interactions. Prioritize response and meaning. Reduced behavior is often instant or near-instant but must keep state legible.

### Expressive

Use for occasional navigation, overlays, route changes, progress, success, and explanatory transitions. Give the product a recognizable rhythm and spatial model without making repetition tiring.

### Signature

Use for rare moments worth remembering: onboarding resolution, first success, milestone, celebration, dramatic reveal, or product-specific transformation. Require explicit trigger frequency, intensity ceiling, fallback, reduced endpoint, performance/resource budget, interruption policy, cleanup, and approval.

Tiers are not global intensity modes. A component recipe owns its default tier and allowed escalation. A Signature recipe cannot become a site-wide theme toggle.

## Category coverage

Classify every category `APPLICABLE`, `NOT APPLICABLE`, or `UNVERIFIED` in `COMPONENT-MOTION-MATRIX.md`:

- `page-load`
- `route-transition`
- `navigation`
- `menu`
- `sidebar-drawer`
- `overlay-dialog`
- `tooltip-popover`
- `tabs-accordion`
- `controls`
- `form-validation`
- `list-table-card`
- `direct-manipulation`
- `skeleton`
- `spinner`
- `loading-progress`
- `empty-error-recovery`
- `toast-notification`
- `onboarding-celebration`

Add product-specific categories when required. Do not mark a category applicable merely to fill the matrix.

For every applicable category specify purpose, trigger, frequency, tier, semantic role, origin/path, public Turbulence family, ownership, interruption/cancellation, reduced endpoint, input/focus behavior, performance/resource budget, cleanup, evidence, and verification status.

## Policy schemas

### RESEARCH.md

Include product and emotional intent, users/journey, current visual direction, stack/public versions, representative page/component/state inventory, interaction frequency, accessibility, performance, delivery constraints, preservation rules, alternatives, and unknowns.

### DIRECTION-OPTIONS.md

Include motion read, option comparison, detailed options, recommendation, rejected blends, validation experiments, append-only preview revisions, user feedback, selected option/revision, and approval provenance.

### MOTION-LANGUAGE.md

Include selected direction, product outcome, emotional qualities, spatial model, rhythm, choreography, Turbulence vocabulary, delight posture, preservation/change budget, prohibited character, reduced/input posture, lifecycle/resource posture, and approved preview evidence.

### ANIMATION-POLICY.md

Include principles and emotional intent, spatial model and rhythm, delight tiers, semantic roles and tokens, page/component recipes, interruption and lifecycle, reduced motion and input, performance/resource budgets, prohibited patterns, exceptions, new-component decision tree, target-project agent/contributor guidance, enforcement/verification, rollout/rollback, and approval.

The new-component decision tree answers:

1. What state or relationship changes?
2. Does motion improve feedback, continuity, explanation, progress, or rare delight?
3. What is the interaction frequency and attention cost?
4. Which semantic role and default tier own it?
5. Which public Turbulence family is verified for the target?
6. How does it interrupt, retarget, reduce, and clean up?
7. Which mechanical and perceptual evidence proves it?
8. Does it require an exception or public capability gap?

### ENFORCEMENT-STRATEGY.md

Map each policy rule to documentation, semantic APIs, tokens, component recipes, static checks, types, unit/component/browser tests, a dedicated runtime fixture, visual/perceptual review, performance/lifecycle diagnostics, CI, ownership, and governed exceptions. Do not propose a linter for a rule that only runtime perception can prove.

## Capability gaps

Verify the installed package or current public documentation first. `CAPABILITY-GAPS.md` may contain:

- desired user-visible behavior;
- public capability checked and evidence date/version;
- current limitation and affected surfaces;
- product impact and approved-direction impact;
- supported fallback and deviation;
- acceptance evidence for the desired outcome;
- Planpro routing status when architecture remains unresolved.

It must not contain maintainer workflow, internal repository paths, source modules, proposed internal architecture, private APIs, release steps, or contribution guidance.

## Handoff readiness

Use Goalpro only when all are true:

- the selected option and preview revision are explicitly approved;
- application targets and migration ownership are concrete;
- required Turbulence capabilities are publicly verified or approved fallbacks preserve intent;
- acceptance criteria, project gates, perceptual checks, rollout, rollback, and manual actions are complete;
- no material architecture or cross-repository decision remains.

Use Planpro when any material implementation architecture, sequencing, dependency, or capability decision remains. Leave the package terminal when the user wants policy only.
