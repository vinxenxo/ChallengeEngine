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
[System.Management.Automation.Language.Parser]::ParseFile($RunnerPath, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw 'POWERSHELL_5_1_AST_PARSE=FAIL' }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw 'PROJECT_ROOT_MISSING' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_EXE_MISSING' }
$probe = & $PythonExe -c "import sys; print('.'.join(map(str,sys.version_info[:3])))" 2>&1
if ($LASTEXITCODE -ne 0 -or ([string]$probe).Trim() -ne '3.13.14') { throw 'PYTHON_RUNTIME_REQUIRED_3_13_14' }
Write-Host 'PYTHON_RUNTIME=Python 3.13.14'

$TestPath = Join-Path $ToolDir 'test_c11e_e6_reuse_evidence_hydration_v1.py'
$AuditPath = Join-Path $ToolDir 'c11e_e6_reuse_evidence_hydration_v1.py'
foreach ($p in @($TestPath,$AuditPath)) { if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "PAYLOAD_MISSING:$p" } }

& $PythonExe -m unittest discover -s $ToolDir -p 'test_c11e_e6_reuse_evidence_hydration_v1.py' -v
$testExit = $LASTEXITCODE
if ($testExit -ne 0) { throw "E6_REUSE_HYDRATION_TESTS_FAILED:$testExit" }
Write-Host 'E6_REUSE_HYDRATION_TESTS=18/18 PASS'

& $PythonExe $AuditPath --project-root $ProjectRoot
$auditExit = $LASTEXITCODE
if ($auditExit -ne 0) { throw "E6_REUSE_EVIDENCE_HYDRATION_BLOCKED:$auditExit; preserve the report and all source evidence." }
Write-Host 'E6_REUSE_EVIDENCE_HYDRATION_RUNNER=PASS'
exit 0
