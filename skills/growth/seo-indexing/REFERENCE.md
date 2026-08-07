# SEO Indexing reference

Use this reference to select safe candidates, preserve Google's provider semantics, approve recurring execution, and record immutable request evidence.

## Contents

- [Provider capability boundary](#provider-capability-boundary)
- [Operating modes and approval](#operating-modes-and-approval)
- [Candidate discovery](#candidate-discovery)
- [Live eligibility matrix](#live-eligibility-matrix)
- [Queue schema](#queue-schema)
- [Selection and deduplication](#selection-and-deduplication)
- [Submission paths](#submission-paths)
- [Automation contract](#automation-contract)
- [Receipts and status language](#receipts-and-status-language)
- [Failure handling](#failure-handling)
- [Official-source starting points](#official-source-starting-points)

## Provider capability boundary

Keep these Google capabilities separate:

| Capability | Supported use | Not proof of |
|---|---|---|
| Search Console URL Inspection API | Read Google's indexed-version status for an owned-property URL | Live indexability, a submitted request, current ranking, or guaranteed search appearance |
| Search Console URL Inspection UI | Inspect indexed state, run a live test, and request indexing for a few owned URLs | Guaranteed crawl time, inclusion, ranking, or a fixed daily allowance |
| XML sitemap | Scalable discovery signal for canonical URLs and truthful update metadata | Crawl, indexation, ranking, or a manual request receipt |
| Google Indexing API | Notify Google about eligible job posting and qualifying livestream event pages | General-purpose submission for articles, landing pages, products, or guides |
| Search operators | Contextual public observation | Complete or authoritative index coverage |

Google documents a daily limit for individual indexing requests but does not publish a guaranteed number. Treat ten as an approved local ceiling when selected, not as quota evidence. Do not split work across accounts or properties to circumvent limits.

Requesting recrawl more than once for the same unchanged URL does not make Google crawl it faster. A healthy sitemap, crawlable internal links, stable canonicals, useful content, and sound site architecture remain the scalable discovery path.

## Operating modes and approval

| Mode | Mutation behavior | Approval requirement | Best fit |
|---|---|---|---|
| `REMINDER` | Verifies and queues URLs; sends exact manual action; never submits | Exact reminder/automation contract | Browser session or standing mutation authority is unavailable |
| `ATTENDED` | Verifies URLs, previews exact batch, then submits through signed-in UI | Per-run exact batch confirmation | Occasional or sensitive properties |
| `UNATTENDED` | Verifies and submits only policy-matching URLs | Standing bounded operating-policy approval | Stable property, durable authorized browser/API path, mature receipts, and clear stop behavior |

A standing approval contains:

```text
approved_revision
approval_time_and_actor
search_console_property
allowed_canonical_origins
environment
candidate_sources
required_publication_evidence
mode
max_requests_per_run
schedule_and_timezone
eligibility_rules
priority_rules
deduplication_and_requeue_rules
provider_path
credential_source_names
artifact_and_retention_policy
notification_behavior
quota_cost_and_failure_policy
pause_disable_delete_path
```

Require renewed approval for a material change to any field. Runtime URLs may vary within the unchanged property, origins, source, eligibility, and cap policy.

## Candidate discovery

Use a bounded incremental cursor. Record the last successful discovery point separately for each source:

| Source | Useful cursor | Trust requirement |
|---|---|---|
| `CONTENT-RECEIPT.md` | Published timestamp plus receipt revision | Authorized production target observed |
| Landing Page receipt or quality report | Published timestamp plus final URL | Approved SEO owner/index posture and observed target |
| CMS/deployment record | Immutable publish/deploy ID and time | Record maps to the approved production origin |
| Sitemap | Prior content digest plus URL and truthful `lastmod` delta | Sitemap is live, canonical, accepted, and not using blanket current timestamps |
| User list | Exact list digest and approval time | URLs are owned, production, and within the property |

Do not infer a new page from a changed title alone. Do not treat every sitemap `lastmod` change as material; verify the underlying published content or defect receipt.

Normalize before deduplication:

- strip fragments;
- reject or remove tracking parameters according to canonical policy;
- resolve approved redirects and retain the source-to-final relationship;
- normalize host, scheme, trailing slash, case, and locale only according to actual site behavior;
- keep separate canonical locale pages separate;
- never rewrite a URL into a preferred form that the live site does not support.

## Live eligibility matrix

| Gate | `READY` evidence | Ineligible or blocked outcome |
|---|---|---|
| Environment | Exact public production origin | Localhost, preview, staging, gated, private, or campaign-only URL |
| Property | URL is contained by approved Search Console property | Property mismatch or ambiguous domain ownership |
| Network | Valid DNS/TLS and stable public GET | DNS/TLS failure, authentication, timeout, or unstable origin |
| HTTP | Final response is intentional `200` | Error, soft 404, loop, or unapproved redirect target |
| Robots | robots.txt permits the relevant crawler | Disallow or unavailable robots policy requiring repair |
| Index directive | No meta or header `noindex`; approved `INDEX` posture | `NOINDEX`, conflicting directive, or unresolved intent |
| Canonical | Expected owner/final URL is the declared canonical | Missing material canonical decision, wrong owner, duplicate target, or conflict |
| Sitemap | Intended canonical is present when Strategy/Setup requires it | Missing or stale sitemap entry requiring source repair |
| Internal discovery | At least one relevant crawlable internal link or approved hub path | Orphan or manipulative link plan |
| Content | Complete, useful, non-placeholder, non-duplicate page | Thin, empty, broken, duplicate, or misleading page |
| Publication | Immutable receipt or equivalent observed production evidence | Build output or route declaration only |
| Indexed state | GSC indexed-version evidence says not indexed, unknown, or materially stale | Already indexed means skip; ambiguous provider result means investigate |
| Request history | No request for the same unchanged version | Duplicate unchanged request |

Use GET, not HEAD alone. Inspect rendered output when client rendering, authentication shells, error boundaries, or content hydration could change the result.

A passing live test does not cover every condition Google applies during indexing. Preserve that limitation in the run report.

## Queue schema

Use this header for `URL-QUEUE.csv`:

```csv
url,canonical_url,property,discovery_source,source_revision,published_or_updated_at,owner,cluster,priority,http_status,final_url,robots_allowed,indexing_allowed,user_canonical,sitemap_present,internal_link_present,content_ready,gsc_verdict,last_request_at,eligibility,reason,next_action
```

Use one of these eligibility states:

```text
DISCOVERED
VERIFYING
READY
ALREADY_INDEXED
UNCHANGED_ALREADY_REQUESTED
INELIGIBLE
ROUTE_FOR_REPAIR
AWAITING_APPROVAL
AWAITING_USER_ACTION
REQUESTED
PROVIDER_REJECTED
QUOTA_STOP
AUTH_BLOCKED
PROPERTY_BLOCKED
SUPERSEDED
```

Do not use `INDEXED` unless current Search Console indexed-version evidence supports it. Preserve exact provider verdict separately from normalized state.

## Selection and deduplication

Order eligible rows by:

1. `P0` new approved canonical owner with complete sitemap and internal-link discovery;
2. `P1` materially changed approved owner or repaired technical issue with a new receipt;
3. `P2` explicit exception with a documented user/product reason;
4. publication time, oldest eligible first within the same priority unless Strategy defines another fair order.

Never prioritize by keyword volume alone. Protect existing winners and avoid requesting a URL whose ownership conflicts with an indexed page.

Deduplicate by canonical URL plus source revision/content digest. A URL is eligible to requeue only when:

- a material published change produced a new receipt or content digest;
- a verified robots, canonical, sitemap, render, deployment, or provider problem was repaired;
- Google explicitly instructs a retry after a transient failure; or
- the user approves a documented exception after reviewing unchanged-request evidence.

Do not use time passage alone to create a fresh request.

## Submission paths

### Ordinary web pages

Use signed-in Search Console computer use:

1. Confirm the visible property before entering the URL.
2. Inspect the exact canonical URL.
3. Preserve the indexed-version result.
4. Skip when already indexed.
5. Request indexing once.
6. Wait for the visible provider result.
7. Record sanitized evidence and stop on any unexpected state.

The UI may run a quick eligibility check. If it reports a problem, record the problem and route repair; do not click around the blocker or alter provider settings.

### Restricted Indexing API

Before any call, consult current official documentation and prove:

- page type is an eligible job posting or qualifying livestream event;
- required structured data is present, visible, valid, and truthful;
- Search Console ownership and API authorization apply to the URL;
- quota and spam-policy requirements are understood;
- the approved operating contract names the API path.

Do not add structured data solely to gain API access. An API `200` records receipt of a notification, not indexation.

### Sitemaps

For many URLs, route source improvements to the owning skill. Submit or maintain a sitemap through `seo-setup` or approved technical execution. `seo-indexing` may verify sitemap membership and cite a prior accepted sitemap receipt, but it does not silently rewrite or resubmit sitemaps.

## Automation contract

Use a host-supported scheduler only after approval. Define:

```text
automation_name
objective_and_exact_prompt
target_repository_or_task
working_directory
schedule_or_interval
timezone
property_and_allowed_origins
operating_mode
max_requests_per_run
candidate_sources_and_cursors
eligibility_and_priority_rules
credential_source_names
artifact_destination_and_retention
notification_destination_and_threshold
quota_or_cost_behavior
partial_failure_behavior
first_run_verification
pause_disable_delete_path
approval_provenance
```

The prompt must direct the agent to:

- read the current brief and prior history;
- fail closed on stale Setup, wrong property/origin, missing receipt, or policy drift;
- verify every candidate live before selection;
- never fill unused capacity with lower-quality or repeated URLs;
- stop on authentication, CAPTCHA, quota, property mismatch, or provider ambiguity;
- update current status and immutable run artifacts;
- notify on requested URLs, no-work success, repeated data failure, blocked priority URL, or lost automation health according to the approved contract.

Use one named local time plus timezone for a daily schedule when possible. A literal every-24-hours interval is acceptable only when its drift and missed-run behavior are intentional.

Automation states:

```text
NOT_REQUESTED
PLANNED_NOT_APPROVED
APPROVED_NOT_CREATED
AWAITING_FIRST_RUN
HEALTHY
DEGRADED
PAUSED
DISABLED
DELETED
```

Do not mark `HEALTHY` until an actual scheduled run completes with valid evidence, including a legitimate no-work run.

## Receipts and status language

Append one history row per candidate with:

```text
run_id
candidate_url
canonical_url
source_revision
property
mode
eligibility
request_action
provider_path
provider_result
requested_at
approval_reference
evidence_path
next_observation
notes
```

Allowed truthful outcomes include:

- `NO ELIGIBLE URLS` — no candidate passed all gates;
- `REMINDER SENT` — verified queue delivered, no submission attempted;
- `AWAITING BATCH APPROVAL` — exact attended batch ready;
- `REQUESTED` — provider visibly accepted the request;
- `PARTIAL — QUOTA STOP` — earlier rows have receipts; remaining rows were not attempted;
- `BLOCKED — AUTHENTICATION` — user action is required;
- `BLOCKED — PROPERTY OR POLICY` — target falls outside approval;
- `ROUTED FOR REPAIR` — a specific owning stage received the defect;
- `INDEXED` — later current indexed-version evidence confirms index state.

Never say “submitted successfully” when the UI outcome was not observed. Never say “accelerated indexing”; say “requested recrawl/indexing” and report later observations separately.

## Failure handling

- **Wrong property or origin:** stop the whole run; do not search for a convenient alternate property.
- **Authentication, MFA, terms, or CAPTCHA:** mark `AWAITING USER ACTION`; do not circumvent.
- **Quota:** stop new requests, preserve completed receipts, leave remaining rows queued, and notify according to policy.
- **Provider rejection:** preserve the sanitized message, route a source defect when known, otherwise investigate.
- **Already indexed:** skip without consuming a request.
- **Stale Setup or publication evidence:** stop affected URLs before live submission.
- **Browser unavailable in a scheduled run:** follow approved fallback; normally send a reminder and mark the submission not attempted.
- **Partial run:** never replay successful rows automatically; resume from immutable history and current live verification.
- **Three repeated failures after substantive local fixes:** classify provider/external versus local, continue independent URLs when honest, and block or route the affected path.

## Official-source starting points

Provider behavior and quotas change. Recheck official sources during live setup and record the access date:

- [Ask Google to recrawl URLs](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl)
- [Search Console URL Inspection help](https://support.google.com/webmasters/answer/9012289)
- [Search Console URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect)
- [Google Indexing API usage](https://developers.google.com/search/apis/indexing-api/v3/using-api)

Prefer current Google documentation over remembered quotas, community anecdotes, third-party plugins, or claims that a request guarantees faster indexing.
