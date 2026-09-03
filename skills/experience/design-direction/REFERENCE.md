# Design Direction Reference

## Contents

- [Evidence statuses](#evidence-statuses)
- [Option quality test](#option-quality-test)
- [Interactive preview](#interactive-preview)
- [Iteration and selection](#iteration-and-selection)
- [System map](#system-map)
- [Experience matrix](#experience-matrix)
- [Artifact schemas](#artifact-schemas)
- [Attribution and references](#attribution-and-references)

## Evidence statuses

- `EVIDENCE` — supported by current product, brand, research, code, or approved decisions.
- `ASSUMPTION` — low-risk working hypothesis with owner and validation.
- `USER DECISION` — material direction choice that cannot be inferred.
- `EXPERIMENT` — cheapest prototype, reference comparison, or user test that reduces uncertainty.
- `NOT APPLICABLE` — demonstrably irrelevant, with reason.

## Visitor modes

Classify from the requested surface. Persist the mode; do not treat Operate as failed Persuade.

| Mode | Visitor success | Default craft posture |
|---|---|---|
| Persuade | Decides and acts | Design is the product. Color may be Committed, Full, or Drenched. Display type may carry voice. One authored first-viewport moment. |
| Operate | Completes a task | Restrained color. One workhorse family and a fixed rem scale are often right. Motion is 150–250ms state feedback, not page-load choreography. Familiar affordances outrank expression. |
| Read | Understands something | Restrained color. Measure, hierarchy, and wayfinding first. System or workhorse faces are acceptable. |
| Experience | Is inside the work | The artifact leads; chrome recedes. Bolder color and display type are permitted when the brief allows. |

## Anti-convergence

Record before options:

- **Category rut** and its predictable opposite — both stay off the option list.
- **Color strategy** before hex values: Restrained (neutrals plus one accent), Committed (one saturated color owns 30–60% of the surface), Full palette (3–4 named roles), Drenched (the surface is the color).
- **Habit faces** that require a unique reason: Fraunces, Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk, Space Mono, IBM Plex, Inter used as display, DM Sans, DM Serif, Outfit, Plus Jakarta Sans, Instrument Sans. A book wanting a serif or tech wanting a mono is not that reason.
- **AI clusters** to refuse unless the brief uniquely earns them: warm cream ground + high-contrast serif display + terracotta/signal-red accent; near-black with one neon accent and glowing edges; broadsheet-editorial hairlines + italic display serif + small tracked mono labels.

These are generation self-checks, not review findings. Familiar patterns remain correct when they improve task speed, density, or accessibility.

## Option quality test

Options are distinct only when they change at least three consequential relationships such as hierarchy, information density, composition, typography role, imagery/material logic, interaction posture, or content voice. Palette swaps, radius swaps, and “same layout but bolder” are not distinct directions. Intensity-only amplify/quiet variants fail this test.

For each option record:

| Dimension | Required evidence |
|---|---|
| Product fit | User/job/trust rationale and guardrail |
| Hierarchy and composition | Attention order, grouping, density, responsive behavior |
| Typography and content | Roles, voice, numeric/data treatment, localization risk |
| Imagery and material | Asset logic, depth, surfaces, brand fit, performance cost |
| Interaction and motion | Feedback, spatial model, frequency, reduced-motion posture |
| System fit | Semantic roles, recipes, themes, enforcement implications |
| Risk | Accessibility, credibility, novelty, maintainability, reversibility |
| Experiment | Smallest test and invalidation signal |

## System map

Map direction to layers:

1. **Foundations:** palette families, type families, spacing/radius/elevation/motion scales as roles, not unsupported exact values.
2. **Semantic roles:** surfaces, foregrounds, borders, focus/status, content emphasis, density, layout, material, and motion purposes.
3. **Component recipes:** sanctioned combinations and states.
4. **Experience rules:** responsive, localization, content extremes, input modes, reduced motion, themes, and failure/recovery.
5. **Governance:** source paths, prohibited shortcuts, exceptions, lint/test/browser/visual evidence.

Theme direction is a semantic remapping, never component conditionals on theme names.

## Interactive preview

`DIRECTION-PREVIEW.html` is the user's primary decision surface, not a decorative mood board. Read [PREVIEW.md](PREVIEW.md) for the complete construction and validation contract.

The preview must make consequential differences visible: attention order, density, navigation model, typography roles, surface nesting, content treatment, component geometry, state behavior, palette families, theme modes, and motion posture. A direction that only changes CSS variables while keeping all relationships identical fails the option-quality test.

## Iteration and selection

Add this append-only table to `DIRECTION-OPTIONS.md`:

| Revision | Options shown | User feedback | Disposition | Preview |
|---|---|---|---|---|
| R1 | A, B, C | Increase density in B; A and C feel generic | REFINE B; REJECT A/C | `previews/DIRECTION-PREVIEW-R1.html` |
| R2 | B, D, E | None captures the product personality | REJECT SET | `previews/DIRECTION-PREVIEW-R2.html` |
| R3 | F, G, H | G approved with quieter motion | APPROVE G | `previews/DIRECTION-PREVIEW-R3.html` |

Preserve rejected concepts and reasons. A new set must change design logic across at least three consequential relationships. Approval names the option and preview revision; prose approval without a matching validated preview is incomplete for non-trivial work.

## Experience matrix

Cover every applicable combination of surface, user goal, loading/empty/error/degraded/recovery state, viewport, input, theme, localization/text expansion, reduced motion, content extreme, and accessibility behavior. When classifying localization and content extremes, also mark overflow strategy, a 30–40% translation budget, logical properties or RTL when locales require them, empty vs permission vs failure, network/offline/concurrency, and extreme string/item counts. Mark absent combinations with evidence instead of assuming them away.

## Artifact schemas

### RESEARCH.md

Include a `Visitor mode` heading with the surface classification and evidence label, then a `Representative component and state inventory` section with source path or evidence, ownership/status (`IMPLEMENTED`, `PROPOSED`, or `INFERRED`), importance, states, content extremes, responsive behavior, and whether/how each item appears in the preview.

### DIRECTION-OPTIONS.md

Include design read, visitor mode, anti-convergence setup, option comparison, detailed options, recommendation, rejected blends, experiments, append-only preview revisions, user decision, selected preview revision, and approval provenance.

### DIRECTION-PREVIEW.html

Include the complete contract in `PREVIEW.md`: accessible direction/theme controls, representative project components and states, realistic content, typography, palette roles, surfaces, responsiveness, reduced motion, rationale/tradeoffs, and embedded provenance/revision metadata. Preserve each validated revision under `previews/`; keep this root file as the latest alias.

### PALETTE-SHORTLIST.md

When applicable include product/theme intent, Theme Library family candidates, interpretation mode, identity anchors, preserve/evolve/add/avoid decisions, evolved semantic-role hypotheses, accessibility risks, rejected families, preview coverage, and selection status.

### VISUAL-LANGUAGE.md

Include selected direction, visitor mode, user outcome, identity qualities, preservation/change budget, hierarchy, composition, typography, content, imagery, materiality, interaction and motion, accessibility, responsive/localization posture, and anti-default rationale.

### DIRECTION-CONTRACT.md

After selection, write six blocks totaling 150 words or fewer: Thesis, Own-world, Story, First viewport, Form, Finish, plus Visitor mode. Finish names Design Review as the later auditor. A mood-only block means the direction is not decided. Never copy this file into product source.

### SYSTEM-MAP.md

Include source-of-truth intent, token layers, semantic roles, component recipes, themes, assets, content, motion, prohibited patterns, exception process, enforcement targets, and validation.

### PLAN.md

Use Planpro's phase rules: working vertical slices, concrete files discovered from the target, product outcome, applicable quality, exact gates, risks, open questions, and final acceptance.

## Attribution and references

This skill's brief inference, option variance, and anti-default discipline were inspired by [Taste Skill by Leonxlnx](https://github.com/Leonxlnx/taste-skill). Its motion posture also draws inspiration from [Emil Kowalski's design engineering skills](https://github.com/emilkowalski/skills). Visitor-mode craft, compact direction contracts, and anti-convergence generation were inspired by [Impeccable](https://github.com/pbakaus/impeccable). Use original, product-specific reasoning; these sources do not define universal aesthetics and do not imply endorsement.
