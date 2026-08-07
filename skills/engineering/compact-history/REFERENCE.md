# Compact History Reference

## Contents

- Evidence and state
- Timestamp and ownership rules
- Stable identities
- Managed summaries
- Manifest and collisions
- follow-up decisions

## Evidence and state

Evidence precedence: latest semantic progress state; checked criteria with cited proof; final quality evidence; current code/tests/configuration; reachable Git commits; earlier plans and prose; filesystem metadata. Completion can be revoked by later reopening or regression evidence. `MIGRATED` is never completion.

Plan-only work is unfinished only when implementation was approved/intended. Terminal audits, research, rejected proposals, and feature-extraction-only requests are `TERMINAL_NON_IMPLEMENTATION`. `SKIP` can satisfy completion only when acceptance criteria make that slice optional. Unrelated workspace blockers do not invalidate a scoped verified result.

Confidence is `HIGH`, `MEDIUM`, or `LOW`; archival requires `HIGH`. Unknown evidence remains explicit.

## Timestamp and ownership rules

Accept `[YYYY-MM-DD HH:MM]`, timezone suffixes, date-only timestamps, and placeholder times. Prefer authored terminal/event timestamps, then corroborating commit dates, then Git file history. Record uncertain dates rather than inventing precision.

Ownership precedence: explicit WORK ownership; changeset/repository manifest; cited paths and commits; workspace manifest project keys; slug prefix only as a non-authoritative hint. One initiative can belong to multiple children and the workspace.

## Stable identities

Initiative ID hashes owning-root identity, original slug, and canonical source identity. Event ID hashes initiative ID, normalized date, outcome, and evidence locator. Finding ID hashes initiative ID, source locator, and category. Store IDs in HTML comments so reruns update managed blocks without prose matching.

## Managed summaries

Changelogs are append-only. In-progress and follow-up files are current-state indexes with compact-history-managed blocks. Preserve all user-authored text outside blocks. Corrections supersede prior entries; do not silently rewrite history.

A follow-up prompt includes outcome, context, verified gap, deferral reason, affected projects, likely code surfaces, constraints, non-goals, risks, decisions, evidence, and independently verifiable planning criteria.

## Manifest and collisions

Manifest operations are `write_managed_block` or `move_tree`. Every operation records expected prior state and intended post-state. The confirmation digest is SHA-256 of canonical JSON excluding the digest field.

If destination has the same initiative ID and identical digest, classify already archived. Same ID with different digest or same slug with different ID is a blocker. Never merge, suffix, or overwrite. Reject absolute operation paths, `..`, symlink escape, reserved-root aliases, and moves outside the owning `agent-work/`.

Preflight inbound links. Rewrite only links listed in the preview. Broken or ambiguous required links block archival.

## follow-up decisions

- `ACTIONABLE`: desired and sufficiently defined.
- `ACCEPTED_DEBT`: deliberately deferred, still worth retaining.
- `NEEDS_DECISION`: blocked on product/architecture choice.
- `REJECTED`: explicitly declined; historical only.
- `ALREADY_ADDRESSED`: later evidence closes it.
- `NON_ACTIONABLE`: observation, optional exclusion, or irrelevant limitation.

