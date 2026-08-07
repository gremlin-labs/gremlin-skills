# Email Lifecycle Strategy Reference

## Contents

- [Evidence and readiness](#evidence-and-readiness)
- [Strategy comparison](#strategy-comparison)
- [Campaign design contract](#campaign-design-contract)
- [Lifecycle state contract](#lifecycle-state-contract)
- [Message and humanization contract](#message-and-humanization-contract)
- [Consent deliverability and operational contract](#consent-deliverability-and-operational-contract)
- [Measurement contract](#measurement-contract)
- [Artifact schemas](#artifact-schemas)
- [Handoff rules](#handoff-rules)

## Evidence and readiness

Use `VERIFIED`, `SUPPORTED`, `INFERRED`, `UNVERIFIED`, and `NOT APPLICABLE` consistently. A supplied audit handoff has three states:

- `READY` — explore from current evidence without hiding unresolved implementation detail.
- `PARTIAL` — preserve every named assumption and experiment in each option and final package.
- `BLOCKED` — stop until the named product, consent, data, safety, authority, or qualified-review decision is resolved.

Validate the handoff structurally, then verify its linked evidence manually. Do not let a passing validator convert weak evidence into truth.

The handoff must say `EVIDENCE_ONLY`. Its readiness state answers whether responsible exploration is possible; it never grants permission to invoke this skill or to mutate anything. Require current-request authorization for Strategy. Reconcile every `EML-*` finding and `EMS-*` strength from the audit report into each option and the selected final package; missing IDs are a contract failure, not an editorial omission.

For greenfield work, classify user/problem, current or intended journey, desired outcome, quality attributes, delivery, alternatives, and unknowns proportionally. Treat “send nothing,” in-product guidance, human support, and a smaller initial program as credible alternatives.

## Strategy comparison

Compare options on the same product truth and show consequential differences:

| Dimension | Specify |
|---|---|
| Product thesis | User progress the program should enable and why email is appropriate |
| First/second value | Evidence, hypothesis, and transition between activation and repetition |
| Lifecycle model | Stages, transitions, expected use, and lapse/reactivation |
| Program shape | Time backbone, behavior branches, breadth, and ramp sequence |
| Segmentation | Role, plan, account, maturity, geography, acquisition, and exclusions |
| Campaign system | Objectives, entry, delay, branches, exit, priority, suppression, frequency |
| Sender and support | Company/person identity, reply expectation, escalation, and ownership |
| Personalization | Allowed state/data, usefulness, fallbacks, and privacy expectation |
| Re-engagement | Prior-value segments, early inactivity, distinct stages, incentives, sunset |
| Trust and delivery | Classification, consent, streams, authentication, reputation, access |
| Access and rendering | Mobile, dark, images off, semantic/plain text, localization, fallbacks |
| Measurement | Product conversion, window, holdout, cohort, guardrail, failure signal |
| Delivery burden | Data, provider, DNS, template, operations, rollout, risk, reversibility |

Options are not distinct if only subject lines, visual style, send day, or message count changes. Preserve incompatible choices until the user selects a direction.

## Campaign design contract

Every approved campaign records:

| Field | Required decision |
|---|---|
| Campaign ID/name | Stable identifier and recognizable product language |
| Lifecycle stage | User maturity and expected progress |
| Objective | One primary user/product outcome |
| Channel fit | Why email rather than in-product, support, sales, or no intervention |
| Classification | Transactional, service, lifecycle, promotional, legal, or human support |
| Audience/exclusions | Role, plan, geography, consent, support, billing, and suppressions |
| Entry/delay | Product event or derived state plus timing basis |
| Branches | Meaningful alternative behavior/data paths |
| Exit/replace | Goal completion, irrelevance, escalation, reactivation, end, or replacement |
| Priority/frequency | Arbitration tier plus global and campaign cap |
| Sender/reply | Identity, monitored route, and expectation |
| CTA/deep link | Exact next action, destination, auth/access, and fallback |
| Dynamic data | Allowed fields, expected use, fallback, deleted/inaccessible behavior |
| Message brief | Moment, promise, objection, proof, action, trust, and protected terms |
| Rendering/access | HTML/plain, mobile, dark, images off, semantics, text, locale |
| Measurement | Product conversion, attribution, holdout, cohort, and guardrails |
| Ownership | Product, lifecycle, data, template, delivery, support, and incident owners |
| Dependencies/state | Required implementation/external work and readiness |

One email has one primary job. Supporting links must not compete with the main action.

## Lifecycle state contract

Define events and derived state separately. Include:

- identity and account scope, role changes, merges, deletion, suspension, and tenancy;
- first value, second value, core/adjacent adoption, active, at risk, lapsed stages, reactivated, churned, suppressed;
- meaningful activity versus incidental sessions;
- event semantics, version, properties, producer, deduplication key, ordering, latency, backfill, and correction;
- eligibility recomputation before send;
- wait, send, replace, suppress, exit, escalate, and sunset outcomes;
- campaign priority, global frequency, support/billing/security conflicts, and re-entry;
- retry/idempotency, cancellation, stale queued work, provider failure, and manual recovery;
- test scenarios for completion before send, late events, duplicate events, role/plan/consent changes, reactivation, inaccessible content, and campaign version migration.

Pseudocode clarifies intent but does not replace project-specific implementation planning.

## Message and humanization contract

For every representative or final message give Prose Humanizer:

- audience, account context, maturity, moment, and objective;
- classification, consent/unsubscribe constraint, sender, reply behavior, and support promise;
- approved facts, product capabilities, claims, qualifiers, and proof;
- actual voice evidence, product terms, and prohibited generic or deceptive patterns;
- CTA destination, action consequence, auth/access fallback, and supporting links;
- allowed merge fields, meaning, fallback, data sensitivity, deletion/inaccessibility behavior;
- subject, preview, plain-text meaning, HTML hierarchy, images-off meaning, and protected structure.

Record the draft, obvious-AI pattern clusters changed, fabrication/meaning audit, and final fidelity comparison. Do not invent accomplishments, use surveillance-like detail, simulate a personal thread, fabricate urgency, or imply a human reply path that is not staffed.

Protected merge fields such as `{first_name}`, `{project_name}`, or provider-specific equivalents may remain only when they are listed in the variable inventory with a safe fallback. Unfinished-task markers, “your product,” dummy copy, and undocumented example tokens are unresolved planning placeholders.

## Consent deliverability and operational contract

Document fact, assumption, external action, and qualified-review need separately:

- message classification, reviewed basis/consent state, geography, source, proof, and owner;
- preference center, visible and one-click unsubscribe where applicable, durable suppression, deletion, and re-enrollment prevention;
- transactional/bulk stream or subdomain separation, SPF, DKIM, DMARC, alignment, return path, sending categories, retries, and rate policy;
- reputation, bounces, complaints, deferrals, volume/ramp, provider requirements, and incident alerts;
- template/version owner, campaign owner, data owner, deliverability owner, support/reply owner, approval and rollback authority;
- current official source, access date, version/jurisdiction, inference, and qualified legal/provider review.

Do not claim compliance, inbox placement, or legal approval from a planning artifact.

## Measurement contract

Prefer product outcomes: first/second value, time to value, workflow completion, feature adoption, collaboration, trial conversion, retained use, quality reactivation, incremental retained users, appropriate revenue/expansion, and support-friction reduction.

For each campaign define:

- primary product conversion and semantic event;
- eligibility denominator and excluded populations;
- attribution window and competing causes;
- holdout/control design when feasible;
- leading diagnostics: delivered, clicked, replied, bounced;
- guardrails: unsubscribe, complaint, support issues, low-quality conversion, downstream retention, successful completion;
- cohort/window compatibility, privacy, minimum maturity, and reporting limitations;
- rollout decision, rollback/abandonment evidence, and next structural experiment.

Treat open measurement as unreliable where privacy behavior obscures it. Do not let statistical confidence replace practical user value or trust.

## Artifact schemas

Use these exact level-two headings in order. Add level-three detail beneath them rather than renaming the contract.

### RESEARCH.md

1. `## Sources`
2. `## Product promise users and jobs`
3. `## Audit input or current evidence`
4. `## Lifecycle outcome brief`
5. `## Segments and maturity states`
6. `## Events data and deep links`
7. `## Consent deliverability and operations`
8. `## Voice sender and visual evidence`
9. `## Measurement and experiments`
10. `## Alternatives`
11. `## Contradictions and unknowns`

### STRATEGY-OPTIONS.md

1. `## Strategy read`
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

### MESSAGE-SAMPLES.md

1. `## Voice sources`
2. `## Protected facts classifications and terms`
3. `## Sample coverage`
4. `## Representative messages`
5. `## Dynamic fields and fallbacks`
6. `## Rendering and accessibility`
7. `## Humanization record`
8. `## Fidelity comparison`
9. `## Unresolved ambiguity`
10. `## Final approved samples`

### LIFECYCLE-STRATEGY.md

1. `## Selected strategy`
2. `## Product outcomes`
3. `## Lifecycle stages and segments`
4. `## Channel fit and sender model`
5. `## Campaign portfolio`
6. `## Cadence frequency and arbitration`
7. `## Activation repetition and expansion`
8. `## Inactivity re-engagement and sunset`
9. `## Preserved strengths and resolved findings`
10. `## Rollout and learning`
11. `## Risks assumptions and prohibited shortcuts`
12. `## Verification targets`

### CAMPAIGN-MAP.md

1. `## Portfolio scope`
2. `## Campaign map`
3. `## Entry branch and exit logic`
4. `## Priority suppression and frequency`
5. `## Sender content and destination`
6. `## Ownership and dependencies`
7. `## Readiness and exclusions`

### STATE-AND-DECISION-MODEL.md

1. `## Identity and account scope`
2. `## Product events`
3. `## Derived lifecycle states`
4. `## Meaningful activity and lapse`
5. `## Decision and conflict model`
6. `## Timing ordering and idempotency`
7. `## Pseudocode`
8. `## Edge cases and recovery`
9. `## Test scenarios`

### MESSAGE-BRIEFS.md

1. `## Portfolio and brief status`
2. `## Shared voice and trust contract`
3. `## Shared data and fallback contract`
4. `## Initial program briefs`
5. `## Later lifecycle briefs`
6. `## Transactional and channel coordination`
7. `## Approval and unresolved evidence`

### COPY-DECK.md

1. `## Voice sources`
2. `## Protected facts classifications and terms`
3. `## Approved initial program`
4. `## Subjects previews and senders`
5. `## Message bodies and calls to action`
6. `## Plain text images off and accessibility`
7. `## Dynamic fields and fallbacks`
8. `## Humanization record`
9. `## Fidelity comparison`
10. `## Unresolved ambiguity`

### DELIVERABILITY-AND-CONSENT-GUARDRAILS.md

1. `## Message classification`
2. `## Eligibility consent and preferences`
3. `## Unsubscribe suppression and deletion`
4. `## Sender domains streams and authentication`
5. `## Reputation volume and monitoring`
6. `## Accessibility rendering and localization`
7. `## Privacy and data minimization`
8. `## Ownership incidents and recovery`
9. `## External actions and qualified review`
10. `## Unverified requirements`

### MEASUREMENT-PLAN.md

1. `## Product outcome hypotheses`
2. `## Event meanings and eligibility`
3. `## Attribution windows`
4. `## Holdouts and cohorts`
5. `## Diagnostics and guardrails`
6. `## Reporting limits and privacy`
7. `## Experiment sequence`
8. `## Rollout learning and rollback`
9. `## Abandonment evidence`

## Handoff rules

- Planpro is the default route because lifecycle implementation normally spans multiple system and external boundaries.
- Direct Goalpro requires explicit named-preview approval and the canonical `GOALPRO-INPUT.md` headings: `Goal and product outcome`, `Approval provenance`, `Implementation slices`, `Acceptance criteria`, `Non-goals and boundaries`, `Quality applicability`, `Project gates`, `Delivery requirements`, `Manual and external actions`, `Unverified assumptions`, `Sensitive-data constraints`, and `Readiness`.
- Mark direct handoff `READY` only when unresolved assumptions cannot materially change user behavior, consent, classification, data integrity, deliverability, operations, or risk.
- Approval scope must name option, revision, included campaigns, excluded work, approved facts, and material external actions. Any later material delta requires renewed approval.
