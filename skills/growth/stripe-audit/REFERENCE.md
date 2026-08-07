# Stripe Audit Reference

Use every applicable section. Verify current behavior against official Stripe documentation and the account's API version rather than relying on this checklist as a frozen API reference.

## Evidence statuses

Assign one status to every check:

- `VERIFIED` — inspected evidence demonstrates the required behavior.
- `FINDING` — evidence demonstrates a defect, weakness, or material risk.
- `NOT APPLICABLE` — the capability is demonstrably absent or irrelevant.
- `UNVERIFIED` — access or evidence is insufficient; state exactly what is missing.

For code, cite `file:line`. For Stripe configuration, record mode, object type, sanitized ID, relevant fields, and inspection date. Never record secret values, payment details, or unnecessary customer data.

## 0. Product and billing policy

Apply [Planpro's product-research lens](contracts/product-research.md) before judging implementation. Record:

- Primary user, billing-account/tenant boundary, paid job-to-be-done, and intended product outcome.
- Which subscription states grant, preserve, restrict, or revoke access.
- Grace, delinquency, cancellation, pause, refund, dispute, trial, and reactivation policy.
- Application-credit replenishment, rollover, expiry, upgrade/downgrade, compensation, and failed-work policy when applicable.
- Acceptable abuse risk, false-positive tolerance, customer recovery, and support/operator path.
- Success signal, guardrail, and failure signal for billing correctness.

Classify each policy as `KNOWN`, `NOT APPLICABLE`, or `UNKNOWN`. A product-policy unknown is not a code defect and must not be guessed; carry it into the handoff as a user decision.

## 1. Architecture and ownership

Map:

- Next.js version, App Router or Pages Router, runtime, and deployment platform.
- Stripe SDK version and explicitly configured API version.
- Authentication, tenant/account model, and billing-account ownership.
- Database tables for customers, subscriptions, invoices, events, entitlements, credits, and jobs.
- Checkout, portal, webhook, reconciliation, and admin entry points.
- Queues, retries, scheduled jobs, transactional boundaries, and observability.
- Which system owns billing truth, product access, usage allowance, and display state.

Flag multiple modules independently mutating subscription, entitlement, or credit state without a shared invariant.

## 2. Credential safety and account selection

Discover variable names without displaying their values. Do not run commands that dump the environment, enable shell tracing, place a secret in command history, or expose it in process arguments.

Prefer, in order:

1. An authenticated read-only Stripe integration or connected tool.
2. Existing Stripe CLI authentication scoped to the intended account.
3. The project's established secret loader with a local read-only inspection process that never outputs the key.
4. Code-only inspection with account checks marked `UNVERIFIED`.

Determine sandbox/test versus live mode before requests. Confirm that code, webhook secrets, products, prices, and deployments do not cross modes. Use list and retrieve operations only. Never create, update, delete, resend, expire, advance a clock, or trigger an event during the audit.

If only live access exists, minimize queries and avoid broad customer or subscription exports.

## 3. Stripe account configuration

Inspect and cross-check:

- Account identity and mode.
- Products, active and archived Prices, currencies, recurring intervals, usage type, tax behavior, lookup keys, and metadata used by the app.
- Repository Price-ID mappings versus actual Prices and environments.
- Duplicate or obsolete products and prices that could still be selected.
- Webhook destinations, endpoint mode, API version, enabled event types, status, and duplicated responsibilities.
- Customer portal configurations, allowed plan changes, quantities, prorations, cancellation timing, promotion codes, and return URLs.
- Billing retry and dunning behavior where accessible.
- Automatic tax and customer-address requirements when applicable.
- Entitlements configuration when Stripe Entitlements is used.
- Radar or trial-abuse controls when applicable.

Flag client-selectable arbitrary Price IDs, missing environment separation, incompatible portal options, and event destinations that receive unnecessary events.

## 4. Customer identity and Checkout

Verify:

- One durable Stripe Customer maps to one internal billing account or tenant.
- Customer ownership is authorized server-side; email is not the sole identity key.
- Concurrent first purchases cannot create duplicate customer mappings.
- Checkout Session creation requires an authenticated and authorized principal.
- Allowed products, Prices, currencies, quantities, trials, and discounts are server-controlled.
- User input cannot set credit amounts, entitlement levels, privileged metadata, or success URLs.
- Internal IDs in `client_reference_id` or metadata contain no secrets or sensitive data.
- Stripe POST operations use stable operation-scoped idempotency keys.
- Repeat clicks and concurrent requests cannot create unintended subscriptions.
- Existing subscribers are sent to management flow when appropriate.
- Success pages display status but do not serve as the only fulfillment or provisioning path.
- Customer portal sessions are created server-side after ownership checks.

Document the uniqueness boundary: user, organization, workspace, or another billing account.

## 5. Webhook ingress and processing

Verify:

- The handler uses the exact raw body and correct endpoint signing secret.
- Signature verification occurs before parsing or side effects.
- The endpoint accepts only expected methods and required event types.
- Expensive work is queued or otherwise separated from prompt acknowledgement.
- Acknowledgement and retry semantics cannot silently lose accepted work.
- Event IDs are durably deduplicated.
- Business effects have their own durable idempotency keys.
- Two distinct Event objects concerning the same Stripe object cannot duplicate effects.
- Concurrent deliveries are serialized, locked, or made safe by database constraints.
- Handlers do not assume event arrival order.
- Stale events retrieve current Stripe state or use monotonic transition rules where needed.
- Database changes that must agree occur in one transaction.
- Failed processing is observable and replayable.
- Unknown event types are safely ignored and recorded at an appropriate level.
- Logs include event ID, type, object ID, mode, attempt, outcome, and correlation ID without sensitive payloads.

A `2xx` before durable acceptance is a finding. A slow handler that risks repeated delivery is a finding.

## 6. Subscription state projection

Model relevant states, including incomplete, trialing, active, past due, unpaid, paused, canceled, and pending changes.

Verify:

- Local state is a query projection, not an unchecked replacement for Stripe billing truth.
- Initial activation, renewal, failure, recovery, cancellation, pause, resume, upgrade, downgrade, and deletion have explicit transitions.
- Paid access is provisioned from payment or entitlement evidence appropriate to the product.
- Payment failure does not accidentally grant a new cycle of access or credits.
- Cancellation-at-period-end preserves access only through the intended boundary.
- Immediate cancellation and delinquency behavior match product policy.
- Pending subscription updates do not provision an upgrade before successful payment.
- Portal changes and dashboard changes converge through the same synchronization path.
- Subscription item and Price changes update plan mapping correctly.
- Multiple subscriptions are either supported explicitly or prevented.
- Timestamps use Stripe period boundaries rather than webhook receipt time.
- A reconciliation job can repair drift without duplicating side effects.

Document whether Stripe Subscriptions, Stripe Entitlements, or local policy controls access.

## 7. Event matrix

For every subscribed or required event, record:

- Event type and Stripe object.
- Business purpose.
- Preconditions and authoritative fields.
- Local transition.
- Idempotency key.
- Concurrency and ordering policy.
- Retry behavior.
- Compensating action.
- Tests.
- Owning module.

At minimum, evaluate applicable subscription, invoice, Checkout, entitlement, refund, and dispute events. Confirm exact event names against current Stripe documentation and the account API version.

Treat `invoice.paid` as the candidate renewal-payment signal. Verify subscription status and qualifying invoice contents before provisioning. Do not treat `customer.subscription.updated` as proof of payment.

## 8. Application usage credits

Apply this section only when the app replenishes an internal pool of tokens, generations, minutes, or similar usage units. Do not confuse these with Stripe Billing Credits.

First define product semantics:

- Which Prices grant credits?
- Does initial purchase grant them?
- Does every paid renewal grant them?
- Does “replenish” reset, top up, preserve rollover, or expire an earlier grant?
- What happens on upgrade, downgrade, proration, trial conversion, manual invoice payment, free invoice, refund, dispute, pause, or cancellation?
- Are bonus and purchased credits consumed or expired differently?

Verify:

- A qualifying paid invoice is the durable business trigger.
- The server derives the amount from a trusted Price-to-allocation mapping.
- The grant is tied to the correct billing account and subscription item.
- A durable uniqueness constraint covers the invoice and grant purpose.
- Event recording, ledger insertion, and balance mutation are atomic.
- Concurrent webhook workers cannot both grant.
- Retrying after a partial failure converges safely.
- The balance is derived from or reconciled against an append-only ledger.
- Each ledger entry records reason, amount, invoice, subscription, Price, period, and timestamp.
- Reset semantics preserve an audit trail rather than overwriting unexplained state.
- Compensation for refunds, voids, disputes, and administrative corrections is explicit and auditable.
- Negative balances or already-consumed refunded credits have a defined policy.
- Reconciliation can identify missing and duplicate grants and repair them idempotently.
- Credit expiry uses the intended billing-period boundary and handles plan changes.
- Usage debits are atomic and cannot overspend under concurrent generation requests.

Recommended business key:

```text
unique(billing_account_id, stripe_invoice_id, grant_kind)
```

Adapt the key when one invoice legitimately grants multiple allocations, such as one per subscription item. The database constraint—not an in-memory check—must be the final duplicate barrier.

## 9. Entitlements and authorization

Verify:

- Every paid feature is enforced server-side at the expensive or privileged operation.
- UI visibility is not the authorization boundary.
- Subscription status, entitlement, and credit balance have distinct meanings.
- Cached access has an expiry and invalidation path.
- Multi-tenant users cannot read or mutate another tenant's billing state.
- Plan changes update entitlements without relying on browser redirects.
- Revocation behavior for cancellation, delinquency, refunds, and disputes matches policy.
- Stripe Entitlements summaries are persisted or paginated correctly when used.
- High-cost work reserves or debits credits transactionally before execution.
- Failed work has a defined refund policy that cannot be abused.

## 10. Abuse and economic controls

Audit:

- Duplicate subscriptions and concurrent Checkout creation.
- Repeated free trials across accounts, emails, payment methods, devices, or organizations.
- Coupon and promotion reuse, stacking, scope, and server-side eligibility.
- Disposable identities and unverified account creation where economically material.
- Checkout, portal, webhook, and generation endpoint rate limits.
- Client-controlled quantities, Prices, trial lengths, credits, or entitlement metadata.
- Resource consumption races and replayed generation requests.
- Refund abuse after credits have been consumed.
- Account resale or credential sharing signals when relevant.
- Radar rules or trial-abuse controls appropriate to the business.
- Administrative credit adjustments and support tooling audit trails.

Do not recommend a single heuristic as definitive fraud detection. Record false-positive risk, operational review needs, and customer-recovery paths.

## 11. Plan changes, proration, and portal behavior

Verify:

- Upgrade and downgrade timing is deliberate.
- Proration behavior is explicit and previewed where users need price certainty.
- Paid upgrades use pending updates or an equivalent payment-safe design.
- Failed upgrade payment does not grant the higher plan or its credits.
- Downgrades do not destroy already-earned value contrary to policy.
- Subscription schedules and portal-managed changes cannot overwrite each other unexpectedly.
- Quantity changes are authorized and bounded.
- Cancellation and reactivation preserve correct period and credit semantics.
- Portal capabilities match what application code and support procedures assume.

## 12. Security and privacy

Verify:

- Secret and restricted keys remain server-only and out of source control.
- Live keys use least privilege where feasible and have a rotation process.
- Webhook signing secrets are distinct per endpoint and environment.
- Preview deployments cannot access production billing unintentionally.
- Sensitive data is absent from metadata, URLs, logs, analytics, and audit artifacts.
- Redirect and return URLs are allowlisted.
- Billing routes enforce authentication, authorization, validation, and rate limits.
- Dependency versions and API upgrades are deliberate and tested.
- Error responses do not expose Stripe payloads, secrets, or internal object ownership.

## 13. Reconciliation and operations

Verify a scheduled or operator-triggered process can:

- Compare local customers, subscriptions, invoices, entitlements, and grants with Stripe.
- Detect missing webhooks, failed jobs, stale projections, duplicate customers, and duplicate subscriptions.
- Reprocess an invoice or event without repeating effects.
- Backfill missed application-credit grants safely.
- Produce a dry-run report before repair.
- Bound pagination, rate limits, and time windows.
- Resume from checkpoints.
- Record who or what initiated a repair.

Require alerts or dashboards for webhook failure rate, processing lag, dead-letter depth, reconciliation drift, duplicate suppression, failed renewals, missing grants, and suspicious credit adjustments.

## 14. Required test scenarios

Require deterministic tests for applicable cases:

1. Initial successful subscription.
2. Successful recurring renewal.
3. Failed renewal and later recovery.
4. Duplicate delivery of the same Event.
5. Two distinct Events for the same business effect.
6. Concurrent processing of duplicate deliveries.
7. Out-of-order subscription and invoice events.
8. Worker failure before and after each transactional boundary.
9. Missing webhook repaired by reconciliation.
10. Upgrade success and upgrade payment failure.
11. Downgrade now and at period end.
12. Cancel, resume, pause, and reactivate.
13. Trial conversion and trial abuse.
14. Refund, dispute, void, and credit-note policy.
15. Customer portal changes.
16. Cross-tenant authorization attempt.
17. Arbitrary or archived Price-ID attempt.
18. Repeated Checkout submission.
19. Two or more consecutive renewal cycles.
20. Concurrent usage debits at the remaining-credit boundary.

Use Stripe CLI for local webhook delivery and Stripe Billing simulations or test clocks for lifecycle behavior when appropriate. Include unit tests for pure transition logic, database tests for uniqueness and transactions, integration tests for handlers, and end-to-end tests for critical billing journeys.

## 15. Finding format

Write each finding as:

```md
## STRIPE-001 — Duplicate renewal can grant credits twice

- Severity: CRITICAL
- Status: VERIFIED
- Evidence: `app/api/stripe/webhook/route.ts:84`
- Stripe evidence: sandbox endpoint `we_...`, inspected 2026-07-09
- Invariant violated: One qualifying invoice grants one allocation.
- Failure scenario: Two workers process the same paid invoice concurrently.
- Customer/business impact: A user receives multiple renewal allocations.
- Recommendation: Add an append-only grant ledger and database uniqueness constraint.
- Done when: Concurrent processing of one qualifying invoice creates exactly one ledger grant.
- Verification: Run the concurrency integration test and assert one grant and one balance change.
```

Use sanitized IDs. Distinguish an observed failure from a plausible risk.

## 16. Priority rules

- `CRITICAL` — unauthorized charges/access, secret exposure, cross-tenant billing access, repeatable double-crediting, or unrecoverable billing corruption.
- `HIGH` — likely subscription drift, missed renewals, incorrect access, exploitable abuse, or no recovery path.
- `MEDIUM` — meaningful reliability, testing, observability, or configuration weakness with bounded impact.
- `LOW` — maintainability, cleanup, or defense-in-depth improvement.

Order goalpro work by dependency and risk, not only severity. Establish invariants and safety nets before risky migrations.

## 17. Stripe additions to GOALPRO-INPUT.md

Follow [Goalpro's canonical handoff contract](contracts/goalpro-handoff.md). In addition, include:

- Links to every Stripe audit artifact and selected finding.
- Stripe account mode, API version, and sanitized configuration evidence.
- Data migration, subscription reconciliation, credit-ledger, and rollback requirements.
- Stripe sandbox verification steps.
- Test-clock scenarios where relevant.
- Security and secret-handling constraints.
- Billing observability and reconciliation gates.
- Manual Dashboard or account actions clearly separated from code changes and marked unauthorized until explicitly approved.
- Product-policy assumptions that Goalpro must not guess.

Do not prescribe a broad rewrite when isolated safe slices can establish the invariants incrementally.

## Current official sources to consult

Start with current official documentation for:

- Subscription webhooks: https://docs.stripe.com/billing/subscriptions/webhooks
- Webhook handling: https://docs.stripe.com/webhooks
- Undelivered events: https://docs.stripe.com/webhooks/process-undelivered-events
- Idempotent requests: https://docs.stripe.com/api/idempotent_requests
- Checkout fulfillment: https://docs.stripe.com/checkout/fulfillment
- Subscription changes: https://docs.stripe.com/billing/subscriptions/change
- Pending updates: https://docs.stripe.com/billing/subscriptions/pending-updates
- Billing testing: https://docs.stripe.com/billing/testing
- Test clocks: https://docs.stripe.com/billing/testing/test-clocks
- Customer portal: https://docs.stripe.com/customer-management
- One-subscription controls: https://docs.stripe.com/payments/checkout/limit-subscriptions
- Entitlements: https://docs.stripe.com/billing/entitlements
- Customer abuse: https://docs.stripe.com/disputes/prevention/abuse
- Key security: https://docs.stripe.com/keys-best-practices
- Metadata safety: https://docs.stripe.com/metadata

Search current official documentation for features not covered here. Record material changes or API-version differences in the audit.
