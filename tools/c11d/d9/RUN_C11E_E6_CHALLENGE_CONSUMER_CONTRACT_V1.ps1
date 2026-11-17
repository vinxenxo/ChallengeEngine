[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,
    [string]$PythonExe = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)

$ToolRoot = Join-Path $ProjectRoot 'tools\c11d\d9'
$AuditModule = Join-Path $ToolRoot 'c11e_e6_challenge_consumer_contract_v1.py'
$TestFile = Join-Path $ToolRoot 'test_c11e_e6_challenge_consumer_contract_v1.py'
$ExpectedModuleSha256 = 'b9511a153e213fefe07a308f3103b631623b54cf64007b54cd6b62d9fe979490'
$ExpectedTestSha256 = 'cbc7f9b5929c601c6d83be089ff88132e56e4a0a363775c4007223c17415ab2f'

if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw 'PROJECT_ROOT_MISSING' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "PYTHON_EXE_MISSING:$PythonExe" }
if (-not (Test-Path -LiteralPath $AuditModule -PathType Leaf)) { throw 'CONTRACT_AUDIT_MODULE_MISSING' }
if (-not (Test-Path -LiteralPath $TestFile -PathType Leaf)) { throw 'CONTRACT_TEST_FILE_MISSING' }

$ModuleSha = (Get-FileHash -LiteralPath $AuditModule -Algorithm SHA256).Hash.ToLowerInvariant()
$TestSha = (Get-FileHash -LiteralPath $TestFile -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ModuleSha -ne $ExpectedModuleSha256) { throw "CONTRACT_AUDIT_MODULE_SHA_MISMATCH:$ModuleSha" }
if ($TestSha -ne $ExpectedTestSha256) { throw "CONTRACT_TEST_FILE_SHA_MISMATCH:$TestSha" }

# Python probe intentionally contains no embedded quotes: safe for Windows PowerShell 5.1 native argument marshalling.
$VersionOutput = & $PythonExe -c 'import sys; print(chr(46).join(map(str, sys.version_info[:3])))'
$VersionExit = $LASTEXITCODE
if ($VersionExit -ne 0) { throw "PYTHON_VERSION_PROBE_FAILED:$VersionExit" }
$PythonVersion = ([string]$VersionOutput).Trim()
if (-not $PythonVersion.StartsWith('3.13.')) { throw "PYTHON_3_13_REQUIRED:$PythonVersion" }
Write-Host "E6_CHALLENGE_CONTRACT_PYTHON_VERSION=$PythonVersion"
Write-Host 'E6_CHALLENGE_CONTRACT_PYTHON_PROBE=PASS_PS51_SAFE'

$PreviousRoot = $env:C11E_PROJECT_ROOT
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$env:C11E_PROJECT_ROOT = $ProjectRoot
$env:PYTHONDONTWRITEBYTECODE = '1'
try {
    Push-Location $ToolRoot
    try {
        Write-Host 'E6_CHALLENGE_CONTRACT_STAGE=FOCUSED_TESTS'
        & $PythonExe $TestFile
        $TestExit = $LASTEXITCODE
        if ($TestExit -ne 0) { throw "FOCUSED_TESTS_FAILED:$TestExit" }
        Write-Host 'E6_CHALLENGE_CONTRACT_FOCUSED_TESTS=36/36_PASS'

        $RunId = 'E6CHCONTRACT_' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '_' + [Guid]::NewGuid().ToString('N').Substring(0, 8).ToUpperInvariant()
        Write-Host 'E6_CHALLENGE_CONTRACT_STAGE=STATIC_SOURCE_AND_PLAN_RECONCILIATION'
        & $PythonExe $AuditModule --project-root $ProjectRoot --run-id $RunId
        $AuditExit = $LASTEXITCODE
        if ($AuditExit -ne 0) { throw "STATIC_CONTRACT_AUDIT_FAILED:$AuditExit" }
    } finally {
        Pop-Location
    }
} finally {
    if ($null -eq $PreviousRoot) { Remove-Item Env:C11E_PROJECT_ROOT -ErrorAction SilentlyContinue } else { $env:C11E_PROJECT_ROOT = $PreviousRoot }
    if ($null -eq $PreviousNoBytecode) { Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue } else { $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode }
}

Write-Host 'E6_CHALLENGE_CONTRACT_RUNNER=PASS_STATIC_ONLY_EXECUTION_HELD'
Write-Host 'GODOT_INVOKED=FALSE'
Write-Host 'FFMPEG_INVOKED=FALSE'
Write-Host 'FFPROBE_INVOKED=FALSE'
Write-Host 'AUDIO_GENERATED=FALSE'
Write-Host 'MEDIA_CREATED=FALSE'
Write-Host 'NEW_BATCH_ID_CONSUMED=FALSE'
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
