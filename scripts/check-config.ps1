param(
    [string]$Account = "default"
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
.\scripts\python.ps1 -m aihub_email.cli check-config --account $Account
