# Maintaining Gremlin Skills

This document is the detailed workflow for creating and maintaining skills in this collection. [AGENTS.md](../AGENTS.md) carries the concise always-loaded invariants; this page owns the procedural detail, examples, and pipeline diagrams.

## Where skills live

This repository is the source of truth. `skills/registry.json` resolves each managed source directory, which may later be categorized without changing its public name. Host installations such as `~/.agents/skills/{skill-name}/` are flat projections produced from the repository; never edit them as the upstream source.

Installed copies are external state. Inspect and synchronize them only with the user's explicit authority, a dry-run manifest, and the guarded sync workflow. Repository validation never silently mutates a host installation.

## Workflow: creating a new skill

### 1. Brainstorm the design

Use the `brainstorming` skill. Ask clarifying questions one at a time. Propose 2-3 approaches with a recommendation. Get user approval on the design before drafting.

Key questions to cover:
- What task/domain does the skill cover?
- What are the specific triggers (the description field is the only thing the agent sees when deciding to load)?
- Does it need executable scripts or just instructions?
- Where does output live, and what shape?
- What's the stopping/done criteria?
- Does it hand off to another skill? If so, which, and is the slug shared?

### 2. Draft the skill

Write `SKILL.md` first. Follow the writing-skills rules:

- **Frontmatter:** `name` + `description` (max 1024 chars, third person, first sentence = what it does, second sentence = "Use when ...").
- **Completeness before line count.** Keep `SKILL.md` focused and navigable, but do not impose a hard line limit. Split detailed checklists, tool tables, and gotchas into `REFERENCE.md` when progressive disclosure makes the skill clearer—not merely to satisfy a size threshold.
- **No XML-like tags.** Path placeholders use `{slug}` / `{version}` etc., NEVER `<slug>` / `<version>` — angle-bracket tags get parsed as XML and break rendering.
- **Decision tree** as a graphviz `dot` block at the top of SKILL.md so the flow is visible at a glance.
- **Concrete examples** in the log format, folder layout, etc.
- **References one level deep** — link to REFERENCE.md or to sibling skills' SKILL.md/REFERENCE.md, never deeper.

### 3. Review with the user

Present the draft. Confirm:
- Does it cover the use cases?
- Anything missing or unclear?
- Should any section be more or less detailed?

Fold in revisions before writing files.

### 4. Register the skill in the repository

Create the source directory named by the registry, then add one registry record covering identity, category, maturity, documentation, invocation, authority, output, capabilities, contracts, dependencies, evals, tests, distribution, provenance, and deprecation.

Do not copy the draft to a global installation during authoring. Repository validation and package extraction must pass first.

### 5. Add human docs, evals, tests, and notices

- Add the curated page at `docs/skills/{skill-name}.md` using the common headings and generated registry block.
- Add all applicable trigger, artifact, quality, handoff, and product fixtures declared by the registry.
- Declare every skill-local test command.
- Add or index third-party notices whenever content is copied or substantially adapted.

### 6. Refresh generated metadata and sections

Run `python3 scripts/generate_plugin_manifests.py --write --clean` to refresh required Codex UI/invocation metadata and stage disposable flat Claude/Codex plugin payloads. Then run `python3 scripts/generate_docs.py --write`. The root README's catalog table is replaced between ordinary Markdown headings, so its public source contains no generator comments. Internal AGENTS, catalog, and skill-page registry sections retain explicit markers. Edit curated prose directly; never place prose that needs human judgment inside a generated section.

### 7. Double verification

Before considering the skill done, run the repository validators. This is the "double verification" step — the agent verifies its own work before declaring complete, and the user can re-run the same commands to confirm.

```bash
# Validator unit tests
python3 -m unittest discover -s scripts/tests -p 'test_*.py'

# Canonical inventory, human docs, and coexistence
python3 scripts/validate_registry.py
python3 scripts/generate_docs.py
python3 scripts/validate_docs.py
python3 scripts/generate_plugin_manifests.py --check
python3 scripts/validate_plugins.py

# One deterministic release-candidate gate (includes all checks below)
python3 scripts/run_validation.py

# Repository structure, frontmatter, decision trees, links, README entries,
# placeholders, and required host UI/invocation metadata
python3 scripts/validate_skills.py

# Trigger-routing and output-artifact fixture coverage
python3 scripts/validate_evals.py

# Installed parity is checked separately after an explicitly approved sync
python3 scripts/validate_skills.py --global-root "$HOME/.agents/skills"
```

All checks must pass:
- Validator tests are green.
- Every promoted skill has valid registry metadata, capability-applicable structure, resolved one-level references, no initializer/XML placeholders, generated registration, and curated human docs.
- Every skill has at least three positive and two near-miss routing fixtures plus an artifact contract.
- Repository and installed copies are recursively identical.
- Files are complete and navigable; split detail when progressive disclosure helps, not because of a fixed line count.

