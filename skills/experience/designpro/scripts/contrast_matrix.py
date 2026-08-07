#!/usr/bin/env python3
"""Calculate WCAG contrast for explicit token and layer models.

The input describes themes with tokens and named pairs. Background arrays are
ordered bottom-to-top. This utility verifies the supplied model; it does not
discover computed browser styles.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HEX_RE = re.compile(r"^#([0-9a-fA-F]{3,8})$")
RGB_RE = re.compile(r"^rgba?\((.+)\)$", re.IGNORECASE)
KINDS = {"normal-text": 4.5, "large-text": 3.0, "non-text": 3.0}


class ContrastInputError(ValueError):
    """Raised when the contrast model is invalid."""


@dataclass(frozen=True)
class Color:
    red: float
    green: float
    blue: float
    alpha: float = 1.0

    def opaque_hex(self) -> str:
        channels = (self.red, self.green, self.blue)
        return "#" + "".join(f"{round(max(0, min(1, item)) * 255):02X}" for item in channels)


def _unit(value: float, label: str) -> float:
    if not math.isfinite(value) or value < 0 or value > 1:
        raise ContrastInputError(f"{label} must be between 0 and 1")
    return value


def parse_color(raw: str) -> Color:
    value = raw.strip()
    match = HEX_RE.fullmatch(value)
    if match:
        digits = match.group(1)
        if len(digits) in {3, 4}:
            digits = "".join(character * 2 for character in digits)
        if len(digits) not in {6, 8}:
            raise ContrastInputError(f"unsupported hex color: {raw}")
        channels = [int(digits[index:index + 2], 16) / 255 for index in range(0, 6, 2)]
        alpha = int(digits[6:8], 16) / 255 if len(digits) == 8 else 1.0
        return Color(*channels, alpha)

    match = RGB_RE.fullmatch(value)
    if not match:
        raise ContrastInputError(f"unsupported color syntax: {raw}")
    body = match.group(1).replace(",", " ").replace("/", " / ")
    parts = body.split()
    if "/" in parts:
        slash = parts.index("/")
        color_parts, alpha_parts = parts[:slash], parts[slash + 1:]
    else:
        color_parts = parts[:3]
        alpha_parts = parts[3:]
    if len(color_parts) != 3 or len(alpha_parts) > 1:
        raise ContrastInputError(f"invalid rgb color: {raw}")

    def channel(part: str) -> float:
        return _unit(float(part[:-1]) / 100 if part.endswith("%") else float(part) / 255, "rgb channel")

    def alpha(part: str) -> float:
        return _unit(float(part[:-1]) / 100 if part.endswith("%") else float(part), "alpha")

    channels = [channel(part) for part in color_parts]
    return Color(*channels, alpha(alpha_parts[0]) if alpha_parts else 1.0)


def composite(top: Color, bottom: Color) -> Color:
    alpha = top.alpha + bottom.alpha * (1 - top.alpha)
    if alpha == 0:
        return Color(0, 0, 0, 0)
    return Color(
        (top.red * top.alpha + bottom.red * bottom.alpha * (1 - top.alpha)) / alpha,
        (top.green * top.alpha + bottom.green * bottom.alpha * (1 - top.alpha)) / alpha,
        (top.blue * top.alpha + bottom.blue * bottom.alpha * (1 - top.alpha)) / alpha,
        alpha,
    )


def _linear(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(color: Color) -> float:
    return 0.2126 * _linear(color.red) + 0.7152 * _linear(color.green) + 0.0722 * _linear(color.blue)


def contrast(first: Color, second: Color) -> float:
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def _resolve(name_or_color: str, tokens: dict[str, Any], stack: tuple[str, ...] = ()) -> Color:
    if name_or_color not in tokens:
        return parse_color(name_or_color)
    if name_or_color in stack:
        cycle = " -> ".join((*stack, name_or_color))
        raise ContrastInputError(f"token alias cycle: {cycle}")
    raw = tokens[name_or_color]
    if isinstance(raw, dict):
        raw = raw.get("value")
    if not isinstance(raw, str) or not raw.strip():
        raise ContrastInputError(f"token {name_or_color!r} needs a string value")
    reference = raw[1:] if raw.startswith("$") else raw
    return _resolve(reference, tokens, (*stack, name_or_color))


def _background(layers: list[str], tokens: dict[str, Any]) -> Color:
    if not layers:
        raise ContrastInputError("background needs at least one bottom-to-top layer")
    result = _resolve(layers[0], tokens)
    for layer in layers[1:]:
        result = composite(_resolve(layer, tokens), result)
    if result.alpha < 1:
        raise ContrastInputError("final background is translucent; add an opaque bottom layer")
    return result


def evaluate_model(model: dict[str, Any]) -> dict[str, Any]:
    themes = model.get("themes")
    if not isinstance(themes, dict) or not themes:
        raise ContrastInputError("input needs a non-empty themes object")
    results: list[dict[str, Any]] = []
    for theme_name, theme in themes.items():
        if not isinstance(theme, dict):
            raise ContrastInputError(f"theme {theme_name!r} must be an object")
        tokens = theme.get("tokens")
        pairs = theme.get("pairs")
        if not isinstance(tokens, dict) or not isinstance(pairs, list):
            raise ContrastInputError(f"theme {theme_name!r} needs tokens and pairs")
        for index, pair in enumerate(pairs):
            if not isinstance(pair, dict):
                raise ContrastInputError(f"pair {index} in {theme_name!r} must be an object")
            name = pair.get("name")
            foreground_name = pair.get("foreground")
            backgrounds = pair.get("background")
            kind = pair.get("kind", "normal-text")
            if not isinstance(name, str) or not isinstance(foreground_name, str):
                raise ContrastInputError(f"pair {index} in {theme_name!r} needs name and foreground")
            if not isinstance(backgrounds, list) or not all(isinstance(item, str) for item in backgrounds):
                raise ContrastInputError(f"pair {name!r} background must be a string array")
            if kind not in KINDS:
                raise ContrastInputError(f"pair {name!r} kind must be one of {', '.join(KINDS)}")
            background = _background(backgrounds, tokens)
            foreground = _resolve(foreground_name, tokens)
            displayed_foreground = composite(foreground, background) if foreground.alpha < 1 else foreground
            ratio = contrast(displayed_foreground, background)
            threshold = KINDS[kind]
            results.append({
                "theme": theme_name,
                "name": name,
                "kind": kind,
                "foreground": foreground_name,
                "background_layers": backgrounds,
                "displayed_foreground": displayed_foreground.opaque_hex(),
                "displayed_background": background.opaque_hex(),
                "ratio": round(ratio, 2),
                "threshold": threshold,
                "status": "PASS" if ratio + 1e-9 >= threshold else "FAIL",
            })
    return {"version": 1, "results": results, "summary": {
        "pairs": len(results),
        "passed": sum(item["status"] == "PASS" for item in results),
        "failed": sum(item["status"] == "FAIL" for item in results),
    }}


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Contrast matrix",
        "",
        "| Theme | Pair | Kind | Foreground | Background layers | Displayed pair | Ratio | Required | Status |",
        "|---|---|---|---|---|---|---:|---:|---|",
    ]
    for item in report["results"]:
        layers = " → ".join(item["background_layers"])
        displayed = f'{item["displayed_foreground"]} / {item["displayed_background"]}'
        lines.append(
            f'| {item["theme"]} | {item["name"]} | {item["kind"]} | {item["foreground"]} | '
            f'{layers} | {displayed} | {item["ratio"]:.2f}:1 | {item["threshold"]:.1f}:1 | {item["status"]} |'
        )
    summary = report["summary"]
    lines.extend(["", f'Pairs: {summary["pairs"]}; passed: {summary["passed"]}; failed: {summary["failed"]}.', ""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON token and layer model")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path, help="write output instead of stdout")
    args = parser.parse_args(argv)
    try:
        model = json.loads(args.input.read_text(encoding="utf-8"))
        report = evaluate_model(model)
        rendered = json.dumps(report, indent=2) + "\n" if args.format == "json" else markdown(report)
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
        return 1 if report["summary"]["failed"] else 0
    except (OSError, json.JSONDecodeError, ContrastInputError) as error:
        print(f"contrast_matrix: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
