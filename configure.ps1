# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Push-Location $scriptDir

Write-Host "Python ..."

# Install Python from .python-version
uv python install

# Create and activate virtual environment
uv venv --allow-existing .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install --editable .
uv pip install --group dev

Pop-Location