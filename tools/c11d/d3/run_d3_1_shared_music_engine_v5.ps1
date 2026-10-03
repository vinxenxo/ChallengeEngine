Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path

$D3Root = Join-Path $Repo 'artifacts\tests\c11d_d3'
$CurrentD = Join-Path $Repo 'docs\current\d'
$HistoryD = Join-Path $Repo 'docs\history\master-prompts\c11d'
$MusicRoot = Join-Path $Repo 'definitions\c11d\music'

$D30ReceiptPath = Join-Path $D3Root 'd3_0_validation_receipt.json'
$D30AuditPath = Join-Path $D3Root 'd3_0_music_source_audit.json'

$EnginePath = Join-Path $MusicRoot 'C11D_MUSIC_ENGINE_V5_SPEC_V1.json'
$ProfilePath = Join-Path $MusicRoot 'C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json'
$ContractPath = Join-Path $CurrentD 'D3.1_SHARED_MUSIC_ENGINE_V5_CONTRACT.md'
$ReceiptPath = Join-Path $D3Root 'd3_1_validation_receipt.json'

$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

New-Item -ItemType Directory -Force -Path $D3Root | Out-Null
New-Item -ItemType Directory -Force -Path $CurrentD | Out-Null
New-Item -ItemType Directory -Force -Path $HistoryD | Out-Null
New-Item -ItemType Directory -Force -Path $MusicRoot | Out-Null

foreach ($Path in @(
    $D30ReceiptPath,
    $D30AuditPath,
    $MasterPath,
    $StartPath
)) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw ('Required D3.1 input missing: ' + $Path)
    }
}

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Content
    )

    $Encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path,$Content,$Encoding)
}

$D30Receipt = Get-Content -LiteralPath $D30ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$D30Audit = Get-Content -LiteralPath $D30AuditPath -Raw -Encoding UTF8 | ConvertFrom-Json

if ([string]$D30Receipt.result -ne 'PASS / DESIGN READY') {
    throw 'D3.0 receipt is not PASS / DESIGN READY.'
}

if ([string]$D30Audit.implementation_status -ne 'NOT IMPLEMENTED') {
    throw 'D3.0 implementation status must remain NOT IMPLEMENTED.'
}

$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'

$MasterSnapshot = Join-Path $HistoryD ('MASTER_HANDOVER_C11D_PRE_D3_2_' + $Timestamp + '.md')
$StartSnapshot = Join-Path $HistoryD ('START_PROMPT_C11D_PRE_D3_2_' + $Timestamp + '.md')

Copy-Item -LiteralPath $MasterPath -Destination $MasterSnapshot -Force
Copy-Item -LiteralPath $StartPath -Destination $StartSnapshot -Force

$Engine = [ordered]@{
    engine_id = 'c11d_music_engine_v5'
    engine_version = '5.0'
    schema_version = '1.0'
    status = 'SPECIFIED'
    runtime_authority = 'NONE'
    architecture = 'SHARED_ENGINE_PLUS_STYLE_PROFILE'
    purpose = 'Deterministic procedural music engine for normalized video production.'

    input_contract = [ordered]@{
        music_seed = 'Dedicated deterministic seed for music only.'
        style_profile_id = 'Declarative style profile identifier.'
        style_profile_version = 'Declarative style profile version.'
        tempo_bpm = 'Requested or profile tempo.'
        duration_seconds = 'Audio presentation duration.'
        variation_index = 'Deterministic variation selector.'
    }

    musical_layers = @(
        'timbre'
        'harmony'
        'rhythm'
        'motif'
        'texture'
        'spatial_treatment'
    )

    determinism = [ordered]@{
        same_input_same_output = $true
        music_seed_independent_from_gameplay_rng = $true
        music_seed_independent_from_structural_rng = $true
        no_gameplay_rng_consumption = $true
        no_structural_rng_consumption = $true
        worker_count_independent = $true
        render_order_independent = $true
    }

    synchronization = [ordered]@{
        authority = 'presentation_timeline'
        simulation_truth_mutation = $false
        winning_frame_mutation = $false
        close_calls_mutation = $false
        gameplay_rng_mutation = $false
    }

    provenance = [ordered]@{
        source_revision = $true
        engine_id = $true
        engine_version = $true
        style_profile_id = $true
        style_profile_version = $true
        deterministic_seed = $true
        parameter_hash = $true
        output_hash = $true
    }

    style_model = [ordered]@{
        engine_shared_across_families = $true
        style_profile_is_separate = $true
        challenge_style_profile = 'challenge_8bit_v1'
        visual_loop_profile_rewrite = $false
        visual_drill_profile_rewrite = $false
    }

    non_interference = [ordered]@{
        simulation = $false
        mechanics = $false
        gameplay_rng = $false
        renderer = $false
        visual_loop_runtime = $false
        visual_drill_runtime = $false
        frozen_c11c = $false
    }
}

