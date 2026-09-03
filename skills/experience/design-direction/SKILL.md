---
name: design-direction
description: Defines and documents an evidence-backed visual and interaction direction for a new product, major new surface, or intentional redesign before implementation. Use when the user asks to art-direct an interface, establish a visual language, explore distinct design directions, avoid generic AI aesthetics in a greenfield UI, turn brand and product intent into a theme-ready design-system map, or when visitor success (persuade, operate, read, or experience) should change the visual logic; do not use for auditing an existing implemented system, ordinary feature planning, image-only generation, scoped amplify/quiet/distill of shipped UI, or source implementation.
---

# Design Direction

Turn product intent into an approved visual language and semantic system map under `agent-work/{slug}/design-direction/`. Remain read-only outside that folder. Hand implementation to Planpro or Goalpro with the same slug.

Resolve the owning work root and maintain the slug index using [the canonical work-artifact contract](contracts/work-artifacts.md).

## Decision tree

```dot
digraph design_direction {
  start [shape=doublecircle, label="Visual direction requested"];
  intent [shape=box, label="Research product, users,\nbrand, and constraints"];
  clarity [shape=diamond, label="Material intent\nclear enough?"];
  ask [shape=box, label="Ask one focused\nproduct question"];
  read [shape=box, label="State evidence-labeled\ndesign read and visitor mode"];
  options [shape=box, label="Develop 2-3 distinct\nanti-convergent options"];
  inventory [shape=box, label="Inventory representative\ncomponents and states"];
  preview [shape=box, label="Build complete interactive\nHTML comparison"];
  choose [shape=diamond, label="User response?"];
  refine [shape=box, label="Apply requested tweaks\nand regenerate preview"];
  regenerate [shape=box, label="Record rejected set and\ncreate new directions"];
  map [shape=box, label="Write direction contract\nand semantic system map"];
  ready [shape=diamond, label="Implementation scope\nalready concrete?"];
  goalpro [shape=doublecircle, label="Approved Goalpro handoff"];
  planpro [shape=doublecircle, label="Planpro handoff"];
  deliver [shape=doublecircle, label="Deliver direction package"];

  start -> intent;
  intent -> clarity;
  clarity -> ask [label="no"];
  ask -> read;
  clarity -> read [label="yes"];
  read -> options;
  options -> inventory;
  inventory -> preview;
  preview -> choose;
  choose -> refine [label="refine"];
  refine -> preview;
  choose -> regenerate [label="none fit"];
  regenerate -> options;
  choose -> map [label="approve"];
  map -> ready;
  ready -> goalpro [label="yes + approved"];
  ready -> planpro [label="no"];
  ready -> deliver [label="direction only"];
}
```

## Boundaries

- Remain read-only on application source, configuration, manifests, docs, external services, and deployed environments.
- Write only under `agent-work/{slug}/design-direction/` plus the shared `WORK.md`.
- Do not generate images. Write an optional reference-board specification that an image-generation skill can consume.
- A self-contained HTML direction preview is a planning artifact, not application implementation. It may reproduce representative UI structure only inside `agent-work/{slug}/design-direction/`; never copy it into product source or present it as production-ready code.
- Do not audit an existing design system comprehensively; use Designpro for implemented-system drift and enforcement.
- Do not implement the direction. Goalpro owns mutations after approval; Planpro owns unresolved implementation architecture.
- Never turn a reference product into a copying instruction or invent brand intent from fashion.

## 1. Establish intent

