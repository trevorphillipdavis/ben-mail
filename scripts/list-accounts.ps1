param(
    [switch]$ReadyOnly
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$argsList = @("-m", "aihub_email.cli", "list-accounts")
if ($ReadyOnly) {
    $argsList += "--ready-only"
}

python @argsList
