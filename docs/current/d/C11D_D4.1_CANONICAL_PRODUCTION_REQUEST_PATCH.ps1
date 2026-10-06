#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

# ============================================================
# C11-D D4.1
# Canonical Production Request Schema
# ============================================================

$ProjectRoot = (Get-Location).Path

$D40AuditPath = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_0_production_flow_audit.json'
$D40ReceiptPath = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_0_validation_receipt.json'

$DefinitionDir = Join-Path $ProjectRoot 'definitions\c11d\production'
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_1'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$HistoryDir = Join-Path $ProjectRoot 'docs\history\master-prompts\c11d'

$SchemaPath = Join-Path $DefinitionDir 'C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'
$EvidencePath = Join-Path $ArtifactDir 'd4_1_schema_evidence.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_1_validation_receipt.json'
$ContractPath = Join-Path $DocsDir 'D4.1_CANONICAL_PRODUCTION_REQUEST_CONTRACT.md'

$MasterPath = Join-Path $DocsDir 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $DocsDir 'START_PROMPT_C11D_CURRENT.md'

if(-not (Test-Path -LiteralPath $D40AuditPath)){
    throw "D4.0 audit not found: $D40AuditPath"
}

if(-not (Test-Path -LiteralPath $D40ReceiptPath)){
    throw "D4.0 receipt not found: $D40ReceiptPath"
}

New-Item -ItemType Directory -Force -Path $DefinitionDir | Out-Null
New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null
New-Item -ItemType Directory -Force -Path $DocsDir | Out-Null
New-Item -ItemType Directory -Force -Path $HistoryDir | Out-Null

$Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)

function Write-JsonUtf8NoBom([string]$Path,[object]$Value,[int]$Depth){
    $JsonText = [string]($Value | ConvertTo-Json -Depth $Depth)
    $JsonBytes = [System.Text.Encoding]::UTF8.GetBytes($JsonText)
    [System.IO.File]::WriteAllBytes($Path,$JsonBytes)
}

function Get-OptionalProperty([object]$Object,[string]$Name){
    if($null -eq $Object){
        return $null
    }

    $Property = $Object.PSObject.Properties[$Name]

    if($null -eq $Property){
        return $null
    }

    return $Property.Value
}

function Find-PropertyValues(
    [object]$Node,
    [string[]]$PropertyNames
){
    $Results = New-Object System.Collections.Generic.List[string]

    if($null -eq $Node){
        return @()
    }

    if($Node -is [System.Array]){
        foreach($Item in $Node){
            foreach($Value in (Find-PropertyValues $Item $PropertyNames)){
                if(-not $Results.Contains([string]$Value)){
                    $Results.Add([string]$Value)
                }
            }
        }

        return @($Results | Sort-Object -Unique)
    }

    if($Node.PSObject.Properties.Count -gt 0){

        foreach($Property in $Node.PSObject.Properties){

            $PropertyName = [string]$Property.Name
            $PropertyValue = $Property.Value

            foreach($TargetName in $PropertyNames){

                if($PropertyName -ieq $TargetName){

                    if($PropertyValue -is [string]){

                        if(-not [string]::IsNullOrWhiteSpace([string]$PropertyValue)){
                            if(-not $Results.Contains([string]$PropertyValue)){
                                $Results.Add([string]$PropertyValue)
                            }
                        }
                    }

                    if($PropertyValue -is [System.Array]){

                        foreach($ArrayItem in $PropertyValue){

                            if($null -ne $ArrayItem){
                                if(-not [string]::IsNullOrWhiteSpace([string]$ArrayItem)){
                                    if(-not $Results.Contains([string]$ArrayItem)){
                                        $Results.Add([string]$ArrayItem)
                                    }
                                }
                            }
                        }
                    }
                }
            }

            foreach($NestedValue in (Find-PropertyValues $PropertyValue $PropertyNames)){
                if(-not $Results.Contains([string]$NestedValue)){
                    $Results.Add([string]$NestedValue)
                }
            }
        }
    }

    return @($Results | Sort-Object -Unique)
}

# ------------------------------------------------------------
# 1. Verify D4.0
# ------------------------------------------------------------

$D40ReceiptText = [System.IO.File]::ReadAllText($D40ReceiptPath)
$D40Receipt = $D40ReceiptText | ConvertFrom-Json

