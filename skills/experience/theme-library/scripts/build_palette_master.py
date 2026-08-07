#!/usr/bin/env python3
"""Generate and validate Theme Library's self-contained palette master."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = SKILL_ROOT / "assets" / "theme-family-catalog.json"
MASTER_PATH = SKILL_ROOT / "PALETTE-MASTER.md"
LOCAL_REFERENCE = re.compile(
    r"/(?:Users|home)/|" + "file:" + r"//|" + r"[A-Za-z]:\\" + "Users" + r"\\",
    re.IGNORECASE,
)


def role_rows(roles: dict[str, dict[str, str]]) -> list[str]:
    rows = ["| Role | Meaning | Dark | Light |", "|---|---|---|---|"]
    for role, values in roles.items():
        dark = f"`{values['dark']}`" if values.get("dark") else "—"
        light = f"`{values['light']}`" if values.get("light") else "—"
        rows.append(
            f"| `{role}` | {values.get('label', role)} | "
            f"{dark} | {light} |"
        )
    return rows


def build(catalog: dict) -> str:
    lines = [
        "# Gremlin Palette Master",
        "",
        "> Canonical, self-contained palette set bundled with the Theme Library skill. No external repository or local file is required.",
        "",
        "## Contents",
        "",
        "- [Ownership and use](#ownership-and-use)",
        "- [Catalog coverage](#catalog-coverage)",
        "- [Foundation palettes](#foundation-palettes)",
        "- [Product palettes](#product-palettes)",
        "- [Experimental reference families](#experimental-reference-families)",
        "- [Generated family index](#generated-family-index)",
        "- [Complete variant catalog](#complete-variant-catalog)",
        "- [Provenance](#provenance)",
        "- [Maintenance](#maintenance)",
        "",
        "## Ownership and use",
        "",
        "This document and `assets/theme-family-catalog.json` form the canonical published palette set for Theme Library and every skill that consults it. The JSON owns exact structured values; this document is its deterministic human-readable rendering. Treat palette values as foundations for exploration, not component styling instructions.",
        "",
        "Always map a selected family through primitive ramps, semantic roles, component recipes, and accessibility/state tests. Ordinary components must never branch on palette or theme names and must never consume raw master values directly.",
        "",
        "## Catalog coverage",
        "",
        f"- Generated families: **{catalog['generatedFamilyCount']}**",
        f"- Concrete variants: **{catalog['generatedThemeCount']}**",
        f"- Foundation palettes: **{len(catalog['foundationPalettes'])}**",
        f"- Product palettes: **{len(catalog['productPalettes'])}**",
        f"- Experimental references: **{len(catalog['referenceFamilies'])}**",
        f"- Unassigned variants: **{len(catalog['unassignedThemes'])}**",
        "",
        "| Category | Families |",
        "|---|---:|",
    ]
    for category in catalog["categories"]:
        count = sum(family["category"] == category for family in catalog["families"])
        lines.append(f"| {category} | {count} |")

    lines.extend(["", "## Foundation palettes", ""])
    for palette in catalog["foundationPalettes"]:
        lines.extend([
            f"### {palette['name']}",
            "",
            f"Category: **{palette['category']}**. {palette['character']}",
            "",
            "| Named color | Value | Intended character or role |",
            "|---|---|---|",
        ])
        for color in palette["namedColors"]:
            lines.append(f"| {color['name']} | `{color['value']}` | {color.get('note') or 'Foundation color'} |")
        lines.extend(["", "Alert mappings:", ""])
        for role, value in palette["alerts"].items():
            lines.append(f"- **{role.title()}:** `{value['value']}` — {value['name']}")
        lines.append("")

    lines.extend(["## Product palettes", "", "Each product palette preserves all source semantic roles. `Related generated family` is a discovery aid, not an instruction to replace these values.", ""])
    for palette in catalog["productPalettes"]:
        lines.extend([
            f"### {palette['name']}",
            "",
            f"Category: **{palette['category']}**. Mode: **{palette['mode']}**. Related generated family: **{palette.get('mapsTo', 'none')}**.",
            "",
            palette["character"],
            "",
            *role_rows(palette["roles"]),
            "",
        ])

    lines.extend(["## Experimental reference families", ""])
    for palette in catalog["referenceFamilies"]:
        lines.extend([
            f"### {palette['name']}",
            "",
            f"Category: **{palette['category']}**. Mode: **{palette['mode']}**. Related generated family: **{palette.get('mapsTo', 'none')}**.",
            "",
            palette["character"],
            "",
            *role_rows(palette["roles"]),
            "",
        ])

    lines.extend(["## Generated family index", ""])
    for category in catalog["categories"]:
        families = [family for family in catalog["families"] if family["category"] == category]
        lines.extend([f"### {category}", "", "| Family | Slug | Modes | Variants | Representative swatches |", "|---|---|---|---:|---|"])
        for family in families:
            swatches = " ".join(f"`{color}`" for color in family["swatches"][:8])
            lines.append(f"| {family['name']} | `{family['slug']}` | {', '.join(family['modes'])} | {family['variantCount']} | {swatches} |")
        lines.append("")

    lines.extend(["## Complete variant catalog", ""])
    for family in catalog["families"]:
        lines.extend([
            f"### {family['name']} variants",
            "",
            f"Category: **{family['category']}**. Family slug: `{family['slug']}`. Representative variant: `{family['representative']}`.",
            "",
            "Family palette: " + " ".join(f"`{color}`" for color in family["swatches"]) + ".",
            "",
        ])
        if family["mappedReferences"]:
            lines.append("Related bundled palettes: " + ", ".join(item["name"] for item in family["mappedReferences"]) + ".")
            lines.append("")
        for variant in family["variants"]:
            lines.append(f"- **{variant['label']}** — {variant['mode']} — variant ID `{variant['file']}`")
        lines.append("")

    lines.extend(["## Provenance", "", "All origins below are descriptive records already incorporated into this bundled set. They are not runtime dependencies.", ""])
    for source in catalog["sources"]:
        lines.append(f"- **{source['label']}** ({source['kind']}) — {source['source']}")

    lines.extend([
        "",
        "## Maintenance",
        "",
        "1. Edit `assets/theme-family-catalog.json` inside this skill.",
        "2. Preserve exact named roles, modes, category, character, and related-family metadata.",
        "3. Run `python3 scripts/build_palette_master.py` from the Theme Library skill root.",
        "4. Run `python3 scripts/build_palette_master.py --check` and the Gremlin Skills repository validators.",
        "5. Synchronize the repository and installed skill copies.",
        "",
        f"Catalog integrity digest: `{catalog['catalogDigest']}`.",
        "",
    ])
    return "\n".join(lines)


def validate_catalog(catalog: dict, raw: str) -> list[str]:
    errors: list[str] = []
    if LOCAL_REFERENCE.search(raw):
        errors.append("catalog contains a local filesystem reference")
    if catalog.get("generatedFamilyCount") != len(catalog.get("families", [])):
        errors.append("generated family count does not match family records")
    if catalog.get("generatedThemeCount") != sum(family.get("variantCount", 0) for family in catalog.get("families", [])):
        errors.append("generated theme count does not match family variant totals")
    if catalog.get("unassignedThemes"):
        errors.append("catalog contains unassigned variants")
    if len(catalog.get("foundationPalettes", [])) != 5:
        errors.append("expected five foundation palettes")
    if len(catalog.get("productPalettes", [])) != 16 or any(len(palette.get("roles", {})) != 18 for palette in catalog.get("productPalettes", [])):
        errors.append("expected sixteen product palettes with eighteen roles each")
    if len(catalog.get("referenceFamilies", [])) != 8 or any(len(palette.get("roles", {})) != 7 for palette in catalog.get("referenceFamilies", [])):
        errors.append("expected eight experimental references with seven roles each")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when the master document is stale or non-portable.")
    args = parser.parse_args()
    raw = CATALOG_PATH.read_text(encoding="utf-8")
    catalog = json.loads(raw)
    errors = validate_catalog(catalog, raw)
    expected = build(catalog)
    if LOCAL_REFERENCE.search(expected):
        errors.append("generated master document contains a local filesystem reference")
    if args.check:
        if not MASTER_PATH.exists() or MASTER_PATH.read_text(encoding="utf-8") != expected:
            errors.append("PALETTE-MASTER.md is missing or stale")
    else:
        MASTER_PATH.write_text(expected, encoding="utf-8")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"Palette master current: {catalog['generatedFamilyCount']} families, {catalog['generatedThemeCount']} variants, {len(catalog['foundationPalettes']) + len(catalog['productPalettes']) + len(catalog['referenceFamilies'])} bundled palettes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
