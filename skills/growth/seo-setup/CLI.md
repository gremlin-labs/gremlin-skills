# `seo-stack` CLI contract

`seo-setup` canonically owns the reusable `seo-stack` CLI and machine-readable schemas. The CLI removes repetitive evidence collection and normalization; it does not replace user approval, official provider documentation, signed-in computer use, or human judgment.

Bundled schema files:

- `schemas/seo-stack-config.schema.json` — secret-free site and provider configuration.
- `schemas/seo-provider-evidence.schema.json` — normalized provider command receipts.
- `schemas/seo-setup-status.schema.json` — integrated Setup completion contract consumed downstream.

## Portability

- Implement as a dependency-light Python 3 command with standard-library-only offline functions.
- Keep optional provider adapters isolated. If a required OAuth/provider library is unavailable, fail with an exact installation or UI fallback instruction; never alter the target application's dependencies.
- Run from the installed `seo-setup` package. Do not copy the CLI into the target repository.
- Read non-secret project configuration from an explicit JSON file or flags. Read credentials only from standard runtime sources or named environment variables.
- Never emit credential values, authorization headers, cookies, raw HTML, or unredacted provider bodies.

## Discovery by downstream skills

1. Ask the host skill registry for `seo-setup` and resolve its package root.
2. If the host has no registry, resolve `../seo-setup/` as a sibling of the current skill.
3. Confirm the CLI version and supported schema version.
4. Use it when compatible.
5. If unavailable, follow the downstream skill's documented UI/API and manual-normalization fallback. Do not silently skip evidence.

## Read-only default

All commands are read-only unless both conditions hold:

1. the user approved the exact `SETUP-PLAN.md` revision containing the action; and
2. the caller passes an explicit apply flag plus the plan revision/digest.

The CLI rejects mutation without both values. It never infers approval from a prior successful command.

## Command surface

```text
seo-stack --version
seo-stack doctor --config {path} [--json {path}]
seo-stack inventory --site {url} --output {path}
seo-stack verify --config {path} --output {path}
seo-stack verify --status {path} [--output {path}]
seo-stack analytics status --config {path} --output {path}
seo-stack search-console status --config {path} --output {path}
seo-stack search-console inspect --config {path} --url {url} --output {path}
seo-stack ads keywords --config {path} --seed {value} --market {id} --language {id} --output {path}
seo-stack bing status --config {path} --output {path}
seo-stack normalize --provider {gsc|google-ads|bing|ga4} --input {path} --metadata {path} --output {path}
```

Setup-only apply operations may be added behind the approval gate for narrowly defined actions such as adding a verified Search Console site or submitting the already-approved sitemap. DNS changes, terms acceptance, account ownership, billing, campaign creation, and consent decisions remain outside generic CLI mutation.

Invoke the bundled command as `python3 {seo-setup-root}/scripts/seo_stack.py ...` when no host-level `seo-stack` launcher is installed. `verify --config` produces an honest incomplete baseline for evidence that still needs provider-specific or human verification; `verify --status` validates the final integrated human-plus-machine status and returns exit code `0` only when it is structurally valid and overall `VERIFIED`.

## `doctor`

Checks:

- Python/runtime compatibility and CLI/schema versions;
- configuration syntax and required non-secret fields;
- presence—not value—of named credential sources;
- optional provider dependencies and executables;
- canonical origin syntax and network reachability when requested;
- output directory safety and redaction rules.

Exit codes:

- `0`: all requested prerequisites present.
- `2`: configuration or invocation error.
- `3`: required credential source absent.
- `4`: provider/network unavailable.
- `5`: evidence incomplete.
- `6`: mutation refused because approval proof is missing or stale.

## `inventory`

Collects bounded live evidence from the canonical origin:

- redirect chain and final HTTPS origin;
- status, content type, title, meta description, canonical, robots directives, and selected structured-data types;
- `robots.txt` status/content digest and declared sitemaps;
- sitemap/index status, URL counts, sampled URL status/canonical/index directives, and cross-origin/redirect/error leakage;
- explicit limits, sampling method, retrieval time, and failures.

Do not persist raw page bodies by default. Store hashes and extracted fields. Bound downloads, redirects, sitemap expansion, concurrency, and timeouts.

## Provider status commands

Provider adapters return the shared evidence envelope:

