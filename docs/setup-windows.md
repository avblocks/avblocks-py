# Setup for Windows

> Setup instructions for Windows 10. All scripts are `PowerShell`.

## PowerShell

In PowerShell as Administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```

> This will allow you to execute PowerShell scripts locally on your machine.

## uv

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.9.26/install.ps1 | iex"
```

## Visual Studio Code

Download and install from [Visual Studio Code](https://code.visualstudio.com/download) site.

Open Visual Studio Code and press `Ctrl + Shift + p`. Select `Shell Command: Install 'code' command in PATH`.
