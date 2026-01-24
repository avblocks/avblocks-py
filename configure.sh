#!/usr/bin/env bash

# get script dir
script_dir=$( cd `dirname ${BASH_SOURCE[0]}` >/dev/null 2>&1 ; pwd -P )

pushd $script_dir > /dev/null

echo "Python ..."

# Install Python from .python-version
uv python install

# create and activate virtual environment
uv venv --allow-existing .venv

# activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install --editable .
uv pip install --group dev

popd > /dev/null
