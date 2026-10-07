#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$pythonScript = Join-Path $PSScriptRoot 'seed_request_plan_integrator.py'
$outputDirectory = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_4'
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
$d63ReceiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_3\d6_3_validation_receipt.json'
if (-not (Test-Path -LiteralPath $d63ReceiptPath -PathType Leaf)) { throw 'D6.3 PASS/CLOSED receipt is missing.' }
$d63Receipt = Get-Content -LiteralPath $d63ReceiptPath -Raw | ConvertFrom-Json
if ($d63Receipt.result -ne 'PASS' -or $d63Receipt.status -ne 'CLOSED') { throw 'D6.3 must be PASS/CLOSED before D6.4.' }

function Get-TreeSnapshot {
    param([string]$Root)
    $snapshotText = & python $pythonScript --root $Root --snapshot-only
    if ($LASTEXITCODE -ne 0) { throw 'Unable to capture D6.4 repository snapshot.' }
    return ($snapshotText | ConvertFrom-Json)
}

$evidenceNames = @(
    'd6_4_integration_matrix.json',
    'd6_4_provenance_matrix.json',
    'd6_4_negative_tests.json',
    'd6_4_integration_receipt.json'
)

function Get-EvidenceHashes {
    param([string]$Directory)
    $hashes = [ordered]@{}
    if (-not (Test-Path -LiteralPath $Directory -PathType Container)) { throw 'D6.4 evidence directory is missing.' }
    $actualEntries = @(Get-ChildItem -LiteralPath $Directory -Force)
    $unexpected = @($actualEntries | Where-Object { $_.PSIsContainer -or ($evidenceNames -notcontains $_.Name) })
    if ($unexpected.Count -gt 0) { throw ('Unexpected D6.4 evidence entry(ies): {0}' -f (($unexpected | Select-Object -ExpandProperty Name | Sort-Object) -join ', ')) }
    foreach ($fileName in $evidenceNames) {
        $filePath = Join-Path $Directory $fileName
        if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) { throw ('Missing D6.4 evidence: {0}' -f $fileName) }
        $hashes[$fileName] = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    return $hashes
}

Write-Host '=================================================='
Write-Host ' C11-D D6.4 - REQUEST / PLAN / PROVENANCE INTEGRATION'
Write-Host '=================================================='
$protectedInputs = @(
    (Join-Path $repoRoot 'artifacts\tests\c11d_d4\d4_2\d4_2_validation_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d4\d4_4\d4_4_validation_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d4\d4_8\d4_8_validation_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d3\d3_3\d3_3_validation_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_1\d6_1_registry_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_2\d6_2_resolution_receipt.json'),
    (Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_3\d6_3_validation_receipt.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_REGISTRY_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_GOVERNANCE_POLICY_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\seeds\C11D_SEED_DERIVATION_SPEC_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\production\C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'),
    (Join-Path $repoRoot 'definitions\c11d\provenance\C11D_PROVENANCE_LINEAGE_REGISTRY_V1.json'),
    (Join-Path $repoRoot 'tools\c11d\d4\production_request_normalizer.py'),
    (Join-Path $repoRoot 'tools\c11d\d4\personalization_resolver.py'),
    (Join-Path $repoRoot 'tools\c11d\d4\canonical_production_orchestrator.py'),
    (Join-Path $repoRoot 'tools\c11d\d6\seed_resolver.py')
)
$protectedHashesBefore = @{}
foreach ($inputPath in $protectedInputs) {
    if (-not (Test-Path -LiteralPath $inputPath -PathType Leaf)) { throw ('Protected input missing: {0}' -f $inputPath) }
    $protectedHashesBefore[$inputPath] = (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash
}

$before = Get-TreeSnapshot -Root $repoRoot
Write-Host ('[OK] Mutation guard baseline captured: {0} worktree files.' -f $before.files)

Push-Location $repoRoot
try {
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.4 integrator run 1 failed.' }
    $firstHashes = Get-EvidenceHashes -Directory $outputDirectory
    & python $pythonScript --root $repoRoot
    if ($LASTEXITCODE -ne 0) { throw 'D6.4 integrator run 2 failed.' }
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
    if ($firstHashes[$fileName] -ne $secondHashes[$fileName]) { throw ('D6.4 deterministic/idempotent evidence mismatch: {0}' -f $fileName) }
}

$receiptPath = Join-Path $outputDirectory 'd6_4_integration_receipt.json'
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D6.4 receipt is not PASS/CLOSED.' }
if ($receipt.runtime_authority -ne 'NONE' -or $receipt.production_execution -ne $false -or $receipt.renderer_execution -ne $false -or $receipt.godot_production_execution -ne $false -or $receipt.ffmpeg_production_execution -ne $false -or $receipt.physical_authorization_inferred -ne $false) { throw 'D6.4 runtime/authorization fence failed.' }
if ($receipt.plan_hash_owner -ne 'canonical_production_orchestrator') { throw 'D6.4 plan hash owner changed.' }
if ($receipt.master_seed -ne 'NOT_ADOPTED') { throw 'D6.4 master_seed state changed.' }
if ($receipt.d4_8_status -ne 'BLOCKED') { throw 'D4.8 must remain BLOCKED.' }

Write-Host '[OK] Mutation guard PASS; only artifacts/tests/c11d_d6/d6_4/ evidence may change.'
Write-Host '[OK] Two runs produced identical evidence files and SHA-256 values.'
Write-Host ('[OK] Request SHA={0}; Seed resolution SHA={1}; Plan SHA={2}.' -f $receipt.request_sha256, $receipt.seed_resolution_sha256, $receipt.plan_sha256)
Write-Host ('[OK] GAMEPLAY provenance={0}; MUSIC provenance={1}; isolation={2}; D5 lineage={3}.' -f $receipt.gameplay_seed_provenance.seed_id, $receipt.music_seed_provenance.seed_id, $receipt.gameplay_music_isolation, $receipt.d5_lineage_compatibility)
Write-Host ('[OK] D4.8={0}; derivation={1}/{2}; master_seed={3}; negative tests={4}/{5}.' -f $receipt.d4_8_status, $receipt.derivation_capability_available, $receipt.derivation_runtime_activation, $receipt.master_seed, $receipt.negative_tests, $receipt.negative_case_count)
Write-Host ('[OK] C11-C preserved={0}; runtime authority={1}; production execution={2}.' -f $receipt.frozen_c11c_preserved, $receipt.runtime_authority, $receipt.production_execution)
Write-Host '=================================================='
Write-Host ' C11-D D6.4 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D6.5 - Full D6 Acceptance'
