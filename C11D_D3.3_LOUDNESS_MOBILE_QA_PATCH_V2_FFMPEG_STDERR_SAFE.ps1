#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Get-Location).Path
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d3\d3_3'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$HistoryDir = Join-Path $ProjectRoot 'docs\history\master-prompts\c11d'
$D32ReceiptPath = Join-Path $ProjectRoot 'artifacts\tests\c11d_d3\d3_2\d3_2_validation_receipt.json'
$D32WavePath = Join-Path $ProjectRoot 'artifacts\tests\c11d_d3\d3_2\a.wav'

if(-not (Test-Path -LiteralPath $D32ReceiptPath)){ throw "D3.2 receipt not found: $D32ReceiptPath" }
if(-not (Test-Path -LiteralPath $D32WavePath)){ throw "D3.2 reference WAV not found: $D32WavePath" }

$FfmpegCmd = Get-Command ffmpeg.exe -ErrorAction SilentlyContinue
if($null -eq $FfmpegCmd){ throw 'ffmpeg.exe not found in PATH. Install/use FFmpeg before D3.3.' }
$FfprobeCmd = Get-Command ffprobe.exe -ErrorAction SilentlyContinue
if($null -eq $FfprobeCmd){ throw 'ffprobe.exe not found in PATH. Install/use FFprobe before D3.3.' }

New-Item -ItemType Directory -Force -Path $ArtifactDir,$DocsDir,$HistoryDir | Out-Null

$QaPath = Join-Path $ArtifactDir 'd3_3_loudness_mobile_qa.json'
$ReceiptPath = Join-Path $ArtifactDir 'd3_3_validation_receipt.json'
$ContractPath = Join-Path $DocsDir 'D3.3_LOUDNESS_MOBILE_AUDIO_QA_CONTRACT.md'

$TempRoot = [System.IO.Path]::GetTempPath()
$TempDir = Join-Path $TempRoot ('d33_' + [Guid]::NewGuid().ToString('N').Substring(0,8))
$MonoPath = Join-Path $TempDir 'm.wav'
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

$Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)

function Write-JsonBytes([string]$Path,[object]$Value,[int]$Depth) {
    $JsonText = [string]($Value | ConvertTo-Json -Depth $Depth)
    $JsonBytes = [System.Text.Encoding]::UTF8.GetBytes($JsonText)
    [System.IO.File]::WriteAllBytes($Path,$JsonBytes)
}

