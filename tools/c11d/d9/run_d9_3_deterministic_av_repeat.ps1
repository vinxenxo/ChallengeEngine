#requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$AuthorizePilot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$Root = (Get-Location).Path
$D93Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_3'
$EvidenceRoot = Join-Path $D93Root 'evidence'
$MediaRoot = Join-Path $D93Root 'pilot_media'
$ContractPath = Join-Path $Root 'definitions\c11d\d9\D9_DETERMINISTIC_AV_REPEAT_V1.json'
$D87Root = Join-Path $Root 'artifacts\tests\c11d_d8\d8_7'
$D90Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_0'
$D91Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_1'
$D92Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_2'
$Receipt91Path = Join-Path $D91Root 'evidence\d9_1_receipt.json'
$Receipt92Path = Join-Path $D92Root 'evidence\d9_2_receipt.json'
$D91MutationPath = Join-Path $D91Root 'evidence\d9_1_mutation_guard.json'
$MusicEnginePath = Join-Path $Root 'tools\c11d\d3\c11d_music_engine_v5.py'
$MusicSpecPath = Join-Path $Root 'definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json'
$StyleProfilePath = Join-Path $Root 'definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json'
$ReceiptPath = Join-Path $EvidenceRoot 'd9_3_receipt.json'
$RepeatabilityPath = Join-Path $EvidenceRoot 'd9_3_repeatability.json'
$NegativePath = Join-Path $EvidenceRoot 'd9_3_negative_control.json'
$ProbePath = Join-Path $EvidenceRoot 'd9_3_ffprobe.json'
$MutationPath = Join-Path $EvidenceRoot 'd9_3_mutation_guard.json'

foreach($p in @($ContractPath,$MusicEnginePath,$MusicSpecPath,$StyleProfilePath,$Receipt91Path,$Receipt92Path,$D91MutationPath)) {
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)){ throw "Required path missing: $p" }
}
foreach($p in @($D87Root,$D90Root,$D91Root,$D92Root)) {
    if(-not (Test-Path -LiteralPath $p -PathType Container)){ throw "Required evidence root missing: $p" }
}