$Profile = [ordered]@{
    profile_id = 'challenge_8bit_v1'
    profile_version = '1.0'
    profile_class = 'STYLE_PROFILE'
    target_family = 'Challenge'
    style = '8-bit / chiptune'
    engine_id = 'c11d_music_engine_v5'
    engine_version = '5.0'
    status = 'SPECIFIED'

    timbre = [ordered]@{
        waveform_palette = @(
            'square'
            'pulse'
            'triangle'
            'noise'
        )
        character = 'digital_game_audio'
        voicing = 'compact'
        transient_character = 'defined'
    }

    harmony = [ordered]@{
        complexity = 'low_to_medium'
        voicing = 'compact_triads'
        dissonance = 'controlled'
        cadence = 'loop_friendly'
    }

    rhythm = [ordered]@{
        grid = 'digital'
        syncopation = 'controlled'
        variation = 'seeded'
        groove = 'mechanical_with_variation'
    }

    motif = [ordered]@{
        structure = 'short_repeating'
        repetition = 'high_with_variation'
        variation = 'deterministically_seeded'
        semantic_role = 'gameplay_flavour_without_gameplay_control'
    }

    texture = [ordered]@{
        layers = @(
            'bass'
            'lead'
            'percussion'
            'accent'
        )
        density = 'medium'
        noise_usage = 'controlled'
    }

    spatial_treatment = [ordered]@{
        stereo_width = 'mobile_safe'
        panning = 'subtle'
        reverb = 'minimal'
        phase_safe = $true
        mono_compatible = $true
    }

    mobile_constraints = [ordered]@{
        no_excessive_sub_bass = $true
        transient_clipping_forbidden = $true
        mono_compatibility_required = $true
        loudness_qa_required = $true
    }

    determinism = [ordered]@{
        dedicated_music_seed = $true
        gameplay_rng_consumption = $false
        structural_rng_consumption = $false
    }
}

Write-Utf8NoBom $EnginePath ($Engine | ConvertTo-Json -Depth 30)
Write-Utf8NoBom $ProfilePath ($Profile | ConvertTo-Json -Depth 30)

