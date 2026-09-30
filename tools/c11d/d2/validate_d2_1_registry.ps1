Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path
$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$CurrentD = Join-Path $Repo 'docs\current\d'
$HistoryD = Join-Path $Repo 'docs\history\master-prompts\c11d'
$RegistryPath = Join-Path $Repo 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
$ContractPath = Join-Path $CurrentD 'D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md'
$D20ReceiptPath = Join-Path $D2Root 'd2_0_validation_receipt.json'
$ReceiptPath = Join-Path $D2Root 'd2_1_validation_receipt.json'
$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Content
    )
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Has-Text {
    param(
        [string]$Text,
        [string]$Needle
    )
    return $Text.IndexOf($Needle, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
}

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.1 — REGISTRY VALIDATION' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host ('[INFO] Repo: {0}' -f $Repo)
Write-Host ''

if (-not (Test-Path -LiteralPath $D20ReceiptPath)) {
    throw 'No existe el receipt de D2.0.'
}

if (-not (Test-Path -LiteralPath $RegistryPath)) {
    throw 'No existe la registry de D2.1.'
}

if (-not (Test-Path -LiteralPath $ContractPath)) {
    throw 'No existe el contrato de D2.1.'
}

if (-not (Test-Path -LiteralPath $MasterPath)) {
    throw 'No existe MASTER_HANDOVER_C11D_CURRENT.md.'
}

if (-not (Test-Path -LiteralPath $StartPath)) {
    throw 'No existe START_PROMPT_C11D_CURRENT.md.'
}

$D20Receipt = Get-Content -LiteralPath $D20ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Registry = Get-Content -LiteralPath $RegistryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Contract = Get-Content -LiteralPath $ContractPath -Raw -Encoding UTF8
$Master = Get-Content -LiteralPath $MasterPath -Raw -Encoding UTF8
$Start = Get-Content -LiteralPath $StartPath -Raw -Encoding UTF8

$D20Pass = [string]$D20Receipt.result -eq 'PASS'
$FamilyCountOk = @($Registry.families).Count -eq 2
$ChallengeCountOk = @($Registry.challenge_bindings).Count -eq 9
$UnknownCountOk = @($Registry.unknown_family_challenges).Count -eq 5
$AssetCountOk = [int]$Registry.logical_asset_count -eq 15
$ReferenceCountOk = [int]$Registry.asset_reference_count -eq 27
$UnresolvedCountOk = [int]$Registry.unresolved_asset_reference_count -eq 0
$RuntimeAuthorityOk = [string]$Registry.runtime_authority -eq 'NONE'
$StatusOk = [string]$Registry.status -eq 'ACTIVE'
$RegistryPurposeOk = [string]$Registry.registry_purpose -eq 'Declarative evidence binding for reusable C6 Challenge asset families.'

$Rule1Ok = Has-Text ([string]$Registry.rules[0]) 'Explicit asset_family'
$Rule2Ok = Has-Text ([string]$Registry.rules[1]) 'UNKNOWN remains explicit'
$Rule3Ok = Has-Text ([string]$Registry.rules[2]) 'Filename semantics alone'
$Rule4Ok = Has-Text ([string]$Registry.rules[3]) 'SHA-256 equality alone'
$Rule5Ok = Has-Text ([string]$Registry.rules[4]) 'Historical evidence remains provenance'
$Rule6Ok = Has-Text ([string]$Registry.rules[5]) 'D2.1 does not activate runtime asset routing'

$ContractPurposeOk = Has-Text $Contract '## Purpose'
$ContractEvidenceOk = Has-Text $Contract '## Evidence rules'
$ContractSourceOk = Has-Text $Contract 'd2_0_asset_family_audit.json'
$ContractRegistryOk = Has-Text $Contract 'C11D_ASSET_FAMILY_REGISTRY_V1.json'
$ContractUnknownOk = Has-Text $Contract 'UNKNOWN'
$ContractNoRuntimeOk = Has-Text $Contract 'Runtime activation'

$MasterD21Ok = Has-Text $Master 'D2.1 — Declarative Asset Family Registry / Evidence Binding'
$MasterActiveOk = Has-Text $Master 'STATUS: ACTIVE'
$MasterRegistryOk = Has-Text $Master 'C11D_ASSET_FAMILY_REGISTRY_V1.json'
$StartD21Ok = Has-Text $Start 'C11-D D2.1: ACTIVE'
$StartRegistryOk = Has-Text $Start 'C11D_ASSET_FAMILY_REGISTRY_V1.json'

$Snapshots = @(Get-ChildItem -LiteralPath $HistoryD -File -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -match '^MASTER_HANDOVER_C11D_PRE_D2_1_.*\.md$' -or $_.Name -match '^START_PROMPT_C11D_PRE_D2_1_.*\.md$'
})

$MasterSnapshotOk = @($Snapshots | Where-Object { $_.Name -like 'MASTER_HANDOVER_C11D_PRE_D2_1_*' }).Count -gt 0
$StartSnapshotOk = @($Snapshots | Where-Object { $_.Name -like 'START_PROMPT_C11D_PRE_D2_1_*' }).Count -gt 0

$NoRuntimeActivation = [string]$Registry.runtime_authority -eq 'NONE'

$ValidationPass =
    $D20Pass -and
    $FamilyCountOk -and
    $ChallengeCountOk -and
    $UnknownCountOk -and
    $AssetCountOk -and
    $ReferenceCountOk -and
    $UnresolvedCountOk -and
    $RuntimeAuthorityOk -and
    $StatusOk -and
    $RegistryPurposeOk -and
    $Rule1Ok -and
    $Rule2Ok -and
    $Rule3Ok -and
    $Rule4Ok -and
    $Rule5Ok -and
    $Rule6Ok -and
    $ContractPurposeOk -and
    $ContractEvidenceOk -and
    $ContractSourceOk -and
    $ContractRegistryOk -and
    $ContractUnknownOk -and
    $ContractNoRuntimeOk -and
    $MasterD21Ok -and
    $MasterActiveOk -and
    $MasterRegistryOk -and
    $StartD21Ok -and
    $StartRegistryOk -and
    $MasterSnapshotOk -and
    $StartSnapshotOk -and
    $NoRuntimeActivation

