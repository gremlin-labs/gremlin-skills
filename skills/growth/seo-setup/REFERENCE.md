# SEO Setup reference

Use this reference to classify prerequisites, choose safe setup paths, and verify evidence. Provider interfaces and APIs drift; consult current official documentation during every live run and record access dates.

## Required evidence matrix

Every row is independently classified. A group is complete only when all applicable rows are `VERIFIED` or `NOT APPLICABLE`.

### Production identity

| Requirement | Verification evidence | Common false positive |
|---|---|---|
| Canonical production origin | Authoritative project/deployment evidence plus live HTTPS response | Guessing from README or package metadata |
| Preferred host and protocol | Representative HTTP, HTTPS, apex, and `www` redirect chains end once at the intended origin | Browser address bar looks correct after multiple hops |
| Environment boundary | Production, preview, staging, and local index behavior are intentional | Preview deployment accidentally indexable |
| Ownership | Operator and account boundary identified without exposing credentials | Agent assumes the signed-in account is the intended owner |

### Crawl and index foundation

| Requirement | Verification evidence | Common false positive |
|---|---|---|
| `robots.txt` | Live final response, valid syntax, intended crawler policy, sitemap declaration when appropriate | File exists only in source |
| Sitemap | Live 200 response, valid XML/index, canonical URLs, correct locale/alternate behavior, no redirect/error/noindex leakage | Search console says “submitted” while URL is stale |
| Canonicals | Representative rendered HTML/header evidence across indexable, duplicate, paginated, localized, and parameterized routes | Framework metadata object looks correct before rendering |
| Index directives | Representative `index`, `noindex`, `follow`, headers, auth/error routes, and environment rules agree | Robots blocks a route and hides an unintended `noindex` |
| Foundational metadata | Unique truthful title/description strategy, social metadata, favicon, and one semantic page title/H1 relationship on representative templates | Every page inherits the homepage title |
| Structured data | Only eligible, truthful entities render; syntax and visible-content parity validate | Adding FAQ, Review, Offer, or price claims because schema exists |
| Status behavior | Redirects, 404/410, soft-404 risk, and canonical error routes are intentional | Custom error page returns HTTP 200 |
| Internal discovery | Primary navigation/hub paths reach intended canonical pages | Sitemap is the only discovery path |
| Performance baseline | Representative mobile/desktop delivery and Core Web Vitals source are recorded when available | One lab score is called production performance |

Do not turn Setup into a full mature-site technical audit. Repair missing or clearly broken prerequisites; route systemic crawl/index/content debt to a later strategy or audit initiative.

### GA4

Required evidence:

1. Intended Google Analytics account, GA4 property, and web data stream identified.
2. Production URL and stream configuration match the canonical site.
3. Tag is implemented once through a deliberate source or Tag Manager owner.
4. Approved consent/privacy posture is implemented before data collection where applicable.
5. Network/runtime evidence proves tag delivery on intended pages and suppression where required.
6. A sanitized test visit/event is visible in Realtime or DebugView, or another current first-party observation path.
7. Referral exclusions, internal traffic, key events, Ads linking, retention, and enhanced measurement are classified `VERIFIED`, `NOT APPLICABLE`, or deferred with an owner; do not enable them by default.

Use the Analytics Admin API when current scopes and account authority are available. Account creation or terms acceptance may require signed-in user action. Never create a replacement property before inspecting existing account summaries and streams.

### Google Search Console

Required evidence:

1. Property type and identifier fit the canonical and subdomain/locale architecture.
2. Ownership is verified with a durable method controlled by the intended owner.
3. The authenticated user has the intended permission level.
4. The live canonical sitemap is submitted and readable.
5. Representative query/site access succeeds even when a new property has no performance rows.
6. Representative URL Inspection read access succeeds when supported.

The Site Verification API can request and verify file, meta, Analytics, Tag Manager, DNS TXT, or DNS CNAME tokens. The Search Console API can add sites, manage sitemaps, query Search Analytics, and inspect indexed state. General indexing requests remain a UI action; do not misuse the restricted Indexing API. After Setup verifies these prerequisites, route ongoing new-page request queues to `seo-indexing`.

### Google Ads Keyword Planner

At least one path must be `VERIFIED`:

- **UI path:** intended user/account can open Keyword Planner, enter a harmless seed, set an explicit market/language/network, and view or export results without creating a campaign.
- **API path:** intended client and manager accounts, OAuth principal, developer token/access level, customer IDs, and `KeywordPlanIdeaService` request succeed with a harmless seed.

Record whether reported volume is exact, rounded, ranged, withheld, or unavailable. Label Google Ads competition as paid-search advertiser competition; never call it organic keyword difficulty.

