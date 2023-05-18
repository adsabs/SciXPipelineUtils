[![Python CI actions](https://github.com/tjacovich/SciXPipelineUtils/actions/workflows/python_actions.yml/badge.svg)](https://github.com/tjacovich/SciXPipelineUtils/actions/workflows/python_actions.yml) [![Coverage Status](https://coveralls.io/repos/github/tjacovich/SciXPipelineUtils/badge.svg?branch=main)](https://coveralls.io/github/tjacovich/SciXPipelineUtils?branch=main)

# Installation and Usage
Any release can be installed and used by running one of the following:
```bash
#Pull a specific release
pip install git+https://github.com/tjacovich/SciXPipelineUtils.git@vX.Y.Z
#Install branch
pip install git+https://github.com/tjacovich/SciXPipelineUtils.git@$BRANCH_NAME
```

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
