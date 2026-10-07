#requires -Version 5.1
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'd7_5_full_acceptance_builder.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_5'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

# Prevent Python from creating/updating __pycache__ outside the D7.5 evidence scope.
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONHASHSEED = '0'

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D7.5 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

$baseline = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files outside d7_5 evidence.' -f $baseline.files)

for ($runIndex = 1; $runIndex -le 2; $runIndex++) {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw ('D7.5 full acceptance builder run {0} failed.' -f $runIndex) }
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($baseline.files -ne $after.files -or $baseline.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $baseline.files,$baseline.sha256,$after.files,$after.sha256)
}

$expected = @(
    'd7_5_full_acceptance.json',
    'd7_5_governance_validation.json',
    'd7_5_negative_tests.json',
    'd7_5_acceptance_receipt.json'
)
$actual = @(Get-ChildItem -LiteralPath $outputDirectory -File | Select-Object -ExpandProperty Name | Sort-Object)
if (@($actual).Count -ne $expected.Count -or (Compare-Object $actual $expected)) {
    throw 'D7.5 evidence scope failure: expected exactly four evidence JSON files.'
}

$hashesA = @()
foreach ($expectedName in $expected) {
    $hashesA += (Get-FileHash -LiteralPath (Join-Path $outputDirectory $expectedName) -Algorithm SHA256).Hash
}
$hashTextA = $hashesA -join '|'
& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D7.5 final idempotency run failed.' }
$hashesB = @()
foreach ($expectedName in $expected) {
    $hashesB += (Get-FileHash -LiteralPath (Join-Path $outputDirectory $expectedName) -Algorithm SHA256).Hash
}
$hashTextB = $hashesB -join '|'
if ($hashTextA -ne $hashTextB) { throw 'D7.5 evidence SHA-256 mismatch across runs.' }

$receipt = Get-Content -LiteralPath (Join-Path $outputDirectory 'd7_5_acceptance_receipt.json') -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D7.5 receipt is not PASS/CLOSED.' }
Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d7/d7_5/ evidence may change.'
Write-Host '[OK] Four D7.5 evidence files present and exactly scoped.'
Write-Host '[OK] Evidence SHA-256 values stable across repeated runs.'
Write-Host ('[OK] D7.0-D7.4 predecessors PASS/CLOSED; challenges={0}; matrix rows={1}; catalog items={2}; core cases={3}.' -f $receipt.challenge_count,$receipt.matrix_rows,$receipt.catalog_items,$receipt.core_cases)
Write-Host ('[OK] C11-C build_factory.py identity={0}; frozen SHA={1}.' -f $receipt.c11c_build_factory_path,$receipt.c11c_build_factory_sha256)
Write-Host ('[OK] Authorities: matrix={0}; catalog={1}; identity/provenance={2}.' -f $receipt.canonical_authorities.matrix,$receipt.canonical_authorities.catalog,$receipt.canonical_authorities.identity_provenance)
Write-Host ('[OK] Governance pass={0}; negative tests={1}; D4.8={2}; runtime={3}; production={4}; release present={5}.' -f $receipt.governance_pass,$receipt.negative_tests_pass,$receipt.d4_8_status,$receipt.runtime_authority,$receipt.production_execution,$receipt.release_directory_present)
Write-Host '=================================================='
Write-Host ' C11-D D7.5 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D8 - Media QA + Release Pipeline'
