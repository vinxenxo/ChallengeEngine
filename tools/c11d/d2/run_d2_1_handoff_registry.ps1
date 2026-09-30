Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path

$CurrentD = Join-Path $Repo 'docs\current\d'
$HistoryD = Join-Path $Repo 'docs\history\master-prompts\c11d'
$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$DefinitionsRoot = Join-Path $Repo 'definitions\c11d\asset_families'

$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

$AuditPath = Join-Path $D2Root 'd2_0_asset_family_audit.json'
$D20ReceiptPath = Join-Path $D2Root 'd2_0_validation_receipt.json'

$RegistryPath = Join-Path $DefinitionsRoot 'C11D_ASSET_FAMILY_REGISTRY_V1.json'
$ContractPath = Join-Path $CurrentD 'D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md'
$ReceiptPath = Join-Path $D2Root 'd2_1_validation_receipt.json'

New-Item -ItemType Directory -Force -Path $CurrentD | Out-Null
New-Item -ItemType Directory -Force -Path $HistoryD | Out-Null
New-Item -ItemType Directory -Force -Path $D2Root | Out-Null
New-Item -ItemType Directory -Force -Path $DefinitionsRoot | Out-Null

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Content
    )

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Get-OptionalProperty {
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

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.0 -> D2.1 — HANDOFF + REGISTRY' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host ('[INFO] Repo: {0}' -f $Repo)
Write-Host ''

if (-not (Test-Path -LiteralPath $AuditPath)) {
    throw 'No existe el audit JSON de D2.0.'
}

if (-not (Test-Path -LiteralPath $D20ReceiptPath)) {
    throw 'No existe el receipt de D2.0.'
}

$D20Receipt = Get-Content -LiteralPath $D20ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json

if ([string]$D20Receipt.result -ne 'PASS') {
    throw 'El receipt de D2.0 no contiene PASS. D2.1 no se puede activar.'
}

$Audit = Get-Content -LiteralPath $AuditPath -Raw -Encoding UTF8 | ConvertFrom-Json

$FamilyGroups = @($Audit.asset_family_groups)
$UnknownFamilyChallenges = @($Audit.unknown_family_challenges)
$ChallengeRecords = @($Audit.current_challenges)
$D0Dossiers = @($Audit.d0_dossiers)
$AssetFiles = @($Audit.asset_files)
$AssetFamilyEvidence = @($Audit.asset_family_evidence)
$AssetRoleEvidence = @($Audit.asset_role_evidence)
$AssetReferenceResolution = @($Audit.asset_reference_resolution)
$UnresolvedReferences = @($Audit.unresolved_asset_references)
$ProtectedChanges = @($Audit.protected_source_new_changes)

if ($FamilyGroups.Count -ne 2) {
    throw ('D2.0 evidence mismatch: expected 2 explicit family groups, found {0}.' -f $FamilyGroups.Count)
}

if ($UnknownFamilyChallenges.Count -ne 5) {
    throw ('D2.0 evidence mismatch: expected 5 UNKNOWN family bindings, found {0}.' -f $UnknownFamilyChallenges.Count)
}

if ($ChallengeRecords.Count -ne 9) {
    throw ('D2.0 evidence mismatch: expected 9 Challenges, found {0}.' -f $ChallengeRecords.Count)
}

if ($D0Dossiers.Count -ne 9) {
    throw ('D2.0 evidence mismatch: expected 9 D0 dossiers, found {0}.' -f $D0Dossiers.Count)
}

if ($AssetFiles.Count -ne 15) {
    throw ('D2.0 evidence mismatch: expected 15 logical assets, found {0}.' -f $AssetFiles.Count)
}

if ($AssetReferenceResolution.Count -ne 27) {
    throw ('D2.0 evidence mismatch: expected 27 asset references, found {0}.' -f $AssetReferenceResolution.Count)
}

if ($UnresolvedReferences.Count -ne 0) {
    throw 'D2.0 contains unresolved asset references.'
}

if ($ProtectedChanges.Count -ne 0) {
    throw 'D2.0 recorded protected source changes.'
}

$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$MasterSnapshot = Join-Path $HistoryD ('MASTER_HANDOVER_C11D_PRE_D2_1_' + $Timestamp + '.md')
$StartSnapshot = Join-Path $HistoryD ('START_PROMPT_C11D_PRE_D2_1_' + $Timestamp + '.md')

$MasterSnapshotCreated = $false
$StartSnapshotCreated = $false

if (Test-Path -LiteralPath $MasterPath) {
    Copy-Item -LiteralPath $MasterPath -Destination $MasterSnapshot -Force
    $MasterSnapshotCreated = $true
}

if (Test-Path -LiteralPath $StartPath) {
    Copy-Item -LiteralPath $StartPath -Destination $StartSnapshot -Force
    $StartSnapshotCreated = $true
}

$FamilyLines = @()

foreach ($Family in $FamilyGroups) {
    $FamilyName = [string]$Family.asset_family
    $ChallengeIds = @($Family.challenge_ids) -join ', '
    $Versions = @($Family.versions) -join ', '

    if ([string]::IsNullOrWhiteSpace($Versions)) {
        $Versions = 'UNKNOWN'
    }

    $FamilyLines += ('- {0} — Challenges: {1} — Version(s): {2}' -f $FamilyName, $ChallengeIds, $Versions)
}

$UnknownLines = @()

foreach ($ChallengeId in $UnknownFamilyChallenges) {
    $UnknownLines += ('- {0} — family binding remains UNKNOWN.' -f $ChallengeId)
}

$MasterLines = @(
    '# C11-D MASTER HANDOVER',
    '',
    '## Current phase',
    '',
    'C11-D — Declarative Challenge recovery, visual/editorial parity, reusable asset families, production and provenance pipeline.',
    '',
    '## Current checkpoint',
    '',
    'D2.1 — Declarative Asset Family Registry / Evidence Binding',
    'STATUS: ACTIVE',
    '',
    '## Frozen reference baseline',
    '',
    'C11-C 2.19.12 is FROZEN and IMMUTABLE.',
    '',
    'Frozen ZIP:',
    'ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip',
    '',
    'Frozen ZIP SHA-256:',
    'D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32',
    '',
    'Frozen tree SHA-256:',
    '2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256',
    '',
    'build_factory.py SHA-256:',
    '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3',
    '',
    '## Closed checkpoints',
    '',
    'D0 — CLOSED / PASS',
    '9/9 Challenge dossiers recovered and evidenced.',
    '',
    'D1 — functional checkpoints complete.',
    'D1.0 source audit: PASS',
    'D1.1 visual/editorial mapping: PASS',
    'D1.5 canonical Instagram Reels layout profile established',
    'D1.6 contract regression: 5/5 PASS',
    'D1.7 declarative Challenge mapping: 9/9 PASS',
    '',
    'D2.0 — CLOSED / PASS',
    '15 logical C6 assets audited.',
    '9/9 Challenges audited.',
    '9/9 D0 dossiers discovered.',
    '2 explicit asset family groups.',
    '5 Challenges remain UNKNOWN for asset family.',
    '27 asset references.',
    '0 unresolved asset references.',
    '0 family promotions.',
    '0 family merges.',
    '0 protected C11-C source modifications.',
    '',
    '## D2.0 evidence',
    '',
    'Audit:',
    'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json',
    '',
    'Contract:',
    'docs\current\d\D2.0_ASSET_FAMILY_AUDIT_CONTRACT.md',
    '',
    'Receipt:',
    'artifacts\tests\c11d_d2\d2_0_validation_receipt.json',
    '',
    '## D2.1 active scope',
    '',
    'Build an additive declarative asset-family registry from the D2.0 audit evidence.',
    '',
    'The registry is an evidence-binding layer, not runtime activation authority.',
    '',
    'Rules:',
    '1. Preserve explicit asset_family and asset_family_version evidence.',
    '2. Preserve UNKNOWN where evidence is insufficient.',
    '3. Do not infer family membership from filenames alone.',
    '4. Do not collapse assets solely because SHA-256 values match.',
    '5. Preserve current Challenge references and D0 provenance separately.',
    '6. Historical evidence remains provenance/reference until explicitly promoted.',
    '7. Do not modify simulation, mechanics, RNG, SimulationResult, winning_frame, close_calls, WinningFrameDetector, RenderedFrameStream, C7, C9, frozen C11-C presentation, or frozen C11-C production.',
    '',
    '## Explicit D2.0 family groups',
    '',
    $FamilyLines,
    '',
    '## UNKNOWN bindings',
    '',
    $UnknownLines,
    '',
    '## D2.1 registry',
    '',
    'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json',
    '',
    '## D2.1 contract',
    '',
    'docs\current\d\D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md',
    '',
    '## D2.1 receipt',
    '',
    'artifacts\tests\c11d_d2\d2_1_validation_receipt.json',
    '',
    '## Next-context rule',
    '',
    'A new context must read MASTER_HANDOVER_C11D_CURRENT.md first, then START_PROMPT_C11D_CURRENT.md, then the D2.0 audit and D2.1 registry, contract and receipt.',
    'Do not reopen D2.0 unless new contradictory evidence appears.',
    '',
    '## Prompt maintenance rule',
    '',
    'Update MASTER HANDOVER and START PROMPT at every major milestone and checkpoint handoff.',
    'Snapshot the previous living prompts under docs\history\master-prompts\c11d before replacing them.'
)

$StartLines = @(
    '# C11-D START PROMPT',
    '',
    'Continue ChallengeEngineV01_STATELESS from the current C11-D checkpoint.',
    '',
    '## Read first',
    '',
    '1. docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md',
    '2. docs\current\d\START_PROMPT_C11D_CURRENT.md',
    '3. artifacts\tests\c11d_d2\d2_0_validation_receipt.json',
    '4. artifacts\tests\c11d_d2\d2_0_asset_family_audit.json',
    '5. definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json',
    '6. docs\current\d\D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md',
    '7. artifacts\tests\c11d_d2\d2_1_validation_receipt.json',
    '',
    '## State',
    '',
    'C11-D D0: CLOSED / PASS',
    'C11-D D1: functional checkpoints complete',
    'C11-D D2.0: CLOSED / PASS',
    'C11-D D2.1: ACTIVE',
    '',
    '## D2.0 confirmed evidence',
    '',
    '15 logical C6 assets',
    '9/9 Challenges',
    '9/9 D0 dossiers',
    '2 explicit asset families',
    '5 UNKNOWN family bindings',
    '27 asset references',
    '0 unresolved references',
    '',
    '## Current D2.1 task',
    '',
    'Maintain the declarative asset-family registry as evidence binding only.',
    'Keep explicit family metadata authoritative where present.',
    'Keep UNKNOWN explicit where absent.',
    'Keep historical provenance separate from current declarations.',
    'Do not alter frozen C11-C runtime/rendering/simulation/mechanics contracts.',
    '',
    '## Current registry',
    '',
    'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json',
    '',
    '## Required next action',
    '',
    'Validate the D2.1 registry against D2.0 evidence, verify deterministic Challenge bindings and role evidence, then produce the D2.1 PASS receipt before deciding the next D2 checkpoint.',
    '',
    '## Frozen baseline',
    '',
    'ZIP SHA-256: D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32',
    'TREE SHA-256: 2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256',
    'build_factory.py SHA-256: 3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3',
    '',
    'Never reopen the frozen C11-C baseline without explicit checkpoint, contract and regression evidence.'
)

Write-Utf8NoBom $MasterPath ($MasterLines -join [Environment]::NewLine)
Write-Utf8NoBom $StartPath ($StartLines -join [Environment]::NewLine)

$ChallengeBindings = @()

foreach ($Challenge in $ChallengeRecords) {
    $ChallengeId = [string]$Challenge.challenge_id
    $FamilyName = Get-OptionalProperty $Challenge 'asset_family'
    $FamilyVersion = Get-OptionalProperty $Challenge 'asset_family_version'
    $EvidenceStatus = [string]$Challenge.asset_family_evidence

    $ChallengeRefs = @(
        $AssetReferenceResolution |
        Where-Object { [string]$_.challenge_id -eq $ChallengeId } |
        ForEach-Object {
            [pscustomobject]@{
                reference = [string]$_.reference
                resolved_asset_path = Get-OptionalProperty $_ 'resolved_asset_path'
                resolution = [string]$_.resolution
                source_file = [string]$_.source_file
                json_path = [string]$_.json_path
            }
        }
    )

    $ChallengeRoles = @(
        $AssetRoleEvidence |
        Where-Object { [string]$_.challenge_id -eq $ChallengeId } |
        ForEach-Object {
            [pscustomobject]@{
                role = [string]$_.role
                reference = Get-OptionalProperty $_ 'reference'
                source_kind = [string]$_.source_kind
                source_file = [string]$_.source_file
                evidence_status = [string]$_.evidence_status
            }
        }
    )

    $D0Source = @(
        $D0Dossiers |
        Where-Object { [string]$_.challenge_id -eq $ChallengeId } |
        Select-Object -First 1
    )

    $D0Path = $null

    if ($D0Source.Count -gt 0) {
        $D0Path = [string]$D0Source[0].dossier_path
    }

    $BoundFamily = 'UNKNOWN'
    if (-not [string]::IsNullOrWhiteSpace([string]$FamilyName)) {
        $BoundFamily = [string]$FamilyName
    }

    $ChallengeBindings += [ordered]@{
        challenge_id = $ChallengeId
        mechanic = [string]$Challenge.mechanic
        mechanic_version = Get-OptionalProperty $Challenge 'mechanic_version'
        current_definition = [string]$Challenge.definition_path
        d0_dossier = $D0Path
        asset_family = $BoundFamily
        asset_family_version = $FamilyVersion
        family_binding_status = $EvidenceStatus
        asset_references = $ChallengeRefs
        role_evidence = $ChallengeRoles
    }
}

$RegistryFamilies = @()

foreach ($Family in $FamilyGroups) {
    $FamilyName = [string]$Family.asset_family

    $FamilyEvidenceRecords = @(
        $AssetFamilyEvidence |
        Where-Object { [string]$_.asset_family -eq $FamilyName } |
        ForEach-Object {
            [ordered]@{
                challenge_id = [string]$_.challenge_id
                source_kind = [string]$_.source_kind
                source_file = [string]$_.source_file
                asset_family = [string]$_.asset_family
                asset_family_version = Get-OptionalProperty $_ 'asset_family_version'
                evidence_status = [string]$_.evidence_status
            }
        }
    )

    $BoundChallenges = @(
        $ChallengeBindings |
        Where-Object { [string]$_['asset_family'] -eq $FamilyName } |
        ForEach-Object { [string]$_['challenge_id'] }
    )

    $FamilyChallengeIds = @($Family.challenge_ids)

    $ResolvedAssets = @(
        $AssetReferenceResolution |
        Where-Object { $FamilyChallengeIds -contains [string]$_['challenge_id'] } |
        Where-Object { [string]$_['resolution'] -ne 'NOT_FOUND' } |
        ForEach-Object { Get-OptionalProperty $_ 'resolved_asset_path' } |
        Where-Object { $null -ne $_ -and [string]$_.Length -gt 0 } |
        Select-Object -Unique
    )

    $RegistryFamilies += [ordered]@{
        asset_family = $FamilyName
        asset_family_versions = @($Family.versions)
        lifecycle = 'EVIDENCE_BACKED'
        runtime_activation = 'NOT_AUTHORIZED_BY_D2_1'
        challenge_bindings = @($BoundChallenges)
        resolved_asset_paths = @($ResolvedAssets)
        evidence_records = @($FamilyEvidenceRecords)
    }
}

$Registry = [ordered]@{
    registry_id = 'c11d_asset_family_registry_v1'
    schema_version = '1.0'
    phase = 'C11-D'
    checkpoint = 'D2.1'
    status = 'ACTIVE'
    registry_purpose = 'Declarative evidence binding for reusable C6 Challenge asset families.'
    runtime_authority = 'NONE'
    source_audit = 'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json'
    source_receipt = 'artifacts\tests\c11d_d2\d2_0_validation_receipt.json'
    frozen_c11c_baseline = [ordered]@{
        zip_sha256 = 'D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32'
        tree_sha256 = '2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256'
        build_factory_sha256 = '3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
    }
    rules = @(
        'Explicit asset_family and asset_family_version are preserved.',
        'UNKNOWN remains explicit where family evidence is absent.',
        'Filename semantics alone cannot create family membership.',
        'SHA-256 equality alone cannot collapse distinct assets.',
        'Historical evidence remains provenance/reference.',
        'D2.1 does not activate runtime asset routing.'
    )
    families = @($RegistryFamilies)
    challenge_bindings = @($ChallengeBindings)
    unknown_family_challenges = @($UnknownFamilyChallenges)
    logical_asset_count = $AssetFiles.Count
    asset_reference_count = $AssetReferenceResolution.Count
    unresolved_asset_reference_count = $UnresolvedReferences.Count
}

Write-Utf8NoBom $RegistryPath ($Registry | ConvertTo-Json -Depth 30)

$ContractLines = @(
    '# C11-D D2.1 — Declarative Asset Family Registry / Evidence Binding V1.0',
    '',
    '## Purpose',
    '',
    'Define the additive declarative registry that binds reusable C6 Challenge asset families to current Challenge evidence without changing runtime rendering or simulation behavior.',
    '',
    '## Registry authority',
    '',
    'This registry is an evidence-binding layer.',
    'It is not runtime activation authority.',
    'It does not alter renderer paths, simulation, mechanics, RNG, or frozen C11-C production.',
    '',
    '## Evidence rules',
    '',
    '1. Explicit asset_family and asset_family_version values are preserved.',
    '2. UNKNOWN remains explicit when family evidence is absent.',
    '3. Filename semantics alone cannot create family membership.',
    '4. SHA-256 equality alone cannot collapse distinct assets.',
    '5. Historical evidence remains provenance/reference until separately promoted.',
    '6. Existing assets are not renamed or merged by this checkpoint.',
    '7. Runtime activation requires a later explicit checkpoint and validation.',
    '',
    '## Source of truth',
    '',
    'D2.0 audit:',
    'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json',
    '',
    'D2.0 receipt:',
    'artifacts\tests\c11d_d2\d2_0_validation_receipt.json',
    '',
    '## Generated registry',
    '',
    'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json',
    '',
    '## Current evidence boundary',
    '',
    ('- Logical C6 assets: {0}' -f $AssetFiles.Count),
    ('- Challenges: {0}' -f $ChallengeRecords.Count),
    ('- Explicit asset families: {0}' -f $FamilyGroups.Count),
    ('- UNKNOWN family bindings: {0}' -f $UnknownFamilyChallenges.Count),
    ('- Asset references: {0}' -f $AssetReferenceResolution.Count),
    ('- Unresolved references: {0}' -f $UnresolvedReferences.Count),
    '',
    '## Explicit family groups',
    '',
    $FamilyLines,
    '',
    '## UNKNOWN Challenge bindings',
    '',
    $UnknownLines,
    '',
    '## D2.1 disposition',
    '',
    'The registry is additive, declarative and evidence-backed.',
    'No runtime promotion, asset merge, renderer change, simulation change or mechanics change is performed by D2.1.',
    '',
    '## Next step',
    '',
    'Validate this registry against D2.0 evidence and preserve the resulting D2.1 receipt before advancing to the next D2 checkpoint.'
)

Write-Utf8NoBom $ContractPath ($ContractLines -join [Environment]::NewLine)

$RegistryText = Get-Content -LiteralPath $RegistryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ContractText = Get-Content -LiteralPath $ContractPath -Raw -Encoding UTF8

$RegistryFamilyCountOk = @($RegistryText.families).Count -eq 2
$RegistryChallengeCountOk = @($RegistryText.challenge_bindings).Count -eq 9
$RegistryUnknownCountOk = @($RegistryText.unknown_family_challenges).Count -eq 5
$RegistryAssetCountOk = [int]$RegistryText.logical_asset_count -eq 15
$RegistryReferenceCountOk = [int]$RegistryText.asset_reference_count -eq 27
$RegistryUnresolvedCountOk = [int]$RegistryText.unresolved_asset_reference_count -eq 0
$RegistryPurposeOk = [string]$RegistryText.registry_purpose -eq 'Declarative evidence binding for reusable C6 Challenge asset families.'
$RegistryRuntimeAuthorityOk = [string]$RegistryText.runtime_authority -eq 'NONE'
$ContractPurposeOk = $ContractText.IndexOf('## Purpose', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractEvidenceOk = $ContractText.IndexOf('## Evidence rules', [System.StringComparison]::OrdinalIgnoreCase) -ge 0
$ContractNextOk = $ContractText.IndexOf('Validate this registry against D2.0 evidence', [System.StringComparison]::OrdinalIgnoreCase) -ge 0

$RegistryPass =
    $RegistryFamilyCountOk -and
    $RegistryChallengeCountOk -and
    $RegistryUnknownCountOk -and
    $RegistryAssetCountOk -and
    $RegistryReferenceCountOk -and
    $RegistryUnresolvedCountOk -and
    $RegistryPurposeOk -and
    $RegistryRuntimeAuthorityOk -and
    $ContractPurposeOk -and
    $ContractEvidenceOk -and
    $ContractNextOk

$ReceiptResult = 'FAIL'

if ($RegistryPass) {
    $ReceiptResult = 'PASS'
}

$MasterSnapshotRelative = $null
$StartSnapshotRelative = $null

if ($MasterSnapshotCreated) {
    $MasterSnapshotRelative = 'docs\history\master-prompts\c11d\' + (Split-Path $MasterSnapshot -Leaf)
}

if ($StartSnapshotCreated) {
    $StartSnapshotRelative = 'docs\history\master-prompts\c11d\' + (Split-Path $StartSnapshot -Leaf)
}

$Receipt = [ordered]@{
    checkpoint = 'C11-D D2.1'
    result = $ReceiptResult
    validation_type = 'DECLARATIVE_ASSET_FAMILY_REGISTRY_GENERATION_AND_VERIFICATION'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    source_audit = 'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json'
    source_d2_0_receipt = 'artifacts\tests\c11d_d2\d2_0_validation_receipt.json'
    registry = 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
    contract = 'docs\current\d\D2.1_ASSET_FAMILY_REGISTRY_CONTRACT.md'
    logical_asset_count = [int]$RegistryText.logical_asset_count
    challenge_binding_count = @($RegistryText.challenge_bindings).Count
    explicit_family_count = @($RegistryText.families).Count
    unknown_family_challenge_count = @($RegistryText.unknown_family_challenges).Count
    asset_reference_count = [int]$RegistryText.asset_reference_count
    unresolved_asset_reference_count = [int]$RegistryText.unresolved_asset_reference_count
    runtime_authority = [string]$RegistryText.runtime_authority
    registry_family_count_verified = $RegistryFamilyCountOk
    registry_challenge_count_verified = $RegistryChallengeCountOk
    registry_unknown_count_verified = $RegistryUnknownCountOk
    registry_asset_count_verified = $RegistryAssetCountOk
    registry_reference_count_verified = $RegistryReferenceCountOk
    registry_unresolved_count_verified = $RegistryUnresolvedCountOk
    contract_verified = ($ContractPurposeOk -and $ContractEvidenceOk -and $ContractNextOk)
    no_runtime_activation_performed = $true
    no_family_merge_performed = $true
    no_renderer_change_performed = $true
    no_simulation_change_performed = $true
    no_mechanics_change_performed = $true
    no_rng_change_performed = $true
    master_prompt_updated = $true
    start_prompt_updated = $true
    master_snapshot_created = $MasterSnapshotCreated
    start_snapshot_created = $StartSnapshotCreated
    master_snapshot = $MasterSnapshotRelative
    start_snapshot = $StartSnapshotRelative
    next_checkpoint = 'D2.1 validation / next D2 checkpoint'
}

Write-Utf8NoBom $ReceiptPath ($Receipt | ConvertTo-Json -Depth 15)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.0 -> D2.1 — RESULT' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''

Write-Host '[OK] D2.0 receipt PASS verified.' -ForegroundColor Green
Write-Host ('[OK] MASTER updated: {0}' -f $MasterPath) -ForegroundColor Green
Write-Host ('[OK] START updated:  {0}' -f $StartPath) -ForegroundColor Green

if ($MasterSnapshotCreated) {
    Write-Host ('[OK] MASTER snapshot: {0}' -f $MasterSnapshot) -ForegroundColor Green
}

if ($StartSnapshotCreated) {
    Write-Host ('[OK] START snapshot:  {0}' -f $StartSnapshot) -ForegroundColor Green
}

if ($RegistryFamilyCountOk) {
    Write-Host '[OK] Registry: 2 explicit families.' -ForegroundColor Green
}

if ($RegistryChallengeCountOk) {
    Write-Host '[OK] Registry: 9/9 Challenge bindings.' -ForegroundColor Green
}

if ($RegistryUnknownCountOk) {
    Write-Host '[OK] Registry: 5 UNKNOWN family bindings preserved.' -ForegroundColor Green
}

if ($RegistryAssetCountOk) {
    Write-Host '[OK] Registry: 15 logical assets.' -ForegroundColor Green
}

if ($RegistryReferenceCountOk) {
    Write-Host '[OK] Registry: 27 asset references.' -ForegroundColor Green
}

if ($RegistryUnresolvedCountOk) {
    Write-Host '[OK] Registry: 0 unresolved references.' -ForegroundColor Green
}

if ($RegistryRuntimeAuthorityOk) {
    Write-Host '[OK] Runtime authority = NONE.' -ForegroundColor Green
}

Write-Host ''
Write-Host ('REGISTRY: {0}' -f $RegistryPath)
Write-Host ('CONTRACT: {0}' -f $ContractPath)
Write-Host ('RECEIPT:  {0}' -f $ReceiptPath)
Write-Host ''

if ($RegistryPass) {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D2.1 — ACTIVE / REGISTRY GENERATED' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'D2.1 is active.'
    Write-Host 'Registry is evidence-backed and additive.'
    Write-Host 'No runtime activation performed.'
    Write-Host 'No family merge performed.'
    Write-Host 'No renderer/simulation/mechanics/RNG changes performed.'
    Write-Host ''
    Write-Host 'NEXT: D2.1 validation and next D2 checkpoint.'
}

if (-not $RegistryPass) {
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ' C11-D D2.1 — REGISTRY VERIFY FAIL' -ForegroundColor Red
    Write-Host '==================================================' -ForegroundColor Red
    exit 2
}
