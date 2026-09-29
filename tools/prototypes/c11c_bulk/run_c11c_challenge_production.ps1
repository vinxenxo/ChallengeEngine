[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidatePattern('^CHALLENGE_[0-9]{3}$')][string]$ChallengeId,
    [Parameter(Mandatory=$true)][ValidateRange(1,2147483646)][int]$Seed,
    [ValidateSet('MASTER_1080','REVIEW_720','MIN_540','META_REELS_FINAL_V1','LONGFORM_1080')][string]$DeliveryProfile='MASTER_1080',
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
if(-not(Test-Path -LiteralPath $source -PathType Leaf)){throw "Challenge definition not found: $source"}

$cfg=Get-Content -Raw -LiteralPath $source -Encoding UTF8 | ConvertFrom-Json
if($null -eq $cfg.generation){throw "Challenge has no generation block: $ChallengeId"}
if($null -eq $cfg.video){throw "Challenge has no video block: $ChallengeId"}
$cfg.generation.seed=$Seed

$video=$cfg.video
$fps=[int]$video.fps
if($fps -lt 24 -or $fps -gt 60){throw "Challenge FPS outside supported range: $fps"}

function Convert-ToFrames {
    param([double]$Seconds,[int]$Rate)
    if($Seconds -lt 0){throw "Challenge timeline contains a negative duration: $Seconds"}
    return [Math]::Max(0,[int][Math]::Floor(($Seconds*$Rate)+0.5))
}

# Canonical C6-D4/C11-A.1 timing: derive exclusively from the four declarative phases.
# Legacy total_duration, when present in old definitions, is intentionally ignored.
$hookFrames=Convert-ToFrames ([double]$video.hook_duration) $fps
$gameFrames=Convert-ToFrames ([double]$video.game_duration) $fps
$revealDuration=0.0
$revealProperty=$video.PSObject.Properties['reveal_duration']
if($null -ne $revealProperty){$revealDuration=[double]$revealProperty.Value}
$revealFrames=Convert-ToFrames $revealDuration $fps
$ctaFrames=Convert-ToFrames ([double]$video.cta_duration) $fps
$frames=$hookFrames+$gameFrames+$revealFrames+$ctaFrames
if($frames -le 0){throw "Challenge timeline has no frames: $ChallengeId"}
if($gameFrames -le 0){throw "Challenge game_duration must be > 0: $ChallengeId"}
$total=$frames/[double]$fps

$sourceWidth=540
$sourceHeight=960
$profileTable = @{
    'MASTER_1080' = @{ Width=1080; Height=1920; DurationMax=90.0; Social=$true; AliasOf='' }
    'META_REELS_FINAL_V1' = @{ Width=1080; Height=1920; DurationMax=90.0; Social=$true; AliasOf='MASTER_1080' }
    'REVIEW_720' = @{ Width=720; Height=1280; DurationMax=90.0; Social=$true; AliasOf='' }
    'MIN_540' = @{ Width=540; Height=960; DurationMax=90.0; Social=$true; AliasOf='' }
    'LONGFORM_1080' = @{ Width=1080; Height=1920; DurationMax=0.0; Social=$false; AliasOf='' }
}
$profile=$profileTable[$DeliveryProfile]
$width=[int]$profile.Width
$height=[int]$profile.Height
$gop=[int]($fps*3)
if($profile.Social -and ($total -lt 3.0 -or $total -gt $profile.DurationMax)){throw "Delivery profile $DeliveryProfile requires duration 3-90s; effective timeline is $total s."}
if([string]::IsNullOrWhiteSpace($OutputRoot)){$OutputRoot=Join-Path $ProjectRoot 'artifacts\production\challenges'}
elseif(-not [IO.Path]::IsPathRooted($OutputRoot)){$OutputRoot=Join-Path $ProjectRoot $OutputRoot}
$OutputRoot=[IO.Path]::GetFullPath($OutputRoot)
$productRoot=Join-Path $OutputRoot $ChallengeId
if((Test-Path -LiteralPath $productRoot -PathType Container) -and -not $Force){throw "Challenge product exists: $productRoot. Use -Force for deliberate replacement."}

