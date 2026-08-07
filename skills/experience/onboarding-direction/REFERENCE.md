# Onboarding Direction Reference

## Contents

- [Evidence statuses](#evidence-statuses)
- [Audit input](#audit-input)
- [Activation brief](#activation-brief)
- [Option quality test](#option-quality-test)
- [Platform adaptation](#platform-adaptation)
- [Embedded humanization](#embedded-humanization)
- [Iteration and approval](#iteration-and-approval)
- [Artifact schemas](#artifact-schemas)
- [Handoff selection](#handoff-selection)

## Evidence statuses

- `EVIDENCE` — supported by current product, user research, implementation, runtime, measurement, or approved decision.
- `ASSUMPTION` — a low-risk working hypothesis with rationale, owner, and validation.
- `USER DECISION` — a material direction choice that cannot be inferred safely.
- `EXPERIMENT` — the cheapest prototype, usability session, instrumentation change, or controlled release that reduces uncertainty.
- `UNKNOWN` — evidence is absent or contradictory and the impact is not yet understood.
- `NOT APPLICABLE` — the dimension cannot materially affect the scoped direction, with reason.

## Audit input

Prefer a validated same-slug `onboarding-audit/DIRECTION-INPUT.md` when an implemented onboarding exists. Read its linked research, current journey, and report. Preserve finding IDs and strengths through options and the final blueprint.

Treat handoff state as follows:

- `READY` — proceed normally.
- `PARTIAL` — expose named gaps in the design read and attach an experiment or user decision to each consequential assumption.
- `BLOCKED` — stop before options when the named gap affects safety, consent, authorization, data, the target user, product promise, or activation definition materially.

The audit identifies problems and evidence. Direction owns the new solution. Do not copy audit recommendations into every option as if they were approved design.

## Activation brief

Record:

| Dimension | Required content |
|---|---|
| Product promise | What brought the user here and supporting evidence |
| Primary user and job | Population, context, desired outcome, and exclusion risk |
| Activation | Earliest meaningful result and confidence in its retention relationship |
| First-value path | Required steps, waits, commitments, and system work |
| Guardrail | Trust, safety, correctness, access, or business behavior that must not regress |
| Failure signal | Evidence that would invalidate the direction |
| Continued success | The next useful behavior after activation |
| Platforms | Shared outcome and justified platform differences |
| Voice and identity | Approved copy and visual evidence to preserve |
| Unknowns | Discoverable gaps, user decisions, and experiments |

Avoid defining activation as “completed onboarding,” “saw the dashboard,” or another product-owned proxy unless evidence shows it is the meaningful user result.

## Option quality test

Options are distinct only when they change at least three consequential relationships such as:

- value-before-commitment versus commitment-before-value with a justified trust model;
- generated, imported, template-based, goal-based, or guided-task activation;
- universal path versus meaningful segmentation;
- linear flow versus in-product checklist or contextual milestones;
- education before action versus action with contextual explanation;
- permission, profile, collaboration, or notification timing;
- first-session scope and later-session continuation;
- platform-specific entry and recovery behavior.

Palette, illustration, headline, progress-indicator, or screen-count changes alone are not distinct directions.

For every option include:

| Dimension | Required evidence |
|---|---|
| User outcome | Activation mechanism, first result, and continued success |
| Path | Steps, choices, waits, commitment, and likely friction |
| Segmentation | Signal, branch consequence, and experienced-user route |
| Learning | Accomplishment, contextual help, and progressive disclosure |
| Trust | Data, auth, permissions, consent, recovery, and transparency |
| Resilience | Loading, error, interruption, retry, offline, and resume |
| Access | Keyboard, touch, assistive technology, motion, text, and localization |
| Platform | Shared outcome and intentional web/mobile differences |
| Measurement | Event meanings, success question, guardrail, and evidence gap |
| Risk | Failure modes, effort, reversibility, and abandonment evidence |
| Audit traceability | Finding IDs resolved and strengths preserved |

## Platform adaptation

### Web

Model marketing-to-product continuity, invitation and deep-link entry, authentication redirects, browser history, refresh, tabs, responsive layout, keyboard and pointer use, autofill, uploads/imports, third-party integration failure, and session recovery.

### Native mobile

Model startup, one-handed reach, safe areas, software keyboard, system back/dismissal, backgrounding and termination, network degradation, touch targets, haptics, reduced motion, Dynamic Type, assistive technology, and each permission state.

### Cross-platform

Keep the product promise, activation meaning, core terms, and measurement semantics coherent. Allow path, input, timing, persistence, and permission differences where platform behavior or user context justifies them. Show differences visibly in the preview and blueprint.

## Embedded humanization

Supply Prose Humanizer with:

- audience, user job, and emotional/trust context;
- approved product claims and source locations;
- protected product, platform, privacy, permission, and legal terms;
- neighboring copy samples and approved design-direction voice evidence;
- exact UI role and structural limits for each string;
- action consequence, state, and accessibility meaning;
- desired output structure.

Require:

1. final copy in the requested structure;
2. material pattern clusters changed;
3. fact, qualifier, and protected-structure comparison;
4. unresolved ambiguity that the direction must expose.

Never let naturalness change the consequence of signup, consent, data use, permissions, payment, deletion, publication, notification, or irreversible action.

## Iteration and approval

Add this append-only table to `DIRECTION-OPTIONS.md`:

| Revision | Options shown | User feedback | Disposition | Preview |
|---|---|---|---|---|
| R1 | A, B, C | B reaches value quickly but asks for notifications too early | REFINE B; REJECT A/C | `previews/ONBOARDING-PREVIEW-R1.html` |
| R2 | B2, D, E | Preserve B2 and strengthen recovery | REFINE B2 | `previews/ONBOARDING-PREVIEW-R2.html` |
| R3 | B3 | Approved for web and mobile | APPROVE B3 | `previews/ONBOARDING-PREVIEW-R3.html` |

Approval must name the option and revision. Record platform scope, approved behavior, explicit exclusions, remaining experiments, and whether implementation is requested. A later change to activation, auth, permissions, data, commitment, or scope requires a new preview revision and delta approval.

## Artifact schemas

Use these exact level-two headings in order. Add option, platform, state, and evidence detail beneath them rather than renaming the contract.

### RESEARCH.md

1. `## Sources`
2. `## Product promise and users`
3. `## Current journey or audit input`
4. `## Activation brief`
5. `## Guardrails`
6. `## Platforms`
7. `## Voice and visual evidence`
8. `## Measurement`
9. `## Alternatives`
10. `## Contradictions`
11. `## Unknowns and experiments`

### DIRECTION-OPTIONS.md

1. `## Design read`
2. `## Shared comparison basis`
3. `## Option comparison`
4. `## Detailed options`
5. `## Recommendation`
6. `## Audit traceability`
7. `## Experiments`
8. `## Preview revisions`
9. `## Selected preview revision`
10. `## User decision`
11. `## Approval provenance`

### ONBOARDING-BLUEPRINT.md

1. `## Selected direction`
2. `## Activation definition`
3. `## Platform and segment flow`
4. `## Step purposes`
5. `## Commitment and permission timing`
6. `## Starter state and learning`
7. `## Interruption and recovery`
8. `## Success and continuation`
9. `## Preserved strengths`
10. `## Resolved findings`
11. `## Constraints and prohibited shortcuts`
12. `## Verification targets`

### EXPERIENCE-MATRIX.md

1. `## Platforms and segments`
2. `## Entries and viewports`
3. `## Inputs and states`
4. `## Permissions and connectivity`
5. `## Accessibility`
6. `## Localization and content extremes`
7. `## Exit and re-entry`
8. `## Expected behavior`

### COPY-DECK.md

1. `## Voice sources`
2. `## Protected claims and terms`
3. `## Representative strings`
4. `## Platform differences`
5. `## Humanization record`
6. `## Fidelity comparison`
7. `## Unresolved ambiguity`
8. `## Final approved copy`

### MEASUREMENT-PLAN.md

1. `## Activation hypothesis`
2. `## Event meanings`
3. `## Funnel and cohort questions`
4. `## Guardrails`
5. `## Instrumentation gaps`
6. `## Experiment sequence`
7. `## Rollout learning`
8. `## Privacy`
9. `## Abandonment evidence`

## Handoff selection

Choose Planpro when any material implementation question remains: concrete files, architecture, shared state, analytics schema, experiment framework, auth, permissions, data lifecycle, cross-platform coordination, migration, rollout, rollback, observability, or project gates.

Choose direct Goalpro only when the selected preview revision and implementation boundary are explicitly approved; current code evidence makes slices and exact gates concrete; every Goalpro handoff section is present; criteria are independently verifiable; and remaining unknowns are safely discoverable.

Direction-only delivery is complete when the user does not request implementation. Never infer mutation approval from selection alone.