If any check fails, fix before declaring done.

## Category-layout migration

`migrations/skill-layout-v2.json` binds the proposed category destinations, compatibility invariants, exact pre-move and post-move tree digests, and every required Markdown link rewrite. Refreshing that proposal changes its approval hash whenever either byte state changes.

Previewing the operation is read-only:

```bash
python3 scripts/prepare_skill_layout.py --check
python3 scripts/apply_skill_layout.py
```

Applying or rolling back requires the owner-approved hash printed by the dry run:

```bash
python3 scripts/apply_skill_layout.py --apply --confirm sha256:{approved-proposal-sha256}
python3 scripts/apply_skill_layout.py --rollback --confirm sha256:{approved-proposal-sha256}
```

The apply path writes a recovery journal before moving anything, verifies the complete post-move state, and restores the exact registry, manifest, skill bytes, and flat paths if a transaction fails. Rollback refuses source, registry, or manifest drift; resolve that drift explicitly instead of forcing the operation.

After the immediate post-move gate passes, seal the one-time migration before making ordinary skill changes:

```bash
python3 scripts/apply_skill_layout.py --seal --confirm sha256:{approved-proposal-sha256}
```

Sealing preserves the approved path map and original byte digests as historical evidence, closes the filesystem rollback window, and lets later skill maintenance validate against the categorized registry. Restore a sealed migration through version control rather than replaying an obsolete tree snapshot.

## Workflow: updating an existing skill

1. Edit the repository source, registry, curated human docs, evals, tests, and notices as applicable.
2. Refresh generated sections and re-run the double-verification checks above.
3. Synchronize an installed copy only through the separately authorized, dry-run-first `scripts/sync_installed_skills.py` workflow.

## Conventions

These conventions are shared across all skills in this collection so they compose cleanly:

- **Kebab-case slugs** for all tracking folders (`add-rate-limit-retries`, not `Add_Rate_Limit_Retries`).
- **Same-slug pipeline:** when one skill hands off to another, both use the same slug so work is cross-referenceable by slug alone.
- **Single generated-work root:** every skill writes under `agent-work/{slug}/{skill-name}/`; `agent-work/{slug}/WORK.md` is the cross-skill index. Workspace-managed child repositories use the parent workspace's `agent-work/` root. See `contracts/work-artifacts.md`.
- **Reserved housekeeping exception:** `compact-history` alone owns `agent-work/• compact-history/` and may relocate verified completed slugs only after a digest-bound preview is explicitly confirmed.
- **Append-only progress logs** with status codes (`DONE`, `WIP`, `BLOCKED`, `SKIP`, `STRENGTHENED`, `FLAKE-FIXED`).
- **Plan→Do→Verify loop** inherited from goalpro across all execution skills (goalpro, feature-goal, gamepro, landing-page, prose-humanizer, migratepro, testpro, restructure, seo-content, seo-indexing, seo-setup, turbulencejs-integration).
- **Self-judgment required:** every step that logs DONE must include "I am satisfied this step is complete because …" alongside the machine gates.
- **Three-attempts rule:** same gate failing 3 substantive fixes in a row → classify blocker-vs-local, BLOCK+ask OR skip-to-next and keep looping. Local failures don't stop the loop.
- **Read-only where stated:** audit-compare, audit-plan, design-direction, design-review, designpro, email-lifecycle-audit, email-lifecycle-strategy, motion-audit, motion-direction, onboarding-audit, onboarding-direction, theme-library, workspacepro, feature-clone, brainstormpro (audit phase) never edit source code.
- **Project-specific verification gates:** skills detect the toolchain from manifest files and run the right suite (`tsc` + `oxlint` + `fallow` + tests for TS, etc.).
- **Canonical execution quality:** execution skills inherit `goalpro/QUALITY.md`, classify every dimension proportionally, and record final integrated evidence in `QUALITY-REPORT.md`.
- **Canonical Goalpro handoff:** direct upstream skills emit `GOALPRO-INPUT.md` under `goalpro/HANDOFF.md`, preserve the same slug, record approval provenance, and expose material deltas instead of repeating unchanged approval.
- **Canonical product research:** planning and audit skills inherit `planpro/PRODUCT-RESEARCH.md`, classify dimensions proportionally, and carry users, outcomes, quality attributes, delivery constraints, alternatives, and unknowns into handoffs.
- **Canonical palette library:** every skill except `theme-library` embeds its own optional discovery contract using the host skill registry or sibling skill directory, so independently installed skills do not depend on repository-level instructions. When found, Theme Library is consulted in embedded mode. Palette DNA guides creative derivation; source role assignments become mandatory only when exact fidelity is explicitly requested.
- **Acceptance criteria as "Done when ..."** checklists — each item independently verifiable.
- **Decision tree as a `dot` graph** at the top of every SKILL.md.
- **No XML-like tags in skill files** — use `{slug}` not `<slug>`.

