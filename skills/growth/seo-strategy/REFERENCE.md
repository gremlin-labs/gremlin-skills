# SEO Strategy reference

Use this reference to validate prerequisites, choose portfolio actions and page types, define briefs, prevent cannibalization, prioritize work, and produce execution-ready handoffs.

## Prerequisite validation

### Setup

Require:

- schema-supported `SEO-SETUP-STATUS.json`;
- `overall_status: VERIFIED`;
- matching canonical origin and environment;
- current access path to needed GSC/Bing/GA4/Keyword Planner evidence;
- no applicable `AWAITING USER ACTION`, `BLOCKED`, or `FAILED` requirement;
- live revalidation of fragile sitemap, canonical origin, and provider access facts.

### Foundation

Require:

- explicit user approval and revision/freshness record;
- product, market, language, engine, and device/context scope;
- source ledger with windows and limitations;
- current baseline, competitor classification, page analysis, and SERP samples;
- normalized keyword demand;
- clusters, owners, protected winners, exclusions, cannibalization rules, and unknowns.

Route back only what is missing. Do not restart a valid Foundation because one narrow query family needs refresh.

## Portfolio row contract

`CONTENT-PORTFOLIO.csv` uses:

```text
item_id
current_url
proposed_url
page_role
cluster
primary_intent
market
language
current_owner
proposed_owner
action
status
protected_winner
frozen_elements
first_party_evidence
external_demand_evidence
serp_page_type
product_fulfilment
user_outcome
conversion_path
same_cluster_support
cross_cluster_bridge
cannibalization_risk
claim_evidence_cost
implementation_effort
reversibility
priority_band
dependencies
recommended_executor
measurement_gate
notes
```

Leave unavailable values empty with an explanation. Use stable item IDs across revisions.

## Action decision rules

### Protect

Use when compatible first-party evidence shows the page owns a valuable query/intent and current behavior is truthful and useful. Define exactly what is frozen and what low-risk work remains allowed.

### Refresh

Use when the owner is correct but content, proof, snippet, accessibility, conversion path, technical posture, or freshness is weak. Preserve primary intent unless an approved ownership change exists.

### Create

Require all:

1. distinct user intent/outcome;
2. truthful product or editorial fulfilment;
3. SERP evidence for the proposed page role;
4. no appropriate existing owner;
5. meaningful differentiated value and proof path;
6. viable internal-link role and maintenance owner;
7. explicit cannibalization and measurement plan.

### Consolidate or redirect

Require compatible ownership evidence, destination relevance, content/link/proof migration, redirect-chain and canonical plan, pre-change baseline, rollback limits, and post-change query/page monitoring. Do not redirect merely because two titles share words.

### Noindex

Use when the surface has product/user value but lacks unique search value, is provisional, duplicates an approved owner, exposes thin/filtered/private state, or needs a launch measurement gate. Define `follow` behavior and sitemap/internal-link posture.

### Remove

Require no remaining user/product/search value, no needed inbound/internal dependency, an appropriate 404/410/redirect decision, sitemap/link cleanup, and rollback/archive policy.

### Investigate, park, or no action

Use when evidence, readiness, capacity, seasonality, traffic maturity, or risk makes mutation premature. Name the cheapest experiment or revalidation trigger.

## Page-role decision matrix

| Observed intent/job | Candidate owner | Evidence gate |
|---|---|---|
| Product category or capability selection | Product/category landing page | Product fulfilment, transactional/commercial SERP mix, conversion path |
| Platform or use-case compatibility | Platform/use-case page | Distinct setup/outcome and no overlap with broad capability owner |
| Browser task or utility | Tool page | Working tool and utility-led SERP |
| Explanation or definition | Hub/guide | Informational SERP and authoritative sources |
| Procedure or troubleshooting | Guide/blog/support article | Distinct task, current product flow, recoverable steps |
| Comparison or “best” evaluation | Editorial comparison/hub | Reproducible methodology, fair evidence, ownership distinct from product page |
| Recurring entities/items | Category/directory/detail | Unique value, inventory quality, lifecycle and rights/governance |
| Query variant only | Existing owner | No distinct page warranted |

Treat this as a hypothesis matrix, not a template. Direct SERP and user evidence wins.

## Brief contract

Each brief uses:

```md
## {brief ID}: {working title}

### Decision and ownership
- Action:
- Current/proposed URL:
- Page role:
- Cluster and primary owner:
- Primary/supporting/excluded intent:
- Market/language:
- Cannibalization result:

### User and product outcome
- Audience and arrival intent:
- Problem/job:
- Desired outcome:
- Product/content promise:
- Conversion or next-step path:

### Evidence and differentiation
- First-party evidence:
- Demand/SERP evidence:
- Competitor patterns to adapt:
- Patterns/claims to reject:
- Product/source proof required:
- Allowed/prohibited claims:

### Content and experience
- Direct answer or value proposition:
- Information hierarchy/outline:
- Proof, visuals, demos, tables, tools, or examples:
- Objections, safety, and limitations:
- Accessibility and responsive needs:

### Search and distribution
- Working title/description/H1 hypotheses:
- Index/canonical/hreflang posture:
- Structured-data eligibility:
- Same-cluster links and anchor roles:
- Optional bridge:

### Delivery and verification
- Dependencies and owner:
- Recommended executor:
- Acceptance criteria:
- Rollout/rollback:
- Baseline and review windows:
- Failure/invalidation signal:
```

