
# Website Security Auditor 🔒

A Django-based web application for comprehensive security auditing of websites.

## Features ✨

- **Website Reachability**: Verify website accessibility
- **SSL/TLS Validation**: Check certificate validity & expiration
- **Security Headers**: Audit HTTP security headers (HSTS, CSP, X-Frame-Options, etc.)
- **Robots.txt Verification**: Validate robots.txt configuration
- **Sitemap Analysis**: Check and validate XML sitemaps
- **Security Scoring**: Overall security rating

## Tech Stack

- Python 3.12+
- Django 6.0.7
- Bootstrap 5
- requests, cryptography, robots parser libraries

## Quick Start

### Prerequisites
```bash
python --version  # Should be 3.12+
```
---
### Project Structure

scanner/
├── services/          # Business logic
│   ├── audit.py      # Main orchestrator
│   ├── website.py    # Reachability checks
│   ├── ssl_check.py  # SSL validation
│   ├── headers.py    # Headers analysis
│   └── robots.py     # Robots.txt checks
├── views.py          # Request handlers
├── forms.py          # Django forms
└── urls.py           # URL routing

## Maintenance checks

Two workflows keep the project healthy:

| Workflow | When it runs | What it checks |
| --- | --- | --- |
| `python-app.yml` | every pull request / push to `development` | Ruff lint, Ruff format, pytest |
| `maintenance.yml` | every Friday 11:45 UTC, or by hand from the Actions tab | dependency upgrades, lockfile, CVEs, risky code |

`maintenance.yml` steps, with the command to reproduce them locally:

| Step | Command | What to do when it fails |
| --- | --- | --- |
| List available upgrades | `uv lock --upgrade --dry-run` | informational only, it never changes `uv.lock` |
| Lockfile in sync | `uv lock --check` | run `uv lock`, commit `uv.lock` |
| Known vulnerabilities | `uv run --with pip-audit pip-audit` | `uv lock --upgrade-package <name>`, then `uv sync` |
| Risky code patterns | `uv run bandit -r scanner securityaudit -x scanner/migrations -ll` | fix the reported line, or add `# nosec BXXX` with a reason |

### (Important) Upgrading dependencies

`uv sync --upgrade` is a local command, not a CI step: the runner is thrown away
after the job, so an upgrade there would never reach the repository. The
procedure is:

```bash
uv sync --upgrade            # upgrade everything to the newest allowed versions
uv run ruff check .          # lint
uv run pytest                # make sure nothing broke
git add uv.lock pyproject.toml && git commit -m "chore: upgrade dependencies"
```

`pyproject.toml` uses `>=` ranges while `uv.lock` pins the exact versions ` == for pins and >= not for pin`, so
CI installs with `uv sync --locked` and gets the versions that were tested.
Upgrade one package at a time with `uv lock --upgrade-package <name>` if a full
upgrade breaks something.

