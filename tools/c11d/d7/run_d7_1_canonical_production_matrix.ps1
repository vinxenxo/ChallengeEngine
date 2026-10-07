#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'production_matrix_builder.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_1'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D7.1 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

$before = Get-TreeSnapshot -Root $repoRoot
Write-Host ((' [OK] Mutation guard baseline captured: {0} worktree files.' -f $before.files))

& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D7.1 matrix builder run 1 failed.' }

$run1 = @{ }
Get-ChildItem -LiteralPath $outputDirectory -File | ForEach-Object {
    $run1[$_.Name] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
}

& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D7.1 matrix builder run 2 failed.' }

$run2 = @{ }
Get-ChildItem -LiteralPath $outputDirectory -File | ForEach-Object {
    $run2[$_.Name] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
}

$expectedNames = @(
    'd7_1_canonical_matrix.json',
    'd7_1_matrix_validation.json',
    'd7_1_negative_tests.json',
    'd7_1_matrix_receipt.json'
)

foreach ($name in $expectedNames) {
    if (-not $run1.ContainsKey($name) -or -not $run2.ContainsKey($name)) {
        throw ('Missing D7.1 evidence file: {0}' -f $name)
    }
    if ($run1[$name] -ne $run2[$name]) {
        throw ('D7.1 evidence is not deterministic: {0}' -f $name)
    }
}

$unexpected = @(Get-ChildItem -LiteralPath $outputDirectory -Force | Where-Object {
    $_.Name -notin $expectedNames
})
if ($unexpected.Count -ne 0) {
    throw ('Unexpected files under D7.1 evidence directory: {0}' -f (($unexpected | Select-Object -ExpandProperty Name) -join ', '))
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $before.files, $before.sha256, $after.files, $after.sha256)
}

$receipt = Get-Content -LiteralPath (Join-Path $outputDirectory 'd7_1_matrix_receipt.json') -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') {
    throw 'D7.1 did not finish PASS/CLOSED.'
}

Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d7/d7_1/ evidence may change.'
Write-Host '[OK] Four D7.1 evidence files present and exactly scoped.'
Write-Host '[OK] Two runs produced identical evidence files and SHA-256 values.'
Write-Host (('[OK] Matrix authority={0}; challenges={1}; delivery profiles={2}; modes={3}; core cases={4}.' -f $receipt.canonical_authorities.matrix, $receipt.challenge_count, $receipt.delivery_profile_count, $receipt.mode_count, $receipt.core_cases))
Write-Host (('[OK] Negative tests={0}; pass={1}; catalog authority={2}.' -f $receipt.negative_cases, $receipt.negative_tests_pass, $receipt.canonical_authorities.catalog))
Write-Host (('[OK] Runtime authority={0}; production execution={1}; C11-C build SHA gate={2}.' -f $receipt.runtime_authority, $receipt.production_execution, $receipt.c11c_build_factory_expected_sha256))
Write-Host '=================================================='
Write-Host ' C11-D D7.1 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D7.2 - Matrix Coverage / Constraint Validator'