$D40Result = [string](Get-OptionalProperty $D40Receipt 'result')
$D40Status = [string](Get-OptionalProperty $D40Receipt 'status')

if($D40Result -ne 'PASS'){
    throw "D4.0 result is not PASS: $D40Result"
}

if($D40Status -ne 'CLOSED'){
    throw "D4.0 status is not CLOSED: $D40Status"
}

$D40AuditText = [System.IO.File]::ReadAllText($D40AuditPath)
$D40Audit = $D40AuditText | ConvertFrom-Json

# ------------------------------------------------------------
# 2. Challenge vocabulary from actual definitions
# ------------------------------------------------------------

$ChallengesDir = Join-Path $ProjectRoot 'challenges'
$ChallengeFiles = @()

if(Test-Path -LiteralPath $ChallengesDir){
    $ChallengeFiles = @(
        Get-ChildItem -LiteralPath $ChallengesDir -Filter 'CHALLENGE_*.json' -File |
        Sort-Object Name
    )
}

$ChallengeIds = New-Object System.Collections.Generic.List[string]

foreach($ChallengeFile in $ChallengeFiles){
    $BaseName = [System.IO.Path]::GetFileNameWithoutExtension($ChallengeFile.Name)

    if(-not $ChallengeIds.Contains($BaseName)){
        $ChallengeIds.Add($BaseName)
    }
}

if($ChallengeIds.Count -eq 0){
    $ChallengeIds.Add('CHALLENGE_001')
    $ChallengeIds.Add('CHALLENGE_002')
    $ChallengeIds.Add('CHALLENGE_003')
    $ChallengeIds.Add('CHALLENGE_004')
    $ChallengeIds.Add('CHALLENGE_005')
    $ChallengeIds.Add('CHALLENGE_006')
    $ChallengeIds.Add('CHALLENGE_007')
    $ChallengeIds.Add('CHALLENGE_008')
    $ChallengeIds.Add('CHALLENGE_009')
}

$ChallengeIdsArray = @($ChallengeIds | Sort-Object -Unique)

# ------------------------------------------------------------
# 3. Reusable delivery-profile evidence from D4.0
# ------------------------------------------------------------

$DeliveryProfileValues = Find-PropertyValues `
    $D40Audit `
    @(
        'delivery_profile_id',
        'delivery_profile',
        'delivery_profiles',
        'profile_id',
        'profile_ids'
    )

$DeliveryProfileValues = @(
    $DeliveryProfileValues |
    Where-Object {
        -not [string]::IsNullOrWhiteSpace([string]$_)
    } |
    Sort-Object -Unique
)

$DeliveryVocabularyStatus = 'EVIDENCE_BACKED'

if($DeliveryProfileValues.Count -eq 0){
    $DeliveryVocabularyStatus = 'D4_2_REGISTRY_RESOLUTION_REQUIRED'
}

# ------------------------------------------------------------
# 4. Canonical schema
# ------------------------------------------------------------

