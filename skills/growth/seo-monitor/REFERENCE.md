# SEO Monitor reference

Use this reference to define comparable scopes, judge maturity, protect winners, classify actions, and configure optional recurring execution safely.

## Prerequisite matrix

| Input | Required content | Failure route |
|---|---|---|
| Setup | Schema-valid overall `VERIFIED`; current canonical, sitemap, provider, consent, and credential-source posture | `seo-setup` for prerequisite drift |
| Foundation | Approved owners, clusters, intent boundaries, protected winners, markets/languages, source limits | `seo-foundation` when research is absent or stale |
| Strategy | Approved actions, page opportunities, baselines, outcomes, guardrails, windows, rollback | `seo-strategy` for ownership or portfolio decisions; page specialist for benchmark and brief |
| Content receipt | Exact target, published time/state, changed files/record, claims, baseline pointer, rollback | `seo-content` for incomplete bounded implementation evidence |
| Current site | Route, response, canonical/index, sitemap, render, links, instrumentation | `INVESTIGATE` or `TECHNICAL FIX` |

A monitor can run before Content exists for whole-site health, but it must not pretend there is a change-specific baseline or receipt.

## Run ID and immutability

Use a UTC run ID such as `2026-08-05T02-30-00Z` and write under:

```text
agent-work/{slug}/seo-monitor/
├── MONITOR-BRIEF.md
├── SEO-MONITOR.md
├── MONITOR-HISTORY.md
├── ACTION-QUEUE.md
└── runs/
    └── {run-id}/
        ├── DATA-INVENTORY.md
        ├── SNAPSHOT.csv
        ├── MONITOR-REPORT.md
        └── receipts/
```

Never rewrite an older run. If normalization or interpretation was wrong, create a corrected run, link the superseded one, and state the correction.

## Normalized observation fields

Use a long-form row where practical:

```text
source_provider
source_account_or_property
retrieved_at
data_available_through
window_start
window_end
market
language
device
channel_or_search_type
query
page
cluster
primary_owner
metric_name
metric_value
metric_precision
source_row_id
baseline_or_observation
notes
```

The `seo-stack normalize` core fields remain canonical when the CLI is used. Monitor may add `data_available_through`, `channel_or_search_type`, `cluster`, `primary_owner`, and `baseline_or_observation` without deleting original semantics.

## Data minimization

- Prefer aggregated query/page/day or query/page/window data.
- Do not persist user IDs, client IDs, IP addresses, cookies, full event payloads, search-console raw responses, or authentication material.
- Avoid low-volume slices that could expose sensitive user intent when aggregate reporting is enough.
- Record environment-variable names, never values.
- Follow the project's consent, privacy, access, retention, and deletion policy.
- Sanitize provider/project identifiers when a durable report does not need them.

## Compatibility gate

Two observations are directly comparable only when every material dimension is equal or an explicit adjustment is justified:

| Dimension | Compatibility question |
|---|---|
| Provider/metric | Is the semantic metric defined the same way by the same provider/report? |
| Property/account | Is it the same verified site/property and channel scope? |
| Search type/channel | Web/image/video/news and organic attribution are not silently mixed |
| Market/language | Same target geography and language, or separately reported |
| Device/context | Same device slice or deliberately `ALL` in both |
| Query/page/owner | Same entity mapping, accounting for approved redirects/URL changes |
| Window length | Same number and type of days when direct delta is claimed |
| Calendar | Comparable weekdays, holidays, seasonality, launches, and outages |
| Availability | Both windows are complete enough under the provider's current reporting behavior |
| Site state | No unaccounted migration, outage, campaign, redesign, or instrumentation change |
| Precision | Exact, rounded, ranged, withheld, and sampled values remain distinguishable |

If a dimension differs, either segment the evidence, normalize with an explicit method, or label the comparison directional/incompatible. Never silently fill missing data with zero.

## Maturity gate

Strategy's 7/14/28-day windows are observation checkpoints, not automatic verdict dates. For each checkpoint record:

- publish/deploy timestamp and first crawl/index evidence;
- provider `data_available_through` and any partial-day exclusion;
- enough comparable days to reduce weekday distortion;
- material seasonality, release, campaign, outage, or migration effects;
- baseline volume and whether the denominator makes the delta unstable;
- whether the intended outcome normally has a longer lag;
- what can be concluded now and what must wait.

Allowed maturity states:

- `MATURE FOR DECISION`
- `DIRECTIONAL ONLY`
- `IMMATURE — WAIT`
- `DATA GAP`
- `INVALIDATED BY SITE OR MEASUREMENT CHANGE`

Do not define universal minimum clicks, impressions, conversions, or rank changes. Use the approved Measurement Plan and report uncertainty.

## Baseline rules

Prefer a baseline captured before implementation. If absent:

1. say there is no true pre-change baseline;
2. use the closest compatible historical or control evidence only as a labelled proxy;
3. do not backfill a convenient window and call it pre-change;
4. make `IMPROVE FUTURE BASELINE CAPTURE` an operational recommendation;
5. avoid causal language.

Keep page and query baselines joined to the Foundation owner map. When a redirect or consolidation changes URLs, preserve the old/new relationship instead of treating the new URL as a fresh unrelated page.

## Metric interpretation guardrails

### Search Console and Bing

- Clicks, impressions, CTR, and average position describe that provider's reported search activity and limitations.
- Average position is an aggregate, not a stable rank for every user.
- Query rows can be withheld or anonymized; visible rows need not sum to site totals.
- Page/query dimensions, search type, country, and device filters change the population.
- Google and Bing remain separate evidence even when they suggest the same direction.

