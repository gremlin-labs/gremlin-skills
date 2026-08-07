#!/usr/bin/env python3
"""Validate the structural contract for an Onboarding Direction HTML preview."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_SECTIONS = {
    "direction-summary",
    "activation-path",
    "screens",
    "states",
    "copy",
    "accessibility",
    "measurement",
    "tradeoffs",
}
REQUIRED_ACTIONS = {"refine", "new-set", "approve"}
PLACEHOLDERS = ("lorem ipsum", "jane doe", "acme", "placeholder gradient", "your product here")


class PreviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.has_main = False
        self.has_title = False
        self.meta_charset = False
        self.meta_viewport = False
        self.controls: list[dict[str, str]] = []
        self.panels: dict[str, dict[str, object]] = {}
        self.panel_dom_ids: dict[str, str] = {}
        self.actions: set[str] = set()
        self.metadata: dict[str, str] = {}
        self._panel_stack: list[str] = []
        self._element_stack: list[tuple[str, str | None]] = []
        self.invalid_panel_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.html_lang = values.get("lang", "")
        elif tag == "main":
            self.has_main = True
        elif tag == "meta":
            self.meta_charset = self.meta_charset or bool(values.get("charset"))
            self.meta_viewport = self.meta_viewport or values.get("name", "").lower() == "viewport"

        if "data-onboarding-preview" in values:
            self.metadata = values

        if "data-direction-target" in values:
            self.controls.append(values)

        panel_id = values.get("data-direction-panel")
        if panel_id:
            if tag not in {"article", "section", "div"}:
                self.invalid_panel_tags.append(tag)
            self.panels[panel_id] = {
                "sections": set(),
                "platforms": set(),
                "steps": 0,
                "activation": 0,
                "interactive": 0,
            }
            self.panel_dom_ids[panel_id] = values.get("id", "")
            self._panel_stack.append(panel_id)

        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self._element_stack.append((tag, panel_id or None))

        if self._panel_stack:
            panel = self.panels[self._panel_stack[-1]]
            section = values.get("data-preview-section")
            if section:
                panel["sections"].add(section)  # type: ignore[union-attr]
            platform = values.get("data-platform-view")
            if platform:
                panel["platforms"].add(platform)  # type: ignore[union-attr]
            if "data-flow-step" in values:
                panel["steps"] = int(panel["steps"]) + 1
            if "data-activation-moment" in values:
                panel["activation"] = int(panel["activation"]) + 1
            if tag in {"a", "button", "input", "select", "textarea"}:
                panel["interactive"] = int(panel["interactive"]) + 1

        action = values.get("data-preview-action")
        if action:
            self.actions.add(action)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.has_title = True
        while self._element_stack:
            opened_tag, opened_panel = self._element_stack.pop()
            if opened_panel and self._panel_stack and self._panel_stack[-1] == opened_panel:
                self._panel_stack.pop()
            if opened_tag == tag:
                break

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if self._element_stack and self._element_stack[-1][0] == tag:
            _, opened_panel = self._element_stack.pop()
            if opened_panel and self._panel_stack and self._panel_stack[-1] == opened_panel:
                self._panel_stack.pop()

    def close(self) -> None:
        super().close()
        self._panel_stack.clear()


def validate_text(text: str) -> list[str]:
    errors: list[str] = []
    lower = text.lower()

    if not re.search(r"<!doctype\s+html", text, re.IGNORECASE):
        errors.append("missing HTML doctype")

    parser = PreviewParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:
        errors.append(f"HTML parse failed: {exc}")
        return errors

    if not parser.html_lang:
        errors.append("missing document language")
    if not parser.has_title:
        errors.append("missing title")
    if not parser.meta_charset:
        errors.append("missing charset metadata")
    if not parser.meta_viewport:
        errors.append("missing viewport metadata")
    if not parser.has_main:
        errors.append("missing main landmark")
    if "planning preview" not in lower or "not production" not in lower:
        errors.append("missing visible planning-preview notice")
    if "<script" not in lower:
        errors.append("missing embedded interaction script")

    for attribute in ("data-preview-revision", "data-onboarding-slug", "data-evidence-date", "data-platform-scope"):
        if not parser.metadata.get(attribute):
            errors.append(f"missing preview metadata: {attribute}")

    if len(parser.controls) < 2:
        errors.append("expected at least two direction controls")

    panel_ids = set(parser.panels)
    if parser.invalid_panel_tags:
        errors.append("direction panels must use article, section, or div containers")
    target_ids: set[str] = set()
    for control in parser.controls:
        target = control.get("data-direction-target", "")
        target_ids.add(target)
        expected_control = parser.panel_dom_ids.get(target, "")
        if not expected_control or control.get("aria-controls") != expected_control:
            errors.append(f"direction control {target or '(unnamed)'} aria-controls must match its panel id")
        if control.get("aria-selected") not in {"true", "false"}:
            errors.append(f"direction control {target or '(unnamed)'} lacks valid aria-selected")
    if target_ids != panel_ids:
        errors.append("direction controls and panel IDs do not match")

    for panel_id, panel in parser.panels.items():
        sections = set(panel["sections"])
        missing = sorted(REQUIRED_SECTIONS - sections)
        if missing:
            errors.append(f"panel {panel_id} missing sections: {', '.join(missing)}")
        platforms = set(panel["platforms"])
        if not platforms:
            errors.append(f"panel {panel_id} has no platform view")
        if int(panel["steps"]) < 2:
            errors.append(f"panel {panel_id} needs at least two flow steps")
        if int(panel["activation"]) < 1:
            errors.append(f"panel {panel_id} has no activation moment")
        if int(panel["interactive"]) < 1:
            errors.append(f"panel {panel_id} has no interactive flow control")

    missing_actions = sorted(REQUIRED_ACTIONS - parser.actions)
    if missing_actions:
        errors.append(f"missing feedback actions: {', '.join(missing_actions)}")

    if "@media" not in lower or "max-width" not in lower:
        errors.append("missing responsive media rule")
    if "prefers-reduced-motion" not in lower:
        errors.append("missing reduced-motion rule")
    if re.search(r"outline\s*:\s*(?:none|0)\b", lower):
        errors.append("focus outlines are suppressed")

    if re.search(r"(?:src|href)\s*=\s*[\"'](?:https?:)?//", text, re.IGNORECASE):
        errors.append("remote resource or navigation URL found")
    if re.search(r"\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\s*\(", text):
        errors.append("network API found")
    if re.search(r"href\s*=\s*[\"'](?:#|javascript:)", text, re.IGNORECASE):
        errors.append("dead or JavaScript link found")

    for placeholder in PLACEHOLDERS:
        if placeholder in lower:
            errors.append(f"placeholder content found: {placeholder}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 1

    errors = validate_text(args.path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated onboarding preview: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
