[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [string]$PythonExe
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "ProjectRoot missing: $ProjectRoot" }
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw "Runner PowerShell AST failed: $($parseErrors[0].Message)" }

$ToolRoot = Join-Path $ProjectRoot 'tools\c11d\d9'
$TestScript = Join-Path $ToolRoot 'test_c11e_e6_smoke18_readonly_audit_v2.py'
$AuditScript = Join-Path $ToolRoot 'c11e_e6_smoke18_readonly_audit_v2.py'
if (-not (Test-Path -LiteralPath $TestScript -PathType Leaf)) { throw "E6 V2 focused tests missing: $TestScript" }
if (-not (Test-Path -LiteralPath $AuditScript -PathType Leaf)) { throw "E6 V2 audit module missing: $AuditScript" }

$ExpectedTestSha = 'cd43e8c746ff57b22fd71d770fd4627bdd2dfbcb104369166a93bd8770b9f1b4'
$ExpectedAuditSha = '21b2a309e4f8a619508e2a44f45b1b62d81783e0ec46a2db95d9725cd1248cad'
$ActualTestSha = Get-Sha256 $TestScript
$ActualAuditSha = Get-Sha256 $AuditScript
if ($ActualTestSha -ne $ExpectedTestSha) { throw "E6 V2 test module pin mismatch: $ActualTestSha" }
if ($ActualAuditSha -ne $ExpectedAuditSha) { throw "E6 V2 audit module pin mismatch: $ActualAuditSha" }

$PythonCommand = $null
$PythonPrefix = @()
if (-not [string]::IsNullOrWhiteSpace($PythonExe)) {
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "PythonExe missing: $PythonExe" }
    $PythonCommand = (Get-Item -LiteralPath $PythonExe).FullName
} else {
    $PyLauncher = Get-Command 'py.exe' -ErrorAction SilentlyContinue
    if ($null -ne $PyLauncher) {
        $PythonCommand = $PyLauncher.Source
        $PythonPrefix = @('-3.13')
    } else {
        $PythonCommandInfo = Get-Command 'python.exe' -ErrorAction SilentlyContinue
        if ($null -eq $PythonCommandInfo) { throw 'Python 3.13 not found. Pass -PythonExe <python.exe>.' }
        $PythonCommand = $PythonCommandInfo.Source
    }
}

$VersionText = & $PythonCommand @PythonPrefix -B -c 'import sys; print("{}.{}.{}".format(*sys.version_info[:3]))'
$VersionExit = $LASTEXITCODE
if ($VersionExit -ne 0) { throw "Python version probe failed: $VersionExit" }
if (-not ($VersionText -match '^3\.13\.[0-9]+$')) { throw "Python 3.13 required; found: $VersionText" }
Write-Host "E6_PYTHON_VERSION=$VersionText"
Write-Host 'E6_READONLY_AUDIT_STAGE=FOCUSED_TESTS'
& $PythonCommand @PythonPrefix -B $TestScript
$TestExit = $LASTEXITCODE
if ($TestExit -ne 0) { throw "E6 V2 focused tests failed: $TestExit" }
Write-Host 'E6_FOCUSED_TESTS=15/15_PASS'

Write-Host 'E6_READONLY_AUDIT_STAGE=SOURCE_AND_EVIDENCE_RECONCILIATION'
& $PythonCommand @PythonPrefix -B $AuditScript --project-root $ProjectRoot
$AuditExit = $LASTEXITCODE
if ($AuditExit -ne 0) { throw "E6 V2 read-only audit produced a fail-closed receipt: $AuditExit. Inspect E6_RECEIPT in output." }
Write-Host 'E6_READONLY_AUDIT_RUNNER=PASS_AUDIT_ONLY_EXECUTION_HELD'
Write-Host 'MEDIA_INVOKED=FALSE'
Write-Host 'NEW_BATCH_ID_CONSUMED=FALSE'
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
exit 0
