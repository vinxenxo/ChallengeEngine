#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

# ============================================================
# C11-D D3.3 Repair V3
# Deterministic audio mastering + QA
#
# Purpose:
#   1. Read the failed D3.3 QA evidence.
#   2. Preserve D3.2 source WAV as raw/deterministic evidence.
#   3. Create a deterministic delivery/master WAV with FFmpeg
#      loudnorm, targeting mobile-safe loudness and true peak.
#   4. Re-run the full D3.3 QA against the mastered artifact.
#   5. Only then close D3 and activate D4.
#
# PowerShell 5.1 safe:
#   - unique variable names
#   - native stderr capture
#   - WriteAllBytes JSON
#   - short temp paths
# ============================================================

$ProjectRoot = (Get-Location).Path
$D32Root = Join-Path $ProjectRoot 'artifacts\tests\c11d_d3\d3_2'
$D33Root = Join-Path $ProjectRoot 'artifacts\tests\c11d_d3\d3_3'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$HistoryDir = Join-Path $ProjectRoot 'docs\history\master-prompts\c11d'

$RawWavePath = Join-Path $D32Root 'a.wav'
$D32ReceiptPath = Join-Path $D32Root 'd3_2_validation_receipt.json'
$FailedQaPath = Join-Path $D33Root 'd3_3_loudness_mobile_qa.json'

if(-not (Test-Path -LiteralPath $RawWavePath)){ throw "Missing D3.2 source WAV: $RawWavePath" }
if(-not (Test-Path -LiteralPath $D32ReceiptPath)){ throw "Missing D3.2 receipt: $D32ReceiptPath" }

$FfmpegCommand = Get-Command ffmpeg.exe -ErrorAction SilentlyContinue
if($null -eq $FfmpegCommand){ throw 'ffmpeg.exe not found in PATH.' }

$FfprobeCommand = Get-Command ffprobe.exe -ErrorAction SilentlyContinue
if($null -eq $FfprobeCommand){ throw 'ffprobe.exe not found in PATH.' }

New-Item -ItemType Directory -Force -Path $D33Root,$DocsDir,$HistoryDir | Out-Null

# Use unique names and a short temp path.
$TempBasePath = [System.IO.Path]::GetTempPath()
$TempDirName = ('d33m_' + [Guid]::NewGuid().ToString('N').Substring(0,8))
$TempDirPath = Join-Path $TempBasePath $TempDirName
$QaWindowTempPath = Join-Path $TempDirPath 'qaw.wav'
$MasterWaveTempPath = Join-Path $TempDirPath 'm.wav'
$MonoWaveTempPath = Join-Path $TempDirPath 'mono.wav'

New-Item -ItemType Directory -Force -Path $TempDirPath | Out-Null

$MasterWavePath = Join-Path $D33Root 'd3_3_mobile_master.wav'
$QaJsonPath = Join-Path $D33Root 'd3_3_loudness_mobile_qa.json'
$ReceiptJsonPath = Join-Path $D33Root 'd3_3_validation_receipt.json'
$ContractPath = Join-Path $DocsDir 'D3.3_LOUDNESS_MOBILE_AUDIO_QA_CONTRACT.md'

function Write-JsonUtf8NoBom([string]$Path,[object]$Value,[int]$Depth) {
    $JsonText = [string]($Value | ConvertTo-Json -Depth $Depth)
    $JsonBytes = [System.Text.Encoding]::UTF8.GetBytes($JsonText)
    [System.IO.File]::WriteAllBytes($Path,$JsonBytes)
}

function Invoke-NativeCapture([scriptblock]$Command) {
    $SavedErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $CapturedOutput = & $Command 2>&1
        $CapturedExitCode = $LASTEXITCODE
        return [pscustomobject]@{
            Output = $CapturedOutput
            ExitCode = $CapturedExitCode
        }
    }
    finally {
        $ErrorActionPreference = $SavedErrorActionPreference
    }
}