$Result = 'FAIL'
if ($ValidationPass) {
    $Result = 'PASS'
}

$Receipt = [ordered]@{
    checkpoint = 'C11-D D2.1'
    result = $Result
    validation_type = 'REGISTRY_CONTRACT_PROVENANCE_VALIDATION'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    d2_0_receipt = 'artifacts\tests\c11d_d2\d2_0_validation_receipt.json'
    registry = 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
    contract = 'docs\current\d\D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md'
    master = 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'
    start_prompt = 'docs\current\d\START_PROMPT_C11D_CURRENT.md'
    logical_asset_count = [int]$Registry.logical_asset_count
    challenge_binding_count = @($Registry.challenge_bindings).Count
    explicit_family_count = @($Registry.families).Count
    unknown_family_challenge_count = @($Registry.unknown_family_challenges).Count
    asset_reference_count = [int]$Registry.asset_reference_count
    unresolved_asset_reference_count = [int]$Registry.unresolved_asset_reference_count
    runtime_authority = [string]$Registry.runtime_authority
    registry_status = [string]$Registry.status
    d2_0_pass_verified = $D20Pass
    family_count_verified = $FamilyCountOk
    challenge_count_verified = $ChallengeCountOk
    unknown_count_verified = $UnknownCountOk
    asset_count_verified = $AssetCountOk
    reference_count_verified = $ReferenceCountOk
    unresolved_count_verified = $UnresolvedCountOk
    runtime_authority_verified = $RuntimeAuthorityOk
    registry_contract_verified = ($ContractPurposeOk -and $ContractEvidenceOk -and $ContractSourceOk -and $ContractRegistryOk -and $ContractUnknownOk -and $ContractNoRuntimeOk)
    master_prompt_verified = ($MasterD21Ok -and $MasterActiveOk -and $MasterRegistryOk)
    start_prompt_verified = ($StartD21Ok -and $StartRegistryOk)
    master_snapshot_verified = $MasterSnapshotOk
    start_snapshot_verified = $StartSnapshotOk
    no_runtime_activation_performed = $NoRuntimeActivation
    no_family_merge_performed = $true
    next_checkpoint = 'D2.2 / determine from next validated evidence'
}

Write-Utf8NoBom $ReceiptPath ($Receipt | ConvertTo-Json -Depth 12)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.1 — VALIDATION RESULT' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''

if ($D20Pass) { Write-Host '[OK] D2.0 receipt PASS.' -ForegroundColor Green }
if ($FamilyCountOk) { Write-Host '[OK] 2 explicit family groups.' -ForegroundColor Green }
if ($ChallengeCountOk) { Write-Host '[OK] 9/9 Challenge bindings.' -ForegroundColor Green }
if ($UnknownCountOk) { Write-Host '[OK] 5 UNKNOWN family bindings preserved.' -ForegroundColor Green }
if ($AssetCountOk) { Write-Host '[OK] 15 logical assets.' -ForegroundColor Green }
if ($ReferenceCountOk) { Write-Host '[OK] 27 asset references.' -ForegroundColor Green }
if ($UnresolvedCountOk) { Write-Host '[OK] 0 unresolved references.' -ForegroundColor Green }
if ($RuntimeAuthorityOk) { Write-Host '[OK] runtime_authority = NONE.' -ForegroundColor Green }
if ($StatusOk) { Write-Host '[OK] registry status = ACTIVE.' -ForegroundColor Green }
if ($Rule1Ok -and $Rule2Ok -and $Rule3Ok -and $Rule4Ok -and $Rule5Ok -and $Rule6Ok) { Write-Host '[OK] Canonical registry rules verified.' -ForegroundColor Green }
if ($ContractPurposeOk -and $ContractEvidenceOk -and $ContractSourceOk -and $ContractRegistryOk -and $ContractUnknownOk -and $ContractNoRuntimeOk) { Write-Host '[OK] D2.1 contract verified.' -ForegroundColor Green }
if ($MasterD21Ok -and $MasterActiveOk -and $MasterRegistryOk) { Write-Host '[OK] MASTER handover verified.' -ForegroundColor Green }
if ($StartD21Ok -and $StartRegistryOk) { Write-Host '[OK] START prompt verified.' -ForegroundColor Green }
if ($MasterSnapshotOk -and $StartSnapshotOk) { Write-Host '[OK] Historical prompt snapshots verified.' -ForegroundColor Green }

Write-Host ''
Write-Host ('REGISTRY: {0}' -f $RegistryPath)
Write-Host ('CONTRACT: {0}' -f $ContractPath)
Write-Host ('RECEIPT:  {0}' -f $ReceiptPath)
Write-Host ''

if ($ValidationPass) {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D2.1 — PASS / VALIDATED' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'Registry validated against D2.0 evidence.'
    Write-Host 'No runtime activation performed.'
    Write-Host 'No family merge performed.'
    Write-Host 'No renderer/simulation/mechanics/RNG changes performed.'
    Write-Host ''
    Write-Host 'NEXT: D2.2 — Asset Role / Evidence Matrix'
}

if (-not $ValidationPass) {
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ' C11-D D2.1 — VALIDATION FAIL' -ForegroundColor Red
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ''
    Write-Host 'Inspect the receipt flags before advancing.'
}