function Read-Json([string]$Path) {
    return ([System.IO.File]::ReadAllText($Path) | ConvertFrom-Json)
}
function Write-Json([string]$Path,[object]$Value,[int]$Depth) {
    $text = [string]($Value | ConvertTo-Json -Depth $Depth)
    [System.IO.File]::WriteAllBytes($Path,[System.Text.Encoding]::UTF8.GetBytes($text))
}
function Hash-File([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Get-TreeSnapshot([string]$Path) {
    if(-not(Test-Path -LiteralPath $Path)){ return @() }
    $items = @(
        Get-ChildItem -LiteralPath $Path -File -Recurse -Force |
        Sort-Object FullName
    )
    $rows = @()
    foreach($f in $items){
        $rows += [pscustomobject]@{
            path = $f.FullName.Substring($Root.Length + 1).Replace('\','/')
            length = [int64]$f.Length
            sha256 = Hash-File $f.FullName
        }
    }
    return @($rows)
}
function Invoke-Music([int]$Seed,[string]$WavPath,[string]$ReceiptPathLocal,[double]$Duration) {
    $raw=& python.exe $MusicEnginePath --engine $MusicSpecPath --profile $StyleProfilePath --output $WavPath --seed $Seed --tempo 104 --duration $Duration --variation 0 2>&1
    if($LASTEXITCODE -ne 0){ throw "Music Engine V5 render failed for music_seed=$Seed." }
    $line=$raw | Select-Object -Last 1
    if([string]::IsNullOrWhiteSpace([string]$line)){ throw "Music Engine returned no JSON receipt for music_seed=$Seed." }
    $info=([string]$line | ConvertFrom-Json)
    if([string]$info.engine_id -ne 'c11d_music_engine_v5'){ throw 'Music receipt engine identity mismatch.' }
    if([string]$info.engine_version -ne '5.0'){ throw 'Music receipt version mismatch.' }
    if([string]$info.style_profile_id -ne 'challenge_8bit_v1'){ throw 'Music receipt style profile mismatch.' }
    if([int]$info.music_seed -ne $Seed){ throw "Music receipt seed mismatch: expected $Seed." }
    if([double]$info.duration_seconds -lt ($Duration-0.01) -or [double]$info.duration_seconds -gt ($Duration+0.01)){ throw "Music duration mismatch for music_seed=$Seed." }
    if([double]$info.peak_linear -le 0){ throw "Music render appears silent for music_seed=$Seed." }
    if(-not(Test-Path -LiteralPath $WavPath -PathType Leaf)){ throw "Music WAV missing for music_seed=$Seed." }
    Write-Json $ReceiptPathLocal $info 12
    return [pscustomobject]@{
        seed=$Seed
        wav_sha256=Hash-File $WavPath
        wav_bytes=[int64](Get-Item -LiteralPath $WavPath).Length
        duration_seconds=[double]$info.duration_seconds
    }
}
function Invoke-Mux([string]$SourceVideo,[string]$WavPath,[string]$OutputPath,[string]$LogPath) {
    $raw=& ffmpeg.exe -y -v error -i $SourceVideo -i $WavPath -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $OutputPath 2>&1
    $log=($raw -join [Environment]::NewLine)
    [System.IO.File]::WriteAllText($LogPath,$log,[System.Text.Encoding]::UTF8)
    if($LASTEXITCODE -ne 0){ throw "FFmpeg A/V mux failed: $OutputPath" }
    if(-not(Test-Path -LiteralPath $OutputPath -PathType Leaf)){ throw "FFmpeg did not produce final MP4: $OutputPath" }
    if([int64](Get-Item -LiteralPath $OutputPath).Length -lt 100000){ throw "Final MP4 unexpectedly small: $OutputPath" }
}
function Probe-Av([string]$Path) {
    $raw=& ffprobe.exe -v error -count_frames -show_streams -show_format -of json -- $Path 2>&1
    if($LASTEXITCODE -ne 0){ throw "ffprobe failed: $Path" }
    $text=$raw -join [Environment]::NewLine
    $p=$text | ConvertFrom-Json
    $video=@($p.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
    $audio=@($p.streams|Where-Object{$_.codec_type -eq 'audio'})|Select-Object -First 1
    if($null -eq $video){ throw "No video stream: $Path" }
    if($null -eq $audio){ throw "No audio stream: $Path" }
    if([int]$video.width -ne 720 -or [int]$video.height -ne 1280){ throw "Video resolution mismatch: $Path" }
    if([string]$video.r_frame_rate -ne '60/1'){ throw "Video FPS mismatch: $Path" }
    if([int]$video.nb_read_frames -ne 540){ throw "Video frame mismatch: $Path" }
    if([string]$audio.codec_name -ne 'aac'){ throw "Audio codec mismatch: $Path" }
    if([int]$audio.sample_rate -ne 48000){ throw "Audio sample rate mismatch: $Path" }
    if([int]$audio.channels -ne 2){ throw "Audio channel mismatch: $Path" }
    $vd=[double]$video.duration
    $ad=[double]$audio.duration
    if([Math]::Abs($vd-$ad) -gt 0.15){ throw "A/V duration drift exceeds tolerance: $Path" }
    return [pscustomobject]@{
        video_width=[int]$video.width
        video_height=[int]$video.height
        video_fps=[string]$video.r_frame_rate
        video_frames=[int]$video.nb_read_frames
        video_duration=$vd
        audio_codec=[string]$audio.codec_name
        audio_sample_rate_hz=[int]$audio.sample_rate
        audio_channels=[int]$audio.channels
        audio_duration=$ad
        size_bytes=[int64](Get-Item -LiteralPath $Path).Length
    }
}

$cfg=Read-Json $ContractPath
if([string]$cfg.schema -ne 'C11-D-D9-DETERMINISTIC-AV-REPEAT-V1'){ throw 'D9.3 contract identity mismatch.' }
if([string]$cfg.challenge_id -ne 'CHALLENGE_001'){ throw 'D9.3 challenge mismatch.' }
if([int]$cfg.seed -ne 12345){ throw 'D9.3 gameplay seed mismatch.' }
if([int]$cfg.music_seed -ne 840001){ throw 'D9.3 music seed mismatch.' }
if([int]$cfg.negative_music_seed -eq [int]$cfg.music_seed){ throw 'D9.3 negative music seed must differ.' }
if([string]$cfg.delivery_profile_id -ne 'REVIEW_720'){ throw 'D9.3 delivery profile mismatch.' }
if([string]$cfg.music_engine_id -ne 'c11d_music_engine_v5'){ throw 'D9.3 music engine mismatch.' }
if([string]$cfg.music_engine_version -ne '5.0'){ throw 'D9.3 music engine version mismatch.' }
if([string]$cfg.style_profile_id -ne 'challenge_8bit_v1'){ throw 'D9.3 style profile mismatch.' }
if([int]$cfg.repeat_count -ne 2){ throw 'D9.3 repeat count mismatch.' }
if([string]$cfg.release_authority -ne 'NONE'){ throw 'D9.3 release authority boundary failed.' }

$d87=$null
$d87Candidates=@(Get-ChildItem -LiteralPath $D87Root -Filter '*.json' -File -Force | Sort-Object Name)
foreach($f in $d87Candidates){ try { $o=Read-Json $f.FullName; if([string]$o.checkpoint -eq 'D8.7' -and [string]$o.status -eq 'CLOSED'){ $d87=$o; break } } catch {} }
if($null -eq $d87){ throw 'No D8.7 PASS/CLOSED receipt found.' }
if([string]$d87.result -ne 'PASS_NO_MEDIA'){ throw 'D8.7 result is not PASS_NO_MEDIA.' }
if([string]$d87.release_authority -ne 'NONE'){ throw 'D8.7 release authority is not NONE.' }

$d90=$null
$d90Candidates=@(Get-ChildItem -LiteralPath $D90Root -Filter '*.json' -File -Recurse -Force | Sort-Object FullName)
foreach($f in $d90Candidates){ try { $o=Read-Json $f.FullName; $isD90=(($null -ne $o.phase -and [string]$o.phase -eq 'D9.0') -or ($null -ne $o.checkpoint -and [string]$o.checkpoint -eq 'D9.0')); $isPre=($null -ne $o.status -and [string]$o.status -eq 'PREFLIGHT_ONLY'); $isPass=($null -ne $o.result -and [string]$o.result -eq 'PASS'); if($isD90 -and $isPre -and $isPass){ $d90=$o; break } } catch {} }
if($null -eq $d90){ throw 'No valid D9.0 PASS/PREFLIGHT_ONLY evidence found.' }
if($null -ne $d90.pilot_authorized -and [bool]$d90.pilot_authorized){ throw 'D9.0 pilot authority must remain false.' }

$d91=Read-Json $Receipt91Path
if([string]$d91.checkpoint -ne 'D9.1' -or [string]$d91.result -ne 'PASS' -or [string]$d91.status -ne 'PILOT_COMPLETE'){ throw 'D9.1 receipt is not PASS/PILOT_COMPLETE.' }
if([string]$d91.challenge_id -ne 'CHALLENGE_001' -or [int]$d91.seed -ne 12345 -or [string]$d91.delivery_profile_id -ne 'REVIEW_720'){ throw 'D9.1 authority/input identity mismatch.' }
if([int]$d91.fps -ne 60 -or [int]$d91.frames -ne 540){ throw 'D9.1 timing baseline mismatch.' }
$d91Mutation=Read-Json $D91MutationPath
if([string]$d91Mutation.result -ne 'PASS' -or -not [bool]$d91Mutation.protected_roots_equal){ throw 'D9.1 mutation guard is not PASS.' }

$d92=Read-Json $Receipt92Path
if([string]$d92.checkpoint -ne 'D9.2' -or [string]$d92.result -ne 'PASS' -or [string]$d92.status -ne 'PILOT_COMPLETE'){ throw 'D9.2 receipt is not PASS/PILOT_COMPLETE.' }
if([int]$d92.music_seed -ne 840001 -or [string]$d92.audio_codec -ne 'aac' -or [int]$d92.audio_sample_rate_hz -ne 48000 -or [int]$d92.audio_channels -ne 2){ throw 'D9.2 A/V baseline identity mismatch.' }

$D91VideoPath=Join-Path $D91Root 'pilot_media\CHALLENGE_001\CHALLENGE_001_seed_12345.mp4'
if(-not(Test-Path -LiteralPath $D91VideoPath -PathType Leaf)){ throw 'D9.1 source video missing.' }

if(-not $AuthorizePilot){ throw 'D9.3 physical repeat execution is disabled. Re-run with -AuthorizePilot.' }
if(Test-Path -LiteralPath $MediaRoot){ $existing=@(Get-ChildItem -LiteralPath $MediaRoot -File -Recurse -Force -ErrorAction SilentlyContinue); if($existing.Count -gt 0){ throw 'D9.3 pilot media root is not empty; replacement is forbidden.' } }
New-Item -ItemType Directory -Force -Path (Join-Path $MediaRoot 'repeat_a'),(Join-Path $MediaRoot 'repeat_b'),(Join-Path $MediaRoot 'negative_music_seed') | Out-Null
New-Item -ItemType Directory -Force -Path $EvidenceRoot | Out-Null

$protectedRoots=@(
    (Join-Path $Root 'c11c-suite'),
    (Join-Path $Root 'challenges'),
    (Join-Path $Root 'core'),
    (Join-Path $Root 'tests'),
    (Join-Path $Root 'tools\c11c'),
    (Join-Path $Root 'tools\c11d\d0'),
    (Join-Path $Root 'tools\c11d\d1'),
    (Join-Path $Root 'tools\c11d\d2'),
    (Join-Path $Root 'tools\c11d\d3'),
    (Join-Path $Root 'tools\c11d\d4'),
    (Join-Path $Root 'tools\c11d\d5'),
    (Join-Path $Root 'tools\c11d\d6'),
    (Join-Path $Root 'tools\c11d\d7'),
    (Join-Path $Root 'definitions\c11d\production'),
    (Join-Path $Root 'definitions\c11d\seeds'),
    (Join-Path $Root 'artifacts\releases'),
    (Join-Path $Root 'release')
)
$beforeProtected=@()
foreach($p in $protectedRoots){ if(Test-Path -LiteralPath $p){ $beforeProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p} } }

$duration=[double]$d91.duration_seconds
$repeatAWav=Join-Path $MediaRoot 'repeat_a\music.wav'
$repeatBWav=Join-Path $MediaRoot 'repeat_b\music.wav'
$negativeWav=Join-Path $MediaRoot 'negative_music_seed\music.wav'
$repeatAMp4=Join-Path $MediaRoot 'repeat_a\CHALLENGE_001_seed_12345_AV_repeat_A.mp4'
$repeatBMp4=Join-Path $MediaRoot 'repeat_b\CHALLENGE_001_seed_12345_AV_repeat_B.mp4'
$negativeMp4=Join-Path $MediaRoot 'negative_music_seed\CHALLENGE_001_seed_12345_AV_musicseed_840002.mp4'
$repeatAMusicReceipt=Join-Path $EvidenceRoot 'd9_3_music_repeat_a.json'
$repeatBMusicReceipt=Join-Path $EvidenceRoot 'd9_3_music_repeat_b.json'
$negativeMusicReceipt=Join-Path $EvidenceRoot 'd9_3_music_negative.json'
$repeatALog=Join-Path $EvidenceRoot 'd9_3_mux_repeat_a.log'
$repeatBLog=Join-Path $EvidenceRoot 'd9_3_mux_repeat_b.log'
$negativeLog=Join-Path $EvidenceRoot 'd9_3_mux_negative.log'

$musicA=Invoke-Music 840001 $repeatAWav $repeatAMusicReceipt $duration
$musicB=Invoke-Music 840001 $repeatBWav $repeatBMusicReceipt $duration
$musicN=Invoke-Music ([int]$cfg.negative_music_seed) $negativeWav $negativeMusicReceipt $duration

Invoke-Mux $D91VideoPath $repeatAWav $repeatAMp4 $repeatALog
Invoke-Mux $D91VideoPath $repeatBWav $repeatBMp4 $repeatBLog
Invoke-Mux $D91VideoPath $negativeWav $negativeMp4 $negativeLog

$probeA=Probe-Av $repeatAMp4
$probeB=Probe-Av $repeatBMp4
$probeN=Probe-Av $negativeMp4
$probeRows=@(
    [ordered]@{case='repeat_a';path=$repeatAMp4.Substring($Root.Length+1).Replace('\','/');probe=$probeA},
    [ordered]@{case='repeat_b';path=$repeatBMp4.Substring($Root.Length+1).Replace('\','/');probe=$probeB},
    [ordered]@{case='negative_music_seed';path=$negativeMp4.Substring($Root.Length+1).Replace('\','/');probe=$probeN}
)
Write-Json $ProbePath $probeRows 12

$mp4HashA=Hash-File $repeatAMp4
$mp4HashB=Hash-File $repeatBMp4
$mp4HashN=Hash-File $negativeMp4
$repeatPass=($musicA.wav_sha256 -eq $musicB.wav_sha256 -and $musicA.wav_bytes -eq $musicB.wav_bytes -and $mp4HashA -eq $mp4HashB)
$negativePass=($musicA.wav_sha256 -ne $musicN.wav_sha256 -and $mp4HashA -ne $mp4HashN)

Write-Json $RepeatabilityPath ([ordered]@{
    result=$(if($repeatPass){'PASS'}else{'FAIL'})
    deterministic_inputs=[ordered]@{challenge_id='CHALLENGE_001';seed=12345;music_seed=840001;delivery_profile_id='REVIEW_720';source_video=$D91VideoPath.Substring($Root.Length+1).Replace('\','/')}
    repeat_a=[ordered]@{wav_sha256=$musicA.wav_sha256;wav_bytes=$musicA.wav_bytes;mp4_sha256=$mp4HashA;mp4_bytes=[int64](Get-Item -LiteralPath $repeatAMp4).Length}
    repeat_b=[ordered]@{wav_sha256=$musicB.wav_sha256;wav_bytes=$musicB.wav_bytes;mp4_sha256=$mp4HashB;mp4_bytes=[int64](Get-Item -LiteralPath $repeatBMp4).Length}
    exact_wav_match=($musicA.wav_sha256 -eq $musicB.wav_sha256)
    exact_mp4_match=($mp4HashA -eq $mp4HashB)
}) 12
Write-Json $NegativePath ([ordered]@{
    result=$(if($negativePass){'PASS'}else{'FAIL'})
    baseline_music_seed=840001
    negative_music_seed=[int]$cfg.negative_music_seed
    baseline_wav_sha256=$musicA.wav_sha256
    negative_wav_sha256=$musicN.wav_sha256
    baseline_mp4_sha256=$mp4HashA
    negative_mp4_sha256=$mp4HashN
    wav_changed=($musicA.wav_sha256 -ne $musicN.wav_sha256)
    mp4_changed=($mp4HashA -ne $mp4HashN)
}) 12
if(-not $repeatPass){ throw 'D9.3 deterministic repeatability assertion failed.' }
if(-not $negativePass){ throw 'D9.3 negative control assertion failed.' }

$afterProtected=@()
foreach($p in $protectedRoots){ if(Test-Path -LiteralPath $p){ $afterProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p} } }
$protectedEqual=([string]($beforeProtected|ConvertTo-Json -Depth 16 -Compress) -eq [string]($afterProtected|ConvertTo-Json -Depth 16 -Compress))
Write-Json $MutationPath ([ordered]@{result=$(if($protectedEqual){'PASS'}else{'FAIL'});allowed_write_root='artifacts/tests/c11d_d9/d9_3';physical_media_mutation_performed=$true;release_product_mutation_performed=$false;protected_roots_equal=$protectedEqual}) 10
if(-not $protectedEqual){ throw 'D9.3 protected root mutation detected.' }

$receipt=[ordered]@{
    contract='C11-D-D9-DETERMINISTIC-AV-REPEAT-V1'
    checkpoint='D9.3'
    result='PASS'
    status='PILOT_REPEAT_COMPLETE'
    pilot_authorized=$true
    challenge_id='CHALLENGE_001'
    seed=12345
    music_seed=840001
    negative_music_seed=[int]$cfg.negative_music_seed
    mode='REVIEW'
    delivery_profile_id='REVIEW_720'
    presentation_profile_id='social_default_v1'
    source_visual=$D91VideoPath.Substring($Root.Length+1).Replace('\','/')
    repeatability_exact_wav=$true
    repeatability_exact_mp4=$true
    negative_control_music_changed=$true
    negative_control_mp4_changed=$true
    audio_codec='aac'
    audio_sample_rate_hz=48000
    audio_channels=2
    release_authority='NONE'
    global_production_execution=$false
    bulk_execution=$false
    release_product_created=$false
    d9_1_receipt=$Receipt91Path.Substring($Root.Length+1).Replace('\','/')
    d9_2_receipt=$Receipt92Path.Substring($Root.Length+1).Replace('\','/')
}
Write-Json $ReceiptPath $receipt 12

Write-Host "D9.3 PASS | challenge=CHALLENGE_001 | seed=12345 | music_seed=840001 | repeat_wav=EXACT | repeat_mp4=EXACT | negative_music_seed=$([int]$cfg.negative_music_seed) | release_authority=NONE"
