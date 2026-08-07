#!/usr/bin/env python3
"""Read-only evidence collector and normalizer for the seo-setup skill."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


VERSION = "1.0.0"
SCHEMA_VERSION = 1
USER_AGENT = f"gremlin-seo-stack/{VERSION} (+read-only setup verification)"
TIMEOUT_SECONDS = 12
MAX_BODY_BYTES = 2_000_000
MAX_REDIRECTS = 6
MAX_SITEMAPS = 8
MAX_SITEMAP_URLS = 2_000
DEFAULT_SAMPLE_SIZE = 20

EXIT_CONFIG = 2
EXIT_CREDENTIAL = 3
EXIT_NETWORK = 4
EXIT_INCOMPLETE = 5
EXIT_MUTATION_REFUSED = 6

SECRET_KEY = re.compile(
    r"authorization|cookie|token|secret|password|credential|api[_-]?key|developer[_-]?token",
    re.IGNORECASE,
)
JWT_LIKE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
BEARER = re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/-]{8,}=*")
SENSITIVE_QUERY = re.compile(r"(?i)(access_token|api[_-]?key|code|secret|token)=([^&\s]+)")
STATUSES = {"VERIFIED", "NOT_APPLICABLE", "AWAITING_USER_ACTION", "BLOCKED", "FAILED"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def redact_text(value: str) -> str:
    value = BEARER.sub("Bearer [REDACTED]", value)
    value = JWT_LIKE.sub("[REDACTED]", value)
    return SENSITIVE_QUERY.sub(lambda match: f"{match.group(1)}=[REDACTED]", value)


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if SECRET_KEY.search(str(key)) else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


class SeoStackError(Exception):
    def __init__(self, message: str, exit_code: int = EXIT_CONFIG):
        super().__init__(redact_text(message))
        self.exit_code = exit_code


def canonical_json(value: Any) -> str:
    return json.dumps(redact(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: str | Path) -> Any:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise SeoStackError(f"JSON input does not exist or is not a file: {source}")
    try:
        return json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SeoStackError(f"Cannot read JSON input {source}: {exc}") from None


def safe_output_path(path: str | Path) -> Path:
    target = Path(path).expanduser().absolute()
    if target.exists() and target.is_symlink():
        raise SeoStackError(f"Refusing to overwrite symlink output: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.parent.is_symlink():
        raise SeoStackError(f"Refusing output through symlink directory: {target.parent}")
    return target


def write_json(path: str | Path, value: Any) -> None:
    safe_output_path(path).write_text(canonical_json(value), encoding="utf-8")


def write_text(path: str | Path, value: str) -> None:
    safe_output_path(path).write_text(value, encoding="utf-8")


def validate_https_url(value: str, field: str, *, allow_local_http: bool = False) -> None:
    parsed = urllib.parse.urlsplit(value)
    local = parsed.hostname in {"localhost", "127.0.0.1", "::1"}
    if not parsed.hostname or parsed.username or parsed.password:
        raise SeoStackError(f"{field} must be an absolute URL without embedded credentials")
    if parsed.scheme != "https" and not (allow_local_http and local and parsed.scheme == "http"):
        raise SeoStackError(f"{field} must use HTTPS")


def validate_config(config: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["configuration root must be an object"]
    allowed_root = {"schema_version", "canonical_origin", "providers"}
    unknown = set(config) - allowed_root
    if unknown:
        errors.append(f"unknown top-level fields: {', '.join(sorted(unknown))}")
    if config.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    try:
        validate_https_url(config.get("canonical_origin", ""), "canonical_origin")
    except SeoStackError as exc:
        errors.append(str(exc))
    providers = config.get("providers")
    if not isinstance(providers, dict):
        errors.append("providers must be an object")
        return errors
    allowed_providers = {"ga4", "search_console", "google_ads", "bing"}
    unknown_providers = set(providers) - allowed_providers
    if unknown_providers:
        errors.append(f"unknown providers: {', '.join(sorted(unknown_providers))}")
    required: dict[str, tuple[str, ...]] = {
        "ga4": ("property_id", "web_stream_id", "credential_source"),
        "search_console": ("site_url", "credential_source"),
        "google_ads": ("customer_id", "credential_source"),
        "bing": ("site_url", "credential_source"),
    }
    allowed_sources = {"application_default_credentials", "oauth", "named_environment", "computer_use"}
    allowed_fields: dict[str, set[str]] = {
        "ga4": {"property_id", "web_stream_id", "measurement_id", "credential_source", "access_token_env"},
        "search_console": {"site_url", "credential_source", "access_token_env"},
        "google_ads": {"customer_id", "login_customer_id", "credential_source", "access_token_env", "developer_token_env", "api_version"},
        "bing": {"site_url", "credential_source", "access_token_env", "api_key_env"},
    }
    for name, provider in providers.items():
        if name not in allowed_providers or not isinstance(provider, dict):
            if name in allowed_providers:
                errors.append(f"providers.{name} must be an object")
            continue
        missing = [field for field in required[name] if not provider.get(field)]
        if missing:
            errors.append(f"providers.{name} missing: {', '.join(missing)}")
        unexpected = set(provider) - allowed_fields[name]
        if unexpected:
            errors.append(f"providers.{name} unknown fields: {', '.join(sorted(unexpected))}")
        if provider.get("credential_source") not in allowed_sources:
            errors.append(f"providers.{name}.credential_source is invalid")
        for field in ("access_token_env", "developer_token_env", "api_key_env"):
            env_name = provider.get(field)
            if env_name is not None and not re.fullmatch(r"[A-Z][A-Z0-9_]*", str(env_name)):
                errors.append(f"providers.{name}.{field} must name an uppercase environment variable")
    for name in ("ga4", "google_ads"):
        provider = providers.get(name, {})
        for field in ("property_id", "web_stream_id", "customer_id", "login_customer_id"):
            value = provider.get(field)
            if value is not None and (not str(value).isdigit() or ("customer" in field and len(str(value)) != 10)):
                errors.append(f"providers.{name}.{field} has an invalid numeric ID")
    return errors


def read_config(path: str | Path) -> dict[str, Any]:
    config = load_json(path)
    errors = validate_config(config)
    if errors:
        raise SeoStackError("Invalid configuration: " + "; ".join(errors))
    return config


def credential_presence(provider: dict[str, Any]) -> tuple[bool, str]:
    source = provider.get("credential_source")
    if source == "computer_use":
        return False, "computer_use requires a signed-in browser check"
    if provider.get("api_key_env"):
        name = provider["api_key_env"]
        return bool(os.environ.get(name)), f"environment variable {name}"
    if provider.get("access_token_env"):
        name = provider["access_token_env"]
        return bool(os.environ.get(name)), f"environment variable {name}"
    if source == "application_default_credentials":
        adc_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        present = bool((adc_file and Path(adc_file).is_file()) or shutil.which("gcloud"))
        return present, "application default credentials"
    return False, "no access_token_env or api_key_env configured"


def named_credential_checks(provider: dict[str, Any]) -> list[tuple[str, bool]]:
    checks = []
    for field in ("access_token_env", "developer_token_env", "api_key_env"):
        env_name = provider.get(field)
        if env_name:
            checks.append((f"environment variable {env_name}", bool(os.environ.get(env_name))))
    if not checks:
        present, source = credential_presence(provider)
        checks.append((source, present))
    return checks


def get_access_token(provider: dict[str, Any]) -> str:
    env_name = provider.get("access_token_env")
    if env_name and os.environ.get(env_name):
        return os.environ[env_name]
    if provider.get("credential_source") == "application_default_credentials" and shutil.which("gcloud"):
        try:
            result = subprocess.run(
                ["gcloud", "auth", "application-default", "print-access-token"],
                check=True,
                capture_output=True,
                text=True,
                timeout=20,
            )
            token = result.stdout.strip()
            if token:
                return token
        except (subprocess.SubprocessError, OSError):
            pass
    raise SeoStackError(
        "Credential unavailable. Configure access_token_env with a named environment variable, "
        "or authenticate Application Default Credentials; use signed-in computer use as the fallback.",
        EXIT_CREDENTIAL,
    )


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.meta: dict[str, str] = {}
        self.canonicals: list[str] = []
        self.json_ld: list[str] = []
        self.in_json_ld = False
        self.json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {str(key).lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "meta":
            key = (values.get("name") or values.get("property") or "").lower()
            if key:
                self.meta[key] = values.get("content", "")
        if tag.lower() == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonicals.append(values.get("href", ""))
        if tag.lower() == "script" and values.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.json_ld_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False
        if tag.lower() == "script" and self.in_json_ld:
            self.json_ld.append("".join(self.json_ld_parts))
            self.in_json_ld = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_ld_parts.append(data)

    def extracted(self) -> dict[str, Any]:
        types: set[str] = set()
        for raw in self.json_ld:
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                continue
            stack = [value]
            while stack:
                item = stack.pop()
                if isinstance(item, dict):
                    kind = item.get("@type")
                    if isinstance(kind, str):
                        types.add(kind)
                    elif isinstance(kind, list):
                        types.update(str(part) for part in kind)
                    stack.extend(item.values())
                elif isinstance(item, list):
                    stack.extend(item)
        return {
            "title": re.sub(r"\s+", " ", "".join(self.title_parts)).strip(),
            "meta_description": self.meta.get("description", ""),
            "robots": self.meta.get("robots", ""),
            "canonical": self.canonicals[0] if len(self.canonicals) == 1 else None,
            "canonical_count": len(self.canonicals),
            "structured_data_types": sorted(types),
        }


class RecordingRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self) -> None:
        self.chain: list[dict[str, Any]] = []

    def redirect_request(self, req: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        self.chain.append({"status": code, "from": redact_text(req.full_url), "to": redact_text(newurl)})
        if len(self.chain) > MAX_REDIRECTS:
            raise SeoStackError(f"Redirect limit exceeded ({MAX_REDIRECTS})", EXIT_NETWORK)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def http_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, str], bytes, str, list[dict[str, Any]]]:
    redirect = RecordingRedirectHandler()
    opener = urllib.request.build_opener(redirect)
    request_headers = {"User-Agent": USER_AGENT, "Accept": "application/json,text/html,application/xml,text/plain;q=0.8"}
    request_headers.update(headers or {})
    data = json.dumps(body).encode("utf-8") if body is not None else None
    if data is not None:
        request_headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            payload = response.read(MAX_BODY_BYTES + 1)
            if len(payload) > MAX_BODY_BYTES:
                raise SeoStackError(f"Response exceeds {MAX_BODY_BYTES} bytes", EXIT_NETWORK)
            return response.status, dict(response.headers.items()), payload, response.geturl(), redirect.chain
    except urllib.error.HTTPError as exc:
        payload = exc.read(min(MAX_BODY_BYTES, 64_000))
        return exc.code, dict(exc.headers.items()), payload, exc.geturl(), redirect.chain
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise SeoStackError(f"Network request failed: {exc}", EXIT_NETWORK) from None


def json_api(
    url: str,
    *,
    token: str | None = None,
    headers: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
) -> tuple[int, Any]:
    request_headers = dict(headers or {})
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    status, _, payload, _, _ = http_request(url, method="POST" if body is not None else "GET", headers=request_headers, body=body)
    try:
        parsed = json.loads(payload.decode("utf-8")) if payload else {}
    except (UnicodeDecodeError, json.JSONDecodeError):
        parsed = {"message": "Provider returned a non-JSON response"}
    return status, parsed


def classify_provider_status(http_status: int, payload: Any) -> tuple[str, str, int]:
    if 200 <= http_status < 300:
        return "VERIFIED", "Provider accepted the read-only request", 0
    if http_status == 401:
        return "UNAUTHORIZED", "Authentication was rejected", EXIT_CREDENTIAL
    if http_status == 403:
        return "UNAUTHORIZED", "Authenticated principal lacks required access or the API is disabled", EXIT_CREDENTIAL
    if http_status == 404:
        return "FAILED", "Configured property, site, account, or API route was not found", EXIT_INCOMPLETE
    if http_status == 429:
        return "UNAVAILABLE", "Provider quota or rate limit blocked verification", EXIT_NETWORK
    detail = "Provider request failed"
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict) and isinstance(error.get("status"), str):
            detail += f" ({error['status']})"
    return "FAILED", detail, EXIT_NETWORK if http_status >= 500 else EXIT_INCOMPLETE


def envelope(provider: str, requested: dict[str, Any], actual: dict[str, Any], status: str, checks: list[dict[str, Any]], warnings: list[str]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "provider": provider,
        "retrieved_at": utc_now(),
        "requested_scope": requested,
        "actual_scope": actual,
        "status": status,
        "checks": checks,
        "warnings": warnings,
        "redactions_applied": True,
    }


def check(check_id: str, status: str, summary: str, evidence: Iterable[str] = ()) -> dict[str, Any]:
    return {"id": check_id, "status": status, "summary": summary, "evidence": list(evidence)}


def doctor(config_path: str, json_path: str | None) -> int:
    config = read_config(config_path)
    checks = [
        {"id": "runtime", "status": "VERIFIED", "summary": f"Python {sys.version_info.major}.{sys.version_info.minor}; CLI {VERSION}; schema {SCHEMA_VERSION}"},
        {"id": "canonical_origin", "status": "VERIFIED", "summary": config["canonical_origin"]},
    ]
    missing = False
    for name, provider in sorted(config["providers"].items()):
        for index, (source, present) in enumerate(named_credential_checks(provider), 1):
            checks.append({"id": f"credential.{name}.{index}", "status": "VERIFIED" if present else "INCOMPLETE", "summary": f"{source}: {'present' if present else 'absent or interactive'}"})
            missing = missing or not present
    result = {"schema_version": SCHEMA_VERSION, "cli_version": VERSION, "checked_at": utc_now(), "status": "INCOMPLETE" if missing else "VERIFIED", "checks": checks, "redactions_applied": True}
    if json_path:
        write_json(json_path, result)
    sys.stdout.write(canonical_json(result))
    return EXIT_CREDENTIAL if missing else 0


def parse_sitemap(payload: bytes) -> tuple[str, list[str]]:
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise SeoStackError(f"Malformed sitemap XML: {exc}", EXIT_INCOMPLETE) from None
    tag = root.tag.rsplit("}", 1)[-1].lower()
    if tag not in {"urlset", "sitemapindex"}:
        raise SeoStackError(f"Unsupported sitemap root element: {tag}", EXIT_INCOMPLETE)
    locations = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1].lower() == "loc" and element.text:
            locations.append(element.text.strip())
    return tag, locations


def extract_sitemap_directives(robots_text: str, base: str) -> list[str]:
    found = []
    for line in robots_text.splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip().lower() == "sitemap" and value.strip():
            found.append(urllib.parse.urljoin(base, value.strip()))
    return sorted(set(found))


def inspect_page(url: str) -> dict[str, Any]:
    status, headers, payload, final_url, redirects = http_request(url)
    content_type = headers.get("Content-Type", "").split(";", 1)[0].lower()
    result: dict[str, Any] = {
        "requested_url": redact_text(url),
        "final_url": redact_text(final_url),
        "status": status,
        "content_type": content_type,
        "redirects": redirects,
        "content_sha256": hashlib.sha256(payload).hexdigest(),
        "content_bytes": len(payload),
    }
    if "html" in content_type:
        parser = PageParser()
        parser.feed(payload.decode("utf-8", errors="replace"))
        result.update(parser.extracted())
        result["x_robots_tag"] = headers.get("X-Robots-Tag", "")
    return result


def inventory(site: str, output: str) -> int:
    validate_https_url(site, "site", allow_local_http=True)
    parsed = urllib.parse.urlsplit(site)
    origin = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    home = inspect_page(site)
    robots_url = urllib.parse.urljoin(origin + "/", "robots.txt")
    robots_status, robots_headers, robots_body, robots_final, robots_redirects = http_request(robots_url)
    robots_text = robots_body.decode("utf-8", errors="replace") if robots_status == 200 else ""
    sitemaps = extract_sitemap_directives(robots_text, origin + "/")
    default_sitemap = urllib.parse.urljoin(origin + "/", "sitemap.xml")
    if not sitemaps:
        sitemaps = [default_sitemap]
    sitemap_results: list[dict[str, Any]] = []
    discovered_urls: list[str] = []
    queue = list(sitemaps[:MAX_SITEMAPS])
    seen: set[str] = set()
    while queue and len(seen) < MAX_SITEMAPS and len(discovered_urls) < MAX_SITEMAP_URLS:
        sitemap_url = queue.pop(0)
        if sitemap_url in seen:
            continue
        seen.add(sitemap_url)
        try:
            validate_https_url(sitemap_url, "sitemap URL", allow_local_http=True)
            code, headers, payload, final_url, redirects = http_request(sitemap_url)
            item: dict[str, Any] = {"url": sitemap_url, "final_url": final_url, "status": code, "redirects": redirects, "content_type": headers.get("Content-Type", "").split(";", 1)[0], "content_sha256": hashlib.sha256(payload).hexdigest()}
            if code == 200:
                kind, locations = parse_sitemap(payload)
                item.update({"kind": kind, "location_count": len(locations)})
                if kind == "sitemapindex":
                    queue.extend(locations[: max(0, MAX_SITEMAPS - len(seen) - len(queue))])
                else:
                    discovered_urls.extend(locations[: MAX_SITEMAP_URLS - len(discovered_urls)])
            sitemap_results.append(item)
        except SeoStackError as exc:
            sitemap_results.append({"url": sitemap_url, "status": "FAILED", "error": str(exc)})
    samples = []
    for url in discovered_urls[:DEFAULT_SAMPLE_SIZE]:
        try:
            validate_https_url(url, "sitemap page URL", allow_local_http=True)
            samples.append(inspect_page(url))
        except SeoStackError as exc:
            samples.append({"requested_url": url, "status": "FAILED", "error": str(exc)})
    final_scheme = urllib.parse.urlsplit(home["final_url"]).scheme
    checks = [
        check("origin.fetch", "VERIFIED" if home["status"] == 200 else "FAILED", f"Homepage returned {home['status']}", [home["final_url"]]),
        check("origin.https", "VERIFIED" if final_scheme == "https" else "FAILED", f"Final scheme is {final_scheme}"),
        check("robots.fetch", "VERIFIED" if robots_status == 200 else "FAILED", f"robots.txt returned {robots_status}", [redact_text(robots_final)]),
        check("sitemap.parse", "VERIFIED" if sitemap_results and all(item.get("status") == 200 for item in sitemap_results) else "FAILED", f"Parsed {sum(1 for item in sitemap_results if item.get('status') == 200)} of {len(sitemap_results)} sitemap resources"),
    ]
    overall = "VERIFIED" if all(item["status"] == "VERIFIED" for item in checks) else "INCOMPLETE"
    result = envelope("live_site", {"site": site}, {"final_url": home["final_url"]}, overall, checks, [])
    result["data"] = {
        "limits": {"body_bytes": MAX_BODY_BYTES, "redirects": MAX_REDIRECTS, "sitemaps": MAX_SITEMAPS, "sitemap_urls": MAX_SITEMAP_URLS, "sample_size": DEFAULT_SAMPLE_SIZE, "timeout_seconds": TIMEOUT_SECONDS},
        "home": home,
        "robots": {"url": robots_url, "final_url": robots_final, "status": robots_status, "redirects": robots_redirects, "content_type": robots_headers.get("Content-Type", "").split(";", 1)[0], "content_sha256": hashlib.sha256(robots_body).hexdigest(), "declared_sitemaps": extract_sitemap_directives(robots_text, origin + "/")},
        "sitemaps": sitemap_results,
        "sitemap_url_count": len(discovered_urls),
        "sample_method": "first URLs in sitemap traversal order, bounded by sample_size",
        "sampled_pages": samples,
    }
    write_json(output, result)
    return 0 if overall == "VERIFIED" else EXIT_INCOMPLETE


def provider_config(config: dict[str, Any], name: str) -> dict[str, Any]:
    provider = config["providers"].get(name)
    if not provider:
        raise SeoStackError(f"Provider {name} is not configured", EXIT_INCOMPLETE)
    return provider


def analytics_status(config_path: str, output: str) -> int:
    config = read_config(config_path)
    provider = provider_config(config, "ga4")
    token = get_access_token(provider)
    prop = provider["property_id"]
    stream_id = provider["web_stream_id"]
    status, payload = json_api(f"https://analyticsadmin.googleapis.com/v1beta/properties/{prop}/dataStreams", token=token)
    state, summary, exit_code = classify_provider_status(status, payload)
    streams = payload.get("dataStreams", []) if isinstance(payload, dict) else []
    matches = [item for item in streams if str(item.get("name", "")).endswith(f"/{stream_id}")]
    checks = [check("ga4.access", "VERIFIED" if state == "VERIFIED" else state, summary, [f"property {prop}"])]
    if state == "VERIFIED":
        checks.append(check("ga4.web_stream", "VERIFIED" if matches else "FAILED", "Configured web stream is accessible" if matches else "Configured web stream was not returned", [f"stream {stream_id}"]))
    overall = "VERIFIED" if checks and all(item["status"] == "VERIFIED" for item in checks) else ("UNAUTHORIZED" if state == "UNAUTHORIZED" else "INCOMPLETE")
    result = envelope("ga4", {"property_id": prop, "web_stream_id": stream_id}, {"property_id": prop, "matched_stream_id": stream_id if matches else None}, overall, checks, ["Live tag delivery, consent behavior, and an observed test event require separate verification."])
    write_json(output, result)
    return 0 if overall == "VERIFIED" else exit_code or EXIT_INCOMPLETE


def search_console_status(config_path: str, output: str) -> int:
    config = read_config(config_path)
    provider = provider_config(config, "search_console")
    token = get_access_token(provider)
    site = provider["site_url"]
    sites_status, sites_payload = json_api("https://www.googleapis.com/webmasters/v3/sites", token=token)
    state, summary, exit_code = classify_provider_status(sites_status, sites_payload)
    entries = sites_payload.get("siteEntry", []) if isinstance(sites_payload, dict) else []
    match = next((item for item in entries if item.get("siteUrl") == site), None)
    checks = [check("gsc.access", "VERIFIED" if state == "VERIFIED" else state, summary)]
    actual: dict[str, Any] = {"site": site if match else None}
    if state == "VERIFIED":
        permission = match.get("permissionLevel") if match else None
        checks.append(check("gsc.property", "VERIFIED" if match else "FAILED", "Configured property is accessible" if match else "Configured property is absent", [f"permission level: {permission}"] if permission else []))
        if match:
            sitemap_url = "https://www.googleapis.com/webmasters/v3/sites/" + urllib.parse.quote(site, safe="") + "/sitemaps"
            sm_status, sm_payload = json_api(sitemap_url, token=token)
            sm_state, sm_summary, sm_exit = classify_provider_status(sm_status, sm_payload)
            sitemaps = sm_payload.get("sitemap", []) if isinstance(sm_payload, dict) else []
            checks.append(check("gsc.sitemaps", "VERIFIED" if sm_state == "VERIFIED" and sitemaps else ("EMPTY" if sm_state == "VERIFIED" else sm_state), f"{sm_summary}; {len(sitemaps)} sitemap entries returned", [str(item.get("path")) for item in sitemaps[:10]]))
            actual["sitemap_count"] = len(sitemaps)
            exit_code = max(exit_code, sm_exit)
    overall = "VERIFIED" if all(item["status"] == "VERIFIED" for item in checks) else ("UNAUTHORIZED" if state == "UNAUTHORIZED" else "INCOMPLETE")
    write_json(output, envelope("google_search_console", {"site": site}, actual, overall, checks, []))
    return 0 if overall == "VERIFIED" else exit_code or EXIT_INCOMPLETE


def search_console_inspect(config_path: str, inspect_url: str, output: str) -> int:
    config = read_config(config_path)
    provider = provider_config(config, "search_console")
    token = get_access_token(provider)
    site = provider["site_url"]
    status, payload = json_api(
        "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
        token=token,
        body={"inspectionUrl": inspect_url, "siteUrl": site, "languageCode": "en-US"},
    )
    state, summary, exit_code = classify_provider_status(status, payload)
    result_link = payload.get("inspectionResult", {}).get("inspectionResultLink") if isinstance(payload, dict) else None
    checks = [check("gsc.url_inspection", "VERIFIED" if state == "VERIFIED" else state, summary, [result_link] if result_link else [])]
    write_json(output, envelope("google_search_console", {"site": site, "url": inspect_url}, {"site": site, "url": inspect_url}, state, checks, []))
    return 0 if state == "VERIFIED" else exit_code


def ads_keywords(config_path: str, seed: str, market: str, language: str, network: str, seed_type: str, output: str) -> int:
    config = read_config(config_path)
    provider = provider_config(config, "google_ads")
    token = get_access_token(provider)
    developer_env = provider.get("developer_token_env")
    developer_token = os.environ.get(developer_env or "")
    if not developer_token:
        raise SeoStackError("Google Ads developer token environment variable is absent", EXIT_CREDENTIAL)
    customer_id = provider["customer_id"]
    version = provider.get("api_version", "v25")
    headers = {"developer-token": developer_token}
    if provider.get("login_customer_id"):
        headers["login-customer-id"] = provider["login_customer_id"]
    body: dict[str, Any] = {
        "language": f"languageConstants/{language}",
        "geoTargetConstants": [f"geoTargetConstants/{market}"],
        "includeAdultKeywords": False,
        "keywordPlanNetwork": network,
    }
    if seed_type == "url":
        validate_https_url(seed, "seed URL")
        body["urlSeed"] = {"url": seed}
    elif seed_type == "site":
        validate_https_url(seed, "seed site")
        body["siteSeed"] = {"site": seed}
    else:
        body["keywordSeed"] = {"keywords": [seed]}
    url = f"https://googleads.googleapis.com/{version}/customers/{customer_id}:generateKeywordIdeas"
    status, payload = json_api(url, token=token, headers=headers, body=body)
    state, summary, exit_code = classify_provider_status(status, payload)
    raw_results = payload.get("results", []) if isinstance(payload, dict) else []
    ideas = []
    for index, item in enumerate(raw_results):
        metrics = item.get("keywordIdeaMetrics") or {}
        ideas.append({
            "source_row_id": str(index + 1),
            "keyword": item.get("text"),
            "average_monthly_searches": metrics.get("avgMonthlySearches"),
            "competition": metrics.get("competition"),
            "competition_index": metrics.get("competitionIndex"),
            "low_top_of_page_bid_micros": metrics.get("lowTopOfPageBidMicros"),
            "high_top_of_page_bid_micros": metrics.get("highTopOfPageBidMicros"),
            "metric_precision": "reported" if metrics else "unavailable",
        })
    checks = [check("google_ads.keyword_ideas", "VERIFIED" if state == "VERIFIED" and ideas else ("EMPTY" if state == "VERIFIED" else state), f"{summary}; {len(ideas)} ideas returned")]
    overall = "VERIFIED" if state == "VERIFIED" and bool(ideas) else ("INCOMPLETE" if state == "VERIFIED" else state)
    result = envelope("google_ads", {"customer_id": customer_id, "market": market, "language": language, "network": network, "seed_type": seed_type, "seed": seed}, {"customer_id": customer_id, "market": market, "language": language, "network": network}, overall, checks, ["Competition metrics describe paid advertising; no organic difficulty was inferred."])
    result["data"] = {"ideas": ideas}
    write_json(output, result)
    return 0 if overall == "VERIFIED" else exit_code or EXIT_INCOMPLETE


def bing_status(config_path: str, output: str) -> int:
    config = read_config(config_path)
    provider = provider_config(config, "bing")
    site = provider["site_url"]
    api_key_env = provider.get("api_key_env")
    api_key = os.environ.get(api_key_env or "")
    token: str | None = None
    if api_key:
        query = urllib.parse.urlencode({"apikey": api_key})
        url = "https://ssl.bing.com/webmaster/api.svc/json/GetUserSites?" + query
    else:
        token = get_access_token(provider)
        url = "https://ssl.bing.com/webmaster/api.svc/json/GetUserSites"
    status, payload = json_api(url, token=token)
    state, summary, exit_code = classify_provider_status(status, payload)
    raw_sites = []
    if isinstance(payload, dict):
        raw_sites = payload.get("d") or payload.get("sites") or payload.get("Sites") or []
    if isinstance(raw_sites, dict):
        raw_sites = raw_sites.get("results") or []
    site_values = []
    for item in raw_sites if isinstance(raw_sites, list) else []:
        value = item.get("Url") or item.get("url") if isinstance(item, dict) else str(item)
        if value:
            site_values.append(str(value))
    match = any(value.rstrip("/") == site.rstrip("/") for value in site_values)
    checks = [check("bing.access", "VERIFIED" if state == "VERIFIED" else state, summary)]
    if state == "VERIFIED":
        checks.append(check("bing.site", "VERIFIED" if match else "FAILED", "Configured site is accessible" if match else "Configured site was not returned", [site] if match else []))
    overall = "VERIFIED" if all(item["status"] == "VERIFIED" for item in checks) else ("UNAUTHORIZED" if state == "UNAUTHORIZED" else "INCOMPLETE")
    write_json(output, envelope("bing_webmaster", {"site": site}, {"site": site if match else None}, overall, checks, ["Sitemap acceptance and query visibility require separate Bing UI or endpoint verification."]))
    return 0 if overall == "VERIFIED" else exit_code or EXIT_INCOMPLETE


NORMALIZED_FIELDS = [
    "source_provider", "source_account_or_property", "retrieved_at", "window_start", "window_end",
    "market", "language", "device", "query", "page", "metric_name", "metric_value",
    "metric_precision", "source_row_id", "notes",
]


def input_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    value = load_json(path)
    if isinstance(value, dict):
        for key in ("rows", "data", "results", "ideas"):
            if isinstance(value.get(key), list):
                value = value[key]
                break
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise SeoStackError("Normalized input must be CSV or a JSON row array/envelope")
    return value


def normalize(provider: str, input_path: str, metadata_path: str, output: str) -> int:
    metadata = load_json(metadata_path)
    if not isinstance(metadata, dict):
        raise SeoStackError("Normalization metadata must be an object")
    column_map = metadata.get("column_map", {})
    if not isinstance(column_map, dict):
        raise SeoStackError("normalization metadata column_map must be an object")
    unsafe_columns = [str(value) for value in column_map.values() if SECRET_KEY.search(str(value))]
    if unsafe_columns:
        raise SeoStackError("Refusing to normalize credential-like source columns: " + ", ".join(sorted(unsafe_columns)))
    source = Path(input_path).expanduser().resolve()
    if not source.is_file():
        raise SeoStackError(f"Normalization input does not exist: {source}")
    rows = input_rows(source)
    normalized = []
    for index, row in enumerate(rows, 1):
        target: dict[str, Any] = {}
        for field in NORMALIZED_FIELDS:
            source_field = column_map.get(field)
            if source_field is not None:
                target[field] = row.get(source_field, "")
            elif field in metadata:
                target[field] = metadata[field]
            else:
                target[field] = ""
        target["source_provider"] = provider
        target["source_row_id"] = target["source_row_id"] or str(index)
        normalized.append(redact(target))
    target_path = safe_output_path(output)
    with target_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=NORMALIZED_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(normalized)
    return 0


def validate_setup_status(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["status root must be an object"]
    required = {"schema_version", "slug", "generated_at", "canonical_origin", "overall_status", "requirements", "credential_sources", "artifact_paths"}
    missing = required - set(value)
    if missing:
        errors.append(f"missing fields: {', '.join(sorted(missing))}")
    unknown = set(value) - required
    if unknown:
        errors.append(f"unknown fields: {', '.join(sorted(unknown))}")
    if value.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(value.get("slug", ""))):
        errors.append("slug must be kebab-case")
    try:
        validate_https_url(str(value.get("canonical_origin", "")), "canonical_origin")
    except SeoStackError as exc:
        errors.append(str(exc))
    try:
        datetime.fromisoformat(str(value.get("generated_at", "")).replace("Z", "+00:00"))
    except ValueError:
        errors.append("generated_at must be an ISO 8601 date-time")
    if value.get("overall_status") not in {"VERIFIED", "INCOMPLETE"}:
        errors.append("overall_status must be VERIFIED or INCOMPLETE")
    requirements = value.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        errors.append("requirements must be a non-empty array")
        return errors
    groups = {"production_identity", "crawl_index", "ga4", "google_search_console", "google_ads_keyword_planner", "bing_webmaster", "documentation"}
    sources = {"repository", "live_http", "api", "computer_use", "user_evidence", "manual_test"}
    requirement_fields = {"id", "group", "required", "status", "summary", "evidence", "verified_at", "source", "user_action", "not_applicable_reason"}
    seen: set[str] = set()
    for index, item in enumerate(requirements):
        prefix = f"requirements[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing_item = requirement_fields - set(item)
        unknown_item = set(item) - requirement_fields
        if missing_item:
            errors.append(f"{prefix} missing fields: {', '.join(sorted(missing_item))}")
        if unknown_item:
            errors.append(f"{prefix} unknown fields: {', '.join(sorted(unknown_item))}")
        item_id = item.get("id")
        if not isinstance(item_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]+", item_id):
            errors.append(f"{prefix}.id is invalid")
        elif item_id in seen:
            errors.append(f"{prefix}.id is duplicated")
        else:
            seen.add(item_id)
        status = item.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix}.status is invalid")
        if item.get("group") not in groups:
            errors.append(f"{prefix}.group is invalid")
        if item.get("source") not in sources:
            errors.append(f"{prefix}.source is invalid")
        if not isinstance(item.get("required"), bool):
            errors.append(f"{prefix}.required must be boolean")
        if not isinstance(item.get("summary"), str) or not item.get("summary", "").strip():
            errors.append(f"{prefix}.summary must be non-empty")
        if not isinstance(item.get("evidence"), list) or not all(isinstance(entry, str) for entry in item.get("evidence", [])):
            errors.append(f"{prefix}.evidence must be a string array")
        if status == "VERIFIED" and (not item.get("evidence") or not item.get("verified_at")):
            errors.append(f"{prefix} VERIFIED requires evidence and verified_at")
        if status == "NOT_APPLICABLE" and not item.get("not_applicable_reason"):
            errors.append(f"{prefix} NOT_APPLICABLE requires not_applicable_reason")
        if status == "AWAITING_USER_ACTION" and not item.get("user_action"):
            errors.append(f"{prefix} AWAITING_USER_ACTION requires user_action")
    if value.get("overall_status") == "VERIFIED":
        incomplete = [item.get("id") for item in requirements if item.get("status") not in {"VERIFIED", "NOT_APPLICABLE"}]
        if incomplete:
            errors.append("overall VERIFIED is invalid while requirements remain incomplete: " + ", ".join(str(item) for item in incomplete))
    credential_sources = value.get("credential_sources")
    if not isinstance(credential_sources, list):
        errors.append("credential_sources must be an array")
    else:
        for index, source in enumerate(credential_sources):
            if not isinstance(source, dict) or set(source) != {"provider", "kind", "present"}:
                errors.append(f"credential_sources[{index}] must contain only provider, kind, and present")
            elif not isinstance(source.get("provider"), str) or not isinstance(source.get("kind"), str) or not isinstance(source.get("present"), bool):
                errors.append(f"credential_sources[{index}] has invalid field types")
    artifact_paths = value.get("artifact_paths")
    if not isinstance(artifact_paths, dict) or not all(isinstance(key, str) and isinstance(path, str) and path for key, path in artifact_paths.items()):
        errors.append("artifact_paths must map string keys to non-empty string paths")
    return errors


def verify(config_path: str | None, status_path: str | None, output: str | None) -> int:
    if status_path:
        status = load_json(status_path)
        errors = validate_setup_status(status)
        result = {"schema_version": SCHEMA_VERSION, "validated_at": utc_now(), "status": "VALID" if not errors else "INVALID", "errors": errors, "redactions_applied": True}
        if output:
            write_json(output, result)
        sys.stdout.write(canonical_json(result))
        if errors:
            return EXIT_INCOMPLETE
        return 0 if status.get("overall_status") == "VERIFIED" else EXIT_INCOMPLETE
    if not config_path or not output:
        raise SeoStackError("verify requires either --status, or both --config and --output")
    config = read_config(config_path)
    slug_host = urllib.parse.urlsplit(config["canonical_origin"]).hostname or "seo-site"
    slug = re.sub(r"[^a-z0-9]+", "-", slug_host.lower()).strip("-")
    now = utc_now()
    requirements = []

    def req(item_id: str, group: str, status: str, summary: str, source: str, evidence: list[str] | None = None, user_action: str | None = None) -> None:
        requirements.append({"id": item_id, "group": group, "required": True, "status": status, "summary": summary, "evidence": evidence or [], "verified_at": now if status == "VERIFIED" else None, "source": source, "user_action": user_action, "not_applicable_reason": None})

    try:
        temp_inventory = str(safe_output_path(output).with_suffix(".inventory.json"))
        inventory_code = inventory(config["canonical_origin"], temp_inventory)
        inv = load_json(temp_inventory)
        req("production.canonical_origin", "production_identity", "VERIFIED" if inventory_code == 0 else "FAILED", "Live canonical origin inventory", "live_http", [temp_inventory])
        req("crawl.robots", "crawl_index", "VERIFIED" if inv.get("data", {}).get("robots", {}).get("status") == 200 else "FAILED", "Live robots.txt fetch", "live_http", [temp_inventory])
        sitemap_items = inv.get("data", {}).get("sitemaps", [])
        sitemap_ok = bool(sitemap_items) and all(item.get("status") == 200 for item in sitemap_items)
        req("crawl.sitemap", "crawl_index", "VERIFIED" if sitemap_ok else "FAILED", "Live sitemap parse", "live_http", [temp_inventory])
    except SeoStackError as exc:
        req("production.canonical_origin", "production_identity", "FAILED", str(exc), "live_http")
        req("crawl.robots", "crawl_index", "FAILED", "Inventory did not complete", "live_http")
        req("crawl.sitemap", "crawl_index", "FAILED", "Inventory did not complete", "live_http")
    provider_rows = [
        ("ga4.access", "ga4", "ga4", "Verify GA4 property, stream, consent behavior, and observed test event."),
        ("gsc.access", "google_search_console", "search_console", "Verify Search Console access and submitted live sitemap."),
        ("ads.keyword_planner", "google_ads_keyword_planner", "google_ads", "Run one harmless Keyword Planner sample without creating a campaign."),
        ("bing.access", "bing_webmaster", "bing", "Verify Bing site access and accepted live sitemap."),
    ]
    credentials = []
    for item_id, group, provider_name, action in provider_rows:
        provider = config["providers"].get(provider_name)
        if not provider:
            req(item_id, group, "BLOCKED", f"{provider_name} is not configured", "repository")
            credentials.append({"provider": provider_name, "kind": "unconfigured", "present": False})
            continue
        present, source = credential_presence(provider)
        credentials.append({"provider": provider_name, "kind": source, "present": present})
        req(item_id, group, "AWAITING_USER_ACTION", "Automated verification requires a provider-specific status command plus manual live evidence.", "manual_test", user_action=action)
    req("documentation.setup", "documentation", "AWAITING_USER_ACTION", "Canonical project SEO setup documentation has not been supplied to this command.", "repository", user_action="Create and review the canonical project SEO setup document, then incorporate it into the final status artifact.")
    status = {"schema_version": SCHEMA_VERSION, "slug": slug, "generated_at": now, "canonical_origin": config["canonical_origin"], "overall_status": "INCOMPLETE", "requirements": requirements, "credential_sources": credentials, "artifact_paths": {"verification_output": str(Path(output).absolute())}}
    write_json(output, status)
    return EXIT_INCOMPLETE


def authorize_apply(plan_revision: str | None, plan_digest: str | None, approved_revision: str, approved_digest: str) -> None:
    if not plan_revision or not plan_digest:
        raise SeoStackError("Mutation refused: exact plan revision and digest are required", EXIT_MUTATION_REFUSED)
    if plan_revision != approved_revision or plan_digest.lower() != approved_digest.lower():
        raise SeoStackError("Mutation refused: plan revision or digest does not match approved proof", EXIT_MUTATION_REFUSED)
    if not re.fullmatch(r"[0-9a-fA-F]{64}", plan_digest):
        raise SeoStackError("Mutation refused: plan digest must be a SHA-256 hex digest", EXIT_MUTATION_REFUSED)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="seo-stack", description="Read-only SEO setup evidence collector")
    parser.add_argument("--version", action="version", version=f"seo-stack {VERSION} (schema {SCHEMA_VERSION})")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor_parser = commands.add_parser("doctor")
    doctor_parser.add_argument("--config", required=True)
    doctor_parser.add_argument("--json")

    inventory_parser = commands.add_parser("inventory")
    inventory_parser.add_argument("--site", required=True)
    inventory_parser.add_argument("--output", required=True)

    verify_parser = commands.add_parser("verify")
    verify_parser.add_argument("--config")
    verify_parser.add_argument("--status")
    verify_parser.add_argument("--output")

    analytics_parser = commands.add_parser("analytics")
    analytics_commands = analytics_parser.add_subparsers(dest="analytics_command", required=True)
    analytics_status_parser = analytics_commands.add_parser("status")
    analytics_status_parser.add_argument("--config", required=True)
    analytics_status_parser.add_argument("--output", required=True)

    sc_parser = commands.add_parser("search-console")
    sc_commands = sc_parser.add_subparsers(dest="search_console_command", required=True)
    sc_status = sc_commands.add_parser("status")
    sc_status.add_argument("--config", required=True)
    sc_status.add_argument("--output", required=True)
    sc_inspect = sc_commands.add_parser("inspect")
    sc_inspect.add_argument("--config", required=True)
    sc_inspect.add_argument("--url", required=True)
    sc_inspect.add_argument("--output", required=True)

    ads_parser = commands.add_parser("ads")
    ads_commands = ads_parser.add_subparsers(dest="ads_command", required=True)
    ads_kw = ads_commands.add_parser("keywords")
    ads_kw.add_argument("--config", required=True)
    ads_kw.add_argument("--seed", required=True)
    ads_kw.add_argument("--seed-type", choices=("keyword", "url", "site"), default="keyword")
    ads_kw.add_argument("--market", required=True)
    ads_kw.add_argument("--language", required=True)
    ads_kw.add_argument("--network", choices=("GOOGLE_SEARCH", "GOOGLE_SEARCH_AND_PARTNERS"), default="GOOGLE_SEARCH")
    ads_kw.add_argument("--output", required=True)

    bing_parser = commands.add_parser("bing")
    bing_commands = bing_parser.add_subparsers(dest="bing_command", required=True)
    bing_status_parser = bing_commands.add_parser("status")
    bing_status_parser.add_argument("--config", required=True)
    bing_status_parser.add_argument("--output", required=True)

    normalize_parser = commands.add_parser("normalize")
    normalize_parser.add_argument("--provider", choices=("gsc", "google-ads", "bing", "ga4"), required=True)
    normalize_parser.add_argument("--input", required=True)
    normalize_parser.add_argument("--metadata", required=True)
    normalize_parser.add_argument("--output", required=True)
    return parser


def run(args: argparse.Namespace) -> int:
    if args.command == "doctor":
        return doctor(args.config, args.json)
    if args.command == "inventory":
        return inventory(args.site, args.output)
    if args.command == "verify":
        return verify(args.config, args.status, args.output)
    if args.command == "analytics":
        return analytics_status(args.config, args.output)
    if args.command == "search-console" and args.search_console_command == "status":
        return search_console_status(args.config, args.output)
    if args.command == "search-console":
        return search_console_inspect(args.config, args.url, args.output)
    if args.command == "ads":
        return ads_keywords(args.config, args.seed, args.market, args.language, args.network, args.seed_type, args.output)
    if args.command == "bing":
        return bing_status(args.config, args.output)
    if args.command == "normalize":
        return normalize(args.provider, args.input, args.metadata, args.output)
    raise SeoStackError("Unsupported command")


def main(argv: list[str] | None = None) -> int:
    try:
        return run(build_parser().parse_args(argv))
    except SeoStackError as exc:
        sys.stderr.write(canonical_json({"status": "ERROR", "message": str(exc), "redactions_applied": True}))
        return exc.exit_code
    except Exception as exc:  # Defensive redaction boundary; traceback is intentionally suppressed.
        sys.stderr.write(canonical_json({"status": "ERROR", "message": f"Unexpected failure: {redact_text(str(exc))}", "redactions_applied": True}))
        return EXIT_NETWORK


if __name__ == "__main__":
    raise SystemExit(main())
