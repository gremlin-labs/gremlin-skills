# Invocation architecture

## Two public invocation modes

Gremlin distinguishes auto-discoverable skills from explicit-invocation-only skills while keeping routing and authority decisions independent. The registry retains the stable machine values `model-visible` and `user-only`.

- **Auto-discoverable (`model-visible`):** a model may select the skill implicitly from its routing description, and a user may still invoke it explicitly.
- **Explicit invocation only (`user-only`):** the host does not expose the skill to implicit model selection; the human must name it. Once named, the model runs it normally.

Invocation is not authority. A model-visible audit remains read-only, while a user-only command may still require a second confirmation before an external action.

## Canonical source

`skills/registry.json` owns the abstract invocation mode and the Claude and Codex values. Host metadata is generated from that record and must agree. The owner approved the initial proposal SHA-256 `8ee99a986e4b38c0c4d59576c0690deba7cb51d02b7e09cfae7666a6bec67220` on 2026-08-06. On 2026-08-09 the owner approved making `landing-page` and `seo-content` auto-discoverable so the SEO pipeline's specialist routes are operational. The current 24 auto-discoverable / 12 explicit-only matrix has SHA-256 `0b1ac09e7a4674ca56ed4138df2735a01084d952480ba98f6a5fc61b78036e88`.

Codex expresses explicit-only behavior as `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Claude plugin payloads express it as `disable-model-invocation: true` in the staged `SKILL.md` frontmatter. Canonical source skill instructions keep portable `name` and `description` frontmatter; the plugin build applies only the host-owned Claude field.

## Classification test

A skill should be auto-discoverable only when autonomous routing is useful, near-miss fixtures distinguish it from adjacent skills, and implicit selection cannot silently broaden mutation or external-action authority. An explicit-only skill should explain its purpose in human-facing language and remain unavailable to implicit routing in every supported host.

## Composition constraint

An explicit-only skill cannot be a hidden dependency of another explicit-only wrapper. Pipeline dependencies that must be selected autonomously need an auto-discoverable contract, or the caller must embed the required behavior and retain artifact ownership.

An advertised specialist route is not operational merely because the downstream files exist in a package. The downstream skill must be present in generated payloads, expose host metadata matching the registry, and be selectable under the advertised invocation policy. After installing skills or changing invocation metadata, run the catalogue smoke test in a fresh host task so a stale task snapshot cannot mask or invent availability.

## Validation

Registry validation rejects host disagreements. Plugin validation verifies that generated Claude and Codex metadata expresses the same approved mode while preserving all non-host-specific source bytes. Trigger fixtures remain required only for registry-declared applicable skills. SEO pipeline tests additionally pin specialist discoverability and prohibit Strategy from restoring page-level briefs or a Goalpro page-content fallback.
