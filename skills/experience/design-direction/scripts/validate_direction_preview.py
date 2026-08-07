#!/usr/bin/env python3
"""Validate the structural contract of a Design Direction HTML preview."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_SECTIONS = {
    "direction-summary", "typography", "palette", "surfaces", "components",
    "states", "responsive", "motion", "tradeoffs",
}
PLACEHOLDERS = re.compile(r"\b(?:TODO|FIXME|lorem ipsum|jane doe|acme)\b", re.IGNORECASE)
CSS_NETWORK = re.compile(r"url\(\s*[\"']?(?:https?:)?//", re.IGNORECASE)
JS_NETWORK = re.compile(r"\b(?:fetch|WebSocket|EventSource)\s*\(\s*[\"'](?:https?:)?//", re.IGNORECASE)
NETWORK_ATTRIBUTES = {"src", "href", "action", "formaction", "poster", "data"}


class PreviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = False
        self.has_title = False
        self.has_main = False
        self.has_viewport = False
        self.controls: list[dict[str, str]] = []
        self.panels: list[dict[str, str]] = []
        self.panel_sections: dict[str, set[str]] = {}
        self.active_panels: list[dict[str, object]] = []
        self.sections: set[str] = set()
        self.feedback_actions: set[str] = set()
        self.remote_references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for panel in self.active_panels:
            panel["depth"] = int(panel["depth"]) + 1
        values = {key: value or "" for key, value in attrs}
        if tag == "html" and values.get("lang"):
            self.html_lang = True
        if tag == "title":
            self.has_title = True
        if tag == "main":
            self.has_main = True
        if tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if "data-direction-target" in values:
            self.controls.append(values)
        if "data-direction-panel" in values:
            self.panels.append(values)
            panel_id = values.get("id", "")
            self.panel_sections.setdefault(panel_id, set())
            self.active_panels.append({"id": panel_id, "depth": 1})
        if values.get("data-preview-section"):
            section = values["data-preview-section"]
            self.sections.add(section)
            for panel in self.active_panels:
                self.panel_sections.setdefault(str(panel["id"]), set()).add(section)
        if values.get("data-feedback-action"):
            self.feedback_actions.add(values["data-feedback-action"])
        for attribute in NETWORK_ATTRIBUTES:
            value = values.get(attribute, "").strip()
            if re.match(r"^(?:https?:)?//", value, re.IGNORECASE):
                self.remote_references.append(f"{attribute}={value}")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        for panel in self.active_panels:
            panel["depth"] = int(panel["depth"]) - 1
        self.active_panels = [panel for panel in self.active_panels if int(panel["depth"]) > 0]


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    parser = PreviewParser()
    parser.feed(text)
    errors: list[str] = []
    if not re.match(r"\s*<!doctype html>", text, re.IGNORECASE):
        errors.append("missing HTML doctype")
    if not parser.html_lang:
        errors.append("html element needs a lang attribute")
    if not parser.has_title or not parser.has_main or not parser.has_viewport:
        errors.append("preview needs title, main landmark, and viewport metadata")
    if len(parser.controls) < 2 or len(parser.panels) < 2:
        errors.append("preview needs at least two direction controls and panels")
    panel_ids = {panel.get("id", "") for panel in parser.panels}
    if "" in panel_ids or len(panel_ids) != len(parser.panels):
        errors.append("direction panels need unique non-empty ids")
    for control in parser.controls:
        if control.get("aria-controls") not in panel_ids:
            errors.append("each direction control needs aria-controls matching a panel id")
        if control.get("aria-selected") not in {"true", "false"}:
            errors.append("each direction control needs aria-selected=true|false")
    missing_sections = sorted(REQUIRED_SECTIONS - parser.sections)
    if missing_sections:
        errors.append(f"missing preview sections globally: {', '.join(missing_sections)}")
    for panel in parser.panels:
        panel_id = panel.get("id", "") or "unnamed panel"
        panel_missing = sorted(REQUIRED_SECTIONS - parser.panel_sections.get(panel.get("id", ""), set()))
        if panel_missing:
            errors.append(f"direction panel {panel_id} is missing sections: {', '.join(panel_missing)}")
    missing_actions = {"refine", "new-set", "approve"} - parser.feedback_actions
    if missing_actions:
        errors.append(f"missing feedback actions: {', '.join(sorted(missing_actions))}")
    if "prefers-reduced-motion" not in text:
        errors.append("missing prefers-reduced-motion behavior")
    if "@media" not in text:
        errors.append("missing responsive media query")
    if parser.remote_references or CSS_NETWORK.search(text) or JS_NETWORK.search(text):
        errors.append("remote assets, form targets, or network calls are forbidden")
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
    print(f"Validated direction preview: {args.preview}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
