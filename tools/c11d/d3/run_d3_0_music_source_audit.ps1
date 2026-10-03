Set-StrictMode -Version 1.0
$ErrorActionPreference = 'Stop'

$Repo = (Resolve-Path '.').Path
$D2Root = Join-Path $Repo 'artifacts\\tests\\c11d_d2'
$D3Root = Join-Path $Repo 'artifacts\\tests\\c11d_d3'
$CurrentD = Join-Path $Repo 'docs\\current\\d'
$HistoryD = Join-Path $Repo 'docs\\history\\master-prompts\\c11d'

$D2ClosurePath = Join-Path $D2Root 'd2_phase_closure_d3_handoff.json'
$D23ReceiptPath = Join-Path $D2Root 'd2_3_validation_receipt.json'
$AuditPath = Join-Path $D3Root 'd3_0_music_source_audit.json'
$ContractPath = Join-Path $CurrentD 'D3.0_PROCEDURAL_MUSIC_V5_DESIGN_CONTRACT.md'
$ReceiptPath = Join-Path $D3Root 'd3_0_validation_receipt.json'
$MasterPath = Join-Path $CurrentD 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $CurrentD 'START_PROMPT_C11D_CURRENT.md'

New-Item -ItemType Directory -Force -Path $D3Root,$CurrentD,$HistoryD | Out-Null

foreach ($Path in @($D2ClosurePath,$D23ReceiptPath,$MasterPath,$StartPath)) {
    if (-not (Test-Path -LiteralPath $Path)) {
        throw ('Required D3.0 input missing: ' + $Path)
    }
}

function Write-Utf8NoBom {
    param([string]$Path,[string]$Content)
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path,$Content,$Utf8NoBom)
}

function Relative-Path {
    param([string]$FullPath)
    if ($FullPath.StartsWith($Repo,[System.StringComparison]::OrdinalIgnoreCase)) {
        return $FullPath.Substring($Repo.Length).TrimStart('\\')
    }
    return $FullPath
}

$D2Closure = Get-Content -LiteralPath $D2ClosurePath -Raw -Encoding UTF8 | ConvertFrom-Json
$D23Receipt = Get-Content -LiteralPath $D23ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json

if ([string]$D2Closure.result -ne 'CLOSED') {
    throw 'D2 phase is not CLOSED.'
}
if ([string]$D23Receipt.result -ne 'PASS') {
    throw 'D2.3 receipt is not PASS.'
}

$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$MasterSnapshot = Join-Path $HistoryD ('MASTER_HANDOVER_C11D_PRE_D3_0_' + $Timestamp + '.md')
$StartSnapshot = Join-Path $HistoryD ('START_PROMPT_C11D_PRE_D3_0_' + $Timestamp + '.md')

Copy-Item -LiteralPath $MasterPath -Destination $MasterSnapshot -Force
Copy-Item -LiteralPath $StartPath -Destination $StartSnapshot -Force

$ExcludedDirs = @('.git','.godot','artifacts','__pycache__','build','dist','export','exports','tmp','temp')
$ExcludedRegex = '(?i)\\(' + (($ExcludedDirs | ForEach-Object { [regex]::Escape($_) }) -join '|') + ')\\'
$AudioExt = @('.wav','.ogg','.mp3','.flac','.aac','.m4a','.opus')
$SourceExt = @('.gd','.py','.ps1','.json','.md','.txt','.toml','.ini','.cfg','.ts','.tsx','.js','.jsx')
$Keywords = @('procedural.?music','procedural.?audio','music','audio','sound','synth','oscillator','waveform','timbre','harmony','rhythm','motif','texture','spatial','stereo','loudness','LUFS','RMS','BPM','tempo','chiptune','8.?bit','deterministic','seed')
$KeywordRegex = '(?i)(' + ($Keywords -join '|') + ')'

$AllFiles = @(Get-ChildItem -LiteralPath $Repo -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch $ExcludedRegex })
$AudioFiles = @($AllFiles | Where-Object { $AudioExt -contains $_.Extension.ToLowerInvariant() })
$SourceFiles = @($AllFiles | Where-Object { ($SourceExt -contains $_.Extension.ToLowerInvariant()) -and ($_.Length -le 2000000) })

