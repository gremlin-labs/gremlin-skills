# Email Lifecycle Audit Reference

## Contents

- [Evidence model](#evidence-model)
- [Product context](#product-context)
- [Scope and sampling](#scope-and-sampling)
- [Evidence precedence](#evidence-precedence)
- [Audit dimensions](#audit-dimensions)
- [Current-system schema](#current-system-schema)
- [Campaign inventory schema](#campaign-inventory-schema)
- [Finding format](#finding-format)
- [Artifact schemas](#artifact-schemas)
- [Strategy handoff schema](#strategy-handoff-schema)
- [Routing examples](#routing-examples)

## Evidence model

Use one status for each claim or dimension:

- `VERIFIED` — directly supported by current source, configuration, provider state, runtime behavior, measurement, or explicit approved decision.
- `SUPPORTED` — multiple current signals agree, but direct behavioral or quantitative proof is incomplete.
- `INFERRED` — a plausible interpretation from limited evidence; state the inference and validation path.
- `UNVERIFIED` — evidence is absent, inaccessible, stale, contradictory, unsafe to obtain, or dependent on an untested client/provider behavior.
- `NOT APPLICABLE` — the dimension cannot materially affect the scoped program; give the reason.

Do not equate configured with working, delivered with read, clicked with product value, returned with meaningfully reactivated, or signup with consent or activation.

## Product context

When Planpro's product-research lens is unavailable, classify each of these as `RELEVANT`, `NOT APPLICABLE`, or `UNKNOWN` and cite evidence:

- user, account, role, plan, geography, acquisition context, and job;
- product promise, current path, first value, second value, maturity, and expected usage cycle;
- observable success, guardrail, failure signal, and abandonment evidence;
- accessibility, privacy, security, billing, account access, support, data integrity, localization, reliability, and operational quality attributes;
- event/data, provider, DNS, template, analytics, rollout, rollback, ownership, and external-review constraints;
- credible alternatives, including sending nothing or using an in-product/support intervention instead;
- discoverable unknowns, assumptions, user decisions, and cheapest validation experiments.

## Scope and sampling

Cover every materially different path rather than every cosmetic template variant. Sample by:

- lifecycle stage: unverified, unactivated, first value, second value, active, expanding, at risk, lapsed, reactivated, churned, suppressed;
- individual/team, role, plan, locale, geography, acquisition source, consent, and assisted-support state;
- classification: transactional, service/operational, lifecycle marketing, promotional, legal/compliance, and human support;
- scheduled and event-triggered entry, every meaningful branch, completed-goal exit, priority conflict, suppression, frequency cap, retry, cancellation, and sunset;
- eligible, unsubscribed, complained, bounced, deleted, suspended, inaccessible-content, and missing-data recipients;
- mobile/desktop, light/dark, images blocked, plain text, large text, keyboard/screen-reader order, long/Unicode/RTL content, and common clients when evidence exists;
- first session, initial program, ongoing education, trial, early inactivity, 30/60/90 re-engagement, and post-reactivation continuation where in scope.

Record exclusions and why they cannot change the conclusion. Never imply complete coverage from one template, recipient, campaign, source path, dashboard, or provider preview.

## Evidence precedence

Precedence depends on the claim:

- Current observed send/exit/suppression behavior outranks prose about intended orchestration.
- Current provider and DNS verification outrank configuration strings that claim authentication or stream separation.
- Versioned event semantics and deduplication tests outrank event names alone.
- Approved product intent outranks repeated accidental behavior.
- Durable consent/preference/suppression records outrank inferred signup intent.
- Retention-linked product measurement and holdouts outrank opens, clicks, or conventional activation guesses.
- Rendered and assistive-technology evidence outranks template-source appearance.
- Current official legal/mailbox/provider sources outrank secondary summaries; qualified counsel owns legal conclusions.

Record contradictions instead of silently selecting the convenient source.

## Audit dimensions

| Dimension | Inspect | Strong evidence | Common failure |
|---|---|---|---|
| Product outcomes | Promise, first/second value, maturity, usage cycle | Approved product definitions plus cohort evidence | Signup or login treated as value |
| Lifecycle state | Event derivation, identity/account scope, latency | Versioned semantics, tests, observed state | Page view resets inactivity |
| Campaign purpose | One primary job and channel fit | Trace from state to desired product outcome | Feature inventory or unnecessary email |
| Entry and branch | Eligibility, timing, segment, alternatives | Code/provider rules plus fixtures | Every user receives the same drip |
| Exit | Goal completion, irrelevance, escalation, end | Tested immediate exit | Reminders continue after completion |
| Arbitration | Priority, global cap, support/billing conflicts | Central rules and conflict tests | Contradictory messages send together |
| Classification | Transactional/service/lifecycle/promotional/legal | Owned classification registry and review | Promotions hidden in critical mail |
| Consent/preferences | Basis, geography, source, opt-out, deletion | Durable records and suppression tests | Signup assumed to authorize marketing |
| Deliverability | SPF, DKIM, DMARC, alignment, streams, reputation | Current DNS/provider evidence and monitoring | Bulk reputation threatens critical mail |
| Copy and sender | Accuracy, voice, expectation, reply path | Approved neighboring copy and monitored sender | Fake personal tone or unsupported claim |
| CTA/deep link | Exact next action, auth, access, fallback | Runtime exercise for eligible/ineligible states | Generic dashboard or dead resource |
| Personalization | Expected data, usefulness, fallback, privacy | Product-state trace and edge fixtures | Creepy detail or broken merge field |
| Accessibility/rendering | Semantics, mobile, dark, images off, text | Client/runtime and assistive evidence | Meaning exists only in images |
| Reliability | Deduplication, ordering, retries, cancellation | Queue/provider tests and observability | Duplicate or stale message sends |
| Operations | Ownership, alerts, runbook, reply/support path | Current dashboards and exercised recovery | Nobody can stop or explain a bad campaign |
| Measurement | Product conversion, window, cohort, guardrail | Versioned metrics plus holdout | Opens select winners |
| Re-engagement | Product-specific lapse and distinct stages | Expected-use evidence and quality retention | Same “we miss you” repeated |
| AI assistance | Approved facts/fields, validation, review, logging | Bounded generation contract and tests | Invented progress or sensitive inference |

## Current-system schema

Document:

| Field | Meaning |
|---|---|
| System component | Product service, scheduler, queue, ESP, stream, template store, analytics, or operator surface |
| Owner | Team or role accountable for behavior and recovery |
| Inputs | Product events, user/account attributes, consent, campaign state, and time |
| State derivation | How eligibility, maturity, meaningful activity, and lapse are computed |
| Decisions | Entry, branch, wait, replace, suppress, send, exit, escalate, or sunset |
| Idempotency and ordering | Duplicate, late, retry, and cancellation behavior |
| Outputs | Message classification, sender/stream, template/version, deep link, and event |
| Failure and recovery | Detection, retry, manual action, rollback, and user consequence |
| Evidence | Source, provider, DNS, test, runtime, analytics, runbook, or approved decision |
| Status | Evidence-model classification |

## Campaign inventory schema

For each material campaign or message record:

| Field | Meaning |
|---|---|
| Campaign ID and name | Stable local identifier and recognizable name |
| Lifecycle stage | User state and maturity addressed |
| Objective | One primary user/product outcome |
| Classification | Transactional, service, lifecycle, promotional, legal, or human support |
| Audience and exclusions | Roles, plans, geographies, consent, and suppressions |
| Entry and delay | Event/state and timing basis |
| Branches | Meaningful behavior or attribute alternatives |
| Exit | Goal, irrelevance, escalation, reactivation, sequence end, or suppression |
| Priority and frequency | Arbitration tier and global/local cap evidence |
| Sender and reply | Identity, monitored route, and expectation |
| CTA and deep link | Exact action, destination, auth/access, and fallback |
| Dynamic data | Fields, allowed use, fallbacks, deleted/inaccessible behavior |
| Rendering | HTML/plain, mobile, dark, images off, access, localization evidence |
| Measurement | Product conversion, attribution window, cohort/holdout, guardrails |
| Owner and operations | Template, campaign, data, deliverability, support, and incident owners |
| Evidence and status | Citations plus evidence-model classification |

## Finding format

Give each verified strength a stable ID before writing findings:

```md
### EMS-001 — Transactional verification is isolated

- Evidence status: VERIFIED
- User or operational value: ...
- Evidence: ...
- Preserve by: ...
```

Strength IDs are append-only within the audit. Use them in findings and downstream strategy traceability; do not renumber strengths merely because presentation order changes.

```md
### EML-001 — Completed users remain eligible for activation rescue

- Severity: HIGH
- Confidence: VERIFIED
- Campaigns, states, and segments: activation-rescue; first-value-completed; individual free users
- Observed behavior: ...
- Desired user outcome: ...
- Product and trust impact: ...
- Evidence: ...
- Foundation principle: explicit exit conditions
- Strengths to preserve: EMS-001
- Recommendation boundary: Strategy must solve ...; implementation remains out of scope
- Cheapest validation experiment: ...
- Related findings: EML-004
```

Severity communicates consequence:

- `CRITICAL` — causes or risks unauthorized, deceptive, unsafe, legally sensitive, account-critical, or widespread trust failure.
- `HIGH` — likely blocks user value, sends materially irrelevant mail, corrupts measurement, harms delivery, or affects a major segment.
- `MEDIUM` — adds meaningful friction, confusion, operational risk, or weakens later success.
- `LOW` — bounded clarity, polish, or observability weakness with limited impact.

Severity is not priority by itself. Rank using impact, confidence, urgency, effort, reversibility, dependencies, and whether the issue blocks learning about other issues.

## Artifact schemas

Use these exact level-two headings in order. Add level-three detail beneath them rather than renaming the contract.

### RESEARCH.md

1. `## Scope and eligibility`
2. `## Product outcomes and lifecycle model`
3. `## Sources and access limits`
4. `## Provider and architecture evidence`
5. `## Consent and legal-review boundary`
6. `## Quality attributes`
7. `## Contradictions`
8. `## Unknowns`

### CURRENT-SYSTEM.md

1. `## Architecture and ownership`
2. `## Events and lifecycle states`
3. `## Message classification and streams`
4. `## Consent preferences and suppression`
5. `## Orchestration and conflict resolution`
6. `## Rendering and accessibility`
7. `## Operations and recovery`
8. `## Measurement and experimentation`
9. `## Unverified behavior`

### CAMPAIGN-INVENTORY.md

1. `## Campaign coverage`
2. `## Campaign inventory`
3. `## Cross-campaign conflicts`
4. `## Content and rendering states`
5. `## Measurement coverage`
6. `## Ownership and exclusions`

### AUDIT-REPORT.md

1. `## Executive read`
2. `## Verified strengths`
3. `## Prioritized findings`
4. `## Systemic patterns`
5. `## Risk and legal-review boundaries`
6. `## Measurement gaps`
7. `## Experiment shortlist`
8. `## Refactor boundary`

Put detailed `EMS-{number}` strengths under level-three headings inside `Verified strengths` and detailed `EML-{number}` findings under level-three headings inside `Prioritized findings`.

## Strategy handoff schema

Write `STRATEGY-INPUT.md` with these exact headings:

1. `# Email lifecycle strategy input`
2. `## Source audit`
3. `## Product promise and lifecycle outcomes`
4. `## Segments and maturity states`
5. `## Current system`
6. `## Strengths to preserve`
7. `## Prioritized findings`
8. `## Campaign and orchestration constraints`
9. `## Consent deliverability and operational guardrails`
10. `## Measurement and evidence gaps`
11. `## Required strategy outcomes`
12. `## Unknowns and experiments`
13. `## Handoff authority`
14. `## Handoff state`

Under `Handoff authority`, include the standalone marker `EVIDENCE_ONLY` and state that the artifact records evidence and readiness but grants no authority to run Strategy, implement, change providers or DNS, deploy, or send. Strategy may run only when the current request explicitly includes strategy/improvement/refactoring or the user later authorizes it.

Under `Handoff state`, include exactly one standalone state:

- `READY` — strategy can explore responsibly from current evidence.
- `PARTIAL` — strategy can proceed only with named assumptions or validation experiments.
- `BLOCKED` — a missing product, consent, safety, data, authority, or legal-review decision makes responsible strategy work impossible.

Link `RESEARCH.md`, `CURRENT-SYSTEM.md`, `CAMPAIGN-INVENTORY.md`, and `AUDIT-REPORT.md`. Carry every `EMS-{number}` strength and `EML-{number}` finding from `AUDIT-REPORT.md` into the matching handoff sections; the validator checks complete ID propagation. `BLOCKED` must name the resolving owner or decision. `PARTIAL` must name each assumption and its validation path. The validator checks shape and ID accounting, not truth; manually verify citations, strength preservation, and state honesty.

## Routing examples

- “Audit our Customer.io onboarding and win-back journeys” → audit.
- “Our lifecycle emails are messy; assess them and propose a better program” → audit, then same-slug strategy.
- “Design lifecycle email for this new SaaS product” → strategy, no audit.
- “Rewrite this welcome email in our voice” → Prose Humanizer or bounded copy workflow, not this audit.
- “Fix our DKIM failure and restore delivery” → incident diagnosis/execution, not a lifecycle-program audit.
- “Implement the approved lifecycle strategy” → Planpro or Goalpro, not this audit.
