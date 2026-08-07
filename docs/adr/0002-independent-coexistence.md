# ADR 0002: Independent coexistence with external skill libraries

- Status: Accepted
- Date: 2026-08-06

## Context

Gremlin Skills should install alongside other agent-skill libraries without name collisions, hidden dependencies, or overwritten files. Catalog parity through copied or look-alike skills would undermine independent ownership and make side-by-side installation confusing.

## Decision

Gremlin adopts interoperable package practices without reproducing another library's catalog. Optional libraries never become required dependencies. Gremlin names and aliases are checked against a committed, pinned reference snapshot. Intersections require explicit disposition; ordinary CI is offline and deterministic. A separate command proposes upstream snapshot changes without mutating the pin.

## Consequences

- No interviewing workflow, setup wrapper, or look-alike skill is added merely for count parity.
- Existing Gremlin names stay stable unless a Gremlin-specific routing or safety defect justifies migration.
- Clean-room installs must prove both package orders preserve foreign files.
- Public attribution is concise in the README and maintained in the acknowledgements without implying endorsement or copied content.
