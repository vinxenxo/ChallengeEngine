#requires -Version 5.1
[CmdletBinding()]
param(
    [switch]$AuthorizePilot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$Root = (Get-Location).Path
$D92Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_2'
$EvidenceRoot = Join-Path $D92Root 'evidence'
$MediaRoot = Join-Path $D92Root 'pilot_media'
$ContractPath = Join-Path $Root 'definitions\c11d\d9\D9_AUDIO_ENABLED_PILOT_V1.json'
$D87Root = Join-Path $Root 'artifacts\tests\c11d_d8\d8_7'
$D90Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_0'
$D91Root = Join-Path $Root 'artifacts\tests\c11d_d9\d9_1'
$MusicEnginePath = Join-Path $Root 'tools\c11d\d3\c11d_music_engine_v5.py'
$MusicSpecPath = Join-Path $Root 'definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json'
$StyleProfilePath = Join-Path $Root 'definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json'
$Receipt91Path = Join-Path $D91Root 'evidence\d9_1_receipt.json'
$D91VideoPath = Join-Path $D91Root 'pilot_media\CHALLENGE_001\CHALLENGE_001_seed_12345.mp4'
$D91MutationPath = Join-Path $D91Root 'evidence\d9_1_mutation_guard.json'
$ReceiptPath = Join-Path $EvidenceRoot 'd9_2_receipt.json'
$ProbePath = Join-Path $EvidenceRoot 'd9_2_ffprobe.json'
$MusicPath = Join-Path $EvidenceRoot 'd9_2_music_render.json'
$MusicShaPath = Join-Path $EvidenceRoot 'd9_2_music_sha256.json'
$MuxLogPath = Join-Path $EvidenceRoot 'd9_2_mux.log'
$MutationPath = Join-Path $EvidenceRoot 'd9_2_mutation_guard.json'
$ShaPath = Join-Path $EvidenceRoot 'd9_2_media_sha256.json'
$QaPath = Join-Path $EvidenceRoot 'd9_2_audio_qa.json'
$PilotOutput = Join-Path $MediaRoot 'CHALLENGE_001_seed_12345_AV.mp4'

foreach($p in @($ContractPath,$MusicEnginePath,$MusicSpecPath,$StyleProfilePath,$Receipt91Path,$D91VideoPath,$D91MutationPath)) {
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)){ throw "Required path missing: $p" }
}
foreach($p in @($D87Root,$D90Root,$D91Root)) {
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
function Hash-Bytes([byte[]]$Bytes) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($Bytes)) -replace '-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
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

$cfg = Read-Json $ContractPath
if([string]$cfg.schema -ne 'C11-D-D9-AUDIO-ENABLED-PILOT-V1'){ throw 'D9.2 contract identity mismatch.' }
if([string]$cfg.challenge_id -ne 'CHALLENGE_001'){ throw 'D9.2 challenge mismatch.' }
if([int]$cfg.seed -ne 12345){ throw 'D9.2 gameplay seed mismatch.' }
if([int]$cfg.music_seed -ne 840001){ throw 'D9.2 music seed mismatch.' }
if([string]$cfg.delivery_profile_id -ne 'REVIEW_720'){ throw 'D9.2 delivery profile mismatch.' }
if([string]$cfg.music_engine_id -ne 'c11d_music_engine_v5'){ throw 'D9.2 music engine mismatch.' }
if([string]$cfg.music_engine_version -ne '5.0'){ throw 'D9.2 music engine version mismatch.' }
if([string]$cfg.style_profile_id -ne 'challenge_8bit_v1'){ throw 'D9.2 style profile mismatch.' }
if([string]$cfg.release_authority -ne 'NONE'){ throw 'D9.2 release authority boundary failed.' }

$d87Candidates=@(Get-ChildItem -LiteralPath $D87Root -Filter '*.json' -File -Force | Sort-Object Name)
$d87=$null
foreach($f in $d87Candidates){
    try {
        $o=Read-Json $f.FullName
        if([string]$o.checkpoint -eq 'D8.7' -and [string]$o.status -eq 'CLOSED'){ $d87=$o; break }
    } catch {}
}
if($null -eq $d87){ throw 'No D8.7 PASS/CLOSED receipt found.' }
if([string]$d87.result -ne 'PASS_NO_MEDIA'){ throw 'D8.7 result is not PASS_NO_MEDIA.' }
if([string]$d87.release_authority -ne 'NONE'){ throw 'D8.7 release authority is not NONE.' }

