#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'production_matrix_catalog_audit.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_0'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

Write-Host '=================================================='
Write-Host ' C11-D D7.0 - PRODUCTION MATRIX / CATALOG AUDIT'
Write-Host '=================================================='

$d6Receipt = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_5\d6_5_acceptance_receipt.json'
if (-not (Test-Path -LiteralPath $d6Receipt -PathType Leaf)) { throw 'D6.5 PASS/CLOSED receipt is missing.' }
$d6 = Get-Content -LiteralPath $d6Receipt -Raw | ConvertFrom-Json
if ($d6.result -ne 'PASS' -or $d6.status -ne 'CLOSED') { throw 'D6.5 must be PASS/CLOSED before D7.0.' }
Write-Host '[OK] D6.5 PASS/CLOSED verified.'

function Get-TreeSnapshot {
    param([string]$Root)
    $raw = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D7.0 repository snapshot.' }
    return ($raw | ConvertFrom-Json)
}

$baseline = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files.' -f $baseline.files)

for ($run = 1; $run -le 2; $run++) {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw ('D7.0 audit run {0} failed.' -f $run) }
}

$after = Get-TreeSnapshot -Root $repoRoot
$baselineComparable = ('{0}|{1}' -f $baseline.files, $baseline.sha256)
$afterComparable = ('{0}|{1}' -f $after.files, $after.sha256)
if ($baselineComparable -ne $afterComparable) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $baseline.files, $baseline.sha256, $after.files, $after.sha256)
}
Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d7/d7_0/ evidence may change.'

$expectedNames = @(
    'd7_0_production_inventory.json',
    'd7_0_matrix_usage_audit.json',
    'd7_0_catalog_findings.json',
    'd7_0_audit_receipt.json'
)
$actualNames = @(Get-ChildItem -LiteralPath $outputDirectory -File | Select-Object -ExpandProperty Name | Sort-Object)
$unexpected = @($actualNames | Where-Object { $_ -notin $expectedNames })
$missing = @($expectedNames | Where-Object { $_ -notin $actualNames })
if ($unexpected.Count -gt 0 -or $missing.Count -gt 0) {
    throw ('D7.0 evidence layout failure. Missing={0}; Unexpected={1}' -f ($missing -join ','), ($unexpected -join ','))
}

$hashes = Get-FileHash -LiteralPath ($expectedNames | ForEach-Object { Join-Path $outputDirectory $_ }) -Algorithm SHA256 | Select-Object Path, Hash
Write-Host '[OK] Four D7.0 evidence files present.'
Write-Host '[OK] D7.0 evidence layout deterministic.'
Write-Host '[OK] No matrix/catalog authority is activated by D7.0.'
Write-Host '[OK] runtime_authority=NONE; production execution=False.'
Write-Host '=================================================='
Write-Host ' C11-D D7.0 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D7.1 - Canonical Production Matrix'