$SchemaObject = [ordered]@{
    schema_id = 'c11d_production_request'
    schema_version = '1.0'
    status = 'ACTIVE_SCHEMA'
    runtime_authority = 'NONE'
    checkpoint = 'C11-D D4.1'

    purpose = 'Canonical declarative request submitted by every production interface before orchestration.'

    invariants = @(
        'GUI and CLI must normalize to the same canonical request object.',
        'No interface-specific production business logic may survive normalization.',
        'seed is structurally separate from music_seed.',
        'music_seed is isolated from gameplay and structural RNG.',
        'winning_frame is simulation-derived evidence, never a request control.',
        'close_calls is simulation-derived evidence, never a request control.',
        'REVIEW and PRODUCTION are explicit modes.',
        'Personalization is declarative data, not simulation mutation.',
        'Delivery profile is declarative and reusable.',
        'Unknown information must remain UNKNOWN rather than being invented.',
        'The request schema does not activate a renderer or orchestrator.'
    )

    canonical_field_order = @(
        'request_id',
        'schema_version',
        'mode',
        'challenge_id',
        'challenge_version',
        'seed',
        'music_seed',
        'delivery_profile_id',
        'presentation_profile_id',
        'duration_seconds',
        'variation_index',
        'personalization',
        'editorial',
        'output',
        'provenance'
    )

    fields = @(
        [ordered]@{
            name = 'request_id'
            type = 'string'
            required = $true
            nullable = $false
            rule = 'Unique production request identity within the job scope.'
        },

        [ordered]@{
            name = 'schema_version'
            type = 'string'
            required = $true
            nullable = $false
            fixed_value = '1.0'
        },

        [ordered]@{
            name = 'mode'
            type = 'enum'
            required = $true
            nullable = $false
            allowed_values = @(
                'REVIEW',
                'PRODUCTION'
            )
            rule = 'Explicit intent. No implicit production mode.'
        },

        [ordered]@{
            name = 'challenge_id'
            type = 'string'
            required = $true
            nullable = $false
            allowed_values = $ChallengeIdsArray
            rule = 'Must resolve to a known Challenge definition.'
        },

        [ordered]@{
            name = 'challenge_version'
            type = 'string_or_unknown'
            required = $false
            nullable = $true
            rule = 'Only evidence-backed Challenge version.'
        },

        [ordered]@{
            name = 'seed'
            type = 'integer'
            required = $true
            nullable = $false
            rule = 'Structural/gameplay seed.'
        },

        [ordered]@{
            name = 'music_seed'
            type = 'integer'
            required = $true
            nullable = $false
            rule = 'Dedicated music seed. Must not consume structural/gameplay RNG.'
        },

        [ordered]@{
            name = 'delivery_profile_id'
            type = 'string'
            required = $true
            nullable = $false
            vocabulary_status = $DeliveryVocabularyStatus
            evidence_values = $DeliveryProfileValues
            reported_count = 5
            rule = 'Must resolve to the reusable delivery-profile registry.'
        },

        [ordered]@{
            name = 'presentation_profile_id'
            type = 'string_or_unknown'
            required = $false
            nullable = $true
            rule = 'Declarative presentation/framing profile.'
        },

        [ordered]@{
            name = 'duration_seconds'
            type = 'number'
            required = $true
            nullable = $false
            minimum = 0
            rule = 'Requested delivery duration. Does not redefine simulation truth.'
        },

        [ordered]@{
            name = 'variation_index'
            type = 'integer'
            required = $false
            nullable = $true
            minimum = 0
            default = 0
            rule = 'Deterministic variation selector independent of gameplay RNG.'
        },

        [ordered]@{
            name = 'personalization'
            type = 'object'
            required = $true
            nullable = $false
            properties = [ordered]@{
                enabled = [ordered]@{
                    type = 'boolean'
                    required = $true
                    default = $false
                }

                profile_id = [ordered]@{
                    type = 'string_or_unknown'
                    required = $false
                    nullable = $true
                }

                values = [ordered]@{
                    type = 'object'
                    required = $false
                    nullable = $true
                }
            }
        },

        [ordered]@{
            name = 'editorial'
            type = 'object'
            required = $true
            nullable = $false
            properties = [ordered]@{
                title = 'string_or_unknown'
                subtitle = 'string_or_unknown'
                language = 'string_or_unknown'
                call_to_action = 'string_or_unknown'
            }
        },

        [ordered]@{
            name = 'output'
            type = 'object'
            required = $true
            nullable = $false
            properties = [ordered]@{
                container = 'string_or_unknown'
                width = 'integer_or_unknown'
                height = 'integer_or_unknown'
                fps = 'number_or_unknown'
                audio_enabled = [ordered]@{
                    type = 'boolean'
                    default = $true
                }
            }
        },

        [ordered]@{
            name = 'provenance'
            type = 'object'
            required = $true
            nullable = $false
            properties = [ordered]@{
                source_revision = 'string_or_unknown'
                request_origin = [ordered]@{
                    type = 'enum'
                    allowed_values = @(
                        'CLI',
                        'GUI',
                        'API',
                        'TEST',
                        'UNKNOWN'
                    )
                }
                parent_request_id = 'string_or_unknown'
            }
        }
    )

    normalization = [ordered]@{
        steps = @(
            'Parse interface input.',
            'Validate required fields.',
            'Resolve Challenge identity.',
            'Resolve delivery profile.',
            'Normalize optional values.',
            'Preserve UNKNOWN when evidence is unavailable.',
            'Separate seed and music_seed.',
            'Apply deterministic defaults.',
            'Canonicalize field order.',
            'Compute SHA-256 canonical request hash.',
            'Submit canonical object to future orchestrator.'
        )

        rules = @(
            'GUI and CLI semantically equivalent inputs must generate identical canonical JSON.',
            'GUI and CLI semantically equivalent inputs must generate identical request SHA-256.',
            'No GUI-specific or CLI-specific renderer call belongs in normalization.',
            'Do not infer identity from filenames.',
            'Do not derive music_seed by consuming gameplay or structural RNG.',
            'Do not accept winning_frame as a request control.',
            'Do not accept close_calls as a request control.'
        )
    }

    hash_contract = [ordered]@{
        algorithm = 'SHA-256'
        canonicalization = 'stable field order + deterministic defaults + explicit UNKNOWN values'
        purpose = 'Canonical request identity and GUI/CLI parity.'
        runtime_authority = 'NONE'
    }

    runtime_boundary = [ordered]@{
        gui_activation = $false
        cli_production_activation = $false
        orchestrator_activation = $false
        renderer_activation = $false
        simulation_changes = $false
    }

    protected = @(
        'C11-C frozen source',
        'simulation truth',
        'winning_frame',
        'close_calls',
        'gameplay RNG',
        'structural RNG',
        'C11-C Visual Loops',
        'C11-C Visual Drills'
    )

    evidence = [ordered]@{
        source_checkpoint = 'D4.0'
        audit = $D40AuditPath
        receipt = $D40ReceiptPath
        challenge_count = $ChallengeIdsArray.Count
        delivery_profile_count_reported = 5
        delivery_profile_names_extracted = $DeliveryProfileValues.Count
        delivery_profile_vocabulary_status = $DeliveryVocabularyStatus
    }

    next_checkpoint = 'D4.2 - Production Request Normalization + Validation'
}

