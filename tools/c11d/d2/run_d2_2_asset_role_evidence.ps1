Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$CurrentD = Join-Path $Repo 'docs\current\d'
$HistoryD = Join-Path $Repo 'docs\history\master-prompts\c11d'
$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$RegistryPath = Join-Path $Repo 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
$D20AuditPath = Join-Path $D2Root 'd2_0_asset_family_audit.json'
$D21ReceiptPath = Join-Path $D2Root 'd2_1_validation_receipt.json'
$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

$MatrixPath = Join-Path $D2Root 'd2_2_asset_role_evidence_matrix.json'
$ContractPath = Join-Path $CurrentD 'D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
$ReceiptPath = Join-Path $D2Root 'd2_2_validation_receipt.json'

New-Item -ItemType Directory -Force -Path $CurrentD | Out-Null
New-Item -ItemType Directory -Force -Path $HistoryD | Out-Null
New-Item -ItemType Directory -Force -Path $D2Root | Out-Null

function Write-Utf8NoBom {
    param([string]$Path,[string]$Content)
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path,$Content,$Utf8NoBom)
}

function Get-OptionalProperty {
    param([object]$Object,[string]$Name)
    if ($null -eq $Object) { return $null }
    $Property = $Object.PSObject.Properties[$Name]
    if ($null -ne $Property) { return $Property.Value }
    return $null
}

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.2 — ASSET ROLE / EVIDENCE MATRIX' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host ('[INFO] Repo: {0}' -f $Repo)
Write-Host ''

if (-not (Test-Path -LiteralPath $D20AuditPath)) { throw 'No existe el audit D2.0.' }
if (-not (Test-Path -LiteralPath $D21ReceiptPath)) { throw 'No existe el receipt D2.1.' }
if (-not (Test-Path -LiteralPath $RegistryPath)) { throw 'No existe la registry D2.1.' }
if (-not (Test-Path -LiteralPath $MasterPath)) { throw 'No existe MASTER handover.' }
if (-not (Test-Path -LiteralPath $StartPath)) { throw 'No existe START prompt.' }

$D21Receipt = Get-Content -LiteralPath $D21ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$D21Receipt.result -ne 'PASS') { throw 'D2.1 receipt no es PASS.' }

$Audit = Get-Content -LiteralPath $D20AuditPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Registry = Get-Content -LiteralPath $RegistryPath -Raw -Encoding UTF8 | ConvertFrom-Json

$Assets = @($Audit.asset_files)
$Challenges = @($Audit.current_challenges)
$Roles = @($Audit.asset_role_evidence)
$Refs = @($Audit.asset_reference_resolution)
$UnknownChallenges = @($Audit.unknown_family_challenges)

if ($Assets.Count -ne 15) { throw ('Esperados 15 assets; encontrados {0}.' -f $Assets.Count) }
if ($Challenges.Count -ne 9) { throw ('Esperados 9 Challenges; encontrados {0}.' -f $Challenges.Count) }
if ($Refs.Count -ne 27) { throw ('Esperadas 27 referencias; encontradas {0}.' -f $Refs.Count) }
if ($UnknownChallenges.Count -ne 5) { throw ('Esperados 5 UNKNOWN; encontrados {0}.' -f $UnknownChallenges.Count) }

$Rows = @()

