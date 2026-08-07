# Releasepro — Policy, Verification, and Exact-Ref Safety

Inherit applicable release dimensions from [Goalpro's quality contract](contracts/execution-quality.md). Release-specific defaults are compatibility, supply-chain safety, package contents, exact provenance, operational rollout, and rollback.

## Contents

- [Policy precedence](#policy-precedence)
- [Release topology](#release-topology)
- [Version classification](#version-classification)
- [Preflight](#preflight)
- [Ecosystem-safe versioning](#ecosystem-safe-versioning)
- [Changelog and release evidence](#changelog-and-release-evidence)
- [Tags and exact-ref pushing](#tags-and-exact-ref-pushing)
- [Partial failure](#partial-failure)
- [Publication boundary](#publication-boundary)

## Policy precedence

Use this order:

1. Explicit user instruction for this release.
2. Repository release documentation, manifests, workspace configuration, and CI.
3. Established tags, changelog, package names, and prior release commits.
4. Ecosystem convention.
5. Generic SemVer defaults.

Stop when higher-priority signals conflict. Do not normalize a repository to a preferred convention during a release.

## Release topology

Inventory all release units before proposing versions:

| Topology | Signal | Behavior |
|---|---|---|
| Single package | One publishable manifest or binary | One version and tag following repository policy |
| Lockstep workspace | Workspace tooling and history release units together | Update only the declared lockstep units and shared lockfile |
| Independent workspace | Packages have distinct versions/tags/history | Classify and version each affected unit independently |
| Polyglot product | Multiple manifests build one shipped product | Follow documented product version source; do not assume every manifest owns the public version |
| Tag-only | Go module, binary, or hosted artifact with no version file | Tag according to repository convention |
| Dynamic/generated | Version comes from SCM or a generator | Use the established generator; do not hand-edit generated output without policy support |

If independent versus lockstep cannot be proven, stop and ask. “Multiple manifests” never implies “same version.”

## Version classification

Follow repository policy. When generic SemVer applies:

- Breaking public contract or required consumer migration → major.
- Backward-compatible capability → minor.
- Backward-compatible defect correction → patch.
- Documentation, tests, refactors, or dependencies → follow release policy; do not assume they are unreleaseable.
- Pre-1.0 breaking behavior → inspect prior convention; SemVer does not require one universal pre-1.0 bump policy.

When unsure whether a change is breaking, stop and present the evidence. Never choose a smaller bump to resolve uncertainty.

## Preflight

Record exact commands and concise outcomes in `RELEASE.md`:

- `git status --short` is empty.
- `git rev-parse HEAD`, current branch, upstream, and remotes are recorded.
- Local and remote target tags do not exist.
- Full configured tests, typecheck, lint, build, generated-file, and smoke gates pass.
- Packaging or dry-run output is inspected for contents, name, version, dependencies, provenance, and accidental secrets.
- CI status for the exact candidate SHA is green, or explicitly `UNVERIFIED` with a user decision when CI is required.
- The source diff matches the proposed changelog.

Use repository commands, not guessed defaults. If no working verification or package dry run exists, treat that as a release blocker unless the user explicitly approves a documented waiver.

## Ecosystem-safe versioning

Detect the package manager and existing scripts before choosing a mechanism:

- **npm-compatible**: prefer the repository's workspace/version tool. When using npm directly, a no-tag version operation can update manifest and lockfile; verify both and prevent automatic git tagging until Releasepro's tag phase.
- **Cargo**: use established workspace tooling when present; otherwise update the authoritative package version and verify `Cargo.lock`, metadata, build, and package output.
- **Python**: determine whether version lives in project metadata, a package module, SCM configuration, or a release tool. Update only authoritative sources and rebuild distributions.
- **Go**: versions are normally tags; verify module path, major-version suffix policy, and package tests.
- **Other or polyglot**: follow repository tooling and record every release unit affected.

Do not install a new release tool during a release. Propose that as separate maintenance work.

## Changelog and release evidence

Preserve existing format and history. A release entry should include only headings that contain changes and cite goal artifacts or commit SHAs.

`RELEASE.md` must record:

- Source range and exact candidate SHA.
- Release units and versions.
- Classification and rationale.
- User-visible changes and migration notes.
- Preflight and prepared-state commands with outcomes.
- Exact local tag and commit.
- Exact remote refs if pushed.
- Known waivers or unverified CI.
- Explicit statement that registry or hosted-release publication has not occurred.

## Tags and exact-ref pushing

Follow existing tag format and signing policy. Prefer an annotated tag when no policy exists. Before and after creation, verify:

- Tag name is unique locally and remotely.
- Tag object and peeled commit resolve to the intended release commit.
- Release commit contains the exact version and notes.

Before pushing, display exact values and obtain confirmation. Push explicit refspecs conceptually equivalent to:

```text
git push {remote} refs/heads/{branch}:refs/heads/{branch}
git push {remote} refs/tags/{tag}:refs/tags/{tag}
```

Never push all tags, rely on an implicit remote, or force-update a release ref.

## Partial failure

After each remote operation, retrieve the exact remote ref and compare its SHA:

- Branch succeeds, tag fails: report that the release commit is remote but unpublished by tag; retry only the same new tag after resolving the cause and renewed confirmation.
- Tag succeeds, branch fails: report that consumers may see the tag; do not move or delete it automatically.
- Verification returns an unexpected SHA: stop immediately and report a remote-state conflict.

Never hide partial success behind a generic “push failed.”

## Publication boundary

Releasepro may prepare locally and, with explicit authority, push exact Git refs. It must not:

- Run registry publication.
- Create or publish a GitHub/GitLab hosted release.
- Upload artifacts.
- Change distribution channels or access level.

Deliver the repository-appropriate operator command only after clearly stating that it remains unexecuted.
