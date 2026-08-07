#!/usr/bin/env python3
"""Validate structural and self-containment rules for landing-page previews."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_ASPECTS = {
    "message",
    "cta",
    "product",
    "proof",
    "objections",
    "responsive",
    "motion",
    "seo",
    "tradeoffs",
}
FEEDBACK_ACTIONS = {"refine", "new-set", "approve"}
PLACEHOLDERS = (
    "lorem ipsum",
    "jane doe",
    "acme corp",
    "example.com",
    "placeholder testimonial",
    "insert screenshot",
    "todo:",
)
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class PreviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.doctype = False
        self.has_html = False
        self.lang = ""
        self.has_charset = False
        self.has_viewport = False
        self.has_title = False
        self.has_main = False
        self.has_preview_marker = False
        self.preview_mode = ""
        self.metadata: set[str] = set()
        self.panels: dict[str, set[str]] = defaultdict(set)
        self.option_ids: set[str] = set()
        self.direction_controls: list[dict[str, str]] = []
        self.feedback_actions: set[str] = set()
        self.ctas: list[dict[str, str]] = []
        self.dead_links: list[str] = []
        self.remote_assets: list[str] = []
        self.text_parts: list[str] = []
        self._panel_stack: list[str | None] = []
        self._current_panel: str | None = None

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower() == "doctype html":
            self.doctype = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        self._panel_stack.append(self._current_panel)

        if tag == "html":
            self.has_html = True
            self.lang = values.get("lang", "").strip()
        if "data-landing-preview" in values:
            self.has_preview_marker = True
        if values.get("data-preview-mode"):
            self.preview_mode = values["data-preview-mode"].strip().lower()
        for name in ("data-slug", "data-revision", "data-evidence-date"):
            if values.get(name):
                self.metadata.add(name)

        if tag == "meta":
            if values.get("charset", "").lower() == "utf-8":
                self.has_charset = True
            if values.get("name", "").lower() == "viewport" and values.get("content"):
                self.has_viewport = True
        if tag == "title":
            self.has_title = True
        if tag == "main":
            self.has_main = True

        panel_marker = values.get("data-direction-panel")
        if "data-direction-panel" in values:
            panel_id = values.get("id") or panel_marker
            if panel_id:
                self._current_panel = panel_id
                self.panels[panel_id]
            option_id = values.get("data-option-id")
            if option_id:
                self.option_ids.add(option_id)

        aspect = values.get("data-preview-aspect", "").strip().lower()
        if aspect and self._current_panel:
            self.panels[self._current_panel].add(aspect)

        if "data-direction-target" in values:
            self.direction_controls.append(values)
        if values.get("data-feedback-action"):
            self.feedback_actions.add(values["data-feedback-action"].strip().lower())
        if "data-cta" in values:
            self.ctas.append(values)

        if tag == "a" and values.get("href", "").strip() in {"", "#"}:
            self.dead_links.append(values.get("href", ""))

        if tag in {"script", "img", "source", "video", "audio", "iframe"}:
            source = values.get("src", "")
            if re.match(r"(?i)https?:|//", source):
                self.remote_assets.append(f"{tag}[src={source}]")
        if tag == "link":
            href = values.get("href", "")
            if re.match(r"(?i)https?:|//", href):
                self.remote_assets.append(f"link[href={href}]")

        if tag in VOID_TAGS and self._panel_stack:
            self._current_panel = self._panel_stack.pop()

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if self._panel_stack:
            self._current_panel = self._panel_stack.pop()

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text_parts.append(data.strip())


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read UTF-8 HTML: {exc}"]

    parser = PreviewParser()
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:  # HTMLParser errors are rare, but report cleanly.
        return [f"HTML parse failed: {exc}"]

    if not parser.doctype:
        errors.append("missing <!doctype html>")
    if not parser.has_html or not parser.lang:
        errors.append("<html> must include a non-empty lang attribute")
    if not parser.has_charset:
        errors.append("missing UTF-8 charset metadata")
    if not parser.has_viewport:
        errors.append("missing viewport metadata")
    if not parser.has_title:
        errors.append("missing descriptive <title>")
    if not parser.has_main:
        errors.append("missing <main> landmark")
    if not parser.has_preview_marker:
        errors.append("missing data-landing-preview marker")

    if parser.preview_mode not in {"single", "comparison"}:
        errors.append('data-preview-mode must be "single" or "comparison"')
    for name in ("data-slug", "data-revision", "data-evidence-date"):
        if name not in parser.metadata:
            errors.append(f"missing visible preview metadata attribute {name}")

    visible_text = " ".join(parser.text_parts).lower()
    if "planning preview" not in visible_text or "not production" not in visible_text:
        errors.append('missing visible "planning preview, not production" notice')

    if parser.preview_mode == "single" and len(parser.panels) < 1:
        errors.append("single mode requires at least one data-direction-panel")
    if parser.preview_mode == "comparison":
        if len(parser.panels) < 2:
            errors.append("comparison mode requires at least two data-direction-panel elements")
        if len(parser.direction_controls) < 2:
            errors.append("comparison mode requires at least two data-direction-target controls")

    panel_ids = set(parser.panels)
    targets: set[str] = set()
    for index, control in enumerate(parser.direction_controls, start=1):
        target = control.get("data-direction-target", "").strip()
        aria_controls = control.get("aria-controls", "").strip()
        if not target:
            errors.append(f"direction control {index} has an empty data-direction-target")
        else:
            targets.add(target)
        if aria_controls != target:
            errors.append(f"direction control {index} aria-controls must match its target")
        if control.get("aria-selected") not in {"true", "false"}:
            errors.append(f"direction control {index} needs aria-selected=true|false")
    missing_targets = targets - panel_ids
    if missing_targets:
        errors.append(f"direction controls target missing panels: {sorted(missing_targets)}")

    for panel_id, aspects in parser.panels.items():
        missing = REQUIRED_ASPECTS - aspects
        if missing:
            errors.append(f"panel {panel_id!r} missing preview aspects: {sorted(missing)}")
    if len(parser.option_ids) < len(parser.panels):
        errors.append("every direction panel needs a unique data-option-id")

    missing_feedback = FEEDBACK_ACTIONS - parser.feedback_actions
    if missing_feedback:
        errors.append(f"feedback tray missing actions: {sorted(missing_feedback)}")
    if not parser.ctas:
        errors.append("preview must include at least one element marked data-cta")
    for index, cta in enumerate(parser.ctas, start=1):
        destination = cta.get("data-destination") or cta.get("href") or ""
        if destination.strip() in {"", "#"}:
            errors.append(f"CTA {index} needs a non-empty data-destination or non-dead href")

    if parser.dead_links:
        errors.append("preview contains empty or href=# links")
    if parser.remote_assets:
        errors.append(f"preview contains remote assets: {parser.remote_assets}")

    if not re.search(r"@media\s*\([^)]*(?:max-width|min-width|width)", source, re.I):
        errors.append("missing responsive @media rule")
    if not re.search(r"@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)", source, re.I):
        errors.append("missing prefers-reduced-motion: reduce rule")
    if re.search(r"url\(\s*['\"]?\s*(?:https?:|//)", source, re.I):
        errors.append("CSS contains a remote URL")
    if re.search(r"\b(?:fetch|XMLHttpRequest|sendBeacon|WebSocket)\s*\(?", source):
        errors.append("preview contains a network API call")
    if re.search(r"outline\s*:\s*(?:0|none)\b", source, re.I):
        errors.append("preview suppresses focus outlines")

    lower_source = source.lower()
    for placeholder in PLACEHOLDERS:
        if placeholder in lower_source:
            errors.append(f"placeholder content found: {placeholder!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Landing-page preview HTML file")
    args = parser.parse_args()

    errors = validate(args.html)
    if errors:
        print(f"Landing-page preview validation failed: {args.html}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Landing-page preview validation passed: {args.html}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
