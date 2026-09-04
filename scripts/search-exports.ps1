param(
    [string]$Query,
    [string]$Sender,
    [string]$Account = "default",
    [int]$Limit = 10,
    [switch]$Unread,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$argsList = @(
    "-m", "aihub_email.cli",
    "search-exports",
    "--account", $Account,
    "--limit", $Limit,
    "--ascii"
)

if ($Query) {
    $argsList += @("--query", $Query)
}

if ($Sender) {
    $argsList += @("--sender", $Sender)
}

if ($Unread) {
    $argsList += "--unread"
}

if ($Json) {
    $argsList += "--json"
}

python @argsList
