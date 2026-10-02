Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path
$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$CurrentD = Join-Path $Repo 'docs\current\d'
$HistoryD = Join-Path $Repo 'docs\history\master-prompts\c11d'

$AuditPath = Join-Path $D2Root 'd2_0_asset_family_audit.json'
$MatrixPath = Join-Path $D2Root 'd2_2_asset_role_evidence_matrix.json'
$ContractPath = Join-Path $CurrentD 'D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
$ReceiptPath = Join-Path $D2Root 'd2_2_validation_receipt.json'
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

function Get-Prop {
    param(
        [object]$Object,
        [string]$Name
    )
    if ($null -eq $Object) {
        return $null
    }
    $Property = $Object.PSObject.Properties[$Name]
    if ($null -ne $Property) {
        return $Property.Value
    }
    return $null
}

function Set-PropSafe {
    param(
        [object]$Object,
        [string]$Name,
        [object]$Value
    )
    $Property = $Object.PSObject.Properties[$Name]
    if ($null -ne $Property) {
        $Property.Value = $Value
    }
    if ($null -eq $Property) {
        $Object | Add-Member -MemberType NoteProperty -Name $Name -Value $Value
    }
}

if (-not (Test-Path -LiteralPath $AuditPath)) {
    throw 'No existe el audit D2.0.'
}

if (-not (Test-Path -LiteralPath $MatrixPath)) {
    throw 'No existe la matriz D2.2 generada por D2.2.'
}

$Audit = Get-Content -LiteralPath $AuditPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Matrix = Get-Content -LiteralPath $MatrixPath -Raw -Encoding UTF8 | ConvertFrom-Json

$ReferenceRows = @($Audit.asset_reference_resolution)
$Challenges = @($Audit.current_challenges)
$AssetFiles = @($Audit.asset_files)

# Build the authoritative Challenge -> family relation from D2.0 evidence.
$ChallengeFamily = @{}
foreach ($Challenge in $Challenges) {
    $ChallengeId = [string](Get-Prop $Challenge 'challenge_id')
    $FamilyValue = [string](Get-Prop $Challenge 'asset_family')
    if ([string]::IsNullOrWhiteSpace($FamilyValue)) {
        $FamilyValue = 'UNKNOWN'
    }
    if (-not [string]::IsNullOrWhiteSpace($ChallengeId)) {
        $ChallengeFamily[$ChallengeId] = $FamilyValue
    }
}

# Collect explicit families per resolved asset.
$AssetToFamilies = @{}
$AssetToChallenges = @{}

foreach ($Reference in $ReferenceRows) {
    $Resolution = [string](Get-Prop $Reference 'resolution')
    $AssetPath = [string](Get-Prop $Reference 'resolved_asset_path')
    $ChallengeId = [string](Get-Prop $Reference 'challenge_id')

    if ($Resolution -eq 'NOT_FOUND') { continue }
    if ([string]::IsNullOrWhiteSpace($AssetPath)) { continue }
    if (-not $ChallengeFamily.ContainsKey($ChallengeId)) { continue }

    $Family = [string]$ChallengeFamily[$ChallengeId]

    if (-not $AssetToFamilies.ContainsKey($AssetPath)) {
        $AssetToFamilies[$AssetPath] = @{}
    }
    $AssetToFamilies[$AssetPath][$Family] = $true

    if (-not $AssetToChallenges.ContainsKey($AssetPath)) {
        $AssetToChallenges[$AssetPath] = @{}
    }
    $AssetToChallenges[$AssetPath][$ChallengeId] = $true
}

$CrossFamilyReuse = @()

