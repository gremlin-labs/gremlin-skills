<!-- GENERATED CONTRACT SNAPSHOT
contract: work-artifacts
source: contracts/work-artifacts.md
source-version: 1
semantic-owner: gremlin-skills
source-sha256: 76a5bb9a63f0ea62200eda23794a179e4664526467b52cd7edb3ffa2bf93b43c
DO NOT EDIT: run python3 scripts/materialize_contracts.py --write
-->

<!-- contract-metadata
id: work-artifacts
version: 1
semantic-owner: gremlin-skills
-->

# Gremlin Skills — Work Artifact Contract

Use this contract for every skill-generated plan, audit, proposal, specification, execution log, quality report, migration record, test audit, restructure record, and release record.

## Canonical layout

```text
agent-work/
  README.md
  {slug}/
    WORK.md
    {skill-name}/
      ... skill-owned artifacts ...
```

Every ordinary skill writes only within its stage directory:

```text
{agent-work-root}/agent-work/{slug}/{skill-name}/
```

The only shared per-slug file is `agent-work/{slug}/WORK.md`. Compact History alone owns the reserved cross-slug namespace `agent-work/• compact-history/`. Do not create type-first roots such as `plans/`, `goals/`, `audits/`, `proposals/`, `feature-specs/`, `migrations/`, `releases/`, `tests/`, `restructures/`, or `brainstorms/` for new work.

## Resolve the agent-work root

Resolve ownership before writing:

1. Inspect applicable AGENTS instructions and a Workspacepro manifest or equivalent workspace registry.
2. If the target repository is a registered child of a parent workspace, the parent workspace is the agent-work root.
3. If the target is a standalone repository, that repository is the agent-work root.
4. If ownership is ambiguous and choosing would place internal material in a potentially public child, stop and ask one focused question.

Never create internal Gremlin work artifacts inside a workspace-managed child repository. Child repositories retain only documentation required to understand, build, test, contribute to, secure, release, and use that repository independently.

## Slug and stage ownership

- Use one stable kebab-case slug for the complete pipeline.
- Preserve the slug across brainstorm, audit, plan, execution, and release-preparation handoffs where they represent the same initiative.
- Use the exact skill name as the stage directory.
- Never silently suffix a conflicting slug. Reconcile whether it is the same initiative or stop.
- Releasepro uses the slug `release-v{version-slug}` unless an approved upstream initiative supplies a stable release slug. Derive `{version-slug}` by replacing non-alphanumeric version separators with hyphens.

Examples:

```text
agent-work/reduce-sync-overhead/brainstormpro/
agent-work/reduce-sync-overhead/planpro/
agent-work/reduce-sync-overhead/goalpro/

agent-work/stripe-renewal-correctness/stripe-audit/
agent-work/stripe-renewal-correctness/goalpro/

agent-work/release-v2-4-0/releasepro/
```

## WORK.md

Create `WORK.md` when the slug is first introduced. Later stages update it without deleting prior decisions.

Required sections:

```md
# Work: {slug}

## Outcome
## Ownership
## Status
## Stages
## Current handoff
## Decisions and material deltas
## Final evidence
```

Use lifecycle status `ACTIVE`, `COMPLETE`, `BLOCKED`, `ABANDONED`, or `SUPERSEDED`. Keep paths stable after completion. The sole exception is a user-confirmed Compact History run, which may relocate independently verified completed slug trees byte-for-byte into `agent-work/• compact-history/archive/` under the applicable project key.

The stage table records skill, status, primary artifact, and approval. Append material decisions and deltas; do not turn `WORK.md` into a duplicate plan or progress log.

## Stage isolation and links

- A skill owns files in its exact stage directory.
- Link sibling stages with relative paths; do not copy their contents.
- Goalpro consumes approved `GOALPRO-INPUT.md` from the upstream sibling stage and writes execution state in `goalpro/`.
- Feature Goal consumes Feature Clone artifacts from the `feature-clone/` sibling and writes to `feature-goal/`.
- Planpro may consume a proposal or brainstorm sibling while writing only to `planpro/`.
- Releasepro may cite completed goal stages without relocating their evidence.
- Compact History excludes its reserved namespace from discovery, preserves whole slug subtrees, preflights inbound links, and is the only skill permitted to create housekeeping summaries or archive completed initiatives.

## Compact History exception

`agent-work/• compact-history/` contains changelogs, current unfinished-work indexes, prompt-shaped TODOs, immutable preview/run manifests, rollback mappings, and archived completed initiatives. No other skill writes there.

Archival requires independent artifact plus implementation verification, exact source/destination digests, an immutable dry-run preview, explicit user confirmation naming its run or digest, stale-state revalidation, collision refusal, and a recovery journal. Unfinished, ambiguous, rejected, superseded, and terminal non-implementation initiatives remain at the actionable top level. Relative stage links remain stable because the whole slug directory moves as one unit.

## Durable documentation boundary

`agent-work/` is not the canonical source for current product or codebase behavior. Durable reader-facing knowledge belongs in root contract documents or `docs/`.

When work reveals durable knowledge:

1. Extract and rewrite it for the intended reader.
2. Verify it against current implementation and policy.
3. Place it in the canonical documentation structure.
4. Add it to the documentation index.
5. Keep the original work artifact as historical evidence.

Do not relabel a completed plan as current architecture documentation.

## Legacy compatibility

Legacy roots remain readable during migration but are never created for new work.

- Search the canonical stage first.
- If unfinished legacy state exists and canonical state does not, do not split execution state silently. Continue only under an explicit migration/reconciliation step.
- If both exist, compare sources and stop on conflicting state.
- Read-only skills may cite legacy artifacts as sources but write new output canonically.
- Execution skills migrate recognized legacy state before continuing when that migration is approved and lossless.
- Documentation Audit classifies legacy roots as `LEGACY_GENERATED_ROOT` and plans consolidation.

## Migration safety

A migration must:

- Run in dry-run mode first.
- Identify the owning skill from an unambiguous artifact signature or explicit mapping.
- Stop on unknown ownership, destination collision, conflicting slug, or path escape.
- Preserve bytes and relative relationships where possible.
- Rewrite links deliberately and verify them.
- Report every source, destination, skipped path, and error.
- Remove an empty legacy root only after all children migrate.
- Never overwrite an existing destination.

## Publication boundary

For workspace-managed projects:

- Parent workspace owns `agent-work/`, internal plans, goals, tasks, audits, proposals, style guides, product research, and cross-project knowledge.
- Child repositories own public/open-source-ready codebase documentation and no internal agent-work roots.
- Parent documents may link to child-public documentation.
- Child-required workflows must not depend on inaccessible parent-only material.

## Done for a skill stage

A stage is complete only when its required artifacts exist in the canonical stage, `WORK.md` reflects its state and handoff, relative links resolve, approval provenance is accurate, and no new legacy root was created.
