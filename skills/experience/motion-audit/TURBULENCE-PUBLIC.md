# Public TurbulenceJS capability reference

Use this as a planning index, not proof of the target's installed version. Verify exact exports against the installed package or current public documentation before making an implementation claim.

## Public entrypoint families

| Family | Planning role | Default posture |
| --- | --- | --- |
| `turbulencejs` | Authored tracks, sequences, timing, ownership, and lifecycle | Foundation for semantic motion roles |
| `turbulencejs/subtle` | Restrained entrances, exits, settling, and feedback | Frequent and low-attention interactions |
| `turbulencejs/interact` | Direct-manipulation and spring-driven interaction continuity | Pointer/touch behavior with explicit ownership |
| `turbulencejs/cartoon` | Friendly overshoot, bubble, skedaddle, and expressive character | Occasional playful interactions |
| `turbulencejs/cinematic` | Editorial depth, anchored reveals, and spatial transitions | Occasional route, overlay, or explanatory motion |
| `turbulencejs/extreme` | Deliberate high-impact composed motion | Rare Signature moments only |
| `turbulencejs/effects` | Public named raster/effect recipes | Rare, bounded, fallback-backed Signature moments |
| `turbulencejs/surfaces` | Capture and render surfaces used by effects | Explicit origin, CSP, pixel, memory, and cleanup policy |
| `turbulencejs/surface-worker` | Public worker boundary for supported surface rendering | Rare effects with explicit worker ownership, fallback, termination, and cleanup |
| `turbulencejs/dom` | Browser/Electron-renderer target adaptation | Renderer-only ownership |
| `turbulencejs/main` | Electron main-process bounds and layout motion | Main-process ownership with destroyed-target guards |
| `turbulencejs/runtime` | Generic values, injected clocks, or host-defined rendering | Non-DOM or testable host-owned values |

## Intensity and frequency

- Intensity 0–1: essential feedback and high-frequency state continuity.
- Intensity 1–2: expressive product motion for common or occasional flows.
- Intensity 3: dramatic motion for meaningful, infrequent moments with explicit approval.
- Intensity 4: theatrical or raster-dominant behavior; rare, bounded, degradable, and explicitly approved.

Frequency outranks novelty. Continuous and frequent interactions prioritize immediate response. Expressive and Signature behavior belongs in occasional or rare moments unless runtime evidence proves otherwise.

## Public-safe verification

For every recommendation verify entrypoint availability, target/process boundary, interruption, retargeting, reduced endpoint, focus and input parity, teardown, idle work, performance/resource budget, and overlapping scheduler removal.

When a desired behavior is not supported by verified public capabilities, record only the user-visible need, public limitation, affected surfaces, supported fallback, impact, and acceptance evidence. Do not include maintainer workflow, internal architecture, private paths, extension designs, release steps, or contribution instructions.
