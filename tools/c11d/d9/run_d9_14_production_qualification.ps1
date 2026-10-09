[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('RUN_C11D_PRODUCTION_QUALIFICATION_NO_RELEASE')]
    [string]$ConfirmProductionQualification,
    [ValidateRange(1,2147483646)][int]$ChallengeSeed = 42001,
    [ValidateRange(1,2147483646)][int]$GameplaySeed = 42002,
    [ValidateRange(1,2147483646)][int]$DrillSeed = 42003,
    [ValidateRange(1,2147483646)][int]$ChallengeMusicSeed = 73020,
    [ValidateRange(1,2147483646)][int]$MusicSeedA = 73021,
    [ValidateRange(1,2147483646)][int]$MusicSeedB = 73022,
    [string]$RunId = ''
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$Python = Get-Command python -ErrorAction Stop
$FFmpeg = Get-Command ffmpeg -ErrorAction Stop
$FFprobe = Get-Command ffprobe -ErrorAction Stop
$Godot = Get-Command godot.exe -ErrorAction SilentlyContinue
if (-not $Godot) { $Godot = Get-Command godot -ErrorAction SilentlyContinue }
if (-not $Godot) { throw 'No se encontró Godot en PATH. La cualificación requiere ejecución real del renderizador existente.' }
if ($ChallengeMusicSeed -eq $MusicSeedA -or $ChallengeMusicSeed -eq $MusicSeedB -or $MusicSeedA -eq $MusicSeedB) { throw 'ChallengeMusicSeed, MusicSeedA y MusicSeedB deben ser distintos para conservar el aislamiento de audio.' }
if ([string]::IsNullOrWhiteSpace($RunId)) { $RunId = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') }
if ($RunId -notmatch '^[A-Za-z0-9_-]{8,40}$') { throw 'RunId debe tener entre 8 y 40 caracteres alfanuméricos, guion o guion bajo.' }

$RunRoot = Join-Path $ProjectRoot (Join-Path 'artifacts\production\c11d_qualification' $RunId)
if (Test-Path -LiteralPath $RunRoot) { throw "La ejecución ya existe y no se sobrescribe: $RunRoot" }
$ChallengeRoot = Join-Path $RunRoot 'challenge'
$LoopARoot = Join-Path $RunRoot 'loop_replay_a'
$LoopBRoot = Join-Path $RunRoot 'loop_replay_b'
$DrillRoot = Join-Path $RunRoot 'drill'
$MediaRoot = Join-Path $RunRoot 'media'
New-Item -ItemType Directory -Force -Path $RunRoot,$MediaRoot | Out-Null

$Authorization = Join-Path $ProjectRoot 'definitions\c11d\production\D9_14_PRODUCTION_QUALIFICATION_AUTHORIZATION_V1.json'
$Contract = Join-Path $ProjectRoot 'tools\c11d\d9\production_qualification_contract.py'
$CandidateAudit = Join-Path $ProjectRoot 'tools\c11d\baseline_candidate\test_d_baseline_candidate.py'
$ChallengeRunner = Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1'
$LoopRunner = Join-Path $ProjectRoot 'tools\prototypes\c11c_geometric_waves_v1\run_prototype.ps1'
$DrillRunner = Join-Path $ProjectRoot 'c11c-suite\c11c-producer\run_visual_drill_production.ps1'
$AmbientScript = Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CSafeAmbient.py'
$MusicEngine = Join-Path $ProjectRoot 'tools\c11d\d3\c11d_music_engine_v5.py'
$MusicEngineSpec = Join-Path $ProjectRoot 'definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json'
$ChallengeMusicProfile = Join-Path $ProjectRoot 'definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json'
$CManifest = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$ExpectedCManifest = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$StartedUtc = (Get-Date).ToUniversalTime().ToString('o')

function Get-FileSha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Invoke-QualificationScript {
    param([string]$ScriptPath,[hashtable]$Arguments,[string]$LogPath,[string]$ExpectedMarker)
    $argSummary = ($Arguments.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join ' '
    Write-Host "[C11-D-QUALIFICATION] Ejecutando: $ScriptPath $argSummary"
    $lines = & $ScriptPath @Arguments *>&1
    $text = ($lines | Out-String)
    [IO.File]::WriteAllText($LogPath,$text,$Utf8NoBom)
    Write-Host $text
    if ($text -notmatch [regex]::Escape($ExpectedMarker)) {
        throw "El launcher no confirmó su PASS contractual: $ScriptPath. Consulte $LogPath"
    }
}
function Get-SourceTreeHash {
    param([string]$LogPath)
    $lines = & python $CandidateAudit 2>&1
    $exitCode = $LASTEXITCODE
    $text = ($lines | Out-String)
    [IO.File]::WriteAllText($LogPath,$text,$Utf8NoBom)
    if ($exitCode -ne 0) { throw "Preflight del árbol falló (exit=$exitCode). Consulte $LogPath" }
    $match = [regex]::Match($text,'tree_sha256=([0-9a-f]{64})')
    if (-not $match.Success) { throw "No se pudo leer tree_sha256 de la auditoría: $LogPath" }
    return $match.Groups[1].Value
}
function Get-AudioMaxVolumeDb {
    param([string]$Path)
    # FFmpeg's volumedetect emits successful analysis messages (including Input #0 and
    # max_volume) on stderr at info level. Windows PowerShell 5.1 can promote redirected
    # native stderr records to terminating errors under the script-wide Stop preference.
    # Relax the preference only within this capture scope, then restore it unconditionally;
    # the native exit code and required max_volume statistic remain mandatory.
    $previousPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'Continue'
        $raw = & ffmpeg -hide_banner -nostats -v info -i $Path -map 0:a:0 -af volumedetect -f null - 2>&1
        $exitCode = $LASTEXITCODE
        $text = (($raw | ForEach-Object { [string]$_ }) -join "`n")
    }
    finally {
        $ErrorActionPreference = $previousPreference
    }
    if ($exitCode -ne 0) { throw "FFmpeg audio loudness audit failed for $Path : $text" }
    $match = [regex]::Match($text,'max_volume:\s*(-inf|-?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+))\s*dB',[System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if (-not $match.Success) { throw "FFmpeg did not report max_volume for $Path" }
    if ($match.Groups[1].Value -eq '-inf') { throw "Audio is silent (max_volume=-inf dB): $Path" }
    $value = [double]::Parse($match.Groups[1].Value,[Globalization.CultureInfo]::InvariantCulture)
    if ($value -le -90.0) { throw "Audio is silent/inaudible by qualification threshold (max_volume=$value dB): $Path" }
    return $value
}
function Invoke-ChallengeMusicEngineV5 {
    param([string]$OutputPath,[string]$ReceiptPath,[int]$Seed,[double]$Duration)
    $durationArg = $Duration.ToString([Globalization.CultureInfo]::InvariantCulture)
    $musicArgs = @($MusicEngine,'--engine',$MusicEngineSpec,'--profile',$ChallengeMusicProfile,'--output',$OutputPath,'--seed',[string]$Seed,'--tempo','104','--duration',$durationArg,'--variation','0')
    $raw = & python @musicArgs 2>&1
    if ($LASTEXITCODE -ne 0) { throw "C11-D Music Engine V5 failed for Challenge seed=${Seed}: $(($raw | Out-String))" }
    $line = @($raw | ForEach-Object { [string]$_ } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Last 1)
    if ($line.Count -ne 1) { throw 'C11-D Music Engine V5 returned no JSON receipt for Challenge.' }
    try { $receipt = $line[0] | ConvertFrom-Json } catch { throw 'C11-D Music Engine V5 returned invalid JSON receipt for Challenge.' }
    if ([string]$receipt.engine_id -ne 'c11d_music_engine_v5' -or [string]$receipt.engine_version -ne '5.0') { throw 'Challenge music engine identity/version mismatch.' }
    if ([string]$receipt.style_profile_id -ne 'challenge_8bit_v1' -or [int]$receipt.music_seed -ne $Seed) { throw 'Challenge music style/seed receipt mismatch.' }
    if ([math]::Abs([double]$receipt.duration_seconds - $Duration) -gt 0.01) { throw 'Challenge music duration mismatch.' }
    if ([double]$receipt.peak_linear -le 0 -or [double]$receipt.rms_linear -le 0) { throw 'Challenge music engine output is silent.' }
    if (-not (Test-Path -LiteralPath $OutputPath -PathType Leaf) -or (Get-Item -LiteralPath $OutputPath).Length -le 4096) { throw 'Challenge music WAV is missing or implausibly small.' }
    $actualHash = Get-FileSha256 $OutputPath
    if ([string]$receipt.output_hash -ne $actualHash) { throw 'Challenge music receipt output hash mismatch.' }
    [IO.File]::WriteAllText($ReceiptPath,($receipt | ConvertTo-Json -Depth 12),$Utf8NoBom)
    return $receipt
}
function Get-Probe {
    param([string]$Path)
    $raw = & ffprobe -v error -count_frames -show_streams -show_format -of json -- $Path 2>&1
    if ($LASTEXITCODE -ne 0) { throw "ffprobe falló para $Path : $($raw -join "`n")" }
    $probe = (($raw | Out-String) | ConvertFrom-Json)
    $video = @($probe.streams | Where-Object { $_.codec_type -eq 'video' }) | Select-Object -First 1
    $audio = @($probe.streams | Where-Object { $_.codec_type -eq 'audio' }) | Select-Object -First 1
    if (-not $video) { throw "No hay stream de vídeo: $Path" }
    if ([int]$video.width -ne 720 -or [int]$video.height -ne 1280) { throw "Resolución inesperada en $Path : $($video.width)x$($video.height)" }
    if ([string]$video.codec_name -ne 'h264') { throw "Codec de vídeo inesperado en $Path : $($video.codec_name)" }
    if ([string]$video.pix_fmt -notin @('yuv420p','yuvj420p')) { throw "Formato de píxel no social en $Path : $($video.pix_fmt)" }
    if ([int]$video.nb_read_frames -le 1) { throw "No se pudieron validar frames en $Path" }
    $rate = [regex]::Match([string]$video.r_frame_rate,'^(\d+)/(\d+)$')
    if (-not $rate.Success) { throw "FPS no interpretable en $Path : $($video.r_frame_rate)" }
    $fps = [double]$rate.Groups[1].Value / [double]$rate.Groups[2].Value
    if ($fps -lt 24 -or $fps -gt 60) { throw "FPS fuera de 24..60 en $Path : $fps" }
    $duration = [double]$probe.format.duration
    if ($duration -lt 3.0) { throw "Duración final inválida en $Path : $duration" }
    if (-not $audio) { throw "El vídeo final debe llevar audio: $Path" }
    if ([int]$audio.channels -ne 2) { throw "Se esperaba audio estéreo en $Path" }
    if ($null -ne $video.duration -and $null -ne $audio.duration -and [math]::Abs([double]$video.duration-[double]$audio.duration) -gt 0.20) { throw "Desfase de duración A/V superior a 200 ms: $Path" }
    $maxVolumeDb = Get-AudioMaxVolumeDb $Path
    return [ordered]@{width=[int]$video.width;height=[int]$video.height;fps=$fps;frames=[int]$video.nb_read_frames;duration_seconds=$duration;video_codec=[string]$video.codec_name;pixel_format=[string]$video.pix_fmt;audio_codec=[string]$audio.codec_name;audio_sample_rate=[int]$audio.sample_rate;audio_channels=[int]$audio.channels;audio_max_volume_db=$maxVolumeDb}
}
function Get-FrameDigests {
    param([string]$VideoPath,[string]$DigestPath)
    & ffmpeg -y -v error -i $VideoPath -map 0:v:0 -f framemd5 $DigestPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $DigestPath)) { throw "No se pudo generar frame digest: $VideoPath" }
    $values = @()
    foreach ($line in Get-Content -LiteralPath $DigestPath) {
        if ($line -match '^\s*[^#].*,\s*([0-9a-f]{32})\s*$') { $values += $Matches[1] }
    }
    if ($values.Count -le 1) { throw "Frame digest vacío: $DigestPath" }
    return ,$values
}
function Get-AudioPcmDigest {
    param([string]$VideoPath,[string]$PcmPath)
    & ffmpeg -y -v error -i $VideoPath -map 0:a:0 -vn -acodec pcm_s16le -ar 44100 -ac 2 -f s16le $PcmPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $PcmPath)) { throw "No se pudo decodificar audio final: $VideoPath" }
    if ((Get-Item -LiteralPath $PcmPath).Length -le 4096) { throw "Audio PCM final inesperadamente pequeño: $PcmPath" }
    return Get-FileSha256 $PcmPath
}
function Invoke-AudioGenerator {
    param([string]$OutputPath,[int]$Seed,[int]$Cycles,[double]$Duration,[string]$Family,[string]$Kind,[string]$Grammar='')
    $durationArg = $Duration.ToString([Globalization.CultureInfo]::InvariantCulture)
    $audioArgs = @($AmbientScript,$OutputPath,[string]$Seed,[string]$Cycles,$durationArg,$Family,$Kind)
    if (-not [string]::IsNullOrWhiteSpace($Grammar)) { $audioArgs += $Grammar }
    & python @audioArgs
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $OutputPath)) { throw "Generador de música falló para seed=$Seed" }
    if ((Get-Item -LiteralPath $OutputPath).Length -le 4096) { throw "WAV inesperadamente pequeño: $OutputPath" }
}
function Invoke-Mux {
    param([string]$SilentVideo,[string]$AudioWav,[string]$OutputPath)
    & ffmpeg -y -hide_banner -loglevel error -i $SilentVideo -i $AudioWav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 -shortest -movflags +faststart $OutputPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $OutputPath)) { throw "Mux A/V falló: $OutputPath" }
}

try {
    if (-not (Test-Path -LiteralPath $Authorization -PathType Leaf)) { throw 'Falta la autorización acotada D9.14.' }
    & python $Contract authorize-check --project-root $ProjectRoot --token $ConfirmProductionQualification
    if ($LASTEXITCODE -ne 0) { throw 'El contrato no autoriza esta ejecución acotada.' }
    if ((Get-FileSha256 $CManifest) -ne $ExpectedCManifest) { throw 'El manifest congelado C11-C no coincide. Se aborta sin render.' }
    foreach ($required in @($ChallengeRunner,$LoopRunner,$DrillRunner,$AmbientScript,$MusicEngine,$MusicEngineSpec,$ChallengeMusicProfile,$CandidateAudit)) {
        if (-not (Test-Path -LiteralPath $required -PathType Leaf)) { throw "Falta dependencia requerida: $required" }
    }
    $sourceBefore = Get-SourceTreeHash (Join-Path $RunRoot 'source_tree_preflight_before.txt')
    $GodotVersionLines = & $Godot.Source --version 2>&1
    $GodotVersion = (($GodotVersionLines | Select-Object -First 1) | Out-String).Trim()
    $FFmpegVersionLines = & ffmpeg -version 2>&1
    $FFmpegVersion = (($FFmpegVersionLines | Select-Object -First 1) | Out-String).Trim()
    $FFprobeVersionLines = & ffprobe -version 2>&1
    $FFprobeVersion = (($FFprobeVersionLines | Select-Object -First 1) | Out-String).Trim()
    $PythonVersion = (& python --version 2>&1 | Out-String).Trim()

    # 1) Render the existing frozen Challenge visual as video-only, then use the canonical D3 Music Engine V5
    # (the already-qualified D9.2 A/V path) to create a final audiovisual MP4 without mutating C11-C.
    Invoke-QualificationScript -ScriptPath $ChallengeRunner -Arguments @{ChallengeId='CHALLENGE_001';Seed=$ChallengeSeed;DeliveryProfile='REVIEW_720';NoSound=$true;OutputRoot=$ChallengeRoot} -LogPath (Join-Path $RunRoot 'challenge_launcher.log') -ExpectedMarker '[CHALLENGE] PASS'
    $challengeMp4 = Join-Path $ChallengeRoot (Join-Path 'CHALLENGE_001' "CHALLENGE_001_seed_${ChallengeSeed}.mp4")
    $challengeManifestPath = Join-Path $ChallengeRoot (Join-Path 'CHALLENGE_001' 'production_manifest.json')
    if (-not (Test-Path -LiteralPath $challengeMp4 -PathType Leaf) -or -not (Test-Path -LiteralPath $challengeManifestPath -PathType Leaf)) { throw "Challenge MP4/production manifest ausente: $challengeMp4" }
    $challengeManifest = Get-Content -Raw -LiteralPath $challengeManifestPath | ConvertFrom-Json
    $challengeDuration = [double]$challengeManifest.duration_seconds
    if ($challengeDuration -lt 3 -or $challengeManifest.audio_present -ne $false) { throw 'Challenge source must be a valid video-only capture before the governed audio mux.' }
    $challengeWav = Join-Path $MediaRoot "challenge_music_seed_${ChallengeMusicSeed}.wav"
    $challengeMusicReceiptPath = Join-Path $RunRoot 'challenge_music_engine_v5_receipt.json'
    $challengeMusicReceipt = Invoke-ChallengeMusicEngineV5 -OutputPath $challengeWav -ReceiptPath $challengeMusicReceiptPath -Seed $ChallengeMusicSeed -Duration $challengeDuration
    $challengeFinal = Join-Path $MediaRoot "challenge_seed_${ChallengeSeed}_music_${ChallengeMusicSeed}.mp4"
    Invoke-Mux -SilentVideo $challengeMp4 -AudioWav $challengeWav -OutputPath $challengeFinal
    [IO.File]::WriteAllText((Join-Path $RunRoot 'challenge_audio_mux.log'),"engine=c11d_music_engine_v5`nseed=$ChallengeMusicSeed`nsource_video=$challengeMp4`nsource_wav=$challengeWav`nfinal_mp4=$challengeFinal`n",$Utf8NoBom)

    # 2) Two genuine, silent loop renders with identical gameplay seed; music is generated separately.
    Invoke-QualificationScript -ScriptPath $LoopRunner -Arguments @{Seed=$GameplaySeed;Grammar='harmonic_membrane';NoSound=$true;OutputRoot=$LoopARoot;OutputTag='replay_a'} -LogPath (Join-Path $RunRoot 'loop_replay_a_launcher.log') -ExpectedMarker '[C11-C-2.16.3] PASS'
    Invoke-QualificationScript -ScriptPath $LoopRunner -Arguments @{Seed=$GameplaySeed;Grammar='harmonic_membrane';NoSound=$true;OutputRoot=$LoopBRoot;OutputTag='replay_b'} -LogPath (Join-Path $RunRoot 'loop_replay_b_launcher.log') -ExpectedMarker '[C11-C-2.16.3] PASS'
    $loopSilentA = Join-Path $LoopARoot "GeometricWaves_v1_seed_${GameplaySeed}_replay_a.mp4"
    $loopSilentB = Join-Path $LoopBRoot "GeometricWaves_v1_seed_${GameplaySeed}_replay_b.mp4"
    $loopManifestA = Join-Path $LoopARoot "GeometricWaves_v1_seed_${GameplaySeed}_replay_a_authoring.json"
    if (-not (Test-Path -LiteralPath $loopSilentA) -or -not (Test-Path -LiteralPath $loopSilentB) -or -not (Test-Path -LiteralPath $loopManifestA)) { throw 'Salida loop/replay o authoring ausente.' }
    $loopAuthor = Get-Content -Raw -LiteralPath $loopManifestA | ConvertFrom-Json
    $loopCycles = [int][math]::Round([double]$loopAuthor.loop_cycles)
    $loopDuration = [double]$loopAuthor.duration_seconds
    if ($loopCycles -le 0 -or $loopDuration -lt 3) { throw 'Metadata loop inválida para generar música independiente.' }
    $loopWavA = Join-Path $MediaRoot "loop_music_seed_${MusicSeedA}.wav"
    $loopWavB = Join-Path $MediaRoot "loop_music_seed_${MusicSeedB}.wav"
    Invoke-AudioGenerator -OutputPath $loopWavA -Seed $MusicSeedA -Cycles $loopCycles -Duration $loopDuration -Family 'geometric' -Kind 'loop' -Grammar 'harmonic_membrane'
    Invoke-AudioGenerator -OutputPath $loopWavB -Seed $MusicSeedB -Cycles $loopCycles -Duration $loopDuration -Family 'geometric' -Kind 'loop' -Grammar 'harmonic_membrane'
    $loopFinalA = Join-Path $MediaRoot "visual_loop_gameplay_${GameplaySeed}_music_${MusicSeedA}.mp4"
    $loopFinalB = Join-Path $MediaRoot "visual_loop_gameplay_${GameplaySeed}_music_${MusicSeedB}.mp4"
    Invoke-Mux -SilentVideo $loopSilentA -AudioWav $loopWavA -OutputPath $loopFinalA
    Invoke-Mux -SilentVideo $loopSilentB -AudioWav $loopWavB -OutputPath $loopFinalB
    $framesA = Get-FrameDigests -VideoPath $loopSilentA -DigestPath (Join-Path $RunRoot 'loop_frames_replay_a.framemd5')
    $framesB = Get-FrameDigests -VideoPath $loopSilentB -DigestPath (Join-Path $RunRoot 'loop_frames_replay_b.framemd5')
    if ($framesA.Count -ne $framesB.Count -or (($framesA -join ',') -ne ($framesB -join ','))) { throw 'Same-seed loop replay produced different decoded video frames.' }
    if ((Get-FileSha256 $loopWavA) -eq (Get-FileSha256 $loopWavB)) { throw 'Different music seeds produced identical WAV bytes; seed isolation test failed.' }
    $frameSequencePathA = Join-Path $RunRoot 'loop_frame_sequence_a.txt'
    $frameSequencePathB = Join-Path $RunRoot 'loop_frame_sequence_b.txt'
    $framesTextA = $framesA -join "`n"
    $framesTextB = $framesB -join "`n"
    [IO.File]::WriteAllText($frameSequencePathA,$framesTextA,$Utf8NoBom)
    [IO.File]::WriteAllText($frameSequencePathB,$framesTextB,$Utf8NoBom)

    # 3) Real Visual Drill production capture with music seeded independently from gameplay.
    Invoke-QualificationScript -ScriptPath $DrillRunner -Arguments @{Family='tracking';Seed=$DrillSeed;DifficultyTier=1;SpeedMultiplier=1.0;PacingMode='constant';DeliveryProfile='REVIEW_720';NoSound=$true;OutputRoot=$DrillRoot} -LogPath (Join-Path $RunRoot 'drill_launcher.log') -ExpectedMarker '[C11-C-PRODUCER-DRILL] FINAL PRODUCT PASS'
    $drillManifestItem = Get-ChildItem -LiteralPath $DrillRoot -Filter 'production_manifest.json' -File -Recurse | Select-Object -First 1
    $drillSilentItem = Get-ChildItem -LiteralPath $DrillRoot -Filter '*.mp4' -File -Recurse | Select-Object -First 1
    if (-not $drillManifestItem -or -not $drillSilentItem) { throw 'Salida/manifest de Visual Drill ausente.' }
    $drillManifest = Get-Content -Raw -LiteralPath $drillManifestItem.FullName | ConvertFrom-Json
    $drillDuration = [double]$drillManifest.total_duration_seconds
    if ($drillDuration -lt 3) { throw 'Duración de Visual Drill inválida.' }
    $drillWav = Join-Path $MediaRoot "drill_music_seed_${MusicSeedA}.wav"
    Invoke-AudioGenerator -OutputPath $drillWav -Seed $MusicSeedA -Cycles 1 -Duration $drillDuration -Family 'tracking' -Kind 'drill'
    $drillFinal = Join-Path $MediaRoot "visual_drill_tracking_gameplay_${DrillSeed}_music_${MusicSeedA}.mp4"
    Invoke-Mux -SilentVideo $drillSilentItem.FullName -AudioWav $drillWav -OutputPath $drillFinal
    $loopPcmA = Join-Path $RunRoot 'loop_final_audio_a.pcm'
    $loopPcmB = Join-Path $RunRoot 'loop_final_audio_b.pcm'
    $loopPcmHashA = Get-AudioPcmDigest -VideoPath $loopFinalA -PcmPath $loopPcmA
    $loopPcmHashB = Get-AudioPcmDigest -VideoPath $loopFinalB -PcmPath $loopPcmB
    if ($loopPcmHashA -eq $loopPcmHashB) { throw 'MP4 final audio decoded identically despite different music seeds.' }

    # 4) Probe every final asset and create deterministic, hash-bound run evidence.
    $mediaOutputs = @()
    foreach ($entry in @(
        @{kind='challenge';path=$challengeFinal},
        @{kind='visual_loop_music_seed_A';path=$loopFinalA},
        @{kind='visual_loop_music_seed_B';path=$loopFinalB},
        @{kind='visual_drill';path=$drillFinal}
    )) {
        $probe = Get-Probe ([string]$entry.path)
        $mediaOutputs += [ordered]@{kind=$entry.kind;path=[IO.Path]::GetFullPath([string]$entry.path);sha256=(Get-FileSha256 ([string]$entry.path));bytes=(Get-Item -LiteralPath ([string]$entry.path)).Length;probe=$probe}
    }
    $probeAudioCount = @($mediaOutputs | Where-Object { $_.probe.audio_channels -eq 2 }).Count
    if ($probeAudioCount -ne 4) { throw 'No todos los MP4 finales tienen audio estéreo.' }
    $sourceAfter = Get-SourceTreeHash (Join-Path $RunRoot 'source_tree_preflight_after.txt')
    if ($sourceBefore -ne $sourceAfter) { throw "El código/configuración del árbol cambió durante el render. before=$sourceBefore after=$sourceAfter" }
    if ((Get-FileSha256 $CManifest) -ne $ExpectedCManifest) { throw 'El manifest congelado C11-C cambió durante la cualificación.' }

    $report = [ordered]@{
        schema='C11-D-D9.14-PRODUCTION-QUALIFICATION-REPORT-V1'
        schema_version='1.0'
        run_id=$RunId
        started_utc=$StartedUtc
        completed_utc=(Get-Date).ToUniversalTime().ToString('o')
        status='BOUNDED_PRODUCTION_QUALIFICATION_PASS_NOT_D9_14_CLOSURE'
        authorization_checkpoint='definitions/c11d/production/D9_14_PRODUCTION_QUALIFICATION_AUTHORIZATION_V1.json'
        authorization_checkpoint_sha256=(Get-FileSha256 $Authorization)
        scope='EXISTING_C11C_PRODUCTION_GENERATORS_BOUNDED_QUALIFICATION'
        source_tree_sha256_before=$sourceBefore
        source_tree_sha256_after=$sourceAfter
        c11c_manifest_sha256=(Get-FileSha256 $CManifest)
        tools=[ordered]@{godot=$GodotVersion;ffmpeg=$FFmpegVersion;ffprobe=$FFprobeVersion;python_version=$PythonVersion}
        seeds=[ordered]@{challenge_gameplay=$ChallengeSeed;challenge_music=$ChallengeMusicSeed;loop_gameplay=$GameplaySeed;drill_gameplay=$DrillSeed;music_a=$MusicSeedA;music_b=$MusicSeedB}
        checks=[ordered]@{
            challenge_video='PASS'
            challenge_audio_mux='PASS'
            visual_loop_video='PASS'
            visual_drill_video='PASS'
            same_seed_loop_video_replay='PASS'
            music_seed_changes_audio_identity='PASS'
            a_v_streams_and_duration='PASS'
            protected_source_unchanged='PASS'
            c11d_editorial_renderer_binding='NOT_CERTIFIED_BY_THIS_RUN'
            c11d_gui_lifecycle='NOT_RUN_BY_THIS_RUNNER'
        }
        media_outputs=$mediaOutputs
        challenge_audio_evidence=[ordered]@{engine_id=[string]$challengeMusicReceipt.engine_id;engine_version=[string]$challengeMusicReceipt.engine_version;style_profile_id=[string]$challengeMusicReceipt.style_profile_id;seed=$ChallengeMusicSeed;duration_seconds=[double]$challengeMusicReceipt.duration_seconds;peak_linear=[double]$challengeMusicReceipt.peak_linear;rms_linear=[double]$challengeMusicReceipt.rms_linear;source_wav_path=[IO.Path]::GetFullPath($challengeWav);source_wav_sha256=(Get-FileSha256 $challengeWav);engine_receipt_path=[IO.Path]::GetFullPath($challengeMusicReceiptPath);engine_receipt_sha256=(Get-FileSha256 $challengeMusicReceiptPath);final_media_path=[IO.Path]::GetFullPath($challengeFinal);final_media_sha256=(Get-FileSha256 $challengeFinal)}
        determinism_evidence=[ordered]@{
            loop_frame_count=$framesA.Count
            loop_frame_sequence_sha256_a=(Get-FileSha256 $frameSequencePathA)
            loop_frame_sequence_sha256_b=(Get-FileSha256 $frameSequencePathB)
            loop_frame_sequences=@(
                [ordered]@{path=[IO.Path]::GetFullPath($frameSequencePathA);sha256=(Get-FileSha256 $frameSequencePathA)},
                [ordered]@{path=[IO.Path]::GetFullPath($frameSequencePathB);sha256=(Get-FileSha256 $frameSequencePathB)}
            )
            music_seed_audio=@(
                [ordered]@{seed=$MusicSeedA;source_wav_path=[IO.Path]::GetFullPath($loopWavA);source_wav_sha256=(Get-FileSha256 $loopWavA);decoded_pcm_path=[IO.Path]::GetFullPath($loopPcmA);decoded_pcm_sha256=$loopPcmHashA},
                [ordered]@{seed=$MusicSeedB;source_wav_path=[IO.Path]::GetFullPath($loopWavB);source_wav_sha256=(Get-FileSha256 $loopWavB);decoded_pcm_path=[IO.Path]::GetFullPath($loopPcmB);decoded_pcm_sha256=$loopPcmHashB}
            )
        }
        d9_14_full_acceptance='NOT_CLOSED'
        d9_15='WAIVED_NOT_EVIDENCED_FOR_CANDIDATE_ONLY'
        d9_16='BLOCKED_PENDING_FULL_ACCEPTANCE'
        d9_17='BLOCKED'
        d4_8='LIMITED_QUALIFICATION_ONLY_NOT_GLOBAL_ACTIVATION'
        general_d_renderer_activation=$false
        release_authority='NONE'
        c11c_reference_mutated=$false
    }
    $reportPath = Join-Path $RunRoot 'D9_14_PRODUCTION_QUALIFICATION_REPORT.json'
    [IO.File]::WriteAllText($reportPath,($report | ConvertTo-Json -Depth 30),$Utf8NoBom)
    & python $Contract finalize --report $reportPath --project-root $ProjectRoot
    if ($LASTEXITCODE -ne 0) { throw 'Report finalization failed; no qualification baseline sealed.' }
    Write-Host "[C11-D-QUALIFICATION] MEDIA ROOT: $MediaRoot"
    Write-Host "[C11-D-QUALIFICATION] REPORT: $reportPath"
    $baselinePath = Join-Path $RunRoot 'C11D_PRODUCTION_QUALIFICATION_BASELINE_V1.json'
    & python $Contract audit-baseline --baseline $baselinePath --project-root $ProjectRoot
    if ($LASTEXITCODE -ne 0) { throw 'Final qualification baseline audit failed.' }
    Write-Host '[C11-D-QUALIFICATION] PASS | 4 final A/V MP4 | Challenge D3 Music Engine V5 mux PASS | deterministic loop replay PASS | music seed isolation PASS | D9.14 full acceptance NOT CLOSED | release_authority=NONE'
}
catch {
    $failure = [ordered]@{schema='C11-D-D9.14-PRODUCTION-QUALIFICATION-FAILURE-V1';run_id=$RunId;failed_utc=(Get-Date).ToUniversalTime().ToString('o');status='FAILED_FAIL_CLOSED';error=$_.Exception.Message;run_root=$RunRoot;release_authority='NONE';D9_14='NOT_CLOSED';D4_8='LIMITED_QUALIFICATION_ONLY_NOT_GLOBAL_ACTIVATION'}
    $failurePath = Join-Path $RunRoot 'D9_14_PRODUCTION_QUALIFICATION_FAILURE.json'
    [IO.File]::WriteAllText($failurePath,($failure | ConvertTo-Json -Depth 10),$Utf8NoBom)
    Write-Error ("Qualification failed closed. Diagnostic root: {0}. Reason: {1}" -f $RunRoot,$_.Exception.Message)
    exit 2
}