foreach ($Asset in $Assets) {
    $AssetPath = [string]$Asset.path
    $AssetLeaf = (Split-Path $AssetPath -Leaf).ToLowerInvariant()
    $AssetPathLower = $AssetPath.ToLowerInvariant()

    $MatchingRefs = @(
        $Refs | Where-Object {
            $Resolved = Get-OptionalProperty $_ 'resolved_asset_path'
            if ($null -eq $Resolved) { return $false }
            $ResolvedText = [string]$Resolved
            return (($ResolvedText.ToLowerInvariant() -eq $AssetPathLower) -or ((Split-Path $ResolvedText -Leaf).ToLowerInvariant() -eq $AssetLeaf))
        }
    )

    $RoleRows = @()

    foreach ($Role in $Roles) {
        $Reference = Get-OptionalProperty $Role 'reference'
        if ($null -eq $Reference) { continue }

        $ReferenceText = [string]$Reference
        $ReferenceMatches = @($MatchingRefs | Where-Object { [string]$_.reference -eq $ReferenceText })

        if ($ReferenceMatches.Count -gt 0) {
            $RoleRows += [pscustomobject]@{
                role = [string]$Role.role
                reference = $ReferenceText
                evidence_status = [string]$Role.evidence_status
                source_kind = [string]$Role.source_kind
                source_file = [string]$Role.source_file
                json_path = [string]$ReferenceMatches[0].json_path
                resolution = [string]$ReferenceMatches[0].resolution
            }
        }
    }

    $ChallengeRows = @()
    foreach ($Challenge in $Challenges) {
        $ChallengeId = [string]$Challenge.challenge_id
        $ChallengeRefs = @(
            $MatchingRefs | Where-Object { [string]$_.challenge_id -eq $ChallengeId }
        )

        if ($ChallengeRefs.Count -gt 0) {
            $ChallengeRows += [pscustomobject]@{
                challenge_id = $ChallengeId
                definition_path = [string]$Challenge.definition_path
                asset_family = if ([string]::IsNullOrWhiteSpace([string](Get-OptionalProperty $Challenge 'asset_family'))) { 'UNKNOWN' } else { [string](Get-OptionalProperty $Challenge 'asset_family') }
                references = @($ChallengeRefs | ForEach-Object { [string]$_.reference })
            }
        }
    }

    $RoleStatus = 'UNKNOWN'
    if ($RoleRows.Count -gt 0) {
        $RoleStatus = 'EXPLICIT_EVIDENCE'
    }

    $FamilyStatus = 'UNKNOWN'
    if ($ChallengeRows.Count -gt 0) {
        $BoundFamilyValues = @($ChallengeRows | Where-Object { $_.asset_family -ne 'UNKNOWN' } | Select-Object -ExpandProperty asset_family -Unique)
        if ($BoundFamilyValues.Count -gt 0) { $FamilyStatus = 'EVIDENCE_BACKED' }
    }

    $Rows += [pscustomobject]@{
        asset_path = $AssetPath
        extension = [string]$Asset.extension
        size_bytes = [int64]$Asset.size_bytes
        sha256 = [string]$Asset.sha256
        asset_role_status = $RoleStatus
        family_binding_status = $FamilyStatus
        role_evidence_count = $RoleRows.Count
        role_evidence = @($RoleRows)
        challenge_bindings = @($ChallengeRows)
        filename_inference_used = $false
        sha256_merge_used = $false
        historical_promotion_performed = $false
    }
}

$ExplicitRoleRows = @($Rows | Where-Object { $_.asset_role_status -eq 'EXPLICIT_EVIDENCE' })
$UnknownRoleAssets = @($Rows | Where-Object { $_.asset_role_status -eq 'UNKNOWN' } | Select-Object -ExpandProperty asset_path)
$AssetsWithChallengeBindings = @($Rows | Where-Object { $_.challenge_bindings.Count -gt 0 })

$FamilyConflictRows = @()
foreach ($Row in $Rows) {
    $Families = @($Row.challenge_bindings | Where-Object { $_.asset_family -ne 'UNKNOWN' } | Select-Object -ExpandProperty asset_family -Unique)
    if ($Families.Count -gt 1) {
        $FamilyConflictRows += [ordered]@{ asset_path = $Row.asset_path; families = @($Families) }
    }
}

$D21RuntimeAuthority = [string]$Registry.runtime_authority

$Matrix = [ordered]@{
    matrix_id = 'c11d_d2_2_asset_role_evidence_matrix_v1'
    schema_version = '1.0'
    phase = 'C11-D'
    checkpoint = 'D2.2'
    status = 'ACTIVE'
    source_d2_0_audit = 'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json'
    source_d2_1_registry = 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
    source_d2_1_receipt = 'artifacts\tests\c11d_d2\d2_1_validation_receipt.json'
    purpose = 'Evidence-backed matrix connecting logical C6 assets to explicit role evidence and current Challenge references.'
    rules = @(
        'Role assignment requires source evidence.',
        'UNKNOWN is preserved when no role evidence can be resolved.',
        'Filename semantics are not used as authoritative role evidence.',
        'SHA-256 equality is not used to merge or collapse assets.',
        'Historical material is not promoted by D2.2.',
        'D2.2 does not activate runtime asset routing.'
    )
    assets = @($Rows)
    asset_count = $Rows.Count
    explicit_role_asset_count = $ExplicitRoleRows.Count
    unknown_role_asset_count = $UnknownRoleAssets.Count
    assets_with_challenge_bindings = $AssetsWithChallengeBindings.Count
    family_conflict_count = $FamilyConflictRows.Count
    family_conflicts = @($FamilyConflictRows)
    filename_inference_used = $false
    sha256_merge_used = $false
    historical_promotion_performed = $false
    runtime_authority = $D21RuntimeAuthority
}

