# SEO Foundation reference

Use this reference for competitor taxonomy, page inspection, SERP evidence, keyword normalization, opportunity ranking, clustering, and page ownership.

## Evidence-strength contract

Classify every material conclusion:

- `OBSERVED` — directly visible in a dated and scoped page, SERP, product source, or first-party dataset.
- `INFERRED` — interpretation supported by named observations; record reasoning and credible alternatives.
- `HYPOTHESIS` — a testable idea for later Strategy or page-specialist investigation; never an implementation requirement.
- `UNSUPPORTED` — unavailable, contradicted, or too weak to carry downstream.

Record source, market/language, query or page scope, retrieval date, counterevidence, limitations, and revalidation trigger. A repeated module, phrase, testing claim, methodology page, outline, page length, or ranking position does not establish causality or adoption value.

## Competitor taxonomy

Classify every domain independently:

- `DIRECT BUSINESS COMPETITOR` — solves the same user job with a substitutable product.
- `PARTIAL BUSINESS COMPETITOR` — overlaps one capability, segment, platform, or market.
- `ORGANIC SERP COMPETITOR` — repeatedly ranks for relevant queries but may have a different business model.
- `PUBLISHER OR REVIEWER` — editorial/listicle/comparison owner influencing discovery.
- `MARKETPLACE OR DIRECTORY` — app store, catalogue, directory, community, or aggregator.
- `ADJACENT SUBSTITUTE` — users may choose it to achieve the outcome differently.
- `IRRELEVANT OR EXCLUDED` — superficially similar but outside product, market, intent, safety, or user scope.

One domain may have multiple roles; classify per page/query when needed. Record evidence, confidence, and who approved exclusions.

## Candidate competitor record

```md
### example.com

- Classification: DIRECT BUSINESS COMPETITOR; ORGANIC SERP COMPETITOR
- Why it matters: Ranks for the primary transactional family and targets the same user job
- Evidence: query/date/result and product-page source
- Markets/languages: US English
- Representative pages: `/`, `/product`, `/guides/topic`
- Include: YES
- User decision: approved on {date}
- Revisit when: a new product line or market changes the overlap
```

## Public inspection safety

- Use ordinary public search and page access.
- Respect explicit access restrictions, bot controls, rate limits, and terms.
- Prefer a bounded representative page set over a full crawl.
- Identify final URL, status, canonical, render dependence, and visible update date.
- Do not authenticate into competitor systems, submit forms, create accounts, or download restricted assets merely for research.
- Quote minimally; summarize patterns and cite URLs/dates.

## Page analysis record

For each representative page capture:

| Field | Purpose |
|---|---|
| Competitor and URL | Evidence identity |
| Retrieval date and final status | Freshness and accessibility |
| Page role | Homepage, product, category, hub, article, comparison, tool, directory, locale |
| Intended user and intent | What job/query the page appears to serve |
| Title, description, H1, H2/H3 outline | Search and information hierarchy |
| Visible proof and claims | Evidence, screenshots, demos, reviews, pricing, testing, citations |
| CTA and conversion path | Desired user action |
| Content format and depth | Structure and useful coverage, not word-count worship |
| Canonical, robots, hreflang, schema | Technical posture where public evidence permits |
| Internal links and anchors | Hubs, support spokes, bridges, authority flow |
| Recurring entities/phrases | Topic language after boilerplate filtering |
| Distinctive strategy | What is meaningfully different from sibling pages |
| Weakness, risk, or uncertainty | Thinness, overlap, unsupported claim, inaccessible evidence |
| Investigation relevance | Why a later portfolio or page-specific study may examine it; never an adoption instruction |

## Term and phrase extraction

Do not rank competitor words by counts alone. Normalize case, punctuation, singular/plural variants, stop words, brand terms, legal/footer/navigation boilerplate, and repeated template chrome. Preserve meaningful multi-word phrases and entities.

Weight evidence qualitatively:

1. Page title, H1, canonical page role, and primary anchor ownership.
2. Repeated H2/H3 concepts, hub labels, breadcrumb/category structure, and schema entities.
3. Internal anchor patterns and supporting-page recurrence.
4. Body phrases linked to a distinct user question, task, objection, or outcome.
5. Raw frequency only as supporting evidence after boilerplate removal.

Separate brand language, product category, feature/capability, platform/use case, problem, question, comparison, audience, and modifier terms.

## SERP snapshot contract

Each query sample records:

```text
engine
query
retrieved_at
market_or_location
language
device_or_context
signed_in_state_when_known
result_position_in_sample
result_type
domain
url
title
snippet_summary
serp_features
intent_classification
limitations
```

Use position only as “observed position in this sample.” Avoid a bare “ranks #3” claim. Note localization, personalization, ads, AI summaries, local packs, video, app stores, shopping, discussions, and other features that affect intent.

## Iterative discovery stop

