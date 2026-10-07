#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'production_matrix_coverage_validator.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_2'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D7.2 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

$before = Get-TreeSnapshot -Root $repoRoot
Write-Host (('[OK] Mutation guard baseline captured: {0} worktree files.' -f $before.files))

& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D7.2 coverage validator run 1 failed.' }

$expectedNames = @(
    'd7_2_coverage_matrix.json',
    'd7_2_constraint_validation.json',
    'd7_2_negative_tests.json',
    'd7_2_validation_receipt.json'
)

$run1 = @{}
foreach ($name in $expectedNames) {
    $path = Join-Path $outputDirectory $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('Missing D7.2 evidence file: {0}' -f $name) }
    $run1[$name] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$unexpected = @(Get-ChildItem -LiteralPath $outputDirectory -Force | Where-Object { $_.Name -notin $expectedNames })
if ($unexpected.Count -ne 0) {
    throw ('Unexpected files under D7.2 evidence directory: {0}' -f (($unexpected | Select-Object -ExpandProperty Name) -join ', '))
}

& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D7.2 coverage validator run 2 failed.' }

$run2 = @{}
foreach ($name in $expectedNames) {
    $path = Join-Path $outputDirectory $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('Missing D7.2 evidence file after run 2: {0}' -f $name) }
    $run2[$name] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}

foreach ($name in $expectedNames) {
    if ($run1[$name] -ne $run2[$name]) { throw ('D7.2 evidence is not deterministic: {0}' -f $name) }
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $before.files, $before.sha256, $after.files, $after.sha256)
}

$receipt = Get-Content -LiteralPath (Join-Path $outputDirectory 'd7_2_validation_receipt.json') -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') {
    throw 'D7.2 did not finish PASS/CLOSED.'
}

Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d7/d7_2/ evidence may change.'
Write-Host '[OK] Four D7.2 evidence files present and exactly scoped.'
Write-Host '[OK] Two runs produced identical evidence files and SHA-256 values.'
Write-Host (('[OK] Matrix authority={0}; challenges={1}; delivery profiles={2}; modes={3}; core cases={4}.' -f $receipt.matrix_authority, $receipt.challenge_count, $receipt.delivery_profile_count, $receipt.mode_count, $receipt.core_cases))
Write-Host (('[OK] Coverage complete={0}; negative tests={1}; pass={2}; catalog authority={3}.' -f $receipt.coverage_complete, $receipt.negative_cases, $receipt.negative_tests_pass, $receipt.catalog_authority))
Write-Host (('[OK] master_seed={0}; derivation_runtime_activation={1}; runtime authority={2}; production execution={3}.' -f $receipt.master_seed, $receipt.derivation_runtime_activation, $receipt.runtime_authority, $receipt.production_execution))
Write-Host '=================================================='
Write-Host ' C11-D D7.2 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D7.3 - Canonical Catalog Builder'
