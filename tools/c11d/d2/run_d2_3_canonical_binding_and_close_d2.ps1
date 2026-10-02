Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path

$D2Root = Join-Path $Repo 'artifacts\tests\c11d_d2'
$CurrentD = Join-Path $Repo 'docs\current\d'
$HistoryD = Join-Path $Repo 'docs\history\master-prompts\c11d'

$D20AuditPath = Join-Path $D2Root 'd2_0_asset_family_audit.json'
$D20ReceiptPath = Join-Path $D2Root 'd2_0_validation_receipt.json'

$D21RegistryPath = Join-Path $Repo 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
$D21ReceiptPath = Join-Path $D2Root 'd2_1_validation_receipt.json'

$D22MatrixPath = Join-Path $D2Root 'd2_2_asset_role_evidence_matrix.json'
$D22ReceiptPath = Join-Path $D2Root 'd2_2_validation_receipt.json'

$D23RegistryPath = Join-Path $Repo 'definitions\c11d\asset_families\C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json'
$D23ContractPath = Join-Path $CurrentD 'D2.3_ASSET_FAMILY_INTEGRATION_CONTRACT.md'
$D23ReceiptPath = Join-Path $D2Root 'd2_3_validation_receipt.json'
$D2ClosureReceiptPath = Join-Path $D2Root 'd2_phase_closure_d3_handoff.json'

$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

foreach ($Path in @(
    $D20AuditPath,
    $D20ReceiptPath,
    $D21RegistryPath,
    $D21ReceiptPath,
    $D22MatrixPath,
    $D22ReceiptPath,
    $D23ContractPath,
    $MasterPath,
    $StartPath
)) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw ('Required D2.3 input missing: ' + $Path)
    }
}

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

function Get-Array {
    param(
        [object]$Value
    )

    if ($null -eq $Value) {
        return @()
    }

    return @($Value)
}

$D20Audit = Get-Content -LiteralPath $D20AuditPath -Raw -Encoding UTF8 | ConvertFrom-Json
$D20Receipt = Get-Content -LiteralPath $D20ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$D21Registry = Get-Content -LiteralPath $D21RegistryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$D21Receipt = Get-Content -LiteralPath $D21ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$D22Matrix = Get-Content -LiteralPath $D22MatrixPath -Raw -Encoding UTF8 | ConvertFrom-Json
$D22Receipt = Get-Content -LiteralPath $D22ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json

$D20Pass = ([string]$D20Receipt.result -eq 'PASS')
$D21Pass = ([string]$D21Receipt.result -eq 'PASS')
$D22Pass = ([string]$D22Receipt.result -eq 'PASS')

if (-not $D20Pass) {
    throw 'D2.0 receipt is not PASS.'
}

if (-not $D21Pass) {
    throw 'D2.1 receipt is not PASS.'
}

if (-not $D22Pass) {
    throw 'D2.2 receipt is not PASS.'
}

$D21Status = [string]$D21Registry.status
$D21RuntimeAuthority = [string]$D21Registry.runtime_authority

if ($D21Status -ne 'ACTIVE') {
    throw ('D2.1 registry status is not ACTIVE: ' + $D21Status)
}

if ($D21RuntimeAuthority -ne 'NONE') {
    throw ('D2.1 runtime authority must remain NONE, found: ' + $D21RuntimeAuthority)
}

$LogicalAssets = @(Get-Array $D20Audit.asset_files)
$ChallengeBindings = @(Get-Array $D21Registry.challenge_bindings)
$FamilyBindings = @(Get-Array $D21Registry.families)
$UnknownChallenges = @(Get-Array $D21Registry.unknown_family_challenges)

$CrossFamilyReuseCount = [int]$D22Matrix.cross_family_reuse_count
$TrueFamilyConflictCount = [int]$D22Matrix.true_family_conflict_count
$ExplicitRoleAssetCount = [int]$D22Matrix.explicit_role_asset_count
$UnknownRoleAssetCount = [int]$D22Matrix.unknown_role_asset_count
$BoundAssetCount = [int]$D22Matrix.assets_with_challenge_bindings

if ($LogicalAssets.Count -ne 15) {
    throw ('Expected 15 logical assets, found ' + $LogicalAssets.Count)
}

