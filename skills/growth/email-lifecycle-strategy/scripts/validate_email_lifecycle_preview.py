#!/usr/bin/env python3
"""Validate the structural contract for an Email Lifecycle Strategy preview."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_SECTIONS = {
    "strategy-summary",
    "lifecycle-map",
    "decision-simulation",
    "campaign-system",
    "message-preview",
    "trust-and-delivery",
    "measurement",
    "tradeoffs",
}
REQUIRED_ACTIONS = {"refine", "new-set", "approve"}
REQUIRED_EMAIL_VIEWS = {"desktop", "mobile"}
REQUIRED_EMAIL_THEMES = {"light", "dark"}
REQUIRED_IMAGE_STATES = {"on", "off"}
NON_SEND_DECISIONS = {"wait", "replace", "suppress", "exit", "escalate", "sunset"}
PLACEHOLDERS = (
    "lorem ipsum",
    "jane doe",
    "acme",
    "your product here",
    "your company here",
    "dummy copy",
    "placeholder gradient",
)


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

        if "data-email-lifecycle-preview" in values:
            self.metadata = values

        if "data-strategy-target" in values:
            self.controls.append(values)

        panel_id = values.get("data-strategy-panel")
        if panel_id:
            if tag not in {"article", "section", "div"}:
                self.invalid_panel_tags.append(tag)
            self.panels[panel_id] = {
                "sections": set(),
                "user_states": set(),
                "campaigns": 0,
                "decisions": set(),
                "message_samples": 0,
                "email_views": set(),
                "email_themes": set(),
                "image_states": set(),
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
            user_state = values.get("data-user-state")
            if user_state:
                panel["user_states"].add(user_state)  # type: ignore[union-attr]
            if "data-campaign-card" in values:
                panel["campaigns"] = int(panel["campaigns"]) + 1
            decision = values.get("data-decision-outcome")
            if decision:
                panel["decisions"].add(decision)  # type: ignore[union-attr]
            if "data-message-sample" in values:
                panel["message_samples"] = int(panel["message_samples"]) + 1
            email_view = values.get("data-email-view")
            if email_view:
                panel["email_views"].add(email_view)  # type: ignore[union-attr]
            email_theme = values.get("data-email-theme")
            if email_theme:
                panel["email_themes"].add(email_theme)  # type: ignore[union-attr]
            image_state = values.get("data-images")
            if image_state:
                panel["image_states"].add(image_state)  # type: ignore[union-attr]
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

    for attribute in ("data-preview-revision", "data-lifecycle-slug", "data-evidence-date", "data-program-scope"):
        if not parser.metadata.get(attribute):
            errors.append(f"missing preview metadata: {attribute}")

    if len(parser.controls) < 2:
        errors.append("expected at least two strategy controls")

    panel_ids = set(parser.panels)
    if parser.invalid_panel_tags:
        errors.append("strategy panels must use article, section, or div containers")
    target_ids: set[str] = set()
    for control in parser.controls:
        target = control.get("data-strategy-target", "")
        target_ids.add(target)
        expected_control = parser.panel_dom_ids.get(target, "")
        if not expected_control or control.get("aria-controls") != expected_control:
            errors.append(f"strategy control {target or '(unnamed)'} aria-controls must match its panel id")
        if control.get("aria-selected") not in {"true", "false"}:
            errors.append(f"strategy control {target or '(unnamed)'} lacks valid aria-selected")
    if target_ids != panel_ids:
        errors.append("strategy controls and panel IDs do not match")

    for panel_id, panel in parser.panels.items():
        missing_sections = sorted(REQUIRED_SECTIONS - set(panel["sections"]))
        if missing_sections:
            errors.append(f"panel {panel_id} missing sections: {', '.join(missing_sections)}")
        if len(set(panel["user_states"])) < 2:
            errors.append(f"panel {panel_id} needs at least two user states")
        if int(panel["campaigns"]) < 3:
            errors.append(f"panel {panel_id} needs at least three campaign cards")
        decisions = set(panel["decisions"])
        if "send" not in decisions:
            errors.append(f"panel {panel_id} needs a send decision")
        if not decisions.intersection(NON_SEND_DECISIONS):
            errors.append(f"panel {panel_id} needs a non-send decision")
        if int(panel["message_samples"]) < 3:
            errors.append(f"panel {panel_id} needs at least three message samples")
        missing_views = sorted(REQUIRED_EMAIL_VIEWS - set(panel["email_views"]))
        if missing_views:
            errors.append(f"panel {panel_id} missing email views: {', '.join(missing_views)}")
        missing_themes = sorted(REQUIRED_EMAIL_THEMES - set(panel["email_themes"]))
        if missing_themes:
            errors.append(f"panel {panel_id} missing email themes: {', '.join(missing_themes)}")
        missing_images = sorted(REQUIRED_IMAGE_STATES - set(panel["image_states"]))
        if missing_images:
            errors.append(f"panel {panel_id} missing image states: {', '.join(missing_images)}")
        if int(panel["interactive"]) < 1:
            errors.append(f"panel {panel_id} has no interactive lifecycle control")

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
    if re.search(r"\b(?:fetch|xmlhttprequest|websocket|eventsource|sendbeacon)\s*\(", lower):
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

    print(f"Validated email lifecycle preview: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
