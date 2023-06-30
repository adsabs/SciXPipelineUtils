[![Python CI actions](https://github.com/adsabs/SciXPipelineUtils/actions/workflows/python_actions.yml/badge.svg)](https://github.com/adsabs/SciXPipelineUtils/actions/workflows/python_actions.yml) [![Coverage Status](https://coveralls.io/repos/github/adsabs/SciXPipelineUtils/badge.svg?branch=main)](https://coveralls.io/github/adsabs/SciXPipelineUtils?branch=main)

# Installation and Usage

## Installing in a python environment
Any release can be installed and used by running one of the following:

```bash
#Pull a specific release
pip install git+https://github.com/adsabs/SciXPipelineUtils.git@vX.Y.Z
#Install branch
pip install git+https://github.com/adsabs/SciXPipelineUtils.git@$BRANCH_NAME
```

## Usage
The `SciXPipelineUtils` package currently provides the following modules
```python
#Methods for interacting with S3 providers
SciXPipelineUtils.s3_methods
#Methods for loading configuration files and schemas
SciXPipelineUtils.utils
#Methods for Serializing and Deserializing AVRO messages using a specified schema
SciXPipelineUtils.avro_serializer
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

Taylor Jacovich and The ADS Team
