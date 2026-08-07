# Theme Library Reference

## Contents

- [Catalog scope](#catalog-scope)
- [How to choose a family](#how-to-choose-a-family)
- [Palette DNA and creative freedom](#palette-dna-and-creative-freedom)
- [Interpretation modes](#interpretation-modes)
- [Anti-cookie-cutter rules](#anti-cookie-cutter-rules)
- [Master family groups](#master-family-groups)
- [Product and reference families](#product-and-reference-families)
- [Family to semantic system](#family-to-semantic-system)
- [Maintenance and provenance](#maintenance-and-provenance)

## Catalog scope

Theme Library owns [PALETTE-MASTER.md](PALETTE-MASTER.md), the canonical human-readable publication document, and `assets/theme-family-catalog.json`, its canonical machine-readable companion. Both ship inside this skill and require no other repository or filesystem location. The current set contains 54 generated base families, 288 concrete variants, five GremlinLabs foundation palettes, 16 complete product palettes, and eight experimental reference families. Use the master document for exact values and browsing, the JSON for filtering, and this guide for interpretation.

Families provide personality and harmony evidence. Existing surface or role assignments are examples from their source context, not universal recipes. Variants suggest contrast, intensity, infusion, accent, or contextual possibilities. Do not mistake every generated variant for a separate design direction.

## How to choose a family

Filter in this order:

1. Product job and trust posture: operational, playful, editorial, clinical, creative, luxurious, nostalgic, restorative, or rebellious.
2. Surface mode and environment: light, dark, both, long-session, sunlight, OLED, presentation, data-dense, or content-heavy.
3. Information behavior: quiet neutrals with scarce semantic color versus expressive multi-accent systems.
4. Accessibility and localization: foreground/surface contrast, non-color cues, focus visibility, chart distinguishability, text expansion, and high-contrast needs.
5. Brand and content fit: imagery, typography, data visualization, code/syntax, illustrations, and status semantics.
6. Variant posture: subdued, standard, vibrant, electric, high contrast, alternate accent, or infused.

Shortlist two to four families. Compare them in representative product context before choosing; semantic roles may differ across directions when those differences are themselves part of the design logic.

## Palette DNA and creative freedom

Triangulate guidance and freedom with three layers:

1. **Identity anchors:** two to four colors or relationships that make the family recognizable. These are the strongest preservation candidates, not mandatory raw values.
2. **Character constraints:** temperature, chroma distribution, contrast rhythm, scarcity or abundance of accents, neutral bias, and emotional posture. Preserve the relationships more than exact hex values.
3. **Freedom zones:** surfaces, borders, text ladders, statuses, charts, focus, shadows, overlays, gradients, imagery coordination, complementary hues, and mode-specific ramps. Derive these for the product.

An interpretation may tint, shade, tone, mix, desaturate, intensify, warm, cool, or slightly rotate source hues. It may add neutrals, accessible status colors, complementary accents, and contrasting highlights absent from the catalog. It may omit catalog colors that create noise or semantic confusion. Record why the result still belongs to the family.

Exact values become trustworthy only after representative rendering and contrast/state checks. The catalog is a starting vocabulary, not a paint-by-number specification.

## Interpretation modes

| Mode | Preserve | Freedom | Use when |
|---|---|---|---|
| Interpretive (default) | Recognizable anchors and character relationships | High; derive or add any product-fit value | Most product design and Design Direction work |
| Fidelity | Named anchors and recognizable source-role intent | Medium; derive accessibility and missing-system values | User asks for the exact/canonical theme |
| Hybrid | Dominant family's anchors plus named borrowed quality | High but explicit; resolve collisions deliberately | Product benefits from a reasoned family combination |

Never infer fidelity merely because the user names a family. “Use Game Boy” normally means a recognizable Game Boy interpretation; “reproduce the Game Boy palette exactly” requests fidelity.

## Anti-cookie-cutter rules

- Begin with product content and component/state inventory, not a universal surface ladder.
- Do not assign the same swatch positions to canvas, card, border, accent, and status across every family.
- Let typography, imagery, density, material, data, and interaction alter how much color the interface can carry.
- Add colors when the source lacks accessible statuses, chart distinction, light/dark parity, or an intentional contrasting moment.
- Remove or mute colors when they compete with high-frequency content or semantic feedback.
- Preserve some asymmetry and surprise when it strengthens the product's personality.
- Explain derivation in terms of user outcome and harmony, not “the catalog says so.”
- Reject a technically complete mapping that feels generic in representative context.

## Master family groups

### Core Mischief

High-energy Gremlin identity: `gremlin-chaos`, `shadow-realm`, `midnight-mischief`, `void-protocol`, `obsidian-chaos`, `electric-rebellion`, `dank-gremlin`, `dank-gremlin-toxic`, and lethal-yellow families. Best for bold developer tools, experimental products, and expressive dark surfaces; use semantic color sparingly in dense workflows.

### Zen and Restorative

Quiet focus: `acceptance-mode`, `transcendence-purple`, lavender light/dark, `pure-void`, and `vibe-black`. Best for long sessions, reflective tools, wellness-adjacent products, and calm creative work. Watch muted-text contrast and avoid confusing low stimulus with weak hierarchy.

### Playful and Candy

Warm, friendly, high-character palettes: cherry candy, cotton candy, lemonade, creamsicle, marshmallow, Candyland, and cereal references. Best for consumer, social, creative, educational, and celebratory products. Preserve credible error/danger states and avoid letting every surface compete.

### Cosmic and Mystical

Nightmare purple, electric purple, moonlight, and crystal families. Best for imaginative developer/AI/creative tools and atmospheric media. Control glow, bloom, and multi-accent noise; validate dark-theme contrast and motion sensitivity.

### Retro Computing and Gaming

Commodore 64, Neon Arcade, Terminal Green, VHS Rewind, plus Atari, Game Boy, and Super Nintendo references. Best when nostalgia or hardware identity supports the product. Use the reference logic, not literal skeuomorphism everywhere; keep body text, forms, and error recovery modern and accessible.

### Nature and Environment

Arctic, concrete, copper, deep ocean, desert bloom, erosion, terra, stone, subway tile, and tidal pool. Best for grounded, tactile, environmental, mapping, infrastructure, and editorial products. Preserve material consistency and verify muted earth tones against status colors.

### Warm Culinary and Material

Deep cacao, cacao mint, and spilled latte. Best for premium warmth, hospitality, community, lifestyle, and calm editorial/productivity surfaces. Avoid brown-on-brown hierarchy collapse and keep interactive accents distinct.

### Professional and Neutral

Beige trousers, wrenchcore, labcoat, and sergeant families. Best for enterprise, clinical, operational, documentation, and high-density tools. Professional does not mean personality-free: use material, typography, and a disciplined accent system for identity.

### Luxury and Expressive

Powder room, rose gold, silk kimono, velvet underground, and reversed-chaos families. Best for fashion, beauty, culture, premium consumer, and expressive editorial work. Validate fine borders, muted foregrounds, and ornamental materials at real content density.

## Product and reference families

The catalog preserves all 18 source token roles for each CodeRank product palette: Default (Void), Chaos, Cheddar, Deep Cacao, Nightmare Purple, Obsidian Chaos, Pixelo Dark, Beige Box Dark, Vibe Lavender Dark, Vibe Marshmallow Dark, Vibe Moonlight, Glacier, Beige Box Light, Vibe Creamsicle Light, Vibe Lavender Light, and Vibe Marshmallow Light. A `mapsTo` value records a related generated Gremlin family without erasing the source palette's distinct role values.

Newer CodeRank directions preserve named role values for every supplied light/dark mode:

- **Gremlin Core:** electric green, blue, disruptive orange, hot pink, purple, mint, and chaotic yellow.
- **Vibe foundations:** Lavender, Marshmallow, Creamsicle, and Moonlight provide complete harmony sets beyond a single accent.
- **Atari:** warm CRT darkness, burnt orange, magenta, cyan, and cartridge gold.
- **Game Boy:** olive LCD neutrals with controlled sticker-like accents.
- **Super Nintendo:** warm console gray, cartridge purple-black, and compressed jewel accents.
- **Candyland:** warm pink light surfaces and unapologetically saturated candy accents.

Reference-only means the palette is available for product design even when no generated VS Code base family exists yet.

## Family to semantic system

Never expose family names or raw palette values directly in ordinary components. The mapping is generative rather than literal:

```text
family DNA + product context
  -> evolved primitive palette, ramps, and deliberate additions
  -> semantic roles per theme
  -> component recipes and data/content palettes
  -> state, contrast, responsive, and visual-regression tests
```

Cover the semantic capabilities the product actually needs: applicable surfaces and foregrounds, boundaries/focus/selection, interactions, statuses, charts/syntax, shadows/overlays, and reduced-transparency behavior. Do not force unused roles merely to mirror a source palette. Theme parity means equivalent capability and accessibility, not identical mood or identical role-to-hue mapping.

## Maintenance and provenance

Canonical exhaustive files live beside this guide:

- [PALETTE-MASTER.md](PALETTE-MASTER.md) — complete human-readable catalog.
- `assets/theme-family-catalog.json` — complete structured catalog.

Regenerate and verify the document with `python3 scripts/build_palette_master.py --check` from the Theme Library skill root. Imported GremlinLabs and CodeRank origins are retained as descriptive provenance inside the catalog; no external file is authoritative or required at runtime. New palette contributions must update the bundled JSON, regenerate the master document, preserve named roles and modes, and pass repository/global parity validation.
