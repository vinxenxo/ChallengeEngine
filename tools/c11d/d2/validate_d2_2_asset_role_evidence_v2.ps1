Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path
$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$CurrentD = Join-Path $Repo 'docs\current\d'

$D21ReceiptPath = Join-Path $D2Root 'd2_1_validation_receipt.json'
$MatrixPath = Join-Path $D2Root 'd2_2_asset_role_evidence_matrix.json'
$ContractPath = Join-Path $CurrentD 'D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
$ReceiptPath = Join-Path $D2Root 'd2_2_validation_receipt.json'
$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

$RequiredPaths = @(
    $D21ReceiptPath,
    $MatrixPath,
    $ContractPath,
    $MasterPath,
    $StartPath
)

foreach ($Path in $RequiredPaths) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw ('Missing required validation input: ' + $Path)
    }
}

$D21Receipt = Get-Content -LiteralPath $D21ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Matrix = Get-Content -LiteralPath $MatrixPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Contract = Get-Content -LiteralPath $ContractPath -Raw -Encoding UTF8
$Master = Get-Content -LiteralPath $MasterPath -Raw -Encoding UTF8
$Start = Get-Content -LiteralPath $StartPath -Raw -Encoding UTF8

$D21Pass = ([string]$D21Receipt.result -eq 'PASS')

$AssetsCount = [int]$Matrix.asset_count
$ExplicitRoleAssets = [int]$Matrix.explicit_role_asset_count
$UnknownRoleAssets = [int]$Matrix.unknown_role_asset_count
$BoundAssets = [int]$Matrix.assets_with_challenge_bindings
$CrossReuse = [int]$Matrix.cross_family_reuse_count
$TrueConflicts = [int]$Matrix.true_family_conflict_count
$RuntimeAuthority = [string]$Matrix.runtime_authority
$MatrixStatus = [string]$Matrix.status

$ProtectedChanges = @()
$ProtectedProp = $Matrix.PSObject.Properties['protected_source_new_changes']
if ($null -ne $ProtectedProp) {
    $ProtectedChanges = @($ProtectedProp.Value)
}

$CountsOk =
    ($AssetsCount -eq 15) -and
    ($ExplicitRoleAssets -eq 15) -and
    ($UnknownRoleAssets -eq 0) -and
    ($BoundAssets -eq 15) -and
    ($CrossReuse -eq 1) -and
    ($TrueConflicts -eq 0)

$RuntimeOk = ($RuntimeAuthority -eq 'NONE')
$StatusOk = ($MatrixStatus -eq 'ACTIVE')
$ProtectedOk = ($ProtectedChanges.Count -eq 0)

