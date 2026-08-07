# SEO Content reference

Use this reference to validate one brief, build a source and claim ledger, implement safely, and prove the asset without weakening upstream ownership.

## Prerequisite validation

### Setup

- Validate `SEO-SETUP-STATUS.json` against `../seo-setup/schemas/seo-setup-status.schema.json` when discoverable.
- Require `overall_status: VERIFIED` and only `VERIFIED` or defensible `NOT_APPLICABLE` requirements.
- Recheck fragile live conditions implicated by the asset: canonical origin, route/index conventions, sitemap generation, metadata/structured-data architecture, consent, and access needed for publication or verification.

### Foundation

The approved Foundation must name:

- primary cluster and intent;
- current or proposed primary owner;
- supporting and bridge roles;
- overlap exclusions;
- protected winners and baselines;
- market, language, device/context, source dates, and known limitations.

### Strategy

The portfolio row and exact brief must agree on:

```text
brief_id
approval_status and revision
action
primary_cluster
intent and user_job
current_owner and proposed_owner
target_url or target decision
page_role and format
product_value and differentiation
required facts, proof, and primary sources
claims requiring user approval
outline requirements and prohibited overlap
internal sources and destinations
index, canonical, schema, and sitemap posture
conversion/outcome
baseline and measurement windows
rollout, rollback, and protected winners
```

Conflicts are `BLOCKED — RETURN TO SEO STRATEGY`, not drafting decisions.

## Route matrix

| Request | Owner |
|---|---|
| One approved article, guide, glossary, help/education, comparison, or use-case content brief | `seo-content` |
| Landing page with unresolved message, CTA, proof, persuasion, layout, visual direction, or preview | `landing-page` |
| Cluster, intent, owner, URL, portfolio action, or cannibalization is unresolved | `seo-strategy` |
| Only humanize existing approved copy without SEO/content implementation | `prose-humanizer` |
| Implement several heterogeneous approved source/config slices | Goalpro |
| Research competitors, SERPs, demand, or ownership | `seo-foundation` |
| Verify and optionally request indexing for an approved published canonical URL | `seo-indexing` |

When routing to Landing Page, provide the exact brief, primary cluster, intent boundary, protected winners, approved facts, required internal links, index/canonical posture, and measurement contract. Landing Page owns message/design/preview decisions but cannot silently change SEO ownership.

## Authority and risk matrix

| Action | Default authority |
|---|---|
| Read repository, public pages, approved artifacts, and primary sources | Inspection; allowed |
| Draft inside `agent-work/{slug}/seo-content/` | Allowed after valid brief |
| Reversible source edit implementing an exact approved brief | Allowed only when the user requested implementation |
| Material claim, target URL, ownership, index/canonical, redirect, analytics, privacy, or strategy delta | Exact renewed approval |
| High-stakes medical, legal, financial, safety, or policy claim | Exact draft approval before publication |
| External CMS mutation or production deployment | Explicit target/publish authorization |
| Destructive replacement, redirect, unpublish, or removal | Exact target, preview, rollback, and approval |
| Credential use | Existing task-relevant runtime source only; never copied into artifacts |

## Source ledger contract

Use one row per source:

```text
source_id
title
publisher_or_owner
url_or_repository_location
source_type: PRODUCT_IMPLEMENTATION | PRODUCT_DOC | PRIMARY_RESEARCH | STANDARD | REGULATOR | ORIGINAL_DATA | SECONDARY_ORIENTATION | USER_EVIDENCE
published_or_updated_at
accessed_at
market_language_scope
claims_supported
limitations
citation_destination
copyright_or_quote_constraint
```

Primary-source preference is not a license to overstate. A source can be authoritative yet stale, outside the target market, based on a different population, or silent about the claimed causality.

## Claim ledger contract

Use one row per material claim:

```text
claim_id
proposed_claim
claim_type: PRODUCT | QUANTITATIVE | TECHNICAL | COMPARATIVE | REGULATORY | EXPERIENCE | RECOMMENDATION
status: VERIFIED | USER_APPROVED | ATTRIBUTED | UNKNOWN | REJECTED
source_ids
scope_and_qualifiers
approved_wording_constraints
final_location
verification_note
```

Rules:

- `VERIFIED` means the cited evidence directly supports the final scoped wording.
- `USER_APPROVED` records an authorized product/business assertion that cannot be independently proved; do not disguise it as external fact.
- `ATTRIBUTED` keeps the speaker/source visible.
- `UNKNOWN` cannot appear as fact.
- `REJECTED` records a useful prevented error, not content to smuggle into softer prose.
- Competitor claims require current public evidence and neutral framing. Do not imply private knowledge or endorse unsupported comparison tables.
- Statistics retain population, geography, sample, window, unit, and uncertainty needed to interpret them.

## Information-gain test

Before drafting, answer:

1. What user decision or task becomes easier?
2. What verified product truth, synthesis, workflow, example, visualization, or source connection is not already owned by another page?
3. Why should this asset exist instead of improving the current owner?
4. What would make the asset thin, duplicative, or misleading?
5. What evidence would invalidate the brief?

