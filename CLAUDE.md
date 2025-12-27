# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## When working I expect
- Be brutally honest don't be a yes man.
- If im wrong point it our bluntly.
- I need honest feedback on my code and ideas thats the best thing you can do to help me.
- Never use the phrases "You're absolutely right ..."
- ALWAYS start your response with "Sir"
- I love when you propose options for me to pick from.
- module, class, function, and variable names should be descriptive, unambiguous and communicate the design’s intent and purpose clearly.
- Use appropriate design patterns. Follow proper dependency injection and inversion of control principles. Ensure code is DRY (Don't Repeat Yourself).
- Write clean, maintainable, and well-documented code. Write doc strings for all modules, classes and functions. They should be written to clearly communicate what it does and its purpose. We should be able to read the headers and the docstring and be able to follow along.
- Write lots of debug logs.
- Don't do more than is tasked of you. Which means on extra functions then what is agreed upon. if you want to add extra functions or things thats not needed for the current task please ask.
- Never use emojis or they will set us both on fire
- Always code in small steps. Don't write too much without giving me a chance to look and or test it.

## Project Overview

AustinRent is a web scraping project that collects rental prices from apartment buildings on Rainey Street in Austin, TX. This is intentionally structured as an "org in a box" to practice production DevOps patterns in a monorepo (ORTRTA - "One Repo To Rule Them All").

**Key Components:**
- **scraper/**: Python web scraper using Crawlee that scrapes building rental data and saves to PostgreSQL
- **opentofu_repo/**: Infrastructure as Code for GCP resources (Cloud Run, Cloud SQL, Pub/Sub, Storage, etc.)
- Monorepo structure where folder names dictate app names and Cloud Run service names

## Development Commands

### Python/Scraper Development

```bash
# Install dependencies (using uv)
cd scraper/
uv sync

# Run the scraper locally
uv run python -m scraper

# Run tests
uv run pytest

# Run a single test
uv run pytest scraper/tests/test_html_handler.py

# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

### Pre-commit Hooks

Install TFLint and Trivy before using pre-commit hooks:

```bash
# Install TFLint
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# Install Trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin v0.58.1

# Install and run pre-commit
pre-commit install
pre-commit run --all-files
```

Pre-commit runs: autoflake, isort, black, flake8, mypy, terraform_fmt, terraform_tflint, terraform_trivy

### Database Operations

**Connect to Cloud SQL locally:**

```bash
./cloud-sql-proxy --address 0.0.0.0 --port 5432 austin-rent:us-central1:austin-rent-db
```

**Database migrations** are managed via Flyway in `scraper/db-migrations/` and run through GitHub Actions (workflow_dispatch).

**Database naming conventions:**
- Tables: snake_case (e.g., `scrape_responses`)
- Primary keys: `table_name_id`
- Follow [PostgreSQL conventions](https://gist.github.com/kyledcline/9b7e864b89c269beb2c34e55fb0903b0)

### Infrastructure (OpenTofu)

```bash
cd opentofu_repo/

# Initialize
tofu init

# Plan changes
tofu plan

# Apply changes
tofu apply
```

## Architecture

### Scraper Service Flow

1. **Entry point:** `scraper/__main__.py` starts a simple webserver (for Cloud Run health checks) and runs the main crawler
2. **Main crawler:** `scraper/main.py` uses Crawlee BeautifulSoupCrawler with a router-based architecture
3. **Buildings list:** Hardcoded in `scraper/buildings.py` as `Request` objects with labels ("JSON" or "HTML") and building IDs
4. **Routing:** `scraper/handlers/routes.py` routes requests based on label:
   - `json_handler`: Handles JSON API responses (e.g., Sightmap APIs)
   - `html_handler`: Handles HTML scraping (currently partially implemented)
   - `default_handler`: Logs unhandled requests
5. **Data flow:**
   - Scrape response → Validate → Save to `scraper-responses` GCS bucket
   - Save metadata to `scrape_responses` PostgreSQL table
   - Extract structured data → Save to `scrape_extraction` table

### Database Schema

- `buildings`: Building metadata (currently unused, hardcoded in code)
- `scrape_responses`: Raw scrape response metadata (scrape_page_id, building_id, request_url, saved_at)
- `scrape_extraction`: Extracted structured data (floor_plan_id, building_id, scrape_page_id, available, beds, sqft, rent)

All DAOs use SQLAlchemy async with asyncpg driver.

### Infrastructure Architecture (OpenTofu)

**Main resources (`opentofu_repo/main.tf`):**
- Shared Artifact Registry for Docker images
- Cloud SQL instance (PostgreSQL) defined in `cloud_sql.tf`
- Scraper module at `./scraper-module/`

**Scraper module (`opentofu_repo/scraper-module/`):**
- `compute.tf`: Cloud Run service, Cloud Scheduler cron job (12 PM UTC daily), service account with permissions
- `storage.tf`: GCS bucket for scrape responses
- `pubsub.tf`: Pub/Sub topics and subscriptions (for future extraction service)
- `database.tf`: Database and user provisioning

### Secret Management

Uses [age encryption](https://github.com/FiloSottile/age) for secrets:

1. Secrets are encrypted with public key: `age1phl53gymlk2rt5fwvdvyeds30w73slkgj8trs6c5nkdf43wzkd2s2mdfx0`
2. Stored encrypted in `scraper/configs/dev.yaml` or `scraper/configs/local.yaml`
3. Decrypted at runtime by `scraper/config/secret_manager.py`
4. Private key stored in GCP Secret Manager (`manual-private-key`)

**To create a new secret:**
```bash
echo "your-secret-value" | age -r $AR_PUBLIC_KEY | base64
# Add to configs/dev.yaml under 'secrets:' section
```

### Settings and Environment

`scraper/config/settings.py` loads configuration based on `ENVIRONMENT` env var:
- `LOCAL`: Uses local PostgreSQL connection
- `DEV`/`PROD`: Uses Cloud SQL Unix socket connection

## GitHub Actions

All workflows are **manually triggered** (workflow_dispatch) with app name selection to avoid rebuilding/deploying all apps on push.

**Available workflows:**
- `google-cloud-run-deploy.yaml`: Build Docker image, push to Artifact Registry, deploy to Cloud Run
- `flyway-migration.yaml`: Run Flyway migrations against Cloud SQL (creates backup first)
- `linter.yaml`: Runs super-linter

## Code Patterns

### Handler Pattern
Handlers in `scraper/handlers/` follow a consistent pattern:
- Validate incoming data
- Extract structured information
- Save via DAOs (Data Access Objects)
- Use structlog for structured logging

### DAO Pattern
Database access through DAOs in `scraper/db/*/`:
- `*_model.py`: SQLAlchemy models
- `*_dao.py`: Data access layer with async methods
- Base class: `scraper/db/base.py`

### Database Connection
- Connection management: `scraper/db/sql_connect.py`
- Uses Cloud SQL Python Connector for cloud environments
- Direct asyncpg connection for local development

## Important Notes

- Building list currently hardcoded in `buildings.py` (intentionally not database-driven to keep handler routing logic in code)
- Extraction service is currently embedded in the scraper; future plan is to separate it for reprocessing capability
- Cloud Run services require a webserver on port 8080 for health checks (see `utils/simple_webserver.py`)
- Python version: 3.12
- Database migrations are versioned with Flyway (V0, V1, V2, etc.)