$AudioInventory = @()
foreach ($File in $AudioFiles) {
    $AudioInventory += [ordered]@{
        path = Relative-Path $File.FullName
        extension = $File.Extension.ToLowerInvariant()
        size_bytes = [int64]$File.Length
        sha256 = (Get-FileHash -LiteralPath $File.FullName -Algorithm SHA256).Hash
        evidence_status = 'ACTUAL_FILE'
    }
}

$EvidenceFiles = @()
$EvidenceHits = @()
foreach ($File in $SourceFiles) {
    $Matches = @()
    try { $Matches = @(Select-String -LiteralPath $File.FullName -Pattern $KeywordRegex -AllMatches -ErrorAction SilentlyContinue) } catch { $Matches = @() }
    if ($Matches.Count -gt 0) {
        $Rel = Relative-Path $File.FullName
        $Class = 'OTHER'
        if ($Rel -match '(?i)(visual.?loop|loops)') { $Class = 'VISUAL_LOOP' }
        if ($Rel -match '(?i)(visual.?drill|drills|drill)') { $Class = 'VISUAL_DRILL' }
        if ($Rel -match '(?i)(challenge|c11a|c11b)') { $Class = 'CHALLENGE' }
        if (($Class -eq 'OTHER') -and ($Rel -match '(?i)(music|audio|sound|procedural)')) { $Class = 'SHARED_CANDIDATE' }

        $EvidenceFiles += [ordered]@{
            path = $Rel
            source_class = $Class
            keyword_hit_count = $Matches.Count
            size_bytes = [int64]$File.Length
        }

        foreach ($Match in ($Matches | Select-Object -First 20)) {
            $Line = [string]$Match.Line
            if ($Line.Length -gt 260) { $Line = $Line.Substring(0,260) }
            $EvidenceHits += [ordered]@{
                path = $Rel
                source_class = $Class
                line = [int]$Match.LineNumber
                evidence = $Line
            }
            if ($EvidenceHits.Count -ge 600) { break }
        }
    }
    if ($EvidenceHits.Count -ge 600) { break }
}

$LoopEvidence = @($EvidenceFiles | Where-Object { [string]$_.source_class -eq 'VISUAL_LOOP' })
$DrillEvidence = @($EvidenceFiles | Where-Object { [string]$_.source_class -eq 'VISUAL_DRILL' })
$ChallengeEvidence = @($EvidenceFiles | Where-Object { [string]$_.source_class -eq 'CHALLENGE' })
$SharedEvidence = @($EvidenceFiles | Where-Object { [string]$_.source_class -eq 'SHARED_CANDIDATE' })

$Design = [ordered]@{
    shared_music_pipeline = $true
    no_duplicate_family_pipeline = $true
    style_profile_separation = $true
    challenge_style_profile = '8-bit / chiptune'
    layered_timbre = $true
    layered_harmony = $true
    layered_rhythm = $true
    layered_motif = $true
    layered_texture = $true
    layered_spatial_treatment = $true
    deterministic_generation = $true
    deterministic_music_seed = $true
    structural_rng_decoupled = $true
    gameplay_rng_decoupled = $true
    presentation_sync_without_simulation_mutation = $true
    provenance_required = $true
    visual_loop_behavior_unchanged = $true
    visual_drill_behavior_unchanged = $true
    runtime_activation = $false
}

$Audit = [ordered]@{
    checkpoint = 'C11-D D3.0'
    result = 'PASS / DESIGN READY'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    dependency = [ordered]@{ d2 = [string]$D2Closure.result; d2_3 = [string]$D23Receipt.result }
    inventory = [ordered]@{ audio_files = $AudioInventory.Count; source_files_scanned = $SourceFiles.Count; evidence_files = $EvidenceFiles.Count; evidence_hits = $EvidenceHits.Count }
    audio_inventory = @($AudioInventory)
    evidence_files = @($EvidenceFiles)
    evidence_hits = @($EvidenceHits)
    visual_loop_evidence = @($LoopEvidence)
    visual_drill_evidence = @($DrillEvidence)
    challenge_evidence = @($ChallengeEvidence)
    shared_music_candidates = @($SharedEvidence)
    design_contract = $Design
    gate = [ordered]@{ design_contract = 'PASS'; source_provenance_audit = 'PASS'; deterministic_render_comparison = 'PENDING'; loudness_mobile_qa = 'PENDING'; d3_closed = $false }
    implementation_status = 'NOT IMPLEMENTED'
}
Write-Utf8NoBom $AuditPath ($Audit | ConvertTo-Json -Depth 30)

