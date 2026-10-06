[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'full_d5_acceptance.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d5\d5_5'
$outputNames = @(
    'd5_5_acceptance_matrix.json',
    'd5_5_acceptance_summary.json',
    'd5_5_acceptance_receipt.json'
)

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotJson = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to compute repository snapshot.' }
    return ($snapshotJson | ConvertFrom-Json)
}

function Get-Sha256 {
    param([string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

Write-Host '=================================================='
Write-Host ' C11-D D5.5 - FULL D5 ACCEPTANCE'
Write-Host '=================================================='

$before = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} files.' -f $before.files)

Push-Location $repoRoot
try {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D5.5 acceptance harness returned a failure.' }
}
finally {
    Pop-Location
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.tree_sha256 -ne $after.tree_sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $before.files, $before.tree_sha256, $after.files, $after.tree_sha256)
}
Write-Host '[OK] Mutation guard PASS; only the three D5.5 output files are excluded.'

$matrixPath = Join-Path $outputDirectory 'd5_5_acceptance_matrix.json'
$summaryPath = Join-Path $outputDirectory 'd5_5_acceptance_summary.json'
$receiptPath = Join-Path $outputDirectory 'd5_5_acceptance_receipt.json'
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
$matrixSha = Get-Sha256 -Path $matrixPath
$summarySha = Get-Sha256 -Path $summaryPath
$receiptSha = Get-Sha256 -Path $receiptPath
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') {
    throw ('D5.5 did not close: result={0}, status={1}' -f $receipt.result, $receipt.status)
}

Write-Host '[OK] D5.0-D5.4 accepted: PASS.'
Write-Host ('[OK] Inventory: {0} identities / {1} locations / {2} edges.' -f $receipt.logical_identities, $receipt.physical_locations, $receipt.lineage_edges)
Write-Host ('[OK] Governance: {0} ORPHANED / {1} global candidates / D4.8 {2}.' -f $receipt.orphaned_governed_records, $receipt.global_candidates_outside_graph, $receipt.d4_8)
Write-Host ('[OK] Runtime authority={0}; production={1}; frozen C11-C={2}.' -f $receipt.runtime_authority, $receipt.production_execution, $receipt.frozen_c11c_preserved)
Write-Host ('[OK] D5.5 hashes: matrix={0}; summary={1}; receipt={2}' -f $matrixSha, $summarySha, $receiptSha)
Write-Host '=================================================='
Write-Host ' C11-D D5.5 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D6 - Seed Registry and Governance'
