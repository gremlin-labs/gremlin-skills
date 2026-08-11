# Landing Page Reference

## Contents

- [Evidence and product truth](#evidence-and-product-truth)
- [Message and benefit framing](#message-and-benefit-framing)
- [Page strategy without templates](#page-strategy-without-templates)
- [Calls to action](#calls-to-action)
- [Product highlights proof and objections](#product-highlights-proof-and-objections)
- [Copy humanization](#copy-humanization)
- [Visual and interaction craft](#visual-and-interaction-craft)
- [SEO Stack composition](#seo-stack-composition)
- [SEO editorial change control](#seo-editorial-change-control)
- [SEO GEO and AEO](#seo-geo-and-aeo)
- [TurbulenceJS motion](#turbulencejs-motion)
- [Implementation and quality](#implementation-and-quality)
- [Artifact schemas](#artifact-schemas)
- [Worked examples](#worked-examples)
- [Research provenance](#research-provenance)

## Evidence and product truth

Use the strongest available source for each statement:

1. Explicit current user decision or approved message brief.
2. Shipped behavior verified in current source/runtime.
3. Current product, pricing, support, or policy documentation.
4. Current research, analytics, interviews, reviews, or sales/support language with date and scope.
5. Existing marketing copy, treated as a claim to verify rather than truth by default.
6. Agent inference, always labeled and never promoted into a claim silently.

Create a claims ledger in `MESSAGE-MAP.md`:

| Proposed statement | Type | Source | Confidence | Proof available | Decision |
|---|---|---|---|---|---|
| Teams can replay failed imports | Capability | `src/...` runtime and docs | High | Product demo | Emphasize |
| Saves hours every week | Outcome claim | None | Low | None | Exclude |

Classify capabilities, outcomes, comparisons, superlatives, numbers, customer statements, guarantees, pricing, availability, and urgency separately. Literal comparative claims such as “best” or “fastest” need a supported comparison basis. Words such as “trusted,” “secure,” or “effortless” can still imply factual or outcome claims in context, so classify the actual sentence rather than banning vocabulary mechanically. Truthful persuasive and navigational language does not become a factual claim merely because it is promotional.

If a desired benefit is plausible but unverified, frame the mechanism rather than inventing the result. “Review failed imports in one place” is safer than “cut debugging time by 80%” when no measurement exists.

## Message and benefit framing

The page should answer, in an order suited to the visitor:

- Who is this for?
- What situation brought them here?
- What can they accomplish?
- Why is this product's approach materially different?
- How does the product make the outcome possible?
- What proof reduces disbelief?
- What could make the visitor hesitate?
- What action is appropriate now?

A feature becomes a benefit only through a supported causal bridge:

```text
feature -> mechanism -> user consequence -> desired outcome
```

Example:

```text
Versioned replay history
-> preserves every failed run and input
-> lets an operator inspect and retry without reconstructing state
-> reduces recovery work and uncertainty
```

Do not skip from feature to an unmeasured business outcome. Preserve technical detail when the buyer needs it to trust the mechanism.

### Message-map headings

`MESSAGE-MAP.md` uses:

- `Audience and arrival intent`
- `Problem and desired outcome`
- `Unique approach and differentiation`
- `Product callouts`
- `Feature to benefit framing`
- `Claims and proof ledger`
- `Objections and risk reversal`
- `CTA ladder`
- `Voice and prohibited language`
- `Approval provenance`
- `Unknowns`

## Page strategy without templates

Choose structure from the persuasion problem. Do not start with a standard section list.

| Visitor and product condition | Useful organizing logic | Common risk |
|---|---|---|
| Visitor already knows the category | Product-first demonstration and differentiation | Re-explaining the category instead of proving the product |
| New or unfamiliar category | Problem narrative, mechanism, then proof | Abstract education that delays the product too long |
| Technical evaluator | Architecture or workflow deep dive with concrete artifacts | Marketing gloss that hides implementation reality |
| Visual or creative product | Representative work, interaction, and product canvas | Beautiful atmosphere without a clear job or CTA |
| High commitment or high price | Objection-led sequence, proof, process, and risk reversal | Premature CTA pressure |
| Comparison traffic | Criteria, transparent differences, fit and non-fit | Unsupported competitor claims |
| Search-led informational traffic | Direct answer, useful depth, product bridge | Thin SEO copy or bait-and-switch |
| Campaign or narrow offer | Tight message match and one commitment level | Navigation and secondary content diluting intent |

Possible forms include narrative, product-first, story-driven, comparison, technical deep dive, visual showcase, documentation style, interactive demo, and editorial long form. Combine them only when the visitor journey explains the combination.

Aim for one dominant message per viewport. Progressive persuasion means objections appear when the visitor is likely to feel them, not that every page must be long.

## Calls to action

Build a CTA ladder instead of repeating one generic label:

| Level | Visitor readiness | Example outcome label |
|---|---|---|
| Primary | Ready for intended commitment | `Create your first workspace` |
| Secondary | Needs product evidence | `Watch the import replay` |
| Tertiary | Needs deeper trust | `Read the security model` |

CTA quality checks:

- The label describes the result or next step accurately.
- Destination, account requirement, price, and commitment match expectations.
- Primary and secondary actions are visually and semantically distinct.
- Repeated CTAs retain meaning in their local context.
- Keyboard, focus, touch target, loading, disabled, error, and success behavior are clear.
- The page does not use urgency, scarcity, or risk reversal without proof.
- Forms request information proportional to commitment.

Avoid empty labels such as “Learn more,” “Submit,” “Get started,” or “Click here” when a more specific truthful label exists. A familiar generic label is acceptable when it is the clearest conventional action and nearby text supplies the missing outcome.

## Product highlights proof and objections

Prioritize highlights by visitor consequence and differentiation, not implementation novelty. A callout should usually include:

1. A specific user situation.
2. The product behavior or artifact.
3. The consequence the source supports.
4. A screenshot, demonstration, example, or proof when available.

Proof may include authentic product UI, workflow demonstrations, documented numbers, named and approved customer evidence, cited case studies, security/compliance evidence, transparent pricing, public changelogs, or concrete support/process commitments.

Logos without permission, composite testimonials, unattributed praise, fake activity, and invented metrics are not placeholders. Omit them and show the decision gap.

Objection work should address the actual cost or risk: setup, migration, learning, reliability, compatibility, privacy, lock-in, pricing, support, or fit. Risk reversal must be real and operationally supportable.

## Copy humanization

Use `prose-humanizer` in embedded mode when discoverable. Return final copy and compact evidence to this stage; never create `agent-work/{slug}/prose-humanizer/` for the embedded pass.

The landing-page copy pass must:

- preserve the approved claims ledger and exact product terminology;
- keep the chosen conversion intent and brand posture;
- replace vague boosterism with concrete mechanisms or remove it;
- vary sentence rhythm without manufacturing punchlines;
- use the customer's language when evidence exists;
- retain deliberate persuasion while removing formulaic hype;
- protect CTA destinations, interpolation, component props, structured data, and code;
- audit the final copy for new facts, changed numbers, stronger guarantees, and altered scope.

If `prose-humanizer` is unavailable, use this fallback loop:

1. Draft from the approved message map.
2. Identify inflated significance, generic hype, vague authorities, forced triples, synonym cycling, false ranges, filler, hedging, signposting, fake candor, slogan formulas, chatbot residue, and overly even rhythm.
3. Check for clusters rather than deleting an isolated stylistic choice.
4. Preserve unusual detail, voice, tension, technical vocabulary, and intentional formatting.
5. Compare every factual statement, number, name, date, quote, and citation with the approved sources.
6. Read aloud and revise once more for natural cadence and clear meaning.

## Visual and interaction craft

Landing-page design should make the product legible and desirable without turning every project into the same gradient-and-card composition.

### Hierarchy

- Establish one dominant message per viewport.
- Let supporting detail earn attention through scale, placement, contrast, rhythm, and progressive disclosure.
- Match density to buyer knowledge and product complexity.
- Keep the product visible early when seeing it resolves uncertainty.

### Typography and layout

- Use existing brand type and tokens when approved.
- Choose line length, leading, weight, and contrast for real copy, not placeholder text.
- Treat narrow layouts as intentional compositions, not stacked desktop fragments.
- Test long product names, translated copy, missing proof, multiple CTA labels, and content extremes.

### Imagery and product evidence

- Prefer authentic screenshots, interactions, diagrams, or approved brand assets.
- Crop and annotate product UI to support the adjacent claim.
- Avoid decorative imagery that competes with the product or implies unsupported capabilities.
- Optimize dimensions, formats, loading, alt text, and responsive sources.

### Trust and accessibility

- Use semantic landmarks and heading order.
- Keep focus visible and interaction states complete.
- Meet contrast and text-spacing needs without relying on color alone.
- Preserve content and action parity for keyboard, touch, zoom, reduced motion, and assistive technology.

## SEO Stack composition

The SEO Stack is optional context, not a prerequisite for every landing page. Activate it when the page is explicitly search-targeted, the user supplies an SEO brief, or same-slug SEO artifacts are discoverable.

### Ownership contract

| Decision | Canonical owner when available | Landing Page responsibility |
|---|---|---|
| Verified technical/provider foundation | `seo-setup` | Preserve consent, canonical origin, sitemap, and index architecture; use read-only evidence only when needed |
| Competitors, keyword demand, clusters, and page ownership | `seo-foundation` | Consume approved evidence; do not rerun research or redefine the cluster |
| Portfolio action, target URL, search intent, protected winners, internal-link role, measurement | `seo-strategy` | Validate and preserve the approved page opportunity without inheriting page prescriptions |
| Page-specific benchmark, title, catalogue durability, persuasion, message, proof, CTA, layout, visual direction, HTML preview, bounded implementation | `landing-page` | Own, challenge, and approve these decisions |
| Editorial article/guide without material landing-page decisions | `seo-content` | Route rather than duplicating editorial execution |
| Post-publication URL verification and individual indexing request | `seo-indexing` | Emit the final canonical URL and production receipt; do not submit inside Landing Page |
| Outcome and guardrail review | `seo-monitor` | Emit a verified page/measurement handoff; do not claim post-launch results during implementation |

An approved SEO opportunity is portfolio evidence, not a landing-page brief. Landing Page applies [the page-quality contract](contracts/seo-page-quality.md), then owns the title, headline wording, persuasion order, CTA hierarchy, proof presentation, structure, and layout while preserving the opportunity's user job, primary owner, overlap exclusions, protected assets, internal-link role, and measurement boundary. Any material delta in those preserved decisions returns to Strategy.

For search-targeted work, `PAGE-BENCHMARK.md`, `PAGE-REQUIREMENTS.md`, and `EDITORIAL-REVIEW.md` are mandatory before message approval. Competitor recurrence cannot become a required module or causal ranking claim. Technical correctness cannot change `REVISE`, `NO PAGE`, or `BLOCKED` into `PUBLISH`.

### Consultation record

When the Stack applies, add to `RESEARCH.md` and `SEO-PLAN.md`:

```text
seo_slug
setup_status_path and freshness
foundation_path and approval
strategy_path, item_id, revision, and approval
page_benchmark_path, scope, and freshness
page_requirements_path
editorial_review_path, verdict, revision, and approval
primary_cluster and search_intent
current_owner and proposed_owner
protected_winners and overlap_exclusions
required_internal_links
index, canonical, and sitemap posture
baseline, outcome, guardrails, and monitor windows
indexing eligibility and publication receipt path
preserved_decisions
landing_page_owned_decisions
material_deltas_or_gaps
seo_stack_cli_version and receipt paths when used
```

### CLI boundary

The optional `seo-stack` CLI is owned by `seo-setup`. Resolve it through the registry or sibling skill, read `CLI.md`, and confirm compatible schemas. Useful Landing Page commands are bounded live inventory, provider status receipts already authorized by Setup, and final integrated status validation. Provider keyword research, setup mutation, campaign work, and monitoring analysis are outside this skill.

If the CLI is absent or incompatible, use browser/project inspection and current official provider interfaces where required. Record the fallback; do not silently skip a material verification.

## SEO editorial change control

For a search-targeted page, apply [the SEO change-control contract](contracts/seo-change-control.md) before source mutation. For a new page, record `NO EXISTING PAGE` as the baseline rather than inventing prior copy. Keep product truth as a constraint while preserving specificity, query coverage, click appeal, persuasive usefulness, and a credible next step.

Classify changed language as `FACTUAL`, `DERIVED`, `COMPARATIVE`, `PERSUASIVE`, or `NAVIGATIONAL`. For every affected page family, record representative exact before/after text, the transformation rule, relevant queries, terms gained and lost, and the search-intent, CTR, persuasion, and conversion mechanism. A phrase does not need a literal database field to be useful and truthful; a factual or comparative assertion still needs support.

Before removing or hiding content, inventory unused facts, traits, aliases, measurements, relationships, taxonomy, media, and product actions. Compare `RETAIN`, `RESTORE`, `REWRITE`, and `REJECT`. “Cleaner,” “less promotional,” repeated across routes, or technically unverifiable are not sufficient removal reasons.

Keep these judgments separate:

- a visible FAQ can help users even when FAQ schema is ineligible or unlikely to receive a rich result;
- repeated framing can provide useful orientation while each complete entity page remains distinct;
- a technically valid schema, build, or snapshot proves conformance only, not that the proposed wording improves search or conversion performance.

Shared-template or multi-route changes require a named canary and independent editorial and technical rollback boundaries. A generic “continue” or approval of a visual preview does not approve an unlisted editorial transformation. `SEO-CHANGE-APPROVAL.json` must reference the SHA-256 of the exact ledger bytes and the approved change IDs.

## SEO GEO and AEO

Start with an explicit disposition:

- `INDEX` — the page is intended as a canonical search destination.
- `NOINDEX` — campaign, experiment, duplicate, gated, private, or otherwise unsuitable for indexing.
- `UNRESOLVED` — a material product or technical decision remains; do not guess.

For indexable pages, align visitor intent, query intent, page promise, and product reality. Optimize humans first while making meaning easy for search and answer systems to extract.

### Technical checklist

- Unique descriptive title and meta description.
- Correct canonical URL and robots posture.
- Server-rendered or otherwise crawlable primary content.
- One coherent H1 and logical heading hierarchy.
- Semantic links and useful internal destinations.
- Fast loading, stable layout, responsive media, and minimal blocking work.
- Valid Open Graph/social metadata where applicable.
- Structured data only when the visible content and schema type support it.
- No duplicate, hidden, keyword-stuffed, or doorway content.

### Content and entity checklist

- Answer the primary question directly before unnecessary scene-setting.
- Use natural terminology and comprehensive coverage proportional to intent.
- Identify product, organization, audience, features, and related entities consistently.
- Use concise summaries before detail where they help scanning and answer extraction.
- Include FAQs only when real objections or search evidence justify them.
- Cite evidence and expose limitations rather than claiming universal fit.

Record Search Console, analytics, conversion events, qualitative behavior, experiment, and refresh plans without treating publication as the end of optimization.

## TurbulenceJS motion

Motion should improve comprehension, continuity, feedback, or character. It must not conceal latency, delay input, or compensate for weak hierarchy.

### Selection

Inspect existing motion ownership and the installed package. Verify exports rather than inventing APIs. A typical landing page starts with root plus `/subtle`; add `/interact`, `/cartoon`, or `/cinematic` only when the approved direction supports them.

| Role | Typical purpose | Default posture |
|---|---|---|
| `page.arrive` | Establish hierarchy without delaying reading | Restrained, once |
| `product.reveal` | Connect explanation to product evidence | Restrained or expressive |
| `story.progress` | Preserve spatial continuity through a narrative | Expressive, interruption-safe |
| `cta.respond` | Confirm hover, focus, press, and completion | High-frequency restrained |
| `proof.enter` | Draw attention to verified evidence | Subtle, never theatrical by default |
| `celebration` | Mark a meaningful completed action | Rare and explicitly justified |

### Required motion record

For every role record target, exact verified entrypoint, trigger, frequency, properties, component owner, interruption/retargeting, teardown, reduced endpoint, performance risk, and acceptance evidence. Remove or retain competing CSS/WAAPI/library ownership deliberately.

Intensity 1-2 is the normal landing-page range. Intensity 3-4 or raster effects require explicit approval, rare triggers, resource caps, CSP/origin analysis, fallback endpoints, and cleanup evidence.

Preview motion is illustrative. Production verification proves normal endpoint, reduced motion, rapid repeat/reverse, unmount, idle cleanup, focus, responsive geometry, and no new console or resource errors.

## Implementation and quality

Detect the target toolchain from manifests and repository instructions. Preserve existing design-system and routing conventions. Prefer reusable sections only when reuse is real; a component abstraction is not automatically better than clear page-local composition.

### Presumptively applicable quality dimensions

| Dimension | Minimum evidence |
|---|---|
| Product truth | Approved claims ledger matches rendered copy and product behavior |
| Conversion clarity | Primary/secondary CTA hierarchy, destinations, states, and message match |
| Copy fidelity | Humanization audit shows no factual or terminology drift |
| Visual craft | Approved preview comparison plus representative rendered inspection |
| Accessibility | Semantics, headings, focus, keyboard, touch, contrast, zoom, reduced motion |
| Responsive | Narrow, medium, wide, text expansion, content extremes |
| SEO | Index posture, metadata, canonical, crawlability, structured data, links |
| Performance | Production build plus representative loading/layout/resource evidence |
| Motion | TurbulenceJS endpoints, interruption, reduced behavior, teardown, idle |
| Correctness | CTA/forms/navigation success, validation, error, recovery, destinations |
| Privacy | Analytics/consent and absence of unauthorized tracking |
| Maintainability | Project conventions, scoped diff, component ownership, documentation |
| Rollback | Revert or feature boundary appropriate to deployment risk |

Use browser automation when the project supports it, but inspect representative screenshots or the live local page as well. A passing build cannot prove hierarchy, tone, or motion feel.

## Artifact schemas

### RESEARCH.md

Headings: `Product and visitors`, `Arrival intent and journey`, `Evidence sources`, `Product truth`, `Brand and implementation inventory`, `Existing page`, `Constraints`, `Alternatives`, `Unknowns`.

### COPY-DECK.md

Headings: `Voice`, `Headline hierarchy`, `Product highlights`, `Proof and objections`, `CTA and microcopy`, `Humanization record`, `Final approved copy`.

The humanization record notes voice evidence, pattern clusters changed, deliberate patterns retained, factual/claim comparison, and approval impact. Do not paste every intermediate rewrite.

### SEO-PLAN.md

Headings: `Disposition`, `Upstream SEO Stack contract`, `Traffic and query intent`, `Ownership and protected winners`, `Information architecture`, `Metadata`, `Canonical crawl and links`, `Entities and structured data`, `Performance`, `Measurement`, `Unknowns`.

### SEO-CHANGE-LEDGER.json and SEO-CHANGE-APPROVAL.json

Use the exact schema and approval semantics in [the SEO change-control contract](contracts/seo-change-control.md). Validate them with `scripts/validate_seo_change_control.py` before implementation. Preserve the approval receipt next to the ledger; never rewrite it to match a later mutation.

### PAGE-DIRECTIONS.md

Headings: `Adaptive mode`, `Shared approved message`, `Directions`, `Recommendation`, `Trade-offs and experiments`, `Revision history`, `Approval`.

Revision table:

| Revision | Options or variants | Feedback | Disposition | Snapshot | Approval |
|---|---|---|---|---|---|

### IMPLEMENTATION-PLAN.md

Headings: `Approved outcome`, `Source targets`, `Content and assets`, `Components and responsive behavior`, `SEO`, `TurbulenceJS target map`, `Implementation slices`, `Project gates`, `Browser scenarios`, `Rollout and rollback`, `Boundaries`.

### PROGRESS.md

```md
## 2026-01-01T12:00:00Z — DONE — Implement approved hero and CTA

- Scope: `src/...`
- Evidence: focused tests; responsive browser scenarios; claim/CTA comparison
- Quality: product truth, accessibility, responsive, performance
- I am satisfied this step is complete because the rendered hero matches approved revision R2, both CTA destinations work, and focused plus project gates pass.
```

### QUALITY-REPORT.md

Use headings `Quality report`, `Approved preview and message`, `Changed files`, `Project gates`, `Rendered and runtime evidence`, `SEO`, `Copy and claims`, `Motion`, `Deviations and waivers`, `Final integrated verification`, `Final status`.

## Worked examples

### Callout correction

Weak and unsupported:

> The fastest way to automate every support workflow.

Evidence-backed:

> Route repeat support questions into reviewed reply workflows, while agents keep control of what gets sent.

The second version explains a mechanism and control boundary without claiming universal coverage or speed.

### CTA ladder

For a product with a self-serve sandbox and a technical buyer:

- Primary: `Run a sample import`
- Secondary: `Watch failure recovery`
- Tertiary: `Read the data model`

Each label tells the visitor what happens next and supports a different readiness level.

### Adaptive direction decision

If the repository contains an approved `VISUAL-LANGUAGE.md` and complete tokens, create one fidelity preview. Compare two hero compositions only if product demonstration versus outcome copy remains unresolved. Do not invent three unrelated visual identities.

If the product is greenfield with no approved direction, create distinct product-first, technical-editorial, and interactive-demo concepts. Keep the approved message and CTA goal stable so the user judges design logic rather than different claims.

## Research provenance

This reference incorporates maintainer research on landing-page foundations, responsible marketing, and SEO. The operational guidance is bundled here so an independently installed skill has no repository-local research dependency. Recheck primary sources and current platform guidance whenever these foundations change materially.
