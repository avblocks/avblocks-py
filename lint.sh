#!/usr/bin/env bash

# activate virtual environment
source .venv/bin/activate

pylint --verbose src samples
