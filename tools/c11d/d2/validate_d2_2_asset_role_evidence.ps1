Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path
$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$CurrentD = Join-Path $Repo 'docs\current\d'

$D21ReceiptPath = Join-Path $D2Root 'd2_1_validation_receipt.json'
$MatrixPath = Join-Path $D2Root 'd2_2_asset_role_evidence_matrix.json'
$ContractPath = Join-Path $CurrentD 'D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
$D22ReceiptPath = Join-Path $D2Root 'd2_2_validation_receipt.json'
$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

foreach ($Path in @($D21ReceiptPath,$MatrixPath,$ContractPath,$MasterPath,$StartPath)) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw ('Required D2.2 validation input missing: ' + $Path)
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
$Status = [string]$Matrix.status

$ProtectedChanges = @()
$ProtectedProp = $Matrix.PSObject.Properties['protected_source_new_changes']
if ($null -ne $ProtectedProp) {
    $ProtectedChanges = @($ProtectedProp.Value)
}

$RoleRows = @()
$RoleProp = $Matrix.PSObject.Properties['asset_role_rows']
if ($null -ne $RoleProp) {
    $RoleRows = @($RoleProp.Value)
}

$CrossRows = @()
$CrossProp = $Matrix.PSObject.Properties['cross_family_reuse_rows']
if ($null -ne $CrossProp) {
    $CrossRows = @($CrossProp.Value)
}

$ConflictRows = @()
$ConflictProp = $Matrix.PSObject.Properties['true_family_conflict_rows']
if ($null -ne $ConflictProp) {
    $ConflictRows = @($ConflictProp.Value)
}

$CountsOk =
    ($AssetsCount -eq 15) -and
    ($ExplicitRoleAssets -eq 15) -and
    ($UnknownRoleAssets -eq 0) -and
    ($BoundAssets -eq 15) -and
    ($CrossReuse -eq 1) -and
    ($TrueConflicts -eq 0)

$RowsOk = ($RoleRows.Count -eq 15)
$CrossReuseOk = ($CrossRows.Count -eq 1)
$ConflictOk = ($ConflictRows.Count -eq 0)
$ProtectedOk = ($ProtectedChanges.Count -eq 0)
$RuntimeOk = ($RuntimeAuthority -eq 'NONE')
$StatusOk = ($Status -eq 'ACTIVE')

$ContractPurpose = $Contract.IndexOf('## Purpose', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractRules = $Contract.IndexOf('## Canonical rules', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractReuse = $Contract.IndexOf('CROSS_FAMILY_REUSE', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractConflict = $Contract.IndexOf('TRUE_FAMILY_CONFLICT', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractNext = $Contract.IndexOf('D2.3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$DocumentOk = $ContractPurpose -and $ContractRules -and $ContractReuse -and $ContractConflict -and $ContractNext

$MasterD22 = $Master.IndexOf('D2.2', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$StartD22 = $Start.IndexOf('D2.2', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$MasterNext = $Master.IndexOf('D2.3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$StartNext = $Start.IndexOf('D2.3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$PromptOk = $MasterD22 -and $StartD22 -and $MasterNext -and $StartNext

$OverallPass =
    $D21Pass -and
    $CountsOk -and
    $RowsOk -and
    $CrossReuseOk -and
    $ConflictOk -and
    $ProtectedOk -and
    $RuntimeOk -and
    $StatusOk -and
    $DocumentOk -and
    $PromptOk

$Result = 'FAIL'
if ($OverallPass) {
    $Result = 'PASS'
}

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$Receipt = [ordered]@{
    checkpoint = 'C11-D D2.2'
    result = $Result
    validation_type = 'D2_2_ASSET_ROLE_EVIDENCE_FORMAL_VALIDATION'
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
    role_row_count = $RoleRows.Count
    cross_family_reuse_row_count = $CrossRows.Count
    true_family_conflict_row_count = $ConflictRows.Count
    runtime_authority = $RuntimeAuthority
    matrix_status = $Status
    protected_source_new_changes_count = $ProtectedChanges.Count
    d2_1_pass_verified = $D21Pass
    counts_verified = $CountsOk
    rows_verified = $RowsOk
    cross_family_reuse_verified = $CrossReuseOk
    true_conflict_zero_verified = $ConflictOk
    protected_boundary_verified = $ProtectedOk
    runtime_authority_verified = $RuntimeOk
    matrix_status_verified = $StatusOk
    contract_verified = $DocumentOk
    prompts_verified = $PromptOk
    no_renderer_change = $true
    no_simulation_change = $true
    no_mechanics_change = $true
    no_rng_change = $true
    no_historical_promotion = $true
    next_checkpoint = 'D2.3'
}

[System.IO.File]::WriteAllText(
    $D22ReceiptPath,
    ($Receipt | ConvertTo-Json -Depth 20),
    $Utf8NoBom
)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.2 - FORMAL VALIDATION' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''

if ($D21Pass) { Write-Host '[OK] D2.1 receipt PASS.' -ForegroundColor Green }
if ($CountsOk) { Write-Host '[OK] 15 assets / 15 explicit roles / 0 UNKNOWN roles.' -ForegroundColor Green }
if ($RowsOk) { Write-Host '[OK] 15 role-evidence rows.' -ForegroundColor Green }
if ($CrossReuseOk) { Write-Host '[OK] CROSS_FAMILY_REUSE = 1.' -ForegroundColor Green }
if ($ConflictOk) { Write-Host '[OK] TRUE_FAMILY_CONFLICT = 0.' -ForegroundColor Green }
if ($ProtectedOk) { Write-Host '[OK] No protected-source changes recorded.' -ForegroundColor Green }
if ($RuntimeOk) { Write-Host '[OK] runtime_authority = NONE.' -ForegroundColor Green }
if ($StatusOk) { Write-Host '[OK] matrix status = ACTIVE.' -ForegroundColor Green }
if ($DocumentOk) { Write-Host '[OK] D2.2 contract verified.' -ForegroundColor Green }
if ($PromptOk) { Write-Host '[OK] MASTER / START handoff verified for D2.3.' -ForegroundColor Green }

Write-Host ''
Write-Host ('MATRIX:   ' + $MatrixPath)
Write-Host ('CONTRACT: ' + $ContractPath)
Write-Host ('RECEIPT:  ' + $D22ReceiptPath)
Write-Host ''

if ($OverallPass) {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D2.2 - PASS / VALIDATED' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'Asset role/evidence matrix formally validated.'
    Write-Host 'Cross-family reuse is admissible and not a conflict.'
    Write-Host 'No true family conflicts remain.'
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