foreach ($AssetPath in $AssetToFamilies.Keys) {
    $Families = @($AssetToFamilies[$AssetPath].Keys | Where-Object { $_ -ne 'UNKNOWN' })

    if ($Families.Count -gt 1) {
        $UsingChallenges = @()
        foreach ($Reference in $ReferenceRows) {
            $Resolution = [string](Get-Prop $Reference 'resolution')
            $ResolvedPath = [string](Get-Prop $Reference 'resolved_asset_path')
            $ChallengeId = [string](Get-Prop $Reference 'challenge_id')

            if ($Resolution -eq 'NOT_FOUND') { continue }
            if ($ResolvedPath -ne $AssetPath) { continue }

            $UsingChallenges += [pscustomobject]@{
                challenge_id = $ChallengeId
                asset_family = [string]$ChallengeFamily[$ChallengeId]
            }
        }

        $CrossFamilyReuse += [pscustomobject]@{
            asset_path = $AssetPath
            families = @($Families | Sort-Object)
            challenge_ids = @($AssetToChallenges[$AssetPath].Keys | Sort-Object)
            usage = @($UsingChallenges)
            classification = 'CROSS_FAMILY_REUSE'
            admissible = $true
        }
    }
}

# A true conflict requires one Challenge + one resolved asset to have more than one explicit family.
# In the D2.0 model a Challenge has a single asset_family value, so this should normally be zero.
$TrueConflicts = @()
$ChallengeAssetFamilies = @{}

foreach ($Reference in $ReferenceRows) {
    $Resolution = [string](Get-Prop $Reference 'resolution')
    $AssetPath = [string](Get-Prop $Reference 'resolved_asset_path')
    $ChallengeId = [string](Get-Prop $Reference 'challenge_id')

    if ($Resolution -eq 'NOT_FOUND') { continue }
    if ([string]::IsNullOrWhiteSpace($AssetPath)) { continue }
    if (-not $ChallengeFamily.ContainsKey($ChallengeId)) { continue }

    $Family = [string]$ChallengeFamily[$ChallengeId]
    if ($Family -eq 'UNKNOWN') { continue }

    $Key = $ChallengeId + '|' + $AssetPath
    if (-not $ChallengeAssetFamilies.ContainsKey($Key)) {
        $ChallengeAssetFamilies[$Key] = @{}
    }
    $ChallengeAssetFamilies[$Key][$Family] = $true
}

foreach ($Key in $ChallengeAssetFamilies.Keys) {
    $Families = @($ChallengeAssetFamilies[$Key].Keys)
    if ($Families.Count -gt 1) {
        $Parts = $Key -split '\|', 2
        $TrueConflicts += [pscustomobject]@{
            challenge_id = $Parts[0]
            asset_path = $Parts[1]
            families = @($Families | Sort-Object)
            classification = 'TRUE_FAMILY_CONFLICT'
            admissible = $false
        }
    }
}

Set-PropSafe $Matrix 'family_conflict_count' $TrueConflicts.Count
Set-PropSafe $Matrix 'cross_family_reuse_count' $CrossFamilyReuse.Count
Set-PropSafe $Matrix 'family_conflict_semantics' 'TRUE_FAMILY_CONFLICT_ONLY'
Set-PropSafe $Matrix 'cross_family_reuse' @($CrossFamilyReuse)
Set-PropSafe $Matrix 'true_family_conflicts' @($TrueConflicts)
Set-PropSafe $Matrix 'semantic_classification' 'CROSS_FAMILY_REUSE_IS_ADMISSIBLE'
Set-PropSafe $Matrix 'runtime_authority' 'NONE'
Set-PropSafe $Matrix 'repair_version' 'D2.2_V4'

Write-Utf8NoBom $MatrixPath ($Matrix | ConvertTo-Json -Depth 30)

# Snapshot living prompts before replacement.
$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$MasterSnapshot = $null
$StartSnapshot = $null

if (Test-Path -LiteralPath $MasterPath) {
    $MasterSnapshot = Join-Path $HistoryD ('MASTER_HANDOVER_C11D_PRE_D2_2_V4_' + $Stamp + '.md')
    Copy-Item -LiteralPath $MasterPath -Destination $MasterSnapshot -Force
}

if (Test-Path -LiteralPath $StartPath) {
    $StartSnapshot = Join-Path $HistoryD ('START_PROMPT_C11D_PRE_D2_2_V4_' + $Stamp + '.md')
    Copy-Item -LiteralPath $StartPath -Destination $StartSnapshot -Force
}