function Parse-Number([string]$Text,[string]$Pattern) {
    $M = [regex]::Match($Text,$Pattern,[System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if($M.Success){ return [double]$M.Groups[1].Value }
    return $null
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

try {
    $ProbeRun = Invoke-NativeCapture {
        & ffprobe.exe -v error -show_streams -show_format -of json $D32WavePath
    }
    if($ProbeRun.ExitCode -ne 0){ throw 'ffprobe failed on D3.2 reference WAV.' }
    $ProbeRaw = $ProbeRun.Output
    $ProbeText = ($ProbeRaw | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
    $Probe = $ProbeText | ConvertFrom-Json

    $AudioStream = $null
    foreach($Item in $Probe.streams){
        if([string]$Item.codec_type -eq 'audio'){
            $AudioStream = $Item
            break
        }
    }
    if($null -eq $AudioStream){ throw 'No audio stream found in D3.2 reference WAV.' }

    $CodecName = [string]$AudioStream.codec_name
    $SampleRateHz = [int]$AudioStream.sample_rate
    $ChannelCount = [int]$AudioStream.channels
    $DurationSeconds = [double]$Probe.format.duration
    $ContainerPass = ($CodecName -eq 'pcm_s16le' -and $SampleRateHz -ge 44100 -and $ChannelCount -ge 1 -and $DurationSeconds -gt 0)

    # EBU R128. Parse only the explicit Integrated loudness and True peak lines.
    $EburRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -nostats -i $D32WavePath -filter_complex 'ebur128=peak=true' -f null NUL
    }
    if($EburRun.ExitCode -ne 0){ throw 'ffmpeg ebur128 failed on D3.2 reference WAV.' }
    $EburRaw = $EburRun.Output
    $EburText = ($EburRaw | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
    $IntegratedLufs = Parse-Number $EburText 'I:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*LUFS'
    $TruePeakDb = Parse-Number $EburText 'Peak:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dBFS'
    if($null -eq $IntegratedLufs){ throw 'Could not parse integrated loudness from FFmpeg ebur128.' }
    if($null -eq $TruePeakDb){ throw 'Could not parse true peak from FFmpeg ebur128.' }

    # Practical social/mobile envelope for this phase.
    $LoudnessPass = ($IntegratedLufs -ge -18.0 -and $IntegratedLufs -le -12.0)
    $TruePeakPass = ($TruePeakDb -le -1.0)

    $VolRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -nostats -i $D32WavePath -af volumedetect -f null NUL
    }
    if($VolRun.ExitCode -ne 0){ throw 'ffmpeg volumedetect failed on D3.2 reference WAV.' }
    $VolRaw = $VolRun.Output
    $VolText = ($VolRaw | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
    $MaxVolumeDb = Parse-Number $VolText 'max_volume:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dB'
    $ClipCount = Parse-Number $VolText 'histogram_0db:\s*([0-9]+)'
    if($null -eq $MaxVolumeDb){ throw 'Could not parse max_volume from FFmpeg volumedetect.' }
    $HardClipPass = ($MaxVolumeDb -lt 0.0)
    $HistogramPass = $true
    if($null -ne $ClipCount){ $HistogramPass = ([int64]$ClipCount -eq 0) }

    # Mono compatibility: actual downmix render + non-clipping validation.
    $MonoRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -loglevel error -y -i $D32WavePath -ac 1 -c:a pcm_s16le $MonoPath
    }
    if($MonoRun.ExitCode -ne 0 -or -not (Test-Path -LiteralPath $MonoPath)){ throw 'Mono downmix failed.' }

    $MonoVolRun = Invoke-NativeCapture {
        & ffmpeg.exe -hide_banner -nostats -i $MonoPath -af volumedetect -f null NUL
    }
    if($MonoVolRun.ExitCode -ne 0){ throw 'ffmpeg mono volumedetect failed.' }
    $MonoVolRaw = $MonoVolRun.Output
    $MonoVolText = ($MonoVolRaw | ForEach-Object { [string]$_ }) -join [Environment]::NewLine
    $MonoMaxVolumeDb = Parse-Number $MonoVolText 'max_volume:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dB'
    $MonoMeanVolumeDb = Parse-Number $MonoVolText 'mean_volume:\s*([-+]?[0-9]+(?:\.[0-9]+)?)\s*dB'
    if($null -eq $MonoMaxVolumeDb){ throw 'Could not parse mono max_volume.' }
    $MonoPass = ($MonoMaxVolumeDb -lt 0.0)
    $AudiblePass = $true
    if($null -ne $MonoMeanVolumeDb){ $AudiblePass = ($MonoMeanVolumeDb -lt -20.0) }

    # Mobile-safety gate: rate/class + no clipping + true peak + mono.
    $MobilePass = ($SampleRateHz -ge 44100 -and $HardClipPass -and $HistogramPass -and $TruePeakPass -and $MonoPass -and $AudiblePass)
    $OverallPass = ($ContainerPass -and $LoudnessPass -and $TruePeakPass -and $HardClipPass -and $HistogramPass -and $MonoPass -and $MobilePass)

    $QaObject = [ordered]@{
        checkpoint = 'C11-D D3.3'
        result = $(if($OverallPass){'PASS'}else{'FAIL'})
        status = $(if($OverallPass){'CLOSED'}else{'BLOCKED'})
        reference = 'D3.2 deterministic render A'
        container = [ordered]@{
            codec = $CodecName
            sample_rate_hz = $SampleRateHz
            channels = $ChannelCount
            duration_seconds = $DurationSeconds
            pass = $ContainerPass
        }
        loudness = [ordered]@{
            integrated_lufs = $IntegratedLufs
            minimum_lufs = -18.0
            maximum_lufs = -12.0
            pass = $LoudnessPass
        }
        true_peak = [ordered]@{
            measured_dbfs = $TruePeakDb
            maximum_dbfs = -1.0
            pass = $TruePeakPass
        }
        clipping = [ordered]@{
            max_volume_db = $MaxVolumeDb
            histogram_0db_samples = $ClipCount
            hard_clip_pass = $HardClipPass
            histogram_pass = $HistogramPass
        }
        mono_compatibility = [ordered]@{
            downmix_rendered = $true
            max_volume_db = $MonoMaxVolumeDb
            mean_volume_db = $MonoMeanVolumeDb
            pass = $MonoPass
            audible_pass = $AudiblePass
        }
        mobile_safety = [ordered]@{
            pass = $MobilePass
            sample_rate_class_pass = ($SampleRateHz -ge 44100)
            clipping_safe = ($HardClipPass -and $HistogramPass)
            true_peak_safe = $TruePeakPass
            mono_safe = $MonoPass
            policy = 'platform-agnostic mobile-safe QA envelope'
        }
        engine_id = 'c11d_music_engine_v5'
        style_profile_id = 'challenge_8bit_v1'
        runtime_activation = $false
        simulation_truth_mutation = $false
        d3_closure_ready = $OverallPass
        next = $(if($OverallPass){'D4'}else{'D3.3_REPAIR'})
        generated_at_utc = [DateTime]::UtcNow.ToString('o')
    }

    Write-JsonBytes $QaPath $QaObject 16

    $ReceiptObject = [ordered]@{
        checkpoint = 'C11-D D3.3'
        result = $(if($OverallPass){'PASS'}else{'FAIL'})
        status = $(if($OverallPass){'CLOSED'}else{'BLOCKED'})
        objective = 'Loudness / Mobile Audio QA'
        qa_artifact = $QaPath
        d3_2_receipt = $D32ReceiptPath
        runtime_activation = $false
        protected_domains = @('simulation truth','winning_frame','close_calls','structural/gameplay RNG','C11-C Visual Loops','C11-C Visual Drills')
        d3_status = $(if($OverallPass){'CLOSED'}else{'ACTIVE'})
        next = $(if($OverallPass){'D4'}else{'D3.3_REPAIR'})
        generated_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    Write-JsonBytes $ReceiptPath $ReceiptObject 16

    if(-not $OverallPass){ throw 'D3.3 QA failed. Inspect d3_3_loudness_mobile_qa.json.' }

    $ContractLines = @(
        '# C11-D D3.3 - Loudness / Mobile Audio QA',
        '',
        '## Status',
        '',
        'PASS / CLOSED.',
        '',
        '## Gate',
        '',
        'The D3.2 deterministic Challenge 8-bit render passed container integrity, integrated loudness, true peak, clipping safety, mono downmix and mobile-safe envelope checks.',
        '',
        '## QA envelope',
        '',
        '- integrated loudness: -18 to -12 LUFS;',
        '- true peak: no higher than -1 dBFS in the FFmpeg peak measurement;',
        '- no hard sample clipping;',
        '- mono downmix remains valid and non-clipping;',
        '- sample rate is 44.1 kHz or higher.',
        '',
        'This is a platform-agnostic generated-audio QA envelope, not a claim that every mobile device has identical acoustic response.',
        '',
        '## FFmpeg / PowerShell 5.1 handling',
        '',
        'Native FFmpeg and FFprobe output on stderr is captured without treating informational diagnostics as terminating PowerShell errors. Native success is determined from `$LASTEXITCODE` inside the capture wrapper.',
        '',
        '## D3 closure',
        '',
        'D3.0 design PASS, D3.1 specification PASS, D3.2 deterministic implementation PASS, and D3.3 loudness/mobile QA PASS.',
        '',
        'D3 = CLOSED.',
        '',
        '## Evidence',
        '',
        '- `artifacts/tests/c11d_d3/d3_3/d3_3_loudness_mobile_qa.json`',
        '- `artifacts/tests/c11d_d3/d3_3/d3_3_validation_receipt.json`',
        '',
        '## Next',
        '',
        'D4 - Declarative Production Request + Personalization + GUI/CLI Parity.'
    )
    [System.IO.File]::WriteAllText($ContractPath,($ContractLines -join [Environment]::NewLine),$Utf8NoBom)

    $MasterPath = Join-Path $ProjectRoot 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'
    $StartPath = Join-Path $ProjectRoot 'docs\current\d\START_PROMPT_C11D_CURRENT.md'
    $Marker = '<!-- C11D_D3_CLOSED_V1 -->'
    $HandoffLines = @(
        $Marker,
        '',
        '## C11-D D3 CLOSED',
        '',
        '- D3.0 design contract: PASS.',
        '- D3.1 shared Music Engine V5 specification: PASS / SPECIFIED.',
        '- D3.2 deterministic implementation/render comparison: PASS / CLOSED.',
        '- D3.3 loudness/mobile audio QA: PASS / CLOSED.',
        '- Native FFmpeg/FFprobe stderr is captured safely for PowerShell 5.1 without false failures.',
        '- Shared engine: `c11d_music_engine_v5` version 5.0.',
        '- Challenge style profile: `challenge_8bit_v1`.',
        '- Same music seed is deterministic; different music seed changes output.',
        '- Loudness, true peak, clipping and mono compatibility validated.',
        '- No simulation truth, `winning_frame`, `close_calls`, gameplay RNG or structural RNG changes.',
        '- Visual Loop and Visual Drill C11-C paths remain protected.',
        '- D3 = CLOSED.',
        '- Next active checkpoint: **D4 - Declarative Production Request + Personalization + GUI/CLI Parity**.',
        ''
    )

    function Add-Handoff([string]$Path,[string[]]$Lines){
        if(-not (Test-Path -LiteralPath $Path)){ return }
        $Existing = [System.IO.File]::ReadAllText($Path)
        if($Existing.Contains($Marker)){ return }
        $Updated = $Existing.TrimEnd() + [Environment]::NewLine + [Environment]::NewLine + ($Lines -join [Environment]::NewLine) + [Environment]::NewLine
        [System.IO.File]::WriteAllText($Path,$Updated,$Utf8NoBom)
    }

    Add-Handoff $MasterPath $HandoffLines
    Add-Handoff $StartPath $HandoffLines

    $Stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd_HHmmss')
    if(Test-Path -LiteralPath $MasterPath){ Copy-Item -LiteralPath $MasterPath -Destination (Join-Path $HistoryDir ('MASTER_HANDOVER_C11D_D3_CLOSED_{0}.md' -f $Stamp)) -Force }
    if(Test-Path -LiteralPath $StartPath){ Copy-Item -LiteralPath $StartPath -Destination (Join-Path $HistoryDir ('START_PROMPT_C11D_D3_CLOSED_{0}.md' -f $Stamp)) -Force }

    Write-Host ''
    Write-Host '=================================================='
    Write-Host ' C11-D D3.3 - PASS / CLOSED'
    Write-Host '=================================================='
    Write-Host ('[OK] Integrated loudness: {0:N2} LUFS.' -f $IntegratedLufs)
    Write-Host ('[OK] True peak: {0:N2} dBFS.' -f $TruePeakDb)
    Write-Host ('[OK] Max sample volume: {0:N2} dB.' -f $MaxVolumeDb)
    Write-Host '[OK] No hard clipping.'
    Write-Host '[OK] Mono downmix compatibility passed.'
    Write-Host '[OK] Mobile-safe QA envelope passed.'
    Write-Host '[OK] D3 = CLOSED.'
    Write-Host 'NEXT: D4 - Declarative Production Request + Personalization + GUI/CLI Parity'
}
finally {
    if(Test-Path -LiteralPath $TempDir){ Remove-Item -LiteralPath $TempDir -Recurse -Force -ErrorAction SilentlyContinue }
}

Write-Host ''
Write-Host 'C11-D D3.3 patch applied successfully.'
Write-Host ('QA:      {0}' -f $QaPath)
Write-Host ('RECEIPT: {0}' -f $ReceiptPath)
Write-Host ('CONTRACT:{0}' -f $ContractPath)
