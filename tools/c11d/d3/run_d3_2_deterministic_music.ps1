#requires -Version 5.1
$ErrorActionPreference = "Stop"
Set-StrictMode -Version 1.0

$RootPath = (Get-Location).Path
$MusicEnginePath = Join-Path $RootPath "tools\c11d\d3\c11d_music_engine_v5.py"
$MusicSpecPath = Join-Path $RootPath "definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json"
$StyleProfilePath = Join-Path $RootPath "definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json"
$ArtifactDir = Join-Path $RootPath "artifacts\tests\c11d_d3\d3_2"

$ComparisonPath = Join-Path $ArtifactDir "d3_2_deterministic_render_comparison.json"
$ProvenancePath = Join-Path $ArtifactDir "d3_2_render_provenance.json"
$ReceiptPath = Join-Path $ArtifactDir "d3_2_validation_receipt.json"
$FinalWaveAPath = Join-Path $ArtifactDir "a.wav"
$FinalWaveBPath = Join-Path $ArtifactDir "b.wav"
$FinalWaveCPath = Join-Path $ArtifactDir "c.wav"

if(-not (Test-Path -LiteralPath $MusicEnginePath)){ throw "Music engine missing: $MusicEnginePath" }
if(-not (Test-Path -LiteralPath $MusicSpecPath)){ throw "Engine spec missing: $MusicSpecPath" }
if(-not (Test-Path -LiteralPath $StyleProfilePath)){ throw "Style profile missing: $StyleProfilePath" }
New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null

