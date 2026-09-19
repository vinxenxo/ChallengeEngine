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
 'docs/04_REPOSITORY_STRUCTURE.md',
 'docs/05_TESTING_AND_REGRESSION.md',
 'docs/06_PRODUCTION_AND_DISTRIBUTION.md',
 'docs/07_ROADMAP.md',
 'docs/checkpoints/C11_FREEZE.md',
 'docs/checkpoints/C11_B_REPOSITORY_ORGANIZATION.md',
 'docs/checkpoints/C11_B_REPOSITORY_CLEANUP_AUDIT.md',
 'docs/master-prompts/MASTER_HANDOVER_C11_B_REPOSITORY_ORGANIZATION.md',
 'docs/master-prompts/START_PROMPT_C11C_ART_DIRECTION.md',
 'docs/contracts/C11_ARCHITECTURE_MANIFESTO.md',
 'tools/c11freeze/finalize_c11_freeze.ps1',
 'tests/run_all.py',
 'tests/helpers/ArtifactPaths.gd',
 'schemas/challenge_schema.json'
)
$missing = @($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_)) })
if ($missing.Count -gt 0) { throw ('Missing repository files: ' + ($missing -join ', ')) }
$forbidden = @('output','output_c7','output_batch_audit','qa','export','c9_c_generated_configs','c9_g_generated_configs','scripts')
$present = @($forbidden | Where-Object { Test-Path -LiteralPath (Join-Path $root $_) })
if ($present.Count -gt 0) { throw ('Obsolete repository roots still present: ' + ($present -join ', ')) }
Write-Host '[C11FREEZE] Repository layout structure PASS'