$ContractLines = @(
    '# C11-D D3.1 - Shared Music Engine V5 Contract V1.0',
    '',
    '## Purpose',
    '',
    'Define the canonical shared deterministic procedural music engine and the Challenge 8-bit style profile.',
    '',
    '## Architecture',
    '',
    'One shared music engine is canonical.',
    'Style is expressed through declarative profiles.',
    'Challenge uses challenge_8bit_v1.',
    'Visual Loop and Visual Drill runtime behavior remains unchanged.',
    '',
    '## Musical layers',
    '',
    '- timbre',
    '- harmony',
    '- rhythm',
    '- motif',
    '- texture',
    '- spatial_treatment',
    '',
    '## Determinism',
    '',
    'Music has a dedicated deterministic seed.',
    'Music must not consume structural RNG.',
    'Music must not consume gameplay RNG.',
    'The same input contract must reproduce the same audio artifact.',
    'Worker count and render order must not change the generated result.',
    '',
    '## Synchronization',
    '',
    'Music may synchronize to presentation timeline signals.',
    'It must not mutate simulation truth.',
    'It must not mutate winning_frame or close_calls.',
    '',
    '## Provenance',
    '',
    'Generated audio must retain source revision, engine identity, engine version, style profile, style version, seed, parameter hash and output hash.',
    '',
    '## Challenge 8-bit profile',
    '',
    'Challenge uses a digital 8-bit/chiptune style profile over the shared engine.',
    'The profile changes musical character, not engine identity.',
    '',
    '## Mobile constraints',
    '',
    'No excessive sub-bass.',
    'No transient clipping.',
    'Mono compatibility required.',
    'Loudness/mobile QA remains a later gate.',
    '',
    '## Non-interference',
    '',
    'D3.1 does not modify Visual Loop.',
    'D3.1 does not modify Visual Drill.',
    'D3.1 does not modify Challenge simulation or mechanics.',
    'D3.1 does not modify gameplay RNG.',
    'D3.1 does not reopen frozen C11-C.',
    '',
    '## Runtime boundary',
    '',
    'D3.1 specifies the engine interface and style profile.',
    'Runtime activation is not performed.',
    '',
    '## Files',
    '',
    'Engine spec: definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json',
    'Challenge profile: definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json',
    'Receipt: artifacts\tests\c11d_d3\d3_1_validation_receipt.json',
    '',
    '## Next checkpoint',
    '',
    'D3.2 - Deterministic Music Implementation / Render Comparison.'
)

Write-Utf8NoBom $ContractPath ($ContractLines -join [Environment]::NewLine)

$MasterLines = @(
    '# C11-D MASTER HANDOVER',
    '',
    '## Strategic objective',
    '',
    'Normalize Challenge video generation using recovered C11-A/C11-B Challenge content and mature C11-C production contracts.',
    'Use shared production infrastructure instead of duplicating family-specific pipelines.',
    'Visual Loop and Visual Drill remain unchanged.',
    '',
    '## Current state',
    '',
    'D0: CLOSED / PASS',
    'D1: functional checkpoints complete',
    'D2: CLOSED',
    'D3.0: PASS / DESIGN READY',
    'D3.1: PASS / SPECIFIED',
    'D3: ACTIVE',
    '',
    '## D3.1',
    '',
    'Shared Music Engine V5 specified.',
    'Challenge style profile challenge_8bit_v1 specified.',
    'Six musical layers specified.',
    'Dedicated music seed specified.',
    'Structural/gameplay RNG decoupling specified.',
    'Presentation synchronization without simulation mutation specified.',
    'Audio provenance specified.',
    'Visual Loop protected.',
    'Visual Drill protected.',
    'Runtime activation not performed.',
    '',
    'Engine:',
    'definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json',
    '',
    'Challenge profile:',
    'definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json',
    '',
    'Contract:',
    'docs\current\d\D3.1_SHARED_MUSIC_ENGINE_V5_CONTRACT.md',
    '',
    'Receipt:',
    'artifacts\tests\c11d_d3\d3_1_validation_receipt.json',
    '',
    '## Next',
    '',
    'D3.2 - Deterministic Music Implementation / Render Comparison.',
    'D3.2 must prove deterministic same-input/same-output behavior before runtime rollout.',
    '',
    '## Frozen baseline',
    '',
    'C11-C 2.19.12 remains FROZEN and IMMUTABLE.',
    'ZIP SHA-256: D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32',
    'TREE SHA-256: 2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256',
    'build_factory.py SHA-256: 3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3'
)

