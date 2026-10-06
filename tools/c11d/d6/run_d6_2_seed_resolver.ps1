#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'seed_resolver.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_2'
$d61ReceiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_1\d6_1_registry_receipt.json'
if (-not (Test-Path -LiteralPath $d61ReceiptPath -PathType Leaf)) { throw 'D6.1 PASS/CLOSED receipt is missing.' }
$d61Receipt = Get-Content -LiteralPath $d61ReceiptPath -Raw | ConvertFrom-Json
if ($d61Receipt.result -ne 'PASS' -or $d61Receipt.status -ne 'CLOSED') { throw 'D6.1 must be PASS/CLOSED before D6.2.' }

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --snapshot-only $Root
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D6.2 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

function Get-EvidenceHashes {
    param([string]$Directory)
    $hashes = [ordered]@{}
    foreach ($fileName in @('d6_2_resolution_matrix.json', 'd6_2_derivation_vectors.json', 'd6_2_negative_tests.json', 'd6_2_resolution_receipt.json')) {
        $filePath = Join-Path $Directory $fileName
        if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) { throw ('Missing D6.2 evidence: {0}' -f $fileName) }
        $hashes[$fileName] = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    return $hashes
}

Write-Host '=================================================='
Write-Host ' C11-D D6.2 - SEED RESOLVER / DETERMINISTIC DERIVATION'
Write-Host '=================================================='
$protectedInputs = @(
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_REGISTRY_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_GOVERNANCE_POLICY_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_DERIVATION_SPEC_V1.json'),
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
    if ($LASTEXITCODE -ne 0) { throw 'D6.2 resolver run 1 failed.' }
    $firstHashes = Get-EvidenceHashes -Directory $outputDirectory
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.2 resolver run 2 failed.' }
    $secondHashes = Get-EvidenceHashes -Directory $outputDirectory
}
finally {
    Pop-Location
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $before.files, $before.sha256, $after.files, $after.sha256)
}
foreach ($inputPath in $protectedInputs) {
    if ($protectedHashesBefore[$inputPath] -ne (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash) { throw ('Protected input changed: {0}' -f $inputPath) }
}
foreach ($fileName in $firstHashes.Keys) {
    if ($firstHashes[$fileName] -ne $secondHashes[$fileName]) { throw ('D6.2 deterministic/idempotent evidence mismatch: {0}' -f $fileName) }
}

$receiptPath = Join-Path $outputDirectory 'd6_2_resolution_receipt.json'
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D6.2 receipt is not PASS/CLOSED.' }
if ($receipt.runtime_authority -ne 'NONE' -or $receipt.production_execution -ne $false -or $receipt.renderer_execution -ne $false -or $receipt.godot_production_execution -ne $false -or $receipt.ffmpeg_production_execution -ne $false) { throw 'D6.2 runtime/production fence failed.' }
Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d6/d6_2/ evidence may change.'
Write-Host '[OK] Two runs produced identical evidence files and SHA-256 values.'
Write-Host ('[OK] Explicit GAMEPLAY/MUSIC resolution; derivation capability={0}; activation={1}; master_seed={2}.' -f $receipt.derivation_capability_available, $receipt.derivation_runtime_activation, $receipt.master_seed_canonical_authority)
Write-Host ('[OK] Negative tests={0}; D3 isolation={1}; D4 separation={2}; D4.8 production blocked={3}.' -f $receipt.negative_tests_pass, $receipt.d3_music_isolation, $receipt.d4_seed_music_seed_separation, $receipt.d4_8_production_blocked)
Write-Host '=================================================='
Write-Host ' C11-D D6.2 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D6.3 - Seed Isolation + Collision Validator'
