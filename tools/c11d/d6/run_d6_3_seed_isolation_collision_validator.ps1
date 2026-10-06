#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'seed_isolation_collision_validator.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_3'
$d62ReceiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_2\d6_2_resolution_receipt.json'
if (-not (Test-Path -LiteralPath $d62ReceiptPath -PathType Leaf)) { throw 'D6.2 PASS/CLOSED receipt is missing.' }
$d62Receipt = Get-Content -LiteralPath $d62ReceiptPath -Raw | ConvertFrom-Json
if ($d62Receipt.result -ne 'PASS' -or $d62Receipt.status -ne 'CLOSED') { throw 'D6.2 must be PASS/CLOSED before D6.3.' }

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --snapshot-only $Root
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D6.3 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

function Get-EvidenceHashes {
    param([string]$Directory)
    $hashes = [ordered]@{}
    $expectedNames = @('d6_3_isolation_matrix.json', 'd6_3_collision_matrix.json', 'd6_3_negative_tests.json', 'd6_3_validation_receipt.json')
    $actualFiles = @(Get-ChildItem -LiteralPath $Directory -File -Force | Select-Object -ExpandProperty Name | Sort-Object)
    $unexpectedFiles = @($actualFiles | Where-Object { $_ -notin $expectedNames })
    $subdirectories = @(Get-ChildItem -LiteralPath $Directory -Directory -Force | Select-Object -ExpandProperty Name | Sort-Object)
    if ($unexpectedFiles.Count -gt 0 -or $subdirectories.Count -gt 0) {
        $unexpectedText = if ($unexpectedFiles.Count -gt 0) { $unexpectedFiles -join ', ' } else { '<none>' }
        $directoryText = if ($subdirectories.Count -gt 0) { $subdirectories -join ', ' } else { '<none>' }
        throw ('D6.3 output directory contains undeclared files/directories. files={0}; directories={1}' -f $unexpectedText, $directoryText)
    }
    foreach ($fileName in $expectedNames) {
        $filePath = Join-Path $Directory $fileName
        if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) { throw ('Missing D6.3 evidence: {0}' -f $fileName) }
        $hashes[$fileName] = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    return $hashes
}


Write-Host '=================================================='
Write-Host ' C11-D D6.3 - SEED ISOLATION / COLLISION VALIDATION'
Write-Host '=================================================='
$protectedInputs = @(
    (Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_0\d6_0_audit_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_0\d6_0_governance_findings.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_1\d6_1_registry_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_2\d6_2_resolution_receipt.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_REGISTRY_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_GOVERNANCE_POLICY_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_DERIVATION_SPEC_V1.json'),
    (Join-Path $repoRoot 'tools\c11d\d6\seed_resolver.py'),
    (Join-Path $repoRoot 'definitions\c11d\production\C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'),
    (Join-Path $repoRoot 'tools\c11d\d4\production_request_normalizer.py'),
    (Join-Path $repoRoot 'tools\c11d\d3\c11d_music_engine_v5.py')
)
$protectedHashesBefore = @{}
foreach ($inputPath in $protectedInputs) { $protectedHashesBefore[$inputPath] = (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash }
$before = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files.' -f $before.files)

Push-Location $repoRoot
try {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.3 validator run 1 failed.' }
    $firstHashes = Get-EvidenceHashes -Directory $outputDirectory
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.3 validator run 2 failed.' }
    $secondHashes = Get-EvidenceHashes -Directory $outputDirectory
}
finally {
    Pop-Location
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE outside allowed D6.3 evidence tree: before={0}/{1}; after={2}/{3}' -f $before.files, $before.sha256, $after.files, $after.sha256)
}
foreach ($inputPath in $protectedInputs) {
    if ($protectedHashesBefore[$inputPath] -ne (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash) { throw ('Protected input changed: {0}' -f $inputPath) }
}
foreach ($fileName in $firstHashes.Keys) {
    if ($firstHashes[$fileName] -ne $secondHashes[$fileName]) { throw ('D6.3 deterministic/idempotent evidence mismatch: {0}' -f $fileName) }
}

$receiptPath = Join-Path $outputDirectory 'd6_3_validation_receipt.json'
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D6.3 receipt is not PASS/CLOSED.' }
if ($receipt.runtime_authority -ne 'NONE' -or $receipt.production_execution -ne $false -or $receipt.renderer_execution -ne $false -or $receipt.godot_production_execution -ne $false -or $receipt.ffmpeg_production_execution -ne $false -or $receipt.physical_authorization_inferred -ne $false) { throw 'D6.3 runtime/authorization fence failed.' }
Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d6/d6_3/ evidence may change.'
Write-Host '[OK] Two runs produced identical evidence files and SHA-256 values.'
Write-Host ('[OK] Authorities={0}; numeric reuse valid={1}; request isolation={2}; derived corpus={3}; observed collisions={4}; validation cases={5}.' -f $receipt.canonical_authority_count, $receipt.numeric_equality_across_domains, $receipt.request_seed_isolation, $receipt.derived_seed_corpus_count, $receipt.derived_collision_count, $receipt.validation_case_count)
Write-Host ('[OK] Shared RNG={0}; Producer automatic selection={1}; UNKNOWN preserved={2}; master_seed={3}.' -f $receipt.shared_rng_finding, $receipt.producer_auto_selection, $receipt.unknown_findings_preserved, $receipt.master_seed)
Write-Host '=================================================='
Write-Host ' C11-D D6.3 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D6.4 - Request / Plan / Provenance Integration'
