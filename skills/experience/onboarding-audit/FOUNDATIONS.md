# Onboarding Foundations

This portable foundation synthesizes the collection's web and mobile onboarding research. Use it as a structured hypothesis set. Verify product fit, user behavior, current platform rules, safety, privacy, accessibility, and implementation constraints before applying any recommendation.

## Contents

- [Outcome and activation](#outcome-and-activation)
- [Friction and learning](#friction-and-learning)
- [Commitment and permissions](#commitment-and-permissions)
- [Starting states and personalization](#starting-states-and-personalization)
- [Copy trust and success](#copy-trust-and-success)
- [Lifecycle and measurement](#lifecycle-and-measurement)
- [Web considerations](#web-considerations)
- [Native mobile considerations](#native-mobile-considerations)
- [AI-native considerations](#ai-native-considerations)
- [Exceptions and guardrails](#exceptions-and-guardrails)

## Outcome and activation

Onboarding exists to help a user reach a meaningful outcome, not to explain the product exhaustively or maximize completion of an introductory sequence.

Start by identifying:

- the promise or problem that brought the user to the product;
- the earliest action or result plausibly associated with retained value;
- the shortest trustworthy path from entry to that result;
- the population and time horizon for which the activation hypothesis applies;
- the guardrail that must not regress while time-to-value improves.

Examples of activation are product-specific: a useful conversation, published artifact, completed payment, collaborative edit, successful import, or first recovered error. Treat these as patterns, not templates.

Optimize activation rate and time-to-value before onboarding completion. Completion remains a diagnostic signal because it can reveal friction, but finishing screens without receiving value is not success.

## Friction and learning

Every screen, tap, field, choice, delay, and context switch spends user attention. Ask whether each one materially advances value, safety, trust, or required understanding.

Prefer:

- doing before explaining;
- guided accomplishment over interface tours;
- one clear purpose and action per step;
- contextual help at the moment of need;
- progressive disclosure of advanced choices;
- defaults, inference, import, or automation where accurate and reversible;
- skip, exit, and resume paths for experienced or interrupted users.

Avoid front-loading technical vocabulary, configuration, long feature lists, or passive walkthroughs. Education should follow the user's task and feedback rather than compete with it.

## Commitment and permissions

Delay account creation, verification, payment, profile completion, integration setup, or other commitment until it unlocks immediate value when the product can do so safely. When commitment is required earlier for authorization, tenancy, saved state, billing, fraud, compliance, or data integrity, explain the reason and resulting benefit plainly.

Request permissions in context:

- camera when scanning or capture begins;
- photo access when the user chooses an upload path;
- microphone when recording begins;
- location when the chosen feature genuinely needs it;
- notifications after the product has delivered something worth returning to.

Design denial, restriction, later enablement, and recovery. Never manipulate consent or imply that optional access is required.

## Starting states and personalization

Blank states demand invention before users understand the product. Consider templates, samples, demo workspaces, example conversations, starter data, imports, or generated drafts that are safe to edit or discard.

Personalize only when a signal changes the experience. Useful signals may include goal, role, experience, acquisition source, device, organization context, or observed behavior. Each question should have a visible consequence; otherwise infer, delay, or remove it.

Use smart defaults when they are accurate, transparent, reversible, and privacy-appropriate. Never infer sensitive traits or silently make consequential choices.

## Copy trust and success

Use the language and personality already supported by the product. Explain the user's outcome, next action, consequences, privacy, recovery, and progress without generic hype or unsupported certainty.

Celebrate real success proportionally. A clear confirmation such as a published artifact, completed scan, saved draft, or received payment usually matters more than decorative spectacle. Motion and haptics should communicate progress, hierarchy, or completion and must respect reduced-motion preferences.

Trust grows when the product:

- asks for information only when its use is clear;
- preserves progress through interruption;
- offers a truthful preview of consequential actions;
- handles errors and denial without blame;
- makes recovery possible;
- avoids hiding costs, data use, or commitment.

## Lifecycle and measurement

Onboarding continues after the first session. Introduce collaboration, organization, automation, or expert features when behavior makes them useful rather than during initial setup.

Measure at minimum where applicable:

- entry or install to first open;
- first open or signup to activation;
- time-to-value;
- drop-off and error per meaningful step;
- permission prompts and outcomes separately;
- day-one, day-seven, and later retention appropriate to the product;
- adoption of capabilities associated with continued success;
- support contacts caused by onboarding confusion.

Define events around user and system outcomes, not only screen views. Confirm event semantics, identity stitching, exclusions, privacy, and freshness before trusting a funnel.

Experiment by isolating a meaningful variable: remove a field, delay a permission, change the activation task, provide starter content, improve recovery, or personalize one branch. Define the hypothesis, population, success signal, guardrail, duration basis, and rollback before interpreting results.

## Web considerations

Web onboarding may begin on a marketing page, invitation, deep link, or authenticated product route. Preserve the promise across that transition.

Inspect:

- responsive behavior and keyboard/pointer parity;
- browser history, refresh, tab changes, and session expiry;
- deep-link and invite recovery;
- password managers, autofill, and social-sign-in failures;
- uploads, imports, popups, redirects, and third-party integrations;
- empty states and starter content at each responsive size;
- cancellation, retry, and return after leaving the site.

Do not start with a generic dashboard tour. Let the first real task teach the relevant interface and reveal the next feature when context exists.

## Native mobile considerations

Mobile users may be interrupted, one-handed, on a small screen, using a software keyboard, or on an unreliable network. Startup and every tap must justify their cost.

Inspect:

- launch responsiveness and non-blocking motion;
- safe areas, thumb reach, touch targets, and gesture discoverability;
- software keyboard focus, scrolling, and visible primary actions;
- app backgrounding, termination, and restored progress;
- slow, offline, degraded, retry, and cached states;
- Dynamic Type, VoiceOver or TalkBack, high contrast, color independence, and reduced motion;
- system permission timing, denial, restriction, and Settings recovery;
- subtle haptics only for meaningful feedback.

One to three welcome screens and a first value within roughly a minute are useful aspirations for many consumer products, not universal requirements. Prefer immediate interaction and allow informed skipping when safe.

## AI-native considerations

AI can perform work instead of explaining work. When the verified product supports it, generate or import a useful first result, then let the user refine it.

Protect this pattern with:

- truthful capability and latency expectations;
- a useful loading or streaming state;
- failure, retry, cancellation, and fallback behavior;
- cost, quota, safety, privacy, and data-use disclosure where material;
- editable output and a clear save boundary;
- no claim that a generated example proves general quality.

The principle is: generate value before asking the user to create value, when doing so is safe, supportable, and aligned with the real product.

## Exceptions and guardrails

Do not optimize time-to-value by weakening:

- informed consent or permission clarity;
- security, authorization, abuse prevention, or account recovery;
- regulated disclosures or suitability checks;
- data integrity, migration safety, or irreversible-action review;
- accessibility and localization;
- trust, pricing transparency, or privacy;
- product comprehension required to avoid harm.

The shortest flow is not automatically the best flow. Prefer the shortest path that delivers meaningful value with the required trust and safety intact.
