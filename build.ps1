# activate virtual environment
. .venv\Scripts\Activate.ps1

# Build the package
# Ensure that the build tools are installed
uv pip install --upgrade pip setuptools wheel build twine

python -m build `
    --sdist `
    --wheel `
    --outdir dist `
    --config-setting=--use-pep517

python -m twine check dist/*
