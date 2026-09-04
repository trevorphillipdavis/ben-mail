param(
    [Parameter(Mandatory = $true)]
    [string]$Account,

    [string]$GrantId,

    [string]$EnvFile = ".env"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
if ([System.IO.Path]::IsPathRooted($EnvFile)) {
    $envPath = $EnvFile
} else {
    $envPath = Join-Path $repoRoot $EnvFile
}

function Convert-ToGrantEnvName {
    param([string]$Name)

    if ($Name -eq "default") {
        return "NYLAS_GRANT_ID"
    }

    $normalized = $Name.Trim().ToUpperInvariant() -replace "[^A-Z0-9]+", "_"
    $normalized = $normalized.Trim("_")
    return "NYLAS_GRANT_ID_$normalized"
}

function Convert-ToAccountAlias {
    param([string]$Name)

    $normalized = $Name.Trim().ToLowerInvariant() -replace "[^a-z0-9]+", "_"
    $normalized = $normalized.Trim("_")
    if (-not $normalized) {
        return "default"
    }
    return $normalized
}

if (-not $GrantId) {
    $GrantId = Read-Host "Paste the Nylas Grant ID for account '$Account'"
}

if (-not $GrantId.Trim()) {
    throw "Grant ID is required."
}

if (-not (Test-Path -LiteralPath $envPath)) {
    $examplePath = Join-Path $repoRoot ".env.example"
    if (Test-Path -LiteralPath $examplePath) {
        Copy-Item -LiteralPath $examplePath -Destination $envPath
    } else {
        New-Item -ItemType File -Path $envPath | Out-Null
    }
}

$grantEnvName = Convert-ToGrantEnvName $Account
$accountAlias = Convert-ToAccountAlias $Account
$lines = @(Get-Content -LiteralPath $envPath)
$updated = $false

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^\s*$([regex]::Escape($grantEnvName))=") {
        $lines[$i] = "$grantEnvName=$GrantId"
        $updated = $true
        break
    }
}

if (-not $updated) {
    $lines += "$grantEnvName=$GrantId"
}

Set-Content -LiteralPath $envPath -Value $lines
Write-Output "Registered account '$accountAlias' using $grantEnvName."
Write-Output "From the repo root, run: .\scripts\check-config.ps1 -Account $accountAlias"
Write-Output "From this scripts folder, run: .\check-config.ps1 -Account $accountAlias"