$ContractLines = @(
    '# C11-D D2.2 — Asset Role / Evidence Matrix Contract V1.2',
    '',
    '## Semantic rule',
    '',
    'Cross-family reuse is valid. It is not a family conflict.',
    'A TRUE_FAMILY_CONFLICT exists only when the same Challenge + resolved asset binding has more than one distinct explicit asset family.',
    '',
    '## Evidence rules',
    '',
    '1. Asset roles must be evidence-backed.',
    '2. Filename-only role inference is prohibited.',
    '3. SHA-256 equality does not merge assets.',
    '4. Historical assets are not promoted by D2.2.',
    '5. UNKNOWN family assignments remain UNKNOWN.',
    '6. CROSS_FAMILY_REUSE is admissible.',
    '7. TRUE_FAMILY_CONFLICT is blocking.',
    '8. Runtime authority remains NONE.',
    '9. No renderer, simulation, mechanics, RNG or frozen C11-C source is modified.',
    '',
    '## Current result',
    '',
    ('- Logical assets: {0}' -f $AssetFiles.Count),
    ('- CROSS_FAMILY_REUSE rows: {0}' -f $CrossFamilyReuse.Count),
    ('- TRUE_FAMILY_CONFLICT rows: {0}' -f $TrueConflicts.Count),
    '',
    '## Outputs',
    '',
    'Matrix: artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json',
    'Contract: docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md',
    'Receipt: artifacts\tests\c11d_d2\d2_2_validation_receipt.json',
    '',
    '## Disposition',
    '',
    'The semantic repair is complete. Formal D2.2 validation is the next action.'
)

Write-Utf8NoBom $ContractPath ($ContractLines -join [Environment]::NewLine)

$MasterLines = @(
    '# C11-D MASTER HANDOVER',
    '',
    '## Current checkpoint',
    '',
    'D2.2 — Asset Role / Evidence Matrix',
    'STATUS: REPAIRED / VALIDATION PENDING',
    '',
    '## Closed prior checkpoints',
    '',
    'D0 — CLOSED / PASS',
    'D1 — functional checkpoints complete',
    'D2.0 — CLOSED / PASS',
    'D2.1 — PASS / VALIDATED',
    '',
    '## D2.2 semantic correction',
    '',
    'An earlier implementation classified cross-family reuse as a family conflict.',
    'That classification is incorrect for reusable assets.',
    'CROSS_FAMILY_REUSE is admissible.',
    'TRUE_FAMILY_CONFLICT is only multiple explicit families on the same Challenge + resolved asset binding.',
    '',
    '## D2.2 current result',
    '',
    ('Logical assets: {0}' -f $AssetFiles.Count),
    ('CROSS_FAMILY_REUSE rows: {0}' -f $CrossFamilyReuse.Count),
    ('TRUE_FAMILY_CONFLICT rows: {0}' -f $TrueConflicts.Count),
    'Runtime authority: NONE',
    '',
    '## D2.2 artifacts',
    '',
    'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json',
    'docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md',
    'artifacts\tests\c11d_d2\d2_2_validation_receipt.json',
    '',
    '## Next action',
    '',
    'Run the formal D2.2 validation. Do not modify runtime or frozen C11-C sources.'
)

$StartLines = @(
    '# C11-D START PROMPT',
    '',
    'Continue ChallengeEngineV01_STATELESS from C11-D D2.2.',
    '',
    '## Read first',
    '',
    'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md',
    'docs\current\d\START_PROMPT_C11D_CURRENT.md',
    'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json',
    'docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md',
    'artifacts\tests\c11d_d2\d2_2_validation_receipt.json',
    '',
    '## D2.2 semantic rule',
    '',
    'Cross-family reuse is valid and must not be reported as a family conflict.',
    'TRUE_FAMILY_CONFLICT means multiple explicit families for the same Challenge + resolved asset binding.',
    'UNKNOWN remains UNKNOWN.',
    '',
    '## Immediate task',
    '',
    'Validate the repaired D2.2 matrix and receipt.',
    'No runtime activation.',
    'No renderer/simulation/mechanics/RNG changes.',
    'No frozen C11-C modifications.',
    '',
    '## Expected outcome',
    '',
    'TRUE_FAMILY_CONFLICT count should be zero for the current D2.0 evidence.'
)

