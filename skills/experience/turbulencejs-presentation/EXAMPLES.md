# Examples

## Adaptive first interview

After inspecting a repository with an existing brand and a launch brief, ask only what remains open:

> I found the product palette, type scale, and a six-minute launch brief. Before I storyboard: who is in the room, what should they believe or do at the end, should the motion feel more cinematic or more product-like, and will 9:16 be presented live or exported for social? I can start from 8–10 slides, intensity 2 with one optional level-3 beat, and a full reduced-motion endpoint if you have no stronger preference.

## Composed style contract excerpt

```md
## Influences

- Primary: developer-keynote — inspectable code, concise claims, restrained default rhythm
- Secondary: launch-trailer — sparse openings and one controlled escalation
- Secondary: technical-workshop — explicit state labels and teachable diagrams

## Conflict resolution

- Density: developer-keynote wins over launch-trailer; code remains readable rather than atmospheric.
- Motion: launch escalation is limited to slide 8; workshop step changes remain instant in reduced motion.
- Decoration: project brand tokens win; none of the guide palettes are copied literally.
```

## Layout role excerpt

```js
const layoutRoles = {
  architecture: {
    landscape: 'claim left; three labeled layers right; connectors travel horizontally',
    portrait: 'claim top; layers form a centered vertical stack; labels remain adjacent',
    safeArea: { landscape: '6% 6%', portrait: '8% 9%' },
    titleLines: { landscape: 3, portrait: 5 },
    focalPoint: { landscape: 'right-center', portrait: 'center-lower' }
  }
};
```

## Approval handoff

At gate 1, show the brief, slide-by-slide claims, density curve, selected influences, resolved conflicts, signature move, motion ceiling, and aspect rules. At gate 2, show exact-size 1920×1080 and 1080×1920 captures of the representative slide plus its reduced endpoint. Name what is still provisional and ask for an explicit decision.

## Validating a generated deck

The helper accepts a declarative JSON object with `slides` and `layoutRoles`. It deliberately refuses JavaScript modules so validation cannot execute deck code:

```sh
node skills/turbulencejs-presentation/scripts/validate-deck.mjs examples/presentation/src/deck.json
```

The validator reports semantic structure. It cannot replace browser geometry checks or visual inspection.
