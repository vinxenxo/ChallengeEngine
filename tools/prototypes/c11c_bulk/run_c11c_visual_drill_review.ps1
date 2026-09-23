param(
    [Parameter(Mandatory=$false)]
    [int[]]$Seeds = @(12345,54321,314159,7770001,998877),
    [switch]$ResetReviewAssets,
    [switch]$RegenerateEnvelopes,
    [switch]$Smoke,
    [switch]$NoSound,
    [Alias("Silent")]
    [switch]$SilentMode
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ReviewRoot=Join-Path $ProjectRoot 'artifacts\prototypes\c11c_visual_drills_review'
$AudioRoot=Join-Path $ReviewRoot '_audio'
$EnvelopeRoot=Join-Path $ReviewRoot '_envelopes'
$MovieCapture=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1'
$AudioGenerator=Join-Path $ProjectRoot 'tools\prototypes\c11c_common\generate_c11c_ambient_audio.py'
$Seeds=@($Seeds | ForEach-Object {[int]$_})
$NoSound = $NoSound -or $SilentMode
$SharedAudioHash = $null
$Drills=@('tracking','saccade','pursuit','peripheral_scan')
$CountdownSeconds=3.0
$MinimumTotalDurationSeconds=20.0
$ExpectedGameplayDurationSeconds=17.0
$ExpectedGameplayFrames=510

if($Smoke){
    if($Seeds.Count -ne 1){throw 'Visual Drill smoke expects exactly one seed.'}
} elseif($Seeds.Count -ne 5){
    throw 'Visual Drill review expects exactly five unique seeds; use -Smoke for a one-seed smoke render.'
}
if(@($Seeds | Sort-Object -Unique).Count -ne $Seeds.Count){throw 'Visual Drill review seeds must be unique.'}
foreach($seed in $Seeds){if($seed -lt 1 -or $seed -gt 2147483646){throw "Seed out of range: $seed"}}

. $MovieCapture

function Invoke-Checked {
    param([Parameter(Mandatory=$true)][string]$Executable,[Parameter(Mandatory=$true)][string[]]$Arguments,[Parameter(Mandatory=$true)][string]$Label)
    Write-Host "[C11-C-DRILL] $Label"
    $process=Start-Process -FilePath $Executable -ArgumentList $Arguments -Wait -PassThru -NoNewWindow
    if($process.ExitCode -ne 0){throw "$Label failed with exit code $($process.ExitCode)"}
}

function Invoke-GodotMovieChecked {
    param(
        [Parameter(Mandatory=$true)][string[]]$Arguments,
        [Parameter(Mandatory=$true)][string]$RunDir,
        [Parameter(Mandatory=$true)][string]$RunId
    )
    $stdoutPath=Join-Path $RunDir 'godot_stdout.log'
    $stderrPath=Join-Path $RunDir 'godot_stderr.log'
    Write-Host "[C11-C-DRILL] Render $RunId"
    $process=Start-Process -FilePath 'godot' -ArgumentList $Arguments -Wait -PassThru -NoNewWindow -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
    $stdout=if(Test-Path -LiteralPath $stdoutPath){Get-Content -Raw -LiteralPath $stdoutPath}else{''}
    $stderr=if(Test-Path -LiteralPath $stderrPath){Get-Content -Raw -LiteralPath $stderrPath}else{''}
    $log=$stdout+"`n"+$stderr
    $fatalPatterns=@(
        'SCRIPT ERROR:',
        'Parse Error:',
        'Compile Error:',
        'ERROR: Failed to load script',
        'Invalid call. Nonexistent function',
        'Nonexistent function',
        'Failed to compile depended scripts'
    )
    foreach($pattern in $fatalPatterns){
        if($log -match [regex]::Escape($pattern)){
            throw "Godot runtime/compile failure for $RunId. See $stdoutPath and $stderrPath. Matched: $pattern"
        }
    }
    if($process.ExitCode -ne 0){throw "Godot render failed for $RunId with exit code $($process.ExitCode)"}
    if($log -notmatch '\[VISUAL_CONTENT_PLAYER\] Ready \[visual_drill/') {
        throw "Godot render for $RunId never reached VisualContentPlayer READY state. See $stdoutPath and $stderrPath."
    }
}

function Get-FileSha256Hex {
    param([Parameter(Mandatory=$true)][string]$Path)
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Wait-ForStableFile {
    param([Parameter(Mandatory=$true)][string]$Path,[Parameter(Mandatory=$true)][string]$Label,[int]$TimeoutSeconds=90)
    $deadline=(Get-Date).AddSeconds($TimeoutSeconds)
    $lastSize=-1L; $stableSamples=0
    while((Get-Date) -lt $deadline){
        if(Test-Path -LiteralPath $Path){
            $item=Get-Item -LiteralPath $Path
            $size=[int64]$item.Length
            if($size -gt 0){
                if($size -eq $lastSize){$stableSamples++} else {$stableSamples=0;$lastSize=$size}
                if($stableSamples -ge 2){return}
            }
        }
        Start-Sleep -Milliseconds 400
    }
    throw "$Label was not stable within ${TimeoutSeconds}s: $Path"
}

function Get-VideoProbe {
    param([Parameter(Mandatory=$true)][string]$Path)
    $json=& ffprobe -v error -show_streams -show_format -of json $Path
    if($LASTEXITCODE -ne 0){throw "ffprobe failed for $Path"}
    return ($json -join "`n") | ConvertFrom-Json
}

function Convert-Mp4VideoOnly {
    param([Parameter(Mandatory=$true)][string]$AviPath,[Parameter(Mandatory=$true)][string]$Mp4Path)
    Invoke-Checked 'ffmpeg' @('-y','-hide_banner','-loglevel','error','-i',$AviPath,'-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',$Mp4Path) "Encode silent video $Mp4Path"
}

function Mux-Audio {
    param([Parameter(Mandatory=$true)][string]$VideoPath,[Parameter(Mandatory=$true)][string]$AudioPath,[Parameter(Mandatory=$true)][string]$OutputPath)
    Invoke-Checked 'ffmpeg' @('-y','-hide_banner','-loglevel','error','-i',$VideoPath,'-stream_loop','-1','-i',$AudioPath,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','128k','-ar','44100','-ac','2','-shortest','-movflags','+faststart',$OutputPath) "Mux shared ambient master $OutputPath"
}

function Assert-FinalContract {
    param([Parameter(Mandatory=$true)][string]$Path,[Parameter(Mandatory=$true)][int]$ExpectedFrames,[Parameter(Mandatory=$true)][double]$ExpectedDuration,[Parameter(Mandatory=$true)][bool]$ExpectedAudio)
    Wait-ForStableFile -Path $Path -Label "Final artifact $Path"
    $probe=Get-VideoProbe -Path $Path
    if((Get-Item -LiteralPath $Path).Length -lt 4096){throw "Final artifact is suspiciously small/empty: $Path"}
    $video=@($probe.streams | Where-Object {$_.codec_type -eq 'video'}) | Select-Object -First 1
    if($null -eq $video){throw "No video stream in $Path"}
    if([int]$video.width -ne 720 -or [int]$video.height -ne 1280){throw "720x1280 contract failed: $Path -> $($video.width)x$($video.height)"}
    if([string]$video.r_frame_rate -ne '30/1'){throw "30 FPS contract failed: $Path -> $($video.r_frame_rate)"}
    if([int]$video.nb_frames -ne $ExpectedFrames){throw "Frame contract failed: $Path -> $($video.nb_frames), expected $ExpectedFrames"}
    $duration=[double]$probe.format.duration
    if([math]::Abs($duration-$ExpectedDuration) -gt 0.05){throw "Duration contract failed: $Path -> $duration, expected ~$ExpectedDuration"}
    $audioCount=@($probe.streams | Where-Object {$_.codec_type -eq 'audio'}).Count
    if($ExpectedAudio -and $audioCount -lt 1){throw "Audio is required but missing: $Path"}
    if(-not $ExpectedAudio -and $audioCount -ne 0){throw "Audio was disabled but is present: $Path"}
    return [ordered]@{codec=[string]$video.codec_name;width=[int]$video.width;height=[int]$video.height;r_frame_rate=[string]$video.r_frame_rate;nb_frames=[int]$video.nb_frames;duration_seconds=$duration;audio_streams=$audioCount}
}

function Export-KeyFrames {
    param([Parameter(Mandatory=$true)][string]$Mp4Path,[Parameter(Mandatory=$true)][string]$RunDir)
	$probe=Get-VideoProbe -Path $Mp4Path
	$video=@($probe.streams | Where-Object {$_.codec_type -eq 'video'}) | Select-Object -First 1
	$availableFrames=[int]$video.nb_frames
	if($availableFrames -lt 1){throw "Cannot derive keyframes: invalid frame count in $Mp4Path"}
	$lastFrame=$availableFrames-1
	$indices=@(0,[int][math]::Floor($lastFrame*0.25),[int][math]::Floor($lastFrame*0.50),[int][math]::Floor($lastFrame*0.75),$lastFrame) | Sort-Object -Unique
	while($indices.Count -lt 5){$indices=@($indices + $lastFrame) | Sort-Object -Unique;if($lastFrame -lt 4){throw "Cannot extract five unique keyframes from $Mp4Path"}}
	$indices=@($indices | Select-Object -First 5)
    $terms=$indices | ForEach-Object {"eq(n\,$($_))"}
    $expr="select='$($terms -join '+')'"
    Invoke-Checked 'ffmpeg' @('-y','-hide_banner','-loglevel','error','-i',$Mp4Path,'-vf',$expr,'-fps_mode','vfr',(Join-Path $RunDir 'frame_%03d.png')) "Extract keyframes $Mp4Path"
    $frames=@(Get-ChildItem -LiteralPath $RunDir -Filter 'frame_*.png' | Sort-Object Name)
    if($frames.Count -ne 5){throw "Expected 5 keyframes, found $($frames.Count) in $RunDir"}
}

function Export-ContactSheet {
    param([Parameter(Mandatory=$true)][string]$RunDir)
    $frames=@(Get-ChildItem -LiteralPath $RunDir -Filter 'frame_*.png' | Sort-Object Name)
    Invoke-Checked 'ffmpeg' @('-y','-hide_banner','-loglevel','error','-i',$frames[0].FullName,'-i',$frames[1].FullName,'-i',$frames[2].FullName,'-i',$frames[3].FullName,'-i',$frames[4].FullName,'-filter_complex','hstack=inputs=5',(Join-Path $RunDir 'contact_sheet.jpg')) "Build contact sheet $RunDir"
}

function Export-Gif {
    param([Parameter(Mandatory=$true)][string]$Mp4Path,[Parameter(Mandatory=$true)][string]$GifPath)
    Invoke-Checked 'ffmpeg' @('-y','-hide_banner','-loglevel','error','-i',$Mp4Path,'-vf','fps=12,scale=360:640:flags=lanczos:force_original_aspect_ratio=decrease,pad=360:640:(ow-iw)/2:(oh-ih)/2','-an',$GifPath) "Build review GIF $GifPath"
}

function Write-SocialSidecar {
    param([Parameter(Mandatory=$true)][string]$Path,[Parameter(Mandatory=$true)][string]$Family,[Parameter(Mandatory=$true)][int]$Seed,[Parameter(Mandatory=$true)][double]$Duration,[Parameter(Mandatory=$true)][int]$Frames,[Parameter(Mandatory=$true)][double]$Countdown,[Parameter(Mandatory=$true)][double]$TotalDuration,[Parameter(Mandatory=$true)][int]$TotalFrames,[Parameter(Mandatory=$true)][string]$AudioMode)
    $display = switch ($Family) {
        'tracking' { 'TRACKING' }
        'saccade' { 'SACCADE' }
        'pursuit' { 'PURSUIT' }
        'peripheral_scan' { 'PERIPHERAL SCAN' }
        default { $Family.ToUpperInvariant() }
    }
    $description = "C11-C Visual Drill / $display. Deterministic procedural visual exercise, seed $Seed. $([math]::Round($Duration,2))s at 30 FPS, with the shared 720x1280 social presentation layer."
    $hashtags = '#VisualDrill #VisualTraining #Perception #ProceduralArt #GenerativeArt #DigitalArt #TechArt'
    $content=@"
TITLE: VISUAL DRILL // $display

DESCRIPTION:
$description

FAMILY: $Family
SEED: $Seed
RESOLUTION: 720x1280
FPS: 30
GAMEPLAY DURATION: $([math]::Round($Duration,2)) s
GAMEPLAY FRAMES: $Frames
COUNTDOWN: $([math]::Round($Countdown,2)) s
TOTAL DURATION: $([math]::Round($TotalDuration,2)) s
TOTAL FRAMES: $TotalFrames
AUDIO: $AudioMode
MATRIX HEADER TRANSITION: ON
SHARED SOCIAL/EDITORIAL LAYOUT: ON

HASHTAGS:
$hashtags

REVIEW SOURCE:
C11-A qualification envelope; seed 12345 uses the deterministic A copy when present.
"@
    [System.IO.File]::WriteAllText($Path,$content,(New-Object System.Text.UTF8Encoding($false)))
}

Write-Host '============================================================'
Write-Host '[C11-C-DRILL] VISUAL DRILL SOCIAL REVIEW — C11-C 2.4.0'
Write-Host ("[C11-C-DRILL] 4 families x $($Seeds.Count) seeds = $($Drills.Count * $Seeds.Count) physical renders")
Write-Host '[C11-C-DRILL] 720x1280 / 30 FPS / 3s countdown + 17s gameplay = 20s total'
Write-Host ("[C11-C-DRILL] Shared editorial layout / Matrix ON / audio ON")
Write-Host '============================================================'

if($ResetReviewAssets -and (Test-Path -LiteralPath $ReviewRoot)){Remove-Item -LiteralPath $ReviewRoot -Recurse -Force}
New-Item -ItemType Directory -Force -Path $ReviewRoot,$AudioRoot,$EnvelopeRoot | Out-Null

$requiredRuns=@()
foreach($family in $Drills){foreach($seed in $Seeds){$requiredRuns += [pscustomobject]@{Family=$family;Seed=$seed;RunId="visual_drill_${family}_seed_${seed}"}}}

function Resolve-SourceEnvelopePath {
    param([Parameter(Mandatory=$true)][string]$Family,[Parameter(Mandatory=$true)][int]$Seed)
    $baseRun = Join-Path $EnvelopeRoot ("visual_drill_${Family}_seed_${Seed}")
    $baseEnvelope = Join-Path $baseRun 'envelope.json'
    if(Test-Path -LiteralPath $baseEnvelope){ return $baseEnvelope }
    return $null
}

function Ensure-RequestedEnvelopes {
    $requestedSeeds = ($Seeds -join ',')
    $env:C11C_DRILL_REVIEW_SEEDS = $requestedSeeds
    $env:C11C_DRILL_REVIEW_ENVELOPE_ROOT = $EnvelopeRoot
    try {
        Invoke-Checked 'godot' @('--headless','--path','.','-s','./tools/prototypes/c11c_bulk/C11CVisualDrillReviewEnvelopeGenerator.gd') 'Generate requested Visual Drill review envelopes'
    } finally {
        Remove-Item Env:C11C_DRILL_REVIEW_SEEDS -ErrorAction SilentlyContinue
        Remove-Item Env:C11C_DRILL_REVIEW_ENVELOPE_ROOT -ErrorAction SilentlyContinue
    }
}

function Test-EnvelopeCompatibility {
    param([Parameter(Mandatory=$true)][string]$Path,[Parameter(Mandatory=$true)][string]$Family)
    try {
        $raw=Get-Content -Raw -LiteralPath $Path
        $json=$raw | ConvertFrom-Json
        if([string]$json.kind -ne 'visual_drill' -or [string]$json.subtype -ne $Family){return $false}
        $payload=$json.payload
        if($null -eq $payload){return $false}
        $duration=[double]$payload.duration
        $fps=[int]$payload.fps
        $frames=[int]$payload.frame_count
        if($fps -ne 30){return $false}
        if([math]::Abs($duration - $ExpectedGameplayDurationSeconds) -gt 0.0001){return $false}
        if($frames -ne $ExpectedGameplayFrames){return $false}
        return $true
    } catch {
        return $false
    }
}

$missing=@($requiredRuns | Where-Object { $null -eq (Resolve-SourceEnvelopePath -Family $_.Family -Seed $_.Seed) })
$incompatible=@($requiredRuns | Where-Object {
    $path=Resolve-SourceEnvelopePath -Family $_.Family -Seed $_.Seed
    $null -ne $path -and -not (Test-EnvelopeCompatibility -Path $path -Family $_.Family)
})
if($RegenerateEnvelopes -or $missing.Count -gt 0 -or $incompatible.Count -gt 0){
    Write-Host '[C11-C-DRILL] Generate request-specific Visual Drill envelopes'
    Ensure-RequestedEnvelopes
}

$missingAfter=@($requiredRuns | Where-Object {
    $path=Resolve-SourceEnvelopePath -Family $_.Family -Seed $_.Seed
    $null -eq $path -or -not (Test-EnvelopeCompatibility -Path $path -Family $_.Family)
})
if($missingAfter.Count -gt 0){throw "Requested Visual Drill envelopes still missing: $($missingAfter.RunId -join ', ')"}

if(-not $NoSound){
    $audioPath=Join-Path $AudioRoot 'global_ambient_master.wav'
    if(Test-Path -LiteralPath $audioPath){Remove-Item -LiteralPath $audioPath -Force}
    Invoke-Checked 'python' @($AudioGenerator,$audioPath,'314159','visual_drill','1','20.0') "Generate one shared ambient master (20s)"
    $SharedAudioHash=Get-FileSha256Hex -Path $audioPath
}

$overrideState=$null
$catalog=@()
try {
    $overrideState=Enter-C11CMovieOverride -ProjectRoot $ProjectRoot -Width 720 -Height 1280
    foreach($family in $Drills){
        $familyRoot=Join-Path $ReviewRoot $family
        New-Item -ItemType Directory -Force -Path $familyRoot | Out-Null
        foreach($seed in $Seeds){
            $runId="visual_drill_${family}_seed_${seed}"
            $envelopePath=Resolve-SourceEnvelopePath -Family $family -Seed $seed
            if(-not(Test-Path -LiteralPath $envelopePath)){throw "Missing envelope: $envelopePath"}
            $envelope=Get-Content -Raw -LiteralPath $envelopePath | ConvertFrom-Json
            if([string]$envelope.kind -ne 'visual_drill' -or [string]$envelope.subtype -ne $family){throw "Unexpected route in $envelopePath"}
            $duration=[double]$envelope.payload.duration
            $fps=[int]$envelope.payload.fps
            $frames=[int]$envelope.payload.frame_count
            if($fps -ne 30){throw "$runId is not 30 FPS: $fps"}
            if([math]::Abs($duration - $ExpectedGameplayDurationSeconds) -gt 0.0001 -or $frames -ne $ExpectedGameplayFrames){throw "$runId must be 17.0s / 510 gameplay frames: got $duration s / $frames frames"}
            $countdownFrames=[int][math]::Round($CountdownSeconds * $fps)
            $totalFrames=$countdownFrames + $frames
            $totalDuration=$CountdownSeconds + $duration
            if($countdownFrames -ne 90 -or $totalFrames -lt 600 -or $totalDuration + 0.0001 -lt $MinimumTotalDurationSeconds){throw "$runId violates 20s presentation contract: countdown=$countdownFrames total_frames=$totalFrames total_duration=$totalDuration"}
            $targetDir=Join-Path $familyRoot "seed_$seed"
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
            Get-ChildItem -LiteralPath $targetDir -File -ErrorAction SilentlyContinue | Remove-Item -Force

            $aviPath=Join-Path $targetDir "VisualDrill_${family}_seed_${seed}.avi"
            $silentMp4=Join-Path $targetDir "VisualDrill_${family}_seed_${seed}_silent.mp4"
            $finalMp4=Join-Path $targetDir "VisualDrill_${family}_seed_${seed}.mp4"
            $gifPath=Join-Path $targetDir "VisualDrill_${family}_seed_${seed}_review.gif"
            $relativeEnvelope=$envelopePath.Substring($ProjectRoot.Length+1).Replace('\','/')

            Invoke-GodotMovieChecked @('--path','.', '--scene','core/presentation/rendering/VisualContentPlayer.tscn', "--definition=$relativeEnvelope", '--write-movie',$aviPath,'--fixed-fps','30','--quit-after',([string]$totalFrames)) -RunDir $targetDir -RunId $runId
            if(-not(Test-Path -LiteralPath $aviPath)){throw "Godot did not create AVI for ${runId}: ${aviPath}"}
            Wait-ForStableFile -Path $aviPath -Label "Movie Maker capture $runId"
            Convert-Mp4VideoOnly -AviPath $aviPath -Mp4Path $silentMp4

            $audioPath=Join-Path $AudioRoot 'global_ambient_master.wav'
            if($NoSound){
                Move-Item -LiteralPath $silentMp4 -Destination $finalMp4 -Force
            } else {
                Mux-Audio -VideoPath $silentMp4 -AudioPath $audioPath -OutputPath $finalMp4
                Remove-Item -LiteralPath $silentMp4 -Force
                if($null -eq $SharedAudioHash){ $SharedAudioHash = Get-FileSha256Hex -Path $audioPath }
                elseif($SharedAudioHash -ne (Get-FileSha256Hex -Path $audioPath)){ throw 'Shared audio master hash changed during review.' }
            }

            $probe=Assert-FinalContract -Path $finalMp4 -ExpectedFrames $totalFrames -ExpectedDuration $totalDuration -ExpectedAudio:(-not $NoSound)
            Export-KeyFrames -Mp4Path $finalMp4 -RunDir $targetDir
            Export-ContactSheet -RunDir $targetDir
            Export-Gif -Mp4Path $finalMp4 -GifPath $gifPath
            Write-SocialSidecar -Path (Join-Path $targetDir "VisualDrill_${family}_seed_${seed}_social.txt") -Family $family -Seed $seed -Duration $duration -Frames $frames -Countdown $CountdownSeconds -TotalDuration $totalDuration -TotalFrames $totalFrames -AudioMode $(if($NoSound){'OFF'}else{'GLOBAL_AMBIENT'})

            $manifest=[ordered]@{
                schema='C11-C-VISUAL-DRILL-REVIEW-V1'
                revision='2.4.0'
                family=$family
                seed=$seed
                route='visual_drill/' + $family
                resolution='720x1280'
                fps=$fps
                duration_seconds=$duration
                gameplay_frame_count=$frames
                countdown_seconds=$CountdownSeconds
                countdown_frames=$countdownFrames
                total_duration_seconds=$totalDuration
                total_frame_count=$totalFrames
                matrix_enabled=$true
                editorial_layout='shared_c11c_social'
                audio_mode=$(if($NoSound){'OFF'}else{'GLOBAL_AMBIENT_MASTER'})
                audio_master_sha256=$(if($NoSound){$null}else{$SharedAudioHash})
                source_envelope=$envelopePath
                final_mp4=$finalMp4
                gif=$gifPath
                contact_sheet=(Join-Path $targetDir 'contact_sheet.jpg')
                keyframes=@(Get-ChildItem -LiteralPath $targetDir -Filter 'frame_*.png' | Sort-Object Name | Select-Object -ExpandProperty Name)
                ffprobe=$probe
                hashes=[ordered]@{mp4_sha256=(Get-FileSha256Hex $finalMp4);envelope_sha256=(Get-FileSha256Hex $envelopePath)}
            }
            $manifestPath=Join-Path $targetDir "VisualDrill_${family}_seed_${seed}_manifest.json"
            [System.IO.File]::WriteAllText($manifestPath,($manifest|ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))
            $catalog += [pscustomobject]@{family=$family;seed=$seed;path=$finalMp4;status='PASS'}
            Write-Host "[C11-C-DRILL] PASS $runId -> 720x1280 / $frames frames / $duration s"
        }
    }
} finally {
    if($null -ne $overrideState){Exit-C11CMovieOverride -State $overrideState}
}

$rootManifest=[ordered]@{
    schema='C11-C-VISUAL-DRILL-REVIEW-CATALOG-V1'
    revision='2.4.0'
    status='COMPLETE'
    family_count=$Drills.Count
    seed_count=$Seeds.Count
    render_count=$catalog.Count
    countdown_seconds=$CountdownSeconds
    gameplay_seconds=$ExpectedGameplayDurationSeconds
    total_seconds=$MinimumTotalDurationSeconds
    gameplay_frames=$ExpectedGameplayFrames
    countdown_frames=90
    total_frames=600
    seeds=@($Seeds)
    families=@($Drills)
    delivery='720x1280 / 9:16 / 30 FPS'
    logical_social_frame='540x960 with Header 0..144, Body 144..816, Footer 816..960'
    matrix_enabled=$true
    audio_mode=$(if($NoSound){'OFF'}else{'GLOBAL_AMBIENT_MASTER'})
    audio_master_sha256=$(if($NoSound){$null}else{$SharedAudioHash})
    source_envelope_root=$EnvelopeRoot
    review_root=$ReviewRoot
    cleanup_performed=$false
    results=$catalog
}
[System.IO.File]::WriteAllText((Join-Path $ReviewRoot 'C11-C_VISUAL_DRILL_REVIEW_CATALOG.json'),($rootManifest|ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))
Write-Host "[C11-C-DRILL] COMPLETE renders=$($catalog.Count) root=$ReviewRoot"
return
