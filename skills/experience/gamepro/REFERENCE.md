# Gamepro Reference

Use this reference to keep Gamepro small in simple projects and rigorous where risk requires it. These are evidence shapes and decision aids, not required departments or a fixed production methodology.

## Contents

- [Artifact schemas](#artifact-schemas)
- [Milestone evidence](#milestone-evidence)
- [Six conditional lenses](#six-conditional-lenses)
- [Runtime discovery](#runtime-discovery)
- [Runtime profiles](#runtime-profiles)
- [Playtest contract](#playtest-contract)
- [Scope and placeholder rules](#scope-and-placeholder-rules)
- [Optional capability fallbacks](#optional-capability-fallbacks)
- [Release Candidate](#release-candidate)
- [Journey examples](#journey-examples)

## Artifact schemas

### GAME.md

```md
# Game: {working title}

## Intent
- Player fantasy:
- Core verb:
- Feedback promise:
- Current hypothesis:

## Mode and target
- Mode: GREENFIELD | EXISTING | SPIKE | RESUME
- Target: FIRST PLAYABLE | MVP | V1 | RELEASE CANDIDATE
- Current milestone:
- Status: ACTIVE | AWAITING USER RUNTIME | BLOCKED | COMPLETE

## Run the game
- Exact launch command or interaction:
- Expected result:
- Last observed evidence:

## Milestones
| Milestone | Status | Done when | Evidence | Next playable slice |
|---|---|---|---|---|

## Content and quality boundary
- Included for target:
- Explicitly deferred:
- Placeholder debt:

## Decisions and non-goals
| Decision | Evidence or owner | Consequence |
|---|---|---|

## Conditional lenses
| Lens | Classification | Evidence needed now |
|---|---|---|

## Next playable slice
```

Make every “Done when …” entry independently observable. Update current state in place; preserve important target and decision changes in `PROGRESS.md`.

### PROGRESS.md

```md
# Progress: {working title}

- [{timestamp}] WIP    {milestone}/{slice}: Plan — {smallest playable change and criterion}.
- [{timestamp}] DONE   {milestone}/{slice}: Do — {changed behavior}; Verify — {command and runtime/playtest evidence}; I am satisfied this step is complete because {reason}.
- [{timestamp}] BLOCKED {milestone}/{slice}: {external blocker}; resume when {specific evidence or action}.
```

Append rather than rewriting history. Log pivots, scope cuts, user observations, changed targets, flaky-gate repairs, and the first unmet criterion for resume. Do not paste large command outputs; cite the command, result, and durable log path when useful.

### QUALITY-REPORT.md

```md
# Quality report: {working title}

## Target and integrated result

## Quality dimensions
| Dimension | Status | Evidence or rationale |
|---|---|---|

## Milestone evidence
| Milestone | Runtime | Playtest | Project gates | Debt |
|---|---|---|---|---|

## Final integrated verification
- End-to-end scenario:
- Launch evidence:
- Full project gate:
- Diff and debris review:
- Remaining manual actions or waivers:
- I am satisfied this game milestone is complete because ...
```

Use final statuses `VERIFIED`, `NOT APPLICABLE`, or `WAIVED`. During execution, `UNKNOWN`, `AWAITING USER RUNTIME`, and `BLOCKED EXTERNAL` are honest interim states but cannot close the requested target.

## Milestone evidence

| Milestone | Required product evidence | Required runtime evidence | Scope posture |
|---|---|---|---|
| First Playable | Fantasy, one core verb, feedback hypothesis | Exact launch path and observed verb→feedback loop | One production-thin slice; placeholders preferred over premature breadth |
| MVP | Minimal complete start→play→resolution→restart journey | Journey plus affected invalid, error, pause/cancel, and recovery states | Only systems essential to the complete loop |
| V1 | Approved content boundary and quality bar | Integrated representative playtest plus full project gates | Complete declared scope; explicit debt only |
| Release Candidate | Approved distribution target and release-readiness boundary | Applicable package/install/launch and recovery evidence | No hidden manual step; release operations remain separate |

A higher target includes evidence from the lower milestones. It does not require separate planning documents for each milestone.

## Six conditional lenses

Classify each lens for the current slice. Expand only its applicable questions.

### 1. Player and creative intent

- Who is playing, in what context, and what should they feel or understand?
- Does the slice strengthen the fantasy and the current hypothesis?
- What is the intended best moment, and is novelty serving it?
- Which aesthetic choices are approved, inferred, provisional, or unknown?

Evidence may be direct user decisions, current game behavior, an approved brief, a small visual/audio sample, or a playtest observation. Do not require a comprehensive design document.

### 2. Mechanics and systems

- Is the verb legible, responsive, and connected to consequence?
- Are goals, rules, failure, recovery, progression, difficulty, and economy relevant now?
- Which states or interactions can create impossible, stuck, duplicate, or unfair outcomes?
- Does AI or procedural behavior remain deterministic or debuggable where it needs to?

Test invariants and transitions, not just one happy-path example. Defer systems that do not affect the current playable loop.

### 3. Technical runtime

- What engine/runtime and version does the repository actually use?
- What is the canonical launch, build, test, export, and asset-import path?
- What timing, physics, frame lifecycle, scene/state ownership, memory, or platform constraints apply?
- Can failures be diagnosed from logs, debug overlays, profiling, or reproducible seeds?

Prefer repository commands and installed declarations. Verify version-sensitive APIs from current official documentation when they affect implementation.

### 4. Experience, content, and accessibility

- Are controls discoverable and remappable where the target requires it?
- Are feedback, HUD, menus, dialogue, onboarding, pause, save/load, error, and recovery states understandable?
- Do text, contrast, focus, input alternatives, motion settings, audio cues/captions, and readable timing fit affected players and platforms?
- Are representative content, localization expansion, and content extremes exercised?

Accessibility begins at the first affected interaction; it is not a release-only polish pass.

### 5. Quality, playtest, performance, security, and privacy

- Which automated and manual checks can falsify the current hypothesis?
- What frame, memory, load, network, battery, or asset budget is actually at risk?
- Do saves, networking, user content, mods, telemetry, commerce, accounts, or external services create trust or abuse boundaries?
- Are secrets, personal data, child safety, authority, validation, rate/cost limits, moderation, offline behavior, and recovery applicable?

Do not invent performance numbers or a threat model for an offline toy. Once an online or sensitive feature exists, classify the relevant checks before building it.

### 6. Delivery and release

- What must remain compatible with existing scenes, saves, controls, mods, assets, or builds?
- Is rollout atomic, staged, reversible, or externally gated?
- What documentation, licenses, attribution, packaging, distribution configuration, or store/platform evidence applies?
- Which manual actions remain, who owns them, and what proves completion?

Release judgment may begin early, but remote release actions require their own authorization and Releasepro.

## Runtime discovery

Use this sequence before proposing tooling:

1. Read repository instructions and docs.
2. Inspect manifests, project descriptors, lockfiles, scenes, assets, source, test configuration, CI, and existing scripts.
3. Identify the established engine/runtime and its local availability.
4. Find the documented launch/build/test/export commands; prefer them over generic examples.
5. Run the cheapest trustworthy static gate, then launch and observe the current loop.
6. If multiple viable targets materially change the game, present the evidence and ask one question. Otherwise preserve the established path.

Never upgrade or install an engine merely to begin. Never replace an existing architecture with a preferred starter unless the user explicitly requests that migration.

## Runtime profiles

Profiles describe what to discover and prove. They intentionally do not pin versions or claim universal commands.

### Browser game

Discovery signals include `package.json`, lockfiles, HTML entrypoints, bundler configuration, source modules, public assets, test setup, and existing development/build scripts.

- Use the detected package manager and scripts.
- Verify type/lint/test/build gates that exist, then open the actual served route when browser control is available.
- Exercise keyboard, pointer, touch, resize, focus loss, pause/restart, reduced motion, audio permission, loading, console, and representative performance where applicable.
- If browser control is unavailable, provide the exact local command and route plus a short observation checklist.

### Godot project

Discovery signals include `project.godot`, scenes, scripts, resources, addons, import configuration, project docs, and CI/export presets.

- Preserve the project's configured renderer, input map, node/scene ownership, and script language.
- Use an available project-compatible command or editor workflow; do not assume headless gameplay proves rendered behavior.
- Verify scene loading, input, signals/state transitions, pause/restart, collision/physics behavior, logs, and affected export targets.
- When the editor or target platform is unavailable, request one exact user-run project or scene check and record returned observations.

### Unity project

Discovery signals include `ProjectSettings`, package manifests and locks, `Assets`, assemblies, scenes, test configuration, CI/build scripts, and documented editor version.

- Preserve project package, input, render-pipeline, serialization, prefab, scene, and assembly conventions.
- Use existing edit-mode/play-mode tests and batch/build automation only where the repository supports them.
- Treat compilation or a batch exit code as insufficient evidence for gameplay, visuals, physics, audio, or platform input.
- When an editor run is required, give the exact scene and playtest steps, expected result, log location if relevant, and await observed evidence.

### Unreal project

Discovery signals include a project descriptor, configuration, `Content`, `Source`, plugins, maps, automation tests, build scripts, and target/platform documentation.

- Preserve module, Blueprint/C++, asset, input, map, networking, and packaging conventions.
- Use existing automation and build paths; verify affected map/mode startup and runtime behavior separately.
- Treat successful compilation or asset discovery as insufficient evidence for play-in-editor, packaged behavior, replication, performance, or platform input.
- If the editor or target cannot run, ask for one exact map/session/package observation and resume from the returned evidence.

For every profile, consult current official engine documentation when version-specific CLI, export, rendering, input, networking, packaging, or platform behavior matters. Record the consulted version and source in `PROGRESS.md` or `NOTES.md` without turning documentation research into a milestone.

## Playtest contract

At First Playable, MVP, and V1, observe a real player loop or conduct the closest available user-run session. Append concise answers:

1. What was the best or clearest moment?
2. What was the worst, confusing, slow, unfair, or inaccessible moment?
3. What unexpected behavior occurred?
4. Did the milestone's hypothesis hold, fail, or remain uncertain?
5. What is the smallest next change, pivot, or scope cut?

Distinguish `AGENT-OBSERVED`, `USER-OBSERVED`, automated evidence, and inference. Do not manufacture player feedback, treat the implementer's intuition as a playtest, or create a separate report for every session.

## Scope and placeholder rules

### Scope cuts

Cut in this order when the game is not becoming playable:

1. content quantity;
2. optional modes, progression, metagame, and settings;
3. secondary mechanics and combinatorial interactions;
4. custom assets, polish, and platform breadth;
5. architectural generality not required by the first loop.

Preserve the core fantasy, one verb, feedback, launchability, and a path to the approved target. If even that is not feasible, surface the product trade-off instead of producing an inert framework.

### Placeholder debt

Every placeholder records:

- what it substitutes for;
- why it does not invalidate the current milestone;
- the milestone by which it must be replaced or explicitly accepted;
- licensing/provenance when third-party material is involved; and
- its effect on feel, accessibility, content, performance, or release evidence.

V1 may retain a placeholder only when the user explicitly accepts it as final or it is irrelevant to the approved content boundary. Release Candidate cannot hide unknown asset rights.

### Just-in-time decisions

Record a decision in `GAME.md` only when alternatives have meaningful product, technical, compatibility, safety, cost, or delivery consequences. Keep it to decision, evidence/owner, and consequence. Comprehensive pre-build ideation belongs to Brainstormpro or Design Direction when explicitly requested.

## Optional capability fallbacks

- **No image generation:** use project assets, simple geometric/vector primitives, licensed placeholders, or explicit asset slots. Do not block the mechanic.
- **No audio generation or playback:** use existing/licensed cues, silent semantic hooks, visible feedback, and a user-run audio checklist. Do not claim mix quality.
- **No browser control:** run static/build gates and provide the exact served route, steps, viewport/input checks, and expected result for user observation.
- **No editor, console, device, or platform runtime:** use project-compatible static gates, then mark the runtime criterion `AWAITING USER RUNTIME` with one exact check.
- **No parallel agents:** continue sequentially. Parallel work may accelerate independent source, asset, test, or research slices, but all changes reconcile through the same artifacts and criteria.
- **No network or current docs:** preserve installed APIs and repository patterns, mark unstable behavior `UNKNOWN`, and avoid speculative upgrades.

Optional capabilities never relax done criteria. They only change who supplies evidence or whether a non-critical asset remains declared debt.

## Release Candidate

Classify each item, then verify only what applies:

- clean install or package, first launch, update, uninstall, and rollback;
- supported platform, controls, display, audio, accessibility, and performance;
- saves, schemas, migrations, corruption recovery, and compatibility;
- accounts, networking, disconnect/reconnect, authority, cheating/abuse, privacy, telemetry, commerce, and user content;
- asset and dependency licenses, attribution, branding, ratings, platform configuration, signing, and store metadata;
- crash/log diagnostics, known issues, manual actions, support path, and release owner.

Gamepro records readiness and remaining manual actions. Releasepro owns repository version selection, changelog mutation, release commit, tag, push, and publication flow.

## Journey examples

### Greenfield browser game to MVP

The user says “build a tiny typing game to MVP.” Inspect the empty repository and local toolchain, infer `GREENFIELD` and `MVP`, record the typing fantasy and one material input assumption, then implement one prompt→type→feedback loop before broad menus or content. Verify it in the served route, playtest, then add the minimal start, resolution, and restart journey. Report First Playable complete and MVP current throughout.

### Existing Godot game requiring a user run

The project already documents its engine/editor workflow. Preserve it, inspect the current scene and input map, and implement the next thin mechanic. If the host cannot launch the editor, run available script/import/test gates, record `AWAITING USER RUNTIME`, and ask the user to open one exact scene, perform one action, and report the expected feedback. Resume from that observation; never call the milestone verified from static checks alone.

### Resume an interrupted V1

Read Gamepro artifacts and source, re-run the recorded launch path, and compare evidence. If MVP still passes and V1 has two unmet content criteria plus declared audio debt, append a reconciliation entry and continue at the first unmet V1 slice. Do not regenerate a plan, re-ask settled decisions, or reset progress to First Playable.

### Game-jam spike

The user asks to prove an unusual control mechanic quickly. Set `SPIKE` and `FIRST PLAYABLE`, use the existing runtime, build only input→response→reset, and record whether the hypothesis held. Stop at the spike target unless the user explicitly promotes it to MVP or V1.
