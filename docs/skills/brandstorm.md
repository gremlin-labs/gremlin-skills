# Brandstorm

Audit product evidence, develop user-directed product-name candidates, and research the approved finalists before the user makes the final naming decision.

## When to reach for it

Use Brandstorm to name or rename a product, app, game, service, company, or feature when the work should include product grounding, competitor discovery, iterative 20-name candidate rounds, preliminary collision research, and Porkbun domain checks.

## Prerequisites

Start with the codebase or undeveloped product idea, available user feedback, the user's brand direction, and any known market or platform constraints. Before targeted research, the user must confirm trademark jurisdictions, goods/services scope, mandatory stores, and domain policy.

Browser research requires either the host agent's built-in browser or an agent-accessible Chrome extension. Brandstorm does not substitute shell networking, search APIs, or scraping tools when those permitted surfaces are unavailable.

## Authority and safety

Brandstorm may inspect project and public evidence and write only its skill-scoped work artifacts. It does not edit project source, rename the product, reserve or purchase domains, file intellectual-property applications, create store listings, submit forms, contact rights holders, or mutate external accounts.

Trademark and patent results are preliminary research, not legal advice or professional clearance. Porkbun availability is an observed, timestamped state that can change immediately.

## Outputs

Work is owned at `agent-work/{slug}/brandstorm/`. The stage records the product and brand brief, competitor landscape, every 20-name round and user feedback, the approved finalist digest, complete clearance matrix, evidence ledger, quality report, and final user decision.

## Common questions

### Why are there two user gates?

The user first approves the exact 20 finalists that deserve expensive targeted research. After the evidence is complete, the user—not the model's ranking—selects the final name.

### What happens when all 20 names fail?

Brandstorm diagnoses the collision pattern, revises only the affected naming territories, produces another exact 20-name round, obtains approval, and reruns the complete targeted search. Browser-access failures remain blocked research; they do not trigger unnecessary renaming.

### Is Porkbun optional?

No. Every approved finalist must be checked through Porkbun for the user's exact domain policy. Brandstorm records availability, premium or aftermarket state when shown, URL or page reference, and timestamp without adding anything to a cart.

### Can it be installed alone?

Yes. It has no required sibling-skill dependency. Its standalone package includes local snapshots of the shared work-artifact, product-research, and quality contracts; browser control remains a host capability.

## Visible success

The user-approved 20-name finalist set has full trademark, patent, Steam, iOS App Store, Google Play, Mac App Store, Google Search, and Porkbun coverage; no unverified cell is presented as viable; the retry loop preserves prior evidence; and the user's explicit final decision is recorded without external mutation.

## Adjacent Gremlin skills

- `brainstormpro` explores product or engineering solutions when the outcome is known but the solution is not.
- `design-direction` defines a broader visual and interaction language after naming when identity direction remains unresolved.
- `theme-library` selects and adapts palette families; it does not own product naming.

## Registry contract

<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->
| Field | Registry value |
|---|---|
| Category | `experience` (promoted) |
| Invocation | `model-visible` |
| Authority | `read-only`; source mutation `never`; external actions `none` |
| Output root | `agent-work/{slug}/brandstorm/` |
| Required skills | None |
| Optional skills | None |
| Evaluation families | `trigger`, `artifact`, `quality`, `product` |
| Skill-local tests | No skill-local suite declared |
| Stable distributions | standalone_archive, stable_plugin, public_install |
<!-- END GENERATED:REGISTRY-CONTRACT -->