### GA4

- Confirm the intended property, web stream, channel grouping, landing-page dimension, time zone, consent posture, and outcome event.
- Analytics attribution and search-console clicks answer different questions; do not expect equality.
- Consent and blocking behavior can change observed counts without a real demand change.
- A conversion-rate delta includes numerator and denominator; show both.

### Crawl and index evidence

- A live `200`, indexable robots posture, and canonical are prerequisites, not proof of indexation or ranking.
- Search Console inspection is sampled URL evidence, not an exhaustive site status.
- Sitemap success does not guarantee every URL is indexed.
- Rank-check observations are contextual diagnostics, not a substitute for provider data or a basis for automatic rewrites.

## Protected-winner gate

For each protected URL or cluster owner, compare:

```text
availability and final URL
robots and canonical
sitemap and redirect state
index/inspection evidence when applicable
owned query clicks/impressions/CTR/position
organic landing outcomes
internal-link authority
competing pages entering the same query/intent set
content/product factual drift
performance or render regression
```

Any recommendation that could harm a winner names the baseline, downside guardrail, staged change, rollback trigger, and next check. `NO CHANGE` is preferred while evidence is immature or competing explanations remain material.

## Cannibalization evidence

Potential cannibalization is a hypothesis when multiple pages appear for related queries. Strengthen it with:

- repeated query-to-page substitution across compatible windows;
- one intent being split without approved bridge/support roles;
- weaker aggregate clicks/outcomes or unstable ownership after the new asset;
- internal-link/canonical signals that contradict the ownership map;
- content overlap verified at the user-job level.

Do not diagnose cannibalization merely because two pages mention the same term or both receive impressions.

## Recommendation matrix

| Recommendation | Evidence threshold | Default route |
|---|---|---|
| `NO CHANGE` | Healthy, inconclusive, immature, or expected variation; guardrails intact | Next monitor window |
| `INVESTIGATE` | Anomaly, incompatibility, broken measurement, unexpected substitution, or uncertain cause | Diagnosis, then owning stage |
| `REFRESH` | Same owner/intent; bounded usefulness, freshness, factual, product, link, or alignment gap | `seo-content` after approval |
| `CONSOLIDATE` | Strong same-intent overlap and evidence that split ownership harms outcomes | `seo-strategy`, then execution |
| `INDEXING ASSIST` | Approved new or materially updated canonical owner is live and technically ready, is not indexed, and the small individual-request path is proportionate | `seo-indexing` after approval |
| `TECHNICAL FIX` | Verified crawl/index/render/canonical/sitemap/redirect/performance/instrumentation defect | `seo-setup` for prerequisite drift; otherwise diagnosis/Goalpro |
| `NEW STRATEGY` | Material change in user intent, market, competition, product truth, ownership, or portfolio assumptions | `seo-strategy` |

Every exception also carries `confidence: HIGH | MEDIUM | LOW`, competing explanations, evidence that would disconfirm it, and the earliest useful recheck.

## Report template

```markdown
# SEO monitor report: {run-id}

## Decision and scope
## Sources, properties, and freshness
## Baseline and comparison compatibility
## Maturity judgment
## Outcome and leading-signal deltas
## Protected winners and guardrails
## Crawl, index, render, and measurement health
## Ownership and cannibalization
## Findings and competing explanations
## Recommendations, confidence, and routes
## Data gaps
## Next observation
## Satisfaction statement
```

## Action queue fields

```text
action_id
opened_run_id
recommendation
owner_or_page
cluster
protected_winner_impact
evidence_and_confidence
smallest_next_step
routed_skill_or_owner
approval_status
success_signal
rollback_or_stop_signal
recheck_at
state: OPEN | WAITING | APPROVED | IN_PROGRESS | RESOLVED | REJECTED | SUPERSEDED
resolution_run_id
```

The Monitor records actions; it does not advance `APPROVED` or `IN_PROGRESS` unless the user or owning execution stage provides evidence.

## Automation contract

Automation is a separate authorized mutation. Before creation, define:

```text
automation_name
objective and exact prompt
target repository/task and working directory
schedule and timezone
providers and credential-source names
scope and comparison windows
artifact destination and retention
notification destination and threshold
expected cost or quota implications
failure and partial-data behavior
first-run verification
pause/disable/delete path
approval provenance
```

Safety rules:

- Use the host-supported automation system; do not improvise cron, launchd, CI, or cloud jobs unless the user explicitly requests that platform.
- Do not embed tokens or copy credentials into the automation definition.
- Fail closed on wrong property, stale status, unavailable data, schema mismatch, or write attempts.
- Default result is a report, never a content/source mutation.
- Avoid noisy alerts. Notify on defined guardrails, repeated data failure, protected-winner risk, or a requested digest cadence.
- Verify the created schedule and one actual run. Until then, status is `AWAITING FIRST RUN`.

## Three-attempt rule

After three substantive attempts at the same collection or normalization failure, determine whether the blocker is local or external. Continue independent providers when partial reporting remains honest. Record the missing source and do not compute a combined verdict that assumes it succeeded.

## Official-source starting points

Provider delays, dimensions, filters, quotas, and APIs change. Consult current official Google Analytics, Search Console, Google Search Central, Bing Webmaster, schema.org, and target-framework documentation during each live run. Record access dates and label interpretations as inferences where appropriate.
