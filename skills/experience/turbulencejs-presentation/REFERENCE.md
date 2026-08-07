# TurbulenceJS presentation reference

## Inspect before interviewing

Prefer evidence over questions. Read project instructions, `package.json`, design tokens, routes, presentation code, tests, and source documents. Inventory local assets with dimensions and provenance. Identify whether TurbulenceJS is already installed and which public entrypoints exist. The included inspector reports repository facts but does not replace source reading.

Interview only for decisions that remain open:

- purpose, decision or feeling the deck should create;
- audience mix and prior knowledge, without assigning a rigid lane;
- authoritative content, sources, citations, and non-negotiable claims;
- target duration or useful slide range and acceptable density;
- visual character, animation character, examples, and disliked patterns;
- brand palette, typography, logos, imagery, code, charts, and provenance;
- primary delivery context, both aspect ratios, controls, export or recording;
- reduced motion, flashing, vestibular, reading, language, and accessibility needs.

## Semantic deck model

Keep the model independent from DOM markup. At minimum each slide should declare:

```js
{
  id: 'stable-kebab-id',
  claim: 'One sentence the audience should retain.',
  title: 'Selectable title text',
  body: 'Selectable supporting copy',
  layout: 'named-layout-role',
  motion: 'named-motion-role',
  logicalMotion: 'toward-reading-flow',
  intensity: 2,
  contentBudget: { maxTitleWords: 8, maxBodyWords: 32, minBodyPx: 18 },
  assets: [{ path, provenance, focalPoint, fit }],
  notes: [],
  sources: []
}
```

Layout roles should declare distinct `landscape` and `portrait` recipes, safe areas, title-line limits, stacking behavior, and focal-point rules. Validate stable unique IDs, one claim, known role references, intensity bounds, content budgets, asset provenance, and source arrays before rendering.

## Narrative planning

Use an arc, not a feature inventory. A useful default for an eight-to-twelve-slide product or technical story is:

1. promise or tension;
2. concrete problem;
3. conceptual model;
4. evidence or inspectable example;
5. meaningful contrast;
6. responsive/aspect proof;
7. composition or recipe;
8. diagnostics or trust;
9. accessibility and resilience;
10. memorable close or next action.

Change the arc to fit the content. Each slide needs a single claim and a job in the argument. Put detailed citations and speaker context in notes when showing them would weaken hierarchy.

## Content budgets

Budgets are measurable constraints, not aesthetic guesses. Declare title word and rendered-line limits, body word counts, minimum text sizes, maximum code lines, chart labels, and evidence items per layout role. Check actual rendered geometry at canonical viewports. If a title wraps beyond its budget, rewrite it before shrinking it.

## Accessibility and interaction

- Use a heading hierarchy, landmarks, buttons, and live announcements.
- Exactly one slide is active. Inactive slides are `hidden`, `aria-hidden="true"`, and inert.
- Preserve focus when keyboard navigation changes the slide. Provide a skip link and visible focus state.
- Ensure normal text reaches WCAG AA contrast and do not rely on color alone.
- Avoid timed auto-advance by default. If present, make it user-controlled.
- A reduced endpoint communicates the same state without gratuitous travel or staging.

## Runtime and export

Keep URL state stable: aspect, reduced-motion override, export flag, and slide ID. Navigation should stop old owned work before starting new work. Publish diagnostics such as active controller count, active owned work, active slide count, and destroyed state.

Export mode should:

1. hide controls and non-slide chrome;
2. load the requested URL state;
3. wait for `document.fonts.ready` and declared assets;
4. resolve normal or reduced motion to a deterministic endpoint;
5. expose a machine-readable `data-capture-ready="true"` signal;
6. capture at an exact viewport rather than approximating an aspect ratio.

## Verification matrix

For every slide, exercise:

| Viewport | Motion |
| --- | --- |
| 1920×1080 | full |
| 1920×1080 | reduced |
| 1080×1920 | full |
| 1080×1920 | reduced |

Machine evidence should include bounds/overflow, title/body budgets, active/inactive semantics, URL restoration, focus, readiness, console, diagnostics, and cleanup. Visual evidence should include full-size slide captures in both aspects, inspected for hierarchy, rhythm, legibility, focal points, awkward empty space, accidental crops, and whether the same claim survives recomposition.

## TurbulenceJS selection

- root: authored tracks, sequences, lifecycle ownership;
- `/subtle`: frequent or restrained reveals;
- `/cinematic`: editorial depth and meaningful staged entrances;
- `/cartoon`: one deliberate playful contrast when the direction supports it;
- `/effects` and `/surfaces`: rare pixel-level proof with origin, CSP, worker, memory, and cleanup checks.

Prefer a small semantic motion vocabulary over unique per-slide choreography. Map roles such as `quiet`, `explain`, `contrast`, `proof`, and `climax` to public entrypoints. Keep the ceiling explicit and never let a style guide override reduced-motion requirements.

## Style file discovery

Built-ins live beside this reference in `styles/*.json`; `style.schema.json` describes the contract. Project-local styles live at `{project}/.turbulencejs/presentation-styles/*.json` and override a built-in with the same `id`. This precedence is local to discovery. Never write or promote a style without an explicit request.

Use:

```sh
node {skill-folder}/scripts/list-styles.mjs --project {target-root}
node {skill-folder}/scripts/validate-styles.mjs --project {target-root}
node {skill-folder}/scripts/validate-deck.mjs {deck.json}
```
