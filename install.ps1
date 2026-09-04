param(
    [switch]$SkipPythonInstall,
    [switch]$SkipSetup,
    [switch]$ForceSkill
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

Write-Host "Installing AIHub Email Integration..."

.\scripts\bootstrap.ps1 -SkipInstall:$SkipPythonInstall
.\scripts\install-skill.ps1 -Force:$ForceSkill

if (-not $SkipSetup) {
    .\scripts\setup.ps1
}

Write-Host ""
Write-Host "Install complete."
Write-Host "The Codex skill name is: ben-mail"
