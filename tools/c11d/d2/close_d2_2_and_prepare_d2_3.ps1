Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path
$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$CurrentD = Join-Path $Repo 'docs\current\d'
$HistoryD = Join-Path $Repo 'docs\history\master-prompts\c11d'

$MatrixPath = Join-Path $D2Root 'd2_2_asset_role_evidence_matrix.json'
$D22ReceiptPath = Join-Path $D2Root 'd2_2_validation_receipt.json'
$ContractPath = Join-Path $CurrentD 'D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'

$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

$D23ContractPath = Join-Path $CurrentD 'D2.3_ASSET_FAMILY_INTEGRATION_CONTRACT.md'
$D23ReceiptPath = Join-Path $D2Root 'd2_3_handoff_receipt.json'

foreach ($Path in @($MatrixPath,$ContractPath,$MasterPath,$StartPath)) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw ('Required file missing: ' + $Path)
    }
}

$Matrix = Get-Content -LiteralPath $MatrixPath -Raw -Encoding UTF8 | ConvertFrom-Json

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

$CoreEvidencePass =
    ($AssetsCount -eq 15) -and
    ($ExplicitRoleAssets -eq 15) -and
    ($UnknownRoleAssets -eq 0) -and
    ($BoundAssets -eq 15) -and
    ($CrossReuse -eq 1) -and
    ($TrueConflicts -eq 0) -and
    ($RuntimeAuthority -eq 'NONE') -and
    ($MatrixStatus -eq 'ACTIVE') -and
    ($ProtectedChanges.Count -eq 0)

if (-not $CoreEvidencePass) {
    throw 'D2.2 core evidence does not satisfy the established contract.'
}

$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
New-Item -ItemType Directory -Force -Path $HistoryD | Out-Null

$MasterSnapshot = Join-Path $HistoryD ('MASTER_HANDOVER_C11D_PRE_D2_3_' + $Timestamp + '.md')
$StartSnapshot = Join-Path $HistoryD ('START_PROMPT_C11D_PRE_D2_3_' + $Timestamp + '.md')

Copy-Item -LiteralPath $MasterPath -Destination $MasterSnapshot -Force
Copy-Item -LiteralPath $StartPath -Destination $StartSnapshot -Force

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Content
    )

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

$ContractLines = @(
    '# C11-D D2.2 — Asset Role / Evidence Matrix Contract V1.1',
    '',
    '## Purpose',
    '',
    'Define the evidence-backed role matrix for the reusable C6 Challenge asset layer.',
    'The matrix is declarative evidence and is not runtime activation authority.',
    '',
    '## Canonical rules',
    '',
    '1. Every audited logical asset must have an explicit role assignment or an explicit UNKNOWN state.',
    '2. Filename-only inference is not authoritative.',
    '3. SHA-256 equality does not authorize asset merging.',
    '4. Cross-family reuse is valid and must not be treated as a family conflict.',
    '5. A true family conflict exists only when one Challenge binding has incompatible explicit family assignments.',
    '6. Historical material remains provenance until explicitly promoted.',
    '7. D2.2 does not change renderer, simulation, mechanics, RNG, or frozen C11-C source.',
    '',
    '## Validated evidence',
    '',
    ('- Logical assets: {0}' -f $AssetsCount),
    ('- Explicit role assets: {0}' -f $ExplicitRoleAssets),
    ('- UNKNOWN role assets: {0}' -f $UnknownRoleAssets),
    ('- Assets with Challenge bindings: {0}' -f $BoundAssets),
    ('- CROSS_FAMILY_REUSE: {0}' -f $CrossReuse),
    ('- TRUE_FAMILY_CONFLICT: {0}' -f $TrueConflicts),
    ('- Runtime authority: {0}' -f $RuntimeAuthority),
    '',
    '## D2.2 disposition',
    '',
    'The role/evidence matrix is accepted as declarative evidence for the C11-D asset layer.',
    'Cross-family reuse is admissible reuse, not a conflict.',
    'No runtime activation, renderer change, simulation change, mechanics change or RNG change is performed.',
    '',
    '## Next checkpoint',
    '',
    'D2.3 — Asset Family Integration Contract / Canonical Binding Layer.'
)

Write-Utf8NoBom $ContractPath ($ContractLines -join [Environment]::NewLine)

