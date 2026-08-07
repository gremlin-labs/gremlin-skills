# AGENTS.md — Gremlin Skills maintenance invariants

Follow this file when changing the collection. The detailed creation workflow, examples, pipeline diagrams, and validator commands live in [docs/maintaining-skills.md](docs/maintaining-skills.md).

## Source of truth

- `skills/registry.json` is the canonical inventory and package API.
- This repository is authoritative. Do not make the global installation the editing source.
- Do not write to `~/.agents/skills`, publish, push, tag, upload, or mutate a marketplace without exact user approval.
- Preserve unrelated dirty-worktree changes and existing public names, aliases, output roots, and pipeline slugs.

## Required workflow

1. Design and approve the skill or material behavior change before implementation.
2. Write or update `SKILL.md` and bundled resources in the repository.
3. Update the registry record, curated human page under `docs/skills/`, applicable eval fixtures, declared tests, notices, and dependencies.
4. Run `python3 scripts/generate_plugin_manifests.py --write --clean` to refresh required host metadata and disposable flat plugin payloads.
5. Run `python3 scripts/generate_docs.py --write` only to refresh registry-owned documentation sections; never overwrite curated prose.
6. Run the full repository gate documented in [docs/maintaining-skills.md](docs/maintaining-skills.md).
7. Use `scripts/sync_installed_skills.py` for guarded repository-to-install synchronization. Dry-run first; applying to a real host installation remains a separate explicitly approved action.

## Skill-file invariants

- Frontmatter includes `name` and a third-person `description`; the first sentence says what the skill does and the second begins `Use when`.
- Skill names and tracking slugs are kebab-case.
- Every `SKILL.md` follows the capability requirements in the registry. Current promoted workflows require a top-level Graphviz `dot` decision tree.
- Use brace placeholders such as `{slug}` and `{version}`. XML-like angle-bracket placeholders are forbidden.
- Keep references one sibling level deep. Standalone packages must include every required dependency or a local contract snapshot.
- Prefer progressive disclosure based on clarity, not an arbitrary line limit.
- Every promoted skill includes generated `agents/openai.yaml` metadata matching its approved invocation mode. Claude-specific explicit-only frontmatter is added only to staged Claude plugin payloads.

## Authority and artifact invariants

- Generated work lives under `agent-work/{slug}/{skill-name}/`; `agent-work/{slug}/WORK.md` is the cross-skill index.
- `compact-history` alone owns `agent-work/• compact-history/` and may move verified completed work only after exact digest confirmation.
- Handoffs preserve the same slug, evidence, approval provenance, material deltas, and authority boundary.
- Audit and direction skills remain read-only where their registry record says so. Preview approval does not silently authorize implementation or external actions.
- Execution skills use Plan→Do→Verify, project-specific gates, canonical Goalpro quality, explicit self-judgment, and final integrated evidence.
- A gate that fails after three substantive fixes must be classified as downstream-blocking or local; local failures do not silently end the overall loop.

## Shared contracts

- Work artifacts: [contracts/work-artifacts.md](contracts/work-artifacts.md)
- Goalpro handoff: [contracts/goalpro-handoff.md](contracts/goalpro-handoff.md)
- Goalpro execution quality: [contracts/execution-quality.md](contracts/execution-quality.md)
- Planpro product research: [contracts/product-research.md](contracts/product-research.md)
- Package terminology: [CONTEXT.md](CONTEXT.md)
- Invocation policy: [docs/architecture/invocation.md](docs/architecture/invocation.md)
- Packaging policy: [docs/architecture/packaging.md](docs/architecture/packaging.md)

## Managed skill pointers

The block below is generated from `skills/registry.json`.

