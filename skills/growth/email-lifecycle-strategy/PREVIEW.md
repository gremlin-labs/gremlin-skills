# Email Lifecycle Strategy HTML Preview Contract

## Contents

- [Purpose](#purpose)
- [Preflight](#preflight)
- [Required comparison](#required-comparison)
- [Lifecycle simulation](#lifecycle-simulation)
- [Message display modes](#message-display-modes)
- [HTML and accessibility](#html-and-accessibility)
- [Iteration](#iteration)
- [Validation](#validation)

## Purpose

Build the cheapest credible simulation of proposed lifecycle email systems before implementation. The preview is the primary surface for comparing, steering, rejecting, refining, and approving product-state logic, campaign arbitration, message direction, and trust constraints. It is not production email HTML, a campaign calendar, or several visual treatments over the same drip sequence.

## Preflight

Before writing HTML, inventory product promise, first/second value, expected usage cycle, segments and roles, maturity/lapse states, audit findings and strengths, approved brand/email patterns, sender/reply behavior, approved claims, events and deep links, consent/preferences, transactional/support/billing conflicts, deliverability, accessibility/localization, measurement, and implementation unknowns.

Use sanitized realistic content from product evidence. Mark preview claims and behavior `IMPLEMENTED`, `PROPOSED`, `INFERRED`, or `UNVERIFIED`. Never copy secrets, customer data, production identifiers, recipient addresses, or unsupported accomplishments.

## Required comparison

Render every option against the same product outcomes and evidence. Each strategy panel must contain these `data-preview-section` values:

1. `strategy-summary` — option ID, thesis, intended user progress, rationale, strongest trade-off, and evidence status.
2. `lifecycle-map` — maturity states, expected transitions, first/second value, inactivity, reactivation, and sunset.
3. `decision-simulation` — representative user states/actions and resulting send, wait, replace, suppress, exit, escalate, or sunset outcomes.
4. `campaign-system` — portfolio, objectives, audiences, classification, entry/exit, priority, frequency, sender, CTA, and ownership.
5. `message-preview` — complete representative humanized messages plus dynamic-field, deleted/inaccessible-content, and reply fallbacks.
6. `trust-and-delivery` — consent, preferences, classification, streams/domains, authentication assumptions, accessibility, rendering, privacy, operations, and external review.
7. `measurement` — product conversions, event semantics, attribution windows, holdouts, cohorts, guardrails, gaps, and cheapest experiment.
8. `tradeoffs` — user value, trust, inbox load, data/provider burden, operational risk, reversibility, audit traceability, and invalidation signal.

Use actual product vocabulary. A team workflow, financial product, creative tool, learning app, and occasional reporting product must not receive the same lifecycle map or cadence.

## Lifecycle simulation

- Provide at least two strategy controls with `data-strategy-target`, `aria-controls`, and managed `aria-selected`.
- Give panels matching `data-strategy-panel` IDs.
- Represent at least two distinct user/maturity states per panel using `data-user-state`.
- Represent at least three campaigns per panel using `data-campaign-card`.
- Provide interactive controls that change product action, lifecycle state, support/billing conflict, consent, or reactivation where relevant.
- Emit at least one `send` and one non-send decision per panel using `data-decision-outcome`. Non-send outcomes include `wait`, `replace`, `suppress`, `exit`, `escalate`, and `sunset`.
- Show the event/state evidence, campaign affected, reason, next eligible state, and uncertainty for every simulated decision.
- Recompute eligibility immediately before the simulated send. Demonstrate at least one completed-action exit and one global conflict/suppression path.
- Include at least three complete message samples per panel using `data-message-sample`, covering activation/value and another materially different lifecycle role.

Do not fake provider execution. If the preview simulates a send, label it as proposed planning behavior.

## Message display modes

Every panel must expose:

- `data-email-view="desktop"` and `data-email-view="mobile"`;
- `data-email-theme="light"` and `data-email-theme="dark"`;
- `data-images="on"` and `data-images="off"`.

Controls must update visible content and accessible state. Images-off retains sender, reason, primary action, destination meaning, help, and unsubscribe/classification context. Dark mode must remain legible. Mobile should use a readable hierarchy and touch targets. Plain-text meaning may be shown as an additional view.

Document protected merge fields and safe fallbacks. A merge field may appear only when `MESSAGE-SAMPLES.md` defines its meaning, allowed source, fallback, sensitivity, and deleted/inaccessible behavior.

## HTML and accessibility

- Use `<!doctype html>`, `lang`, UTF-8, viewport metadata, a descriptive title, semantic headings, landmarks, and real buttons.
- Include a visible notice containing “planning preview” and “not production.”
- Add metadata to the element with `data-email-lifecycle-preview`: `data-preview-revision`, `data-lifecycle-slug`, `data-evidence-date`, and `data-program-scope`.
- Keep the file self-contained: inline CSS/JS, no external resources, network calls, forms that submit, dead links, analytics, trackers, or recipient data.
- Use visible focus, keyboard-operable tabs/controls, labels, `aria-live` for decision changes, and no positive tab indexes.
- Avoid essential hover-only behavior, focus traps, autoplay, flashing, or motion-dependent meaning.
- Support narrow/mobile layouts, 200% zoom, at least 30% text expansion, long/Unicode/RTL content, and `prefers-reduced-motion`.
- Use restrained planning-interface styling grounded in approved product identity. The strategy must remain understandable without decorative images or motion.
- Do not use fake brands, lorem ipsum, dummy recipients, placeholder gradients, or undocumented planning tokens.

## Iteration

Keep `EMAIL-LIFECYCLE-PREVIEW.html` as the latest alias. Before presenting a revision, copy the validated bytes to `previews/EMAIL-LIFECYCLE-PREVIEW-R{n}.html`; record the digest and change summary in `STRATEGY-OPTIONS.md`. Never overwrite an immutable revision.

Provide three feedback actions:

- `data-preview-action="refine"`
- `data-preview-action="new-set"`
- `data-preview-action="approve"`

The visible approval instruction must name the option and revision format. Approval of screenshots, copy alone, an unvalidated file, or an unnamed revision is insufficient.

## Validation

Run:

```bash
python3 {email-lifecycle-strategy-skill-root}/scripts/validate_email_lifecycle_preview.py \
  agent-work/{slug}/email-lifecycle-strategy/EMAIL-LIFECYCLE-PREVIEW.html
```

Then manually exercise:

1. every strategy tab and keyboard transition;
2. every user state/action/conflict/consent/reactivation control;
3. send and non-send decisions, completed-goal exits, and conflict suppression;
4. at least three representative messages per option;
5. desktop/mobile, light/dark, images on/off, and any plain-text mode;
6. dynamic-field missing/long/Unicode/RTL and deleted/inaccessible-resource paths;
7. feedback actions and visible approval instruction;
8. narrow layout, zoom/text expansion, focus, live announcements, and reduced motion;
9. self-containment, browser console, and exact root/revision digest equality.

Record limitations honestly. Browser planning previews cannot prove real mailbox clients, provider templating, sender authentication, inbox placement, screen-reader/client combinations, or live orchestration.
