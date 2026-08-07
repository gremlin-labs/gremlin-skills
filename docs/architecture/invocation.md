# Invocation architecture

## Two public invocation modes

Gremlin distinguishes auto-discoverable skills from explicit-invocation-only skills while keeping routing and authority decisions independent. The registry retains the stable machine values `model-visible` and `user-only`.

- **Auto-discoverable (`model-visible`):** a model may select the skill implicitly from its routing description, and a user may still invoke it explicitly.
- **Explicit invocation only (`user-only`):** the host does not expose the skill to implicit model selection; the human must name it. Once named, the model runs it normally.

Invocation is not authority. A model-visible audit remains read-only, while a user-only command may still require a second confirmation before an external action.

## Canonical source

`skills/registry.json` owns the abstract invocation mode and the Claude and Codex values. Host metadata is generated from that record and must agree. The owner approved proposal SHA-256 `8ee99a986e4b38c0c4d59576c0690deba7cb51d02b7e09cfae7666a6bec67220` on 2026-08-06: 22 skills are auto-discoverable and 14 require explicit invocation.

Codex expresses explicit-only behavior as `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Claude plugin payloads express it as `disable-model-invocation: true` in the staged `SKILL.md` frontmatter. Canonical source skill instructions keep portable `name` and `description` frontmatter; the plugin build applies only the host-owned Claude field.

## Classification test

A skill should be auto-discoverable only when autonomous routing is useful, near-miss fixtures distinguish it from adjacent skills, and implicit selection cannot silently broaden mutation or external-action authority. An explicit-only skill should explain its purpose in human-facing language and remain unavailable to implicit routing in every supported host.

## Composition constraint

An explicit-only skill cannot be a hidden dependency of another explicit-only wrapper. Pipeline dependencies that must be selected autonomously need an auto-discoverable contract, or the caller must embed the required behavior and retain artifact ownership.

## Validation

Registry validation rejects host disagreements. Plugin validation verifies that generated Claude and Codex metadata expresses the same approved mode while preserving all non-host-specific source bytes. Trigger fixtures remain required only for registry-declared applicable skills.
