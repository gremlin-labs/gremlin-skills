# Contributing to Gremlin Skills

Thanks for helping improve the collection. Contributions should make a skill clearer, safer, more portable, or more effective without weakening its authority boundaries.

## Before changing a skill

Read [AGENTS.md](AGENTS.md) and the detailed [maintenance workflow](docs/maintaining-skills.md). Each managed skill has one record in `skills/registry.json`; that record controls its public identity, documentation, dependencies, evaluations, tests, and distribution.

Keep pull requests focused. Explain the user problem, the behavior being changed, and the evidence that the change is safe. Do not include generated work from `agent-work/`, private research or reference checkouts, credentials, local machine paths, or build artifacts.

## Required updates

When applicable, update all of the following together:

- the skill's `SKILL.md` and bundled resources;
- its registry record;
- its page under `docs/skills/`;
- routing, artifact, authority, quality, handoff, or product fixtures under `evals/`;
- declared tests, contracts, and third-party notices.

Refresh registry-owned documentation sections with:

```bash
python3 scripts/generate_docs.py --write
```

After the initial `0.1.0` candidate, add a Changeset for user-visible behavior, metadata, contracts, packaging, documentation, or migrations:

```bash
npm run changeset
```

## Validation

Run the complete local gate before opening a pull request:

```bash
python3 scripts/run_validation.py
```

The gate covers root and skill-local tests, documentation and contract drift, public-release safety, evaluation fixtures, standalone packages, flat host plugins, version synchronization, coexistence, and whitespace. A passing structural gate does not authorize external actions or prove an unexecuted workflow outcome.

## Pull-request expectations

- Preserve existing public names, aliases, output roots, and same-slug handoffs unless the change includes explicit migration guidance.
- Keep audit and direction skills read-only where their registry authority requires it.
- Use portable placeholders and runtime temporary directories instead of user-specific absolute paths.
- Add focused regression evidence for corrected behavior.
- Credit copied or substantially adapted work in the applicable third-party notice.
- Do not bundle an optional external skill as a hidden dependency.

By contributing, you agree that your contribution is submitted under the repository's root license.