$stage=Join-Path $ProjectRoot ('artifacts\scratch\challenge_production\'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $stage | Out-Null
$request=Join-Path $stage "${ChallengeId}_seed_${Seed}_effective.json"
$avi=Join-Path $stage "${ChallengeId}_seed_${Seed}_source.avi"
$pcm=Join-Path $stage "${ChallengeId}_seed_${Seed}.pcm"
$out=Join-Path $stage "${ChallengeId}_seed_${Seed}.mp4"
$runLog=Join-Path $stage 'godot.log'
$commandFile=Join-Path $stage 'godot_command.txt'
[IO.File]::WriteAllText($request,($cfg|ConvertTo-Json -Depth 40),(New-Object Text.UTF8Encoding($false)))

function Quote-NativeArg {
    param([Parameter(Mandatory=$true)][string]$Value)
    if($Value -notmatch '[\s"]'){return $Value}
    return '"'+(($Value -replace '(\\*)"','$1$1\"') -replace '(\\+)$','$1$1')+'"'
}

function Resolve-GodotExecutable {
    $command=Get-Command godot.exe -CommandType Application -ErrorAction SilentlyContinue
    if($null -eq $command){$command=Get-Command godot -CommandType Application -ErrorAction SilentlyContinue}
    if($null -eq $command){throw 'No se encontró godot.exe en PATH.'}
    return [string]$command.Source
}

function Invoke-GodotMovieProcess {
    param(
        [Parameter(Mandatory=$true)][string]$FilePath,
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$WorkingDirectory,
        [Parameter(Mandatory=$true)][string]$StdoutPath,
        [Parameter(Mandatory=$true)][string]$StderrPath,
        [Parameter(Mandatory=$true)][string]$CommandPath
    )
    $psi=[Diagnostics.ProcessStartInfo]::new()
    $psi.FileName=$FilePath
    $psi.WorkingDirectory=$WorkingDirectory
    $psi.UseShellExecute=$false
    $psi.CreateNoWindow=$true
    $psi.RedirectStandardOutput=$true
    $psi.RedirectStandardError=$true
    # Preserve Godot UTF-8 diagnostics; Windows ANSI decoding can corrupt the Unicode multiplication sign.
    $psi.StandardOutputEncoding=[Text.Encoding]::UTF8
    $psi.StandardErrorEncoding=[Text.Encoding]::UTF8
    $quotedArguments=foreach($arg in $Arguments){Quote-NativeArg ([string]$arg)}
    $psi.Arguments=$quotedArguments -join ' '
    [IO.File]::WriteAllText($CommandPath,("$FilePath $($psi.Arguments)"),(New-Object Text.UTF8Encoding($false)))

    $process=[Diagnostics.Process]::new()
    $process.StartInfo=$psi
    if(-not $process.Start()){throw 'No se pudo iniciar godot.exe.'}
    $stdoutTask=$process.StandardOutput.ReadToEndAsync()
    $stderrTask=$process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdoutText=$stdoutTask.Result
    $stderrText=$stderrTask.Result
    [IO.File]::WriteAllText($StdoutPath,$stdoutText,(New-Object Text.UTF8Encoding($false)))
    [IO.File]::WriteAllText($StderrPath,$stderrText,(New-Object Text.UTF8Encoding($false)))
    [IO.File]::WriteAllText($runLog,$stdoutText+"`n"+$stderrText,(New-Object Text.UTF8Encoding($false)))
    return [int]$process.ExitCode
}

function Invoke-FFProbe {
    param([string]$VideoPath)
    $raw=& ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_read_frames,duration,codec_name,pix_fmt -of json -- $VideoPath 2>&1
    if($LASTEXITCODE -ne 0){throw "ffprobe falló para $VideoPath`n$($raw -join "`n")"}
    return (($raw -join "`n")|ConvertFrom-Json)
}

function Invoke-CommandOutput {
    param([string]$FilePath,[string[]]$Arguments)
    $raw=& $FilePath @Arguments 2>&1
    if($LASTEXITCODE -ne 0){throw "$FilePath falló con exit=$LASTEXITCODE`n$($raw -join "`n")"}
    return ($raw -join "`n")
}

function Enter-ChallengeNativeViewport {
    param([string]$Root)
    $override=Join-Path $Root 'override.cfg'
    if(-not(Test-Path -LiteralPath $override -PathType Leaf)){return $null}
    $quarantine=Join-Path $Root ('.override.challenge_quarantine_'+[guid]::NewGuid().ToString('N')+'.cfg')
    Move-Item -LiteralPath $override -Destination $quarantine -Force
    return [pscustomobject]@{Original=$override;Quarantine=$quarantine}
}

function Exit-ChallengeNativeViewport {
    param([object]$State)
    if($null -eq $State){return}
    $original=[string]$State.Original
    $quarantine=[string]$State.Quarantine
    if(Test-Path -LiteralPath $original){Remove-Item -LiteralPath $original -Force}
    if(Test-Path -LiteralPath $quarantine){Move-Item -LiteralPath $quarantine -Destination $original -Force}
}

$nativeViewportState=$null
$success=$false
try{
    Write-Host "[CHALLENGE] $ChallengeId seed=$Seed profile=$DeliveryProfile source=${sourceWidth}x${sourceHeight} delivery=${width}x${height} fps=$fps duration=$total frames=$frames"
    Write-Host "[CHALLENGE] Standard delivery profile: MASTER_1080=1080x1920; review/minimum profiles are additive; runtime capture remains native 540x960."
    Write-Host '[CHALLENGE] Contract-safe path: Godot source capture remains native 540x960; delivery scale is post-capture FFmpeg only.'

    # Challenge capture is deliberately isolated from the C11-C visual prototype override.
    # Any stale override.cfg is quarantined temporarily and restored byte-for-byte afterward.
    $nativeViewportState=Enter-ChallengeNativeViewport -Root $ProjectRoot

    $godotExe=Resolve-GodotExecutable
    $stdout=Join-Path $stage 'godot_stdout.log'
    $stderr=Join-Path $stage 'godot_stderr.log'
    $godotArgs=@(
        '--path',$ProjectRoot,
        '--scene','Main.tscn',
        '--write-movie',$avi,
        '--fixed-fps',([string]$fps),
        '--quit-after',([string]$frames),
        '--',
        ('--config={0}' -f $request)
    )
    if(-not $NoSound){$godotArgs += ('--audio-output={0}' -f $pcm)}

    $godotExit=Invoke-GodotMovieProcess -FilePath $godotExe -Arguments $godotArgs -WorkingDirectory $ProjectRoot -StdoutPath $stdout -StderrPath $stderr -CommandPath $commandFile
    $godotLogText=Get-Content -Raw -LiteralPath $runLog -Encoding UTF8
    if($godotExit -ne 0){throw "Godot challenge render failed: exit=$godotExit. Diagnostic stage retained: $stage"}
    if($godotLogText -notmatch 'Movie Maker mode enabled'){throw "Godot did not enter Movie Maker mode. Diagnostic stage retained: $stage"}
    if($godotLogText -notmatch 'Done recording movie at path:'){throw "Godot did not report Movie Maker completion. Diagnostic stage retained: $stage"}
    # The actual source AVI is the authority for source resolution. Log text is telemetry only.
    if($godotLogText -notmatch ("recording movie in\s+540.*960\s+@\s+"+[regex]::Escape([string]$fps)+" FPS")){
        Write-Warning "Godot source-resolution telemetry could not be matched textually; FFprobe will be authoritative. Diagnostic stage retained: $stage"
    }
    if($godotLogText -match 'CHALLENGE_INVALID'){throw "GeneradorMaestro rejected the challenge configuration. Diagnostic stage retained: $stage"}
    if($godotLogText -match '\[ERROR_JSON\]'){throw "Godot emitted [ERROR_JSON]. Diagnostic stage retained: $stage"}
    if(-not(Test-Path -LiteralPath $avi -PathType Leaf)){throw "Movie Maker did not create source AVI: $avi. Diagnostic stage retained: $stage"}

    $aviProbe=Invoke-FFProbe $avi
    $avis=@($aviProbe.streams)|Select-Object -First 1
    if([int]$avis.width -ne $sourceWidth -or [int]$avis.height -ne $sourceHeight){throw "Source AVI resolution mismatch: $($avis.width)x$($avis.height); expected ${sourceWidth}x${sourceHeight}. Diagnostic stage retained: $stage"}
    if([string]$avis.r_frame_rate -ne ("{0}/1" -f $fps)){throw "Source AVI FPS mismatch: $($avis.r_frame_rate); expected ${fps}/1. Diagnostic stage retained: $stage"}
    if([int]$avis.nb_read_frames -ne $frames){throw "Source AVI frame mismatch: $($avis.nb_read_frames); expected $frames. Diagnostic stage retained: $stage"}

    # Build FFmpeg inputs first; raw C7 PCM must be declared before its -i.
    $ff=@('-y','-hide_banner','-loglevel','error','-i',$avi)
    $hasAudio=(-not $NoSound -and (Test-Path -LiteralPath $pcm -PathType Leaf))
    if($hasAudio){
        $ff += @('-f','s16le','-ar','44100','-ac','1','-i',$pcm,'-map','0:v:0','-map','1:a:0')
    }else{
        $ff += @('-map','0:v:0','-an')
    }
    $ff += @(
        '-vf',("scale={0}:{1}:flags=lanczos" -f $width,$height),
        '-c:v','libx264','-preset','fast','-crf','18','-profile:v','high','-pix_fmt','yuv420p',
        '-g',([string]$gop),'-keyint_min',([string]$gop),'-sc_threshold','0','-flags','+cgop',
        '-x264-params',("open_gop=0:keyint=$gop:min-keyint=$gop:scenecut=0"),'-movflags','+faststart'
    )
    if($hasAudio){
        $ff += @('-c:a','aac','-profile:a','aac_low','-b:a','192k','-ar','48000','-ac','2','-shortest')
    }
    $ff += $out
    & ffmpeg @ff
    if($LASTEXITCODE -ne 0){throw "FFmpeg delivery encode failed. Diagnostic stage retained: $stage"}
    if(-not(Test-Path -LiteralPath $out -PathType Leaf)){throw "Final MP4 missing: $out. Diagnostic stage retained: $stage"}

    $probe=(& ffprobe -v error -count_frames -show_streams -show_format -of json -- $out 2>&1)|ConvertFrom-Json
    if($LASTEXITCODE -ne 0){throw "ffprobe failed on final MP4. Diagnostic stage retained: $stage"}
    $streams=@($probe.streams)
    $v=@($streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
    if([int]$v.width -ne $width -or [int]$v.height -ne $height){throw "Final resolution mismatch: $($v.width)x$($v.height); expected ${width}x${height}"}
    if([string]$v.r_frame_rate -ne ("{0}/1" -f $fps)){throw "Final FPS mismatch: $($v.r_frame_rate); expected ${fps}/1"}
    if([int]$v.nb_read_frames -ne $frames){throw "Final frame mismatch: $($v.nb_read_frames); expected $frames"}
    if([string]$v.codec_name -ne 'h264'){throw "Final codec mismatch: $($v.codec_name)"}
    if([string]$v.pix_fmt -notin @('yuv420p','yuvj420p')){throw "Final pixel format is not YUV420-compatible: $($v.pix_fmt)"}
    if([string]$v.field_order -notin @('', 'progressive')){throw "Final video is not progressive: field_order=$($v.field_order)"}
    if($hasAudio){
        $a=@($streams|Where-Object{$_.codec_type -eq 'audio'})|Select-Object -First 1
        if($null -eq $a){throw "Final audio stream missing although C7 audio was requested. Diagnostic stage retained: $stage"}
        if([string]$a.codec_name -ne 'aac'){throw "Final audio codec mismatch: $($a.codec_name)"}
        if([string]$a.sample_rate -ne '48000' -or [int]$a.channels -ne 2){throw "Final audio format mismatch: $($a.sample_rate) Hz / $($a.channels) channels; expected 48000 / 2"}
        if([math]::Abs([double]$v.duration-[double]$a.duration) -gt 0.05){throw "A/V duration mismatch exceeds 50 ms: video=$($v.duration) audio=$($a.duration)"}
    }
    if($profile.Social -and [double]$probe.format.duration -gt [double]$profile.DurationMax){throw "Delivery target duration exceeds profile maximum $($profile.DurationMax)s."}

    if($Force -and(Test-Path -LiteralPath $productRoot -PathType Container)){Remove-Item -LiteralPath $productRoot -Recurse -Force}
    New-Item -ItemType Directory -Force -Path $productRoot | Out-Null
    $productMp4=Join-Path $productRoot "${ChallengeId}_seed_${Seed}.mp4"
    Copy-Item -LiteralPath $out -Destination $productMp4 -Force
    Copy-Item -LiteralPath $request -Destination (Join-Path $productRoot 'challenge_definition_effective.json') -Force
    Copy-Item -LiteralPath $runLog -Destination (Join-Path $productRoot 'godot.log') -Force
    if(Test-Path -LiteralPath $commandFile){Copy-Item -LiteralPath $commandFile -Destination (Join-Path $productRoot 'godot_command.txt') -Force}
    if($KeepAvi){Copy-Item -LiteralPath $avi -Destination (Join-Path $productRoot "${ChallengeId}_seed_${Seed}_source.avi") -Force}
    if($ExportGif){& ffmpeg -y -hide_banner -loglevel error -i $productMp4 -vf 'fps=24,scale=360:640:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96:stats_mode=diff[p];[s1][p]paletteuse=dither=sierra2_4a' -loop 0 (Join-Path $productRoot "${ChallengeId}_seed_${Seed}.gif");if($LASTEXITCODE -ne 0){throw "GIF export failed. Diagnostic stage retained: $stage"}}

    $content=[string]$cfg.content.hook
    $hashtags='#VisualChallenge #GenerativeArt #GodotEngine #ProceduralArt'
    $copy="$content`n`nChallenge $ChallengeId · $($cfg.mechanic)`n`n$hashtags"
    [IO.File]::WriteAllText((Join-Path $productRoot 'social.txt'),("COPY_PASTE_READY:`n"+$copy+"`n`nTITLE:`n$ChallengeId · $($cfg.mechanic)`n`nDESCRIPTION:`n$copy`n`nHASHTAGS:`n$hashtags`n"),(New-Object Text.UTF8Encoding($false)))

    $manifest=[ordered]@{
        schema='C11-C-CHALLENGE-PRODUCTION-V3'
        revision='2.17.8'
        status='CONTRACT_SAFE_ADDITIVE_WRAPPER_PENDING_SMOKE'
        challenge_id=$ChallengeId
        seed=$Seed
        mechanic=$cfg.mechanic
        delivery_profile=$DeliveryProfile
        standard_delivery_profile='MASTER_1080'
        profile_alias=([string]$profile.AliasOf)
        simulation_canvas='1080x1920'
        logical_presentation='540x960'
        source_movie_resolution='540x960'
        delivery_resolution="${width}x${height}"
        delivery_scale_filter=("scale={0}:{1}:flags=lanczos" -f $width,$height)
        physical_resolution="${width}x${height}"
        fps=$fps
        duration_seconds=$total
        frames=$frames
        timing_source='hook_duration+game_duration+(optional)reveal_duration+cta_duration'
        legacy_total_duration_ignored=$true
        gop_seconds=3
        closed_gop_encoder_contract=$true
        video_codec='h264'
        pixel_format='yuv420p'
        audio_present=([bool](@($streams|Where-Object{$_.codec_type -eq 'audio'}).Count))
        product=$productMp4
        source_definition=$source
        asset_paths=$cfg.assets
    }
    [IO.File]::WriteAllText((Join-Path $productRoot 'production_manifest.json'),($manifest|ConvertTo-Json -Depth 30),(New-Object Text.UTF8Encoding($false)))

    $success=$true
    Write-Host "[CHALLENGE] PASS $ChallengeId seed=$Seed -> $productRoot"
    Write-Host "[CHALLENGE] Source  ${sourceWidth}x${sourceHeight} / $frames frames -> Delivery ${width}x${height}"
}
finally{
    if($null -ne $nativeViewportState){try{Exit-ChallengeNativeViewport -State $nativeViewportState}catch{Write-Warning "No se pudo restaurar override.cfg: $($_.Exception.Message)"}}
    if($success){if(Test-Path -LiteralPath $stage){Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue}}
    else{Write-Host "[CHALLENGE] FAILURE DIAGNOSTICS RETAINED: $stage" -ForegroundColor Red}
}