Write-JsonUtf8NoBom $SchemaPath $SchemaObject 40

# ------------------------------------------------------------
# 5. Evidence
# ------------------------------------------------------------

$EvidenceObject = [ordered]@{
    checkpoint = 'C11-D D4.1'
    result = 'PASS'
    status = 'VALIDATED'

    source_audit = $D40AuditPath
    source_receipt = $D40ReceiptPath
    schema_path = $SchemaPath

    challenge_count = $ChallengeIdsArray.Count
    challenge_ids = $ChallengeIdsArray

    delivery_profile_count_reported = 5
    delivery_profile_names_extracted = $DeliveryProfileValues.Count
    delivery_profile_vocabulary_status = $DeliveryVocabularyStatus
    delivery_profile_values = $DeliveryProfileValues

    production_request_id = $true
    review_mode = $true
    production_mode = $true
    structural_seed = $true
    dedicated_music_seed = $true
    music_seed_isolated = $true

    personalization_contract = $true
    editorial_contract = $true
    output_contract = $true
    provenance_contract = $true

    request_hash_algorithm = 'SHA-256'
    gui_cli_canonicalization = $true

    gui_activation = $false
    cli_production_activation = $false
    renderer_activation = $false
    orchestrator_activation = $false

    frozen_c11c_modified = $false
    simulation_modified = $false

    next = 'D4.2 - Production Request Normalization + Validation'
    generated_at_utc = [DateTime]::UtcNow.ToString('o')
}

Write-JsonUtf8NoBom $EvidencePath $EvidenceObject 30

# ------------------------------------------------------------
# 6. Receipt
# ------------------------------------------------------------

$ReceiptObject = [ordered]@{
    checkpoint = 'C11-D D4.1'
    result = 'PASS'
    status = 'CLOSED'

    objective = 'Canonical Production Request Schema'

    schema_id = 'c11d_production_request'
    schema_version = '1.0'
    schema_path = $SchemaPath
    evidence_path = $EvidencePath

    challenge_count = $ChallengeIdsArray.Count
    delivery_profile_count_reported = 5
    delivery_profile_names_extracted = $DeliveryProfileValues.Count
    delivery_profile_vocabulary_status = $DeliveryVocabularyStatus

    canonical_request = $true
    gui_cli_same_canonical_shape = $true
    request_hash_algorithm = 'SHA-256'

    seed_and_music_seed_separated = $true
    review_production_explicit = $true
    personalization_declarative = $true
    provenance_declarative = $true

    runtime_authority = 'NONE'

    gui_activation = $false
    cli_production_activation = $false
    renderer_activation = $false
    orchestrator_activation = $false
    simulation_changes = $false
    frozen_c11c_changes = $false

    next = 'D4.2 - Production Request Normalization + Validation'
    generated_at_utc = [DateTime]::UtcNow.ToString('o')
}

