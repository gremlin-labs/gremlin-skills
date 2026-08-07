#!/usr/bin/env python3
"""Validate the structural contract of a Motion Direction Studio preview."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_CATEGORIES = {
    "page-route",
    "navigation",
    "menu-sidebar",
    "overlay",
    "form-feedback",
    "data-update",
    "loading-progress",
    "state-recovery",
    "notification",
    "signature-delight",
}
REQUIRED_EVIDENCE = {"SIMULATED", "PUBLIC-RUNTIME", "UNVERIFIED"}
PLACEHOLDERS = re.compile(r"\b(?:TODO|FIXME|lorem ipsum|jane doe|acme)\b", re.IGNORECASE)
CSS_NETWORK = re.compile(r"url\(\s*[\"']?(?:https?:)?//", re.IGNORECASE)
JS_NETWORK = re.compile(r"\b(?:fetch|WebSocket|EventSource)\s*\(\s*[\"'](?:https?:)?//", re.IGNORECASE)
NETWORK_ATTRIBUTES = {"src", "href", "action", "formaction", "poster", "data"}


class PreviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = False
        self.has_charset = False
        self.has_title = False
        self.has_main = False
        self.has_viewport = False
        self.direction_controls: list[dict[str, str]] = []
        self.direction_panels: list[dict[str, str]] = []
        self.surface_controls: list[dict[str, str]] = []
        self.surface_panels: list[dict[str, str]] = []
        self.replay_controls = 0
        self.motion_modes: set[str] = set()
        self.stress_controls = 0
        self.categories: dict[str, list[str]] = {}
        self.feedback_actions: set[str] = set()
        self.remote_references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html" and values.get("lang"):
            self.html_lang = True
        if tag == "title":
            self.has_title = True
        if tag == "main":
            self.has_main = True
        if tag == "meta" and "charset" in values:
            self.has_charset = bool(values["charset"])
        if tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if "data-direction-target" in values:
            self.direction_controls.append(values)
        if "data-direction-panel" in values:
            self.direction_panels.append(values)
        if "data-surface-target" in values:
            self.surface_controls.append(values)
        if "data-surface-panel" in values:
            self.surface_panels.append(values)
        if "data-replay-motion" in values:
            self.replay_controls += 1
        if values.get("data-motion-mode"):
            self.motion_modes.add(values["data-motion-mode"].lower())
        if "data-stress-motion" in values:
            self.stress_controls += 1
        if values.get("data-motion-category"):
            category = values["data-motion-category"].lower()
            self.categories.setdefault(category, []).append(values.get("data-evidence-status", "").upper())
        if values.get("data-feedback-action"):
            self.feedback_actions.add(values["data-feedback-action"].lower())
        for attribute in NETWORK_ATTRIBUTES:
            value = values.get(attribute, "").strip()
            if re.match(r"^(?:https?:)?//", value, re.IGNORECASE):
                self.remote_references.append(f"{attribute}={value}")
            if attribute == "href" and value == "#":
                self.remote_references.append("href=#")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def _validate_control_links(
    controls: list[dict[str, str]],
    panels: list[dict[str, str]],
    label: str,
) -> list[str]:
    errors: list[str] = []
    panel_ids = {panel.get("id", "") for panel in panels}
    if "" in panel_ids or len(panel_ids) != len(panels):
        errors.append(f"{label} panels need unique non-empty ids")
    for control in controls:
        if control.get("aria-controls") not in panel_ids:
            errors.append(f"each {label} control needs aria-controls matching a panel id")
        if control.get("aria-selected") not in {"true", "false"}:
            errors.append(f"each {label} control needs aria-selected=true|false")
    return errors


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    parser = PreviewParser()
    parser.feed(text)
    errors: list[str] = []
    if not re.match(r"\s*<!doctype html>", text, re.IGNORECASE):
        errors.append("missing HTML doctype")
    if not parser.html_lang:
        errors.append("html element needs a lang attribute")
    if not parser.has_charset or not parser.has_title or not parser.has_main or not parser.has_viewport:
        errors.append("preview needs charset, title, main landmark, and viewport metadata")
    if len(parser.direction_controls) < 2 or len(parser.direction_panels) < 2:
        errors.append("preview needs at least two direction controls and panels")
    errors.extend(_validate_control_links(parser.direction_controls, parser.direction_panels, "direction"))
    if len(parser.surface_controls) < 2 or len(parser.surface_panels) < 2:
        errors.append("preview needs at least two surface controls and panels")
    errors.extend(_validate_control_links(parser.surface_controls, parser.surface_panels, "surface"))
    if parser.replay_controls < 1:
        errors.append("preview needs a data-replay-motion control")
    if not {"full", "reduced"}.issubset(parser.motion_modes):
        errors.append("preview needs full and reduced data-motion-mode controls")
    if parser.stress_controls < 1:
        errors.append("preview needs a data-stress-motion interruption control")
    missing_categories = sorted(REQUIRED_CATEGORIES - set(parser.categories))
    if missing_categories:
        errors.append(f"missing motion categories: {', '.join(missing_categories)}")
    invalid_evidence = sorted(
        category
        for category, statuses in parser.categories.items()
        if any(status not in REQUIRED_EVIDENCE for status in statuses)
    )
    if invalid_evidence:
        errors.append(f"motion specimens need valid data-evidence-status labels: {', '.join(invalid_evidence)}")
    missing_actions = {"refine", "new-set", "approve"} - parser.feedback_actions
    if missing_actions:
        errors.append(f"missing feedback actions: {', '.join(sorted(missing_actions))}")
    if "prefers-reduced-motion" not in text:
        errors.append("missing prefers-reduced-motion behavior")
    if "@media" not in text:
        errors.append("missing responsive media query")
    if not re.search(r"planning preview,? not production", text, re.IGNORECASE):
        errors.append("missing planning-preview notice")
    for attribute in ("data-slug", "data-revision", "data-evidence-timestamp"):
        if not re.search(rf"\b{attribute}\s*=\s*[\"'][^\"']+[\"']", text, re.IGNORECASE):
            errors.append(f"missing non-empty {attribute} metadata")
    if parser.remote_references or CSS_NETWORK.search(text) or JS_NETWORK.search(text):
        errors.append("remote assets, dead hash links, form targets, or network calls are forbidden")
    placeholder = PLACEHOLDERS.search(text)
    if placeholder:
        errors.append(f"placeholder content is forbidden: {placeholder.group(0)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("preview", type=Path)
    args = parser.parse_args()
    if not args.preview.is_file():
        parser.error(f"not a file: {args.preview}")
    errors = validate(args.preview)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"Validated Motion Direction Studio: {args.preview}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
