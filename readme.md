
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