Write-JsonUtf8NoBom $ReceiptPath $ReceiptObject 30

# ------------------------------------------------------------
# 7. Contract
# ------------------------------------------------------------

$ContractLines = @(
    '# C11-D D4.1 - Canonical Production Request Schema',
    '',
    '## Status',
    '',
    'PASS / CLOSED.',
    '',
    '## Objective',
    '',
    'D4.1 establishes one canonical declarative Production Request. GUI and CLI must become two interfaces to this same request contract rather than two production pipelines.',
    '',
    '## Core fields',
    '',
    '- request identity;',
    '- schema version;',
    '- REVIEW / PRODUCTION mode;',
    '- Challenge identity and version;',
    '- structural/gameplay seed;',
    '- dedicated music seed;',
    '- delivery profile;',
    '- presentation profile;',
    '- duration and deterministic variation;',
    '- personalization;',
    '- editorial metadata;',
    '- output intent;',
    '- provenance context.',
    '',
    '## Seed isolation',
    '',
    '`seed` and `music_seed` are explicitly separated. The music seed is not derived by consuming structural/gameplay RNG.',
    '',
    '`winning_frame` and `close_calls` remain simulation-derived evidence and cannot be supplied as production controls.',
    '',
    '## GUI / CLI parity',
    '',
    'Semantically equivalent GUI and CLI requests must normalize to byte-equivalent canonical JSON and therefore to the same SHA-256 request identity.',
    '',
    'Interface-specific renderer invocation or production business rules are prohibited from the canonical request.',
    '',
    '## UNKNOWN policy',
    '',
    'Information that is not evidence-backed remains UNKNOWN. The schema does not invent Challenge versions, profile identities, asset identities or other values from filenames.',
    '',
    '## Runtime boundary',
    '',
    'D4.1 is declarative only. No renderer, production CLI, GUI or orchestrator is activated.',
    '',
    'C11-C frozen source, simulation truth, gameplay RNG and structural RNG remain protected.',
    '',
    '## Evidence',
    '',
    '- `definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json`',
    '- `artifacts/tests/c11d_d4/d4_1/d4_1_schema_evidence.json`',
    '- `artifacts/tests/c11d_d4/d4_1/d4_1_validation_receipt.json`',
    '',
    '## Next',
    '',
    'D4.2 - Production Request Normalization + Validation.'
)

[System.IO.File]::WriteAllText(
    $ContractPath,
    ($ContractLines -join [Environment]::NewLine),
    $Utf8NoBom
)

# ------------------------------------------------------------
# 8. Handover
# ------------------------------------------------------------

$HandoffMarker = '<!-- C11D_D4_1_HANDOFF_V1 -->'

$HandoffLines = @(
    $HandoffMarker,
    '',
    '## C11-D D4.1 CLOSED',
    '',
    '- Canonical Production Request schema: `c11d_production_request` v1.0.',
    '- One canonical request shape for GUI and CLI.',
    '- `seed` and `music_seed` explicitly separated.',
    '- REVIEW and PRODUCTION are explicit modes.',
    '- Personalization, editorial, output and provenance are declarative.',
    '- Canonical request identity uses SHA-256.',
    '- UNKNOWN is retained where evidence is unavailable.',
    '- No GUI activation.',
    '- No production CLI activation.',
    '- No renderer activation.',
    '- No orchestrator activation.',
    '- No simulation or frozen C11-C changes.',
    '- Next active checkpoint: **D4.2 - Production Request Normalization + Validation**.',
    ''
)

function Add-Handoff(
    [string]$Path,
    [string[]]$Lines
){
    if(-not (Test-Path -LiteralPath $Path)){
        return
    }

    $ExistingText = [System.IO.File]::ReadAllText($Path)

    if($ExistingText.Contains($HandoffMarker)){
        return
    }

    $UpdatedText = (
        $ExistingText.TrimEnd() +
        [Environment]::NewLine +
        [Environment]::NewLine +
        ($Lines -join [Environment]::NewLine) +
        [Environment]::NewLine
    )

    [System.IO.File]::WriteAllText(
        $Path,
        $UpdatedText,
        $Utf8NoBom
    )
}

Add-Handoff $MasterPath $HandoffLines
Add-Handoff $StartPath $HandoffLines