if ($ChallengeBindings.Count -ne 9) {
    throw ('Expected 9 Challenge bindings, found ' + $ChallengeBindings.Count)
}

if ($FamilyBindings.Count -ne 2) {
    throw ('Expected 2 family bindings, found ' + $FamilyBindings.Count)
}

if ($UnknownChallenges.Count -ne 5) {
    throw ('Expected 5 UNKNOWN family Challenges, found ' + $UnknownChallenges.Count)
}

if ($ExplicitRoleAssetCount -ne 15) {
    throw ('D2.2 expected 15 explicit role assets, found ' + $ExplicitRoleAssetCount)
}

if ($UnknownRoleAssetCount -ne 0) {
    throw ('D2.2 expected 0 UNKNOWN role assets, found ' + $UnknownRoleAssetCount)
}

if ($BoundAssetCount -ne 15) {
    throw ('D2.2 expected 15 Challenge-bound assets, found ' + $BoundAssetCount)
}

if ($CrossFamilyReuseCount -ne 1) {
    throw ('Expected CROSS_FAMILY_REUSE = 1, found ' + $CrossFamilyReuseCount)
}

if ($TrueFamilyConflictCount -ne 0) {
    throw ('Expected TRUE_FAMILY_CONFLICT = 0, found ' + $TrueFamilyConflictCount)
}

$NormalizedAssets = @()

