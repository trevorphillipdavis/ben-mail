param(
    [int]$Limit = 25,
    [string[]]$Account,
    [switch]$SkipRefresh,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not $SkipRefresh -and -not $Account) {
    .\scripts\refresh-all.ps1 -Limit $Limit
}

$argsList = @("-m", "aihub_email.cli", "today-review")
foreach ($accountId in $Account) {
    $argsList += @("--account", $accountId)
}
if ($Json) {
    $argsList += "--json"
}

.\scripts\python.ps1 @argsList