API credentials are optional when the UI path works. The CLI may normalize a UI export for Foundation. No ad, budget, billing method, or campaign is created by Setup.

### Bing Webmaster Tools

Required evidence:

1. Intended site is added and ownership verified.
2. OAuth or user API-key access is available when API use is chosen; values remain secret.
3. Live sitemap is submitted and accessible.
4. Representative query/crawl/site read succeeds even if a new site has no rows.

IndexNow is optional. Classify it based on publishing frequency, framework support, current ownership, and operational value. Accepted submission proves receipt, not indexing.

## Setup-plan schema

`SETUP-PLAN.md` contains:

```md
# SEO setup plan

## Revision and scope
## Product and privacy context
## Current verified strengths
## Proposed source changes
## Proposed external-provider changes
## User-only actions
## Material risks and authority
## Verification matrix
## Rollback
## Approval provenance
```

For each action include a stable ID such as `SETUP-GSC-01`, exact target, current state, proposed state, method, owner, prerequisite, verification, failure signal, and rollback.

## Machine status contract

The canonical JSON shape is:

```json
{
  "schema_version": 1,
  "slug": "launch-organic-growth",
  "generated_at": "2026-08-04T20:15:00Z",
  "canonical_origin": "https://example.com",
  "overall_status": "INCOMPLETE",
  "requirements": [
    {
      "id": "gsc.sitemap",
      "group": "google_search_console",
      "required": true,
      "status": "AWAITING USER ACTION",
      "summary": "Domain ownership verification is pending",
      "evidence": [],
      "verified_at": null,
      "source": "computer_use",
      "user_action": "Approve the displayed DNS TXT record with the domain owner",
      "not_applicable_reason": null
    }
  ],
  "credential_sources": [
    {
      "provider": "google",
      "kind": "application_default_credentials",
      "present": false
    }
  ],
  "artifact_paths": {
    "audit": "agent-work/launch-organic-growth/seo-setup/AUDIT.md",
    "quality_report": "agent-work/launch-organic-growth/seo-setup/QUALITY-REPORT.md"
  }
}
```

Rules:

- `overall_status` is `VERIFIED` only when every required row is `VERIFIED` or `NOT_APPLICABLE` with a non-empty reason.
- Secret values, raw tokens, cookies, authorization headers, and provider response bodies are forbidden.
- Evidence contains concise receipts such as status codes, sanitized IDs, timestamps, paths, commands, or screenshot references.
- Timestamps use UTC RFC 3339.
- `source` is `repository`, `live_http`, `api`, `computer_use`, `user_evidence`, or `manual_test`.

## Durable project documentation

Prefer the project's current SEO documentation location. If none exists, use `docs/seo/SEO-SETUP.md` and link it from the nearest documentation index.

Required sections:

```md
# SEO setup

## Canonical site and environments
## Crawl and index architecture
## Analytics and consent
## Google Search Console
## Google Ads Keyword Planner
## Bing Webmaster Tools and IndexNow
## Credential ownership and rotation
## Verification and troubleshooting
## Known limitations and next review
```

Document non-secret property/account identifiers only when they help operators distinguish targets. Name credential sources, owners, and rotation procedures without values.

## Project gate discovery

Detect the toolchain from manifests and repository instructions. Run focused and full gates proportionally:

- TypeScript/JavaScript: project formatter, typecheck, lint, tests, production build, rendered browser checks.
- Python: formatter/lint/type checks when configured, tests, framework route checks.
- Ruby, Go, Rust, PHP, Java, and static-site systems: use project-native equivalents.
- CMS/no-code: export or preview checks, live rendered inspection, provider receipts, and rollback evidence.

Do not install a new toolchain merely to satisfy a generic checklist.

## Three-attempt rule

After the same gate fails following three substantive local fixes, classify whether the blocker is local or external. Continue independent safe work. For an external or authority-bound blocker, record `BLOCKED` or `AWAITING USER ACTION` and ask one focused question. Do not weaken the verification requirement.

## Official-source starting points

Refresh these during live use:

- Google Analytics Admin API: `https://developers.google.com/analytics/devguides/config/admin/v1`
- Google Site Verification API: `https://developers.google.com/site-verification/v1/invoking`
- Search Console API: `https://developers.google.com/webmaster-tools/v1/api_reference_index`
- Search Console URL Inspection: `https://support.google.com/webmasters/answer/9012289`
- Google Ads keyword ideas: `https://developers.google.com/google-ads/api/docs/keyword-planning/generate-keyword-ideas`
- Bing Webmaster API: `https://learn.microsoft.com/en-us/bingwebmaster/`
- IndexNow: `https://www.bing.com/indexnow/getstarted`