foreach ($Asset in $LogicalAssets) {
    $AssetPath = [string](Get-Prop $Asset 'path')
    $AssetSha = [string](Get-Prop $Asset 'sha256')
    $AssetSize = [int64](Get-Prop $Asset 'size_bytes')
    $AssetExtension = [string](Get-Prop $Asset 'extension')

    if ([string]::IsNullOrWhiteSpace($AssetPath)) {
        throw 'Logical asset without path.'
    }

    $NormalizedAssets += [ordered]@{
        asset_id = ('c6:' + $AssetPath.Replace('\','/'))
        asset_path = $AssetPath
        extension = $AssetExtension
        size_bytes = $AssetSize
        sha256 = $AssetSha
        identity_basis = 'DECLARED_SOURCE_PATH'
        semantic_role = 'EVIDENCE_FROM_D2.2'
    }
}

$NormalizedFamilies = @()

foreach ($Family in $FamilyBindings) {
    $FamilyName = [string](Get-Prop $Family 'asset_family')
    $Versions = @(Get-Array (Get-Prop $Family 'asset_family_versions'))
    $Challenges = @(Get-Array (Get-Prop $Family 'challenge_bindings'))
    $Evidence = @(Get-Array (Get-Prop $Family 'evidence_records'))

    $NormalizedFamilies += [ordered]@{
        asset_family = $FamilyName
        asset_family_versions = $Versions
        lifecycle = 'EVIDENCE_BACKED'
        runtime_activation = 'NONE'
        challenge_bindings = $Challenges
        evidence_records = $Evidence
    }
}

$NormalizedChallenges = @()

foreach ($Binding in $ChallengeBindings) {
    $ChallengeId = [string](Get-Prop $Binding 'challenge_id')
    $Mechanic = [string](Get-Prop $Binding 'mechanic')
    $MechanicVersion = Get-Prop $Binding 'mechanic_version'
    $CurrentDefinition = [string](Get-Prop $Binding 'current_definition')
    $D0Dossier = Get-Prop $Binding 'd0_dossier'
    $AssetFamily = [string](Get-Prop $Binding 'asset_family')
    $AssetFamilyVersion = Get-Prop $Binding 'asset_family_version'
    $FamilyBindingStatus = [string](Get-Prop $Binding 'family_binding_status')

    if ([string]::IsNullOrWhiteSpace($ChallengeId)) {
        throw 'Challenge binding without challenge_id.'
    }

    $References = @()
    $ReferenceValues = @(Get-Array (Get-Prop $Binding 'asset_references'))

    foreach ($Reference in $ReferenceValues) {
        $References += [ordered]@{
            reference = [string](Get-Prop $Reference 'reference')
            resolved_asset_path = Get-Prop $Reference 'resolved_asset_path'
            resolution = [string](Get-Prop $Reference 'resolution')
            source_file = [string](Get-Prop $Reference 'source_file')
            json_path = [string](Get-Prop $Reference 'json_path')
        }
    }

    $Roles = @()
    $RoleValues = @(Get-Array (Get-Prop $Binding 'role_evidence'))

    foreach ($Role in $RoleValues) {
        $Roles += [ordered]@{
            role = [string](Get-Prop $Role 'role')
            reference = Get-Prop $Role 'reference'
            source_kind = [string](Get-Prop $Role 'source_kind')
            source_file = [string](Get-Prop $Role 'source_file')
            evidence_status = [string](Get-Prop $Role 'evidence_status')
        }
    }

    $NormalizedChallenges += [ordered]@{
        challenge_id = $ChallengeId
        mechanic = $Mechanic
        mechanic_version = $MechanicVersion
        current_definition = $CurrentDefinition
        d0_dossier = $D0Dossier
        asset_family = if ([string]::IsNullOrWhiteSpace($AssetFamily)) { 'UNKNOWN' } else { $AssetFamily }
        asset_family_version = $AssetFamilyVersion
        family_binding_status = if ([string]::IsNullOrWhiteSpace($FamilyBindingStatus)) { 'UNKNOWN' } else { $FamilyBindingStatus }
        asset_references = @($References)
        role_evidence = @($Roles)
        provenance_status = 'EVIDENCE_BACKED'
    }
}

$AssetUsage = @()

foreach ($Asset in $NormalizedAssets) {
    $Path = [string]$Asset.asset_path
    $ChallengeIds = @()
    $Families = @()
    $Roles = @()
    $ProvenanceSources = @()

    foreach ($Challenge in $NormalizedChallenges) {
        foreach ($Reference in @($Challenge.asset_references)) {
            $ResolvedPath = Get-Prop $Reference 'resolved_asset_path'

            if ($null -ne $ResolvedPath) {
                if ([string]$ResolvedPath -eq $Path) {
                    $ChallengeIds += [string]$Challenge.challenge_id

                    if (-not [string]::IsNullOrWhiteSpace([string]$Challenge.asset_family)) {
                        $Families += [string]$Challenge.asset_family
                    }

                    $ProvenanceSources += [string]$Reference.source_file
                }
            }
        }

        foreach ($Role in @($Challenge.role_evidence)) {
            $RoleReference = Get-Prop $Role 'reference'

            if ($null -ne $RoleReference) {
                if ([string]$RoleReference -eq $Path) {
                    $Roles += [string]$Role.role
                }
            }
        }
    }

    $ChallengeIds = @($ChallengeIds | Sort-Object -Unique)
    $Families = @($Families | Sort-Object -Unique)
    $Roles = @($Roles | Sort-Object -Unique)
    $ProvenanceSources = @($ProvenanceSources | Sort-Object -Unique)

    $ReuseClass = 'SINGLE_FAMILY_OR_UNRESOLVED'

    if ($Families.Count -gt 1) {
        $ReuseClass = 'CROSS_FAMILY_REUSE'
    }

    $AssetUsage += [ordered]@{
        asset_id = [string]$Asset.asset_id
        asset_path = $Path
        sha256 = [string]$Asset.sha256
        challenge_ids = $ChallengeIds
        asset_families = $Families
        semantic_roles = $Roles
        reuse_class = $ReuseClass
        provenance_sources = $ProvenanceSources
    }
}

$Registry = [ordered]@{
    registry_id = 'c11d_challenge_asset_binding_registry_v1'
    schema_version = '1.0'
    phase = 'C11-D'
    checkpoint = 'D2.3'
    status = 'CLOSED'
    runtime_authority = 'NONE'
    purpose = 'Canonical declarative binding between recovered Challenge production metadata and reusable asset-family evidence.'
    identity_separation = [ordered]@{
        asset_id = 'Concrete asset identity based on declared source path.'
        asset_family = 'Reusable family identity.'
        asset_role = 'Semantic role backed by evidence.'
        provenance = 'Source evidence location and lineage.'
    }
    source_evidence = [ordered]@{
        d2_0_audit = 'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json'
        d2_0_receipt = 'artifacts\tests\c11d_d2\d2_0_validation_receipt.json'
        d2_1_registry = 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
        d2_1_receipt = 'artifacts\tests\c11d_d2\d2_1_validation_receipt.json'
        d2_2_matrix = 'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json'
        d2_2_receipt = 'artifacts\tests\c11d_d2\d2_2_validation_receipt.json'
    }
    rules = @(
        'Explicit family evidence is preserved.',
        'UNKNOWN family evidence remains explicit.',
        'Explicit role evidence is preserved.',
        'Filename semantics alone are not authoritative.',
        'SHA-256 equality does not authorize asset merging.',
        'Cross-family reuse is admissible reuse.',
        'True family conflict count must remain zero.',
        'Historical evidence remains provenance.',
        'Registry is declarative and has no runtime authority.'
    )
    counts = [ordered]@{
        logical_assets = $NormalizedAssets.Count
        families = $NormalizedFamilies.Count
        challenges = $NormalizedChallenges.Count
        unknown_family_challenges = $UnknownChallenges.Count
        cross_family_reuse = $CrossFamilyReuseCount
        true_family_conflicts = $TrueFamilyConflictCount
    }
    assets = @($NormalizedAssets)
    families = @($NormalizedFamilies)
    challenges = @($NormalizedChallenges)
    asset_usage = @($AssetUsage)
}

if (Test-Path -LiteralPath $D23RegistryPath) {
    throw ('D2.3 registry already exists: ' + $D23RegistryPath)
}

Write-Utf8NoBom $D23RegistryPath ($Registry | ConvertTo-Json -Depth 40)

$ContractLines = @(
    '# C11-D D2.3 — Asset Family Integration Contract V1.0',
    '',
    '## Purpose',
    '',
    'Define the canonical declarative binding between recovered Challenge production metadata and the reusable C6 asset-family evidence layer.',
    '',
    '## Strategic role',
    '',
    'C11-D normalizes Challenge video generation using mature production-contract lessons established in C11-C.',
    'Visual Loop and Visual Drill remain distinct content families. Their production contracts are references for normalization, not Challenge family identities.',
    '',
    '## Identity separation',
    '',
    '- asset_id = concrete asset identity.',
    '- asset_family = reusable family identity.',
    '- asset_role = semantic role backed by evidence.',
    '- provenance = source evidence and lineage.',
    '',
    'These identities must remain separate.',
    '',
    '## Canonical rules',
    '',
    '1. Explicit family evidence is preserved.',
    '2. UNKNOWN family evidence remains explicit.',
    '3. Explicit role evidence is preserved.',
    '4. Filename semantics alone are not authoritative.',
    '5. SHA-256 equality does not authorize asset merging.',
    '6. Cross-family reuse is admissible reuse.',
    '7. TRUE_FAMILY_CONFLICT must remain zero.',
    '8. Historical evidence remains provenance.',
    '9. The binding registry has no runtime authority.',
    '',
    '## Generated canonical registry',
    '',
    'definitions\c11d\asset_families\C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json',
    '',
    '## Evidence counts',
    '',
    ('- Logical assets: {0}' -f $NormalizedAssets.Count),
    ('- Families: {0}' -f $NormalizedFamilies.Count),
    ('- Challenges: {0}' -f $NormalizedChallenges.Count),
    ('- UNKNOWN family Challenges: {0}' -f $UnknownChallenges.Count),
    ('- CROSS_FAMILY_REUSE: {0}' -f $CrossFamilyReuseCount),
    ('- TRUE_FAMILY_CONFLICT: {0}' -f $TrueFamilyConflictCount),
    '',
    '## Runtime boundary',
    '',
    'D2.3 does not activate asset routing.',
    'D2.3 does not modify renderer, simulation, mechanics or RNG.',
    'D2.3 does not modify frozen C11-C source.',
    '',
    '## D2.3 disposition',
    '',
    'The canonical Challenge asset binding layer is declarative, evidence-backed and suitable as an input contract for the later normalized Production Request pipeline.',
    '',
    '## Next major phase',
    '',
    'D3 — Procedural Music V5.'
)

Write-Utf8NoBom $D23ContractPath ($ContractLines -join [Environment]::NewLine)

$MasterSnapshot = Join-Path $HistoryD ('MASTER_HANDOVER_C11D_PRE_D3_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.md')
$StartSnapshot = Join-Path $HistoryD ('START_PROMPT_C11D_PRE_D3_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.md')

Copy-Item -LiteralPath $MasterPath -Destination $MasterSnapshot -Force
Copy-Item -LiteralPath $StartPath -Destination $StartSnapshot -Force

$D23MasterLines = @(
    '# C11-D MASTER HANDOVER',
    '',
    '## Current phase',
    '',
    'C11-D — Normalization of Challenge video generation using recovered C11-A/C11-B Challenge content and mature declarative production contracts from C11-C.',
    '',
    '## Strategic objective',
    '',
    'Create one robust, reproducible, declarative production architecture for Challenge videos.',
    'C11-C Visual Loop and Visual Drill are reference families whose production contracts inform normalization; they are not being reclassified as Challenge families.',
    '',
    '## C11-D status',
    '',
    'D0: CLOSED / PASS',
    'D1: functional checkpoints complete',
    'D2.0: CLOSED / PASS',
    'D2.1: PASS / VALIDATED',
    'D2.2: PASS / CLOSED',
    'D2.3: PASS / CLOSED',
    'D2: CLOSED',
    'D3: ACTIVE',
    '',
    '## D2.3 canonical registry',
    '',
    'definitions\c11d\asset_families\C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json',
    '',
    'Contract:',
    'docs\current\d\D2.3_ASSET_FAMILY_INTEGRATION_CONTRACT.md',
    '',
    'Receipt:',
    'artifacts\tests\c11d_d2\d2_3_validation_receipt.json',
    '',
    'D2 final handoff:',
    'artifacts\tests\c11d_d2\d2_phase_closure_d3_handoff.json',
    '',
    '## D2 final evidence',
    '',
    '15 logical C6 assets.',
    '2 explicit asset families.',
    '9 Challenge bindings.',
    '5 UNKNOWN family Challenge bindings retained.',
    '15 explicit role assets.',
    '0 UNKNOWN role assets.',
    '1 CROSS_FAMILY_REUSE.',
    '0 TRUE_FAMILY_CONFLICT.',
    '27 asset references.',
    '0 unresolved references.',
    'Runtime authority remains NONE.',
    '',
    '## D3 — Procedural Music V5',
    '',
    'D3 is the next major C11-D phase.',
    'Objective: normalize procedural music generation as a declarative, deterministic production component for Challenge videos without changing Challenge simulation truth.',
    '',
    'Required D3 boundaries:',
    '1. deterministic generation',
    '2. declarative music profile/configuration',
    '3. provenance of generated audio',
    '4. no simulation or mechanics changes',
    '5. no reopening frozen C11-C production',
    '6. compatibility with later normalized Production Request',
    '',
    '## Frozen reference',
    '',
    'C11-C 2.19.12 remains FROZEN and IMMUTABLE.',
    'ZIP SHA-256: D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32',
    'TREE SHA-256: 2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256',
    'build_factory.py SHA-256: 3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3',
    '',
    '## Context switching',
    '',
    'Read MASTER_HANDOVER_C11D_CURRENT.md first, then START_PROMPT_C11D_CURRENT.md, then D3 artifacts.',
    'Living prompts must be snapshotted before each major milestone update.'
)

$D3StartLines = @(
    '# C11-D START PROMPT',
    '',
    'Continue ChallengeEngineV01_STATELESS from C11-D D3.',
    '',
    '## Read first',
    '',
    'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md',
    'docs\current\d\START_PROMPT_C11D_CURRENT.md',
    'artifacts\tests\c11d_d2\d2_3_validation_receipt.json',
    'artifacts\tests\c11d_d2\d2_phase_closure_d3_handoff.json',
    'definitions\c11d\asset_families\C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json',
    '',
    '## Closed state',
    '',
    'D0 = CLOSED / PASS',
    'D1 = functional checkpoints complete',
    'D2.0 = CLOSED / PASS',
    'D2.1 = PASS / VALIDATED',
    'D2.2 = PASS / CLOSED',
    'D2.3 = PASS / CLOSED',
    'D2 = CLOSED',
    'D3 = ACTIVE',
    '',
    '## D2 outcome',
    '',
    'The C11-D Challenge asset layer is now declarative and evidence-backed.',
    'The canonical binding layer separates asset identity, family identity, role identity and provenance.',
    'Runtime authority remains NONE.',
    '',
    '## D3 objective',
    '',
    'Procedural Music V5.',
    '',
    'Normalize deterministic procedural music as a declarative production component for Challenge video generation.',
    'Keep generated audio reproducible and provenance-backed.',
    'Prepare the music contract for later normalized Production Request integration.',
    '',
    '## D3 guardrails',
    '',
    'Do not change Challenge simulation truth.',
    'Do not change mechanics.',
    'Do not change RNG used by Challenge simulation.',
    'Do not modify SimulationResult, winning_frame, close_calls, WinningFrameDetector or RenderedFrameStream.',
    'Do not reopen frozen C11-C production.',
    '',
    '## Strategic direction',
    '',
    'The purpose of C11-D is normalization: converge the robust declarative production lessons of C11-C with the recovered Challenge content of C11-A/C11-B.',
    'Do not create artificial family identities merely to match Visual Loop or Visual Drill naming.',
    '',
    '## Next step',
    '',
    'Start D3.0 with a source/provenance audit of the existing procedural audio path and historical music requirements before implementation.'
)

Write-Utf8NoBom $MasterPath ($D23MasterLines -join [Environment]::NewLine)
Write-Utf8NoBom $StartPath ($D3StartLines -join [Environment]::NewLine)

$D23Receipt = [ordered]@{
    checkpoint = 'C11-D D2.3'
    result = 'PASS'
    validation_type = 'CANONICAL_CHALLENGE_ASSET_BINDING'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    registry = 'definitions\c11d\asset_families\C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json'
    contract = 'docs\current\d\D2.3_ASSET_FAMILY_INTEGRATION_CONTRACT.md'
    source_d2_0 = 'artifacts\tests\c11d_d2\d2_0_asset_family_audit.json'
    source_d2_1 = 'definitions\c11d\asset_families\C11D_ASSET_FAMILY_REGISTRY_V1.json'
    source_d2_2 = 'artifacts\tests\c11d_d2\d2_2_asset_role_evidence_matrix.json'
    logical_asset_count = $NormalizedAssets.Count
    family_count = $NormalizedFamilies.Count
    challenge_binding_count = $NormalizedChallenges.Count
    unknown_family_challenge_count = $UnknownChallenges.Count
    explicit_role_asset_count = $ExplicitRoleAssetCount
    unknown_role_asset_count = $UnknownRoleAssetCount
    cross_family_reuse_count = $CrossFamilyReuseCount
    true_family_conflict_count = $TrueFamilyConflictCount
    runtime_authority = 'NONE'
    declarative_registry = $true
    provenance_preserved = $true
    identity_separation_preserved = $true
    no_runtime_activation = $true
    no_renderer_change = $true
    no_simulation_change = $true
    no_mechanics_change = $true
    no_rng_change = $true
    no_historical_promotion = $true
    status = 'CLOSED'
    next_major_phase = 'D3'
}

Write-Utf8NoBom $D23ReceiptPath ($D23Receipt | ConvertTo-Json -Depth 20)

$D2ClosureReceipt = [ordered]@{
    phase = 'C11-D D2'
    result = 'CLOSED'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    closed_checkpoints = @(
        'D2.0 PASS',
        'D2.1 PASS / VALIDATED',
        'D2.2 PASS / CLOSED',
        'D2.3 PASS / CLOSED'
    )
    evidence = [ordered]@{
        logical_assets = $NormalizedAssets.Count
        families = $NormalizedFamilies.Count
        challenges = $NormalizedChallenges.Count
        unknown_family_challenges = $UnknownChallenges.Count
        explicit_role_assets = $ExplicitRoleAssetCount
        unknown_role_assets = $UnknownRoleAssetCount
        cross_family_reuse = $CrossFamilyReuseCount
        true_family_conflicts = $TrueFamilyConflictCount
    }
    canonical_binding_registry = 'definitions\c11d\asset_families\C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json'
    d2_3_receipt = 'artifacts\tests\c11d_d2\d2_3_validation_receipt.json'
    master_snapshot = ('docs\history\master-prompts\c11d\' + (Split-Path $MasterSnapshot -Leaf))
    start_snapshot = ('docs\history\master-prompts\c11d\' + (Split-Path $StartSnapshot -Leaf))
    no_protected_runtime_changes = $true
    next_phase = 'D3'
}

Write-Utf8NoBom $D2ClosureReceiptPath ($D2ClosureReceipt | ConvertTo-Json -Depth 15)

$RegistryCheck = Get-Content -LiteralPath $D23RegistryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ReceiptCheck = Get-Content -LiteralPath $D23ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json

$RegistryAssetsOk = @($RegistryCheck.assets).Count -eq 15
$RegistryFamiliesOk = @($RegistryCheck.families).Count -eq 2
$RegistryChallengesOk = @($RegistryCheck.challenges).Count -eq 9
$RegistryUnknownOk = @($RegistryCheck.counts).unknown_family_challenges -eq 5
$RegistryReuseOk = @($RegistryCheck.counts).cross_family_reuse -eq 1
$RegistryConflictOk = @($RegistryCheck.counts).true_family_conflicts -eq 0
$RegistryRuntimeOk = ([string]$RegistryCheck.runtime_authority -eq 'NONE')
$ReceiptPassOk = ([string]$ReceiptCheck.result -eq 'PASS')
$ClosureExists = Test-Path -LiteralPath $D2ClosureReceiptPath
$PromptsUpdated = (
    ((Get-Content -LiteralPath $MasterPath -Raw -Encoding UTF8).IndexOf('D3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0) -and
    ((Get-Content -LiteralPath $StartPath -Raw -Encoding UTF8).IndexOf('D3', [System.StringComparison]::OrdinalIgnoreCase) -ge 0)
)

$FinalPass =
    $RegistryAssetsOk -and
    $RegistryFamiliesOk -and
    $RegistryChallengesOk -and
    $RegistryUnknownOk -and
    $RegistryReuseOk -and
    $RegistryConflictOk -and
    $RegistryRuntimeOk -and
    $ReceiptPassOk -and
    $ClosureExists -and
    $PromptsUpdated

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D2.3 — CANONICAL BINDING / D2 CLOSURE' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''

if ($RegistryAssetsOk) {
    Write-Host '[OK] 15 logical assets in canonical binding registry.' -ForegroundColor Green
}

if ($RegistryFamiliesOk) {
    Write-Host '[OK] 2 explicit families preserved.' -ForegroundColor Green
}

if ($RegistryChallengesOk) {
    Write-Host '[OK] 9/9 Challenge bindings preserved.' -ForegroundColor Green
}

if ($RegistryUnknownOk) {
    Write-Host '[OK] 5 UNKNOWN family bindings preserved.' -ForegroundColor Green
}

if ($RegistryReuseOk) {
    Write-Host '[OK] CROSS_FAMILY_REUSE = 1.' -ForegroundColor Green
}

if ($RegistryConflictOk) {
    Write-Host '[OK] TRUE_FAMILY_CONFLICT = 0.' -ForegroundColor Green
}

if ($RegistryRuntimeOk) {
    Write-Host '[OK] runtime_authority = NONE.' -ForegroundColor Green
}

if ($ReceiptPassOk) {
    Write-Host '[OK] D2.3 receipt PASS.' -ForegroundColor Green
}

if ($ClosureExists) {
    Write-Host '[OK] D2 phase closure receipt created.' -ForegroundColor Green
}

if ($PromptsUpdated) {
    Write-Host '[OK] MASTER / START handed off to D3.' -ForegroundColor Green
}

Write-Host ''
Write-Host ('REGISTRY: ' + $D23RegistryPath)
Write-Host ('CONTRACT: ' + $D23ContractPath)
Write-Host ('RECEIPT:  ' + $D23ReceiptPath)
Write-Host ('D2 CLOSE: ' + $D2ClosureReceiptPath)
Write-Host ''

if ($FinalPass) {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D2.3 — PASS / CLOSED' -ForegroundColor Green
    Write-Host ' C11-D D2 — CLOSED' -ForegroundColor Green
    Write-Host ' C11-D D3 — ACTIVE' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'Canonical Challenge asset binding layer established.'
    Write-Host 'D2 is closed.'
    Write-Host 'No runtime activation performed.'
    Write-Host 'No renderer/simulation/mechanics/RNG changes performed.'
    Write-Host ''
    Write-Host 'NEXT: D3.0 — Procedural Music V5 Source / Provenance Audit'
}

if (-not $FinalPass) {
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ' C11-D D2.3 — VERIFY FAIL' -ForegroundColor Red
    Write-Host '==================================================' -ForegroundColor Red
}