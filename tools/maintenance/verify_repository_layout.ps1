[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $root

$requiredDirs = @(
    '.continue/rules',
    'core',
    'challenges',
    'definitions',
    'profiles',
    'assets',
    'schemas',
    'tests',
    'tests/fixtures',
    'tools/c11freeze',
    'tools/qa/c7',
    'tools/qa/c10',
    'tools/qa/c11',
    'tools/maintenance',
    'docs',
    'docs/current/c11c',
    'docs/current/d',
    'docs/master-prompts',
    'docs/history/c11c/releases',
    'c11c-suite',
    'c11c-suite/c11c-test',
    'c11c-suite/c11c-catalog',
    'c11c-suite/c11c-config',
    'c11c-suite/c11c-maintenance',
    'c11c-suite/c11c-producer'
)

$requiredFiles = @(
    'project.godot',
    'README.md',
    'AGENTS.md',
    '.gitignore',
    'GeneradorMaestro.gd',
    'build_factory.py',
    'release_gate.py',
    'schemas/challenge_schema.json',
    'tests/run_all.py',
    'FULL_ACCEPTANCE_C11C_2.19.12.ps1',
    'MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md',
    'START_PROMPT_C11C_2.19_CONSOLIDATED.md',
    'C11C_2.19.12_CONTEXT_INDEX.md',
    'tools/maintenance/consolidate_c11c_2_19_documentation.ps1',
    'tools/maintenance/create_c11c_freeze_zip.ps1',
    'tools/maintenance/verify_repository_layout.ps1',
    'tools/qa/c11/run_c11c_complete_video_review.ps1',
    'tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1',
    'tools/qa/c11/verify_c11c_suite_launchers.ps1',
    'tests/C11CParallelReviewWorkerIsolationContractTest.gd',
    'tests/C11CVisualDrillReviewEnvelopePathContractTest.gd',
    'docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md',
    'docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md',
    'docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md',
    'docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md',
    'docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md',
    'docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md',
    'docs/current/d/D0_MIGRATION_MAP.md',
    'docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS.md',
    'docs/master-prompts/START_PROMPT_C11D_V1.0_STATELESS.md',
    'c11c-suite/self_test.py',
    'c11c-suite/c11c-producer/self_test.py',
    'c11c-suite/c11c-maintenance/main.py'
)

$obsoleteRoots = @('output','output_c7','output_batch_audit','qa','export','c9_c_generated_configs','c9_g_generated_configs','scripts','c11c-studio')

$missingDirs = @($requiredDirs | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_) -PathType Container) })
$missingFiles = @($requiredFiles | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf) })
$obsolete = @($obsoleteRoots | Where-Object { Test-Path -LiteralPath (Join-Path $root $_) })

if ($missingDirs.Count -gt 0) { Write-Host ('[LAYOUT] Missing directories: ' + ($missingDirs -join ', ')) -ForegroundColor Red }
if ($missingFiles.Count -gt 0) { Write-Host ('[LAYOUT] Missing files: ' + ($missingFiles -join ', ')) -ForegroundColor Red }
if ($obsolete.Count -gt 0) { Write-Host ('[LAYOUT] Obsolete roots present: ' + ($obsolete -join ', ')) -ForegroundColor Red }

if ($missingDirs.Count -gt 0 -or $missingFiles.Count -gt 0 -or $obsolete.Count -gt 0) {
    Write-Host '[C11C_LAYOUT] FAIL' -ForegroundColor Red
    exit 1
}

Write-Host '[C11C_LAYOUT] PASS - current C11-C 2.19.12 / C11-D handover layout is coherent.' -ForegroundColor Green
exit 0