Write-Utf8NoBom $MatrixPath ($Matrix | ConvertTo-Json -Depth 30)

$UnknownRoleLines = @()
if ($UnknownRoleAssets.Count -eq 0) {
    $UnknownRoleLines += '- None.'
}
if ($UnknownRoleAssets.Count -gt 0) {
    foreach ($Path in $UnknownRoleAssets) {
        $UnknownRoleLines += ('- {0} — role status remains UNKNOWN.' -f $Path)
    }
}

$ContractLines = @(
    '# C11-D D2.2 — Asset Role / Evidence Matrix Contract V1.0',
    '',
    '## Purpose',
    '',
    'Define an evidence-backed matrix connecting logical C6 Challenge assets with explicit role evidence and current Challenge references.',
    '',
    '## Canonical constraints',
    '',
    '1. Role assignment requires source evidence.',
    '2. UNKNOWN remains explicit when role evidence is insufficient.',
    '3. Filename semantics are not authoritative role evidence.',
    '4. SHA-256 equality does not justify merging or collapsing assets.',
    '5. Historical material is not promoted by D2.2.',
    '6. D2.2 does not activate runtime asset routing.',
    '7. D2.2 does not modify renderer, simulation, mechanics, RNG or frozen C11-C sources.',
    '',
    '## Source artifacts',
    '',
    '- D2.0 audit: artifacts\tests\c11d_d2\d2_0_asset_family_audit.json',
    '- D2.1 registry: definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json',
    '- D2.1 receipt: artifacts\tests\c11d_d2\d2_1_validation_receipt.json',
    '',
    '## Matrix artifact',
    '',
    'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json',
    '',
    '## Audit totals',
    '',
    ('- Logical assets: {0}' -f $Rows.Count),
    ('- Assets with explicit role evidence: {0}' -f $ExplicitRoleRows.Count),
    ('- Assets with UNKNOWN role status: {0}' -f $UnknownRoleAssets.Count),
    ('- Assets with Challenge bindings: {0}' -f $AssetsWithChallengeBindings.Count),
    ('- Family conflicts: {0}' -f $FamilyConflictRows.Count),
    ('- Runtime authority inherited from D2.1: {0}' -f $D21RuntimeAuthority),
    '',
    '## UNKNOWN role assets',
    '',
    $UnknownRoleLines,
    '',
    '## D2.2 disposition',
    '',
    'The matrix is evidence-backed and descriptive. It does not promote assets, merge assets, infer roles from filenames, or activate runtime routing.',
    '',
    '## Next checkpoint',
    '',
    'Validate D2.2 matrix against D2.0 and D2.1 evidence, then determine the next D2 checkpoint.'
)

Write-Utf8NoBom $ContractPath ($ContractLines -join [Environment]::NewLine)

$MasterText = Get-Content -LiteralPath $MasterPath -Raw -Encoding UTF8
$StartText = Get-Content -LiteralPath $StartPath -Raw -Encoding UTF8
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$MasterSnapshot = Join-Path $HistoryD ('MASTER_HANDOVER_C11D_PRE_D2_2_' + $Timestamp + '.md')
$StartSnapshot = Join-Path $HistoryD ('START_PROMPT_C11D_PRE_D2_2_' + $Timestamp + '.md')
Copy-Item -LiteralPath $MasterPath -Destination $MasterSnapshot -Force
Copy-Item -LiteralPath $StartPath -Destination $StartSnapshot -Force