If these do not have concrete answers, return to Strategy with `NO NEW URL` or `REFRESH CURRENT OWNER` as the likely alternatives.

## Draft-quality checklist

### Intent and usefulness

- The first useful answer appears without a padded preamble.
- The structure follows the reader's decisions/tasks, not a keyword list.
- Scope and intended audience are apparent.
- Examples are accurate, runnable or clearly illustrative, and not fabricated firsthand experience.
- Each section contributes new information, synthesis, proof, or action.
- The conclusion points to the next useful product/content action only when relevant.

### Language

- Natural terms replace forced exact-match repetition.
- Titles/headings are descriptive and non-clickbait.
- Claims retain caveats and attribution.
- Domain language remains precise.
- Copy avoids generic AI transitions, inflated importance, forced triples, fake quotations, and repetitive summaries.
- Competitor language is not mimicked.

### Citations and copyright

- Direct quotations are rare, necessary, attributed, and within applicable limits.
- Paraphrases are genuinely rewritten and cited where the claim needs support.
- Search snippets are never evidence.
- Images, charts, code, screenshots, and datasets have verified rights or approved project provenance.
- A citation supports the exact nearby claim, not merely the topic.

## Search implementation checklist

| Surface | Verify |
|---|---|
| URL | Stable, intended owner, correct locale/trailing-slash policy, no accidental collision |
| Title/H1 | Honest, useful, distinguishable, and aligned without requiring exact duplication |
| Description | Accurate invitation, no unsupported promise or keyword list |
| Canonical | Self or approved alternative, absolute when required, correct final origin |
| Robots | Intended index posture in rendered HTTP/meta behavior |
| Sitemap | Included only when indexable and generated at the correct canonical URL |
| Headings | Semantic outline serving readers, one coherent primary heading |
| Structured data | Applicable visible content, valid types/values, no fake author/review/rating/FAQ |
| Internal links | Strategy destinations and source links, descriptive anchors, no ownership confusion |
| External links | Claim-level support, safe attributes per project policy, live or deliberately archived |
| Social metadata | Truthful image/text, correct dimensions/URLs when used |
| Render | Crawlable content in final HTML and no client-only blank state |

Do not add schema merely because a generator supports it. Eligibility for a search feature is not guaranteed and is not a reason to invent or duplicate visible content.

## Accessibility and rendering checklist

- Landmarks and heading hierarchy remain navigable.
- Link text is meaningful out of context; repeated CTAs remain distinguishable when necessary.
- Tables have headers/captions and a responsive alternative or safe overflow.
- Images have appropriate alt text; decorative images are ignored; complex visuals have equivalent explanation.
- Code, formulas, audio, and video have labels, transcripts/captions, controls, and keyboard behavior when applicable.
- Footnotes/citations are reachable and return behavior is usable when the project supports it.
- Text survives 200% zoom, narrow screens, long strings, localization, and user font settings.
- New media does not cause avoidable layout shift or excessive payload.

## Verification ladder

1. **Factual:** compare final rendered copy with claim and source ledgers.
2. **Ownership:** compare URL, intent, headings, and links with Foundation/Strategy.
3. **Static:** parse content/frontmatter/schema; check links/assets/citations.
4. **Project:** format, lint, type, tests, content build, full build.
5. **Rendered:** representative viewports, zoom, keyboard, themes/locales, console/network.
6. **Search:** final HTML/head, response/index headers, canonical, sitemap, structured data.
7. **Target:** observed local/preview/CMS/production result at the authorized target.
8. **Receipt:** baseline pointer, changed target, rollback, limitations, Monitor handoff.

A lower rung never substitutes for a higher one. A successful build is not production publication, and rendered presence is not indexation.

## Content plan template

```markdown
# SEO content plan

## Brief, revision, and approval
## Owner, intent, and protected winners
## Target and authority
## Source and claim plan
## Information gain and content structure
## Source/CMS implementation
## Search, links, schema, and accessibility
## Verification gates
## Publish or deployment path
## Rollout and rollback
## Material deltas and approval
```

## Content receipt template

```markdown
# SEO content receipt

## Brief and approval provenance
## Final target and status
## Owner, cluster, intent, and action
## Changed files or records
## Claims, sources, and rejected claims
## Search and internal-link posture
## Project and rendered verification
## Published-target evidence
## Indexing handoff
## Baseline and monitor windows
## Rollback
## Limitations and follow-up
```

## Three-attempt rule

After the same gate fails through three substantive fixes, decide whether the defect is local or external. Keep working on independent checks when safe. Record `BLOCKED` and ask one focused question when access, approval, provider state, deployment, or an upstream ownership decision is required.

## Official-source starting points

Provider and search guidance changes. During live work, consult current official sources relevant to the asset, including Google Search Central, Search Console, Bing Webmaster guidance, schema.org, WCAG/WAI guidance, and the target framework/CMS documentation. Record access dates and do not turn recommendations into guaranteed ranking outcomes.