```json
{
  "schema_version": 1,
  "provider": "google_search_console",
  "retrieved_at": "2026-08-04T20:15:00Z",
  "requested_scope": {
    "site": "sc-domain:example.com"
  },
  "actual_scope": {
    "site": "sc-domain:example.com"
  },
  "status": "VERIFIED",
  "checks": [],
  "warnings": [],
  "redactions_applied": true
}
```

Provider-specific rows and bounded live-site inventory fields live under the optional `data` object so the shared envelope remains schema-valid.

Commands must distinguish authentication, authorization, no-data, quota, invalid target, unavailable API, and network failure. An empty new property is not automatically an authorization failure.

## Keyword ideas

`ads keywords` is used by `seo-foundation`, not by Setup beyond one harmless access proof. It requires explicit market, language, network, seed type, seed, and retrieval date. Output distinguishes:

- average monthly searches or reported range;
- paid-ad competition and competition index;
- high/low top-of-page bid when returned;
- requested and actual targeting;
- exact, rounded, ranged, withheld, or unavailable metric precision;
- seed provenance and source URL when applicable.

It never invents organic difficulty.

## Normalized export contract

`normalize` converts user-approved exports without erasing source semantics. Every row includes:

```text
source_provider
source_account_or_property
retrieved_at
window_start
window_end
market
language
device
query
page
metric_name
metric_value
metric_precision
source_row_id
notes
```

Google, Bing, Ads, and Analytics rows remain distinguishable. Do not join different windows automatically. Downstream skills perform explicit compatible-scope comparisons.

## Configuration

Example secret-free configuration:

```json
{
  "schema_version": 1,
  "canonical_origin": "https://example.com",
  "providers": {
    "ga4": {
      "property_id": "123456789",
      "web_stream_id": "987654321",
      "credential_source": "named_environment",
      "access_token_env": "SEO_GOOGLE_OAUTH_ACCESS_TOKEN"
    },
    "search_console": {
      "site_url": "sc-domain:example.com",
      "credential_source": "named_environment",
      "access_token_env": "SEO_GOOGLE_OAUTH_ACCESS_TOKEN"
    },
    "google_ads": {
      "customer_id": "1234567890",
      "login_customer_id": "0987654321",
      "credential_source": "named_environment",
      "access_token_env": "SEO_GOOGLE_OAUTH_ACCESS_TOKEN",
      "developer_token_env": "SEO_GOOGLE_ADS_DEVELOPER_TOKEN",
      "api_version": "v25"
    },
    "bing": {
      "site_url": "https://example.com/",
      "credential_source": "named_environment",
      "api_key_env": "SEO_BING_WEBMASTER_API_KEY"
    }
  }
}
```

IDs may be documented only when non-secret and operationally useful. Environment-variable names are safe; values are not.

## Redaction

Redact case-insensitively:

- authorization, cookie, token, secret, password, credential, API-key, and developer-token fields;
- OAuth codes, refresh/access tokens, JWT-like values, cookies, and URL query secrets;
- raw provider error bodies that may echo requests.

Tests use fake credentials and assert the fake values never appear in stdout, stderr, JSON, Markdown, tracebacks, or fixtures.

## Current endpoint references

Recheck these official sources before live use because API versions and provider interfaces change:

- [Google Analytics Admin API](https://developers.google.com/analytics/devguides/config/admin/v1)
- [Google Search Console API](https://developers.google.com/webmaster-tools/v1/api_reference_index)
- [Google Ads Keyword Ideas](https://developers.google.com/google-ads/api/docs/keyword-planning/generate-keyword-ideas) and [version lifecycle](https://developers.google.com/google-ads/api/docs/sunset-dates)
- [Bing Webmaster `GetUserSites`](https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.getusersites)

## Test contract

Required automated coverage:

- valid/invalid config and schema versions;
- safe path handling and bounded network behavior;
- redirect, robots, sitemap, canonical, noindex, malformed XML, timeout, and partial-fetch fixtures;
- unavailable credentials and optional dependencies;
- authentication vs authorization vs empty-data provider responses;
- source/window-preserving normalization;
- redaction from success, error, traceback, and debug paths;
- read-only defaults and mutation refusal without exact plan approval proof;
- stale/mismatched plan digest refusal;
- deterministic JSON and Markdown output.

Run the CLI against local HTTP fixtures. Live-provider tests are opt-in, read-only, sanitized, and never required for repository unit tests.