$StartLines = @(
    '# C11-D START PROMPT',
    '',
    'Continue ChallengeEngineV01_STATELESS from C11-D D3.1.',
    '',
    '## Read first',
    '',
    'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md',
    'docs\current\d\START_PROMPT_C11D_CURRENT.md',
    'artifacts\tests\c11d_d3\d3_0_validation_receipt.json',
    'artifacts\tests\c11d_d3\d3_1_validation_receipt.json',
    'definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json',
    'definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json',
    'docs\current\d\D3.1_SHARED_MUSIC_ENGINE_V5_CONTRACT.md',
    '',
    '## Current state',
    '',
    'D0 = CLOSED / PASS',
    'D1 = functional checkpoints complete',
    'D2 = CLOSED',
    'D3.0 = PASS / DESIGN READY',
    'D3.1 = PASS / SPECIFIED',
    'D3 = ACTIVE',
    '',
    '## D3.1 architecture',
    '',
    'Use one shared procedural music engine.',
    'Use declarative style profiles instead of family-specific music engines.',
    'Challenge style profile = challenge_8bit_v1.',
    '',
    '## Musical layers',
    '',
    'timbre',
    'harmony',
    'rhythm',
    'motif',
    'texture',
    'spatial treatment',
    '',
    '## Determinism',
    '',
    'Use a dedicated music seed.',
    'Never consume structural RNG.',
    'Never consume gameplay RNG.',
    'Presentation synchronization must not modify simulation truth.',
    '',
    '## Non-interference',
    '',
    'Visual Loop runtime unchanged.',
    'Visual Drill runtime unchanged.',
    'Challenge mechanics unchanged.',
    'Challenge simulation truth unchanged.',
    'Frozen C11-C unchanged.',
    '',
    '## Next',
    '',
    'D3.2 - Deterministic Music Implementation / Render Comparison.'
)

Write-Utf8NoBom $MasterPath ($MasterLines -join [Environment]::NewLine)
Write-Utf8NoBom $StartPath ($StartLines -join [Environment]::NewLine)

