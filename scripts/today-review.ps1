param(
    [int]$Limit = 25,
    [switch]$SkipRefresh,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not $SkipRefresh) {
    .\scripts\refresh-all.ps1 -Limit $Limit
}

$argsList = @("-m", "aihub_email.cli", "today-review")
if ($Json) {
    $argsList += "--json"
}

python @argsList
