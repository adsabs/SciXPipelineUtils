
# Setting Up a Development Environment
## Installing dependencies and hooks
This project uses `pyproject.toml` to install necessary dependencies and otherwise set up a working development environment. To set up a local working environment, simply run the following:
```bash
virtualenv .venv
source .venv/bin/activate
pip install .[dev]
pip install .
pre-commit install
pre-commit install --hook-type commit-msg
```

## Maintainers

First Last
