# Workspacepro Reference

Use each applicable section. Verify version-sensitive Git, manifest, task-runner, and schema behavior against current primary documentation.

## Contents

- [Evidence and safety](#evidence-and-safety)
- [Repository discovery](#repository-discovery)
- [Inventory matrix](#inventory-matrix)
- [Manifest contract](#manifest-contract)
- [Dependency and task model](#dependency-and-task-model)
- [Agent and documentation model](#agent-and-documentation-model)
- [Tool selection](#tool-selection)
- [Artifact schemas](#artifact-schemas)
- [Current primary sources](#current-primary-sources)

## Evidence and safety

Assign every check `VERIFIED`, `FINDING`, `NOT APPLICABLE`, or `UNVERIFIED`. Separate observed defects, policy contradictions, risks lacking runtime proof, and improvements.

Cite `file:line` for source evidence. For Git state record sanitized repo name/path, branch or detached state, abbreviated commit, dirty counts, worktree form, and inspection date. Do not copy changed file contents unless required to understand the finding.

Read-only audit commands include `git status --short`, `git rev-parse`, `git remote get-url`, `git branch --show-current`, `git symbolic-ref`, `git worktree list --porcelain`, `git submodule status`, and manifest validation. Do not fetch merely to calculate ahead/behind. Mark remote currency `UNVERIFIED` when local refs are insufficient.

Sanitize remote URLs by removing username/password userinfo from HTTP(S) URLs. Do not record tokens, environment values, credential-helper output, SSH private paths, or query fragments containing secrets.

## Repository discovery

Prefer explicit manifest paths. For an unmanifested collection, scan to a bounded depth selected from the observed layout. Avoid model caches, package dependencies, build outputs, vendor trees, and references unless they are in scope.

For each candidate use `git -C {path} rev-parse --is-inside-work-tree`. A `.git` path may be a directory or a gitfile used by worktrees and submodules. Use `--show-toplevel`, `--git-dir`, and `--git-common-dir` instead of resolving Git internals manually.

Classify:

- **Independent checkout** — distinct common Git directory and project history.
- **Main worktree** — primary working tree for a common Git directory.
- **Linked worktree** — shares common Git storage with another checkout.
- **Submodule** — gitlink-owned checkout inside a superproject.
- **Nested independent repo** — repository nested physically but not owned as a submodule.
- **Reference clone** — read-only evidence source by workspace policy.
- **Vendor checkout** — third-party source shipped or built as part of an owned project.

Canonicalize paths before checking containment. Record symlinks and external targets. Never infer ownership from physical nesting alone.

## Inventory matrix

For each project record:

| Field | Required evidence |
|---|---|
| Name and path | Unique workspace-relative identity |
| Role/lifecycle | Evidence or explicit `UNKNOWN` |
| Ownership | Team, product, or user decision |
| Git form | Independent, main/linked worktree, submodule, nested |
| Remote/ref/commit | Sanitized local Git evidence |
| Dirty state | Tracked/untracked counts |
| Toolchain | Manifest and version files |
| Stable tasks | Child-owned documented commands |
| Instructions/docs | Existing entry points and scope |
| Outputs/consumers | Public binary, package, service, schema, or asset |
| Dependencies | Kind, direction, compatibility, local override |
| Groups/profiles | Existing or recommended membership |
| Manifest/lock | Registered, absent, stale, or contradictory |
| Risks | Safety, portability, reproducibility, drift |

Also inventory shared docs, scripts, assets, protocols, references, models, fixtures, plans/goals, caches, and artifacts with ownership, authority, retention, consumers, and Git policy.

## Manifest contract

When no established manifest exists, prefer JSON so standard-library tooling and JSON Schema validation remain portable.

Example desired shape:

```json
{
  "version": 1,
  "workspace": {"name": "example-workspace", "topology": "sibling-repos"},
  "projects": [
    {
      "name": "api",
      "path": "services/api",
      "role": "service",
      "lifecycle": "active",
      "remote": "git@example.com:team/api.git",
      "default_ref": "main",
      "groups": ["core", "services", "ci"],
      "dependencies": [{"project": "protocol", "kind": "build"}],
      "tasks": {"build": "build", "test": "test"},
      "docs": {"readme": "README.md", "agents": "AGENTS.md"}
    }
  ],
  "shared_paths": [
    {"path": "docs", "kind": "documentation", "owner": "workspace"}
  ],
  "profiles": {
    "minimal": {"groups": ["core"], "tasks": ["validate"]}
  }
}
```

The exact schema may differ, but must define:

- Versioned format and topology.
- Unique project identity and portable path.
- Known roles and lifecycle.
- Sanitized remote and desired ref without local credentials.
- Groups, dependency kinds, stable task aliases, docs entry points, ownership, trust, and optionality.
- Shared paths, references, profiles, generated/local paths, and external-path policy.

The lock records exact commits and a canonical manifest digest. Compute the digest from canonical JSON with sorted keys and compact separators, excluding local overrides. A lock mismatch is a finding; do not silently regenerate it during validation.

Local overrides must be ignored and may change paths, profile selection, caches, private aliases, or resource settings, but never project identity, trust, or locked commit.

Validation includes duplicate names/paths, path escape, unknown enums/groups/dependencies, missing dependency targets, self-dependency, cycles, missing required docs, owned-to-reference editable coupling, invalid lock commits, missing required lock entries, extra stale lock entries, and manifest digest mismatch.

## Dependency and task model

Use a directed edge from consumer to dependency. Validate the graph as acyclic unless the workspace explicitly models a justified runtime cycle separately. Produce both dependency-first execution order and human-readable edges.

Classify dependencies: build, runtime, development, integration-test, documentation/reference, process/binary, package/API, or local override. Record version or compatibility boundary where evidenced.

Root task aliases must remain thin. A manifest task value should identify a trusted task alias owned by a child, not embed an arbitrary shell program when avoidable. Reference and vendor projects are non-executable by default.

Cross-repo runners define selection, dependency closure, order, concurrency, timeout, fail policy, result aggregation, JSON schema, environment-name allowlist, platform/profile filters, and trust boundary.

## Agent and documentation model

Root AGENTS instructions contain only universal workspace rules. Detailed guidance belongs in one-level agent documents; child instructions own child implementation. Require a scope-switch protocol before an agent edits another repository.

Documentation classes:

- `AUTHORITATIVE` — current contract, specification, or decision.
- `GUIDE` — supported procedure derived from authoritative sources.
- `RESEARCH` — evidence and alternatives, not binding policy.
- `REFERENCE` — external or illustrative context.
- `GENERATED` — reproducible report or index.
- `SUPERSEDED` — retained history with a current replacement.
- `ARCHIVED` — no longer active and not an implementation source.

An index names title, class, scope, owner, related projects, current path, and replacement when applicable. Use frontmatter only when the repository already supports it or validators will enforce it.

Cross-repo changesets record start/end SHA, repository authority, dependency order, compatibility window, gates, lock update, external actions, rollback, partial delivery, and final evidence. The root integration commit cannot make independent child commits atomic.

## Tool selection

Evaluate fit rather than sophistication:

| Option | Strong fit | Cautions |
|---|---|---|
| Existing root scripts | Small stable workspace | Avoid duplicated parsers and unsafe mutation defaults. |
| Make/Just/Task/package scripts | Thin discoverable task aliases | Do not embed repository registry in many files. |
| mise | Tool versions, profiles, namespaced tasks | Adds trust and version-management policy. |
| West | Manifest-driven multi-repo projects and groups | Brings Zephyr-oriented conventions and detached revisions. |
| Google Repo | Very large Git workspace with manifest workflows | Heavy operating model and XML manifest. |
| Git submodules | Superproject-owned pinned dependencies | Detached workflows and tighter parent ownership. |
| Custom standard-library CLI | Small precise contract and low dependency budget | Requires tests, ownership, and long-term maintenance. |

Do not adopt an external tool merely to avoid a small validator. Do not build a custom platform when an existing tool fits the approved workflow.

All mutating tools require dry-run output, explicit apply, dirty/local-commit protection, previous-state capture, partial-failure reporting, and recovery. Validation and status remain non-mutating.

## Artifact schemas

### WORKSPACE-AUDIT.md

Include users/outcomes, scope, methodology, evidence coverage, strengths, contradictions, prioritized findings, safety risks, and unverified checks.

### REPO-INVENTORY.md

Include root/control plane, project matrix, Git/worktree matrix, shared-path inventory, references, toolchains/tasks, docs/instructions, manifest/lock status, and unknowns.

### DEPENDENCY-MAP.md

Include owned project graph, reference relationships, dependency kinds, compatibility boundaries, groups, task order, cycles, and integration slices.

### INFORMATION-ARCHITECTURE.md

Include document classes, current map, target map, authoritative index, ownership, shared-resource rules, supersession/archive policy, and validation.

### MANIFEST-SPEC.md

Include format selection, desired schema, lock schema, local overrides, canonical digest, invariants, examples, lifecycle changes, and migration.

### AGENT-OPERATING-MODEL.md

Include instruction hierarchy, scope switching, Git boundaries, reference/vendor policy, search/discovery, changesets, gates, reporting, and conflict handling.

### TOOLING-SPEC.md

Include current tools, selected approach, command contracts, safety, trust, profiles, output schemas, fixtures, CI, rollout, and ownership.

### GOVERNANCE.md

Include roles, ownership, lifecycle procedures, exceptions, lock policy, documentation policy, changesets, external authority, and review cadence or conditions.

## Current primary sources

Consult current official documentation applicable to the selected model:

- Git repository layout: https://git-scm.com/docs/gitrepository-layout.html
- Git worktrees: https://git-scm.com/docs/git-worktree.html
- Git submodules: https://git-scm.com/docs/gitsubmodules
- Zephyr West manifests: https://docs.zephyrproject.org/latest/develop/west/manifest.html
- Zephyr West workspaces: https://docs.zephyrproject.org/latest/develop/west/workspaces.html
- Google Repo manifest format: https://gerrit.googlesource.com/git-repo.git/+/HEAD/docs/manifest-format.md
- mise tasks: https://mise.jdx.dev/tasks/
- JSON Schema: https://json-schema.org/learn/getting-started-step-by-step

Record access date, relevant versions, and inferences. Prefer Git and selected-tool documentation over secondary articles.
