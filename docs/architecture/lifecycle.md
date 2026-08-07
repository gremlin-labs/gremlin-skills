# Skill lifecycle

## States

1. **Incubating** — evidence, routing boundaries, artifact contracts, and ownership are still being proven. Incubating skills are outside stable recursive plugin roots.
2. **Promoted** — public name, docs, evals, tests, package closure, and supported-host metadata are complete and stable.
3. **Misc** — maintained for a narrow or internal purpose but not promised as part of the stable collection.
4. **Deprecated** — no longer discoverable as a live stable skill; carries replacement or removal guidance and a compatibility window where applicable.

## Promotion evidence

Promotion requires one registry record, valid frontmatter, an explicit authority boundary, output and artifact contracts, applicable eval families, declared skill-local tests, human docs, package closure, and supported distribution metadata. Passing structural validation alone does not prove product usefulness or routing quality.

## Changes

Public names, aliases, installed paths, output roots, and pipeline slugs are compatibility surfaces. Change them only through an explicit migration record. Category moves may change repository paths but must preserve installed flat names and `agent-work` roots.

## Deprecation

Deprecated entries live outside stable recursive plugin roots. The registry records the replacement, last supported version, reason, and migration guidance. Validators reject live promoted references to an expired deprecated skill.

## Execution boundary

Local release preparation does not publish. Pushes, tags, hosted releases, uploads, marketplace entries, and global installation remain separate exact-action approvals.
