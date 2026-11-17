[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$RunnerPath = [System.IO.Path]::GetFullPath($MyInvocation.MyCommand.Path)
$ToolDir = Split-Path -Parent $RunnerPath
$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)

$parseErrors = $null
$tokens = $null
[System.Management.Automation.Language.Parser]::ParseFile($RunnerPath,[ref]$tokens,[ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw 'POWERSHELL_5_1_AST_PARSE=FAIL' }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw 'PROJECT_ROOT_MISSING' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_EXE_MISSING' }
$probe = & $PythonExe -c "import sys; print('.'.join(map(str,sys.version_info[:3])))" 2>&1
if ($LASTEXITCODE -ne 0 -or ([string]$probe).Trim() -ne '3.13.14') { throw 'PYTHON_RUNTIME_REQUIRED_3_13_14' }
Write-Host 'PYTHON_RUNTIME=Python 3.13.14'

$TestPath = Join-Path $ToolDir 'test_c11e_e6_reuse_evidence_hydration_v2.py'
$AuditPath = Join-Path $ToolDir 'c11e_e6_reuse_evidence_hydration_v2.py'
foreach ($p in @($TestPath,$AuditPath)) { if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "PAYLOAD_MISSING:$p" } }

$testOutput = & $PythonExe -m unittest discover -s $ToolDir -p 'test_c11e_e6_reuse_evidence_hydration_v2.py' -v 2>&1
$testExit = $LASTEXITCODE
$testText = ($testOutput | Out-String)
$testOutput | ForEach-Object { Write-Host $_ }
if ($testExit -ne 0) { throw "E6_REUSE_HYDRATION_V2_TESTS_FAILED:$testExit" }
$testMatch = [regex]::Match($testText,'Ran\s+(\d+)\s+tests?')
if (-not $testMatch.Success -or [int]$testMatch.Groups[1].Value -ne 34) { throw 'E6_REUSE_HYDRATION_V2_TEST_COUNT_MISMATCH_EXPECTED_34' }
Write-Host 'E6_REUSE_HYDRATION_V2_TESTS=34/34 PASS'

& $PythonExe $AuditPath --project-root $ProjectRoot
$auditExit = $LASTEXITCODE
if ($auditExit -eq 0) {
    Write-Host 'E6_REUSE_EVIDENCE_HYDRATION_V2_RUNNER=PASS_EVIDENCE_HYDRATED_NOT_AUTHORIZED'
    exit 0
}
if ($auditExit -eq 2) {
    Write-Host 'E6_REUSE_EVIDENCE_HYDRATION_V2_RUNNER=PASS_REPORT_CREATED_WITH_BLOCKERS'
    Write-Host 'E6_REUSE_EVIDENCE_HYDRATION_V2_NEXT=REVIEW_REPORT_FAILURE_CATEGORIES; DO_NOT_WAIVE_SOURCE_PIN_DRIFT'
    exit 0
}
throw "E6_REUSE_EVIDENCE_HYDRATION_V2_AUDIT_INTERNAL_ERROR:$auditExit"
