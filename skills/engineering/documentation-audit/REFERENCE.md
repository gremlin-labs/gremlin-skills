# Documentation Audit Reference

## Classification axes

### Kind

`ENTRYPOINT`, `GUIDE`, `REFERENCE`, `ARCHITECTURE`, `ADR`, `RUNBOOK`, `POLICY`, `API`, `GENERATED_REFERENCE`, `STYLE_GUIDE`, `PLAN`, `TASK`, `TICKET`, `SPEC`, `RESEARCH`, `REPORT`, `WORK_ARTIFACT`, `ARCHIVE`, `OTHER`.

### Freshness

- `CURRENT`: material claims match authoritative evidence.
- `DRIFTED`: useful and substantially correct, but one or more material claims differ.
- `OUTDATED`: the primary behavior, structure, or policy described no longer applies.
- `UNVERIFIED`: evidence is unavailable, ambiguous, or too costly to establish safely.
- `N/A`: freshness does not meaningfully apply, normally for immutable historical records.

### Implementation state

Use for plans, tickets, specs, tasks, and coding instructions; otherwise `N/A`.

`NOT_IMPLEMENTED`, `PARTIALLY_IMPLEMENTED`, `IMPLEMENTED`, `BLOCKED`, `DEFERRED`, `REJECTED`, `ABANDONED`, `SUPERSEDED`, `RETIRED`, `UNVERIFIED`, `N/A`.

`IMPLEMENTED` requires every material acceptance outcome or an explicit recorded scope reduction, plus implementation evidence. Partial delivery is `PARTIALLY_IMPLEMENTED` even if the document says complete.

### Authority

`CANONICAL`, `SUPPORTING`, `HISTORICAL`, `DUPLICATE`, `CONFLICTING`, `UNKNOWN`.

### Structural condition

Apply zero or more: `WELL_PLACED`, `MISPLACED`, `ORPHANED`, `BROKEN_LINKS`, `UNINDEXED`, `MISSING_OWNER`, `MIXED_AUDIENCE`, `PUBLIC_PRIVATE_LEAK`, `CHILD_DEPENDS_ON_PARENT`, `LEGACY_GENERATED_ROOT`, `GENERATED_WITHOUT_PROVENANCE`, `DUPLICATED_CONTENT`.

### Action

`KEEP`, `UPDATE`, `REWRITE`, `MERGE`, `SPLIT`, `MOVE`, `PROMOTE_TO_CANONICAL`, `DEMOTE_TO_SUPPORTING`, `ARCHIVE`, `DELETE_AFTER_REPLACEMENT`, `REGENERATE`, `ADD_REDIRECT`, `ADD_INDEX`, `ADD_OWNER`, `INVESTIGATE`.

## Evidence hierarchy

Prefer, in order: running behavior and schemas; executable tests and CI; current configuration/manifests; published external contracts; maintained canonical docs; recent reviewed changes; issue/PR history; commit messages; prose claims without corroboration.

Record evidence as stable repository-relative paths and symbols or commands. Do not include secrets, customer data, or inaccessible private URLs in artifacts intended for publication.

## Catalog columns

Use a Markdown table or equivalent structured data with: path, repository, kind, audience, freshness, implementation, authority, structural conditions, action, proposed destination, confidence, evidence, notes.

Confidence is `HIGH`, `MEDIUM`, or `LOW`; it never replaces `UNVERIFIED`.

## Archive rules

- Archive only when historical value exists and readers can distinguish historical from current truth.
- Preserve ADRs as immutable records; supersede them with explicit links rather than rewriting decisions retroactively.
- Delete only generated, duplicated, trivial, or harmful material after replacement and backlink verification.
- Completed plans remain work evidence under `agent-work/`; promote durable outcomes into canonical docs instead of moving plans into architecture folders.

## Deterministic enforcement candidates

- markdown link and anchor checking
- documentation index completeness
- forbidden legacy root detection
- public-child forbidden path/content checks
- generated-file provenance and clean-regeneration checks
- required root file checks
- stale code-symbol references
- duplicate heading or canonical-topic declarations
- catalog schema validation

