param(
    [int]$Seed = 314159,
    [switch]$NoFooter,
    [string]$Grammar = '',
    [ValidateRange(20.0,23.0)]
    [double]$Duration = 0.0,
    [Alias('Silent')]
    [switch]$NoSound,
    [switch]$ExportGif,
    [switch]$KeepAvi,
    [string]$OutputRoot = ''
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$env:C11C_SEED = [string]$Seed
if ([string]::IsNullOrWhiteSpace($Grammar)) {
    Remove-Item Env:C11C_VISUAL_GRAMMAR -ErrorAction SilentlyContinue
} else {
    $env:C11C_VISUAL_GRAMMAR = $Grammar
}
$env:C11C_SHOW_FOOTER = if ($NoFooter) { '0' } else { '1' }
$env:C11C_SOUND_ENABLED = if ($NoSound) { '0' } else { '1' }
if($Duration -gt 0){ $env:C11C_DURATION_SECONDS = $Duration.ToString([System.Globalization.CultureInfo]::InvariantCulture) } else { Remove-Item Env:C11C_DURATION_SECONDS -ErrorAction SilentlyContinue }
if([string]::IsNullOrWhiteSpace($OutputRoot)){ $ArtifactRoot = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_invisible_forces_v1' } else { $ArtifactRoot = [System.IO.Path]::GetFullPath($OutputRoot) }
$Stem = "InvisibleForces_v1_seed_${Seed}"
$Avi = if($KeepAvi) { Join-Path $ArtifactRoot ($Stem + '.avi') } else { Join-Path ([System.IO.Path]::GetTempPath()) ($Stem + '_' + [Guid]::NewGuid().ToString('N') + '.avi') }
$LegacyMp4Silent = Join-Path $ArtifactRoot ($Stem + '_silent.mp4')
$TempSilent = Join-Path ([System.IO.Path]::GetTempPath()) ('C11C_' + $Stem + '_silent.mp4')
$Mp4 = Join-Path $ArtifactRoot ($Stem + '.mp4')
$Gif = Join-Path $ArtifactRoot ($Stem + '.gif')
$Probe = Join-Path $ArtifactRoot ($Stem + '_ffprobe.json')
$Audio = Join-Path $ArtifactRoot ($Stem + '_music.wav')
$AudioScript = Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CSafeAmbient.py'
$GodotLog = Join-Path $ArtifactRoot ($Stem + '_godot.log')
$MovieCaptureHelper = Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CMovieCapture.ps1'
$Manifest = Join-Path $ArtifactRoot ($Stem + '_manifest.json')
$Authoring = Join-Path $ArtifactRoot ($Stem + '_authoring.json')
$Social = Join-Path $ArtifactRoot ($Stem + '_social.txt')

New-Item -ItemType Directory -Force -Path $ArtifactRoot | Out-Null
foreach ($p in @($Avi,$LegacyMp4Silent,$Mp4,$Probe,$Audio,$GodotLog,$Manifest,$Authoring,$Social,$TempSilent,$Gif)) {
    if (Test-Path -LiteralPath $p) { Remove-Item -Force -LiteralPath $p }
}

$movieOverride = $null
Push-Location $ProjectRoot
try {
    . $MovieCaptureHelper
    $movieOverride = Enter-C11CMovieOverride -ProjectRoot $ProjectRoot -Width 720 -Height 1280
    Write-Host '[C11C-RESOLUTION] Movie Maker override active: 720x1280'
    $DeliveryResolution='720x1280'
    $godotArgs=@('--path','.','--scene','tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.tscn','--write-movie',$Avi,'--fixed-fps','30','--resolution',$DeliveryResolution,'--quit-after','900')
    # Windows PowerShell 5.1 can promote native stderr (including non-fatal Godot warnings)
    # to NativeCommandError when $ErrorActionPreference='Stop'. Keep stderr visible in the log
    # without aborting the export; the real process exit code is still validated below.
    $nativeEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        & godot @godotArgs 2>&1 | Tee-Object -FilePath $GodotLog
        $godotExit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $nativeEap
    }
    if ($godotExit -ne 0) { throw "Godot prototype export failed: exit=$godotExit" }
    # Prototype scenes still write their authoring snapshot under the canonical project artifact path.
    # When OutputRoot is overridden for an extraordinary review, mirror that snapshot into the requested root.
    if(-not (Test-Path -LiteralPath $Authoring)){
        $canonicalAuthoring=Join-Path $ProjectRoot ('artifacts\prototypes\c11c_invisible_forces_v1\' + ($Stem + '_authoring.json'))
        if(Test-Path -LiteralPath $canonicalAuthoring){ Copy-Item -LiteralPath $canonicalAuthoring -Destination $Authoring -Force }
    }
    $errors = Select-String -Path $GodotLog -Pattern 'SHADER ERROR|Shader compilation failed|SCRIPT ERROR|Parse Error|ERROR:' -SimpleMatch:$false
    if ($errors) { throw "Godot reported prototype errors. See: $GodotLog" }
    $captureLine = Select-String -Path $GodotLog -Pattern 'recording movie in\s+720[^\r\n]*1280\s+@\s+30\s+FPS' -SimpleMatch:$false
    if (-not $captureLine) { throw "Movie Maker resolution contract failed. Expected 720x1280 in Godot log: $GodotLog" }
    if (-not (Test-Path -LiteralPath $Avi)) { throw "Godot finished without creating AVI: $Avi" }
    if ((Get-Item -LiteralPath $Avi).Length -le 0) { throw 'Generated AVI is empty.' }

    $authorForAudio = Get-Content -Raw $Authoring | ConvertFrom-Json
    $loopCycles = [int][math]::Round([double]$authorForAudio.loop_cycles)
    $DurationSeconds = [double]$authorForAudio.duration_seconds
    $FrameCount = [int]$authorForAudio.frame_count
    $audioGrammar = [string]$authorForAudio.grammar
    $audioProfile = [string]$authorForAudio.audio_profile

    if (-not $NoSound) {
        & python $AudioScript $Audio $Seed $loopCycles $DurationSeconds 'invisible_forces' 'loop' $audioGrammar
        if ($LASTEXITCODE -ne 0) { throw "Music generation failed: exit=$LASTEXITCODE" }
        if (-not (Test-Path -LiteralPath $Audio)) { throw 'Music WAV missing.' }
    }

    if ($NoSound) {
        & ffmpeg -y -hide_banner -loglevel error -i $Avi -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -movflags +faststart $Mp4
        if ($LASTEXITCODE -ne 0) { throw "Silent MP4 packaging failed: exit=$LASTEXITCODE" }
    } else {
        & ffmpeg -y -hide_banner -loglevel error -i $Avi -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -movflags +faststart $TempSilent
        if ($LASTEXITCODE -ne 0) { throw "Intermediate silent MP4 packaging failed: exit=$LASTEXITCODE" }
        & ffmpeg -y -hide_banner -loglevel error -i $TempSilent -i $Audio -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 -shortest -movflags +faststart $Mp4
        if ($LASTEXITCODE -ne 0) { throw "Audio mux failed: exit=$LASTEXITCODE" }
    }
    if($ExportGif) {
        & ffmpeg -y -hide_banner -loglevel error -i $Mp4 -vf 'fps=24,scale=360:640:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96:stats_mode=diff[p];[s1][p]paletteuse=dither=sierra2_4a' -loop 0 $Gif
        if ($LASTEXITCODE -ne 0) { throw "GIF packaging failed: exit=$LASTEXITCODE" }
    }

    & ffprobe -v error -show_entries format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels -of json $Mp4 | Set-Content -Encoding UTF8 $Probe
    if ($LASTEXITCODE -ne 0) { throw "FFprobe validation failed: exit=$LASTEXITCODE" }

    $probe = Get-Content -Raw $Probe | ConvertFrom-Json
    $video = $probe.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
    $audioStream = $probe.streams | Where-Object { $_.codec_type -eq 'audio' } | Select-Object -First 1
    if (-not $video) { throw 'Final MP4 has no video stream.' }
    if ((-not $NoSound) -and (-not $audioStream)) { throw 'Final MP4 has no audio stream.' }
    if ([int]$video.width -ne 720) { throw "Width contract failed: $($video.width)" }
    if ([int]$video.height -ne 1280) { throw "Height contract failed: $($video.height)" }
    if ([string]$video.r_frame_rate -ne '30/1') { throw "FPS contract failed: $($video.r_frame_rate)" }
    if ([int]$video.nb_frames -ne $FrameCount) { throw "Frame count contract failed: $($video.nb_frames), expected $FrameCount" }
    if ([math]::Abs([double]$video.duration - $DurationSeconds) -gt 0.05) { throw "Video duration contract failed: $($video.duration), expected $DurationSeconds" }
    if (-not $NoSound) {
        if ([int]$audioStream.sample_rate -ne 44100) { throw "Audio rate contract failed: $($audioStream.sample_rate)" }
        if ([int]$audioStream.channels -ne 2) { throw "Audio channel contract failed: $($audioStream.channels)" }
    }

    $author = Get-Content -Raw $Authoring | ConvertFrom-Json
    $repro = '.\tools\prototypes\c11c_invisible_forces_v1\run_prototype.ps1 -Seed ' + [string]$Seed
    if (-not [string]::IsNullOrWhiteSpace($Grammar)) { $repro += ' -Grammar "' + $Grammar + '"' }
    $repro += ' -Duration ' + $DurationSeconds.ToString([System.Globalization.CultureInfo]::InvariantCulture)
    if ($NoFooter) { $repro += ' -NoFooter' }
    if ($NoSound) { $repro += ' -NoSound' }
    if ($ExportGif) { $repro += ' -ExportGif' }
    if ($KeepAvi) { $repro += ' -KeepAvi' }
    if (-not [string]::IsNullOrWhiteSpace($OutputRoot)) { $repro += ' -OutputRoot "' + $OutputRoot + '"' }
    $manifestObject = [ordered]@{
        prototype_id = 'C11-C.5_INVISIBLE_FORCES_V1'
        revision = '2.15.0'
        status = 'EDITORIAL_AUDIO_LOOP_REVIEW'
        seed = $Seed
        family_id = $author.family_id
        technical_id = 'vector_field'
        artistic_name = 'Invisible Forces'
        production_id = 'c11c_invisible_forces_v1'
        runtime_id = 'invisible_forces'
        display_name = $author.display_name
        grammar_id = $author.grammar_id
        grammar = $author.grammar
        palette = $author.palette
        visual = [ordered]@{
            canvas = '720x1280'
            body = 'y=192..1088'
            duration_seconds = $DurationSeconds
            fps = 30
            frame_count = $FrameCount
            loop_cycles = [double]$author.loop_cycles
            loop_closed = $true
            background = '05070B'
            footer_enabled = -not $NoFooter
        }
        editorial = [ordered]@{
            header_line_1 = $author.header_math
            header_line_2 = $author.header_primary
            header_secondary = $author.header_secondary
            matrix_transition = $true
            footer = 'generation telemetry / prototype QA'
        }
        audio = [ordered]@{
            mode = 'FAMILY_MUSIC_V4'
            profile_id = $author.audio_profile
            style = $author.audio_style
            semantic_key = $audioGrammar
            sample_rate = 44100
            channels = 2
            duration_seconds = $DurationSeconds
            muxed_into_mp4 = -not $NoSound
            enabled = -not $NoSound
            C7_modified = $false
            family_grammar_bound = $true
        }
        typography = [ordered]@{
            header = 'Inter Bold'
            footer = 'Noto Sans Mono Regular'
            license = 'SIL Open Font License 1.1'
        }
        social_metadata = [System.IO.Path]::GetFileName($Social)
        artifact_policy = [ordered]@{ export_gif = [bool]$ExportGif; keep_avi = [bool]$KeepAvi; avi_intermediate = [bool](-not $KeepAvi); output_root = $ArtifactRoot }
        reproduction_command = $repro
        technobabble = $author.technobabble
        frozen_boundaries_modified = $false
    }
    $manifestJson = $manifestObject | ConvertTo-Json -Depth 12
    [System.IO.File]::WriteAllText($Manifest, $manifestJson, (New-Object System.Text.UTF8Encoding($false)))

    & python (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\write_social_metadata.py') --manifest $Manifest --command $repro --output $Social
    if ($LASTEXITCODE -ne 0) { throw "Social metadata generation failed: exit=$LASTEXITCODE" }
    if (-not (Test-Path -LiteralPath $Social)) { throw "Social sidecar was not created: $Social" }
    if ((Get-Item -LiteralPath $Social).Length -lt 100) { throw "Social sidecar is unexpectedly small: $Social" }

    Write-Host "[C11-C-2.15.0] PASS - 720x1280 / 30 FPS / $FrameCount frames / $DurationSeconds s / AUDIO=$(-not $NoSound) / LOOP / EDITORIAL"
    Write-Host ("[C11-C-2.13.0] MP4: " + $Mp4)
    if($ExportGif){ Write-Host ("[C11-C-2.15.0] GIF: " + $Gif) }
    Write-Host ("[C11-C-2.13.0] AUDIO: " + $Audio)
    Write-Host ("[C11-C-2.13.0] SOCIAL: " + $Social)
} finally {
    if ($null -ne $movieOverride) {
        Exit-C11CMovieOverride -State $movieOverride
    }
    if (Test-Path -LiteralPath $TempSilent) {
        Remove-Item -Force -LiteralPath $TempSilent -ErrorAction SilentlyContinue
    }
    if (Test-Path -LiteralPath $LegacyMp4Silent) {
        Remove-Item -Force -LiteralPath $LegacyMp4Silent -ErrorAction SilentlyContinue
    }
    # AVI is an intermediate capture. Retain only when explicitly requested with -KeepAvi.
    if (-not $KeepAvi -and (Test-Path -LiteralPath $Avi)) {
        Remove-Item -Force -LiteralPath $Avi -ErrorAction SilentlyContinue
    }
    Pop-Location
}
