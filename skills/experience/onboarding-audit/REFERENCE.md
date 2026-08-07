# Onboarding Audit Reference

## Contents

- [Evidence model](#evidence-model)
- [Scope and sampling](#scope-and-sampling)
- [Audit dimensions](#audit-dimensions)
- [Platform lenses](#platform-lenses)
- [Current journey schema](#current-journey-schema)
- [Finding format](#finding-format)
- [Artifact schemas](#artifact-schemas)
- [Direction handoff schema](#direction-handoff-schema)
- [Routing examples](#routing-examples)

## Evidence model

Use one status for each claim or dimension:

- `VERIFIED` — directly supported by current source, configuration, test, runtime behavior, measurement, or explicit approved decision.
- `SUPPORTED` — multiple current signals agree, but direct behavioral or quantitative proof is incomplete.
- `INFERRED` — a plausible interpretation from limited evidence; state the inference and validation path.
- `UNVERIFIED` — evidence is absent, inaccessible, stale, contradictory, or unsafe to obtain.
- `NOT APPLICABLE` — the dimension cannot materially affect the scoped onboarding; give the reason.

Evidence precedence depends on the claim. Current observed behavior outranks prose about implementation. Approved product intent outranks repeated accidental behavior. Retention-linked measurement outranks a conventional activation guess. Never convert a common industry practice into product evidence.

## Scope and sampling

Cover every materially different path rather than every cosmetic variant. Sample by:

- acquisition source or entry promise;
- anonymous, newly authenticated, invited, returning, and migrated users;
- novice and experienced users when the flow branches;
- supported platform, viewport, input, and accessibility mode;
- permission accepted, denied, restricted, and later-recovered states;
- happy, validation, loading, empty, degraded, offline, error, cancellation, retry, and resume states;
- first session and the earliest later-session teaching or retention step.

Record exclusions and why they cannot change the conclusion. Never imply complete coverage from one screenshot, one source path, one test, or one analytics funnel.

## Audit dimensions

| Dimension | Inspect | Strong evidence | Common failure |
|---|---|---|---|
| Product promise | Entry message and expected outcome | Campaign/product copy plus user intent evidence | Onboarding teaches features unrelated to the promise |
| Activation | Earliest retained-value action | Cohort or retention relationship plus product judgment | Completion is treated as activation |
| Time-to-value | Steps, waits, decisions, and actual elapsed time | Instrumented journey or repeatable timing | A short flow delivers no meaningful result |
| Outcome orientation | Real task versus interface tour | Representative first task and success output | Sidebar or feature tour before value |
| Cognitive load | Choices, fields, concepts, and jargon | Step inventory and usability evidence | Configuration precedes trust or context |
| Learning model | Doing, feedback, and contextual help | Successful guided accomplishment | Passive slides or blocking coach marks |
| Progressive disclosure | What is delayed and why | Later contextual introduction | Advanced settings front-loaded |
| Personalization | Collected signal and resulting branch | Trace from answer to changed experience | Questions collect data but change nothing |
| Commitment | Signup, verification, payment, import, or invite timing | Product, risk, and save-value constraints | Commitment requested before value without need |
| Permissions | Request timing, rationale, denial, recovery | Runtime paths and platform configuration | Blanket launch-time requests |
| Starter state | Templates, samples, imports, or generation | Useful editable starting point | Blank canvas with no next action |
| AI assistance | Work performed before user effort | Verified generation or import capability | AI promise followed by setup burden |
| Copy and trust | Voice, claims, action labels, privacy, recovery | Approved neighboring copy and factual sources | Generic hype or ambiguous consequences |
| Accessibility | Semantics, focus, targets, text, contrast, motion | Runtime and automated evidence | Flow blocks zoom, assistive tech, or reduced motion |
| Resilience | Loading, retry, offline, interruption, resume | State tests and runtime exercise | Progress disappears or the user is stranded |
| Continuation | Later mastery and feature timing | Lifecycle messaging or contextual triggers | Everything is taught in session one |
| Measurement | Event definitions, properties, funnels, cohorts | Versioned analytics definitions and observed data | Events measure screens, not user success |
| Experimentability | Hypothesis, unit, guardrail, rollback | Existing experiment and feature-flag contract | Many variables change without attribution |

## Platform lenses

### Web

Inspect responsive layout, keyboard and pointer parity, browser back/forward behavior, deep links, refresh and session recovery, autofill and password managers, popup or third-party auth failure, tab changes, import/upload behavior, and the transition from marketing promise to product outcome.

Do not assume account creation can be delayed when authorization, billing, tenancy, saved state, compliance, or abuse controls require it. Require the flow to explain necessary commitment in user terms.

### Native mobile

Inspect startup latency, one-handed reach, safe areas, software keyboard behavior, touch target size, system back or dismissal behavior, app background/termination recovery, poor connectivity, haptics, reduced motion, Dynamic Type, VoiceOver or TalkBack semantics, and each operating-system permission state.

Treat an under-one-minute first value as an aspiration where practical, not a pass/fail rule. A trustworthy safety, finance, health, identity, or data-migration flow may need more time.

### Cross-platform

Require a shared product outcome and vocabulary, not identical screens. Record where platform capabilities, trust expectations, input, persistence, or permission models justify different paths. Flag accidental divergence and forced parity separately.

## Current journey schema

For each journey row record:

| Field | Meaning |
|---|---|
| Step ID | Stable identifier such as `WEB-NOVICE-03` |
| Segment and platform | The affected population and environment |
| Entry and prerequisite | How the user arrived and required state |
| User job | What the user is trying to accomplish now |
| User action | Tap, click, text, selection, wait, or external action |
| Information or permission | Data, commitment, or access requested |
| System response | Visible and behavioral result |
| Value advanced | Concrete progress toward activation |
| States | Loading, validation, error, denial, retry, resume, success |
| Evidence | Source, test, runtime, analytics, or decision citation |
| Measurement | Event/property and known semantic quality |
| Exit and re-entry | What happens on skip, close, refresh, background, or return |

## Finding format

```md
## ONB-001 — Permission request precedes user intent

- Severity: HIGH
- Confidence: VERIFIED
- Platforms and segments: native mobile, new users
- Observed behavior: ...
- Expected user outcome: ...
- Activation impact: ...
- Evidence: ...
- Foundation principle: contextual permissions
- Strength to preserve: ...
- Recommendation boundary: Direction must solve ...; implementation remains out of scope
- Cheapest validation experiment: ...
- Related findings: ONB-004
```

Use severity to communicate consequence:

- `CRITICAL` — prevents or materially misrepresents safe access to the promised outcome.
- `HIGH` — likely blocks activation, trust, accessibility, recovery, or a major segment.
- `MEDIUM` — adds meaningful friction or weakens later success without blocking most users.
- `LOW` — bounded clarity, polish, or instrumentation weakness with limited user impact.

Severity is not priority by itself. Rank using impact, confidence, urgency, effort, reversibility, dependencies, and whether the issue blocks learning about other issues.

## Artifact schemas

Use these exact level-two headings in order. Add level-three detail beneath them rather than renaming the contract.

### RESEARCH.md

1. `## Scope and platforms`
2. `## Product promise and users`
3. `## Activation evidence`
4. `## Sources`
5. `## Constraints and guardrails`
6. `## Quality attributes`
7. `## Contradictions`
8. `## Unknowns`

### CURRENT-JOURNEY.md

1. `## Segments and entry points`
2. `## Journey inventory`
3. `## States and recovery`
4. `## Platform behavior`
5. `## Accessibility and localization`
6. `## Measurement coverage`
7. `## Exclusions`

### AUDIT-REPORT.md

1. `## Executive read`
2. `## Verified strengths`
3. `## Prioritized findings`
4. `## Systemic patterns`
5. `## Measurement gaps`
6. `## Experiment shortlist`
7. `## Improvement boundary`

Put detailed `ONB-{number}` findings under level-three headings inside `Prioritized findings` so the required report structure remains stable.

## Direction handoff schema

Write `DIRECTION-INPUT.md` with these exact headings:

1. `# Onboarding direction input`
2. `## Source audit`
3. `## Product promise and activation`
4. `## Platforms and segments`
5. `## Current journey`
6. `## Strengths to preserve`
7. `## Prioritized findings`
8. `## Constraints and non-goals`
9. `## Measurement and evidence gaps`
10. `## Required direction outcomes`
11. `## Unknowns and experiments`
12. `## Handoff state`

Under `Handoff state`, include exactly one state:

- `READY` — the direction can explore responsibly from current evidence.
- `PARTIAL` — direction can proceed only with named assumptions or validation experiments.
- `BLOCKED` — a missing product, safety, data, or authority decision makes responsible direction work impossible.

Also state one platform classification: `WEB`, `MOBILE`, or `CROSS-PLATFORM`. Link `RESEARCH.md`, `CURRENT-JOURNEY.md`, and `AUDIT-REPORT.md`. Preserve finding IDs and do not restate every finding.

## Routing examples

- “Audit this signup funnel and report problems” produces the audit package and stops.
- “Audit and redesign our first-run flow” produces the package, validates it, and invokes Onboarding Direction.
- “Design onboarding for our new app” routes directly to Onboarding Direction because no implemented flow exists.
- “Rewrite these onboarding labels only” routes to Prose Humanizer.
- “Implement the approved onboarding blueprint” routes to Planpro or Goalpro, not this audit.