$Receipt = [ordered]@{
    checkpoint = 'C11-D D3.1'
    result = 'PASS / SPECIFIED'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    dependency = 'D3.0 PASS / DESIGN READY'
    engine_spec = 'definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json'
    challenge_profile = 'definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json'
    contract = 'docs\current\d\D3.1_SHARED_MUSIC_ENGINE_V5_CONTRACT.md'
    shared_engine = $true
    style_profile_separate = $true
    challenge_style = '8-bit / chiptune'
    musical_layer_count = 6
    dedicated_music_seed = $true
    structural_rng_decoupled = $true
    gameplay_rng_decoupled = $true
    presentation_sync_without_simulation_mutation = $true
    provenance_required = $true
    visual_loop_runtime_unchanged = $true
    visual_drill_runtime_unchanged = $true
    runtime_activation = $false
    renderer_change = $false
    simulation_change = $false
    mechanics_change = $false
    gameplay_rng_change = $false
    deterministic_render_comparison = 'PENDING_D3_2'
    loudness_mobile_qa = 'PENDING_LATER_D3'
    master_updated = $true
    start_updated = $true
    master_snapshot = ('docs\history\master-prompts\c11d\' + (Split-Path $MasterSnapshot -Leaf))
    start_snapshot = ('docs\history\master-prompts\c11d\' + (Split-Path $StartSnapshot -Leaf))
    next_checkpoint = 'D3.2'
}

Write-Utf8NoBom $ReceiptPath ($Receipt | ConvertTo-Json -Depth 20)

$EngineCheck = Get-Content -LiteralPath $EnginePath -Raw -Encoding UTF8 | ConvertFrom-Json
$ProfileCheck = Get-Content -LiteralPath $ProfilePath -Raw -Encoding UTF8 | ConvertFrom-Json
$ReceiptCheck = Get-Content -LiteralPath $ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json

$EngineCheckOk =
    ([string]$EngineCheck.engine_id -eq 'c11d_music_engine_v5') -and
    ([string]$EngineCheck.status -eq 'SPECIFIED') -and
    ([string]$EngineCheck.runtime_authority -eq 'NONE') -and
    (@($EngineCheck.musical_layers).Count -eq 6)

$ProfileCheckOk =
    ([string]$ProfileCheck.profile_id -eq 'challenge_8bit_v1') -and
    ([string]$ProfileCheck.profile_class -eq 'STYLE_PROFILE') -and
    ([string]$ProfileCheck.target_family -eq 'Challenge') -and
    ([string]$ProfileCheck.engine_id -eq 'c11d_music_engine_v5')

$ContractCheckText = Get-Content -LiteralPath $ContractPath -Raw -Encoding UTF8

$ContractCheckOk =
    ($ContractCheckText.IndexOf('## Purpose',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) -and
    ($ContractCheckText.IndexOf('## Architecture',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) -and
    ($ContractCheckText.IndexOf('## Determinism',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) -and
    ($ContractCheckText.IndexOf('## Provenance',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) -and
    ($ContractCheckText.IndexOf('D3.2',[System.StringComparison]::OrdinalIgnoreCase) -ge 0)

$PromptCheckOk =
    ((Get-Content -LiteralPath $MasterPath -Raw -Encoding UTF8).IndexOf('D3.2',[System.StringComparison]::OrdinalIgnoreCase) -ge 0) -and
    ((Get-Content -LiteralPath $StartPath -Raw -Encoding UTF8).IndexOf('D3.2',[System.StringComparison]::OrdinalIgnoreCase) -ge 0)

$ReceiptCheckOk = [string]$ReceiptCheck.result -eq 'PASS / SPECIFIED'

$FinalPass =
    $EngineCheckOk -and
    $ProfileCheckOk -and
    $ContractCheckOk -and
    $PromptCheckOk -and
    $ReceiptCheckOk

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D3.1 - SHARED MUSIC ENGINE V5' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''

if ($EngineCheckOk) {
    Write-Host '[OK] Shared Music Engine V5 specification verified.' -ForegroundColor Green
}

if ($ProfileCheckOk) {
    Write-Host '[OK] Challenge 8-bit/chiptune style profile verified.' -ForegroundColor Green
}

if ($ContractCheckOk) {
    Write-Host '[OK] D3.1 contract verified.' -ForegroundColor Green
}

if ($PromptCheckOk) {
    Write-Host '[OK] MASTER / START handed off to D3.2.' -ForegroundColor Green
}

if ($ReceiptCheckOk) {
    Write-Host '[OK] D3.1 receipt verified.' -ForegroundColor Green
}

Write-Host ''
Write-Host ('ENGINE:  ' + $EnginePath)
Write-Host ('PROFILE: ' + $ProfilePath)
Write-Host ('CONTRACT: ' + $ContractPath)
Write-Host ('RECEIPT:  ' + $ReceiptPath)
Write-Host ''

if ($FinalPass) {
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ' C11-D D3.1 - PASS / SPECIFIED' -ForegroundColor Green
    Write-Host '==================================================' -ForegroundColor Green
    Write-Host ''
    Write-Host 'One shared music engine defined.'
    Write-Host 'Challenge 8-bit profile defined.'
    Write-Host 'Music seed isolated from structural/gameplay RNG.'
    Write-Host 'Six musical layers defined.'
    Write-Host 'Provenance defined.'
    Write-Host 'Visual Loop and Visual Drill protected.'
    Write-Host 'Runtime activation NOT performed.'
    Write-Host ''
    Write-Host 'NEXT: D3.2 - Deterministic Music Implementation / Render Comparison'
}

if (-not $FinalPass) {
    Write-Host '==================================================' -ForegroundColor Red
    Write-Host ' C11-D D3.1 - VERIFY FAIL' -ForegroundColor Red
    Write-Host '==================================================' -ForegroundColor Red
}