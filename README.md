[![Python CI actions](https://github.com/tjacovich/SciXPipelineUtils/actions/workflows/python_actions.yml/badge.svg)](https://github.com/tjacovich/SciXPipelineUtils/actions/workflows/python_actions.yml) [![Coverage Status](https://coveralls.io/repos/github/tjacovich/SciXPipelineUtils/badge.svg?branch=main)](https://coveralls.io/github/tjacovich/SciXPipelineUtils?branch=main)
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

Taylor Jacovich
