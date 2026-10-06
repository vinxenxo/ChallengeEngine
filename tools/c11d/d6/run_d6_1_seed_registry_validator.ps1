[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'seed_registry_validator.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_1'
$d55ReceiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d5\d5_5\d5_5_acceptance_receipt.json'
if (-not (Test-Path -LiteralPath $d55ReceiptPath -PathType Leaf)) { throw 'D5.5 acceptance receipt is missing.' }
$d55Receipt = Get-Content -LiteralPath $d55ReceiptPath -Raw | ConvertFrom-Json
if ($d55Receipt.result -ne 'PASS' -or $d55Receipt.status -ne 'CLOSED') { throw 'D5.5 must be PASS/CLOSED before D6.1.' }

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --snapshot-only $Root
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D6.1 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

function Get-EvidenceHashes {
    param([string]$Directory)
    $hashes = [ordered]@{}
    foreach ($fileName in @('d6_1_registry_validation.json', 'd6_1_governance_matrix.json', 'd6_1_negative_tests.json', 'd6_1_registry_receipt.json')) {
        $filePath = Join-Path $Directory $fileName
        if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) { throw ('Missing D6.1 evidence: {0}' -f $fileName) }
        $hashes[$fileName] = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    return $hashes
}

Write-Host '=================================================='
Write-Host ' C11-D D6.1 - CANONICAL SEED REGISTRY VALIDATION'
Write-Host '=================================================='
$registryPath = Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_REGISTRY_V1.json'
$policyPath = Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_GOVERNANCE_POLICY_V1.json'
$registryHashBefore = (Get-FileHash -LiteralPath $registryPath -Algorithm SHA256).Hash
$policyHashBefore = (Get-FileHash -LiteralPath $policyPath -Algorithm SHA256).Hash
$before = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files.' -f $before.files)

Push-Location $repoRoot
try {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.1 validation run 1 failed.' }
    $firstHashes = Get-EvidenceHashes -Directory $outputDirectory
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.1 validation run 2 failed.' }
    $secondHashes = Get-EvidenceHashes -Directory $outputDirectory
}
finally {
    Pop-Location
}

$after = Get-TreeSnapshot -Root $repoRoot
if ($before.files -ne $after.files -or $before.sha256 -ne $after.sha256) {
    throw ('FILESYSTEM_MUTATION_FAILURE: before={0}/{1}; after={2}/{3}' -f $before.files, $before.sha256, $after.files, $after.sha256)
}
if (($registryHashBefore -ne (Get-FileHash -LiteralPath $registryPath -Algorithm SHA256).Hash) -or ($policyHashBefore -ne (Get-FileHash -LiteralPath $policyPath -Algorithm SHA256).Hash)) {
    throw 'D6.1 authoring inputs were rewritten.'
}
foreach ($fileName in $firstHashes.Keys) {
    if ($firstHashes[$fileName] -ne $secondHashes[$fileName]) { throw ('D6.1 deterministic/idempotent evidence mismatch: {0}' -f $fileName) }
}

$receiptPath = Join-Path $outputDirectory 'd6_1_registry_receipt.json'
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D6.1 receipt is not PASS/CLOSED.' }
if ($receipt.runtime_authority -ne 'NONE' -or $receipt.production_execution -ne $false -or $receipt.renderer_execution -ne $false -or $receipt.godot_production_execution -ne $false -or $receipt.ffmpeg_production_execution -ne $false) { throw 'D6.1 runtime/production fence failed.' }
Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d6/d6_1/ evidence may change.'
Write-Host '[OK] Two runs produced identical evidence files and SHA-256 values.'
Write-Host ('[OK] Canonical authorities={0}; unknown preserved={1}; shared RNG finding={2}; Producer selections={3}.' -f (($receipt.canonical_authorities -join ',')), $receipt.unknown_findings_preserved, $receipt.shared_rng_finding, $receipt.producer_nondeterministic_selections)
Write-Host '=================================================='
Write-Host ' C11-D D6.1 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D6.2 - Seed Resolver / Deterministic Derivation'
