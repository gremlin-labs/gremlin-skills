# Gremlin Skills context

## Purpose

Gremlin Skills is an independent collection of evidence-heavy agent workflows for planning, audits, product and design direction, growth systems, and verified execution. It can coexist with other skill libraries without copying their branded workflows or requiring them at runtime.

## Domain language

- **Skill:** one discoverable workflow with a stable kebab-case name and `SKILL.md` entrypoint.
- **Orchestrator:** a skill that coordinates several phases or other skills while retaining ownership of the user outcome and artifacts.
- **Specialist:** a bounded skill with deep domain judgment, explicit authority, and a narrow done condition.
- **Promoted:** supported in stable documentation, plugins, archives, and public installation.
- **Incubating:** still under evaluation and excluded from stable recursive discovery and distribution.
- **Misc:** maintained for a narrow use but not part of the promoted public collection.
- **Deprecated:** no longer discoverable as a live stable skill and accompanied by migration guidance.
- **Model-visible:** the model may select the skill implicitly when its routing description matches.
- **User-only:** only an explicit human invocation may select the skill.
- **Contract snapshot:** the local copy of a shared Gremlin contract bundled with a standalone skill so installation does not depend on the repository layout.
- **Dependency closure:** the complete set of skill files, contract snapshots, notices, and resources needed for a supported standalone package.
- **Artifact:** a durable, reviewable output written under `agent-work/{slug}/{skill-name}/` or an explicitly reserved exception.
- **Handoff:** a same-slug transition that preserves evidence, approval provenance, authority, and acceptance criteria between skills.

## Package boundary

The canonical inventory is `skills/registry.json`. Repository categories organize source and documentation; installed skill names remain flat and stable. Registry aliases are public identities and therefore participate in collision checks. No skill may silently depend on an external skill library.

## Authority boundary

Read-only skills may inspect source and write their own `agent-work` artifacts but may not mutate project source or external systems. Executors may change only the in-scope project and only within the user's authority. Hybrid skills have an explicit audit, preview, or approval boundary before mutation. External actions such as pushes, provider mutations, submissions, and publication retain separate approval requirements.

## Work lifecycle

All generated work is slug-first and skill-scoped. Direct handoffs preserve the slug. Audits and direction skills stop at evidence or an approved handoff; execution skills use Plan→Do→Verify and integrated quality evidence. Publication is not implied by a completed local release candidate.

## Compatibility posture

Interoperability with another library means compatible organization, packaging, and installation behavior—not copying its capability catalog. External libraries may be optional complements, never hidden dependencies, fork targets, or sources of names to recreate.