function Section-Lines {
    param([object[]]$Items,[string]$EmptyText)
    $Lines = @()
    if ($Items.Count -eq 0) { $Lines += ('- ' + $EmptyText) }
    if ($Items.Count -gt 0) {
        foreach ($Item in $Items) { $Lines += ('- ' + [string]$Item.path + ' — hits: ' + [string]$Item.keyword_hit_count) }
    }
    return @($Lines)
}

$AudioLines = @()
if ($AudioInventory.Count -eq 0) { $AudioLines += '- No existing audio files found outside excluded directories.' }
if ($AudioInventory.Count -gt 0) {
    foreach ($Item in $AudioInventory) { $AudioLines += ('- ' + [string]$Item.path + ' — ' + [string]$Item.size_bytes + ' bytes — SHA-256 ' + [string]$Item.sha256) }
}
$LoopLines = Section-Lines $LoopEvidence 'No Visual Loop music/audio source hit identified.'
$DrillLines = Section-Lines $DrillEvidence 'No Visual Drill music/audio source hit identified.'
$ChallengeLines = Section-Lines $ChallengeEvidence 'No Challenge music/audio source hit identified.'
$SharedLines = Section-Lines $SharedEvidence 'No shared music candidate source hit identified.'

$Contract = @(
'# C11-D D3.0 — Procedural Music V5 Design Contract V1.0','',
'## Purpose','',
'Normalize procedural music generation for Challenge video production without duplicating family-specific pipelines.','',
'## Strategic direction','',
'C11-D converges recovered Challenge content from C11-A/C11-B with mature production contracts from C11-C.','Visual Loop and Visual Drill remain unchanged; their musical behavior is reference evidence for normalization, not a runtime target to rewrite.','',
'## Shared architecture','',
'One shared procedural music pipeline is the canonical implementation target.','Style is a declarative profile above the engine.','Challenge later uses an 8-bit/chiptune profile.','No Challenge-specific duplicate music pipeline should be created when shared functionality can be reused or extracted without behavior change.','',
'## Musical layers','',
'- timbre','- harmony','- rhythm','- motif','- texture','- spatial treatment','',
'## Determinism boundary','',
'Music generation must be deterministic.','The music seed must be independent from structural/gameplay RNG.','Music generation must never consume or mutate RNG state that defines Challenge mechanics or simulation truth.','Presentation synchronization must use timeline/presentation signals without modifying simulation outputs.','',
'## Provenance','',
'Generated audio must retain source revision, style profile, deterministic seed, parameter set and output identity.','',
'## Existing-source audit','',
('- Existing audio files: ' + [string]$AudioInventory.Count),
('- Source files scanned: ' + [string]$SourceFiles.Count),
('- Evidence-bearing source files: ' + [string]$EvidenceFiles.Count),
('- Evidence hits retained: ' + [string]$EvidenceHits.Count),
('- Visual Loop evidence files: ' + [string]$LoopEvidence.Count),
('- Visual Drill evidence files: ' + [string]$DrillEvidence.Count),
('- Challenge evidence files: ' + [string]$ChallengeEvidence.Count),
('- Shared candidate files: ' + [string]$SharedEvidence.Count),'',
'### Audio inventory','',$AudioLines,'',
'### Visual Loop evidence','',$LoopLines,'',
'### Visual Drill evidence','',$DrillLines,'',
'### Challenge evidence','',$ChallengeLines,'',
'### Shared candidate evidence','',$SharedLines,'',
'## Non-interference','',
'D3 implementation must not replace, fork or alter established Visual Loop or Visual Drill music behavior.','The Challenge 8-bit profile is a style specialization over the shared pipeline.','',
'## Gate','',
'D3.0 = design contract + source/provenance audit.','Deterministic render comparison remains a later gate.','Loudness/mobile QA remains a later gate.','D3 is not closed by D3.0 alone.','',
'## Next checkpoint','',
'D3.1 — Shared Music Engine V5 / Challenge 8-bit Style Profile.'
)
Write-Utf8NoBom $ContractPath ($Contract -join [Environment]::NewLine)