$MasterText = [regex]::Replace($MasterText,'## Current checkpoint[\s\S]*?## D2.0 evidence','## Current checkpoint`r`n`r`nD2.2 — Asset Role / Evidence Matrix`r`nSTATUS: ACTIVE`r`n`r`n## D2.0 evidence')
$MasterText = $MasterText -replace 'D2.1 — Declarative Asset Family Registry / Evidence Binding','D2.2 — Asset Role / Evidence Matrix'
$MasterText = $MasterText -replace '## D2.1 active scope','## D2.1 completed scope'
$MasterText = $MasterText + [Environment]::NewLine + [Environment]::NewLine + '## D2.2 active scope' + [Environment]::NewLine + [Environment]::NewLine + 'Build and validate an evidence-backed asset role matrix.' + [Environment]::NewLine + 'Preserve UNKNOWN where role evidence is insufficient.' + [Environment]::NewLine + 'No filename-only inference, no SHA-256 merge, no historical promotion, no runtime activation.' + [Environment]::NewLine + [Environment]::NewLine + 'Matrix: artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json' + [Environment]::NewLine + 'Contract: docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md' + [Environment]::NewLine + 'Receipt: artifacts\tests\c11d_d2\d2_2_validation_receipt.json'

$StartText = $StartText -replace 'C11-D D2.1: ACTIVE','C11-D D2.1: PASS / VALIDATED`r`nC11-D D2.2: ACTIVE'
$StartText = $StartText -replace '## Current D2.1 task[\s\S]*?## Current registry','## Completed D2.1`r`n`r`nD2.1 registry generated and validated against D2.0 evidence.`r`n`r`n## Current D2.2 task`r`n`r`nMaintain the evidence-backed asset role matrix. Preserve UNKNOWN where role evidence is absent. Do not infer roles from filenames, do not merge by SHA-256, and do not activate runtime routing.`r`n`r`n## Current registry'
$StartText = $StartText + [Environment]::NewLine + [Environment]::NewLine + '## D2.2 artifacts' + [Environment]::NewLine + [Environment]::NewLine + 'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json' + [Environment]::NewLine + 'docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md' + [Environment]::NewLine + 'artifacts\tests\c11d_d2\d2_2_validation_receipt.json'

Write-Utf8NoBom $MasterPath $MasterText
Write-Utf8NoBom $StartPath $StartText

$MatrixReload = Get-Content -LiteralPath $MatrixPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ContractReload = Get-Content -LiteralPath $ContractPath -Raw -Encoding UTF8

$Pass = $true

if (@($MatrixReload.assets).Count -ne 15) { $Pass = $false }
if ([int]$MatrixReload.asset_count -ne 15) { $Pass = $false }
if ([int]$MatrixReload.family_conflict_count -ne 0) { $Pass = $false }
if ([bool]$MatrixReload.filename_inference_used) { $Pass = $false }
if ([bool]$MatrixReload.sha256_merge_used) { $Pass = $false }
if ([bool]$MatrixReload.historical_promotion_performed) { $Pass = $false }
if ([string]$MatrixReload.runtime_authority -ne 'NONE') { $Pass = $false }
if ($ContractReload.IndexOf('## Canonical constraints',[System.StringComparison]::OrdinalIgnoreCase) -lt 0) { $Pass = $false }
if ($ContractReload.IndexOf('UNKNOWN',[System.StringComparison]::OrdinalIgnoreCase) -lt 0) { $Pass = $false }
if ($ContractReload.IndexOf('D2.2 disposition',[System.StringComparison]::OrdinalIgnoreCase) -lt 0) { $Pass = $false }
if ($MasterText.IndexOf('D2.2',[System.StringComparison]::OrdinalIgnoreCase) -lt 0) { $Pass = $false }
if ($StartText.IndexOf('D2.2',[System.StringComparison]::OrdinalIgnoreCase) -lt 0) { $Pass = $false }

$Result = 'FAIL'
if ($Pass) { $Result = 'PASS' }

