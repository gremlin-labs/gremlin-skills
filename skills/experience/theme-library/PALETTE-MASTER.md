# Gremlin Palette Master

> Canonical, self-contained palette set bundled with the Theme Library skill. No external repository or local file is required.

## Contents

- [Ownership and use](#ownership-and-use)
- [Catalog coverage](#catalog-coverage)
- [Foundation palettes](#foundation-palettes)
- [Product palettes](#product-palettes)
- [Experimental reference families](#experimental-reference-families)
- [Generated family index](#generated-family-index)
- [Complete variant catalog](#complete-variant-catalog)
- [Provenance](#provenance)
- [Maintenance](#maintenance)

## Ownership and use

This document and `assets/theme-family-catalog.json` form the canonical published palette set for Theme Library and every skill that consults it. The JSON owns exact structured values; this document is its deterministic human-readable rendering. Treat palette values as foundations for exploration, not component styling instructions.

Always map a selected family through primitive ramps, semantic roles, component recipes, and accessibility/state tests. Ordinary components must never branch on palette or theme names and must never consume raw master values directly.

## Catalog coverage

- Generated families: **54**
- Concrete variants: **288**
- Foundation palettes: **5**
- Product palettes: **16**
- Experimental references: **8**
- Unassigned variants: **0**

| Category | Families |
|---|---:|
| Core Mischief | 10 |
| Zen and Restorative | 6 |
| Playful and Candy | 6 |
| Cosmic and Mystical | 4 |
| Retro Computing and Gaming | 4 |
| Nature and Environment | 10 |
| Warm Culinary and Material | 3 |
| Professional and Neutral | 6 |
| Luxury and Expressive | 5 |

## Foundation palettes

### Gremlin Core

Category: **Core Mischief**. Audacious brand energy with electric greens, disruptive orange, hot pink, purple, blue, mint, yellow, and explicit alert roles.

| Named color | Value | Intended character or role |
|---|---|---|
| Slurpy Blue | `#00A3FF` | Clear communication, trust |
| Gremlin Green | `#1FCC00` | Primary brand, success states |
| Electric Gremlin | `#4AFF33` | High energy accents |
| Disruptive Orange | `#FF5722` | Attention, warnings |
| Hot Pink Rebellion | `#FF0080` | Maximum impact |
| Mischief Purple | `#8000FF` | Creative chaos |
| Danger Red | `#CC2900` | Critical alerts |
| Warm Energy | `#FF7744` | Secondary actions |
| Radioactive Mint | `#00FF80` | Success explosions |
| Chaotic Yellow | `#FFD600` | Notifications, energy |

Alert mappings:

- **Danger:** `#CC2900` — Danger Red
- **Info:** `#00A3FF` — Slurpy Blue
- **Success:** `#27EE00` — Bright Gremlin
- **Warning:** `#FF5722` — Disruptive Orange

### Vibe Lavender

Category: **Zen and Restorative**. Spa-like lavender, sage, clay, dusty rose, aqua, and chamomile.

| Named color | Value | Intended character or role |
|---|---|---|
| Soft Sky Blue | `#9BB5D6` | Foundation color |
| Sage Green | `#A8C09A` | Foundation color |
| Mint Tea | `#B8CFB8` | (green alternative) |
| Warm Clay | `#E6B89C` | (orange) |
| Dusty Rose | `#D4A5C8` | (pink) |
| Soft Lavender | `#B19CD9` | (purple) |
| Muted Coral | `#D68B8B` | (red) |
| Peachy Blush | `#E6A89C` | (salmon) |
| Spa Aqua | `#9FC5C5` | (turquoise) |
| Chamomile | `#E6D5A8` | (yellow) |

Alert mappings:

- **Danger:** `#D68B8B` — Muted Coral
- **Info:** `#9BB5D6` — Soft Sky Blue
- **Success:** `#A8C09A` — Sage Green
- **Warning:** `#E6D5A8` — Chamomile

### Vibe Marshmallow

Category: **Playful and Candy**. Breakfast-cereal pastels with blueberry, mint, strawberry, grape, peach, and banana milk.

| Named color | Value | Intended character or role |
|---|---|---|
| Pale Blueberry Milk | `#B8D4E3` | Foundation color |
| Lucky Charm Green | `#C7E3C7` | Foundation color |
| Mint Marshmallow | `#D4E8D4` | (green alternative) |
| Creamy Orange | `#FFD4B8` | Foundation color |
| Strawberry Milk | `#FFB8D1` | (pink) |
| Grape Marshmallow | `#D1B8FF` | (purple) |
| Cherry Pastel | `#FFB8B8` | (red) |
| Peach Cream | `#FFC8B8` | (salmon) |
| Mint Cream | `#B8E3D4` | (turquoise) |
| Banana Milk | `#FFF4B8` | (yellow) |

Alert mappings:

- **Danger:** `#FFB8B8` — Cherry Pastel
- **Info:** `#B8D4E3` — Pale Blueberry Milk
- **Success:** `#C7E3C7` — Lucky Charm Green
- **Warning:** `#FFF4B8` — Banana Milk

### Vibe Creamsicle

Category: **Playful and Candy**. Warm orange sorbet with denim, pistachio, watermelon, lavender ice, coral, and mint chip.

| Named color | Value | Intended character or role |
|---|---|---|
| Soft Denim | `#A8C4D6` | (blue - more saturated) |
| Pistachio Cream | `#B8D6A8` | (green - more saturated) |
| Key Lime Sorbet | `#C4E0B4` | (green alternative) |
| Creamsicle Core | `#FFB88C` | (orange - more saturated) |
| Watermelon Sorbet | `#FFA8B8` | (pink - more saturated) |
| Lavender Ice | `#C8A8E0` | (purple - more saturated) |
| Strawberry Swirl | `#FF9999` | (red - more saturated) |
| Coral Cream | `#FFB09C` | (salmon - more saturated) |
| Mint Chip | `#9CD6C8` | (turquoise - more saturated) |
| Lemon Sorbet | `#FFE09C` | (yellow - more saturated) |

Alert mappings:

- **Danger:** `#FF9999` — Strawberry Swirl
- **Info:** `#A8C4D6` — Soft Denim
- **Success:** `#B8D6A8` — Pistachio Cream
- **Warning:** `#FFE09C` — Lemon Sorbet

### Vibe Moonlight

Category: **Cosmic and Mystical**. Dark cosmic color with aurora green, nebula pink, deep-space purple, cyan, coral, and starlight yellow.

| Named color | Value | Intended character or role |
|---|---|---|
| Cosmic Blue | `#5E9EFF` | Foundation color |
| Aurora Green | `#4EE89E` | Foundation color |
| Northern Light | `#6EF8BE` | (green alternative) |
| Sunset Ember | `#FF9E5E` | (orange) |
| Nebula Pink | `#FF6E9E` | Foundation color |
| Deep Space Purple | `#9E6EFF` | Foundation color |
| Mars Red | `#FF6E6E` | Foundation color |
| Cosmic Coral | `#FF8E7E` | (salmon) |
| Celestial Cyan | `#6EDEE8` | (turquoise) |
| Starlight Yellow | `#FFE86E` | Foundation color |

Alert mappings:

- **Danger:** `#FF6E6E` — Mars Red
- **Info:** `#5E9EFF` — Cosmic Blue
- **Success:** `#4EE89E` — Aurora Green
- **Warning:** `#FFE86E` — Starlight Yellow

## Product palettes

Each product palette preserves all source semantic roles. `Related generated family` is a discovery aid, not an instruction to replace these values.

### Default (Void)

Category: **Core Mischief**. Mode: **dark**. Related generated family: **void-protocol**.

Deep void with electric green accents

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#000000` | — |
| `background` | background | `#0A0A0A` | — |
| `surface` | surface | `#111111` | — |
| `elevated` | elevated | `#1A1A1A` | — |
| `hover` | hover | `#222222` | — |
| `border` | border | `#2A2A2A` | — |
| `border-subtle` | border-subtle | `#1F1F1F` | — |
| `foreground` | foreground | `#FAFAFA` | — |
| `muted` | muted | `#888888` | — |
| `subtle` | subtle | `#555555` | — |
| `accent` | accent | `#1FCC00` | — |
| `accent-bright` | accent-bright | `#4AFF33` | — |
| `accent-electric` | accent-electric | `#80FF66` | — |
| `success` | success | `#1FCC00` | — |
| `danger` | danger | `#FF4444` | — |
| `warning` | warning | `#FFDD00` | — |
| `info` | info | `#00D4FF` | — |
| `magic` | magic | `#8B5CF6` | — |

### Chaos

Category: **Core Mischief**. Mode: **dark**. Related generated family: **gremlin-chaos**.

Maximum mischief with neon greens and hot pink

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#1A1A1A` | — |
| `background` | background | `#262726` | — |
| `surface` | surface | `#2E2F2E` | — |
| `elevated` | elevated | `#383938` | — |
| `hover` | hover | `#424342` | — |
| `border` | border | `#4A4B4A` | — |
| `border-subtle` | border-subtle | `#3A3B3A` | — |
| `foreground` | foreground | `#E0E6D3` | — |
| `muted` | muted | `#9AA2A6` | — |
| `subtle` | subtle | `#666666` | — |
| `accent` | accent | `#1FCC00` | — |
| `accent-bright` | accent-bright | `#4AFF33` | — |
| `accent-electric` | accent-electric | `#64DE39` | — |
| `success` | success | `#1FCC00` | — |
| `danger` | danger | `#FF1998` | — |
| `warning` | warning | `#FFDC00` | — |
| `info` | info | `#339AFF` | — |
| `magic` | magic | `#C489FF` | — |

### Cheddar

Category: **Warm Culinary and Material**. Mode: **dark**. Related generated family: **none**.

Warm amber tones on deep brown

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#0D0906` | — |
| `background` | background | `#1A140D` | — |
| `surface` | surface | `#241C14` | — |
| `elevated` | elevated | `#2E241A` | — |
| `hover` | hover | `#3A2E22` | — |
| `border` | border | `#5D4D33` | — |
| `border-subtle` | border-subtle | `#443826` | — |
| `foreground` | foreground | `#FFDFB9` | — |
| `muted` | muted | `#C8A878` | — |
| `subtle` | subtle | `#8899AA` | — |
| `accent` | accent | `#F5A623` | — |
| `accent-bright` | accent-bright | `#FFC653` | — |
| `accent-electric` | accent-electric | `#FFD680` | — |
| `success` | success | `#00AD49` | — |
| `danger` | danger | `#F93E3E` | — |
| `warning` | warning | `#FFC653` | — |
| `info` | info | `#5899FF` | — |
| `magic` | magic | `#C489FF` | — |

### Deep Cacao

Category: **Warm Culinary and Material**. Mode: **dark**. Related generated family: **deep-cacao**.

Rich chocolate with golden yellow

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#1A1200` | — |
| `background` | background | `#261C00` | — |
| `surface` | surface | `#302400` | — |
| `elevated` | elevated | `#3C2E08` | — |
| `hover` | hover | `#4C4020` | — |
| `border` | border | `#5C5030` | — |
| `border-subtle` | border-subtle | `#4A4018` | — |
| `foreground` | foreground | `#EFDEBB` | — |
| `muted` | muted | `#A09080` | — |
| `subtle` | subtle | `#6A5A4A` | — |
| `accent` | accent | `#FFD600` | — |
| `accent-bright` | accent-bright | `#FFE233` | — |
| `accent-electric` | accent-electric | `#FFEE66` | — |
| `success` | success | `#1FCC00` | — |
| `danger` | danger | `#CC2900` | — |
| `warning` | warning | `#FF5722` | — |
| `info` | info | `#00A3FF` | — |
| `magic` | magic | `#9D51FF` | — |

### Nightmare Purple

Category: **Cosmic and Mystical**. Mode: **dark**. Related generated family: **nightmare-purple**.

Void purple with hot pink rebellion

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#120026` | — |
| `background` | background | `#1D0039` | — |
| `surface` | surface | `#281048` | — |
| `elevated` | elevated | `#3D2060` | — |
| `hover` | hover | `#4D2878` | — |
| `border` | border | `#5D3888` | — |
| `border-subtle` | border-subtle | `#3D2060` | — |
| `foreground` | foreground | `#E8D0FF` | — |
| `muted` | muted | `#9080A0` | — |
| `subtle` | subtle | `#6A5A7A` | — |
| `accent` | accent | `#FF0080` | — |
| `accent-bright` | accent-bright | `#FF40A0` | — |
| `accent-electric` | accent-electric | `#FF80C0` | — |
| `success` | success | `#1FCC00` | — |
| `danger` | danger | `#FF4000` | — |
| `warning` | warning | `#FFD600` | — |
| `info` | info | `#00A3FF` | — |
| `magic` | magic | `#9D51FF` | — |

### Obsidian Chaos

Category: **Core Mischief**. Mode: **dark**. Related generated family: **obsidian-chaos**.

Near-black with explosive yellow energy

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#080808` | — |
| `background` | background | `#121212` | — |
| `surface` | surface | `#1C1C1C` | — |
| `elevated` | elevated | `#282828` | — |
| `hover` | hover | `#404040` | — |
| `border` | border | `#505050` | — |
| `border-subtle` | border-subtle | `#383838` | — |
| `foreground` | foreground | `#FFFFC0` | — |
| `muted` | muted | `#909090` | — |
| `subtle` | subtle | `#606060` | — |
| `accent` | accent | `#FFD600` | — |
| `accent-bright` | accent-bright | `#FFE233` | — |
| `accent-electric` | accent-electric | `#FFEE66` | — |
| `success` | success | `#1FCC00` | — |
| `danger` | danger | `#CC2900` | — |
| `warning` | warning | `#FF5722` | — |
| `info` | info | `#00A3FF` | — |
| `magic` | magic | `#8000FF` | — |

### Pixelo Dark

Category: **Professional and Neutral**. Mode: **dark**. Related generated family: **none**.

Neon CMYK design system

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#141415` | — |
| `background` | background | `#1F1F20` | — |
| `surface` | surface | `#292929` | — |
| `elevated` | elevated | `#333333` | — |
| `hover` | hover | `#404040` | — |
| `border` | border | `#505050` | — |
| `border-subtle` | border-subtle | `#3A3A3A` | — |
| `foreground` | foreground | `#F8F8F8` | — |
| `muted` | muted | `#B0B0B0` | — |
| `subtle` | subtle | `#808080` | — |
| `accent` | accent | `#00ACE5` | — |
| `accent-bright` | accent-bright | `#00DBFF` | — |
| `accent-electric` | accent-electric | `#33E3FF` | — |
| `success` | success | `#00CF53` | — |
| `danger` | danger | `#D0006C` | — |
| `warning` | warning | `#99CC00` | — |
| `info` | info | `#00CDF2` | — |
| `magic` | magic | `#9D51FF` | — |

### Beige Box Dark

Category: **Professional and Neutral**. Mode: **dark**. Related generated family: **none**.

90s office nostalgia after hours

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#1A1814` | — |
| `background` | background | `#373025` | — |
| `surface` | surface | `#423A2E` | — |
| `elevated` | elevated | `#4D4438` | — |
| `hover` | hover | `#5A5040` | — |
| `border` | border | `#6A6050` | — |
| `border-subtle` | border-subtle | `#524A3E` | — |
| `foreground` | foreground | `#C8C0B0` | — |
| `muted` | muted | `#9A9284` | — |
| `subtle` | subtle | `#6A6258` | — |
| `accent` | accent | `#D0B080` | — |
| `accent-bright` | accent-bright | `#E0C8A0` | — |
| `accent-electric` | accent-electric | `#F0DCC0` | — |
| `success` | success | `#80B080` | — |
| `danger` | danger | `#B08070` | — |
| `warning` | warning | `#D0C090` | — |
| `info` | info | `#80A0C8` | — |
| `magic` | magic | `#A888A0` | — |

### Vibe Lavender Dark

Category: **Zen and Restorative**. Mode: **dark**. Related generated family: **vibe-lavender-dark**.

Zen spa coding vibes

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#201A28` | — |
| `background` | background | `#2D2436` | — |
| `surface` | surface | `#382E42` | — |
| `elevated` | elevated | `#3A2F48` | — |
| `hover` | hover | `#4A3D58` | — |
| `border` | border | `#5A4D66` | — |
| `border-subtle` | border-subtle | `#443858` | — |
| `foreground` | foreground | `#E8DFF0` | — |
| `muted` | muted | `#B0A0B8` | — |
| `subtle` | subtle | `#7A6A88` | — |
| `accent` | accent | `#B19CD9` | — |
| `accent-bright` | accent-bright | `#C8A8E8` | — |
| `accent-electric` | accent-electric | `#DCC0F8` | — |
| `success` | success | `#A8C09A` | — |
| `danger` | danger | `#D68B8B` | — |
| `warning` | warning | `#E6D5A8` | — |
| `info` | info | `#9BB5D6` | — |
| `magic` | magic | `#D4A5C8` | — |

### Vibe Marshmallow Dark

Category: **Playful and Candy**. Mode: **dark**. Related generated family: **vibe-marshmallow-dark**.

Pastel cereal on chocolate

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#1E1A18` | — |
| `background` | background | `#2A2420` | — |
| `surface` | surface | `#343028` | — |
| `elevated` | elevated | `#3A3028` | — |
| `hover` | hover | `#4A4038` | — |
| `border` | border | `#5A5048` | — |
| `border-subtle` | border-subtle | `#443C34` | — |
| `foreground` | foreground | `#FFF8F0` | — |
| `muted` | muted | `#C8C0B8` | — |
| `subtle` | subtle | `#8A8278` | — |
| `accent` | accent | `#FFB8D1` | — |
| `accent-bright` | accent-bright | `#FFB8E1` | — |
| `accent-electric` | accent-electric | `#FFC8E8` | — |
| `success` | success | `#C7E3C7` | — |
| `danger` | danger | `#FFB8B8` | — |
| `warning` | warning | `#FFF4B8` | — |
| `info` | info | `#B8D4E3` | — |
| `magic` | magic | `#D1B8FF` | — |

### Vibe Moonlight

Category: **Cosmic and Mystical**. Mode: **dark**. Related generated family: **vibe-moonlight-dark**.

Cosmic night sky exploration

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | `#080E1A` | — |
| `background` | background | `#0F1729` | — |
| `surface` | surface | `#182035` | — |
| `elevated` | elevated | `#1A2340` | — |
| `hover` | hover | `#2A3550` | — |
| `border` | border | `#3A4560` | — |
| `border-subtle` | border-subtle | `#283148` | — |
| `foreground` | foreground | `#E0E8F0` | — |
| `muted` | muted | `#8E9EAE` | — |
| `subtle` | subtle | `#5A6A7A` | — |
| `accent` | accent | `#6EDEE8` | — |
| `accent-bright` | accent-bright | `#8EE8F0` | — |
| `accent-electric` | accent-electric | `#AEF0F8` | — |
| `success` | success | `#4EE89E` | — |
| `danger` | danger | `#FF6E6E` | — |
| `warning` | warning | `#FFE86E` | — |
| `info` | info | `#5E9EFF` | — |
| `magic` | magic | `#9E6EFF` | — |

### Glacier

Category: **Zen and Restorative**. Mode: **light**. Related generated family: **none**.

Arctic ice, crisp and clean

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | — | `#FFFFFF` |
| `background` | background | — | `#E8F4FA` |
| `surface` | surface | — | `#F0F8FF` |
| `elevated` | elevated | — | `#D8EAF4` |
| `hover` | hover | — | `#C8DEF0` |
| `border` | border | — | `#A0D4F0` |
| `border-subtle` | border-subtle | — | `#C8E4F8` |
| `foreground` | foreground | — | `#1E2E3E` |
| `muted` | muted | — | `#4A6680` |
| `subtle` | subtle | — | `#7A9AB0` |
| `accent` | accent | — | `#5AACDC` |
| `accent-bright` | accent-bright | — | `#7AB0E0` |
| `accent-electric` | accent-electric | — | `#4A9AD0` |
| `success` | success | — | `#4A7A7A` |
| `danger` | danger | — | `#8B5A6B` |
| `warning` | warning | — | `#7A8A6A` |
| `info` | info | — | `#4A6A8B` |
| `magic` | magic | — | `#6B5A7A` |

### Beige Box Light

Category: **Professional and Neutral**. Mode: **light**. Related generated family: **none**.

Classic 90s office aesthetic

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | — | `#FFFFFF` |
| `background` | background | — | `#E8E0D0` |
| `surface` | surface | — | `#F5F0E8` |
| `elevated` | elevated | — | `#DED6C6` |
| `hover` | hover | — | `#D0C8B8` |
| `border` | border | — | `#C8B898` |
| `border-subtle` | border-subtle | — | `#DCD4C4` |
| `foreground` | foreground | — | `#3A3630` |
| `muted` | muted | — | `#5A5248` |
| `subtle` | subtle | — | `#8A8278` |
| `accent` | accent | — | `#8A7A5A` |
| `accent-bright` | accent-bright | — | `#A09060` |
| `accent-electric` | accent-electric | — | `#B0A070` |
| `success` | success | — | `#5A7A5A` |
| `danger` | danger | — | `#8B5A4A` |
| `warning` | warning | — | `#A09060` |
| `info` | info | — | `#5A6A7A` |
| `magic` | magic | — | `#7A5A6A` |

### Vibe Creamsicle Light

Category: **Playful and Candy**. Mode: **light**. Related generated family: **vibe-creamsicle-light**.

Orange sorbet summer

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | — | `#FFFFFF` |
| `background` | background | — | `#FFE7D0` |
| `surface` | surface | — | `#FFF2E8` |
| `elevated` | elevated | — | `#FFE0C8` |
| `hover` | hover | — | `#FFD8B8` |
| `border` | border | — | `#E8C8A8` |
| `border-subtle` | border-subtle | — | `#F0D8C0` |
| `foreground` | foreground | — | `#3A3028` |
| `muted` | muted | — | `#6A5A4A` |
| `subtle` | subtle | — | `#8A7A6A` |
| `accent` | accent | — | `#FF8844` |
| `accent-bright` | accent-bright | — | `#FF9966` |
| `accent-electric` | accent-electric | — | `#FFAA77` |
| `success` | success | — | `#A7CD94` |
| `danger` | danger | — | `#FF9999` |
| `warning` | warning | — | `#D1AB54` |
| `info` | info | — | `#8BACC2` |
| `magic` | magic | — | `#A27CBF` |

### Vibe Lavender Light

Category: **Zen and Restorative**. Mode: **light**. Related generated family: **vibe-lavender-light**.

Spa day zen

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | — | `#FFFFFF` |
| `background` | background | — | `#F3E2F6` |
| `surface` | surface | — | `#F9F0FC` |
| `elevated` | elevated | — | `#E8D4F0` |
| `hover` | hover | — | `#DCC8E8` |
| `border` | border | — | `#D6A7FF` |
| `border-subtle` | border-subtle | — | `#E4C8F8` |
| `foreground` | foreground | — | `#2D2436` |
| `muted` | muted | — | `#5A4D66` |
| `subtle` | subtle | — | `#8A7A9A` |
| `accent` | accent | — | `#9B7CC0` |
| `accent-bright` | accent-bright | — | `#B19CD9` |
| `accent-electric` | accent-electric | — | `#C8B0E8` |
| `success` | success | — | `#608060` |
| `danger` | danger | — | `#B06060` |
| `warning` | warning | — | `#A09060` |
| `info` | info | — | `#606090` |
| `magic` | magic | — | `#806090` |

### Vibe Marshmallow Light

Category: **Playful and Candy**. Mode: **light**. Related generated family: **vibe-marshmallow-light**.

Sweet pastel breakfast

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `void` | void | — | `#FFFFFF` |
| `background` | background | — | `#FFF8F0` |
| `surface` | surface | — | `#FFFCF8` |
| `elevated` | elevated | — | `#FFF0E8` |
| `hover` | hover | — | `#FFE8E0` |
| `border` | border | — | `#FFD0E8` |
| `border-subtle` | border-subtle | — | `#FFE0F0` |
| `foreground` | foreground | — | `#2A2420` |
| `muted` | muted | — | `#5A5048` |
| `subtle` | subtle | — | `#8A8078` |
| `accent` | accent | — | `#E890B8` |
| `accent-bright` | accent-bright | — | `#F0A0C8` |
| `accent-electric` | accent-electric | — | `#F8B0D8` |
| `success` | success | — | `#68A868` |
| `danger` | danger | — | `#C87878` |
| `warning` | warning | — | `#B8A050` |
| `info` | info | — | `#6888A8` |
| `magic` | magic | — | `#9878B8` |

## Experimental reference families

### Atari

Category: **Retro Computing and Gaming**. Mode: **dark**. Related generated family: **none**.

Atari product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#0D0906` | — |
| `--color-yellow` | CodeRank | `#FF6600` | — |
| `--color-purple` | Tastemaker | `#CC44AA` | — |
| `--color-blue` | Influence | `#44AACC` | — |
| `--color-green` | Success/Green | `#66BB44` | — |
| `--color-magenta` | Alert/Magenta | `#FF3366` | — |
| `--color-orange` | Warm accent | `#FFB300` | — |

### Candyland

Category: **Playful and Candy**. Mode: **light-and-dark**. Related generated family: **none**.

Candyland product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#2A050F` | `#FFF0F5` |
| `--color-yellow` | CodeRank | `#FF0055` | `#CC0044` |
| `--color-purple` | Tastemaker | `#9900FF` | `#7700CC` |
| `--color-blue` | Influence | `#0099FF` | `#0077CC` |
| `--color-green` | Success/Green | `#00CC66` | `#009944` |
| `--color-magenta` | Alert/Magenta | `#FF00AA` | `#CC0077` |
| `--color-orange` | Warm accent | `#FF7700` | `#CC5500` |

### Commodore 64

Category: **Retro Computing and Gaming**. Mode: **dark**. Related generated family: **commodore-64**.

Commodore 64 product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#1E1B38` | — |
| `--color-yellow` | CodeRank | `#FFD700` | — |
| `--color-purple` | Tastemaker | `#FF69B4` | — |
| `--color-blue` | Influence | `#55FFFF` | — |
| `--color-green` | Success/Green | `#55FF55` | — |
| `--color-magenta` | Alert/Magenta | `#FF55FF` | — |
| `--color-orange` | Warm accent | `#FFAA00` | — |

### Game Boy

Category: **Retro Computing and Gaming**. Mode: **dark**. Related generated family: **none**.

Game Boy product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#211E20` | — |
| `--color-yellow` | CodeRank | `#9AFF6E` | — |
| `--color-purple` | Tastemaker | `#C0EDEF` | — |
| `--color-blue` | Influence | `#A39BD6` | — |
| `--color-green` | Success/Green | `#7BA145` | — |
| `--color-magenta` | Alert/Magenta | `#DF529E` | — |
| `--color-orange` | Warm accent | `#EE9662` | — |

### Marshmallow Cereal

Category: **Playful and Candy**. Mode: **light-and-dark**. Related generated family: **vibe-marshmallow-light**.

Marshmallow Cereal product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#2A1E2C` | `#FDF8F0` |
| `--color-yellow` | CodeRank | `#FF6EB4` | `#E0007A` |
| `--color-purple` | Tastemaker | `#9B59FF` | `#6B00CC` |
| `--color-blue` | Influence | `#33C3FF` | `#0088CC` |
| `--color-green` | Success/Green | `#44D48A` | `#008855` |
| `--color-magenta` | Alert/Magenta | `#FF3399` | `#CC0066` |
| `--color-orange` | Warm accent | `#FF8C42` | `#CC5500` |

### Super Nintendo

Category: **Retro Computing and Gaming**. Mode: **light-and-dark**. Related generated family: **none**.

Super Nintendo product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#0E0C18` | `#D5D2CE` |
| `--color-yellow` | CodeRank | `#FFCC00` | `#CC8800` |
| `--color-purple` | Tastemaker | `#943CA6` | `#6B2FA0` |
| `--color-blue` | Influence | `#4E7AE8` | `#2255CC` |
| `--color-green` | Green | `#3ECC6E` | `#228C44` |
| `--color-magenta` | Magenta | `#E8327A` | `#B3004A` |
| `--color-orange` | Orange | `#FF8C22` | `#B85C00` |

### Terminal

Category: **Retro Computing and Gaming**. Mode: **dark**. Related generated family: **terminal-green**.

Terminal product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#040804` | — |
| `--color-yellow` | CodeRank | `#AAFF00` | — |
| `--color-purple` | Tastemaker | `#00FFCC` | — |
| `--color-blue` | Influence | `#33CCFF` | — |
| `--color-green` | Success/Green | `#00FF41` | — |
| `--color-magenta` | Alert/Magenta | `#FF00AA` | — |
| `--color-orange` | Warm accent | `#FFAA00` | — |

### VHS

Category: **Retro Computing and Gaming**. Mode: **dark**. Related generated family: **vhs-rewind**.

VHS product palette

| Role | Meaning | Dark | Light |
|---|---|---|---|
| `--color-background` | Background | `#08060F` | — |
| `--color-yellow` | CodeRank | `#FFE000` | — |
| `--color-purple` | Tastemaker | `#FF2D95` | — |
| `--color-blue` | Influence | `#00FFCC` | — |
| `--color-green` | Success/Green | `#44FF99` | — |
| `--color-magenta` | Alert/Magenta | `#FF00CC` | — |
| `--color-orange` | Warm accent | `#FF9933` | — |

## Generated family index

### Core Mischief

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Dank Gremlin | `dank-gremlin` | dark | 5 | `#032700` `#D0FFD0` `#032800` `#063500` `#0D9600` `#4AFF33` `#4DD732` `#6ED0E8` |
| Dank Gremlin Toxic | `dank-gremlin-toxic` | dark | 6 | `#032700` `#C0FFE0` `#032A00` `#053805` `#0D9600` `#00FF80` `#00FFE5` `#FF0080` |
| Electric Rebellion | `electric-rebellion` | dark | 5 | `#2D2D2D` `#FFE0F0` `#2C2C2C` `#383838` `#656565` `#FF0080` `#00FF99` `#0099FF` |
| Gremlin Chaos | `gremlin-chaos` | dark | 5 | `#2D2D2D` `#D1FFA2` `#2E2E2E` `#363636` `#656565` `#1FCC00` `#00FF80` `#0080FF` |
| Lethal Yellow | `lethal-yellow` | light | 5 | `#CBF000` `#1A1A1A` `#E0FF20` `#D0F500` `#829900` `#FF5722` `#009900` `#0066CC` |
| Lethal Yellow Reversed | `lethal-yellow-reversed` | light | 5 | `#CBF000` `#000000` `#E0FF20` `#D0F500` `#829900` `#8000FF` `#FF0080` `#00A3FF` |
| Midnight Mischief | `midnight-mischief` | dark | 6 | `#1C1C1C` `#E8E0FF` `#1D1D1D` `#252525` `#545454` `#B366FF` `#5AD87F` `#5A8FD8` |
| Obsidian Chaos | `obsidian-chaos` | dark | 5 | `#0D0D0D` `#F0E8D0` `#0E0E0E` `#161616` `#454545` `#FFD600` `#4DD732` `#6ED0E8` |
| Shadow Realm | `shadow-realm` | dark | 6 | `#2D2D2D` `#E0E0E0` `#2E2E2E` `#363636` `#656565` `#1FCC00` `#4DD732` `#6ED0E8` |
| Void Protocol | `void-protocol` | dark | 5 | `#000000` `#F0F0F0` `#030303` `#050505` `#333333` `#00FF80` `#0080FF` `#FF0080` |

### Zen and Restorative

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Acceptance Mode | `acceptance-mode` | dark | 5 | `#2D2D2D` `#D4D4D4` `#2E2E2E` `#363636` `#656565` `#A9DC76` `#78DCE8` `#E991E3` |
| Pure Void | `pure-void` | dark | 4 | `#0F0F0F` `#606060` `#101010` `#181818` `#474747` `#454545` `#485848` `#404858` |
| Transcendence Purple | `transcendence-purple` | dark | 6 | `#26292E` `#E0D8F0` `#262930` `#2E3037` `#585E6B` `#B366FF` `#66FF66` `#6666FF` |
| Vibe Black | `vibe-black` | dark | 5 | `#0F0F0F` `#C8C8C8` `#101010` `#181818` `#474747` `#00A3FF` `#A9DC76` `#78DCE8` |
| Vibe Lavender Dark | `vibe-lavender-dark` | dark | 5 | `#282130` `#E0D0F0` `#292032` `#312840` `#604D73` `#C8A8E8` `#A8C09A` `#9BB5D6` |
| Vibe Lavender Light | `vibe-lavender-light` | light | 6 | `#EFE7F0` `#4A3A5A` `#F8F3F9` `#F0EBF2` `#CBB0D0` `#9B7CC0` `#A8C09A` `#9BB5D6` |

### Playful and Candy

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Cherry Candy | `cherry-candy` | light | 6 | `#FFE1EB` `#4A2A3A` `#FFF5FA` `#FFE8F0` `#FF8AB1` `#FF88B8` `#88FF88` `#88B8FF` |
| Cotton Candy Brainrot | `cotton-candy-brainrot` | light | 4 | `#E1F1FF` `#4A4560` `#F5FAFF` `#E8F0FA` `#8AC8FF` `#FF88CC` `#7ABF8A` `#6A8ABF` |
| Lemonade Stand | `lemonade-stand` | light | 4 | `#FFF5CE` `#4A4535` `#FFFAE5` `#FFF4D5` `#FFE377` `#6ABF4A` `#5A8A4A` `#4A7A9A` |
| Vibe Creamsicle Light | `vibe-creamsicle-light` | light | 6 | `#FFE6CE` `#4A3020` `#FFF2E5` `#FFEAD5` `#FFBB77` `#FF8844` `#B8D6A8` `#A8C4D6` |
| Vibe Marshmallow Dark | `vibe-marshmallow-dark` | dark | 5 | `#25201C` `#FFE8D0` `#26201C` `#2E2824` `#64564C` `#FFB8E1` `#C7E3C7` `#B8D4E3` |
| Vibe Marshmallow Light | `vibe-marshmallow-light` | light | 5 | `#FFF1E1` `#410B26` `#FFFCF8` `#FFF4E8` `#FFC88A` `#FF99CC` `#C7E3C7` `#B8D4E3` |

### Cosmic and Mystical

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Crystal Healing | `crystal-healing` | light | 5 | `#FFE9F5` `#4A3A4A` `#FFFCFE` `#FFF0F8` `#FF92D0` `#D8B8FF` `#A8E8C8` `#A8C8E8` |
| Nightmare Purple | `nightmare-purple` | dark | 4 | `#180030` `#FFD0F0` `#190033` `#200042` `#51009F` `#FF0080` `#8F4FD8` `#6A4FD8` |
| Nightmare Purple Electric | `nightmare-purple-electric` | dark | 6 | `#180030` `#C0F0FF` `#190035` `#210043` `#51009F` `#00A3FF` `#00FF80` `#FF0080` |
| Vibe Moonlight Dark | `vibe-moonlight-dark` | dark | 6 | `#0D1322` `#E0E8FF` `#0C1426` `#121A2C` `#2A4174` `#6EDEE8` `#4EE89E` `#5E9EFF` |

### Retro Computing and Gaming

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Commodore 64 | `commodore-64` | dark | 5 | `#322572` `#70A4B2` `#302473` `#3A2C7F` `#5945C2` `#6C5EB5` `#B468A8` `#FFF468` |
| Neon Arcade | `neon-arcade` | dark, light | 5 | `#050505` `#00FFFF` `#060606` `#0E0E0E` `#3D3D3D` `#FF00FF` `#00FF00` `#FFFF00` |
| Terminal Green | `terminal-green` | dark | 5 | `#000000` `#00FF00` `#000800` `#001100` `#333333` `#00CC00` `#999999` `#B3B3B3` |
| VHS Rewind | `vhs-rewind` | dark | 8 | `#07050B` `#E0F0FF` `#080610` `#0C0A14` `#312759` `#FF00AA` `#00FF88` `#00E5FF` |

### Nature and Environment

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Arctic Aurora | `arctic-aurora` | light | 5 | `#EBF3FF` `#2A3344` `#FCFEFF` `#F5F8FC` `#94BFFF` `#00CC88` `#4488CC` `#FF88CC` |
| Concrete Jungle | `concrete-jungle` | dark | 6 | `#252525` `#D0D0D0` `#262626` `#2E2E2E` `#5D5D5D` `#FFCC00` `#7A8A5A` `#5A7A8A` |
| Copper Wire | `copper-wire` | dark | 5 | `#151210` `#D8C8B8` `#161210` `#1E1A18` `#544740` `#FF8844` `#4FA87F` `#4A8FA8` |
| Deep Ocean | `deep-ocean` | dark | 5 | `#00050B` `#88DDEE` `#000510` `#020A16` `#00317A` `#00CCCC` `#00CC88` `#00A8CC` |
| Desert Bloom | `desert-bloom` | dark | 6 | `#25201C` `#E0D0C0` `#26211C` `#2E2924` `#64584C` `#FF00AA` `#7A9A6A` `#6A8AAA` |
| Erosion Protocol | `erosion-protocol` | dark | 5 | `#35302E` `#C8C0B8` `#353028` `#403A37` `#716761` `#A8957A` `#8FA87A` `#7A8FA8` |
| Gremlin Terra | `gremlin-terra` | dark | 6 | `#211F24` `#E0D0C8` `#222025` `#2A272D` `#595260` `#1FCC00` `#4DD732` `#6ED0E8` |
| Mischief Stone | `mischief-stone` | dark | 6 | `#26292E` `#E0E0E0` `#26292F` `#2E3137` `#585E6B` `#8000FF` `#A9DC76` `#78DCE8` |
| Subway Tile | `subway-tile` | light | 6 | `#F2F2F2` `#1A1A1A` `#FCFCFC` `#F5F5F5` `#C7C7C7` `#5A9A7A` `#4A7A8A` `#CC8A9A` |
| Tidal Pool | `tidal-pool` | light | 6 | `#EBF5F5` `#2A3A3A` `#F8FCFC` `#F0F5F5` `#B1D8D8` `#5ACCCC` `#5AAA7A` `#4A8ACC` |

### Warm Culinary and Material

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Deep Cacao | `deep-cacao` | dark | 6 | `#2A1F00` `#B19073` `#241A00` `#322400` `#876200` `#A56F40` `#7A8F6A` `#6A7A8F` |
| Deep Cacao Mint | `deep-cacao-mint` | dark | 5 | `#231900` `#D0FFE0` `#281C00` `#302200` `#926A00` `#00FF80` `#5AD4B8` `#FFB8D1` |
| Spilled Latte | `spilled-latte` | light | 5 | `#F1E5DA` `#3A2F2A` `#F8F0E8` `#F0E8E0` `#D9BA9B` `#8F5A2A` `#7A8F6A` `#6A7A8F` |

### Professional and Neutral

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Beige Trousers | `beige-trousers` | light | 5 | `#EAD8AF` `#2A2A2A` `#F0E0BD` `#E8D9B6` `#D8B76A` `#1FCC00` `#8FAA7D` `#5A8FB8` |
| Beige Trousers Pro | `beige-trousers-pro` | light | 5 | `#EAD8AF` `#1E1E1E` `#F0E2C0` `#E5D6B3` `#D8B76A` `#00A3FF` `#7A9B6C` `#4A90B8` |
| Chaos Wrenchcore | `chaos-wrenchcore` | dark | 6 | `#1A1D25` `#D8E0E8` `#1B1E28` `#20232D` `#484F67` `#FC9867` `#8FB86B` `#6B8FB8` |
| Labcoat | `labcoat` | light | 5 | `#C4C6C2` `#1A1A1A` `#D0D2CE` `#999D95` `#0D9900` `#4A8FB8` `#B88FA8` `#B8B85A` |
| Labcoat Experimental | `labcoat-experimental` | light | 6 | `#C4C6C2` `#1A1A1A` `#D2CECC` `#C8C4C0` `#999D95` `#FF5722` `#4AFF33` `#00A3FF` |
| Sergeant Mischief | `sergeant-mischief` | dark | 6 | `#353A2B` `#D8D0C0` `#353A2A` `#404435` `#70795B` `#FFD700` `#7A8F5A` `#5A7A8F` |

### Luxury and Expressive

| Family | Slug | Modes | Variants | Representative swatches |
|---|---|---|---:|---|
| Chaos Reversed | `chaos-reversed` | dark | 5 | `#13151B` `#E0FFF0` `#141620` `#1A1C24` `#41475D` `#98A2B5` `#A9DC76` `#78DCE8` |
| Powder Room | `powder-room` | light | 5 | `#FFF1E1` `#3A3A4A` `#FFFCF8` `#FFF0E8` `#FFC88A` `#FFA8C8` `#A8D8A8` `#8FB8D8` |
| Rose Gold Empress | `rose-gold-empress` | dark | 5 | `#251C23` `#FFE8F0` `#26201C` `#2E242C` `#644C5F` `#FFB8D8` `#A8D8B8` `#B8A8D8` |
| Silk Kimono | `silk-kimono` | light | 5 | `#FFEEE6` `#4A3A3A` `#FFFCFA` `#FFF0EC` `#FFB18F` `#FFB8CC` `#7FB87F` `#6B9BD8` |
| Velvet Underground | `velvet-underground` | dark | 5 | `#140C14` `#E8D0E0` `#160C18` `#1E1220` `#5B345B` `#D8B86B` `#6BD86B` `#6B6BD8` |

## Complete variant catalog

### Acceptance Mode variants

Category: **Zen and Restorative**. Family slug: `acceptance-mode`. Representative variant: `gremlin-theme-acceptance-mode.json`.

Family palette: `#2D2D2D` `#D4D4D4` `#2E2E2E` `#363636` `#656565` `#A9DC76` `#78DCE8` `#E991E3` `#FFD866` `#FC9867` `#B7D175` `#BBBBBB`.

- **Gremlin Dark - Acceptance Mode Clarity** — dark — variant ID `gremlin-theme-acceptance-mode-high-contrast-clarity.json`
- **Gremlin Dark - Acceptance Mode Balanced** — dark — variant ID `gremlin-theme-acceptance-mode-infused-low-balanced.json`
- **Gremlin Dark - Acceptance Mode Flow** — dark — variant ID `gremlin-theme-acceptance-mode-medium-vibrant-flow.json`
- **Gremlin Dark - Acceptance Mode Tranquil** — dark — variant ID `gremlin-theme-acceptance-mode-subdued-tranquil.json`
- **Gremlin Dark - Acceptance Mode** — dark — variant ID `gremlin-theme-acceptance-mode.json`

### Arctic Aurora variants

Category: **Nature and Environment**. Family slug: `arctic-aurora`. Representative variant: `gremlin-theme-arctic-aurora.json`.

Family palette: `#EBF3FF` `#2A3344` `#FCFEFF` `#F5F8FC` `#94BFFF` `#00CC88` `#4488CC` `#FF88CC` `#FFCC66` `#FF9966` `#00FF99` `#CC6666`.

- **Gremlin Light - Arctic Aurora Glacier** — light — variant ID `gremlin-theme-arctic-aurora-high-contrast-glacier.json`
- **Gremlin Light - Arctic Aurora Northern Lights** — light — variant ID `gremlin-theme-arctic-aurora-infused-medium-northern-lights.json`
- **Gremlin Light - Arctic Aurora Polar Night** — light — variant ID `gremlin-theme-arctic-aurora-subdued-polar-night.json`
- **Gremlin Light - Arctic Aurora Solar Storm** — light — variant ID `gremlin-theme-arctic-aurora-vibrant-solar-storm.json`
- **Gremlin Light - Arctic Aurora** — light — variant ID `gremlin-theme-arctic-aurora.json`

### Beige Trousers variants

Category: **Professional and Neutral**. Family slug: `beige-trousers`. Representative variant: `gremlin-theme-beige-trousers.json`.

Family palette: `#EAD8AF` `#2A2A2A` `#F0E0BD` `#E8D9B6` `#D8B76A` `#1FCC00` `#8FAA7D` `#5A8FB8` `#D4B5B5` `#D4C85A` `#C4945A` `#A3B891`.

- **Gremlin Light - Beige Trousers Presentation** — light — variant ID `gremlin-theme-beige-trousers-high-contrast-presentation.json`
- **Gremlin Light - Beige Trousers Casual Friday** — light — variant ID `gremlin-theme-beige-trousers-infused-low-casual-friday.json`
- **Gremlin Light - Beige Trousers Boardroom** — light — variant ID `gremlin-theme-beige-trousers-subdued-boardroom.json`
- **Gremlin Light - Beige Trousers Promotion** — light — variant ID `gremlin-theme-beige-trousers-vibrant-promotion.json`
- **Gremlin Light - Beige Trousers** — light — variant ID `gremlin-theme-beige-trousers.json`

### Beige Trousers Pro variants

Category: **Professional and Neutral**. Family slug: `beige-trousers-pro`. Representative variant: `gremlin-theme-beige-trousers-pro.json`.

Family palette: `#EAD8AF` `#1E1E1E` `#F0E2C0` `#E5D6B3` `#D8B76A` `#00A3FF` `#7A9B6C` `#4A90B8` `#C4A5A5` `#C4B85A` `#B8845A` `#8FAA7D`.

- **Gremlin Light - Beige Trousers Executive** — light — variant ID `gremlin-theme-beige-trousers-pro-high-contrast-executive.json`
- **Gremlin Light - Beige Trousers Stakeholder** — light — variant ID `gremlin-theme-beige-trousers-pro-infused-low-stakeholder.json`
- **Gremlin Light - Beige Trousers IPO** — light — variant ID `gremlin-theme-beige-trousers-pro-medium-vibrant-ipo.json`
- **Gremlin Light - Beige Trousers Quarterly Report** — light — variant ID `gremlin-theme-beige-trousers-pro-subdued-quarterly-report.json`
- **Gremlin Light - Beige Trousers Pro** — light — variant ID `gremlin-theme-beige-trousers-pro.json`

### Chaos Reversed variants

Category: **Luxury and Expressive**. Family slug: `chaos-reversed`. Representative variant: `gremlin-theme-chaos-reversed.json`.

Family palette: `#13151B` `#E0FFF0` `#141620` `#1A1C24` `#41475D` `#98A2B5` `#A9DC76` `#78DCE8` `#E991E3` `#FFD866` `#FC9867` `#B7D175`.

- **Gremlin Dark - Chaos Reversed Paradox** — dark — variant ID `gremlin-theme-chaos-reversed-extreme-electric-paradox.json`
- **Gremlin Dark - Chaos Reversed Inverted** — dark — variant ID `gremlin-theme-chaos-reversed-high-contrast-inverted.json`
- **Gremlin Dark - Chaos Reversed Dimensional** — dark — variant ID `gremlin-theme-chaos-reversed-infused-medium-dimensional.json`
- **Gremlin Dark - Chaos Reversed Mirror** — dark — variant ID `gremlin-theme-chaos-reversed-subdued-mirror.json`
- **Gremlin Dark - Chaos Reversed** — dark — variant ID `gremlin-theme-chaos-reversed.json`

### Chaos Wrenchcore variants

Category: **Professional and Neutral**. Family slug: `chaos-wrenchcore`. Representative variant: `gremlin-theme-chaos-wrenchcore.json`.

Family palette: `#1A1D25` `#D8E0E8` `#1B1E28` `#20232D` `#484F67` `#FC9867` `#8FB86B` `#6B8FB8` `#B88FA8` `#B8A86B` `#A3B87F` `#B8C7D5`.

- **Gremlin Dark - Chaos Wrenchcore Plasma** — dark — variant ID `gremlin-theme-chaos-wrenchcore-electric-plasma.json`
- **Gremlin Dark - Chaos Wrenchcore Foundry** — dark — variant ID `gremlin-theme-chaos-wrenchcore-extreme-vibrant-foundry.json`
- **Gremlin Dark - Chaos Wrenchcore Forged** — dark — variant ID `gremlin-theme-chaos-wrenchcore-high-contrast-forged.json`
- **Gremlin Dark - Chaos Wrenchcore Oil Stained** — dark — variant ID `gremlin-theme-chaos-wrenchcore-infused-medium-oil-stained.json`
- **Gremlin Dark - Chaos Wrenchcore Rust** — dark — variant ID `gremlin-theme-chaos-wrenchcore-subdued-rust.json`
- **Gremlin Dark - Chaos Wrenchcore** — dark — variant ID `gremlin-theme-chaos-wrenchcore.json`

### Cherry Candy variants

Category: **Playful and Candy**. Family slug: `cherry-candy`. Representative variant: `gremlin-theme-cherry-candy.json`.

Family palette: `#FFE1EB` `#4A2A3A` `#FFF5FA` `#FFE8F0` `#FF8AB1` `#FF88B8` `#88FF88` `#88B8FF` `#FFE888` `#FFA888` `#A8FFA8` `#FF8888`.

- **Gremlin Light - Cherry Candy Rock Candy** — light — variant ID `gremlin-theme-cherry-candy-high-contrast-rock-candy.json`
- **Gremlin Light - Cherry Candy Swirled** — light — variant ID `gremlin-theme-cherry-candy-infused-medium-swirled.json`
- **Gremlin Light - Cherry Candy Pop Rocks** — light — variant ID `gremlin-theme-cherry-candy-medium-electric-pop-rocks.json`
- **Gremlin Light - Cherry Candy Taffy** — light — variant ID `gremlin-theme-cherry-candy-subdued-taffy.json`
- **Gremlin Light - Cherry Candy Sugar Rush** — light — variant ID `gremlin-theme-cherry-candy-vibrant-sugar-rush.json`
- **Gremlin Light - Cherry Candy** — light — variant ID `gremlin-theme-cherry-candy.json`

### Commodore 64 variants

Category: **Retro Computing and Gaming**. Family slug: `commodore-64`. Representative variant: `gremlin-theme-commodore-64.json`.

Family palette: `#322572` `#70A4B2` `#302473` `#3A2C7F` `#5945C2` `#6C5EB5` `#B468A8` `#FFF468` `#9F7E5B` `#548C9B` `#9B5252` `#E2DFF4`.

Related bundled palettes: Commodore 64.

- **Gremlin Dark - Commodore 64 Breadbin** — dark — variant ID `gremlin-theme-commodore-64-high-contrast-breadbin.json`
- **Gremlin Dark - Commodore 64 Datasette** — dark — variant ID `gremlin-theme-commodore-64-infused-low-datasette.json`
- **Gremlin Dark - Commodore 64 VIC-II** — dark — variant ID `gremlin-theme-commodore-64-subdued-vic-ii.json`
- **Gremlin Dark - Commodore 64 SID Chip** — dark — variant ID `gremlin-theme-commodore-64-vibrant-sid-chip.json`
- **Gremlin Dark - Commodore 64** — dark — variant ID `gremlin-theme-commodore-64.json`

### Concrete Jungle variants

Category: **Nature and Environment**. Family slug: `concrete-jungle`. Representative variant: `gremlin-theme-concrete-jungle.json`.

Family palette: `#252525` `#D0D0D0` `#262626` `#2E2E2E` `#5D5D5D` `#FFCC00` `#7A8A5A` `#5A7A8A` `#AA7A8A` `#FF6600` `#8A9A6A` `#B6B6B6`.

- **Gremlin Dark - Concrete Jungle Demolition** — dark — variant ID `gremlin-theme-concrete-jungle-extreme-electric-demolition.json`
- **Gremlin Dark - Concrete Jungle Brutalist** — dark — variant ID `gremlin-theme-concrete-jungle-high-contrast-brutalist.json`
- **Gremlin Dark - Concrete Jungle Graffiti** — dark — variant ID `gremlin-theme-concrete-jungle-infused-medium-graffiti.json`
- **Gremlin Dark - Concrete Jungle Overcast** — dark — variant ID `gremlin-theme-concrete-jungle-subdued-overcast.json`
- **Gremlin Dark - Concrete Jungle Construction** — dark — variant ID `gremlin-theme-concrete-jungle-vibrant-construction.json`
- **Gremlin Dark - Concrete Jungle** — dark — variant ID `gremlin-theme-concrete-jungle.json`

### Copper Wire variants

Category: **Nature and Environment**. Family slug: `copper-wire`. Representative variant: `gremlin-theme-copper-wire.json`.

Family palette: `#151210` `#D8C8B8` `#161210` `#1E1A18` `#544740` `#FF8844` `#4FA87F` `#4A8FA8` `#D8848F` `#FFB855` `#5FB88F` `#C6AF97`.

- **Gremlin Dark - Copper Wire High Voltage** — dark — variant ID `gremlin-theme-copper-wire-high-contrast-high-voltage.json`
- **Gremlin Dark - Copper Wire Oxidized** — dark — variant ID `gremlin-theme-copper-wire-infused-medium-oxidized.json`
- **Gremlin Dark - Copper Wire Patina** — dark — variant ID `gremlin-theme-copper-wire-subdued-patina.json`
- **Gremlin Dark - Copper Wire Live Wire** — dark — variant ID `gremlin-theme-copper-wire-vibrant-live-wire.json`
- **Gremlin Dark - Copper Wire** — dark — variant ID `gremlin-theme-copper-wire.json`

### Cotton Candy Brainrot variants

Category: **Playful and Candy**. Family slug: `cotton-candy-brainrot`. Representative variant: `gremlin-theme-cotton-candy-brainrot.json`.

Family palette: `#E1F1FF` `#4A4560` `#F5FAFF` `#E8F0FA` `#8AC8FF` `#FF88CC` `#7ABF8A` `#6A8ABF` `#CF7A9A` `#CFBF7A` `#CF9A7A` `#8ACF9A`.

- **Gremlin Light - Cotton Candy Brainrot Pixie** — light — variant ID `gremlin-theme-cotton-candy-brainrot-alt-accent-pixie.json`
- **Gremlin Light - Cotton Candy Brainrot Overdose** — light — variant ID `gremlin-theme-cotton-candy-brainrot-electric-overdose.json`
- **Gremlin Light - Cotton Candy Brainrot Melted** — light — variant ID `gremlin-theme-cotton-candy-brainrot-low-contrast-melted.json`
- **Gremlin Light - Cotton Candy Brainrot** — light — variant ID `gremlin-theme-cotton-candy-brainrot.json`

### Crystal Healing variants

Category: **Cosmic and Mystical**. Family slug: `crystal-healing`. Representative variant: `gremlin-theme-crystal-healing.json`.

Family palette: `#FFE9F5` `#4A3A4A` `#FFFCFE` `#FFF0F8` `#FF92D0` `#D8B8FF` `#A8E8C8` `#A8C8E8` `#FFB8E8` `#FFE8A8` `#FFC8A8` `#B8F8D8`.

- **Gremlin Light - Crystal Healing Clarity** — light — variant ID `gremlin-theme-crystal-healing-high-contrast-clarity.json`
- **Gremlin Light - Crystal Healing Aura** — light — variant ID `gremlin-theme-crystal-healing-infused-medium-aura.json`
- **Gremlin Light - Crystal Healing Meditation** — light — variant ID `gremlin-theme-crystal-healing-subdued-meditation.json`
- **Gremlin Light - Crystal Healing Charged** — light — variant ID `gremlin-theme-crystal-healing-vibrant-charged.json`
- **Gremlin Light - Crystal Healing** — light — variant ID `gremlin-theme-crystal-healing.json`

### Dank Gremlin variants

Category: **Core Mischief**. Family slug: `dank-gremlin`. Representative variant: `gremlin-theme-dank-gremlin.json`.

Family palette: `#032700` `#D0FFD0` `#032800` `#063500` `#0D9600` `#4AFF33` `#4DD732` `#6ED0E8` `#E986DD` `#FFDB62` `#FC975F` `#B1CE69`.

- **Gremlin Dark - Dank Gremlin Algae Bloom** — dark — variant ID `gremlin-theme-dank-gremlin-electric-algae-bloom.json`
- **Gremlin Dark - Dank Gremlin Abyss** — dark — variant ID `gremlin-theme-dank-gremlin-extreme-contrast-abyss.json`
- **Gremlin Dark - Dank Gremlin Bog** — dark — variant ID `gremlin-theme-dank-gremlin-infused-high-bog.json`
- **Gremlin Dark - Dank Gremlin Moss** — dark — variant ID `gremlin-theme-dank-gremlin-subdued-moss.json`
- **Gremlin Dark - Dank Gremlin** — dark — variant ID `gremlin-theme-dank-gremlin.json`

### Dank Gremlin Toxic variants

Category: **Core Mischief**. Family slug: `dank-gremlin-toxic`. Representative variant: `gremlin-theme-dank-gremlin-toxic.json`.

Family palette: `#032700` `#C0FFE0` `#032A00` `#053805` `#0D9600` `#00FF80` `#00FFE5` `#FF0080` `#FFD600` `#FF8800` `#8DFFC7` `#FF3300`.

- **Gremlin Dark - Dank Gremlin Meltdown** — dark — variant ID `gremlin-theme-dank-gremlin-toxic-electric-meltdown.json`
- **Gremlin Dark - Dank Gremlin HAZMAT** — dark — variant ID `gremlin-theme-dank-gremlin-toxic-extreme-contrast-hazmat.json`
- **Gremlin Dark - Dank Gremlin Biohazard** — dark — variant ID `gremlin-theme-dank-gremlin-toxic-high-vibrant-biohazard.json`
- **Gremlin Dark - Dank Gremlin Contaminated** — dark — variant ID `gremlin-theme-dank-gremlin-toxic-infused-high-contaminated.json`
- **Gremlin Dark - Dank Gremlin Quarantine** — dark — variant ID `gremlin-theme-dank-gremlin-toxic-subdued-quarantine.json`
- **Gremlin Dark - Dank Gremlin Toxic** — dark — variant ID `gremlin-theme-dank-gremlin-toxic.json`

### Deep Cacao variants

Category: **Warm Culinary and Material**. Family slug: `deep-cacao`. Representative variant: `gremlin-theme-deep-cacao.json`.

Family palette: `#2A1F00` `#B19073` `#241A00` `#322400` `#876200` `#A56F40` `#7A8F6A` `#6A7A8F` `#BA7A8A` `#CAB85A` `#BA8A5A` `#8FA87A`.

Related bundled palettes: Deep Cacao.

- **Gremlin Dark - Deep Cacao Espresso** — dark — variant ID `gremlin-theme-deep-cacao-electric-espresso.json`
- **Gremlin Dark - Deep Cacao Truffle** — dark — variant ID `gremlin-theme-deep-cacao-extreme-contrast-truffle.json`
- **Gremlin Dark - Deep Cacao Dark Roast** — dark — variant ID `gremlin-theme-deep-cacao-high-vibrant-dark-roast.json`
- **Gremlin Dark - Deep Cacao Mocha** — dark — variant ID `gremlin-theme-deep-cacao-infused-medium-mocha.json`
- **Gremlin Dark - Deep Cacao Milk** — dark — variant ID `gremlin-theme-deep-cacao-subdued-milk.json`
- **Gremlin Dark - Deep Cacao** — dark — variant ID `gremlin-theme-deep-cacao.json`

### Deep Cacao Mint variants

Category: **Warm Culinary and Material**. Family slug: `deep-cacao-mint`. Representative variant: `gremlin-theme-deep-cacao-mint.json`.

Family palette: `#231900` `#D0FFE0` `#281C00` `#302200` `#926A00` `#00FF80` `#5AD4B8` `#FFB8D1` `#FFE86E` `#D4945A` `#4AFF33` `#9DFFBE`.

- **Gremlin Dark - Deep Cacao Peppermint Bark** — dark — variant ID `gremlin-theme-deep-cacao-mint-electric-peppermint-bark.json`
- **Gremlin Dark - Deep Cacao After Eight** — dark — variant ID `gremlin-theme-deep-cacao-mint-high-vibrant-after-eight.json`
- **Gremlin Dark - Deep Cacao Mint Chip** — dark — variant ID `gremlin-theme-deep-cacao-mint-infused-high-mint-chip.json`
- **Gremlin Dark - Deep Cacao White Chocolate Mint** — dark — variant ID `gremlin-theme-deep-cacao-mint-subdued-white-chocolate.json`
- **Gremlin Dark - Deep Cacao Mint** — dark — variant ID `gremlin-theme-deep-cacao-mint.json`

### Deep Ocean variants

Category: **Nature and Environment**. Family slug: `deep-ocean`. Representative variant: `gremlin-theme-deep-ocean.json`.

Family palette: `#00050B` `#88DDEE` `#000510` `#020A16` `#00317A` `#00CCCC` `#00CC88` `#00A8CC` `#FF88CC` `#FFCC00` `#FF6644` `#00FFAA`.

- **Gremlin Dark - Deep Ocean Bioluminescent** — dark — variant ID `gremlin-theme-deep-ocean-electric-bioluminescent.json`
- **Gremlin Dark - Deep Ocean Abyss** — dark — variant ID `gremlin-theme-deep-ocean-extreme-contrast-abyss.json`
- **Gremlin Dark - Deep Ocean Pressure** — dark — variant ID `gremlin-theme-deep-ocean-infused-high-pressure.json`
- **Gremlin Dark - Deep Ocean Twilight Zone** — dark — variant ID `gremlin-theme-deep-ocean-subdued-twilight-zone.json`
- **Gremlin Dark - Deep Ocean** — dark — variant ID `gremlin-theme-deep-ocean.json`

### Desert Bloom variants

Category: **Nature and Environment**. Family slug: `desert-bloom`. Representative variant: `gremlin-theme-desert-bloom.json`.

Family palette: `#25201C` `#E0D0C0` `#26211C` `#2E2924` `#64584C` `#FF00AA` `#7A9A6A` `#6A8AAA` `#FFCC5A` `#CC7A4A` `#8AAA7A` `#CFB79E`.

- **Gremlin Dark - Desert Bloom Superbloom** — dark — variant ID `gremlin-theme-desert-bloom-extreme-electric-superboom.json`
- **Gremlin Dark - Desert Bloom Canyon** — dark — variant ID `gremlin-theme-desert-bloom-high-contrast-canyon.json`
- **Gremlin Dark - Desert Bloom Oasis** — dark — variant ID `gremlin-theme-desert-bloom-infused-medium-oasis.json`
- **Gremlin Dark - Desert Bloom Drought** — dark — variant ID `gremlin-theme-desert-bloom-subdued-drought.json`
- **Gremlin Dark - Desert Bloom Monsoon** — dark — variant ID `gremlin-theme-desert-bloom-vibrant-monsoon.json`
- **Gremlin Dark - Desert Bloom** — dark — variant ID `gremlin-theme-desert-bloom.json`

### Electric Rebellion variants

Category: **Core Mischief**. Family slug: `electric-rebellion`. Representative variant: `gremlin-theme-electric-rebellion.json`.

Family palette: `#2D2D2D` `#FFE0F0` `#2C2C2C` `#383838` `#656565` `#FF0080` `#00FF99` `#0099FF` `#FFCC00` `#FF9900` `#33FFAA` `#FFADD7`.

- **Gremlin Dark - Electric Rebellion Revolution** — dark — variant ID `gremlin-theme-electric-rebellion-electric-revolution.json`
- **Gremlin Dark - Electric Rebellion Anarchy** — dark — variant ID `gremlin-theme-electric-rebellion-extreme-contrast-anarchy.json`
- **Gremlin Dark - Electric Rebellion Uprising** — dark — variant ID `gremlin-theme-electric-rebellion-high-electric-uprising.json`
- **Gremlin Dark - Electric Rebellion Insurgent** — dark — variant ID `gremlin-theme-electric-rebellion-infused-high-insurgent.json`
- **Gremlin Dark - Electric Rebellion** — dark — variant ID `gremlin-theme-electric-rebellion.json`

### Erosion Protocol variants

Category: **Nature and Environment**. Family slug: `erosion-protocol`. Representative variant: `gremlin-theme-erosion-protocol.json`.

Family palette: `#35302E` `#C8C0B8` `#353028` `#403A37` `#716761` `#A8957A` `#8FA87A` `#7A8FA8` `#C4A5B5` `#C4C49A` `#C4A58A` `#A8B89A`.

- **Gremlin Dark - Erosion Protocol Patina** — dark — variant ID `gremlin-theme-erosion-protocol-high-subdued-patina.json`
- **Gremlin Dark - Erosion Protocol Oxidized** — dark — variant ID `gremlin-theme-erosion-protocol-infused-medium-oxidized.json`
- **Gremlin Dark - Erosion Protocol Dust** — dark — variant ID `gremlin-theme-erosion-protocol-low-contrast-dust.json`
- **Gremlin Dark - Erosion Protocol Weathered** — dark — variant ID `gremlin-theme-erosion-protocol-subdued-weathered.json`
- **Gremlin Dark - Erosion Protocol** — dark — variant ID `gremlin-theme-erosion-protocol.json`

### Gremlin Chaos variants

Category: **Core Mischief**. Family slug: `gremlin-chaos`. Representative variant: `gremlin-theme-gremlin-chaos.json`.

Family palette: `#2D2D2D` `#D1FFA2` `#2E2E2E` `#363636` `#656565` `#1FCC00` `#00FF80` `#0080FF` `#FF0080` `#FFD600` `#FF8000` `#B8FF6F`.

Related bundled palettes: Chaos.

- **Gremlin Dark - Gremlin Chaos Maximum** — dark — variant ID `gremlin-theme-gremlin-chaos-electric-maximum.json`
- **Gremlin Dark - Gremlin Chaos Void** — dark — variant ID `gremlin-theme-gremlin-chaos-extreme-contrast-void.json`
- **Gremlin Dark - Gremlin Chaos Nuclear** — dark — variant ID `gremlin-theme-gremlin-chaos-extreme-electric-nuclear.json`
- **Gremlin Dark - Gremlin Chaos Radioactive** — dark — variant ID `gremlin-theme-gremlin-chaos-infused-high-radioactive.json`
- **Gremlin Dark - Gremlin Chaos** — dark — variant ID `gremlin-theme-gremlin-chaos.json`

### Gremlin Terra variants

Category: **Nature and Environment**. Family slug: `gremlin-terra`. Representative variant: `gremlin-theme-gremlin-terra.json`.

Family palette: `#211F24` `#E0D0C8` `#222025` `#2A272D` `#595260` `#1FCC00` `#4DD732` `#6ED0E8` `#E986DD` `#FFDB62` `#FC975F` `#B1CE69`.

- **Gremlin Dark - Gremlin Terra Volcanic Soil** — dark — variant ID `gremlin-theme-gremlin-terra-extreme-electric-volcanic-soil.json`
- **Gremlin Dark - Gremlin Terra Bedrock** — dark — variant ID `gremlin-theme-gremlin-terra-high-contrast-bedrock.json`
- **Gremlin Dark - Gremlin Terra Loam** — dark — variant ID `gremlin-theme-gremlin-terra-infused-medium-loam.json`
- **Gremlin Dark - Gremlin Terra Clay** — dark — variant ID `gremlin-theme-gremlin-terra-subdued-clay.json`
- **Gremlin Dark - Gremlin Terra Fertile** — dark — variant ID `gremlin-theme-gremlin-terra-vibrant-fertile.json`
- **Gremlin Dark - Gremlin Terra** — dark — variant ID `gremlin-theme-gremlin-terra.json`

### Labcoat variants

Category: **Professional and Neutral**. Family slug: `labcoat`. Representative variant: `gremlin-theme-labcoat.json`.

Family palette: `#C4C6C2` `#1A1A1A` `#D0D2CE` `#999D95` `#0D9900` `#4A8FB8` `#B88FA8` `#B8B85A` `#B8845A` `#1FCC00` `#B85A5A` `#000000`.

- **Gremlin Light - Labcoat Sterile** — light — variant ID `gremlin-theme-labcoat-high-contrast-sterile.json`
- **Gremlin Light - Labcoat Surgical** — light — variant ID `gremlin-theme-labcoat-infused-low-surgical.json`
- **Gremlin Light - Labcoat Cleanroom** — light — variant ID `gremlin-theme-labcoat-subdued-cleanroom.json`
- **Gremlin Light - Labcoat Emergency** — light — variant ID `gremlin-theme-labcoat-vibrant-emergency.json`
- **Gremlin Light - Labcoat** — light — variant ID `gremlin-theme-labcoat.json`

### Labcoat Experimental variants

Category: **Professional and Neutral**. Family slug: `labcoat-experimental`. Representative variant: `gremlin-theme-labcoat-experimental.json`.

Family palette: `#C4C6C2` `#1A1A1A` `#D2CECC` `#C8C4C0` `#999D95` `#FF5722` `#4AFF33` `#00A3FF` `#FF0080` `#FFD600` `#00FF80` `#CC2900`.

- **Gremlin Light - Labcoat Critical Mass** — light — variant ID `gremlin-theme-labcoat-experimental-electric-critical-mass.json`
- **Gremlin Light - Labcoat HAZMAT** — light — variant ID `gremlin-theme-labcoat-experimental-extreme-contrast-hazmat.json`
- **Gremlin Light - Labcoat Meltdown** — light — variant ID `gremlin-theme-labcoat-experimental-high-vibrant-meltdown.json`
- **Gremlin Light - Labcoat Contaminated** — light — variant ID `gremlin-theme-labcoat-experimental-infused-high-contaminated.json`
- **Gremlin Light - Labcoat Control Group** — light — variant ID `gremlin-theme-labcoat-experimental-subdued-control-group.json`
- **Gremlin Light - Labcoat Experimental** — light — variant ID `gremlin-theme-labcoat-experimental.json`

### Lemonade Stand variants

Category: **Playful and Candy**. Family slug: `lemonade-stand`. Representative variant: `gremlin-theme-lemonade-stand.json`.

Family palette: `#FFF5CE` `#4A4535` `#FFFAE5` `#FFF4D5` `#FFE377` `#6ABF4A` `#5A8A4A` `#4A7A9A` `#AA6A7A` `#AA9A3A` `#AA7A3A` `#6A9A5A`.

- **Gremlin Light - Lemonade Stand Tart** — light — variant ID `gremlin-theme-lemonade-stand-high-contrast-tart.json`
- **Gremlin Light - Lemonade Stand Diluted** — light — variant ID `gremlin-theme-lemonade-stand-infused-low-diluted.json`
- **Gremlin Light - Lemonade Stand Concentrate** — light — variant ID `gremlin-theme-lemonade-stand-vibrant-concentrate.json`
- **Gremlin Light - Lemonade Stand** — light — variant ID `gremlin-theme-lemonade-stand.json`

### Lethal Yellow variants

Category: **Core Mischief**. Family slug: `lethal-yellow`. Representative variant: `gremlin-theme-lethal-yellow.json`.

Family palette: `#CBF000` `#1A1A1A` `#E0FF20` `#D0F500` `#829900` `#FF5722` `#009900` `#0066CC` `#FF0066` `#FFCC00` `#FF6600` `#00CC00`.

- **Gremlin Light - Lethal Yellow Nuclear** — light — variant ID `gremlin-theme-lethal-yellow-electric-nuclear.json`
- **Gremlin Light - Lethal Yellow Biohazard** — light — variant ID `gremlin-theme-lethal-yellow-extreme-contrast-biohazard.json`
- **Gremlin Light - Lethal Yellow Contaminated** — light — variant ID `gremlin-theme-lethal-yellow-infused-high-contaminated.json`
- **Gremlin Light - Lethal Yellow Caution** — light — variant ID `gremlin-theme-lethal-yellow-subdued-caution.json`
- **Gremlin Light - Lethal Yellow** — light — variant ID `gremlin-theme-lethal-yellow.json`

### Lethal Yellow Reversed variants

Category: **Core Mischief**. Family slug: `lethal-yellow-reversed`. Representative variant: `gremlin-theme-lethal-yellow-reversed.json`.

Family palette: `#CBF000` `#000000` `#E0FF20` `#D0F500` `#829900` `#8000FF` `#FF0080` `#00A3FF` `#00FF80` `#FF00AA` `#00FF00` `#FF00FF`.

- **Gremlin Light - Lethal Yellow Acid Trip** — light — variant ID `gremlin-theme-lethal-yellow-reversed-electric-acid-trip.json`
- **Gremlin Light - Lethal Yellow Mind Melt** — light — variant ID `gremlin-theme-lethal-yellow-reversed-extreme-contrast-mind-melt.json`
- **Gremlin Light - Lethal Yellow Dimension Shift** — light — variant ID `gremlin-theme-lethal-yellow-reversed-high-electric-dimension-shift.json`
- **Gremlin Light - Lethal Yellow Kaleidoscope** — light — variant ID `gremlin-theme-lethal-yellow-reversed-infused-high-kaleidoscope.json`
- **Gremlin Light - Lethal Yellow Reversed** — light — variant ID `gremlin-theme-lethal-yellow-reversed.json`

### Midnight Mischief variants

Category: **Core Mischief**. Family slug: `midnight-mischief`. Representative variant: `gremlin-theme-midnight-mischief.json`.

Family palette: `#1C1C1C` `#E8E0FF` `#1D1D1D` `#252525` `#545454` `#B366FF` `#5AD87F` `#5A8FD8` `#D85A8F` `#D8C85A` `#D8845A` `#7AD89F`.

- **Gremlin Dark - Midnight Mischief Neon Night** — dark — variant ID `gremlin-theme-midnight-mischief-electric-neon-night.json`
- **Gremlin Dark - Midnight Mischief Nocturnal** — dark — variant ID `gremlin-theme-midnight-mischief-extreme-vibrant-nocturnal.json`
- **Gremlin Dark - Midnight Mischief Witching Hour** — dark — variant ID `gremlin-theme-midnight-mischief-high-contrast-witching-hour.json`
- **Gremlin Dark - Midnight Mischief Purple Haze** — dark — variant ID `gremlin-theme-midnight-mischief-infused-medium-purple-haze.json`
- **Gremlin Dark - Midnight Mischief Twilight** — dark — variant ID `gremlin-theme-midnight-mischief-subdued-twilight.json`
- **Gremlin Dark - Midnight Mischief** — dark — variant ID `gremlin-theme-midnight-mischief.json`

### Mischief Stone variants

Category: **Nature and Environment**. Family slug: `mischief-stone`. Representative variant: `gremlin-theme-mischief-stone.json`.

Family palette: `#26292E` `#E0E0E0` `#26292F` `#2E3137` `#585E6B` `#8000FF` `#A9DC76` `#78DCE8` `#E991E3` `#FFD866` `#FC9867` `#B7D175`.

- **Gremlin Dark - Mischief Stone Obsidian** — dark — variant ID `gremlin-theme-mischief-stone-extreme-electric-obsidian.json`
- **Gremlin Dark - Mischief Stone Granite** — dark — variant ID `gremlin-theme-mischief-stone-high-contrast-granite.json`
- **Gremlin Dark - Mischief Stone Enchanted** — dark — variant ID `gremlin-theme-mischief-stone-infused-medium-enchanted.json`
- **Gremlin Dark - Mischief Stone Limestone** — dark — variant ID `gremlin-theme-mischief-stone-subdued-limestone.json`
- **Gremlin Dark - Mischief Stone Crystal** — dark — variant ID `gremlin-theme-mischief-stone-vibrant-crystal.json`
- **Gremlin Dark - Mischief Stone** — dark — variant ID `gremlin-theme-mischief-stone.json`

### Neon Arcade variants

Category: **Retro Computing and Gaming**. Family slug: `neon-arcade`. Representative variant: `gremlin-theme-neon-arcade.json`.

Family palette: `#050505` `#00FFFF` `#060606` `#0E0E0E` `#3D3D3D` `#FF00FF` `#00FF00` `#FFFF00` `#FF6600` `#39FF14` `#00CCCC` `#FF0066`.

- **Gremlin Dark - Neon Arcade Laser Tag** — dark — variant ID `gremlin-theme-neon-arcade-electric-laser-tag.json`
- **Gremlin Dark - Neon Arcade High Score** — dark — variant ID `gremlin-theme-neon-arcade-extreme-contrast-high-score.json`
- **Gremlin Dark - Neon Arcade Prize Zone** — dark — variant ID `gremlin-theme-neon-arcade-high-vibrant-prize-zone.json`
- **Gremlin Dark - Neon Arcade Black Light** — light — variant ID `gremlin-theme-neon-arcade-infused-high-black-light.json`
- **Gremlin Dark - Neon Arcade** — dark — variant ID `gremlin-theme-neon-arcade.json`

### Nightmare Purple variants

Category: **Cosmic and Mystical**. Family slug: `nightmare-purple`. Representative variant: `gremlin-theme-nightmare-purple.json`.

Family palette: `#180030` `#FFD0F0` `#190033` `#200042` `#51009F` `#FF0080` `#8F4FD8` `#6A4FD8` `#D8AF4F` `#D84F8F` `#AF6FD8` `#FF9DE0`.

Related bundled palettes: Nightmare Purple.

- **Gremlin Dark - Nightmare Purple Void** — dark — variant ID `gremlin-theme-nightmare-purple-extreme-contrast-void.json`
- **Gremlin Dark - Nightmare Purple Lucid** — dark — variant ID `gremlin-theme-nightmare-purple-high-vibrant-lucid.json`
- **Gremlin Dark - Nightmare Purple Hallucination** — dark — variant ID `gremlin-theme-nightmare-purple-infused-high-hallucination.json`
- **Gremlin Dark - Nightmare Purple** — dark — variant ID `gremlin-theme-nightmare-purple.json`

### Nightmare Purple Electric variants

Category: **Cosmic and Mystical**. Family slug: `nightmare-purple-electric`. Representative variant: `gremlin-theme-nightmare-purple-electric.json`.

Family palette: `#180030` `#C0F0FF` `#190035` `#210043` `#51009F` `#00A3FF` `#00FF80` `#FF0080` `#FFD600` `#FF8800` `#4AFF33` `#8DE4FF`.

- **Gremlin Dark - Nightmare Purple Neon** — dark — variant ID `gremlin-theme-nightmare-purple-electric-electric-neon.json`
- **Gremlin Dark - Nightmare Purple Matrix** — dark — variant ID `gremlin-theme-nightmare-purple-electric-extreme-contrast-matrix.json`
- **Gremlin Dark - Nightmare Purple Fever** — dark — variant ID `gremlin-theme-nightmare-purple-electric-fever.json`
- **Gremlin Dark - Nightmare Purple Cyberpunk** — dark — variant ID `gremlin-theme-nightmare-purple-electric-high-electric-cyberpunk.json`
- **Gremlin Dark - Nightmare Purple Hologram** — dark — variant ID `gremlin-theme-nightmare-purple-electric-infused-high-hologram.json`
- **Gremlin Dark - Nightmare Purple Electric** — dark — variant ID `gremlin-theme-nightmare-purple-electric.json`

### Obsidian Chaos variants

Category: **Core Mischief**. Family slug: `obsidian-chaos`. Representative variant: `gremlin-theme-obsidian-chaos.json`.

Family palette: `#0D0D0D` `#F0E8D0` `#0E0E0E` `#161616` `#454545` `#FFD600` `#4DD732` `#6ED0E8` `#E986DD` `#FFDB62` `#FC975F` `#B1CE69`.

Related bundled palettes: Obsidian Chaos.

- **Gremlin Dark - Obsidian Chaos Eruption** — dark — variant ID `gremlin-theme-obsidian-chaos-electric-eruption.json`
- **Gremlin Dark - Obsidian Chaos Magma** — dark — variant ID `gremlin-theme-obsidian-chaos-extreme-contrast-magma.json`
- **Gremlin Dark - Obsidian Chaos Volcanic** — dark — variant ID `gremlin-theme-obsidian-chaos-high-vibrant-volcanic.json`
- **Gremlin Dark - Obsidian Chaos Lava Flow** — dark — variant ID `gremlin-theme-obsidian-chaos-infused-high-lava-flow.json`
- **Gremlin Dark - Obsidian Chaos** — dark — variant ID `gremlin-theme-obsidian-chaos.json`

### Powder Room variants

Category: **Luxury and Expressive**. Family slug: `powder-room`. Representative variant: `gremlin-theme-powder-room.json`.

Family palette: `#FFF1E1` `#3A3A4A` `#FFFCF8` `#FFF0E8` `#FFC88A` `#FFA8C8` `#A8D8A8` `#8FB8D8` `#FFE8B8` `#FFB8A8` `#B8E8B8` `#FF9898`.

- **Gremlin Light - Powder Room Vanity Mirror** — light — variant ID `gremlin-theme-powder-room-high-contrast-vanity-mirror.json`
- **Gremlin Light - Powder Room Perfumed** — light — variant ID `gremlin-theme-powder-room-infused-low-perfumed.json`
- **Gremlin Light - Powder Room Soft Focus** — light — variant ID `gremlin-theme-powder-room-subdued-soft-focus.json`
- **Gremlin Light - Powder Room Hollywood** — light — variant ID `gremlin-theme-powder-room-vibrant-hollywood.json`
- **Gremlin Light - Powder Room** — light — variant ID `gremlin-theme-powder-room.json`

### Pure Void variants

Category: **Zen and Restorative**. Family slug: `pure-void`. Representative variant: `gremlin-theme-pure-void.json`.

Family palette: `#0F0F0F` `#606060` `#101010` `#181818` `#474747` `#454545` `#485848` `#404858` `#584048` `#585848` `#584840` `#505850`.

- **Gremlin Dark - Pure Void Ghost** — dark — variant ID `gremlin-theme-pure-void-infused-low-ghost.json`
- **Gremlin Dark - Pure Void Phantom** — dark — variant ID `gremlin-theme-pure-void-low-contrast-phantom.json`
- **Gremlin Dark - Pure Void Whisper** — dark — variant ID `gremlin-theme-pure-void-subdued-whisper.json`
- **Gremlin Dark - Pure Void** — dark — variant ID `gremlin-theme-pure-void.json`

### Rose Gold Empress variants

Category: **Luxury and Expressive**. Family slug: `rose-gold-empress`. Representative variant: `gremlin-theme-rose-gold-empress.json`.

Family palette: `#251C23` `#FFE8F0` `#26201C` `#2E242C` `#644C5F` `#FFB8D8` `#A8D8B8` `#B8A8D8` `#FFD8A8` `#FFB8A8` `#B8E8C8` `#FFB5CF`.

- **Gremlin Dark - Rose Gold Empress Throne** — dark — variant ID `gremlin-theme-rose-gold-empress-high-contrast-throne.json`
- **Gremlin Dark - Rose Gold Empress Jeweled** — dark — variant ID `gremlin-theme-rose-gold-empress-infused-medium-jeweled.json`
- **Gremlin Dark - Rose Gold Empress Silk** — dark — variant ID `gremlin-theme-rose-gold-empress-subdued-silk.json`
- **Gremlin Dark - Rose Gold Empress Crown** — dark — variant ID `gremlin-theme-rose-gold-empress-vibrant-crown.json`
- **Gremlin Dark - Rose Gold Empress** — dark — variant ID `gremlin-theme-rose-gold-empress.json`

### Sergeant Mischief variants

Category: **Professional and Neutral**. Family slug: `sergeant-mischief`. Representative variant: `gremlin-theme-sergeant-mischief.json`.

Family palette: `#353A2B` `#D8D0C0` `#353A2A` `#404435` `#70795B` `#FFD700` `#7A8F5A` `#5A7A8F` `#A87A8F` `#C4B85A` `#A8845A` `#8FA874`.

- **Gremlin Dark - Sergeant Mischief Bronze** — dark — variant ID `gremlin-theme-sergeant-mischief-alt-accent-bronze.json`
- **Gremlin Dark - Sergeant Mischief Combat** — dark — variant ID `gremlin-theme-sergeant-mischief-extreme-vibrant-combat.json`
- **Gremlin Dark - Sergeant Mischief Tactical** — dark — variant ID `gremlin-theme-sergeant-mischief-high-contrast-tactical.json`
- **Gremlin Dark - Sergeant Mischief Night Vision** — dark — variant ID `gremlin-theme-sergeant-mischief-nightvision.json`
- **Gremlin Dark - Sergeant Mischief Stealth** — dark — variant ID `gremlin-theme-sergeant-mischief-subdued-stealth.json`
- **Gremlin Dark - Sergeant Mischief** — dark — variant ID `gremlin-theme-sergeant-mischief.json`

### Shadow Realm variants

Category: **Core Mischief**. Family slug: `shadow-realm`. Representative variant: `gremlin-theme-shadow-realm.json`.

Family palette: `#2D2D2D` `#E0E0E0` `#2E2E2E` `#363636` `#656565` `#1FCC00` `#4DD732` `#6ED0E8` `#E986DD` `#FFDB62` `#FC975F` `#B1CE69`.

- **Gremlin Dark - Shadow Realm Void Walker** — dark — variant ID `gremlin-theme-shadow-realm-extreme-electric-void-walker.json`
- **Gremlin Dark - Shadow Realm Umbra** — dark — variant ID `gremlin-theme-shadow-realm-high-contrast-umbra.json`
- **Gremlin Dark - Shadow Realm Twilight** — dark — variant ID `gremlin-theme-shadow-realm-infused-medium-twilight.json`
- **Gremlin Dark - Shadow Realm Penumbra** — dark — variant ID `gremlin-theme-shadow-realm-subdued-penumbra.json`
- **Gremlin Dark - Shadow Realm Eclipse** — dark — variant ID `gremlin-theme-shadow-realm-vibrant-eclipse.json`
- **Gremlin Dark - Shadow Realm** — dark — variant ID `gremlin-theme-shadow-realm.json`

### Silk Kimono variants

Category: **Luxury and Expressive**. Family slug: `silk-kimono`. Representative variant: `gremlin-theme-silk-kimono.json`.

Family palette: `#FFEEE6` `#4A3A3A` `#FFFCFA` `#FFF0EC` `#FFB18F` `#FFB8CC` `#7FB87F` `#6B9BD8` `#FFD89C` `#FFB88C` `#8FC88F` `#FF8888`.

- **Gremlin Light - Silk Kimono Calligraphy** — light — variant ID `gremlin-theme-silk-kimono-high-contrast-calligraphy.json`
- **Gremlin Light - Silk Kimono Morning Mist** — light — variant ID `gremlin-theme-silk-kimono-infused-low-morning-mist.json`
- **Gremlin Light - Silk Kimono Tea Ceremony** — light — variant ID `gremlin-theme-silk-kimono-subdued-tea-ceremony.json`
- **Gremlin Light - Silk Kimono Festival** — light — variant ID `gremlin-theme-silk-kimono-vibrant-festival.json`
- **Gremlin Light - Silk Kimono** — light — variant ID `gremlin-theme-silk-kimono.json`

### Spilled Latte variants

Category: **Warm Culinary and Material**. Family slug: `spilled-latte`. Representative variant: `gremlin-theme-spilled-latte.json`.

Family palette: `#F1E5DA` `#3A2F2A` `#F8F0E8` `#F0E8E0` `#D9BA9B` `#8F5A2A` `#7A8F6A` `#6A7A8F` `#BA7A8A` `#CAB85A` `#BA8A5A` `#8FA87A`.

- **Gremlin Light - Spilled Latte Blonde** — light — variant ID `gremlin-theme-spilled-latte-alt-accent-blonde.json`
- **Gremlin Light - Spilled Latte Ristretto** — light — variant ID `gremlin-theme-spilled-latte-high-contrast-ristretto.json`
- **Gremlin Light - Spilled Latte Macchiato** — light — variant ID `gremlin-theme-spilled-latte-infused-medium-macchiato.json`
- **Gremlin Light - Spilled Latte Espresso** — light — variant ID `gremlin-theme-spilled-latte-vibrant-espresso.json`
- **Gremlin Light - Spilled Latte** — light — variant ID `gremlin-theme-spilled-latte.json`

### Subway Tile variants

Category: **Nature and Environment**. Family slug: `subway-tile`. Representative variant: `gremlin-theme-subway-tile.json`.

Family palette: `#F2F2F2` `#1A1A1A` `#FCFCFC` `#F5F5F5` `#C7C7C7` `#5A9A7A` `#4A7A8A` `#CC8A9A` `#CCAA5A` `#CC7A5A` `#6AAA8A` `#AA5A5A`.

- **Gremlin Light - Subway Tile Exposed Brick** — light — variant ID `gremlin-theme-subway-tile-high-contrast-exposed-brick.json`
- **Gremlin Light - Subway Tile Patina** — light — variant ID `gremlin-theme-subway-tile-infused-low-patina.json`
- **Gremlin Light - Subway Tile Vintage** — light — variant ID `gremlin-theme-subway-tile-medium-subdued-vintage.json`
- **Gremlin Light - Subway Tile Flat White** — light — variant ID `gremlin-theme-subway-tile-subdued-flat-white.json`
- **Gremlin Light - Subway Tile Neon Sign** — light — variant ID `gremlin-theme-subway-tile-vibrant-neon-sign.json`
- **Gremlin Light - Subway Tile** — light — variant ID `gremlin-theme-subway-tile.json`

### Terminal Green variants

Category: **Retro Computing and Gaming**. Family slug: `terminal-green`. Representative variant: `gremlin-theme-terminal-green.json`.

Family palette: `#000000` `#00FF00` `#000800` `#001100` `#333333` `#00CC00` `#999999` `#B3B3B3` `#0AC20A` `#404040`.

Related bundled palettes: Terminal.

- **Gremlin Dark - Terminal Green Matrix** — dark — variant ID `gremlin-theme-terminal-green-electric-matrix.json`
- **Gremlin Dark - Terminal Green Mainframe** — dark — variant ID `gremlin-theme-terminal-green-extreme-contrast-mainframe.json`
- **Gremlin Dark - Terminal Green Phosphor Burn** — dark — variant ID `gremlin-theme-terminal-green-infused-high-phosphor-burn.json`
- **Gremlin Dark - Terminal Green Amber** — dark — variant ID `gremlin-theme-terminal-green-subdued-amber.json`
- **Gremlin Dark - Terminal Green** — dark — variant ID `gremlin-theme-terminal-green.json`

### Tidal Pool variants

Category: **Nature and Environment**. Family slug: `tidal-pool`. Representative variant: `gremlin-theme-tidal-pool.json`.

Family palette: `#EBF5F5` `#2A3A3A` `#F8FCFC` `#F0F5F5` `#B1D8D8` `#5ACCCC` `#5AAA7A` `#4A8ACC` `#FFAACC` `#FFCC8A` `#FF8A5A` `#6ACC8A`.

- **Gremlin Light - Tidal Pool Reef** — light — variant ID `gremlin-theme-tidal-pool-high-contrast-reef.json`
- **Gremlin Light - Tidal Pool Sea Spray** — light — variant ID `gremlin-theme-tidal-pool-infused-medium-sea-spray.json`
- **Gremlin Light - Tidal Pool Lagoon** — light — variant ID `gremlin-theme-tidal-pool-medium-vibrant-lagoon.json`
- **Gremlin Light - Tidal Pool Low Tide** — light — variant ID `gremlin-theme-tidal-pool-subdued-low-tide.json`
- **Gremlin Light - Tidal Pool High Tide** — light — variant ID `gremlin-theme-tidal-pool-vibrant-high-tide.json`
- **Gremlin Light - Tidal Pool** — light — variant ID `gremlin-theme-tidal-pool.json`

### Transcendence Purple variants

Category: **Zen and Restorative**. Family slug: `transcendence-purple`. Representative variant: `gremlin-theme-transcendence-purple.json`.

Family palette: `#26292E` `#E0D8F0` `#262930` `#2E3037` `#585E6B` `#B366FF` `#66FF66` `#6666FF` `#FF66CC` `#FFCC66` `#FF8866` `#88FF88`.

- **Gremlin Dark - Transcendence Purple Enlightenment** — dark — variant ID `gremlin-theme-transcendence-purple-electric-enlightenment.json`
- **Gremlin Dark - Transcendence Purple Clarity** — dark — variant ID `gremlin-theme-transcendence-purple-high-contrast-clarity.json`
- **Gremlin Dark - Transcendence Purple Aura** — dark — variant ID `gremlin-theme-transcendence-purple-infused-medium-aura.json`
- **Gremlin Dark - Transcendence Purple Zen** — dark — variant ID `gremlin-theme-transcendence-purple-low-subdued-zen.json`
- **Gremlin Dark - Transcendence Purple Meditation** — dark — variant ID `gremlin-theme-transcendence-purple-subdued-meditation.json`
- **Gremlin Dark - Transcendence Purple** — dark — variant ID `gremlin-theme-transcendence-purple.json`

### Velvet Underground variants

Category: **Luxury and Expressive**. Family slug: `velvet-underground`. Representative variant: `gremlin-theme-velvet-underground.json`.

Family palette: `#140C14` `#E8D0E0` `#160C18` `#1E1220` `#5B345B` `#D8B86B` `#6BD86B` `#6B6BD8` `#D86B95` `#D8956B` `#8BD88B` `#D7AEC9`.

- **Gremlin Dark - Velvet Underground Opium** — dark — variant ID `gremlin-theme-velvet-underground-electric-opium.json`
- **Gremlin Dark - Velvet Underground Midnight** — dark — variant ID `gremlin-theme-velvet-underground-extreme-contrast-midnight.json`
- **Gremlin Dark - Velvet Underground Burgundy Wine** — dark — variant ID `gremlin-theme-velvet-underground-infused-high-burgundy-wine.json`
- **Gremlin Dark - Velvet Underground Smoke** — dark — variant ID `gremlin-theme-velvet-underground-subdued-smoke.json`
- **Gremlin Dark - Velvet Underground** — dark — variant ID `gremlin-theme-velvet-underground.json`

### VHS Rewind variants

Category: **Retro Computing and Gaming**. Family slug: `vhs-rewind`. Representative variant: `gremlin-theme-vhs-rewind-base.json`.

Family palette: `#07050B` `#E0F0FF` `#080610` `#0C0A14` `#312759` `#FF00AA` `#00FF88` `#00E5FF` `#FFFF00` `#FF8800` `#44FF00` `#ADD7FF`.

Related bundled palettes: VHS.

- **Gremlin Dark - VHS Rewind - Cyan Accent** — dark — variant ID `gremlin-theme-vhs-rewind-alt-accent-cyan.json`
- **Gremlin Dark - VHS Rewind** — dark — variant ID `gremlin-theme-vhs-rewind-base.json`
- **Gremlin Dark - VHS Rewind - Full Saturation** — dark — variant ID `gremlin-theme-vhs-rewind-electric-full-saturation.json`
- **Gremlin Dark - VHS Rewind - OLED CRT** — dark — variant ID `gremlin-theme-vhs-rewind-extreme-vibrant-oled-crt.json`
- **Gremlin Dark - VHS Rewind - Tracking Error** — dark — variant ID `gremlin-theme-vhs-rewind-high-contrast-tracking-error.json`
- **Gremlin Dark - VHS Rewind - Chroma Bleed** — dark — variant ID `gremlin-theme-vhs-rewind-infused-high-chroma-bleed.json`
- **Gremlin Dark - VHS Rewind - Pause Mode** — dark — variant ID `gremlin-theme-vhs-rewind-low-subdued-pause-mode.json`
- **Gremlin Dark - VHS Rewind - Degraded Tape** — dark — variant ID `gremlin-theme-vhs-rewind-subdued-degraded.json`

### Vibe Black variants

Category: **Zen and Restorative**. Family slug: `vibe-black`. Representative variant: `gremlin-theme-vibe-black.json`.

Family palette: `#0F0F0F` `#C8C8C8` `#101010` `#181818` `#474747` `#00A3FF` `#A9DC76` `#78DCE8` `#E991E3` `#FFD866` `#FC9867` `#B7D175`.

- **Gremlin Dark - Vibe Black Absolute** — dark — variant ID `gremlin-theme-vibe-black-extreme-contrast-absolute.json`
- **Gremlin Dark - Vibe Black Eclipse** — dark — variant ID `gremlin-theme-vibe-black-high-vibrant-eclipse.json`
- **Gremlin Dark - Vibe Black Shadow** — dark — variant ID `gremlin-theme-vibe-black-infused-low-shadow.json`
- **Gremlin Dark - Vibe Black Stealth** — dark — variant ID `gremlin-theme-vibe-black-subdued-stealth.json`
- **Gremlin Dark - Vibe Black** — dark — variant ID `gremlin-theme-vibe-black.json`

### Vibe Creamsicle Light variants

Category: **Playful and Candy**. Family slug: `vibe-creamsicle-light`. Representative variant: `gremlin-theme-vibe-creamsicle-light.json`.

Family palette: `#FFE6CE` `#4A3020` `#FFF2E5` `#FFEAD5` `#FFBB77` `#FF8844` `#B8D6A8` `#A8C4D6` `#FFA8B8` `#FFE09C` `#FFB88C` `#C4E0B4`.

Related bundled palettes: Vibe Creamsicle Light.

- **Gremlin Light - Vibe Creamsicle Popsicle** — light — variant ID `gremlin-theme-vibe-creamsicle-light-high-contrast-popsicle.json`
- **Gremlin Light - Vibe Creamsicle Swirl** — light — variant ID `gremlin-theme-vibe-creamsicle-light-infused-medium-swirl.json`
- **Gremlin Light - Vibe Creamsicle Sherbet** — light — variant ID `gremlin-theme-vibe-creamsicle-light-medium-subdued-sherbet.json`
- **Gremlin Light - Vibe Creamsicle Melted** — light — variant ID `gremlin-theme-vibe-creamsicle-light-subdued-melted.json`
- **Gremlin Light - Vibe Creamsicle Citrus** — light — variant ID `gremlin-theme-vibe-creamsicle-light-vibrant-citrus.json`
- **Gremlin Light - Vibe Creamsicle** — light — variant ID `gremlin-theme-vibe-creamsicle-light.json`

### Vibe Lavender Dark variants

Category: **Zen and Restorative**. Family slug: `vibe-lavender-dark`. Representative variant: `gremlin-theme-vibe-lavender-dark.json`.

Family palette: `#282130` `#E0D0F0` `#292032` `#312840` `#604D73` `#C8A8E8` `#A8C09A` `#9BB5D6` `#D4A5C8` `#E6D5A8` `#E6B89C` `#B8CFB8`.

Related bundled palettes: Vibe Lavender Dark.

- **Gremlin Dark - Vibe Lavender Lucid** — dark — variant ID `gremlin-theme-vibe-lavender-dark-high-vibrant-lucid.json`
- **Gremlin Dark - Vibe Lavender Dreamy** — dark — variant ID `gremlin-theme-vibe-lavender-dark-infused-medium-dreamy.json`
- **Gremlin Dark - Vibe Lavender Twilight** — dark — variant ID `gremlin-theme-vibe-lavender-dark-low-contrast-twilight.json`
- **Gremlin Dark - Vibe Lavender Moonlit** — dark — variant ID `gremlin-theme-vibe-lavender-dark-subdued-moonlit.json`
- **Gremlin Dark - Vibe Lavender** — dark — variant ID `gremlin-theme-vibe-lavender-dark.json`

### Vibe Lavender Light variants

Category: **Zen and Restorative**. Family slug: `vibe-lavender-light`. Representative variant: `gremlin-theme-vibe-lavender-light.json`.

Family palette: `#EFE7F0` `#4A3A5A` `#F8F3F9` `#F0EBF2` `#CBB0D0` `#9B7CC0` `#A8C09A` `#9BB5D6` `#D4A5C8` `#E6D5A8` `#E6B89C` `#B8CFB8`.

Related bundled palettes: Vibe Lavender Light.

- **Gremlin Light - Vibe Lavender Clarity** — light — variant ID `gremlin-theme-vibe-lavender-light-high-contrast-clarity.json`
- **Gremlin Light - Vibe Lavender Aromatherapy** — light — variant ID `gremlin-theme-vibe-lavender-light-infused-low-aromatherapy.json`
- **Gremlin Light - Vibe Lavender Zen** — light — variant ID `gremlin-theme-vibe-lavender-light-medium-subdued-zen.json`
- **Gremlin Light - Vibe Lavender Meditation** — light — variant ID `gremlin-theme-vibe-lavender-light-subdued-meditation.json`
- **Gremlin Light - Vibe Lavender Bloom** — light — variant ID `gremlin-theme-vibe-lavender-light-vibrant-bloom.json`
- **Gremlin Light - Vibe Lavender** — light — variant ID `gremlin-theme-vibe-lavender-light.json`

### Vibe Marshmallow Dark variants

Category: **Playful and Candy**. Family slug: `vibe-marshmallow-dark`. Representative variant: `gremlin-theme-vibe-marshmallow-dark.json`.

Family palette: `#25201C` `#FFE8D0` `#26201C` `#2E2824` `#64564C` `#FFB8E1` `#C7E3C7` `#B8D4E3` `#FFB8D1` `#FFF4B8` `#FFD4B8` `#D4E8D4`.

Related bundled palettes: Vibe Marshmallow Dark.

- **Gremlin Dark - Vibe Marshmallow Candy Land** — dark — variant ID `gremlin-theme-vibe-marshmallow-dark-electric-candy-land.json`
- **Gremlin Dark - Vibe Marshmallow S'mores** — dark — variant ID `gremlin-theme-vibe-marshmallow-dark-infused-high-s-mores.json`
- **Gremlin Dark - Vibe Marshmallow Midnight Snack** — dark — variant ID `gremlin-theme-vibe-marshmallow-dark-medium-vibrant-midnight-snack.json`
- **Gremlin Dark - Vibe Marshmallow Cocoa** — dark — variant ID `gremlin-theme-vibe-marshmallow-dark-subdued-cocoa.json`
- **Gremlin Dark - Vibe Marshmallow** — dark — variant ID `gremlin-theme-vibe-marshmallow-dark.json`

### Vibe Marshmallow Light variants

Category: **Playful and Candy**. Family slug: `vibe-marshmallow-light`. Representative variant: `gremlin-theme-vibe-marshmallow-light.json`.

Family palette: `#FFF1E1` `#410B26` `#FFFCF8` `#FFF4E8` `#FFC88A` `#FF99CC` `#C7E3C7` `#B8D4E3` `#FFB8D1` `#FFF4B8` `#FFD4B8` `#D4E8D4`.

Related bundled palettes: Vibe Marshmallow Light, Marshmallow Cereal.

- **Gremlin Light - Vibe Marshmallow Cartoon** — light — variant ID `gremlin-theme-vibe-marshmallow-light-high-contrast-cartoon.json`
- **Gremlin Light - Vibe Marshmallow Cereal Bowl** — light — variant ID `gremlin-theme-vibe-marshmallow-light-infused-medium-cereal-bowl.json`
- **Gremlin Light - Vibe Marshmallow Skim Milk** — light — variant ID `gremlin-theme-vibe-marshmallow-light-subdued-skim-milk.json`
- **Gremlin Light - Vibe Marshmallow Sugar Rush** — light — variant ID `gremlin-theme-vibe-marshmallow-light-vibrant-sugar-rush.json`
- **Gremlin Light - Vibe Marshmallow** — light — variant ID `gremlin-theme-vibe-marshmallow-light.json`

### Vibe Moonlight Dark variants

Category: **Cosmic and Mystical**. Family slug: `vibe-moonlight-dark`. Representative variant: `gremlin-theme-vibe-moonlight-dark.json`.

Family palette: `#0D1322` `#E0E8FF` `#0C1426` `#121A2C` `#2A4174` `#6EDEE8` `#4EE89E` `#5E9EFF` `#FF6E9E` `#FFE86E` `#FF9E5E` `#6EF8BE`.

Related bundled palettes: Vibe Moonlight.

- **Gremlin Dark - Vibe Moonlight Supernova** — dark — variant ID `gremlin-theme-vibe-moonlight-dark-electric-supernova.json`
- **Gremlin Dark - Vibe Moonlight Void** — dark — variant ID `gremlin-theme-vibe-moonlight-dark-extreme-contrast-void.json`
- **Gremlin Dark - Vibe Moonlight Cosmos** — dark — variant ID `gremlin-theme-vibe-moonlight-dark-high-vibrant-cosmos.json`
- **Gremlin Dark - Vibe Moonlight Nebula** — dark — variant ID `gremlin-theme-vibe-moonlight-dark-infused-medium-nebula.json`
- **Gremlin Dark - Vibe Moonlight Aurora** — dark — variant ID `gremlin-theme-vibe-moonlight-dark-vibrant-aurora.json`
- **Gremlin Dark - Vibe Moonlight** — dark — variant ID `gremlin-theme-vibe-moonlight-dark.json`

### Void Protocol variants

Category: **Core Mischief**. Family slug: `void-protocol`. Representative variant: `gremlin-theme-void-protocol.json`.

Family palette: `#000000` `#F0F0F0` `#030303` `#050505` `#333333` `#00FF80` `#0080FF` `#FF0080` `#FFD600` `#FF8000` `#33FF99` `#D6D6D6`.

Related bundled palettes: Default (Void).

- **Gremlin Dark - Void Protocol Radiation** — dark — variant ID `gremlin-theme-void-protocol-electric-radiation.json`
- **Gremlin Dark - Void Protocol Singularity** — dark — variant ID `gremlin-theme-void-protocol-extreme-contrast-singularity.json`
- **Gremlin Dark - Void Protocol Event Horizon** — dark — variant ID `gremlin-theme-void-protocol-extreme-electric-event-horizon.json`
- **Gremlin Dark - Void Protocol Contamination** — dark — variant ID `gremlin-theme-void-protocol-infused-high-contamination.json`
- **Gremlin Dark - Void Protocol** — dark — variant ID `gremlin-theme-void-protocol.json`

## Provenance

All origins below are descriptive records already incorporated into this bundled set. They are not runtime dependencies.

- **Generated VS Code themes** (generated) — Bundled Gremlin generated editor-theme corpus
- **Gremlin variation declarations** (source) — Bundled Gremlin variation-family declarations
- **VS Code theme contribution metadata** (manifest) — Bundled editor-theme labels and mode metadata
- **GremlinLabs Theme Color Palettes** (corporate) — Bundled GremlinLabs brand and Vibe palette corpus
- **CodeRank Theme Specifications** (product) — Bundled CodeRank product palette corpus
- **CodeRank New Theme Specifications** (product) — Bundled CodeRank experimental theme corpus

## Maintenance

1. Edit `assets/theme-family-catalog.json` inside this skill.
2. Preserve exact named roles, modes, category, character, and related-family metadata.
3. Run `python3 scripts/build_palette_master.py` from the Theme Library skill root.
4. Run `python3 scripts/build_palette_master.py --check` and the Gremlin Skills repository validators.
5. Synchronize the repository and installed skill copies.

Catalog integrity digest: `sha256:52f2f469a03dddcece1124c076ed0ddd7acc72d248751f37bc7fdfd81d16d108`.