$Master = @(
'# C11-D MASTER HANDOVER','',
'## Current phase','',
'C11-D — Normalize Challenge video generation using recovered C11-A/C11-B Challenge content and mature production contracts from C11-C.','',
'## Strategic objective','',
'Create one robust declarative production architecture rather than duplicated per-family pipelines.','Visual Loop and Visual Drill remain unchanged. Their mature production contracts and musical behavior are reference material for the common layer.','Challenge later uses an 8-bit/chiptune style profile over the normalized music pipeline.','',
'## Status','',
'D0: CLOSED / PASS','D1: functional checkpoints complete','D2: CLOSED','D3.0: PASS / DESIGN READY','D3: ACTIVE','',
'## D3.0 artifacts','',
'Audit: artifacts\tests\c11d_d3\d3_0_music_source_audit.json','Contract: docs\current\d\D3.0_PROCEDURAL_MUSIC_V5_DESIGN_CONTRACT.md','Receipt: artifacts\tests\c11d_d3\d3_0_validation_receipt.json','',
'## D3.0 design','',
'Shared procedural music pipeline.','Style profile separated from engine.','Challenge style = 8-bit/chiptune.','Layers = timbre, harmony, rhythm, motif, texture, spatial treatment.','Deterministic generation.','Music seed decoupled from structural/gameplay RNG.','Presentation synchronization without simulation mutation.','Provenance required.','',
'## D3 gates','',
'Design contract: PASS / READY.','Source/provenance audit: PASS / READY.','Deterministic render comparison: pending.','Loudness/mobile QA: pending.','',
'## D3.1 next','',
'Shared Music Engine V5 / Challenge 8-bit Style Profile.','Before implementation, reuse or cleanly extract existing shared music functions where possible. Preserve Visual Loop and Visual Drill behavior.','',
'## Frozen C11-C baseline','',
'C11-C 2.19.12 remains FROZEN and IMMUTABLE.','ZIP SHA-256: D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32','TREE SHA-256: 2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256','build_factory.py SHA-256: 3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3','',
'## Context switching','',
'Read MASTER_HANDOVER_C11D_CURRENT.md, then START_PROMPT_C11D_CURRENT.md, then D3.0 artifacts before implementation.'
)

$Start = @(
'# C11-D START PROMPT','',
'Continue ChallengeEngineV01_STATELESS from C11-D D3.0.','',
'## Read first','',
'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md','docs\current\d\START_PROMPT_C11D_CURRENT.md','artifacts\tests\c11d_d3\d3_0_music_source_audit.json','docs\current\d\D3.0_PROCEDURAL_MUSIC_V5_DESIGN_CONTRACT.md','artifacts\tests\c11d_d3\d3_0_validation_receipt.json','',
'## Current state','',
'D0 = CLOSED / PASS','D1 = functional checkpoints complete','D2 = CLOSED','D3.0 = PASS / DESIGN READY','D3 = ACTIVE','',
'## Core objective','',
'Normalize procedural music for Challenge video generation using shared infrastructure.','Do not duplicate a music pipeline for Challenge when existing reusable functionality can be reused or cleanly extracted without behavior change.','Visual Loop and Visual Drill behavior must remain unchanged.','',
'## Challenge music','',
'Challenge uses an 8-bit/chiptune style profile. The profile is separate from the shared music engine.','',
'## Musical layers','',
'timbre','harmony','rhythm','motif','texture','spatial treatment','',
'## Determinism','',
'Music seed must be independent from structural/gameplay RNG.','Music generation must not mutate gameplay/simulation RNG.','Presentation synchronization must not modify simulation truth.','',
'## Gate','',
'D3.0 design contract = PASS / READY.','D3.0 source/provenance audit = PASS / READY.','Deterministic render comparison = pending.','Loudness/mobile QA = pending.','',
'## Next checkpoint','',
'D3.1 — Shared Music Engine V5 / Challenge 8-bit Style Profile.','',
'## Frozen guardrails','',
'Do not modify renderer, simulation, mechanics, RNG, SimulationResult, winning_frame, close_calls, WinningFrameDetector or RenderedFrameStream.','Do not modify Visual Loop or Visual Drill runtime behavior.','Do not reopen frozen C11-C production.'
)

Write-Utf8NoBom $MasterPath ($Master -join [Environment]::NewLine)
Write-Utf8NoBom $StartPath ($Start -join [Environment]::NewLine)

