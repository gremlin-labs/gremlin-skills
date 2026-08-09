# SEO Strategy reference

Use this reference to validate prerequisites, choose portfolio actions and candidate page roles, define page opportunities, prevent cannibalization, prioritize work, and produce bounded specialist or technical handoffs.

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
- source and evidence ledgers with windows, evidence strength, and limitations;
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
benchmark_state
evidence_gaps
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
3. SERP evidence supporting investigation of the proposed page role;
4. no appropriate existing owner;
5. a credible differentiated-value hypothesis and proof path for the specialist to test;
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
| Comparison or “best” evaluation | Editorial comparison/hub | Page-specialist benchmark; real evaluation evidence if comparative claims survive |
| Recurring entities/items | Category/directory/detail | Unique value, inventory quality, lifecycle and rights/governance |
| Query variant only | Existing owner | No distinct page warranted |

Treat this as a hypothesis matrix, not a template. Direct SERP and user evidence wins.

## Page-opportunity contract

Each entry in `PAGE-OPPORTUNITIES.md` uses:

```md
## {item ID}: {cluster or user job}

### Portfolio decision and ownership
- Action:
- Current/proposed URL:
- Candidate page-role hypothesis:
- Cluster and primary owner:
- Primary/supporting/excluded intent:
- Market/language:
- Cannibalization result:

### User and product outcome
- Audience and arrival intent:
- Problem/job:
- Desired outcome:
- Conversion or next-step path:

### Evidence strength and gaps
- First-party evidence:
- Demand/SERP evidence:
- Observed:
- Inferred:
- Hypotheses for page-specific testing:
- Unsupported ideas to exclude:
- Material evidence gaps:

### Portfolio relationship
- Same-cluster links and anchor roles:
- Optional bridge:
- Protected assets:
- Baseline and measurement gate:

### Specialist route
- Dependencies and owner:
- Recommended executor:
- Benchmark state:
- Failure/invalidation signal:
```

Do not include working titles, outlines, module lists, proof formats, testing or methodology requirements, final metadata, or page-content acceptance criteria. The specialist derives and challenges those only after applying [the page-quality contract](contracts/seo-page-quality.md).

## Specialist boundary

- `landing-page` owns page-specific search benchmarking, message, title, proof, CTA, persuasion order, layout, preview, approval, and implementation.
- `seo-content` owns page-specific search benchmarking, editorial position, title, catalogue durability, sources, structure, brief, approval, implementation, and comparative review.
- Strategy's owner, cluster, prohibited overlap, protected winners, baseline, and measurement contract remain binding inputs.
- A specialist may return `REVISE`, `NO PAGE`, or `BLOCKED`; Strategy does not override that verdict by restating its portfolio hypothesis.
- Missing specialist availability is an operational blocker, not permission to substitute Goalpro or generic prose generation.

Truth and competitiveness are independent downstream gates. Removing an unsupported comparison or “best” claim does not make bland, indistinguishable wording acceptable. Methodology, testing, authorship, tables, tools, examples, or other modules are required only when the specialist's actual page claims and benchmark support them.

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
2. One owner/page-benchmark intervention.
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

Create `GOALPRO-INPUT.md` only after explicit implementation approval for bounded technical work that does not create or rewrite page content. Follow [Goalpro's direct handoff contract](contracts/goalpro-handoff.md) and include:

- approved strategy revision and exact portfolio item IDs;
- source Foundation and Setup artifacts;
- ordered reversible slices;
- “Done when …” criteria for redirects, canonicals, index directives, sitemaps, internal links, or other approved technical items;
- protected assets and prohibited changes;
- project gates and representative browser/runtime checks;
- quality applicability from [Goalpro's quality contract](contracts/execution-quality.md);
- release, monitoring, rollback, external/manual, and sensitive-data boundaries;
- material post-approval deltas and honest readiness state.

Never use Strategy's Goalpro handoff to implement editorial copy, titles, page modules, landing-page persuasion, or page structures. Those require the owning page specialist's benchmark, approval, and execution contract.

## `SEO-STRATEGY.md` consumption index

Required sections:

```md
# SEO strategy

## Approval, revision, and scope
## Product and search outcomes
## Prerequisite sources and freshness
## Portfolio decisions and protected assets
## Landing-page opportunities
## Editorial opportunities
## Internal-link and technical plan
## Prioritized roadmap
## Measurement, rollout, and rollback
## Rejected/deferred alternatives
## Risks, unknowns, and revalidation triggers
## Implementation approval and handoff
```

The index links detailed files and surfaces material deltas from Foundation. Do not copy the full keyword corpus into it.
