from __future__ import annotations

import csv
import importlib.util
import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).parents[1] / "seo_stack.py"
SPEC = importlib.util.spec_from_file_location("seo_stack", MODULE_PATH)
assert SPEC and SPEC.loader
seo_stack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(seo_stack)


class FixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        port = self.server.server_port
        routes = {
            "/": (200, "text/html", b'<html><head><title>Fixture</title><meta name="description" content="Test site"><link rel="canonical" href="PLACEHOLDER/"><script type="application/ld+json">{"@type":"WebSite"}</script></head></html>'),
            "/robots.txt": (200, "text/plain", b"User-agent: *\nSitemap: PLACEHOLDER/sitemap.xml\n"),
            "/sitemap.xml": (200, "application/xml", b'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>PLACEHOLDER/</loc></url></urlset>'),
            "/malformed.xml": (200, "application/xml", b"<urlset><url>"),
            "/redirect": (301, "text/plain", b""),
        }
        status, content_type, payload = routes.get(self.path, (404, "text/plain", b"missing"))
        if self.path == "/redirect":
            self.send_response(status)
            self.send_header("Location", f"http://127.0.0.1:{port}/")
            self.end_headers()
            return
        origin = f"http://127.0.0.1:{port}"
        payload = payload.replace(b"PLACEHOLDER", origin.encode())
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):  # noqa: A002
        return


class SeoStackTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_json(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def valid_config(self):
        return {
            "schema_version": 1,
            "canonical_origin": "https://example.com",
            "providers": {
                "ga4": {"property_id": "123", "web_stream_id": "456", "credential_source": "named_environment", "access_token_env": "SEO_GOOGLE_TOKEN"},
                "search_console": {"site_url": "sc-domain:example.com", "credential_source": "named_environment", "access_token_env": "SEO_GOOGLE_TOKEN"},
                "google_ads": {"customer_id": "1234567890", "credential_source": "named_environment", "access_token_env": "SEO_GOOGLE_TOKEN", "developer_token_env": "SEO_ADS_DEV_TOKEN", "api_version": "v25"},
                "bing": {"site_url": "https://example.com/", "credential_source": "named_environment", "api_key_env": "SEO_BING_KEY"},
            },
        }

    def test_valid_and_invalid_config(self):
        config = self.valid_config()
        self.assertEqual([], seo_stack.validate_config(config))
        config["schema_version"] = 2
        config["providers"]["ga4"]["access_token_env"] = "not-safe"
        errors = seo_stack.validate_config(config)
        self.assertTrue(any("schema_version" in item for item in errors))
        self.assertTrue(any("uppercase" in item for item in errors))

    def test_doctor_reports_presence_not_values_and_redacts(self):
        config_path = self.write_json("config.json", self.valid_config())
        output = self.root / "doctor.json"
        fake = "fake-super-secret-access-token"
        with mock.patch.dict(os.environ, {"SEO_GOOGLE_TOKEN": fake, "SEO_ADS_DEV_TOKEN": "fake-dev", "SEO_BING_KEY": "fake-bing"}, clear=True):
            code = seo_stack.doctor(str(config_path), str(output))
        rendered = output.read_text(encoding="utf-8")
        self.assertEqual(0, code)
        self.assertNotIn(fake, rendered)
        self.assertNotIn("fake-dev", rendered)

    def test_redaction_covers_headers_query_tokens_and_jwt(self):
        jwt = "eyJabcdefghij.abcdefghijklmnop.abcdefghijklmnop"
        value = {"Authorization": "Bearer fake-access-token", "url": f"https://x.test/?api_key=fake-key&code=fake-code", "nested": jwt}
        rendered = seo_stack.canonical_json(value)
        for secret in ("fake-access-token", "fake-key", "fake-code", jwt):
            self.assertNotIn(secret, rendered)

    def test_safe_output_rejects_symlink(self):
        real = self.root / "real.json"
        real.write_text("{}", encoding="utf-8")
        link = self.root / "link.json"
        link.symlink_to(real)
        with self.assertRaises(seo_stack.SeoStackError):
            seo_stack.write_json(link, {"safe": True})

    def test_inventory_uses_bounded_local_fixture_and_extracts_fields(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            origin = f"http://127.0.0.1:{server.server_port}/"
            output = self.root / "inventory.json"
            code = seo_stack.inventory(origin, str(output))
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(seo_stack.EXIT_INCOMPLETE, code)  # Local fixture is intentionally HTTP.
            self.assertEqual("Fixture", data["data"]["home"]["title"])
            self.assertEqual(["WebSite"], data["data"]["home"]["structured_data_types"])
            self.assertEqual(1, data["data"]["sitemap_url_count"])
            self.assertEqual(seo_stack.DEFAULT_SAMPLE_SIZE, data["data"]["limits"]["sample_size"])
            self.assertNotIn("<html", output.read_text(encoding="utf-8"))
        finally:
            server.shutdown()
            server.server_close()

    def test_malformed_sitemap_is_classified(self):
        with self.assertRaises(seo_stack.SeoStackError) as caught:
            seo_stack.parse_sitemap(b"<urlset><url>")
        self.assertEqual(seo_stack.EXIT_INCOMPLETE, caught.exception.exit_code)

    def test_normalize_preserves_provider_window_and_source_row(self):
        source = self.root / "source.csv"
        source.write_text("term,clicks\nred shoes,9\n", encoding="utf-8")
        metadata = self.write_json("metadata.json", {
            "source_account_or_property": "sc-domain:example.com",
            "retrieved_at": "2026-08-04T20:00:00Z",
            "window_start": "2026-07-01",
            "window_end": "2026-07-31",
            "market": "US",
            "language": "en",
            "device": "ALL",
            "metric_name": "clicks",
            "metric_precision": "exact",
            "column_map": {"query": "term", "metric_value": "clicks"},
        })
        output = self.root / "normalized.csv"
        self.assertEqual(0, seo_stack.normalize("gsc", str(source), str(metadata), str(output)))
        with output.open(encoding="utf-8") as handle:
            row = next(csv.DictReader(handle))
        self.assertEqual("gsc", row["source_provider"])
        self.assertEqual("2026-07-01", row["window_start"])
        self.assertEqual("1", row["source_row_id"])
        self.assertEqual("9", row["metric_value"])

    def test_normalize_rejects_secret_source_column(self):
        source = self.root / "source.csv"
        source.write_text("access_token\nfake-secret\n", encoding="utf-8")
        metadata = self.write_json("metadata.json", {"column_map": {"notes": "access_token"}})
        with self.assertRaises(seo_stack.SeoStackError):
            seo_stack.normalize("ga4", str(source), str(metadata), str(self.root / "out.csv"))

    def test_status_validation_rejects_false_verified(self):
        status = {
            "schema_version": 1,
            "slug": "example-seo",
            "generated_at": "2026-08-04T20:00:00Z",
            "canonical_origin": "https://example.com",
            "overall_status": "VERIFIED",
            "requirements": [{"id": "ga4.event", "group": "ga4", "required": True, "status": "AWAITING_USER_ACTION", "summary": "Need event", "evidence": [], "verified_at": None, "source": "manual_test", "user_action": "Observe event", "not_applicable_reason": None}],
            "credential_sources": [],
            "artifact_paths": {},
        }
        errors = seo_stack.validate_setup_status(status)
        self.assertTrue(any("overall VERIFIED" in item for item in errors))

    def test_status_validation_accepts_complete_verified_shape(self):
        status = {
            "schema_version": 1,
            "slug": "example-seo",
            "generated_at": "2026-08-04T20:00:00Z",
            "canonical_origin": "https://example.com",
            "overall_status": "VERIFIED",
            "requirements": [{"id": "crawl.sitemap", "group": "crawl_index", "required": True, "status": "VERIFIED", "summary": "Sitemap fetched", "evidence": ["sanitized receipt"], "verified_at": "2026-08-04T20:00:00Z", "source": "live_http", "user_action": None, "not_applicable_reason": None}],
            "credential_sources": [{"provider": "gsc", "kind": "named environment", "present": True}],
            "artifact_paths": {"audit": "agent-work/example-seo/seo-setup/AUDIT.md"},
        }
        self.assertEqual([], seo_stack.validate_setup_status(status))

    def test_apply_guard_requires_exact_revision_and_sha256(self):
        digest = "a" * 64
        seo_stack.authorize_apply("r2", digest, "r2", digest)
        for revision, supplied_digest in ((None, None), ("r1", digest), ("r2", "b" * 64), ("r2", "short")):
            with self.assertRaises(seo_stack.SeoStackError) as caught:
                seo_stack.authorize_apply(revision, supplied_digest, "r2", digest)
            self.assertEqual(seo_stack.EXIT_MUTATION_REFUSED, caught.exception.exit_code)

    def test_provider_status_distinguishes_auth_authorization_and_quota(self):
        self.assertEqual("UNAUTHORIZED", seo_stack.classify_provider_status(401, {})[0])
        self.assertEqual("UNAUTHORIZED", seo_stack.classify_provider_status(403, {})[0])
        self.assertEqual("UNAVAILABLE", seo_stack.classify_provider_status(429, {})[0])
        self.assertEqual("VERIFIED", seo_stack.classify_provider_status(200, {})[0])


if __name__ == "__main__":
    unittest.main()
