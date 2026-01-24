#!/usr/bin/env bash

# activate virtual environment
source .venv/bin/activate

# Ensure that the build tools are installed
uv pip install --upgrade pip setuptools wheel build twine

# Build the package
python -m build \
    --sdist \
    --wheel \
    --outdir dist \
    --config-setting=--use-pep517

python -m twine check dist/*
