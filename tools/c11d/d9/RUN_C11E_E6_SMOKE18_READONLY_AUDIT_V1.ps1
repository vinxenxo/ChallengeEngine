[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "ProjectRoot missing: $ProjectRoot" }
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw "Runner PowerShell AST failed: $($parseErrors[0].Message)" }
$TestScript = Join-Path $ProjectRoot 'tools\c11d\d9\test_c11e_e6_smoke18_readonly_audit_v1.py'
$AuditScript = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_smoke18_readonly_audit_v1.py'
if (-not (Test-Path -LiteralPath $TestScript -PathType Leaf)) { throw 'E6 focused tests missing.' }
if (-not (Test-Path -LiteralPath $AuditScript -PathType Leaf)) { throw 'E6 audit module missing.' }

Write-Host 'E6_READONLY_AUDIT_STAGE=FOCUSED_TESTS'
& py -3.13 $TestScript
$TestExit = $LASTEXITCODE
if ($TestExit -ne 0) { throw "E6 focused tests failed: $TestExit" }
Write-Host 'E6_FOCUSED_TESTS=10/10_PASS'

Write-Host 'E6_READONLY_AUDIT_STAGE=SOURCE_AND_EVIDENCE_RECONCILIATION'
& py -3.13 $AuditScript --project-root $ProjectRoot
$AuditExit = $LASTEXITCODE
if ($AuditExit -ne 0) { throw "E6 read-only audit failed closed: $AuditExit" }
Write-Host 'E6_READONLY_AUDIT_RUNNER=PASS_AUDIT_ONLY_EXECUTION_HELD'
Write-Host 'MEDIA_INVOKED=FALSE'
Write-Host 'NEW_BATCH_ID_CONSUMED=FALSE'
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
exit 0
