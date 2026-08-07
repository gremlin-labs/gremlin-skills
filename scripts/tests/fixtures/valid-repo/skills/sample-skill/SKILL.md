---
name: sample-skill
description: Performs a useful sample workflow. Use when testing the repository validator.
---

# Sample skill

```dot
digraph sample {
  start -> done;
}
```

See [REFERENCE.md](REFERENCE.md).
See [work-artifact contract](contracts/work-artifacts.md).

Write to `agent-work/{slug}/sample-skill/`.

## Optional shared Theme Library

Discover an independently installed Theme Library through the host registry or sibling skill directory.
