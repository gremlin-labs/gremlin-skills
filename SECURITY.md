# Security policy

## Reporting a vulnerability

Please do not disclose a suspected vulnerability, exposed credential, unsafe installer behavior, or path-traversal issue in a public issue.

Use GitHub's private **Report a vulnerability** form for this repository when it is available. If private vulnerability reporting is unavailable, contact the maintainers through a private channel listed on the Gremlin Labs GitHub organization profile. Include the affected skill or script, impact, reproduction steps, and any safe remediation you have identified. Do not include live credentials or sensitive user data.

Maintainers will acknowledge a private report, assess affected versions and distribution surfaces, and coordinate disclosure after a fix or mitigation is available.

## Supported versions

Until the first versioned public release, only the latest commit on the default branch is eligible for security fixes. A version support table will be added when stable releases begin.

## Scope

Security-sensitive surfaces include installer ownership and rollback, archive extraction, executable helper scripts, external provider actions, credential redaction, generated artifacts, and authority boundaries that could cause unintended source or external-system changes.
