param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PythonArgs
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
$pythonExe = "python"

if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
}

& $pythonExe @PythonArgs
exit $LASTEXITCODE
