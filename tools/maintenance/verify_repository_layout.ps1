[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $root

$requiredDirs = @(
    'core',
    'challenges',
    'definitions',
    'profiles',
    'assets',
    'assets/reference',
    'schemas',
    'tests',
    'tests/fixtures',
    'tests/fixtures/c7/challenges',
    'tests/fixtures/seeds',
    'tools/c11freeze',
    'tools/qa/c7',
    'tools/qa/c10',
    'tools/qa/c11',
    'tools/maintenance',
    'artifacts/production',
    'artifacts/qa',
    'artifacts/regression',
    'artifacts/tests',
    'artifacts/releases',
    'artifacts/releases/c11-b',
    'artifacts/legacy',
    'artifacts/scratch',
    'docs',
    'docs/contracts',
    'docs/operations',
    'docs/checkpoints',
    'docs/master-prompts',
    'docs/mechanics',
    'docs/history'
)

$requiredFiles = @(
    'project.godot',
    'README.md',
    'AGENTS.md',
    '.gitignore',
    'GeneradorMaestro.gd',
    'Main.tscn',
    'build_factory.py',
    'release_gate.py',
    'schemas/challenge_schema.json',
    'tests/run_all.py',
    'tests/helpers/ArtifactPaths.gd',
    'tests/fixtures/seeds/stress_v1.json',
    'tools/c11freeze/run_all.ps1',
    'tools/c11freeze/run_seed_stress.py',
    'tools/c11freeze/run_retrocompatibility.py',
    'tools/c11freeze/run_physical_export_suite.ps1',
    'tools/c11freeze/run_qa_video_matrix.ps1',
    'tools/maintenance/verify_repository_layout.ps1',
    'docs/00_PROJECT_OVERVIEW.md',
    'docs/01_ARCHITECTURE.md',
    'docs/02_DATA_AND_CONTRACTS.md',
    'docs/03_PRESENTATION.md',
    'docs/04_REPOSITORY_STRUCTURE.md',
    'docs/05_TESTING_AND_REGRESSION.md',
    'docs/06_PRODUCTION_AND_DISTRIBUTION.md',
    'docs/07_ROADMAP.md',
    'docs/operations/TEST_RUNBOOK.md',
    'docs/operations/ARTIFACT_POLICY.md',
    'docs/operations/REPOSITORY_ORGANIZATION.md',
    'docs/operations/GOVERNANCE.md',
    'docs/checkpoints/C11_FREEZE.md',
    'docs/checkpoints/C11_B_REPOSITORY_ORGANIZATION.md',
    'docs/checkpoints/C11_B_REPOSITORY_CLEANUP_AUDIT.md',
    'docs/master-prompts/MASTER_HANDOVER_C11_B_REPOSITORY_ORGANIZATION.md',
    'docs/master-prompts/START_PROMPT_C11C_ART_DIRECTION.md',
    'docs/contracts/C11_ARCHITECTURE_MANIFESTO.md'
)

$forbiddenRoots = @(
    'output',
    'output_c7',
    'output_batch_audit',
    'qa',
    'export',
    'c9_c_generated_configs',
    'c9_g_generated_configs',
    'scripts'
)

$missingDirs = @($requiredDirs | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_) -PathType Container) })
$missingFiles = @($requiredFiles | Where-Object { -not (Test-Path -LiteralPath (Join-Path $root $_) -PathType Leaf) })
$obsolete = @($forbiddenRoots | Where-Object { Test-Path -LiteralPath (Join-Path $root $_) })

if ($missingDirs.Count -gt 0) {
    Write-Host ('[LAYOUT] Missing directories: ' + ($missingDirs -join ', ')) -ForegroundColor Red
}
if ($missingFiles.Count -gt 0) {
    Write-Host ('[LAYOUT] Missing files: ' + ($missingFiles -join ', ')) -ForegroundColor Red
}
if ($obsolete.Count -gt 0) {
    Write-Host ('[LAYOUT] Obsolete roots present: ' + ($obsolete -join ', ')) -ForegroundColor Red
}

if ($missingDirs.Count -or $missingFiles.Count -or $obsolete.Count) {
    Write-Host '[C11B_LAYOUT] FAIL' -ForegroundColor Red
    exit 1
}

Write-Host '[C11B_LAYOUT] PASS' -ForegroundColor Green
