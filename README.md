# Playwright + Python UI Test Automation Framework

![Python](https://img.shields.io/badge/python-3.11-blue)
![Playwright](https://img.shields.io/badge/playwright-1.45+-green)
![pytest](https://img.shields.io/badge/pytest-7.x-orange)
![CI](https://github.com/nkosti/playwright_python/actions/workflows/ci.yml/badge.svg)

A showcase test automation framework built with **Playwright**, **pytest** and **pytest-bdd**.
It demonstrates how I structure UI + API test suites for real products: page objects, BDD
scenarios readable by non-developers, environment-aware configuration, encrypted credentials,
parallel execution and rich reporting.

## Highlights

- **Page Object Model** — every page is a small package (`pom.py` + `locators.py`) built on a
  shared `BasePOM`, so tests never touch raw selectors.
- **BDD with pytest-bdd** — Gherkin feature files paired with reusable step definitions;
  scenarios read like documentation.
- **Hybrid UI + API testing** — REST API clients (auth, users, organizations, roles) are used
  for fast test-data setup and teardown, keeping UI tests focused on what they verify.
- **DTO-driven test data** — JSON blueprints are deserialized into DTOs with sensible random
  defaults, so each test gets unique, isolated data.
- **Encrypted credentials** — passwords in environment configs are Fernet-encrypted and
  decrypted at runtime; no plain-text secrets in the repo.
- **Multi-environment support** — per-environment JSON configs selected with a single
  `ENV_NAME` variable.
- **Parallel execution** — pytest-xdist ready, including per-worker log files.
- **Reporting** — Allure and Cucumber-JSON reports, plus Playwright traces retained on failure
  for step-by-step debugging.
- **Quality gates** — git pre-commit hook and a GitHub Actions pipeline validating the suite on
  every push.

## Project structure

```
test/
├── conftest.py                 # fixtures: browser context, POM/API containers, login, test data
├── features/                   # BDD layer
│   ├── conftest.py             # shared steps (navigation, common assertions)
│   └── users/
│       ├── user_management.feature
│       └── step_definitions.py
├── domains/
│   ├── api_client/             # REST clients for data setup/teardown
│   ├── config/                 # environment configs + loader
│   ├── enum/                   # typed constants (filters, endpoints, severities)
│   ├── page_objects/           # POM packages (landing, authentication, users, organizations)
│   └── test_data/dto/          # JSON → DTO deserialization with random defaults
├── resources/                  # JSON test-data blueprints keyed by test id
└── utils/                      # helpers: random data, decryption, test-name parsing
```

## Getting started

Requires Python 3.11+ and [Poetry](https://python-poetry.org/).

```shell
poetry config virtualenvs.in-project true
poetry install
poetry run playwright install
sh setup-hooks.sh   # optional: install the git pre-commit hook
```

## Running tests

```shell
# whole suite
poetry run pytest

# in parallel
poetry run pytest -n 4

# by tag / keyword
poetry run pytest -k regression

# against a specific environment (default: test)
ENV_NAME=dev poetry run pytest
```

Environment configs live in `test/domains/config/environments/<env>.json` and define the base
URL and (encrypted) credentials per environment.

## Reporting

```shell
# Allure
poetry run pytest --alluredir allure-dir
allure serve allure-dir

# Cucumber-style JSON (CI integrations)
poetry run pytest --cucumber-json cucumber.json
```

Playwright traces are kept for failed tests (`--tracing=retain-on-failure`) and can be opened
with `playwright show-trace`.

## Design notes

- Fixtures compose two containers — `Context` (page objects) and `ApiContext` (API clients) —
  so a step definition asks for exactly one object and stays one line of intent.
- Test data files are resolved by test id parsed from the scenario name (`[TEST-1]` →
  `resources/test_data/TEST-1.json`), which keeps data next to the test without hardcoding
  paths in steps.
- API clients own authentication and expose a small CRUD core, so adding a new service client
  is a few lines of endpoints.
