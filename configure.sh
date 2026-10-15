#!/usr/bin/env bash

# get script dir
script_dir=$( cd `dirname ${BASH_SOURCE[0]}` >/dev/null 2>&1 ; pwd -P )

pushd $script_dir > /dev/null

echo "Python ..."

# Select the Python build that matches the platform (OS and CPU architecture),
# so the arm64 or x64 AVBlocks library can be loaded.
case "$(uname -s)" in
    Darwin) py_os=macos ;;
    Linux)  py_os=linux ;;
    *) echo "Unsupported OS: $(uname -s)" >&2; exit 1 ;;
esac

case "$(uname -m)" in
    arm64|aarch64) py_arch=aarch64 ;;
    x86_64|amd64)  py_arch=x86_64 ;;
    *) echo "Unsupported architecture: $(uname -m)" >&2; exit 1 ;;
esac

# Python version from .python-version
py_version=$(cat .python-version)
py_request="cpython-${py_version}-${py_os}-${py_arch}-none"

# Remove the virtual environment if it was created with a Python for another architecture
if [ -x .venv/bin/python ]; then
    venv_arch=$(.venv/bin/python -c "import platform; print(platform.machine().lower())" 2>/dev/null)
    case "$venv_arch" in
        arm64|aarch64) venv_arch=aarch64 ;;
        amd64) venv_arch=x86_64 ;;
    esac
    if [ "$venv_arch" != "$py_arch" ]; then
        echo "Removing .venv (architecture '$venv_arch', expected '$py_arch')"
        rm -rf .venv
    fi
fi

# Install Python for this platform
uv python install "$py_request"

# create and activate virtual environment
uv venv --python "$py_request" --allow-existing .venv

# activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install --editable .
uv pip install --group dev

popd > /dev/null