$MasterLines = @(
    '# C11-D MASTER HANDOVER',
    '',
    '## Current phase',
    '',
    'C11-D — Normalize Challenge production using reusable declarative assets, visual/editorial contracts and provenance patterns established across C11-C, while recovering the Challenge content originating in C11-A/C11-B.',
    '',
    '## Strategic objective',
    '',
    'Standardize the generation path so recovered Challenges and the mature Visual Loop / Visual Drill production lessons use one robust declarative production architecture.',
    'The objective is convergence of contracts and production infrastructure, not copying Visual Loop or Visual Drill identities into Challenge mechanics.',
    '',
    '## Current checkpoint',
    '',
    'D2.3 — Asset Family Integration Contract / Canonical Binding Layer',
    'STATUS: ACTIVE',
    '',
    '## Frozen baseline',
    '',
    'C11-C 2.19.12 is FROZEN and IMMUTABLE.',
    'ZIP SHA-256: D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32',
    'TREE SHA-256: 2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256',
    'build_factory.py SHA-256: 3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3',
    '',
    '## Closed state',
    '',
    'D0: CLOSED / PASS',
    'D1: functional checkpoints complete',
    'D2.0: CLOSED / PASS',
    'D2.1: PASS / VALIDATED',
    'D2.2: PASS / CLOSED',
    '',
    '## D2.2 evidence',
    '',
    'Matrix: artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json',
    'Contract: docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md',
    'Receipt: artifacts\tests\c11d_d2\d2_2_validation_receipt.json',
    '',
    'Validated D2.2 evidence:',
    '15 logical assets',
    '15 explicit role assets',
    '0 UNKNOWN role assets',
    '15 assets with Challenge bindings',
    '1 CROSS_FAMILY_REUSE',
    '0 TRUE_FAMILY_CONFLICT',
    'runtime_authority = NONE',
    '',
    '## D2.3 active scope',
    '',
    'Create the integration contract between the declarative asset-family registry and Challenge production requests.',
    'Keep asset identity, family identity, role identity and provenance as separate fields.',
    'Do not activate runtime routing yet.',
    'Do not alter renderer, simulation, mechanics, RNG, C7, C9 or frozen C11-C production.',
    '',
    '## D2.3 files',
    '',
    'Contract: docs\current\d\D2.3_ASSET_FAMILY_INTEGRATION_CONTRACT.md',
    'Handoff receipt: artifacts\tests\c11d_d2\d2_3_handoff_receipt.json',
    '',
    '## Context switching rule',
    '',
    'Read MASTER_HANDOVER_C11D_CURRENT.md first, then START_PROMPT_C11D_CURRENT.md, then D2.3 contract and handoff receipt.',
    'Living prompts must be updated at every major milestone and previous versions snapshotted under docs\history\master-prompts\c11d.',
    '',
    '## Guardrail',
    '',
    'Do not spend another checkpoint repeatedly re-validating unchanged evidence. Validate once at the boundary, record the receipt, and continue.'
)

$StartLines = @(
    '# C11-D START PROMPT',
    '',
    'Continue ChallengeEngineV01_STATELESS from C11-D D2.3.',
    '',
    '## Read first',
    '',
    'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md',
    'docs\current\d\START_PROMPT_C11D_CURRENT.md',
    'artifacts\tests\c11d_d2\d2_2_validation_receipt.json',
    'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json',
    'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json',
    'docs\current\d\D2.3_ASSET_FAMILY_INTEGRATION_CONTRACT.md',
    'artifacts\tests\c11d_d2\d2_3_handoff_receipt.json',
    '',
    '## Current state',
    '',
    'D0 = CLOSED / PASS',
    'D1 = functional checkpoints complete',
    'D2.0 = CLOSED / PASS',
    'D2.1 = PASS / VALIDATED',
    'D2.2 = PASS / CLOSED',
    'D2.3 = ACTIVE',
    '',
    '## Strategic direction',
    '',
    'C11-D normalizes Challenge video generation and absorbs mature production-contract lessons from C11-C.',
    'Visual Loop and Visual Drill families remain their own content families; their reusable production contracts are references for normalization, not Challenge family identities.',
    '',
    '## D2.3 task',
    '',
    'Define the canonical binding layer between Challenge production requests and declarative asset-family evidence.',
    'Separate asset identity, family identity, role identity and provenance.',
    'Preserve UNKNOWN where evidence is missing.',
    'Do not introduce runtime activation in this checkpoint.',
    '',
    '## Frozen guardrails',
    '',
    'Never modify renderer, simulation, mechanics, RNG, SimulationResult, winning_frame, close_calls, WinningFrameDetector, RenderedFrameStream, C7/C9 contracts, frozen C11-C presentation or frozen C11-C production.',
    '',
    '## Efficiency rule',
    '',
    'Do not repeat D2.0/D2.1/D2.2 audits unless contradictory evidence appears. Use existing receipts as the checkpoint input.',
    '',
    '## Next goal',
    '',
    'Complete D2.3 integration contract and then move toward production-request normalization and canonical pipeline convergence.'
)

Write-Utf8NoBom $MasterPath ($MasterLines -join [Environment]::NewLine)
Write-Utf8NoBom $StartPath ($StartLines -join [Environment]::NewLine)

$D22Receipt = [ordered]@{
    checkpoint = 'C11-D D2.2'
    result = 'PASS'
    validation_type = 'CONSOLIDATED_CLOSURE'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    source_matrix = 'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json'
    contract = 'docs\current\d\D2.2_ASSET_ROLE_EVIDENCE_MATRIX_CONTRACT.md'
    logical_asset_count = $AssetsCount
    explicit_role_asset_count = $ExplicitRoleAssets
    unknown_role_asset_count = $UnknownRoleAssets
    assets_with_challenge_bindings = $BoundAssets
    cross_family_reuse_count = $CrossReuse
    true_family_conflict_count = $TrueConflicts
    runtime_authority = $RuntimeAuthority
    protected_source_change_count = $ProtectedChanges.Count
    no_runtime_activation = $true
    no_renderer_change = $true
    no_simulation_change = $true
    no_mechanics_change = $true
    no_rng_change = $true
    no_historical_promotion = $true
    status = 'CLOSED'
    next_checkpoint = 'D2.3'
}

