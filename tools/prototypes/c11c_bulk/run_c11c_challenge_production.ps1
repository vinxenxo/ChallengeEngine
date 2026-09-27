param(
    [Parameter(Mandatory=$true)][ValidatePattern('^CHALLENGE_[0-9]{3}$')][string]$ChallengeId,
    [Parameter(Mandatory=$true)][ValidateRange(1,2147483646)][int]$Seed,
    [ValidateSet('REVIEW_720','META_REELS_FINAL_V1')][string]$DeliveryProfile='REVIEW_720',
    [string]$OutputRoot='',
    [switch]$NoSound,
    [switch]$ExportGif,
    [switch]$KeepAvi,
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$source=Join-Path $ProjectRoot "challenges\$ChallengeId.json"
if(-not(Test-Path -LiteralPath $source)){throw "Challenge definition not found: $source"}
$cfg=Get-Content -Raw -LiteralPath $source | ConvertFrom-Json
if($null -eq $cfg.generation){throw "Challenge has no generation block: $ChallengeId"}
$cfg.generation.seed=$Seed
$video=$cfg.video
$fps=[int]$video.fps
if($fps -lt 24 -or $fps -gt 60){throw "Challenge FPS outside supported range: $fps"}
$total=if($null -ne $video.total_duration){[double]$video.total_duration}else{[double]$video.hook_duration+[double]$video.game_duration+[double]$video.reveal_duration+[double]$video.cta_duration}
$frames=[int][math]::Round($total*$fps)
if($DeliveryProfile -eq 'META_REELS_FINAL_V1'){$width=1080;$height=1920;$gop=[int]($fps*3)}else{$width=720;$height=1280;$gop=[int]($fps*3)}
if([string]::IsNullOrWhiteSpace($OutputRoot)){$OutputRoot=Join-Path $ProjectRoot 'artifacts\production\challenges'}
$productRoot=Join-Path $OutputRoot $ChallengeId
if((Test-Path -LiteralPath $productRoot) -and -not $Force){throw "Challenge product exists: $productRoot. Use -Force for deliberate replacement."}
$stage=Join-Path $ProjectRoot ('artifacts\scratch\challenge_production\'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $stage | Out-Null
$request=Join-Path $stage "${ChallengeId}_seed_${Seed}_effective.json"
[IO.File]::WriteAllText($request,($cfg|ConvertTo-Json -Depth 40),(New-Object Text.UTF8Encoding($false)))
$avi=Join-Path $stage "${ChallengeId}_seed_${Seed}.avi"
$pcm=Join-Path $stage "${ChallengeId}_seed_${Seed}.pcm"
$out=Join-Path $stage "${ChallengeId}_seed_${Seed}.mp4"
$runLog=Join-Path $stage 'godot.log'
try{
    Write-Host "[CHALLENGE] $ChallengeId seed=$Seed profile=$DeliveryProfile resolution=${width}x${height} fps=$fps duration=$total"
    $godotArgs=@('--headless','--path',$ProjectRoot,'--scene','Main.tscn','--write-movie',$avi,'--fixed-fps',([string]$fps),'--resolution',("${width}x${height}"),'--quit-after',([string]$frames),'--','--config='+$request)
    if(-not $NoSound){$godotArgs += '--audio-output='+$pcm}
    $old=$ErrorActionPreference; $ErrorActionPreference='Continue'
    try{& godot @godotArgs *> $runLog; $godotExit=$LASTEXITCODE}finally{$ErrorActionPreference=$old}
    if($godotExit -ne 0){throw "Godot challenge render failed: exit=$godotExit. See $runLog"}
    if(-not(Test-Path -LiteralPath $avi)){throw "Movie Maker did not create AVI: $avi"}
    $ff=@('-y','-hide_banner','-loglevel','error','-i',$avi,'-an','-c:v','libx264','-preset','fast','-crf','18','-profile:v','high','-pix_fmt','yuv420p','-r',([string]$fps),'-g',([string]$gop),'-keyint_min',([string]$gop),'-sc_threshold','0','-flags','+cgop','-x264-params',("open_gop=0:keyint=$gop:min-keyint=$gop:scenecut=0"),'-movflags','+faststart')
    if(-not $NoSound -and (Test-Path -LiteralPath $pcm)){$ff += @('-i',$pcm,'-map','0:v:0','-map','1:a:0','-c:a','aac','-profile:a','aac_low','-b:a','192k','-ar','48000','-ac','2','-shortest')}
    $ff += $out
    & ffmpeg @ff
    if($LASTEXITCODE -ne 0){throw 'FFmpeg encode failed.'}
    if(-not(Test-Path -LiteralPath $out)){throw "Final MP4 missing: $out"}
    $probe=((& ffprobe -v error -show_streams -show_format -of json $out) -join "`n")|ConvertFrom-Json
    $streams=@($probe.streams)
    $v=@($streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
    if([int]$v.width -ne $width -or [int]$v.height -ne $height){throw "Final resolution mismatch: $($v.width)x$($v.height)"}
    if($DeliveryProfile -eq 'META_REELS_FINAL_V1' -and [double]$probe.format.duration -gt 90.0){throw 'Meta Reels target duration exceeds 90 seconds.'}
    if($Force -and(Test-Path -LiteralPath $productRoot)){Remove-Item -LiteralPath $productRoot -Recurse -Force}
    New-Item -ItemType Directory -Force -Path $productRoot | Out-Null
    $productMp4=Join-Path $productRoot "${ChallengeId}_seed_${Seed}.mp4"
    Copy-Item -LiteralPath $out -Destination $productMp4 -Force
    Copy-Item -LiteralPath $request -Destination (Join-Path $productRoot 'challenge_definition_effective.json') -Force
    Copy-Item -LiteralPath $runLog -Destination (Join-Path $productRoot 'godot.log') -Force
    if($KeepAvi){Copy-Item -LiteralPath $avi -Destination (Join-Path $productRoot "${ChallengeId}_seed_${Seed}.avi") -Force}
    if($ExportGif){& ffmpeg -y -hide_banner -loglevel error -i $productMp4 -vf 'fps=24,scale=360:640:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96:stats_mode=diff[p];[s1][p]paletteuse=dither=sierra2_4a' -loop 0 (Join-Path $productRoot "${ChallengeId}_seed_${Seed}.gif");if($LASTEXITCODE -ne 0){throw 'GIF export failed.'}}
    $content=[string]$cfg.content.hook
    $hashtags='#VisualChallenge #GenerativeArt #GodotEngine #ProceduralArt'
    $copy="$content`n`nChallenge $ChallengeId · $($cfg.mechanic)`n`n$hashtags"
    [IO.File]::WriteAllText((Join-Path $productRoot 'social.txt'),("COPY_PASTE_READY:`n"+$copy+"`n`nTITLE:`n$ChallengeId · $($cfg.mechanic)`n`nDESCRIPTION:`n$copy`n`nHASHTAGS:`n$hashtags`n"),(New-Object Text.UTF8Encoding($false)))
    $manifest=[ordered]@{schema='C11-C-CHALLENGE-PRODUCTION-V2';revision='2.17.0';status='EXPERIMENTAL_ADDITIVE_WRAPPER';challenge_id=$ChallengeId;seed=$Seed;mechanic=$cfg.mechanic;delivery_profile=$DeliveryProfile;resolution="${width}x${height}";fps=$fps;duration_seconds=$total;frames=$frames;gop_seconds=3;closed_gop_encoder_contract=$true;video_codec='h264';pixel_format='yuv420p';audio_present=([bool](@($streams|Where-Object{$_.codec_type -eq 'audio'}).Count));product=$productMp4;source_definition=$source;asset_paths=$cfg.assets}
    [IO.File]::WriteAllText((Join-Path $productRoot 'production_manifest.json'),($manifest|ConvertTo-Json -Depth 30),(New-Object Text.UTF8Encoding($false)))
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[CHALLENGE] PASS $ChallengeId seed=$Seed -> $productRoot"
}finally{if(Test-Path -LiteralPath $stage){Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue}}