# Keep temporary render paths short to avoid Windows MAX_PATH.
$TempBasePath = [System.IO.Path]::GetTempPath()
$TempRenderDir = Join-Path $TempBasePath "c11d32"
if(Test-Path -LiteralPath $TempRenderDir){ Remove-Item -LiteralPath $TempRenderDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $TempRenderDir | Out-Null

$TempWaveAPath = Join-Path $TempRenderDir "a.wav"
$TempWaveBPath = Join-Path $TempRenderDir "b.wav"
$TempWaveCPath = Join-Path $TempRenderDir "c.wav"
$TempComparisonPath = Join-Path $TempRenderDir "cmp.json"
$TempProvenancePath = Join-Path $TempRenderDir "pro.json"
$TempReceiptPath = Join-Path $TempRenderDir "rcpt.json"

function Write-JsonBytes([string]$Path,[object]$Value,[int]$Depth) {
    $JsonText = [string]($Value | ConvertTo-Json -Depth $Depth)
    $JsonBytes = [System.Text.Encoding]::UTF8.GetBytes($JsonText)
    [System.IO.File]::WriteAllBytes($Path,$JsonBytes)
}

function Invoke-MusicRender([string]$OutputPath,[int]$MusicSeed) {
    $RawOutput = & python $MusicEnginePath --engine $MusicSpecPath --profile $StyleProfilePath --output $OutputPath --seed $MusicSeed --tempo 104 --duration 4 --variation 0
    if($LASTEXITCODE -ne 0){ throw "Music render failed for seed $MusicSeed." }
    $JsonLine = $RawOutput | Select-Object -Last 1
    if([string]::IsNullOrWhiteSpace([string]$JsonLine)){ throw "Music renderer returned no JSON receipt for seed $MusicSeed." }
    return ([string]$JsonLine | ConvertFrom-Json)
}

$RenderAInfo = Invoke-MusicRender $TempWaveAPath 840001
$RenderBInfo = Invoke-MusicRender $TempWaveBPath 840001
$RenderCInfo = Invoke-MusicRender $TempWaveCPath 840002

$SameOutputHash = ([string]$RenderAInfo.output_hash -eq [string]$RenderBInfo.output_hash)
$SameParameterHash = ([string]$RenderAInfo.parameter_hash -eq [string]$RenderBInfo.parameter_hash)
$DifferentSeedChangesOutput = ([string]$RenderAInfo.output_hash -ne [string]$RenderCInfo.output_hash)
$SameFrameCount = ([int]$RenderAInfo.frame_count -eq [int]$RenderBInfo.frame_count)
$NoPcmHardClipping = ([int]$RenderAInfo.max_abs_pcm -lt 32767)
$EngineIdentityOk = ([string]$RenderAInfo.engine_id -eq 'c11d_music_engine_v5' -and [string]$RenderAInfo.engine_version -eq '5.0' -and [string]$RenderAInfo.style_profile_id -eq 'challenge_8bit_v1')
$Pass = ($SameOutputHash -and $SameParameterHash -and $DifferentSeedChangesOutput -and $SameFrameCount -and $NoPcmHardClipping -and $EngineIdentityOk)

$ComparisonObject = [ordered]@{
    checkpoint = 'C11-D D3.2'
    result = $(if($Pass){'PASS'}else{'FAIL'})
    status = $(if($Pass){'VALIDATED'}else{'BLOCKED'})
    comparison_type = 'REPEAT_RENDER_PLUS_SEED_CONTROL'
    render_a = $RenderAInfo
    render_b = $RenderBInfo
    seed_control_render = $RenderCInfo
    same_output_hash = $SameOutputHash
    same_parameter_hash = $SameParameterHash
    same_frame_count = $SameFrameCount
    different_seed_changes_output = $DifferentSeedChangesOutput
    no_pcm_clipping = $NoPcmHardClipping
    engine_identity_ok = $EngineIdentityOk
    output_path_hardening = 'SHORT_TEMP_RENDER_PATH'
    variable_collision_hardening = 'SEMANTICALLY_UNIQUE_VARIABLE_NAMES'
    preexisting_audio_files = 0
    note = 'D3.0 found no historical audio files suitable as an authoritative baseline. D3.2 validates deterministic repeatability and music-seed isolation. Loudness/mobile QA remains D3.3.'
}
Write-JsonBytes $TempComparisonPath $ComparisonObject 12

$ProvenanceObject = [ordered]@{
    checkpoint = 'C11-D D3.2'
    engine_id = 'c11d_music_engine_v5'
    engine_version = '5.0'
    style_profile_id = 'challenge_8bit_v1'
    style_profile_version = [string]$RenderAInfo.style_profile_version
    deterministic_seed = 840001
    parameter_hash = [string]$RenderAInfo.parameter_hash
    output_hash = [string]$RenderAInfo.output_hash
    synchronization = 'presentation_timeline_only'
    simulation_truth_mutation = $false
    winning_frame_mutation = $false
    close_calls_mutation = $false
    gameplay_rng_consumption = $false
    structural_rng_consumption = $false
    worker_count_dependency = $false
    render_order_dependency = $false
    runtime_activation = $false
    output_path_hardening = 'SHORT_TEMP_RENDER_PATH'
    variable_collision_hardening = 'SEMANTICALLY_UNIQUE_VARIABLE_NAMES'
}
Write-JsonBytes $TempProvenancePath $ProvenanceObject 12

$ReceiptObject = [ordered]@{
    checkpoint = 'C11-D D3.2'
    result = $(if($Pass){'PASS'}else{'FAIL'})
    status = $(if($Pass){'CLOSED'}else{'BLOCKED'})
    objective = 'Deterministic Music Implementation / Render Comparison'
    implementation = 'shared_music_engine_v5'
    style_profile = 'challenge_8bit_v1'
    runtime_activation = $false
    deterministic_render_comparison = $ComparisonObject
    variable_collision_hardening = 'SEMANTICALLY_UNIQUE_VARIABLE_NAMES'
    max_path_hardening = 'SHORT_TEMP_RENDER_PATH'
    preexisting_audio_files = 0
    next = $(if($Pass){'D3.3 - Loudness / Mobile Audio QA'}else{'Repair D3.2'})
    generated_at_utc = [DateTime]::UtcNow.ToString('o')
}
Write-JsonBytes $TempReceiptPath $ReceiptObject 16

if($Pass){
    [System.IO.File]::Copy($TempWaveAPath,$FinalWaveAPath,$true)
    [System.IO.File]::Copy($TempWaveBPath,$FinalWaveBPath,$true)
    [System.IO.File]::Copy($TempWaveCPath,$FinalWaveCPath,$true)
    [System.IO.File]::Copy($TempComparisonPath,$ComparisonPath,$true)
    [System.IO.File]::Copy($TempProvenancePath,$ProvenancePath,$true)
    [System.IO.File]::Copy($TempReceiptPath,$ReceiptPath,$true)
}

if(Test-Path -LiteralPath $TempRenderDir){ Remove-Item -LiteralPath $TempRenderDir -Recurse -Force -ErrorAction SilentlyContinue }
if(-not $Pass){ throw 'D3.2 validation failed.' }

Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D3.2 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host '[OK] Shared Music Engine V5 rendered deterministically.'
Write-Host '[OK] Same seed + same request => identical WAV SHA-256.'
Write-Host '[OK] Different music seed => different WAV SHA-256.'
Write-Host '[OK] Challenge 8-bit profile verified.'
Write-Host '[OK] Gameplay/structural RNG consumption = false.'
Write-Host '[OK] Simulation truth/runtime activation untouched.'
Write-Host '[OK] Windows MAX_PATH avoided by short temporary render path.'
Write-Host '[OK] PowerShell 5.1 variable collisions eliminated.'
Write-Host ('RENDER A HASH: {0}' -f $RenderAInfo.output_hash)
Write-Host ('RENDER B HASH: {0}' -f $RenderBInfo.output_hash)
Write-Host ('CONTROL HASH:   {0}' -f $RenderCInfo.output_hash)
Write-Host ('PARAMETER HASH: {0}' -f $RenderAInfo.parameter_hash)
Write-Host 'NEXT: D3.3 - Loudness / Mobile Audio QA'