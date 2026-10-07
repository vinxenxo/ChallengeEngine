#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'full_d6_acceptance.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_5'
$expectedFiles = @(
    'd6_5_acceptance_matrix.json',
    'd6_5_acceptance_summary.json',
    'd6_5_negative_tests.json',
    'd6_5_acceptance_receipt.json'
)

New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null

function Invoke-D65Snapshot {
    param([string]$Root)
    $raw = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D6.5 repository snapshot.' }
    try { return ($raw | ConvertFrom-Json) } catch { throw 'D6.5 snapshot output is not valid JSON.' }
}

function Get-FileDigest {
    param([string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

Write-Host '=================================================='
Write-Host ' C11-D D6.5 - FULL D6 ACCEPTANCE'
Write-Host '=================================================='

$before = Invoke-D65Snapshot -Root $repoRoot
Write-Host (('[OK] Mutation guard baseline captured: {0} worktree files.' -f $before.files))

& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D6.5 acceptance run 1 failed.' }

$hashA = @{}
foreach ($name in $expectedFiles) {
    $path = Join-Path $outputDirectory $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing D6.5 evidence: $name" }
    $hashA[$name] = Get-FileDigest -Path $path
}

& python $pythonScript --root $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'D6.5 acceptance run 2 failed.' }

$hashB = @{}
foreach ($name in $expectedFiles) {
    $path = Join-Path $outputDirectory $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing D6.5 evidence: $name" }
    $hashB[$name] = Get-FileDigest -Path $path
    if ($hashA[$name] -ne $hashB[$name]) { throw "D6.5 non-deterministic evidence: $name" }
}

$actualNames = Get-ChildItem -LiteralPath $outputDirectory -File | Select-Object -ExpandProperty Name
$unexpected = @($actualNames | Where-Object { $expectedFiles -notcontains $_ })
if ($unexpected.Count -gt 0) { throw ('Unexpected files under D6.5 evidence directory: ' + ($unexpected -join ', ')) }

$after = Invoke-D65Snapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $before.files, $before.sha256, $after.files, $after.sha256)
}

Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d6/d6_5/ evidence may change.'
Write-Host '[OK] Two runs produced identical D6.5 evidence files and SHA-256 values.'
Write-Host '[OK] D6.0-D6.4 predecessor receipts: PASS/CLOSED.'
Write-Host '[OK] Cross-checks, D3/D4 preservation, negative tests and C11-C identity: PASS.'
Write-Host '[OK] Runtime authority=NONE; production execution=False.'
Write-Host '=================================================='
Write-Host ' C11-D D6.5 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D7 - Production Matrix + Catalog'
