---
author: "Lewi Lie Uberg"
---

# Chocolatey

[Chocolatey](https://chocolatey.org/) is a machine-level package manager and installer for software packages, like Homebrew for macOS. It is an execution engine using the NuGet packaging infrastructure and Windows PowerShell to provide an automation tool for installing software on Windows machines, designed to simplify the process from the user perspective. The name is an extension on a pun of NuGet (from "nougat") "because everyone loves Chocolatey nougat".

## Install Chocolatey

[Installing](https://docs.chocolatey.org/en-us/choco/setup) chocolatey is done by opening a PowerShell window as an **administrator** and run the following command, which checks if the PowerShell profile exists, if not it creates it. Then it installs Chocolatey and refreshes the environment variables.

```powershell
Set-Location $env:USERPROFILE
If ( ! ( Test-Path $PROFILE ) ) { New-Item -Force -ItemType File -Path $PROFILE; Add-Content -Path $PROFILE -Encoding UTF8 -Value "# Powershell Profile"; }
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
RefreshEnv.cmd
```

## PowerShell Auto-Completion

Chocolatey provides PowerShell auto-completion for the `choco` command. To enable it, run the following command in PowerShell:

```powershell
echo "
# Chocolatey
`$ChocolateyProfile = ""`$env:ChocolateyInstall\helpers\chocolateyProfile.psm1""
if (Test-Path(`$ChocolateyProfile)) {
    Import-Module ""`$ChocolateyProfile""
}
" | Out-File $PROFILE -Encoding UTF8 -Append
```
