param(
    [int]$Limit = 10
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$accountsJson = .\scripts\python.ps1 -m aihub_email.cli list-accounts --ready-only --json | ConvertFrom-Json
$readyAccounts = @($accountsJson | Where-Object { $_.configured -eq $true })

if ($readyAccounts.Count -eq 0) {
    Write-Output "No configured accounts found."
    exit 1
}

foreach ($account in $readyAccounts) {
    Write-Output ""
    Write-Output "Refreshing $($account.account_id)"
    .\scripts\refresh-snapshot.ps1 -Account $account.account_id -Limit $Limit
}