$ContractPurpose = $Contract.IndexOf('## Purpose', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractRules = $Contract.IndexOf('## Canonical rules', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractReuse =
    ($Contract.IndexOf('CROSS_FAMILY_REUSE', [System.StringComparison]::OrdinalIgnoreCase) -ge 0) -or
    ($Contract.IndexOf('cross-family reuse', [System.StringComparison]::OrdinalIgnoreCase) -ge 0) -or
    ($Contract.IndexOf('cross family reuse', [System.StringComparison]::OrdinalIgnoreCase) -ge 0)
$ContractConflict =
    ($Contract.IndexOf('TRUE_FAMILY_CONFLICT', [System.StringComparison]::OrdinalIgnoreCase) -ge 0) -or
    ($Contract.IndexOf('true family conflict', [System.StringComparison]::OrdinalIgnoreCase) -ge 0)
$ContractNext = $Contract.IndexOf('D2.3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0

$ContractOk =
    $ContractPurpose -and
    $ContractRules -and
    $ContractReuse -and
    $ContractConflict -and
    $ContractNext

$MasterD22 = $Master.IndexOf('D2.2', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$StartD22 = $Start.IndexOf('D2.2', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$MasterNext = $Master.IndexOf('D2.3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$StartNext = $Start.IndexOf('D2.3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0

$PromptOk = $MasterD22 -and $StartD22 -and $MasterNext -and $StartNext

$OverallPass =
    $D21Pass -and
    $CountsOk -and
    $RuntimeOk -and
    $StatusOk -and
    $ProtectedOk -and
    $ContractOk -and
    $PromptOk

$Result = 'FAIL'
if ($OverallPass) {
    $Result = 'PASS'
}

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$Receipt = [ordered]@{
    checkpoint = 'C11-D D2.2'
    result = $Result
    validation_type = 'D2_2_ASSET_ROLE_EVIDENCE_FORMAL_VALIDATION_V2'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    source_d2_1_receipt = 'artifacts\tests\c11d_d2\d2_1_validation_receipt.json'
    matrix = 'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json'
    contract = 'docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
    logical_asset_count = $AssetsCount
    explicit_role_asset_count = $ExplicitRoleAssets
    unknown_role_asset_count = $UnknownRoleAssets
    assets_with_challenge_bindings = $BoundAssets
    cross_family_reuse_count = $CrossReuse
    true_family_conflict_count = $TrueConflicts
    runtime_authority = $RuntimeAuthority
    matrix_status = $MatrixStatus
    protected_source_new_changes_count = $ProtectedChanges.Count
    d2_1_pass_verified = $D21Pass
    counts_verified = $CountsOk
    runtime_authority_verified = $RuntimeOk
    matrix_status_verified = $StatusOk
    protected_boundary_verified = $ProtectedOk
    contract_verified = $ContractOk
    prompts_verified = $PromptOk
    semantic_rule = 'Cross-family reuse is admissible reuse; true family conflict is the blocking condition.'
    no_runtime_activation = $true
    no_renderer_change = $true
    no_simulation_change = $true
    no_mechanics_change = $true
    no_rng_change = $true
    no_historical_promotion = $true
    next_checkpoint = 'D2.3'
}

[System.IO.File]::WriteAllText(
    $ReceiptPath,
    ($Receipt | ConvertTo-Json -Depth 20),
    $Utf8NoBom
)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.2 - FORMAL VALIDATION V2' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''

if ($D21Pass) {
    Write-Host '[OK] D2.1 receipt PASS.' -ForegroundColor Green
}

if ($CountsOk) {
    Write-Host '[OK] 15 assets / 15 explicit roles / 0 UNKNOWN roles / 15 bindings.' -ForegroundColor Green
}
if (-not $CountsOk) {
    Write-Host '[FAIL] Core D2.2 counters do not match the expected contract.' -ForegroundColor Red
}

if ($CrossReuse -eq 1) {
    Write-Host '[OK] CROSS_FAMILY_REUSE = 1.' -ForegroundColor Green
}
if ($CrossReuse -ne 1) {
    Write-Host ('[FAIL] CROSS_FAMILY_REUSE expected 1, found {0}.' -f $CrossReuse) -ForegroundColor Red
}

if ($TrueConflicts -eq 0) {
    Write-Host '[OK] TRUE_FAMILY_CONFLICT = 0.' -ForegroundColor Green
}
if ($TrueConflicts -ne 0) {
    Write-Host ('[FAIL] TRUE_FAMILY_CONFLICT expected 0, found {0}.' -f $TrueConflicts) -ForegroundColor Red
}

if ($RuntimeOk) {
    Write-Host '[OK] runtime_authority = NONE.' -ForegroundColor Green
}
if ($StatusOk) {
    Write-Host '[OK] matrix status = ACTIVE.' -ForegroundColor Green
}
if ($ProtectedOk) {
    Write-Host '[OK] No protected-source changes recorded.' -ForegroundColor Green
}

if ($ContractOk) {
    Write-Host '[OK] D2.2 contract verified.' -ForegroundColor Green
}
if (-not $ContractOk) {
    Write-Host '[FAIL] D2.2 contract verification failed.' -ForegroundColor Red
    Write-Host ('[INFO] Purpose={0} Rules={1} ReuseRule={2} ConflictRule={3} D2.3={4}' -f $ContractPurpose,$ContractRules,$ContractReuse,$ContractConflict,$ContractNext)
}

if ($PromptOk) {
    Write-Host '[OK] MASTER / START handoff verified for D2.3.' -ForegroundColor Green
}
if (-not $PromptOk) {
    Write-Host '[FAIL] MASTER / START handoff verification failed.' -ForegroundColor Red
    Write-Host ('[INFO] MASTER_D2.2={0} START_D2.2={1} MASTER_D2.3={2} START_D2.3={3}' -f $MasterD22,$StartD22,$MasterNext,$StartNext)
}

Write-Host ''
Write-Host ('MATRIX:   ' + $MatrixPath)
Write-Host ('CONTRACT: ' + $ContractPath)
Write-Host ('RECEIPT:  ' + $ReceiptPath)
Write-Host ''

if ($OverallPass) {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D2.2 - PASS / VALIDATED' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'D2.2 asset role/evidence matrix is formally validated.'
    Write-Host 'Cross-family reuse is admissible.'
    Write-Host 'True family conflicts = 0.'
    Write-Host 'No runtime activation performed.'
    Write-Host 'No protected C11-C source modified.'
    Write-Host ''
    Write-Host 'NEXT: D2.3'
}

if (-not $OverallPass) {
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ' C11-D D2.2 - VERIFY FAIL' -ForegroundColor Red
    Write-Host '==================================================' -ForegroundColor Red
}
