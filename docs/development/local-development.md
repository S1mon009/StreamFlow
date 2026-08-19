# Local development

This guide describes how to prepare a development environment for StreamFlow.

## Clone the repository

```bash
git clone https://github.com/S1mon009/StreamFlow.git
cd StreamFlow
```

## Create a virtual environment

```bash
python -m venv .venv
```

Activate it according to your operating system.

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run StreamFlow

```bash
python main.py
```

## Run tests

The repository contains a `tests/` directory.

If pytest is configured for the project:

```bash
pytest
```

## Development principles

When adding functionality:

* keep related functionality in the appropriate package;
* avoid placing business logic directly in `main.py`;
* keep configuration centralized;
* use decorators for cross-cutting concerns;
* add tests for new behavior;
* update documentation when user-visible behavior changes.

## Code organization

A new feature should normally be placed according to its responsibility.

For example:

```text
Download functionality
    ↓
classes/

Configuration
    ↓
config/

Cross-cutting behavior
    ↓
decorators/

Reusable helpers
    ↓
utils/
```

## External dependencies

When introducing a new dependency, consider:

* whether it is necessary;
* whether an existing dependency already provides the functionality;
* how it affects installation;
* whether it is actively maintained.

Update `requirements.txt` when a runtime dependency is added.
