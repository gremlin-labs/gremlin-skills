# ADR 0001: Registry as the package API

- Status: Accepted
- Date: 2026-08-06

## Context

README indexes, validators, evals, package discovery, host metadata, and install manifests previously maintained overlapping skill inventories. Independent directory scans could disagree without one surface noticing.

## Decision

`skills/registry.json` is the canonical inventory for every managed skill. It owns identity, source and documentation paths, category, maturity, invocation, authority, outputs, capabilities, contracts, dependencies, eval applicability, tests, distribution, provenance, and deprecation. Consumers share `scripts/skill_registry.py` and may scan the filesystem only to detect unregistered or missing paths.

## Consequences

- Public surfaces can be generated or validated deterministically.
- A new skill is incomplete until registered.
- Registry schema changes require versioning and mutation tests.
- Human prose remains curated; generated blocks own only mechanical identity and relationship fields.
