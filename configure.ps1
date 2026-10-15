# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Push-Location $scriptDir

Write-Host "Python ..."

# Select the Python build that matches the platform (CPU architecture),
# so the arm64 or x64 AVBlocks library can be loaded.
# OSArchitecture reports the native architecture even when PowerShell runs under x64 emulation on arm64.
$osArch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture
switch ($osArch) {
    'Arm64' { $pyArch = 'aarch64' }
    'X64'   { $pyArch = 'x86_64' }
    default { Write-Error "Unsupported architecture: $osArch"; Pop-Location; exit 1 }
}

# uv uses this architecture for Python requests that do not specify one
$env:UV_PYTHON_ARCH = $pyArch

# Remove the virtual environment if it was created with a Python for another architecture
if (Test-Path .\.venv\Scripts\python.exe) {
    $venvArch = (& .\.venv\Scripts\python.exe -c "import platform; print(platform.machine().lower())" 2>$null)
    switch ($venvArch) {
        { $_ -in 'arm64', 'aarch64' } { $venvArch = 'aarch64' }
        { $_ -in 'amd64', 'x86_64' }  { $venvArch = 'x86_64' }
    }
    if ($venvArch -ne $pyArch) {
        Write-Host "Removing .venv (architecture '$venvArch', expected '$pyArch')"
        Remove-Item -Recurse -Force .\.venv
    }
}

# Install Python from .python-version
uv python install

# Create and activate virtual environment
uv venv --allow-existing .venv --link-mode copy

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install --editable . --link-mode copy
uv pip install --group dev --link-mode copy

Pop-Location