## Skill index

See the generated [human skill catalog](skills/README.md) and the registry-owned pointers in [AGENTS.md](../AGENTS.md).

## Pipeline diagrams (canonical)

Plan-to-execution:
```
brainstormpro ─┐
               ├─→ planpro ──→ goalpro ──→ releasepro
feature-clone ─┴─→ feature-goal ──────────→ releasepro
designpro ───────────────→ goalpro ───────→ releasepro
design-direction ──→ planpro/goalpro ─────→ releasepro
onboarding-direction ──→ planpro/goalpro ─→ releasepro
email-lifecycle-strategy ──→ planpro/goalpro ─→ releasepro
theme-library ─────→ planpro/goalpro ─────→ releasepro
motion-audit ──→ optional motion-direction ──→ planpro/goalpro ──→ releasepro
motion-direction ───────────────────────────→ planpro/goalpro ──→ releasepro
goalpro ─────────────→ design-review ─────→ releasepro or goalpro correction
workspacepro ────────────→ goalpro ───────→ releasepro
gamepro ──→ First Playable ──→ MVP ──→ V1 ──→ optional Release Candidate ──→ releasepro
```

Audit-driven:
```
audit-compare ──→ (optional: goalpro)
audit-plan ──→ (optional: planpro → goalpro)
stripe-audit ──→ goalpro
designpro ──→ goalpro
motion-audit ──→ motion-direction or planpro/goalpro
onboarding-audit ──→ onboarding-direction ──→ planpro/goalpro
email-lifecycle-audit ──→ email-lifecycle-strategy ──→ planpro/goalpro
workspacepro ──→ goalpro
```

Shared palette consultation:
```
theme-library ──→ design-direction / designpro / design-review / motion-direction / planpro / goalpro
                  (embedded evidence; caller keeps artifact ownership)
```

TurbulenceJS planning consultation:
```
motion-audit ──→ motion-direction (when the future creative language is unresolved)
            └─→ planpro/goalpro (when remediation is concrete)
motion-direction ──→ turbulencejs-integration (public implementation reference)
                 └─→ planpro/goalpro (executes the approved TurbulenceJS-aware policy)
```

Onboarding improvement:
```
greenfield onboarding ───────────────────────→ onboarding-direction
implemented onboarding + audit only ────────→ onboarding-audit ──→ report
implemented onboarding + improve/redesign ──→ onboarding-audit ──→ onboarding-direction
                                                                    ├─→ prose-humanizer (embedded copy)
                                                                    └─→ approved preview → planpro/goalpro
```

Email lifecycle improvement:
```
greenfield lifecycle email ───────────────────────→ email-lifecycle-strategy
implemented program + audit only ────────────────→ email-lifecycle-audit ──→ report
implemented program + improve/refactor ──────────→ email-lifecycle-audit ──→ email-lifecycle-strategy
                                                                        ├─→ prose-humanizer (embedded copy)
                                                                        └─→ approved preview → planpro/goalpro
```

Standalone execution:
```
compact-history ──→ (terminal housekeeping)
migratepro ──→ (terminal)
restructure ──→ (terminal)
testpro ──→ (terminal)
turbulencejs-integration ──→ (terminal specialist integration)
landing-page ──→ (terminal landing-page preview and implementation)
prose-humanizer ──→ (terminal direct rewrite; embedded use stays with caller)
gamepro ──→ (terminal at requested playable milestone; optional Releasepro handoff)
```

Landing-page composition:
```
landing-page ──→ prose-humanizer (embedded copy pass; landing-page keeps artifact ownership)
             └─→ turbulencejs-integration (embedded implementation guidance)
             └─→ approved preview → direct Plan→Do→Verify implementation
```

SEO growth:
```
seo-setup ──→ seo-foundation ──→ seo-strategy ──┬─→ landing-page ──┐
                                                ├─→ seo-content ───┼─→ seo-indexing ──→ seo-monitor
                                                └─→ goalpro ───────┘                       ├─→ INDEXING ASSIST → seo-indexing
                                                                                          └─→ other measured routes
```

`seo-monitor` remains read-only. `seo-indexing` alone owns approved individual indexing requests and optional reminder/recurring submission jobs; `seo-setup` retains ownership of the shared `seo-stack` CLI and prerequisite configuration.

## Getting help

- Report issues with a skill: edit the skill file and submit a PR to this repo.
- To preview a managed installation: `python3 scripts/sync_installed_skills.py --target "$HOME/.agents/skills" --dry-run`. Applying requires explicit names or `--all`, `--apply`, and authority for the real host installation.
- To build independently installable Claude Code archives: `python3 scripts/package_skills.py --clean`; use positional skill names to package a subset.
- To verify installation: invoke any skill by its trigger phrase and confirm the agent loads it.