Apply [Planpro's product-research lens](contracts/product-research.md). Read product, brand, audience, workflow, content, accessibility, platform, device, localization, theme, performance, and delivery evidence. Identify the job, emotion, trust posture, information density, existing identity assets, and qualities that must be preserved.

Write a one-line **design read** covering product, audience, job, personality, density, layout, material or imagery, and motion. Classify **visitor mode** from the requested surface, not the product: `Persuade` (decide and act), `Operate` (complete a task), `Read` (understand), or `Experience` (the work itself leads). A tool's landing page is still Persuade; documentation is still Read; settings are Operate. Mark every statement `EVIDENCE`, `ASSUMPTION`, or `USER DECISION`. Persist the mode in `RESEARCH.md` and every option. Ask one focused question only when a material direction cannot be discovered safely. Mode changes type, color, motion, and critique posture — see [REFERENCE.md](REFERENCE.md). Do not treat an Operate surface as failed Persuade.

## 2. Develop distinct options

Before writing options, record the **anti-convergence setup** in `DIRECTION-OPTIONS.md`:

1. **Category rut** — one sentence naming the page this category always ships and its predictable opposite; keep both out of the option list.
2. **Color strategy** — choose Restrained, Committed, Full palette, or Drenched before picking colors. Operate and Read default to Restrained; Persuade and Experience may take the bolder strategies when the brief allows.
3. **Habit-face self-check** — choose faces from the subject's world. Naming a listed habit face in [REFERENCE.md](REFERENCE.md) requires a reason no other face could satisfy; a subject association is never that reason.
4. **AI-cluster self-check** — if someone could guess the aesthetic from the category alone, or the options land on cream+serif+terracotta, near-black+neon, or broadsheet hairline+italic serif+tracked mono without a unique product reason, rewrite them.

Create two or three directions that differ in design logic, not merely palette or intensity. Each option must specify:

- Product rationale and intended user response.
- Hierarchy, composition, density, typography, imagery, material, iconography, content voice, and motion posture.
- Accessibility, localization, responsive, theme, performance, and implementation implications.
- What it preserves, what it changes, failure modes, reversibility, and a cheap validation experiment.
- Visitor mode, color strategy, and the category rut it refuses.
- Anti-default choices justified by product fit, plus familiar patterns deliberately retained for learnability or task speed. Amplify or quiet may be option *axes* only when hierarchy, composition, or material also change; “same layout but bolder” is not a distinct direction.

Recommend one option with evidence, but do not ask for selection until the interactive preview is complete and validated. Do not silently blend incompatible options.

Research and option artifacts may be written before selection so the decision is durable. Do not finalize `VISUAL-LANGUAGE.md`, `DIRECTION-CONTRACT.md`, `SYSTEM-MAP.md`, `PLAN.md`, or `GOALPRO-INPUT.md` until the user selects a direction. When the only evidence is the user's brief, a recommendation may still be useful, but label it provisional, expose every material assumption, and propose the cheapest validation experiment; do not present it as researched product truth.

## 3. Build the interactive direction preview

For every non-trivial visual-direction decision, create `DIRECTION-PREVIEW.html` before asking the user to choose. “Non-trivial” includes two or more options, a whole-product or major-surface reskin, a material typography/layout/theme change, or any decision whose quality cannot be judged responsibly from prose alone.

Inventory the target project's real components, surfaces, states, content density, and route patterns first, and preserve that inventory in `RESEARCH.md` under `Representative component and state inventory`. The preview must visualize the most representative set available: application shell/navigation; typography hierarchy; palette and semantic roles; nested surfaces; buttons and links; inputs and validation; cards or equivalent groupings; tables/lists/timelines/charts where present; status, loading, empty, error, disabled, and success states; responsive behavior; and motion posture. When no implementation exists, label inferred components and derive them from the proposed experience matrix.

Place all directions in one self-contained, responsive HTML file with an accessible keyboard-operable switcher. Use no remote scripts, stylesheets, fonts, or tracking. Include normal and reduced-motion behavior, representative realistic content, palette swatches, token-role labels, and a concise rationale/tradeoff panel. Each `direction-summary` must show visitor mode, color strategy, and the rut it refuses. The first viewport of the representative slice is a thesis — the product mechanism at scale — not a generic hero. In tradeoffs, note whether a copy-stripped skeleton still communicates the section's job. When themes are relevant, include light/dark or alternative family selectors that preserve the same semantic capabilities rather than showing palette-only recolors.

Read [PREVIEW.md](PREVIEW.md) completely before generating the preview. Run `python3 {design-direction-skill-root}/scripts/validate_direction_preview.py agent-work/{slug}/design-direction/DIRECTION-PREVIEW.html` and fix every failure before presenting it.

## 4. Iterate until the user loves a direction

After presenting the preview, accept one of three outcomes:

1. **Refine** — apply concrete feedback to one or more options, increment the preview revision, preserve unaffected distinctions, regenerate the HTML, validate it, and present it again.
2. **New set** — record the complete option set as rejected with the user's reasons, then create two or three genuinely new directions. Do not disguise palette swaps or renamed blends as new concepts.
3. **Approve** — record the selected direction and preview revision, then proceed to system mapping.

Maintain an append-only revision table in `DIRECTION-OPTIONS.md` with revision, options shown, feedback, disposition, and immutable snapshot path. Save each validated revision at `previews/DIRECTION-PREVIEW-R{n}.html`, then copy the current revision to `DIRECTION-PREVIEW.html` as the stable latest alias. Never pressure the user to choose the recommended option. Do not finalize system mapping or execution handoff while the user is still refining or while every option is rejected.

For theme-heavy products or users, consult the independently discovered `theme-library` skill in embedded mode. Treat its families as creative seeds: preserve palette DNA while freely evolving ramps, surfaces, borders, neutrals, statuses, complementary/contrasting colors, and mode-specific relationships for the selected direction. Use exact fidelity only when the user requests it. Record the interpretation and additions in `PALETTE-SHORTLIST.md`, then make them visible in the HTML preview. Never require an external repository or local filesystem path to access a palette.

## 5. Map the selected direction into a system

Translate qualities into:

- Primitive foundations and component-facing semantic roles.
- Typography, spacing, layout, geometry, elevation, imagery, icon, content, and motion roles.
- Component recipes and state behavior without theme-name branches.
- Theme-ready mappings, complete semantic parity, and accessible fallbacks.
- Asset/content rules, prohibited shortcuts, governed exceptions, and contributor guidance.
- Mechanical and rendered verification criteria.

The map specifies roles and relationships. Avoid inventing exact values without evidence; mark experiments and user decisions explicitly.

Write `DIRECTION-CONTRACT.md` in the same step: six short blocks, 150 words at most.

- **Thesis** — the one idea this surface owns and the category default it refuses.
- **Own-world** — palette and component language recognizable with content removed.
- **Story** — what the visitor understands, believes, and does.
- **First viewport** — exact composition, scale, and where the primary action sits.
- **Form** — the chosen form and its position on the option list.
- **Finish** — this contract is what Design Review audits; unreviewed implementation is unfinished.

If a block reads like a mood, the direction is not decided. Never copy the contract into product source or any browser-delivered artifact.

## 6. Produce artifacts

Create:

- `RESEARCH.md` — users, product, journey, intent sources, representative component/state inventory, constraints, quality, alternatives, and unknowns.
- `DIRECTION-OPTIONS.md` — distinct options, recommendation, tradeoffs, experiments, and decision status.
- `DIRECTION-PREVIEW.html` — required self-contained interactive comparison for non-trivial direction decisions, aliasing the latest immutable `previews/DIRECTION-PREVIEW-R{n}.html` snapshot.
- `PALETTE-SHORTLIST.md` — conditional family/variant comparison when palettes or multiple themes materially shape the direction.
- `VISUAL-LANGUAGE.md` — selected direction, visitor mode, design read, preservation rules, and craft posture.
- `DIRECTION-CONTRACT.md` — compact six-block review authority after selection; do not finalize before approval.
- `SYSTEM-MAP.md` — semantic roles, token layers, recipes, themes, assets, content, motion, and enforcement targets.
- `EXPERIENCE-MATRIX.md` — routes or surfaces, states, viewports, inputs, accessibility, localization, content extremes, hardening, and intended behavior.
- `PLAN.md` — implementation slices when the direction can be planned without further architecture work.
- `GOALPRO-INPUT.md` — conditional direct handoff only when scope and criteria are concrete and approved.
- `REFERENCE-BOARD-SPEC.md` — optional image-generation brief.
- `NOTES.md` — optional sanitized decisions or sources.

Follow [REFERENCE.md](REFERENCE.md) for schemas, option tests, and handoff selection.

## Handoff

- Use Planpro when feature scope, architecture, data, or delivery remains unresolved.
- Use Goalpro only when the selected direction and implementation scope have explicit approval and the direct handoff satisfies [Goalpro's contract](contracts/goalpro-handoff.md).
- Leave the direction package terminal when the user wants design guidance only.

## Done

Finish when evidence and assumptions are separated; visitor mode is classified from the surface; options are genuinely distinct, anti-convergent, and visually compared in a validated HTML preview; requested refinements or rejected sets are durably recorded; the selected preview revision has explicit user approval; the direction contract is complete and under 150 words; every quality maps to semantic roles and verification; accessibility, localization, states, themes, and performance are classified; implementation shortcuts are prohibited; and the correct handoff is ready without rediscovering direction.

State: “I am satisfied this design direction is complete because …” and cite the selection, visitor mode, direction contract, system map, and unresolved decisions.


## Optional shared Theme Library

When the request contains a material named-theme or palette decision, discover the independently installed `theme-library` skill through the host skill registry. If the host has no registry, resolve `theme-library/SKILL.md` as a sibling of this skill directory (the standard relative location is `../theme-library/SKILL.md`). If found, read it and use embedded mode while keeping artifacts in this skill's stage. If it is not installed, continue the primary workflow and disclose the unavailable palette library only when it materially limits the result. Never rely on repository-level AGENTS or README files for discovery.
