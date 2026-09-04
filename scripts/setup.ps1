param(
    [string]$EnvFile = ".env",
    [switch]$SkipValidation
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

if ([System.IO.Path]::IsPathRooted($EnvFile)) {
    $envPath = $EnvFile
} else {
    $envPath = Join-Path $repoRoot $EnvFile
}

function Read-RequiredValue {
    param(
        [string]$Prompt,
        [string]$CurrentValue = ""
    )

    if ($CurrentValue) {
        $value = Read-Host "$Prompt [press Enter to keep existing]"
        if (-not $value.Trim()) {
            return $CurrentValue
        }
        return $value.Trim()
    }

    do {
        $value = Read-Host $Prompt
    } while (-not $value.Trim())

    return $value.Trim()
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

function Read-EnvFile {
    param([string]$Path)

    $values = [ordered]@{}
    if (-not (Test-Path -LiteralPath $Path)) {
        return $values
    }

    foreach ($line in Get-Content -LiteralPath $Path) {
        if (-not $line.Trim() -or $line.Trim().StartsWith("#") -or $line -notmatch "=") {
            continue
        }
        $key, $value = $line.Split("=", 2)
        $values[$key.Trim()] = $value.Trim()
    }

    return $values
}

function Set-EnvValue {
    param(
        [string[]]$Lines,
        [string]$Key,
        [string]$Value
    )

    $updated = $false
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match "^\s*$([regex]::Escape($Key))=") {
            $Lines[$i] = "$Key=$Value"
            $updated = $true
            break
        }
    }

    if (-not $updated) {
        $Lines += "$Key=$Value"
    }

    return $Lines
}

if (-not (Test-Path -LiteralPath $envPath)) {
    $examplePath = Join-Path $repoRoot ".env.example"
    if (Test-Path -LiteralPath $examplePath) {
        Copy-Item -LiteralPath $examplePath -Destination $envPath
    } else {
        New-Item -ItemType File -Path $envPath | Out-Null
    }
}

$values = Read-EnvFile $envPath
$lines = @(Get-Content -LiteralPath $envPath)

Write-Host ""
Write-Host "AIHub Email Integration setup"
Write-Host "Values are saved locally to $envPath. Do not commit this file."
Write-Host ""

$apiKey = Read-RequiredValue "Paste your Nylas API key" $values["NYLAS_API_KEY"]
$apiUriCurrent = $values["NYLAS_API_URI"]
if (-not $apiUriCurrent) {
    $apiUriCurrent = "https://api.us.nylas.com"
}
$apiUri = Read-RequiredValue "Nylas API URI" $apiUriCurrent

$lines = Set-EnvValue $lines "NYLAS_API_KEY" $apiKey
$lines = Set-EnvValue $lines "NYLAS_API_URI" $apiUri
$lines = Set-EnvValue $lines "AIHUB_ENV" "local"

Write-Host ""
Write-Host "Add email accounts. Use simple aliases like gmail_personal, gmail_work, yahoo_personal."
Write-Host "Press Enter without an alias when you are done."
Write-Host ""

$addedAccounts = @()
while ($true) {
    $aliasInput = Read-Host "Account alias"
    if (-not $aliasInput.Trim()) {
        break
    }

    $accountAlias = Convert-ToAccountAlias $aliasInput
    $grantEnvName = Convert-ToGrantEnvName $accountAlias
    $currentGrant = $values[$grantEnvName]
    $grantId = Read-RequiredValue "Paste the Nylas Grant ID for '$accountAlias'" $currentGrant
    $lines = Set-EnvValue $lines $grantEnvName $grantId
    $values[$grantEnvName] = $grantId
    $addedAccounts += $accountAlias
    Write-Host "Registered $accountAlias as $grantEnvName."
    Write-Host ""
}

Set-Content -LiteralPath $envPath -Value $lines

Write-Host "Saved setup values."

if (-not $SkipValidation) {
    Write-Host ""
    Write-Host "Checking configured accounts..."
    .\scripts\python.ps1 -m aihub_email.cli list-accounts --ready-only

    foreach ($account in $addedAccounts) {
        .\scripts\python.ps1 -m aihub_email.cli check-config --account $account
    }
}

Write-Host ""
Write-Host "Next useful commands:"
Write-Host ".\scripts\list-accounts.ps1 -ReadyOnly"
Write-Host ".\scripts\today-review.ps1"