Working snippet/headline hypotheses are inputs to implementation and testing, not guaranteed search-result display.

## Landing-page-specific requirements

- Verified product callouts and feature-to-benefit framing.
- Arrival intent and CTA ladder.
- Proof and objection plan.
- Product demonstration/visual evidence needs.
- Conversion tracking already authorized or separately proposed.
- Explicit handoff to `landing-page` when message, design, or preview decisions remain.
- Strategy's page owner, cluster, prohibited overlap, and measurement contract remain binding inputs.

## Editorial-specific requirements

- Direct question/task and intended reader.
- Primary sources and freshness requirements.
- Author/tester/methodology disclosure where claims rely on testing or expertise.
- Examples, screenshots, tables, tools, or original evidence that create value beyond paraphrase.
- Fact, product, legal/safety, and citation review.
- Clear distinction between editorial and transactional owners.
- No target word count unless a minimum is tied to specific coverage obligations; competitor length is context, not a quota.

## Internal-link map

Each row includes:

```text
source_url
source_role
destination_url
destination_owner
anchor_family
user_reason
relationship
placement_or_component
existing_or_proposed
template_or_manual
risk
removal_or_migration_behavior
verification
```

Relationship is `PRIMARY HUB`, `SAME-CLUSTER SUPPORT`, `CROSS-CLUSTER BRIDGE`, `CONVERSION PATH`, `PRODUCT HELP`, or `CONTEXTUAL CITATION`. Keep one optional cross-cluster bridge when useful; do not force it.

## Cannibalization gate

Before approving `CREATE` or a primary-intent rewrite:

1. List existing pages receiving the query or close variants.
2. Compare intent and page type, not just keywords.
3. Inspect matched-window query-by-page evidence when available.
4. Identify current internal anchors, canonicals, redirects, and sitemap owners.
5. Define one resulting owner and subordinate roles.
6. Prove distinct value or choose refresh/consolidation/no page.
7. Record a pre-change baseline, rollback boundary, and review window.

## Priority model

Use explicit bands rather than false precision unless the project approves weights:

- `P0 PROTECT/REPAIR` — valuable winner, correctness/indexation break, or high-risk ownership conflict.
- `P1` — strong user/product value, evidence, readiness, and feasible differentiation.
- `P2` — credible opportunity with a dependency or uncertainty.
- `EXPERIMENT` — cheapest test needed before commitment.
- `PARK` — valid but not ready/capacity-aligned.
- `REJECT` — weak fit, unsupported claim, harmful overlap, unsafe topic, or no useful page.

For each priority state outcome, evidence, guardrail, effort, reversibility, dependency, and invalidation signal.

## Roadmap slicing

Prefer vertical, measurable slices:

1. Baseline and guardrails.
2. One owner/brief intervention.
3. Required internal-link/technical delivery.
4. Build/render/release verification.
5. Index/crawl/provider observation.
6. 7/14/28-day or evidence-appropriate review.
7. Continue, revert, strengthen, consolidate, or stop.

Do not batch unrelated clusters merely because they share a template.

## Measurement plan

Classify metrics by role:

- **Acquisition:** impressions, clicks, CTR, position distribution, indexed coverage, crawl state.
- **Engagement:** qualified landing engagement, tool use, scroll/read completion where authorized and meaningful.
- **Conversion:** approved product/account/download/store/contact actions; do not equate clicks with installs or revenue.
- **Guardrails:** existing owner traffic, branded/non-branded mix, neighboring-page ownership, performance, errors, privacy/consent.
- **Quality:** factual accuracy, broken links, render/accessibility, structured-data validity, freshness.

Record provider, property, query/page filters, market, language, device, requested/actual window, baseline date, release SHA/date, expected evidence maturity, and decision rule. Use matched windows for before/after claims and label external influences.

## Goalpro handoff

Create `GOALPRO-INPUT.md` only after explicit implementation approval. Follow [Goalpro's direct handoff contract](contracts/goalpro-handoff.md) and include:

- approved strategy revision and exact portfolio item IDs;
- source Foundation and Setup artifacts;
- ordered reversible slices;
- “Done when …” criteria per brief and shared infrastructure;
- protected assets and prohibited changes;
- project gates and representative browser/runtime checks;
- quality applicability from [Goalpro's quality contract](contracts/execution-quality.md);
- release, monitoring, rollback, external/manual, and sensitive-data boundaries;
- material post-approval deltas and honest readiness state.

## `SEO-STRATEGY.md` consumption index

Required sections:

```md
# SEO strategy

## Approval, revision, and scope
## Product and search outcomes
## Prerequisite sources and freshness
## Portfolio decisions and protected assets
## Landing-page plan
## Editorial plan
## Internal-link and technical plan
## Prioritized roadmap
## Measurement, rollout, and rollback
## Rejected/deferred alternatives
## Risks, unknowns, and revalidation triggers
## Implementation approval and handoff
```

The index links detailed files and surfaces material deltas from Foundation. Do not copy the full keyword corpus into it.
