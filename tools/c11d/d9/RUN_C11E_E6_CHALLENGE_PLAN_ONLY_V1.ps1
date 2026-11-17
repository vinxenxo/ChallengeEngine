[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,
    [string]$PythonExe = ''
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)

if ([string]::IsNullOrWhiteSpace($PythonExe)) {
    $Candidate = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
    if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
        $PythonExe = $Candidate
    } else {
        $Command = Get-Command -Name 'py.exe' -ErrorAction SilentlyContinue
        if ($null -ne $Command) {
            $PythonExe = $Command.Source
        }
    }
}

if ([string]::IsNullOrWhiteSpace($PythonExe)) {
    throw 'Python 3.13 executable was not found. Pass -PythonExe explicitly.'
}

$PythonIsPyLauncher = ([System.IO.Path]::GetFileName($PythonExe).ToLowerInvariant() -eq 'py.exe')
if (-not $PythonIsPyLauncher -and -not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python executable missing: $PythonExe"
}

if ($PythonIsPyLauncher) {
    $VersionText = & $PythonExe -3.13 -c 'import sys; print(chr(46).join(map(str, sys.version_info[:3])))'
} else {
    $VersionText = & $PythonExe -c 'import sys; print(chr(46).join(map(str, sys.version_info[:3])))'
}
$VersionExit = $LASTEXITCODE
if ($VersionExit -ne 0) {
    throw "Python version probe failed: $VersionExit"
}
if ([string]$VersionText -notmatch '^3\.13\.') {
    throw "Python 3.13 required; found: $VersionText"
}
Write-Host "E6_CHALLENGE_PYTHON_VERSION=$VersionText"

$ToolRoot = Join-Path $ProjectRoot 'tools\c11d\d9'
$Tests = Join-Path $ToolRoot 'test_c11e_e6_challenge_plan_only_v1.py'
$Audit = Join-Path $ToolRoot 'c11e_e6_challenge_plan_only_v1.py'

foreach ($Path in @($Tests, $Audit)) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "E6 Challenge plan-only component missing: $Path"
    }
}

$env:C11E_PROJECT_ROOT = $ProjectRoot
$env:PYTHONDONTWRITEBYTECODE = '1'

Write-Host 'E6_CHALLENGE_PLAN_ONLY_STAGE=FOCUSED_TESTS'
if ($PythonIsPyLauncher) {
    & $PythonExe -3.13 $Tests
} else {
    & $PythonExe $Tests
}
$TestExit = $LASTEXITCODE
if ($TestExit -ne 0) {
    throw "E6 Challenge plan-only focused tests failed: $TestExit"
}

Write-Host 'E6_CHALLENGE_PLAN_ONLY_STAGE=LIVE_CHECKOUT_E1_AND_D_ENVELOPE_PLANNING'
if ($PythonIsPyLauncher) {
    & $PythonExe -3.13 $Audit --project-root $ProjectRoot
} else {
    & $PythonExe $Audit --project-root $ProjectRoot
}
$AuditExit = $LASTEXITCODE
if ($AuditExit -ne 0) {
    throw "E6 Challenge plan-only audit failed closed: $AuditExit"
}

Write-Host 'E6_CHALLENGE_PLAN_ONLY_RUNNER=PASS_PLAN_ONLY_EXECUTION_HELD'
Write-Host 'GODOT_INVOKED=FALSE'
Write-Host 'FFMPEG_INVOKED=FALSE'
Write-Host 'FFPROBE_INVOKED=FALSE'
Write-Host 'AUDIO_GENERATED=FALSE'
Write-Host 'MEDIA_CREATED=FALSE'
Write-Host 'NEW_BATCH_ID_CONSUMED=FALSE'
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