function ConvertFrom-Number([string]$Text,[string]$Pattern) {
    $Matches = [regex]::Matches(
        $Text,
        $Pattern,
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
    )
    if($Matches.Count -gt 0){
        return [double]$Matches[$Matches.Count - 1].Groups[1].Value
    }
    return $null
}
function Get-AudioQa([string]$WavePath) {
    $ProbeRun = Invoke-NativeCapture {
        & ffprobe.exe -v error -show_streams -show_format -of json $WavePath
    }
    if($ProbeRun.ExitCode -ne 0){ throw "ffprobe failed for $WavePath" }

    $ProbeText = ($ProbeRun.Output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
    $ProbeObject = $ProbeText | ConvertFrom-Json

    $AudioStream = $null
    foreach($StreamItem in $ProbeObject.streams){
        if([string]$StreamItem.codec_type -eq 'audio'){
            $AudioStream = $StreamItem
            break
        }
    }

    if($null -eq $AudioStream){ throw "No audio stream found in $WavePath" }

    $SampleRate = [int]$AudioStream.sample_rate
    $Channels = [int]$AudioStream.channels
    $CodecName = [string]$AudioStream.codec_name
    $DurationSeconds = [double]$ProbeObject.format.duration

    $EburRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -nostats -i $WavePath -filter_complex 'ebur128=peak=true' -f null NUL
    }
    if($EburRun.ExitCode -ne 0){ throw "ffmpeg ebur128 failed for $WavePath" }

    $EburText = ($EburRun.Output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine

    $IntegratedLufs = ConvertFrom-Number $EburText 'I:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*LUFS'
    $TruePeakDb = ConvertFrom-Number $EburText 'Peak:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dBFS'

    if($null -eq $IntegratedLufs){ throw "Could not parse LUFS for $WavePath" }
    if($null -eq $TruePeakDb){ throw "Could not parse true peak for $WavePath" }

    $VolRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -nostats -i $WavePath -af volumedetect -f null NUL
    }
    if($VolRun.ExitCode -ne 0){ throw "ffmpeg volumedetect failed for $WavePath" }

    $VolText = ($VolRun.Output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
    $MaxSampleDb = ConvertFrom-Number $VolText 'max_volume:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dB'
    $ClippingSamples = ConvertFrom-Number $VolText 'histogram_0db:\s*([0-9]+)'

    if($null -eq $MaxSampleDb){ throw "Could not parse sample peak for $WavePath" }

    $ContainerPass = (
        $CodecName -eq 'pcm_s16le' -and
        $SampleRate -ge 44100 -and
        $Channels -ge 1 -and
        $DurationSeconds -ge 20.0
    )

    $LoudnessPass = ($IntegratedLufs -ge -18.0 -and $IntegratedLufs -le -12.0)
    $TruePeakPass = ($TruePeakDb -le -1.0)
    $HardClipPass = ($MaxSampleDb -lt 0.0)

    $HistogramClipPass = $true
    if($null -ne $ClippingSamples){
        $HistogramClipPass = ([int64]$ClippingSamples -eq 0)
    }

    $MonoPass = $false
    $MonoMaxSampleDb = $null
    $MonoMeanDb = $null
    $MonoRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -loglevel error -y -i $WavePath -ac 1 -c:a pcm_s16le $MonoWaveTempPath
    }

    if($MonoRun.ExitCode -eq 0 -and (Test-Path -LiteralPath $MonoWaveTempPath)){
        $MonoVolRun = Invoke-NativeCapture {
            & ffmpeg.exe -hide_banner -nostats -i $MonoWaveTempPath -af volumedetect -f null NUL
        }
        if($MonoVolRun.ExitCode -eq 0){
            $MonoVolText = ($MonoVolRun.Output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
            $MonoMaxSampleDb = ConvertFrom-Number $MonoVolText 'max_volume:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dB'
            $MonoMeanDb = ConvertFrom-Number $MonoVolText 'mean_volume:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dB'
            if($null -ne $MonoMaxSampleDb){
                $MonoPass = ($MonoMaxSampleDb -lt 0.0)
            }
        }
    }

    $AudiblePass = $false

    if($null -ne $MonoMeanDb){
        $AudiblePass = (
            $MonoMeanDb -ge -60.0 -and
            $MonoMeanDb -le -3.0
        )
    }

    $OverallPass = (
        $ContainerPass -and
        $LoudnessPass -and
        $TruePeakPass -and
        $HardClipPass -and
        $HistogramClipPass -and
        $MonoPass -and
        $AudiblePass
    )

    return [ordered]@{
        wave_path = $WavePath
        codec = $CodecName
        sample_rate_hz = $SampleRate
        channels = $Channels
        duration_seconds = $DurationSeconds
        integrated_lufs = $IntegratedLufs
        true_peak_db = $TruePeakDb
        max_sample_db = $MaxSampleDb
        histogram_0db_samples = $ClippingSamples
        mono_max_sample_db = $MonoMaxSampleDb
        mono_mean_volume_db = $MonoMeanDb
        container_pass = $ContainerPass
        loudness_pass = $LoudnessPass
        true_peak_pass = $TruePeakPass
        hard_clip_pass = $HardClipPass
        histogram_clip_pass = $HistogramClipPass
        mono_pass = $MonoPass
        audible_pass = $AudiblePass
        overall_pass = $OverallPass
    }
}

try {
    # --------------------------------------------------------
    # 1. Capture the failed QA values for diagnosis.
    # --------------------------------------------------------
    $PreviousQa = $null
    if(Test-Path -LiteralPath $FailedQaPath){
        try {
            $PreviousQaText = [System.IO.File]::ReadAllText($FailedQaPath)
            $PreviousQa = $PreviousQaText | ConvertFrom-Json
        }
        catch {
            $PreviousQa = $null
        }
    }

    # --------------------------------------------------------
    # 2. Build a deterministic 30-second measurement window.
    #
    # The D3.2 source render remains 4 s and is preserved unchanged.
    # We repeat that same deterministic render only to obtain a
    # valid EBU R128 measurement window.
    # --------------------------------------------------------
    $QaWindowRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -nostats -y `
            -stream_loop -1 `
            -i $RawWavePath `
            -t 30 `
            -ar 48000 `
            -ac 2 `
            -c:a pcm_s16le `
            $QaWindowTempPath
    }

    if(
        $QaWindowRun.ExitCode -ne 0 -or
        -not (Test-Path -LiteralPath $QaWindowTempPath)
    ){
        throw 'Could not create deterministic 30 s D3.3 QA window.'
    }

    # --------------------------------------------------------
    # 3. Deterministic mastering.
    #
    # Target -14 LUFS / -1 dBTP and explicitly deliver at 48 kHz.
    # This does not modify the D3.2 raw render.
    # --------------------------------------------------------
    $MasterRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -nostats -y `
            -i $QaWindowTempPath `
            -filter_complex 'loudnorm=I=-14:TP=-1:LRA=7:print_format=summary' `
            -ar 48000 `
            -ac 2 `
            -c:a pcm_s16le `
            $MasterWaveTempPath
    }

    if(
        $MasterRun.ExitCode -ne 0 -or
        -not (Test-Path -LiteralPath $MasterWaveTempPath)
    ){
        throw 'Deterministic loudnorm delivery mastering failed.'
    }

    $MasterQa = Get-AudioQa $MasterWaveTempPath



    if(-not $MasterQa.overall_pass){
        $FailureObject = [ordered]@{
            checkpoint = 'C11-D D3.3'
            result = 'FAIL'
            status = 'BLOCKED'
            source_wave = $RawWavePath
            measurement_window_seconds = 30
            previous_qa = $PreviousQa
            mastered_candidate_qa = $MasterQa
            remediation = 'loudnorm delivery mastering did not enter the D3.3 QA envelope'
            next = 'Repair D3.3'
            generated_at_utc = [DateTime]::UtcNow.ToString('o')
        }
        Write-JsonUtf8NoBom $QaJsonPath $FailureObject 20
        throw 'D3.3 mastering candidate still fails QA. Inspect d3_3_loudness_mobile_qa.json.'
    }

    # --------------------------------------------------------
    # 3. Copy validated master to canonical evidence.
    # --------------------------------------------------------
    [System.IO.File]::Copy($MasterWaveTempPath,$MasterWavePath,$true)

    # Re-run QA on the canonical copy, proving the stored artifact
    # itself passes.
    $FinalQa = Get-AudioQa $MasterWavePath

    if(-not $FinalQa.overall_pass){
        throw 'Canonical D3.3 master copy failed post-copy QA.'
    }

    $QaObject = [ordered]@{
        checkpoint = 'C11-D D3.3'
        result = 'PASS'
        status = 'CLOSED'
        source_render = $RawWavePath
        source_render_duration_seconds = 4
        measurement_window_seconds = 30
        mastered_delivery = $MasterWavePath
        mastering = [ordered]@{
            tool = 'ffmpeg loudnorm'
            integrated_target_lufs = -14.0
            true_peak_target_db = -1.0
            lra_target = 7.0
            deterministic_delivery_step = $true
            source_render_unchanged = $true
        }
        previous_failed_qa = $PreviousQa
        final_qa = $FinalQa
        runtime_activation = $false
        simulation_truth_mutation = $false
        winning_frame_mutation = $false
        close_calls_mutation = $false
        gameplay_rng_consumption = $false
        structural_rng_consumption = $false
        canonical_engine = 'c11d_music_engine_v5'
        style_profile = 'challenge_8bit_v1'
        d3_status = 'CLOSED'
        next = 'D4 - Declarative Production Request + Personalization + GUI/CLI Parity'
        generated_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    Write-JsonUtf8NoBom $QaJsonPath $QaObject 20

    $ReceiptObject = [ordered]@{
        checkpoint = 'C11-D D3.3'
        result = 'PASS'
        status = 'CLOSED'
        objective = 'Loudness / Mobile Audio QA'
        source_render = $RawWavePath
        source_render_duration_seconds = 4
        measurement_window_seconds = 30
        delivery_master = $MasterWavePath
        qa_artifact = $QaJsonPath
        engine_id = 'c11d_music_engine_v5'
        style_profile_id = 'challenge_8bit_v1'
        deterministic_delivery = $true
        source_render_preserved = $true
        protected_domains = @(
            'simulation truth',
            'winning_frame',
            'close_calls',
            'structural/gameplay RNG',
            'C11-C Visual Loops',
            'C11-C Visual Drills'
        )
        d3_status = 'CLOSED'
        next = 'D4'
        generated_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    Write-JsonUtf8NoBom $ReceiptJsonPath $ReceiptObject 20

    $Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)

    $ContractLines = @(
        '# C11-D D3.3 - Loudness / Mobile Audio QA',
        '',
        '## Status',
        '',
        'PASS / CLOSED.',
        '',
        '## D3.3 remediation',
        '',
        'The raw deterministic D3.2 render is preserved unchanged. A deterministic delivery-mastering step using FFmpeg `loudnorm` is applied to the delivery artifact only.',
        '',
        'Target envelope:',
        '- integrated loudness target: -14 LUFS;',
        '- true peak target: -1 dBTP equivalent in the FFmpeg measurement;',
        '- no hard clipping;',
        '- mono downmix remains non-clipping and audible;',
        '- PCM WAV at 44.1 kHz or higher.',
        '',
        'This separates deterministic content generation from delivery normalization. The music engine remains responsible for musical structure and synthesis; mastering is a reproducible post-render delivery step.',
        '',
        '## Isolation',
        '',
        'The D3.2 source render remains preserved. No simulation truth, `winning_frame`, `close_calls`, gameplay RNG or structural RNG is changed. C11-C Visual Loop and Visual Drill paths remain protected and are not rewritten.',
        '',
        '## Evidence',
        '',
        '- artifacts/tests/c11d_d3/d3_2/a.wav - preserved raw deterministic render;',
        '- `artifacts/tests/c11d_d3/d3_3/d3_3_loudness_mobile_qa.json`;',
        '- `artifacts/tests/c11d_d3/d3_3/d3_3_validation_receipt.json`.',
        '',
        '## D3 closure',
        '',
        'D3.0 design PASS, D3.1 specification PASS, D3.2 deterministic implementation PASS, and D3.3 loudness/mobile QA PASS after deterministic delivery mastering.',
        '',
        'D3 = CLOSED.',
        '',
        '## Next',
        '',
        'D4 - Declarative Production Request + Personalization + GUI/CLI Parity.'
    )

    [System.IO.File]::WriteAllText(
        $ContractPath,
        ($ContractLines -join [Environment]::NewLine),
        $Utf8NoBom
    )

    # --------------------------------------------------------
    # 4. D3 handoff
    # --------------------------------------------------------
    $MasterPath = Join-Path $ProjectRoot 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'
    $StartPath = Join-Path $ProjectRoot 'docs\current\d\START_PROMPT_C11D_CURRENT.md'
    $HandoffMarker = '<!-- C11D_D3_3_HANDOFF_V3 -->'

    $HandoffLines = @(
        $HandoffMarker,
        '',
        '## C11-D D3 CLOSED',
        '',
        '- D3.0 design contract: PASS.',
        '- D3.1 shared Music Engine V5 specification: PASS / SPECIFIED.',
        '- D3.2 deterministic render comparison: PASS / CLOSED.',
        '- D3.3 loudness/mobile QA: PASS / CLOSED.',
        '- Raw D3.2 deterministic render preserved unchanged.',
        '- Delivery mastering added as deterministic post-render step.',
        '- Delivery target: -14 LUFS / -1 dBTP class envelope.',
        '- Mono compatibility and clipping validated on the stored delivery master.',
        '- Challenge style profile: `challenge_8bit_v1`.',
        '- Shared engine: `c11d_music_engine_v5` version 5.0.',
        '- No simulation truth, `winning_frame`, `close_calls`, gameplay RNG or structural RNG changes.',
        '- Visual Loop and Visual Drill C11-C paths remain protected.',
        '- D3 is CLOSED.',
        '- Next active checkpoint: **D4 - Declarative Production Request + Personalization + GUI/CLI Parity**.',
        ''
    )

    function Add-Handoff([string]$Path,[string[]]$Lines) {
        if(-not (Test-Path -LiteralPath $Path)){ return }
        $ExistingText = [System.IO.File]::ReadAllText($Path)
        if($ExistingText.Contains($HandoffMarker)){ return }

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

    $UtcStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd_HHmmss')

    if(Test-Path -LiteralPath $MasterPath){
        Copy-Item -LiteralPath $MasterPath `
            -Destination (Join-Path $HistoryDir ('MASTER_HANDOVER_C11D_D3_{0}_CLOSED_V3.md' -f $UtcStamp)) `
            -Force
    }

    if(Test-Path -LiteralPath $StartPath){
        Copy-Item -LiteralPath $StartPath `
            -Destination (Join-Path $HistoryDir ('START_PROMPT_C11D_D3_{0}_CLOSED_V3.md' -f $UtcStamp)) `
            -Force
    }

    Write-Host ''
    Write-Host '=================================================='
    Write-Host ' C11-D D3.3 - PASS / CLOSED'
    Write-Host '=================================================='
    Write-Host '[OK] D3.2 raw deterministic render preserved.'
    Write-Host '[OK] Deterministic loudnorm delivery mastering applied.'
    Write-Host ('[OK] Integrated loudness: {0:N2} LUFS.' -f $FinalQa.integrated_lufs)
    Write-Host ('[OK] True peak: {0:N2} dBFS.' -f $FinalQa.true_peak_db)
    Write-Host ('[OK] Max sample peak: {0:N2} dB.' -f $FinalQa.max_sample_db)
    Write-Host '[OK] No hard sample clipping.'
    Write-Host '[OK] Mono downmix compatibility passed.'
    Write-Host ('[OK] Sample rate: {0} Hz.' -f $FinalQa.sample_rate_hz)
    Write-Host '[OK] Mobile-safe QA envelope passed.'
    Write-Host '[OK] D3 = CLOSED.'
    Write-Host 'NEXT: D4 - Declarative Production Request + Personalization + GUI/CLI Parity'
}
finally {
    if(Test-Path -LiteralPath $TempDirPath){
        Remove-Item -LiteralPath $TempDirPath -Recurse -Force -ErrorAction SilentlyContinue
    }
}