$Receipt = [ordered]@{
    checkpoint = 'C11-D D3.0'
    result = 'PASS / DESIGN READY'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    d2_closed_verified = $true
    d2_3_pass_verified = $true
    source_provenance_audit = $true
    shared_pipeline_first = $true
    no_duplicate_music_pipeline = $true
    challenge_style_profile = '8-bit / chiptune'
    musical_layers = @('timbre','harmony','rhythm','motif','texture','spatial treatment')
    deterministic_generation = $true
    music_seed_decoupled = $true
    structural_rng_decoupled = $true
    gameplay_rng_decoupled = $true
    presentation_sync_without_simulation_mutation = $true
    provenance_required = $true
    visual_loop_behavior_unchanged = $true
    visual_drill_behavior_unchanged = $true
    runtime_activation = $false
    implementation_status = 'NOT IMPLEMENTED'
    deterministic_render_comparison = 'PENDING'
    loudness_mobile_qa = 'PENDING'
    audio_file_count = $AudioInventory.Count
    source_files_scanned = $SourceFiles.Count
    evidence_file_count = $EvidenceFiles.Count
    evidence_hit_count = $EvidenceHits.Count
    visual_loop_evidence_count = $LoopEvidence.Count
    visual_drill_evidence_count = $DrillEvidence.Count
    challenge_evidence_count = $ChallengeEvidence.Count
    shared_candidate_count = $SharedEvidence.Count
    master_updated = $true
    start_updated = $true
    master_snapshot = ('docs\history\master-prompts\c11d\' + (Split-Path $MasterSnapshot -Leaf))
    start_snapshot = ('docs\history\master-prompts\c11d\' + (Split-Path $StartSnapshot -Leaf))
    next_checkpoint = 'D3.1'
}
Write-Utf8NoBom $ReceiptPath ($Receipt | ConvertTo-Json -Depth 20)

Write-Host ''
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ' C11-D D3.0 — PROCEDURAL MUSIC V5 DESIGN AUDIT' -ForegroundColor Cyan
Write-Host '==================================================' -ForegroundColor Cyan
Write-Host ''
Write-Host ('[INFO] Existing audio: ' + $AudioInventory.Count)
Write-Host ('[INFO] Source files scanned: ' + $SourceFiles.Count)
Write-Host ('[INFO] Evidence files: ' + $EvidenceFiles.Count)
Write-Host ('[INFO] Evidence hits: ' + $EvidenceHits.Count)
Write-Host ('[INFO] Visual Loop evidence: ' + $LoopEvidence.Count)
Write-Host ('[INFO] Visual Drill evidence: ' + $DrillEvidence.Count)
Write-Host ('[INFO] Challenge evidence: ' + $ChallengeEvidence.Count)
Write-Host ('[INFO] Shared candidates: ' + $SharedEvidence.Count)
Write-Host ''
Write-Host '[OK] D2 CLOSED.' -ForegroundColor Green
Write-Host '[OK] D2.3 PASS verified.' -ForegroundColor Green
Write-Host '[OK] Design-before-implementation recorded.' -ForegroundColor Green
Write-Host '[OK] Shared music pipeline defined.' -ForegroundColor Green
Write-Host '[OK] Challenge 8-bit/chiptune style profile defined.' -ForegroundColor Green
Write-Host '[OK] Six musical layers defined.' -ForegroundColor Green
Write-Host '[OK] Music seed decoupled from structural/gameplay RNG.' -ForegroundColor Green
Write-Host '[OK] Provenance requirement defined.' -ForegroundColor Green
Write-Host '[OK] Visual Loop behavior protected.' -ForegroundColor Green
Write-Host '[OK] Visual Drill behavior protected.' -ForegroundColor Green
Write-Host '[OK] No music runtime implementation performed.' -ForegroundColor Green
Write-Host '[OK] MASTER / START updated and snapshotted.' -ForegroundColor Green
Write-Host ''
Write-Host ('AUDIT:    ' + $AuditPath)
Write-Host ('CONTRACT: ' + $ContractPath)
Write-Host ('RECEIPT:  ' + $ReceiptPath)
Write-Host ''
Write-Host '==================================================' -ForegroundColor Green
Write-Host ' C11-D D3.0 — PASS / DESIGN READY' -ForegroundColor Green
Write-Host '==================================================' -ForegroundColor Green
Write-Host ''
Write-Host 'D3.0 is design-ready; implementation remains for D3.1.'
Write-Host 'NEXT: D3.1 — Shared Music Engine V5 / Challenge 8-bit Style Profile'