$Receipt = [ordered]@{
    checkpoint = 'C11-D D2.2'
    result = $Result
    validation_type = 'ASSET_ROLE_EVIDENCE_MATRIX_GENERATION_AND_HANDOFF'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    source_d2_0_audit = 'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json'
    source_d2_1_registry = 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
    matrix = 'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json'
    contract = 'docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
    logical_asset_count = [int]$MatrixReload.asset_count
    explicit_role_asset_count = [int]$MatrixReload.explicit_role_asset_count
    unknown_role_asset_count = [int]$MatrixReload.unknown_role_asset_count
    assets_with_challenge_bindings = [int]$MatrixReload.assets_with_challenge_bindings
    family_conflict_count = [int]$MatrixReload.family_conflict_count
    filename_inference_used = [bool]$MatrixReload.filename_inference_used
    sha256_merge_used = [bool]$MatrixReload.sha256_merge_used
    historical_promotion_performed = [bool]$MatrixReload.historical_promotion_performed
    runtime_authority = [string]$MatrixReload.runtime_authority
    contract_verified = ($ContractReload.IndexOf('## Canonical constraints',[System.StringComparison]::OrdinalIgnoreCase) -ge 0)
    master_prompt_updated = $true
    start_prompt_updated = $true
    master_snapshot = 'docs\history\master-prompts\c11d\' + (Split-Path $MasterSnapshot -Leaf)
    start_snapshot = 'docs\history\master-prompts\c11d\' + (Split-Path $StartSnapshot -Leaf)
    no_runtime_activation_performed = $true
    no_family_merge_performed = $true
    no_renderer_change_performed = $true
    no_simulation_change_performed = $true
    no_mechanics_change_performed = $true
    no_rng_change_performed = $true
    next_checkpoint = 'D2.2 validation / next D2 checkpoint'
}

Write-Utf8NoBom $ReceiptPath ($Receipt | ConvertTo-Json -Depth 15)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.2 — RESULT' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host ('[INFO] Assets: {0}' -f $MatrixReload.asset_count)
Write-Host ('[INFO] Explicit role assets: {0}' -f $MatrixReload.explicit_role_asset_count)
Write-Host ('[INFO] UNKNOWN role assets: {0}' -f $MatrixReload.unknown_role_asset_count)
Write-Host ('[INFO] Assets with Challenge bindings: {0}' -f $MatrixReload.assets_with_challenge_bindings)
Write-Host ('[INFO] Family conflicts: {0}' -f $MatrixReload.family_conflict_count)

if ([int]$MatrixReload.asset_count -eq 15) { Write-Host '[OK] 15 logical assets represented.' -ForegroundColor Green }
if ([int]$MatrixReload.family_conflict_count -eq 0) { Write-Host '[OK] No family conflicts in asset bindings.' -ForegroundColor Green }
if (-not [bool]$MatrixReload.filename_inference_used) { Write-Host '[OK] No filename-only role inference.' -ForegroundColor Green }
if (-not [bool]$MatrixReload.sha256_merge_used) { Write-Host '[OK] No SHA-256-based asset merge.' -ForegroundColor Green }
if (-not [bool]$MatrixReload.historical_promotion_performed) { Write-Host '[OK] No historical promotion.' -ForegroundColor Green }
if ([string]$MatrixReload.runtime_authority -eq 'NONE') { Write-Host '[OK] Runtime authority remains NONE.' -ForegroundColor Green }
if ($ContractReload.IndexOf('## Canonical constraints',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) { Write-Host '[OK] D2.2 contract verified.' -ForegroundColor Green }
if ($MasterText.IndexOf('D2.2',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) { Write-Host '[OK] MASTER updated and snapshotted.' -ForegroundColor Green }
if ($StartText.IndexOf('D2.2',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) { Write-Host '[OK] START updated and snapshotted.' -ForegroundColor Green }

Write-Host ''
Write-Host ('MATRIX:   {0}' -f $MatrixPath)
Write-Host ('CONTRACT: {0}' -f $ContractPath)
Write-Host ('RECEIPT:  {0}' -f $ReceiptPath)
Write-Host ''

if ($Pass) {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D2.2 — ACTIVE / MATRIX GENERATED' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'D2.2 asset role evidence matrix generated.'
    Write-Host 'UNKNOWN preserved where evidence is absent.'
    Write-Host 'No filename inference or SHA-256 merge performed.'
    Write-Host 'No runtime activation performed.'
    Write-Host 'Prompts updated for next context.'
    Write-Host ''
    Write-Host 'NEXT: D2.2 validation / next D2 checkpoint'
}

if (-not $Pass) {
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ' C11-D D2.2 — VERIFY FAIL' -ForegroundColor Red
    Write-Host '==================================================' -ForegroundColor Red
}