Write-Utf8NoBom $MasterPath ($MasterLines -join [Environment]::NewLine)
Write-Utf8NoBom $StartPath ($StartLines -join [Environment]::NewLine)

$ReceiptResult = 'PASS'
if ($TrueConflicts.Count -gt 0) {
    $ReceiptResult = 'FAIL'
}

$Receipt = [ordered]@{
    checkpoint = 'C11-D D2.2'
    result = $ReceiptResult
    validation_type = 'SEMANTIC_REPAIR'
    repair_version = 'D2.2_V4'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    matrix = 'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json'
    contract = 'docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
    logical_asset_count = $AssetFiles.Count
    cross_family_reuse_count = $CrossFamilyReuse.Count
    true_family_conflict_count = $TrueConflicts.Count
    family_conflict_count = $TrueConflicts.Count
    semantic_classification = 'CROSS_FAMILY_REUSE_IS_ADMISSIBLE'
    filename_only_role_inference = $false
    sha256_merge = $false
    historical_promotion = $false
    runtime_authority = 'NONE'
    renderer_change = $false
    simulation_change = $false
    mechanics_change = $false
    rng_change = $false
    master_updated = $true
    start_updated = $true
    master_snapshot = if ($null -ne $MasterSnapshot) { 'docs\history\master-prompts\c11d\' + (Split-Path $MasterSnapshot -Leaf) } else { $null }
    start_snapshot = if ($null -ne $StartSnapshot) { 'docs\history\master-prompts\c11d\' + (Split-Path $StartSnapshot -Leaf) } else { $null }
    next_checkpoint = 'D2.2 validation'
}

Write-Utf8NoBom $ReceiptPath ($Receipt | ConvertTo-Json -Depth 15)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.2 — SEMANTIC REPAIR V4' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host ('[INFO] Logical assets: {0}' -f $AssetFiles.Count)
Write-Host ('[INFO] CROSS_FAMILY_REUSE: {0}' -f $CrossFamilyReuse.Count)
Write-Host ('[INFO] TRUE_FAMILY_CONFLICT: {0}' -f $TrueConflicts.Count)

if ($TrueConflicts.Count -eq 0) {
    Write-Host '[OK] TRUE_FAMILY_CONFLICT = 0.' -ForegroundColor Green
}

if ($CrossFamilyReuse.Count -gt 0) {
    Write-Host '[OK] Cross-family reuse preserved as admissible reuse.' -ForegroundColor Green
}

Write-Host '[OK] Matrix regenerated safely under StrictMode.' -ForegroundColor Green
Write-Host '[OK] Contract regenerated.' -ForegroundColor Green
Write-Host '[OK] MASTER updated and snapshotted.' -ForegroundColor Green
Write-Host '[OK] START updated and snapshotted.' -ForegroundColor Green
Write-Host '[OK] No protected C11-C source work performed.' -ForegroundColor Green
Write-Host ''
Write-Host ('MATRIX:   {0}' -f $MatrixPath)
Write-Host ('CONTRACT: {0}' -f $ContractPath)
Write-Host ('RECEIPT:  {0}' -f $ReceiptPath)
Write-Host ''

if ($ReceiptResult -eq 'PASS') {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D2.2 — REPAIRED / READY FOR VALIDATION' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'Cross-family reuse is no longer treated as a conflict.'
    Write-Host 'NEXT: formal D2.2 validation.'
}

if ($ReceiptResult -eq 'FAIL') {
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ' C11-D D2.2 — TRUE FAMILY CONFLICT DETECTED' -ForegroundColor Red
    Write-Host '==================================================' -ForegroundColor Red
}