$d90Candidates=@(Get-ChildItem -LiteralPath $D90Root -Filter '*.json' -File -Recurse -Force | Sort-Object FullName)
$d90=$null
foreach($f in $d90Candidates){
    try {
        $o=Read-Json $f.FullName
        $isD90=(($null -ne $o.phase -and [string]$o.phase -eq 'D9.0') -or ($null -ne $o.checkpoint -and [string]$o.checkpoint -eq 'D9.0'))
        $isPreflight=($null -ne $o.status -and [string]$o.status -eq 'PREFLIGHT_ONLY')
        $isPass=($null -ne $o.result -and [string]$o.result -eq 'PASS')
        if($isD90 -and $isPreflight -and $isPass){ $d90=$o; break }
    } catch {}
}
if($null -eq $d90){ throw 'No valid D9.0 PASS/PREFLIGHT_ONLY evidence found.' }
if($null -ne $d90.pilot_authorized -and [bool]$d90.pilot_authorized){ throw 'D9.0 pilot authority must remain false.' }

$d91=Read-Json $Receipt91Path
if([string]$d91.checkpoint -ne 'D9.1'){ throw 'D9.1 receipt checkpoint mismatch.' }
if([string]$d91.result -ne 'PASS'){ throw 'D9.1 result is not PASS.' }
if([string]$d91.status -ne 'PILOT_COMPLETE'){ throw 'D9.1 status is not PILOT_COMPLETE.' }
if([string]$d91.challenge_id -ne 'CHALLENGE_001'){ throw 'D9.1 challenge mismatch.' }
if([int]$d91.seed -ne 12345){ throw 'D9.1 gameplay seed mismatch.' }
if([int]$d91.music_seed -ne 840001){ throw 'D9.1 music seed mismatch.' }
if([string]$d91.delivery_profile_id -ne 'REVIEW_720'){ throw 'D9.1 delivery profile mismatch.' }

$d91Mutation=Read-Json $D91MutationPath
if([string]$d91Mutation.result -ne 'PASS'){ throw 'D9.1 mutation guard is not PASS.' }
if([bool]$d91Mutation.protected_roots_equal -ne $true){ throw 'D9.1 protected roots are not equal.' }
if([bool]$d91Mutation.release_product_mutation_performed){ throw 'D9.1 release mutation occurred.' }

if(-not $AuthorizePilot){ throw 'D9.2 physical A/V execution is disabled. Re-run with -AuthorizePilot.' }
if((Test-Path -LiteralPath $MediaRoot) -and @((Get-ChildItem -LiteralPath $MediaRoot -File -Recurse -Force -ErrorAction SilentlyContinue)).Count -gt 0){ throw 'D9.2 pilot media root is not empty; replacement is forbidden.' }
New-Item -ItemType Directory -Force -Path $EvidenceRoot,$MediaRoot | Out-Null

$duration=[double]$d91.duration_seconds
$frames=[int]$d91.frames
$fps=[int]$d91.fps
if($frames -lt 1 -or $fps -lt 1 -or $duration -le 0){ throw 'D9.1 timing data is invalid.' }

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
foreach($p in $protectedRoots){
    if(Test-Path -LiteralPath $p){
        $beforeProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p}
    }
}

