# Brandstorm Research Reference

Use this reference for competitor discovery, candidate construction, browser research, preliminary collision analysis, Porkbun checks, and final evidence classification. Read it completely before web research begins.

## Contents

- [Research posture](#research-posture)
- [Browser-only operating rule](#browser-only-operating-rule)
- [Competitor discovery](#competitor-discovery)
- [Naming territories and candidates](#naming-territories-and-candidates)
- [Clearance scope](#clearance-scope)
- [Surface-specific search protocol](#surface-specific-search-protocol)
- [Porkbun domain protocol](#porkbun-domain-protocol)
- [Evidence schema](#evidence-schema)
- [Status and candidate disposition](#status-and-candidate-disposition)
- [Coverage and freshness](#coverage-and-freshness)
- [Loop diagnosis](#loop-diagnosis)
- [Communication rules](#communication-rules)

## Research posture

Brandstorm produces structured preliminary research for a product-name decision. It does not provide a legal opinion, comprehensive clearance search, registration prediction, or guarantee that a platform, registry, or market will accept the name.

Use four evidence labels in narrative conclusions:

- `OBSERVED` — directly visible in the cited browser source at the recorded time;
- `INFERRED` — a bounded interpretation supported by observations;
- `HYPOTHESIS` — plausible but needs validation or user/legal judgment;
- `UNSUPPORTED` — proposed or repeated claim without adequate evidence.

Prefer current official sources for registrations, platform records, and availability. General search results can reveal collision risk but do not override an official record. Absence from a search result is weak negative evidence.

## Browser-only operating rule

Every network interaction must occur through the host's built-in browser or an agent-accessible Chrome extension.

Allowed:

- navigating and searching through visible website interfaces;
- inspecting official public pages and authorized signed-in sessions;
- using browser-native page search, screenshots, and visible result extraction;
- opening result links and recording URLs, query scope, and timestamps.

Forbidden:

- `curl`, `wget`, HTTP libraries, search APIs, store APIs, registrar APIs, or scraping packages;
- standalone Playwright, Selenium, browser MCP servers, or unrelated browser-control surfaces;
- automated CAPTCHA solving, rate-limit evasion, proxy rotation, hidden endpoint calls, or terms bypass;
- inspecting cookies, passwords, local storage, or browser profile data;
- submitting purchases, filings, reservations, account changes, or contact forms.

If the user names a browser, use that browser only. Otherwise prefer the built-in browser for public pages and accessible Chrome when a signed-in or existing browser session is necessary. Follow the active Browser/Chrome control skill rather than duplicating its setup mechanics in work artifacts.

## Competitor discovery

### Broad pass

Use multiple product-language angles:

- product category and common synonyms;
- user problem and desired outcome;
- workflow or task language;
- target audience plus product type;
- direct product substitutes and manual alternatives;
- platform-specific searches for apps, games, services, or developer tools;
- existing names and terminology found in product evidence.

Classify each discovered entity:

| Class | Meaning | Naming relevance |
|---|---|---|
| Direct competitor | Similar user, problem, and product mechanism | High confusion and positioning relevance |
| Adjacent competitor | Overlapping audience or job with different scope | Semantic and expansion relevance |
| Substitute | Different mechanism for the same outcome | User-language and positioning relevance |
| Marketplace or directory | Aggregates products rather than competing directly | Search-result crowding, not business equivalence |
| Publisher or community | Owns attention or vocabulary in the category | Search and cultural relevance |
| Lexical collision | Same or similar name outside the category | Searchability and expansion risk |
| Unrelated | No material audience, category, or naming overlap | Preserve as excluded evidence |

Do not infer market importance from a single result position. Search results vary by time, location, language, device, and personalization.

### Scoped pass

After the user confirms the competitor set, inspect representative official surfaces: homepage or product page, store listing, documentation or feature overview, about/company page, and relevant search-result context. Record only what affects naming:

- exact product and company names;
- pronunciation, spelling, word formation, and suffix patterns;
- category descriptors and recurring semantic territories;
- app or package identifiers when publicly visible;
- brand architecture and product-family patterns;
- obvious confusion, saturation, or differentiation signals.

The scoped pass is not a general competitive product audit. Do not prescribe copying a competitor's identity.

## Naming territories and candidates

A naming territory is a coherent semantic or linguistic strategy, not a list of synonyms. Useful territory families include:

- user outcome or transformation;
- product mechanism or metaphor;
- audience identity or community language;
- emotional posture or desired feeling;
- invented or blended terms;
- concrete objects, places, motion, sound, or natural phenomena;
- category-adjacent language used in an unexpected but defensible way.

Use only territories that fit the approved brief. Generate internal working material freely, but present exactly 20 candidates per round.

Screen candidates qualitatively before presentation for:

- fit with the product promise and audience;
- meaningful distinction between territories;
- pronunciation after reading and spelling after hearing;
- length, rhythm, visual shape, and likely abbreviation;
- negative meanings, slang, translation, or cultural risk in scoped languages;
- accidental category mismatch or misleading descriptiveness;
- future product-family and geographic expansion;
- obvious collisions already observed in the competitor pass.

This screen must not become undisclosed targeted clearance. Domain and legal availability remain unchecked until the approved finalist stage.

## Clearance scope

Before targeted research, freeze:

- the exact 20 candidate spellings;
- launch countries and trademark jurisdictions;
- languages and relevant transliterations;
- likely goods/services and provisional Nice classes;
- product platforms and mandatory stores;
- domain requirements, TLDs, modifiers, hyphen policy, and premium-price tolerance;
- automatic rejection rules and concerns that require judgment.

If the user cannot select a legal jurisdiction, record that as a blocking user decision rather than defaulting silently to the researcher's country. If useful, explain common scopes such as national registries and WIPO's international database, but do not choose legal coverage for the user.

Patents do not protect product names in the way trademarks do. Patent research can expose entities, technologies, terminology, and crowded product territory. Keep it separate from trademark conclusions.

## Surface-specific search protocol

Run each mandatory surface for every finalist. Use exact spelling first, then the smallest useful set of close variants. Do not generate so many speculative variants that the evidence becomes unauditable.

### Trademark databases

Use current official databases for the approved jurisdictions and WIPO when international registrations are relevant. Record database, jurisdiction, search mode, goods/services scope, classes, exact query, close variants, live/dead status when shown, owner, registration/application identifier, and relevant similarity.

Check:

- exact normalized phrase;
- spacing, hyphenation, plural, and common spelling variants;
- close phonetic or dominant-root variants when confusion is plausible;
- relevant classes and related goods/services, not only an unrestricted text hit count.

Do not decide legal likelihood of confusion. Mark material similarities for professional review.

### Patent databases

Use official patent-office search interfaces appropriate to the approved markets. Search exact and close candidate terminology in titles, abstracts, assignees, and inventors when supported, then narrow with category terms.

Record whether the result is a terminology collision, company/entity collision, relevant technology cluster, or unrelated use. Never convert “no patent result” into name clearance.

### Steam

Use Steam's official store search and relevant product pages. Search exact and close title variants plus the candidate with the game/software category when needed. Record title, developer/publisher, release state, category, URL, and confusion rationale.

### iOS App Store and Mac App Store

Use Apple's official App Store search or official web listings. Keep iPhone/iPad and macOS platform evidence distinct when the interface exposes the distinction. Record app title, subtitle where visible, developer, platform, category, territory storefront, URL, and confusion rationale.

### Google Play

Use Google Play's official search and listing pages. Record app title, developer, category, availability/territory caveat, URL, and confusion rationale.

### Google Search

Use Google's visible search interface. At minimum search:

- `"{candidate}"`;
- `{candidate}`;
- `"{candidate}" {product-category}`;
- material spacing or spelling variants;
- `{candidate} app`, `{candidate} software`, or another product-type qualifier when relevant.

Record material entities and result types rather than copying whole result pages. Search-result absence does not prove uniqueness.

## Porkbun domain protocol

Porkbun is a mandatory surface. Use Porkbun's visible domain-search interface through the permitted browser.

For every finalist:

1. Check the exact candidate under every approved TLD.
2. Check only user-approved modifiers or alternative constructions.
3. Preserve punctuation normalization decisions, such as removing spaces or hyphens.
4. Record each complete domain string independently.
5. Record the visible status exactly enough to distinguish available, registered/unavailable, premium, aftermarket, unsupported, and unclear.
6. Record displayed first-year and renewal price when visible and material to the user's premium tolerance; do not infer a price hidden by the interface.
7. Record result URL or page reference, local timestamp with timezone, and any storefront/session limitation.

Never add a domain to a cart, reserve it, begin checkout, sign up, or purchase it. Do not treat a search result as a hold. State that the result can change immediately.

An exact-name domain rule is satisfied only by the approved exact construction. A prefixed, suffixed, hyphenated, alternate-TLD, premium, or aftermarket option does not satisfy it unless the user approved that policy.

## Evidence schema

Each row in `CLEARANCE-MATRIX.md` should contain:

| Field | Meaning |
|---|---|
| Candidate | Frozen exact spelling |
| Surface | Trademark jurisdiction, patent source, store, Google, or Porkbun |
| Query or asset | Exact search string, variant, class scope, or complete domain |
| Status | `CLEAR SIGNAL`, `CONCERN`, `BLOCKED`, `UNAVAILABLE`, or `UNVERIFIED` |
| Material observation | Concise result affecting the decision |
| Source | Official or visible result URL/page reference |
| Checked at | Timestamp with timezone |
| Scope and limitation | Jurisdiction, class, storefront, language, session, or uncertainty |

Put detailed hits in `EVIDENCE-LEDGER.md` using stable evidence identifiers. Matrix rows link those identifiers rather than embedding long narratives.

For screenshots, use a project-safe path inside the Brandstorm stage when the browser and host permit capture. Never store sensitive browser chrome, account data, or irrelevant personal information.

## Status and candidate disposition

### Individual checks

- `CLEAR SIGNAL` means the scoped search revealed no obvious material conflict. It is not legal clearance.
- `CONCERN` means evidence is ambiguous, similar, crowded, or warrants user/legal judgment.
- `BLOCKED` means observed evidence violates a user-approved disqualifier or presents a material collision.
- `UNAVAILABLE` is reserved for scarce assets such as domains observed unavailable under the approved policy.
- `UNVERIFIED` means the search was incomplete, inaccessible, stale, or not interpretable enough to classify.

### Candidate disposition

- `VIABLE` — every mandatory surface is verified, no disqualifier is hit, the approved domain policy is satisfied, and concerns remain within the user's stated tolerance.
- `CONDITIONAL` — every mandatory surface is verified, but one or more concerns require explicit user or professional review.
- `NOT VIABLE` — at least one material conflict, unavailable required asset, or disqualifier prevents advancement.
- `UNVERIFIED` — at least one mandatory surface is unverified.

Do not compute viability by majority vote. One mandatory conflict can outweigh many clear signals. Keep any scoring model secondary and explain its weights; scores never replace source evidence or the user gate.

## Coverage and freshness

Track coverage as candidate-by-mandatory-surface cells. Report both counts and missing cells, for example `160/160 mandatory cells verified`, without implying that one matrix row always equals one query.

Recheck a cell when:

- the candidate spelling changes;
- jurisdiction, class, platform, language, or domain policy expands;
- the recorded result is stale relative to the decision risk;
- contradictory evidence appears;
- the user asks to refresh time-sensitive availability.

Domain availability is the most volatile evidence and should be rechecked immediately before any later purchase decision. Brandstorm itself does not purchase.

## Loop diagnosis

When a round yields no viable candidates, preserve the evidence and classify the cause:

| Cause | Return point |
|---|---|
| Same root collides repeatedly | Replace or radically alter that naming territory |
| Category is lexically saturated | Explore a more distinctive semantic or invented territory |
| Store/search confusion | Improve spelling, sound, or category distance |
| Exact-domain rule eliminates all names | Ask whether the domain policy changes; never relax it silently |
| Cultural or language failures | Replace the affected territory with scoped-language input |
| Trademark concerns dominate | Revisit goods/services assumptions with the user and professional counsel |
| Product brief caused misleading names | Return to product truth and brand criteria |
| Browser access is incomplete | Do not regenerate; unblock and finish the missing checks |

Every new clearance round requires a newly approved exact 20-name finalist set and a complete matrix. Reuse only still-valid product, competitor, and brand-direction evidence.

## Communication rules

Use careful phrases:

- “No obvious conflict found in the recorded preliminary search.”
- “Observed available on Porkbun at {timestamp}; not reserved and subject to change.”
- “This result needs trademark counsel or jurisdiction-specific review.”
- “The candidate is viable under the approved research rules, not legally cleared.”

Avoid:

- “The trademark is available.”
- “This name is safe.”
- “The domain is secured.”
- “No one else uses this name.”
- “The patent search clears the brand.”

In the final presentation, distinguish observed facts, model recommendations, unresolved professional-review questions, and the user's decision. The user's choice is authoritative; Brandstorm's ranking is advisory.
