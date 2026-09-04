param(
    [int]$Days = 30,
    [int]$Limit = 200,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$argsList = @(
    "-m", "aihub_email.cli",
    "review-inbox",
    "--account", "yahoo_trevorphillipdavis",
    "--days", $Days,
    "--limit", $Limit
)

if ($Json) {
    $argsList += "--json"
}

.\scripts\python.ps1 @argsList