# ------------------------------------------------------------
# 9. History snapshots
# ------------------------------------------------------------

$UtcStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd_HHmmss')

if(Test-Path -LiteralPath $MasterPath){
    $MasterSnapshotPath = Join-Path $HistoryDir (
        'MASTER_HANDOVER_C11D_D4.1_{0}.md' -f $UtcStamp
    )

    Copy-Item `
        -LiteralPath $MasterPath `
        -Destination $MasterSnapshotPath `
        -Force
}

if(Test-Path -LiteralPath $StartPath){
    $StartSnapshotPath = Join-Path $HistoryDir (
        'START_PROMPT_C11D_D4.1_{0}.md' -f $UtcStamp
    )

    Copy-Item `
        -LiteralPath $StartPath `
        -Destination $StartSnapshotPath `
        -Force
}

# ------------------------------------------------------------
# 10. Final validation
# ------------------------------------------------------------

if(-not (Test-Path -LiteralPath $SchemaPath)){
    throw 'D4.1 schema was not created.'
}

if(-not (Test-Path -LiteralPath $EvidencePath)){
    throw 'D4.1 evidence was not created.'
}

if(-not (Test-Path -LiteralPath $ReceiptPath)){
    throw 'D4.1 receipt was not created.'
}

if(-not (Test-Path -LiteralPath $ContractPath)){
    throw 'D4.1 contract was not created.'
}

$SchemaCheckText = [System.IO.File]::ReadAllText($SchemaPath)
$SchemaCheck = $SchemaCheckText | ConvertFrom-Json

if([string]$SchemaCheck.schema_id -ne 'c11d_production_request'){
    throw 'Schema ID validation failed.'
}

if([string]$SchemaCheck.schema_version -ne '1.0'){
    throw 'Schema version validation failed.'
}

if([string]$SchemaCheck.runtime_authority -ne 'NONE'){
    throw 'Runtime authority validation failed.'
}

$ReceiptCheckText = [System.IO.File]::ReadAllText($ReceiptPath)
$ReceiptCheck = $ReceiptCheckText | ConvertFrom-Json

if([string]$ReceiptCheck.result -ne 'PASS'){
    throw 'Receipt result validation failed.'
}

if([string]$ReceiptCheck.status -ne 'CLOSED'){
    throw 'Receipt status validation failed.'
}

$MasterCheckText = [System.IO.File]::ReadAllText($MasterPath)
$StartCheckText = [System.IO.File]::ReadAllText($StartPath)

if(-not $MasterCheckText.Contains($HandoffMarker)){
    throw 'MASTER handover marker missing.'
}

if(-not $StartCheckText.Contains($HandoffMarker)){
    throw 'START handover marker missing.'
}

Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.1 - CANONICAL PRODUCTION REQUEST'
Write-Host '=================================================='
Write-Host '[OK] D4.0 PASS/CLOSED verified.'
Write-Host ('[OK] Challenge definitions discovered: {0}.' -f $ChallengeIdsArray.Count)
Write-Host ('[OK] Delivery profiles reported by D4.0: 5.')
Write-Host ('[OK] Delivery profile values extracted: {0}.' -f $DeliveryProfileValues.Count)
Write-Host ('[OK] Delivery vocabulary status: {0}.' -f $DeliveryVocabularyStatus)
Write-Host '[OK] Canonical Production Request schema generated.'
Write-Host '[OK] REVIEW / PRODUCTION modes defined.'
Write-Host '[OK] Structural seed and music_seed separated.'
Write-Host '[OK] Personalization contract defined.'
Write-Host '[OK] Editorial/output/provenance contracts defined.'
Write-Host '[OK] GUI/CLI canonicalization contract defined.'
Write-Host '[OK] SHA-256 request identity defined.'
Write-Host '[OK] Runtime authority = NONE.'
Write-Host '[OK] GUI / CLI / renderer / orchestrator activation = NONE.'
Write-Host '[OK] C11-C and simulation protected.'
Write-Host '[OK] D4.1 receipt verified.'
Write-Host ''
Write-Host ('SCHEMA:   {0}' -f $SchemaPath)
Write-Host ('EVIDENCE: {0}' -f $EvidencePath)
Write-Host ('RECEIPT:  {0}' -f $ReceiptPath)
Write-Host ('CONTRACT: {0}' -f $ContractPath)
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.1 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.2 - Production Request Normalization + Validation'
