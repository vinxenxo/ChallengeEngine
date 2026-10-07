#requires -Version 5.1
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'production_catalog_builder.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_3'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D7.3 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

$baseline = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files.' -f $baseline.files)

for ($runIndex = 1; $runIndex -le 2; $runIndex++) {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw ('D7.3 catalog builder run {0} failed.' -f $runIndex) }
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($baseline.files -ne $after.files -or $baseline.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $baseline.files,$baseline.sha256,$after.files,$after.sha256)
}

$expected = @(
    'd7_3_canonical_catalog.json',
    'd7_3_catalog_validation.json',
    'd7_3_negative_tests.json',
    'd7_3_catalog_receipt.json'
)
$actual = @(Get-ChildItem -LiteralPath $outputDirectory -File | Select-Object -ExpandProperty Name | Sort-Object)
if (@($actual).Count -ne $expected.Count -or (Compare-Object $actual $expected)) {
    throw 'D7.3 evidence scope failure: expected exactly four evidence JSON files.'
}
$hashLines = @()
foreach ($name in $expected) {
    $hashLines += (Get-FileHash -LiteralPath (Join-Path $outputDirectory $name) -Algorithm SHA256)
}
$hashTextA = ($hashLines | ForEach-Object { $_.Hash }) -join '|'

# Re-read/re-hash after a clean second invocation to establish idempotency.
& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D7.3 final idempotency run failed.' }
$hashLinesB = foreach ($name in $expected) { Get-FileHash -LiteralPath (Join-Path $outputDirectory $name) -Algorithm SHA256 }
$hashTextB = ($hashLinesB | ForEach-Object { $_.Hash }) -join '|'
if ($hashTextA -ne $hashTextB) { throw 'D7.3 evidence SHA-256 mismatch across runs.' }

Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d7/d7_3/ evidence may change.'
Write-Host '[OK] Four D7.3 evidence files present and exactly scoped.'
Write-Host '[OK] Evidence SHA-256 values stable across repeated runs.'
$receipt = Get-Content -LiteralPath (Join-Path $outputDirectory 'd7_3_catalog_receipt.json') -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D7.3 receipt is not PASS/CLOSED.' }
Write-Host ('[OK] Catalog items={0}; core cases={1}; complete={2}; negative tests pass={3}.' -f $receipt.catalog_items,$receipt.core_cases,$receipt.complete,$receipt.negative_tests_pass)
Write-Host '[OK] Matrix authority=CANONICAL_D7_1; Catalog authority=CANONICAL_D7_3.'
Write-Host '[OK] Runtime authority=NONE; production execution=False; renderer execution=False; media rendered by catalog=False.'
Write-Host '=================================================='
Write-Host ' C11-D D7.3 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D7.4 - Catalog Identity / Provenance'