<!-- BEGIN GENERATED:AGENT-POINTERS -->
| Skill | Category | Authority | Output root | Human docs |
|---|---|---|---|---|
| `audit-compare` | engineering | read-only | `agent-work/{slug}/audit-compare/` | [docs/skills/audit-compare.md](docs/skills/audit-compare.md) |
| `audit-plan` | engineering | read-only | `agent-work/{slug}/audit-plan/` | [docs/skills/audit-plan.md](docs/skills/audit-plan.md) |
| `brainstormpro` | engineering | read-only | `agent-work/{slug}/brainstormpro/` | [docs/skills/brainstormpro.md](docs/skills/brainstormpro.md) |
| `compact-history` | engineering | executor | `agent-work/• compact-history/` | [docs/skills/compact-history.md](docs/skills/compact-history.md) |
| `design-direction` | experience | read-only | `agent-work/{slug}/design-direction/` | [docs/skills/design-direction.md](docs/skills/design-direction.md) |
| `design-review` | experience | read-only | `agent-work/{slug}/design-review/` | [docs/skills/design-review.md](docs/skills/design-review.md) |
| `designpro` | experience | read-only | `agent-work/{slug}/designpro/` | [docs/skills/designpro.md](docs/skills/designpro.md) |
| `documentation-audit` | engineering | read-only | `agent-work/{slug}/documentation-audit/` | [docs/skills/documentation-audit.md](docs/skills/documentation-audit.md) |
| `email-lifecycle-audit` | growth | read-only | `agent-work/{slug}/email-lifecycle-audit/` | [docs/skills/email-lifecycle-audit.md](docs/skills/email-lifecycle-audit.md) |
| `email-lifecycle-strategy` | growth | read-only | `agent-work/{slug}/email-lifecycle-strategy/` | [docs/skills/email-lifecycle-strategy.md](docs/skills/email-lifecycle-strategy.md) |
| `feature-clone` | engineering | read-only | `agent-work/{slug}/feature-clone/` | [docs/skills/feature-clone.md](docs/skills/feature-clone.md) |
| `feature-goal` | engineering | executor | `agent-work/{slug}/feature-goal/` | [docs/skills/feature-goal.md](docs/skills/feature-goal.md) |
| `gamepro` | experience | executor | `agent-work/{slug}/gamepro/` | [docs/skills/gamepro.md](docs/skills/gamepro.md) |
| `goalpro` | engineering | executor | `agent-work/{slug}/goalpro/` | [docs/skills/goalpro.md](docs/skills/goalpro.md) |
| `landing-page` | experience | hybrid | `agent-work/{slug}/landing-page/` | [docs/skills/landing-page.md](docs/skills/landing-page.md) |
| `migratepro` | engineering | executor | `agent-work/{slug}/migratepro/` | [docs/skills/migratepro.md](docs/skills/migratepro.md) |
| `motion-audit` | experience | read-only | `agent-work/{slug}/motion-audit/` | [docs/skills/motion-audit.md](docs/skills/motion-audit.md) |
| `motion-direction` | experience | read-only | `agent-work/{slug}/motion-direction/` | [docs/skills/motion-direction.md](docs/skills/motion-direction.md) |
| `onboarding-audit` | experience | read-only | `agent-work/{slug}/onboarding-audit/` | [docs/skills/onboarding-audit.md](docs/skills/onboarding-audit.md) |
| `onboarding-direction` | experience | read-only | `agent-work/{slug}/onboarding-direction/` | [docs/skills/onboarding-direction.md](docs/skills/onboarding-direction.md) |
| `planpro` | engineering | read-only | `agent-work/{slug}/planpro/` | [docs/skills/planpro.md](docs/skills/planpro.md) |
| `prose-humanizer` | experience | executor | `agent-work/{slug}/prose-humanizer/` | [docs/skills/prose-humanizer.md](docs/skills/prose-humanizer.md) |
| `releasepro` | engineering | executor | `agent-work/release-v{version-slug}/releasepro/` | [docs/skills/releasepro.md](docs/skills/releasepro.md) |
| `restructure` | engineering | executor | `agent-work/{slug}/restructure/` | [docs/skills/restructure.md](docs/skills/restructure.md) |
| `seo-content` | growth | executor | `agent-work/{slug}/seo-content/` | [docs/skills/seo-content.md](docs/skills/seo-content.md) |
| `seo-foundation` | growth | read-only | `agent-work/{slug}/seo-foundation/` | [docs/skills/seo-foundation.md](docs/skills/seo-foundation.md) |
| `seo-indexing` | growth | executor | `agent-work/{slug}/seo-indexing/` | [docs/skills/seo-indexing.md](docs/skills/seo-indexing.md) |
| `seo-monitor` | growth | read-only | `agent-work/{slug}/seo-monitor/` | [docs/skills/seo-monitor.md](docs/skills/seo-monitor.md) |
| `seo-setup` | growth | executor | `agent-work/{slug}/seo-setup/` | [docs/skills/seo-setup.md](docs/skills/seo-setup.md) |
| `seo-strategy` | growth | read-only | `agent-work/{slug}/seo-strategy/` | [docs/skills/seo-strategy.md](docs/skills/seo-strategy.md) |
| `stripe-audit` | growth | read-only | `agent-work/{slug}/stripe-audit/` | [docs/skills/stripe-audit.md](docs/skills/stripe-audit.md) |
| `testpro` | engineering | hybrid | `agent-work/{slug}/testpro/` | [docs/skills/testpro.md](docs/skills/testpro.md) |
| `theme-library` | experience | read-only | `agent-work/{slug}/theme-library/` | [docs/skills/theme-library.md](docs/skills/theme-library.md) |
| `turbulencejs-integration` | experience | executor | `agent-work/{slug}/turbulencejs-integration/` | [docs/skills/turbulencejs-integration.md](docs/skills/turbulencejs-integration.md) |
| `turbulencejs-presentation` | experience | executor | `agent-work/{slug}/turbulencejs-presentation/` | [docs/skills/turbulencejs-presentation.md](docs/skills/turbulencejs-presentation.md) |
| `workspacepro` | engineering | read-only | `agent-work/{slug}/workspacepro/` | [docs/skills/workspacepro.md](docs/skills/workspacepro.md) |
<!-- END GENERATED:AGENT-POINTERS -->
