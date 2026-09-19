[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$root = (Get-Location).Path
$required = @(
 'docs/00_PROJECT_OVERVIEW.md',
 'docs/01_ARCHITECTURE.md',
 'docs/02_DATA_AND_CONTRACTS.md',
 'docs/03_PRESENTATION.md',
 'docs/04_PRODUCTION_AND_ARTIFACTS.md',
 'docs/05_TESTING_AND_REGRESSION.md',
 'docs/06_ROADMAP.md',
 'docs/checkpoints/C11_FREEZE.md',
 'docs/c11-freeze/13_ARCHITECTURE_MANIFESTO.md',
 'MASTER_HANDOVER_C11_FREEZE.md',
 'START_PROMPT_C11C_NEXT_WINDOW.md',
 'tools/c11freeze/finalize_c11_freeze.ps1'
)
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_)) })
if ($missing.Count -gt 0) { throw ('Missing freeze files: ' + ($missing -join ', ')) }
Write-Host '[C11FREEZE] Documentation/tool structure PASS'
