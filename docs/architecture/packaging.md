# Packaging architecture

## Canonical inventory

`skills/registry.json` is the package API. Validators, documentation, tests, plugins, installers, and archive builders consume it rather than discovering skills independently from directory listings.

## Source and installed layouts

Repository categories may nest promoted skills under `skills/engineering/`, `skills/experience/`, and `skills/growth/`. Installed layouts remain flat: `{install-root}/{skill-name}/`. Names, aliases, frontmatter names, output roots, and pipeline slugs do not inherit category prefixes.

## Host plugin staging

Repository categories are an authoring and documentation concern, not the plugin payload shape. Current Codex plugin ingestion expects each bundled skill to be an immediate real directory under the manifest's `./skills/` root; Claude supports custom skill paths but its conventional plugin layout is also flat. Release builds therefore materialize registry-selected skills into disposable host-specific plugin roots as `skills/{skill-name}/`. They never point a plugin manifest directly at the categorized source root and never use symlinks.

Codex and Claude express user-only invocation through different metadata surfaces. The build may normalize only those host-owned metadata fields while preserving `SKILL.md` instructions and every other resource byte. The package manifest must record any such transformation, and validators compare the staged payload back to its registry record and source digest. This follows the current [OpenAI plugin packaging contract](https://developers.openai.com/plugins/build/plugins) and [Claude Code plugin structure](https://code.claude.com/docs/en/plugins-reference).

## Standalone closure

A standalone archive must contain its owning skill, required local contract snapshots, bundled resources, and applicable third-party notices. Optional integrations remain optional and must be discovered safely at runtime. A package validator extracts every archive outside the repository and validates it without relying on sibling source paths.

## Determinism

Archives use fixed timestamps and normalized permissions. Manifests record file counts, byte sizes, checksums, package version, and dependency closure. Deterministic CI uses a synthetic foreign-library fixture to verify collision handling and install-order independence without depending on a third-party catalog or the network.

## Installation ownership

The installer records only exact paths and hashes it created. Updates are dry-run-first, atomic per skill, cache-aware, and rollbackable. It refuses broad roots, unresolved variables, foreign files, and deletion outside its ownership manifest. Side-by-side tests install Gremlin and a synthetic foreign library in both orders into disposable homes.

## Release boundary

Building and validating release candidates is local work. Publication, marketplace mutation, global installation, push, tag, and upload require separately approved actions.
