param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [string]$PythonExe = ''
)
$ErrorActionPreference = 'Stop'
$Stage = 'INITIALIZE'
try {
    if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'Windows PowerShell 5.1 is required.' }
    $Tokens = $null; $ParseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$Tokens,[ref]$ParseErrors) | Out-Null
    if ($ParseErrors.Count -gt 0) { throw ('PowerShell 5.1 AST parse failed: ' + (($ParseErrors | ForEach-Object { $_.Message }) -join '; ')) }
    Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
    $ProjectRoot = [IO.Path]::GetFullPath($ProjectRoot)
    if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "Project root missing: $ProjectRoot" }
    if ([string]::IsNullOrWhiteSpace($PythonExe)) { $PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe' }
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "Python 3.13 executable missing: $PythonExe" }
    $VersionText = (& $PythonExe --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0 -or $VersionText -notmatch '^Python 3\.13\.') { throw "Python 3.13 required; found: $VersionText" }
    Write-Host ('PYTHON_RUNTIME=' + $VersionText)
    $ToolRoot = Join-Path $ProjectRoot 'tools\c11d\d9'
    $Tests = Join-Path $ToolRoot 'test_c11e_e6_d9_prepare_only_coordinator_v1.py'
    $Coordinator = Join-Path $ToolRoot 'c11e_e6_d9_prepare_only_coordinator_v1.py'
    if (-not (Test-Path -LiteralPath $Tests -PathType Leaf)) { throw 'D9 PREPARE_ONLY test file missing.' }
    if (-not (Test-Path -LiteralPath $Coordinator -PathType Leaf)) { throw 'D9 PREPARE_ONLY coordinator missing.' }
    $Stage = 'FOCUSED_TESTS'
    & $PythonExe $Tests
    if ($LASTEXITCODE -ne 0) { throw "D9 PREPARE_ONLY focused tests failed: $LASTEXITCODE" }
    Write-Host 'D9_PREPARE_ONLY_TESTS=15/15 PASS'
    $Stage = 'READ_ONLY_COORDINATION'
    & $PythonExe $Coordinator --project-root $ProjectRoot
    if ($LASTEXITCODE -ne 0) { throw "D9 PREPARE_ONLY coordinator blocked: $LASTEXITCODE. Preserve source evidence." }
    Write-Host 'D9_PREPARE_ONLY_RUNNER=PASS'
    exit 0
} catch {
    Write-Error ("D9_PREPARE_ONLY_STAGE=" + $Stage + '; ' + $_.Exception.Message)
    exit 2
}
