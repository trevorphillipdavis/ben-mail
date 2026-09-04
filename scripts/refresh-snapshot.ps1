param(
    [string]$Account = "default",
    [int]$Limit = 10,
    [int]$Top = 10,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$argsList = @(
    "-m", "aihub_email.cli",
    "refresh-snapshot",
    "--account", $Account,
    "--limit", $Limit,
    "--top", $Top,
    "--ascii"
)

if ($Json) {
    $argsList += "--json"
}

python @argsList
