<!-- contract-metadata
id: seo-change-control
version: 1
semantic-owner: seo-content
-->

# SEO Change-Control Contract

Apply this contract to every user-facing SEO change and to every technical SEO handoff that could touch a shared page template. It binds editorial judgment, exact approval, implementation scope, rollout, and rollback so mechanical verification cannot legitimize an unapproved or weaker search experience.

## Contents

- [Optimization order](#optimization-order)
- [Language and change classes](#language-and-change-classes)
- [Improve before remove](#improve-before-remove)
- [FAQ, schema, and repeated copy](#faq-schema-and-repeated-copy)
- [Editorial change ledger](#editorial-change-ledger)
- [Exact approval](#exact-approval)
- [Technical-only handoff](#technical-only-handoff)
- [Implementation and rollout](#implementation-and-rollout)
- [Validation integrity](#validation-integrity)
- [Required evidence](#required-evidence)

## Optimization order

Truth, safety, privacy, and product reality are non-negotiable constraints. Within them, optimize for:

1. the actual search intent and user job;
2. specificity, query coverage, click appeal, and persuasive usefulness;
3. support from available product facts, entity data, taxonomy, relationships, and authoritative sources;
4. a credible conversion or next-step bridge.

Do not optimize the proxy of eliminating every phrase that lacks a literal database field. A truthful change still fails when it becomes vaguer, less useful, less relevant, or less persuasive without a compensating user benefit.

## Language and change classes

Classify each affected phrase by its strongest applicable class:

- `FACTUAL` — a product, entity, quantitative, temporal, or externally verifiable assertion.
- `DERIVED` — a statement produced from documented taxonomy, relationships, rules, or calculation; record the derivation.
- `COMPARATIVE` — a ranking, superlative, preference, superiority, or comparison claim; record the comparison basis.
- `PERSUASIVE` — truthful framing, benefit language, specificity, invitation, or motivation that does not assert an independently testable fact merely by being marketing copy.
- `NAVIGATIONAL` — orientation, task, category, venue, entity, or next-step language that helps users and engines understand the destination.

Do not apply factual-claim evidence rules indiscriminately to persuasive or navigational wording. Do not disguise a factual or comparative claim as persuasion.

Classify user-facing changes as `TITLE`, `DESCRIPTION`, `VISIBLE_COPY`, `FAQ_VISIBLE`, `FAQ_SCHEMA`, `MODULE_VISIBILITY`, `STRUCTURED_DATA`, `CTA`, `INTERNAL_LINK_COPY`, or `INTERNAL_LINK_DESTINATION`. Pure routing, canonical, index, sitemap, pagination, and relationship-data work belongs in the technical scope rather than the editorial ledger.

## Improve before remove

Before deleting, hiding, neutralizing, or replacing visible content:

1. Inventory the facts, traits, aliases, descriptions, measurements, relationships, taxonomy, media, and product actions already available.
2. Attempt the smallest truthful improvement that preserves the user job, useful terminology, specificity, and conversion bridge.
3. Compare retain, restore, rewrite, and reject options.
4. Remove only when no useful truthful treatment remains or the content is harmful, inaccessible, deceptive, obsolete, or genuinely valueless.

“Cleaner,” “more factual,” “less promotional,” “repeated,” or “passes the verifier” are not sufficient removal reasons.

## FAQ, schema, and repeated copy

Evaluate visible FAQ utility independently from structured-data eligibility. A useful visible FAQ may remain without FAQ schema. Schema ineligibility, rich-result uncertainty, or a generator limitation is never itself a reason to remove visible questions or answers.

Repeated framing, descriptions, or CTAs are not automatically harmful duplicate content. Inspect whether the complete page has distinct entity or user value, whether shared language aids orientation, and whether existing data can strengthen entity-specific answers. Suppress repeated copy only with page-level evidence and an improvement attempt.

## Editorial change ledger

Write `SEO-CHANGE-LEDGER.json` before source mutation for any title, description, visible copy, FAQ, module-visibility, structured-data, CTA, or link-copy change. It is mandatory for every shared-template or multi-route user-facing change and for any proposed deletion or suppression.

The ledger uses `schema_version: 1` and contains:

- `slug`, immutable `revision`, creation time, and `approval_receipt` path;
- page families with exact route counts, shared-template status, baseline, and canary definition;
- one stable change ID per proposed transformation;
- exact representative route, before value, proposed-after value, and templated transformation rule;
- language and change classes;
- relevant queries plus terms gained and lost;
- explicit dispositions for every lost term;
- search-intent, CTR, persuasion, and conversion mechanism;
- factual, derived, taxonomy, and available-unused evidence;
- visible-content value and structured-data eligibility;
- protected-winner and baseline state;
- improve-before-remove, FAQ, and repeated-copy decisions where applicable;
- `RETAIN`, `RESTORE`, `REWRITE`, or `REJECT` disposition;
- specialist owner, canary boundary, rollout boundary, and rollback boundary;
- `approval_requirement: EXACT`.

The ledger is a proposal, not proof of improvement. Do not place secrets, private analytics rows, or unnecessary personal data in it.

## Exact approval

Write `SEO-CHANGE-APPROVAL.json` only after the user approves the presented ledger. It records:

- `schema_version: 1`;
- SHA-256 of the exact ledger bytes;
- approved change IDs;
- approval statement, approver, and timestamp;
- `explicit_exclusions` or an empty list.

Generic instructions such as “continue,” “finish Phase 4,” or “proceed with the technical work” authorize only the next unchanged, already-listed slice. They never approve an unlisted title, description, FAQ, module, visibility, structured-data, CTA, or copy change.

Any byte change to the ledger, new change ID, changed after-value, increased route count, altered transformation rule, broader rollout, or weaker rollback invalidates the receipt. Re-present the material delta and obtain renewed exact approval.

## Technical-only handoff

Every Strategy-to-Goalpro SEO handoff includes `SEO-TECHNICAL-SCOPE.json` with:

- approved Strategy revision and portfolio item IDs;
- explicit allowed technical classes and targets;
- `user_facing_changes: FORBIDDEN`;
- an empty `editorial_change_ids` list;
- prohibited user-facing change classes;
- an `approval` object with `status: APPROVED`, statement, approver, timestamp, and approved artifact;
- gates, `rollout_boundary`, and `rollback_boundary`.

Allowed technical classes are `CANONICAL`, `REDIRECT`, `SITEMAP`, `ROBOTS`, `INDEX_DIRECTIVE`, `ROUTING`, `PAGINATION`, `RELATIONSHIP_DATA`, `GEOGRAPHY_DATA`, and `INTERNAL_LINK_DESTINATION` only when existing approved visible labels remain unchanged.

If a handoff mixes technical work with titles, metadata copy, FAQs, visible sections, schema-dependent content, CTA language, internal-link wording, or other editorial changes, split it. The technical handoff may proceed independently; the user-facing slice routes to `seo-content` or `landing-page` with its own ledger and approval.

## Implementation and rollout

Before each mutation slice, validate the ledger and approval or the technical scope with the bundled validator. Implement only approved change IDs or allowed technical classes.

For a shared template or more than one route:

1. Render the named representative routes before and after.
2. Apply the approved canary boundary before broad rollout.
3. Compare query terms, specificity, promise, persuasion, visible utility, and conversion path—not only correctness.
4. Stop on a material delta, unexpected term loss, vaguer wording, or failure signal.
5. Keep technical and editorial rollback boundaries independent.

Record actual rendered output in the final receipt. If actual output differs materially from the approved proposed-after value or transformation, return to exact approval before rollout or completion.

## Validation integrity

Tests and validators prove only the rule they exercise. A test authored from the same new editorial opinion is `CONFORMANCE` evidence, not independent evidence that the opinion improves SEO, CTR, persuasion, or conversion.

An editorial decision requires at least one independent basis: approved product/editorial policy, page-specific benchmark, protected-winner baseline, user-approved before/after, authoritative source, or post-release measurement. Type checks, builds, schema validation, snapshot tests, and an agent's self-judgment cannot supply that basis.

Never write a verifier that rejects existing visible content unless the approved ledger or an independent policy already requires that disposition. A green technical suite cannot change an unapproved, `REVISE`, `NO PAGE`, or `BLOCKED` editorial state into approval.

## Required evidence

The owning workflow preserves:

- `SEO-CHANGE-LEDGER.json` and conditional `SEO-CHANGE-APPROVAL.json` for user-facing changes;
- `SEO-TECHNICAL-SCOPE.json` for Strategy-to-Goalpro technical work;
- representative rendered before/after evidence for each affected page family;
- exact implemented change IDs or technical classes;
- term/query gains and losses, material deltas, and editorial verdict;
- canary, rollout, rollback, baseline, and monitoring pointers;
- technical gate results labelled with their actual evidence limits.

Absence of a user-facing change does not require an empty editorial ledger. Use the technical scope and prove the final diff contains no prohibited user-facing delta.