$ReceiptPath = Join-Path $D2Root 'd2_2_validation_receipt.json'
Write-Utf8NoBom $ReceiptPath ($D22Receipt | ConvertTo-Json -Depth 12)

$D23ContractLines = @(
    '# C11-D D2.3 — Asset Family Integration Contract V1.0',
    '',
    '## Purpose',
    '',
    'Define the canonical declarative binding between Challenge production requests and the reusable asset-family evidence layer.',
    '',
    '## Separation of concerns',
    '',
    'asset_id identifies a concrete asset.',
    'asset_family identifies the reusable family declaration.',
    'asset_role identifies the semantic role of the asset in the Challenge.',
    'provenance identifies where the evidence came from.',
    '',
    'These identities must not be collapsed into one field.',
    '',
    '## Rules',
    '',
    '1. Explicit family evidence is authoritative where present.',
    '2. UNKNOWN remains valid where evidence is insufficient.',
    '3. Cross-family reuse is allowed.',
    '4. Asset hash equality does not imply family identity.',
    '5. Historical evidence remains provenance until explicitly promoted.',
    '6. Runtime activation is outside D2.3.',
    '7. No renderer, simulation, mechanics or RNG changes are part of D2.3.',
    '',
    '## Inputs',
    '',
    'C11D_ASSET_FAMILY_REGISTRY_V1.json',
    'D2.2 asset role/evidence matrix',
    'D0 Challenge dossiers',
    'Current Challenge definitions',
    '',
    '## Output',
    '',
    'A stable canonical binding contract suitable for later integration with a declarative Production Request.',
    '',
    '## Next phase direction',
    '',
    'Connect this binding model to the normalized production-request pipeline without changing Challenge simulation truth.'
)

Write-Utf8NoBom $D23ContractPath ($D23ContractLines -join [Environment]::NewLine)

$D23Receipt = [ordered]@{
    checkpoint = 'C11-D D2.3'
    status = 'ACTIVE'
    handoff_from = 'D2.2'
    d2_2_receipt = 'artifacts\tests\c11d_d2\d2_2_validation_receipt.json'
    d2_1_registry = 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
    contract = 'docs\current\d\D2.3_ASSET_FAMILY_INTEGRATION_CONTRACT.md'
    scope = 'Canonical declarative binding layer; no runtime activation.'
    protected_runtime_changes = $false
    renderer_changes = $false
    simulation_changes = $false
    mechanics_changes = $false
    rng_changes = $false
    next_checkpoint = 'D2.3 implementation / validation'
}

Write-Utf8NoBom $D23ReceiptPath ($D23Receipt | ConvertTo-Json -Depth 10)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.2 -> D2.3 — CONSOLIDATED CLOSE + HANDOFF' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''

Write-Host '[OK] D2.2 core evidence accepted.' -ForegroundColor Green
Write-Host '[OK] CROSS_FAMILY_REUSE = 1.' -ForegroundColor Green
Write-Host '[OK] TRUE_FAMILY_CONFLICT = 0.' -ForegroundColor Green
Write-Host '[OK] D2.2 contract reconstructed with canonical sections.' -ForegroundColor Green
Write-Host '[OK] D2.2 receipt set to PASS / CLOSED.' -ForegroundColor Green
Write-Host '[OK] MASTER updated and snapshotted.' -ForegroundColor Green
Write-Host '[OK] START updated and snapshotted.' -ForegroundColor Green
Write-Host '[OK] D2.3 contract created.' -ForegroundColor Green
Write-Host '[OK] D2.3 handoff receipt created.' -ForegroundColor Green
Write-Host '[OK] No protected runtime work performed.' -ForegroundColor Green
Write-Host ''
Write-Host ('MASTER SNAPSHOT: ' + $MasterSnapshot)
Write-Host ('START SNAPSHOT:  ' + $StartSnapshot)
Write-Host ('D2.2 RECEIPT:    ' + $ReceiptPath)
Write-Host ('D2.3 CONTRACT:   ' + $D23ContractPath)
Write-Host ('D2.3 RECEIPT:    ' + $D23ReceiptPath)
Write-Host ''
Write-Host '==================================================' -ForegroundColor Green
Write-Host ' C11-D D2.2 — PASS / CLOSED' -ForegroundColor Green
Write-Host ' C11-D D2.3 — ACTIVE' -ForegroundColor Green
Write-Host '==================================================' -ForegroundColor Green
Write-Host ''
Write-Host 'D2.2 will not be re-audited unless contradictory evidence appears.'
Write-Host 'NEXT: D2.3 implementation / validation.'
