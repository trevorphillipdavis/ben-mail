param(
    [string]$CodexHome = $env:CODEX_HOME,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$skillName = "ben-mail"
$sourceSkill = Join-Path $repoRoot "skill\$skillName"

if (-not (Test-Path -LiteralPath $sourceSkill)) {
    throw "Skill source not found: $sourceSkill"
}

if (-not $CodexHome) {
    $CodexHome = Join-Path $HOME ".codex"
}

$skillsRoot = Join-Path $CodexHome "skills"
$targetSkill = Join-Path $skillsRoot $skillName
$legacySkill = Join-Path $skillsRoot "aihub-email"

if ((Test-Path -LiteralPath $targetSkill) -and -not $Force) {
    throw "Skill already exists at $targetSkill. Re-run with -Force to replace it."
}

New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null

if (Test-Path -LiteralPath $targetSkill) {
    Remove-Item -LiteralPath $targetSkill -Recurse -Force
}

Copy-Item -LiteralPath $sourceSkill -Destination $targetSkill -Recurse

if ((Test-Path -LiteralPath $legacySkill) -and ($legacySkill -ne $targetSkill)) {
    $legacySkillPath = Resolve-Path -LiteralPath $legacySkill
    $skillsRootPath = Resolve-Path -LiteralPath $skillsRoot
    if ($legacySkillPath.Path.StartsWith($skillsRootPath.Path)) {
        Remove-Item -LiteralPath $legacySkillPath.Path -Recurse -Force
        Write-Host "Removed legacy Codex skill: aihub-email"
    }
}

$referencesDir = Join-Path $targetSkill "references"
New-Item -ItemType Directory -Path $referencesDir -Force | Out-Null

$installLocation = @(
    "# Install Location"
    ""
    "Run Ben Mail commands from this repo:"
    ""
    '```text'
    $repoRoot
    '```'
)

Set-Content -LiteralPath (Join-Path $referencesDir "install-location.md") -Value $installLocation

Write-Host "Installed Codex skill: $skillName"
Write-Host "Skill location: $targetSkill"
Write-Host "Repo location: $repoRoot"
