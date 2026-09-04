param(
    [string]$Account = "default"
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
python -m aihub_email.cli check-config --account $Account