After the first approved competitor inspection:

1. Search the extracted primary and supporting intent families.
2. Add domains that recur materially or reveal a distinct page type/intent.
3. Classify them and inspect representative pages.
4. Re-run only the affected query families.
5. Stop when the next pass adds no material competitor, intent, or page-role evidence, or when added evidence cannot change ownership/priorities.

Record the stop rationale. Do not promise exhaustive coverage of the web.

## First-party evidence

Prefer query-by-page exports over top-query or top-page screenshots when ownership decisions matter. Preserve:

- provider/property/site;
- requested and actual date window;
- search type, market/country, language, device, page, and query filters;
- clicks, impressions, CTR, position, conversions, and any aggregation/row-limit notes;
- screenshots only as directional evidence when filters/windows are truncated.

Never add or directly compare unmatched provider totals. Bing may validate a query family without justifying a Google-page rewrite.

## Keyword Planner evidence

For each retrieval record:

- account/client scope without secrets;
- UI or API path;
- seed type and value;
- market/location, language, network, and date options;
- returned keyword, average monthly searches or range, trend, paid competition, competition index, bid range, and precision/availability;
- retrieval date and quota/access limitations.

Seed from product truth, approved competitor pages, current queries, and SERP language. Whole-site competitor seeds may use public information; they do not prove the competitor intentionally targets every returned idea.

## Normalized keyword-demand fields

`KEYWORD-DEMAND.csv` uses:

```text
keyword
normalized_keyword
intent
market
language
source
source_window
source_precision
search_volume_or_range
trend
paid_competition
gsc_clicks
gsc_impressions
gsc_ctr
gsc_position
bing_clicks
bing_impressions
bing_ctr
bing_position
current_owner
competitor_recurrence
serp_page_types
product_fulfilment
protected_winner
cannibalization_risk
opportunity_band
confidence
notes
```

Leave unavailable metrics empty with an explanation; do not write zero.

## Opportunity ranking

Rank into explicit bands such as `P0`, `P1`, `P2`, `PARK`, and `REJECT`, or use a project-approved score. Evaluate:

- user value and product/business fit;
- search intent and truthful fulfilment;
- demand, trend, current traction, and conversion evidence;
- SERP intent and observed page-role mix;
- competitor coverage and differentiation opportunity;
- current authority and internal-link support;
- protected-winner and cannibalization risk;
- evidence/claim cost, content/engineering effort, and reversibility;
- uncertainty and cheapest validation experiment.

Do not assign fixed universal weights. If numeric weights are used, document and approve them. High volume with weak product fit or high harm risk can be `REJECT`. Any proposed page role remains `HYPOTHESIS` until Strategy and the owning page specialist validate it.

## Cluster contract

Each cluster in `KEYWORD-CLUSTERS.md` includes:

```md
## {cluster name}

- User intent and outcome:
- Primary query family:
- Supporting queries and modifiers:
- Excluded or neighboring intents:
- Current/proposed owner:
- Same-cluster support pages:
- Optional cross-cluster bridge:
- Product fulfilment and proof:
- First-party evidence:
- External demand and SERP evidence:
- Protected assets:
- Cannibalization rules:
- Unknowns and revalidation trigger:
```

## Page ownership rules

- Assign one primary owner per compatible intent family.
- Broad anchors route to broad hubs; narrow anchors route to narrow owners.
- A homepage may own a head term when evidence supports it; do not force every keyword into a dedicated landing page.
- Distinguish browser, desktop, mobile, product, informational, comparison, directory, and local intent.
- Preserve a ranking URL unless stronger matched-window and product evidence supports a controlled change.
- New keywords can map to an existing owner, a supporting section, a future candidate, or `NO PAGE WARRANTED`.
- Record redirects, noindex pages, locale alternates, and known duplicate/canonical state.

## Protected-winner record

```md
### https://example.com/current-owner

- Owned query/intent:
- Source and window:
- Evidence of strength:
- Frozen elements: URL, title, H1, canonical, primary intent, or structure
- Allowed low-risk work:
- Change gate:
- Measurement window:
- Rollback evidence:
```

Protection is proportional. It does not freeze factual corrections, security, accessibility, or broken behavior, but those changes still require careful measurement.

## `SEO-FOUNDATION.md` consumption index

Required sections:

```md
# SEO foundation

## Approval and freshness
## Product, market, language, and outcome
## Source ledger and limitations
## Evidence ledger and claim strength
## Current site and first-party baseline
## Competitor map
## SERP and page-strategy findings
## Ranked keyword opportunities
## Keyword clusters
## Page ownership and protected winners
## Risks, unknowns, and revalidation triggers
## Downstream contract for SEO Strategy
```

The downstream contract names required detailed artifacts and flags incompatible or stale scopes. It never grants implementation approval and never prescribes titles, modules, methodology, testing, proof formats, outlines, or acceptance criteria.