$TempRoot=[System.IO.Path]::GetTempPath()
$TempDir=Join-Path $TempRoot 'c11d92'
if(Test-Path -LiteralPath $TempDir){ Remove-Item -LiteralPath $TempDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null
$TempMusicPath=Join-Path $TempDir 'music.wav'
$TempFinalPath=Join-Path $TempDir 'final.mp4'
$TempMusicReceipt=Join-Path $TempDir 'music.json'

try {
    $musicRaw=& python.exe $MusicEnginePath --engine $MusicSpecPath --profile $StyleProfilePath --output $TempMusicPath --seed 840001 --tempo 104 --duration $duration --variation 0 2>&1
    if($LASTEXITCODE -ne 0){ throw 'Music Engine V5 render failed.' }
    $musicLine=$musicRaw | Select-Object -Last 1
    if([string]::IsNullOrWhiteSpace([string]$musicLine)){ throw 'Music Engine returned no JSON receipt.' }
    $musicInfo=([string]$musicLine | ConvertFrom-Json)
    if([string]$musicInfo.engine_id -ne 'c11d_music_engine_v5'){ throw 'Music receipt engine identity mismatch.' }
    if([string]$musicInfo.engine_version -ne '5.0'){ throw 'Music receipt version mismatch.' }
    if([string]$musicInfo.style_profile_id -ne 'challenge_8bit_v1'){ throw 'Music receipt style profile mismatch.' }
    if([int]$musicInfo.music_seed -ne 840001){ throw 'Music receipt seed mismatch.' }
    if([double]$musicInfo.duration_seconds -lt ($duration-0.01) -or [double]$musicInfo.duration_seconds -gt ($duration+0.01)){ throw 'Music duration mismatch.' }
    if([double]$musicInfo.peak_linear -le 0){ throw 'Music render appears silent.' }
    Write-Json $MusicPath $musicInfo 12
    Write-Json $MusicShaPath ([ordered]@{wav_sha256=(Hash-File $TempMusicPath);bytes=[int64](Get-Item $TempMusicPath).Length;music_seed=840001;duration_seconds=$duration}) 8

    $muxRaw=& ffmpeg.exe -y -v error -i $D91VideoPath -i $TempMusicPath -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $TempFinalPath 2>&1
    $muxLogText=($muxRaw -join [Environment]::NewLine)
    [System.IO.File]::WriteAllText($MuxLogPath,$muxLogText,[System.Text.Encoding]::UTF8)
    if($LASTEXITCODE -ne 0){ throw 'FFmpeg A/V mux failed.' }
    if(-not(Test-Path -LiteralPath $TempFinalPath -PathType Leaf)){ throw 'FFmpeg did not produce final MP4.' }

    [System.IO.File]::Copy($TempFinalPath,$PilotOutput,$false)

    $probeRaw=& ffprobe.exe -v error -count_frames -show_streams -show_format -of json -- $PilotOutput 2>&1
    if($LASTEXITCODE -ne 0){ throw 'ffprobe failed on D9.2 final MP4.' }
    $probeText=$probeRaw -join [Environment]::NewLine
    [System.IO.File]::WriteAllText($ProbePath,$probeText,[System.Text.Encoding]::UTF8)
    $probe=$probeText|ConvertFrom-Json
    $video=@($probe.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
    $audio=@($probe.streams|Where-Object{$_.codec_type -eq 'audio'})|Select-Object -First 1
    if($null -eq $video){ throw 'D9.2 final MP4 has no video stream.' }
    if($null -eq $audio){ throw 'D9.2 final MP4 has no audio stream.' }
    if([int]$video.width -ne 720 -or [int]$video.height -ne 1280){ throw "D9.2 video resolution mismatch: $($video.width)x$($video.height)" }
    if([string]$video.r_frame_rate -ne ('{0}/1' -f $fps)){ throw "D9.2 video FPS mismatch: $($video.r_frame_rate)" }
    if([int]$video.nb_read_frames -ne $frames){ throw "D9.2 frame mismatch: $($video.nb_read_frames), expected $frames" }
    if([int]$audio.sample_rate -ne 48000){ throw "D9.2 audio sample rate mismatch: $($audio.sample_rate)" }
    if([int]$audio.channels -ne 2){ throw "D9.2 audio channel mismatch: $($audio.channels)" }
    if([string]$audio.codec_name -ne 'aac'){ throw "D9.2 audio codec mismatch: $($audio.codec_name)" }
    $videoDuration=[double]$video.duration
    $audioDuration=[double]$audio.duration
    if([Math]::Abs($videoDuration-$audioDuration) -gt 0.15){ throw "D9.2 A/V duration drift exceeds tolerance: video=$videoDuration audio=$audioDuration" }

    $qaPsi=New-Object System.Diagnostics.ProcessStartInfo
    $qaPsi.FileName='ffmpeg.exe'
    $qaPilot=$PilotOutput.Replace('"','\"')
    $qaPsi.Arguments='-hide_banner -nostats -v info -i "'+$qaPilot+'" -map 0:a:0 -af volumedetect -f null NUL'
    $qaPsi.UseShellExecute=$false
    $qaPsi.CreateNoWindow=$true
    $qaPsi.RedirectStandardError=$true
    $qaProc=New-Object System.Diagnostics.Process
    $qaProc.StartInfo=$qaPsi
    [void]$qaProc.Start()
    $qaText=$qaProc.StandardError.ReadToEnd()
    $qaProc.WaitForExit()
    $qaExit=$qaProc.ExitCode
    $maxMatch=[regex]::Match($qaText,'max_volume:\s*(-?(?:[0-9]+(?:\.[0-9]+)?|[0-9]*\.[0-9]+))\s*dB', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $meanMatch=[regex]::Match($qaText,'mean_volume:\s*(-?(?:[0-9]+(?:\.[0-9]+)?|[0-9]*\.[0-9]+))\s*dB', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if($qaExit -ne 0 -or -not $maxMatch.Success){
        Write-Json $QaPath ([ordered]@{result='FAIL';audio_stream_present=$true;metric='volumedetect';max_volume_db=$null;mean_volume_db=$null;diagnostic='FFmpeg volumedetect execution or statistics extraction failed';ffmpeg_exit_code=$qaExit;ffmpeg_output=$qaText}) 10
        throw 'Unable to determine final audio max volume from FFmpeg volumedetect output.'
    }
    $maxVolume=[double]$maxMatch.Groups[1].Value
    $meanVolume=$null
    if($meanMatch.Success){ $meanVolume=[double]$meanMatch.Groups[1].Value }
    if($maxVolume -eq [double]::NegativeInfinity -or $maxVolume -le -90){ throw 'Final audio appears silent.' }
    Write-Json $QaPath ([ordered]@{result='PASS';audio_stream_present=$true;codec='aac';sample_rate_hz=48000;channels=2;max_volume_db=$maxVolume;mean_volume_db=$meanVolume;non_silent=$true;d3_2_music_engine='c11d_music_engine_v5';style_profile='challenge_8bit_v1';music_seed=840001}) 10

    $mediaSha=@(
        [ordered]@{path=$PilotOutput.Substring($Root.Length+1).Replace('\','/');sha256=Hash-File $PilotOutput;bytes=[int64](Get-Item $PilotOutput).Length},
        [ordered]@{path=$TempMusicPath;sha256=Hash-File $TempMusicPath;bytes=[int64](Get-Item $TempMusicPath).Length}
    )
    Write-Json $ShaPath $mediaSha 8

    $afterProtected=@()
    foreach($p in $protectedRoots){
        if(Test-Path -LiteralPath $p){
            $afterProtected += [pscustomobject]@{root=$p.Substring($Root.Length+1).Replace('\','/');files=Get-TreeSnapshot $p}
        }
    }
    $protectedEqual=([string]($beforeProtected|ConvertTo-Json -Depth 16 -Compress) -eq [string]($afterProtected|ConvertTo-Json -Depth 16 -Compress))
    Write-Json $MutationPath ([ordered]@{result=$(if($protectedEqual){'PASS'}else{'FAIL'});allowed_write_root='artifacts/tests/c11d_d9/d9_2';physical_media_mutation_performed=$true;release_product_mutation_performed=$false;protected_roots_equal=$protectedEqual}) 10
    if(-not $protectedEqual){ throw 'D9.2 protected root mutation detected.' }

    if([string]$d91.release_authority -ne 'NONE'){ throw 'D9.1 release authority is not NONE.' }
    $receipt=[ordered]@{
        contract='C11-D-D9-AUDIO-ENABLED-PILOT-V1'
        checkpoint='D9.2'
        result='PASS'
        status='PILOT_COMPLETE'
        pilot_authorized=$true
        challenge_id='CHALLENGE_001'
        seed=12345
        music_seed=840001
        mode='REVIEW'
        delivery_profile_id='REVIEW_720'
        presentation_profile_id='social_default_v1'
        audio_enabled=$true
        music_engine_id='c11d_music_engine_v5'
        music_engine_version='5.0'
        style_profile_id='challenge_8bit_v1'
        source_visual=$D91VideoPath.Substring($Root.Length+1).Replace('\','/')
        delivery_resolution='720x1280'
        fps=$fps
        frames=$frames
        duration_seconds=$duration
        audio_codec='aac'
        audio_sample_rate_hz=48000
        audio_channels=2
        final_av_mp4=$PilotOutput.Substring($Root.Length+1).Replace('\','/')
        release_authority='NONE'
        global_production_execution=$false
        bulk_execution=$false
        release_product_created=$false
        d9_1_receipt=$Receipt91Path.Substring($Root.Length+1).Replace('\','/')
        next='D9.3 - deterministic A/V repeat + negative controls'
    }
    Write-Json $ReceiptPath $receipt 12

    Write-Host "D9.2 PASS | challenge=CHALLENGE_001 | profile=REVIEW_720 | frames=$frames | video=$($PilotOutput) | audio=AAC@48kHz | music_seed=840001 | release_authority=NONE"
}
finally {
    if(Test-Path -LiteralPath $TempDir){ Remove-Item -LiteralPath $TempDir -Recurse -Force -ErrorAction SilentlyContinue }
}
