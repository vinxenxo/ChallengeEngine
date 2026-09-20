param([int]$Seed = 314159)

$ErrorActionPreference = 'Stop'

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$env:C11C_SEED = [string]$Seed
$ArtifactRoot = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_geometric_waves_v1'
$Avi = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}.avi"
$Mp4Silent = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}_silent.mp4"
$Mp4 = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}.mp4"
$Gif = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}.gif"
$Probe = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}_ffprobe.json"
$Audio = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}_music.wav"
$AudioScript = Join-Path $PSScriptRoot 'generate_geometric_waves_music.py'
$GodotLog = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}_godot.log"
$Manifest = Join-Path $ArtifactRoot "GeometricWaves_v1_seed_${Seed}_manifest.json"

New-Item -ItemType Directory -Force -Path $ArtifactRoot | Out-Null
foreach ($p in @($Avi, $Mp4Silent, $Mp4, $Gif, $Probe, $Audio, $GodotLog, $Manifest)) {
    if (Test-Path -LiteralPath $p) { Remove-Item -Force -LiteralPath $p }
}

Push-Location $ProjectRoot
try {
    # 1) Physical visual render.
    & godot --path . --scene tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.tscn `
        --write-movie $Avi `
        --fixed-fps 30 `
        --quit-after 300 2>&1 | Tee-Object -FilePath $GodotLog
    $godotExit = $LASTEXITCODE
    if ($godotExit -ne 0) { throw "Godot prototype export failed: exit=$godotExit" }

    $shaderErrors = Select-String -Path $GodotLog -Pattern 'SHADER ERROR|Shader compilation failed' -SimpleMatch:$false
    if ($shaderErrors) {
        throw "Godot reported shader compilation errors. See: $GodotLog"
    }

    if (-not (Test-Path -LiteralPath $Avi)) {
        throw "Godot finished without creating the expected AVI: $Avi"
    }
    if ((Get-Item -LiteralPath $Avi).Length -le 0) {
        throw "Godot created an empty AVI: $Avi"
    }

    # 2) Procedural deterministic music bed. Prototype-only; C7 remains untouched.
    & python $AudioScript $Audio $Seed
    if ($LASTEXITCODE -ne 0) { throw "Procedural music generation failed: exit=$LASTEXITCODE" }
    if (-not (Test-Path -LiteralPath $Audio)) { throw "Music WAV missing: $Audio" }
    if ((Get-Item -LiteralPath $Audio).Length -le 0) { throw "Music WAV is empty: $Audio" }

    # 3) Video-only encode first, preserving the verified visual stream.
    & ffmpeg -y -hide_banner -loglevel error `
        -i $Avi `
        -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -movflags +faststart `
        $Mp4Silent
    if ($LASTEXITCODE -ne 0) { throw "FFmpeg silent MP4 packaging failed: exit=$LASTEXITCODE" }

    # 4) Mux prototype music into the final product MP4.
    & ffmpeg -y -hide_banner -loglevel error `
        -i $Mp4Silent -i $Audio `
        -map 0:v:0 -map 1:a:0 `
        -c:v copy -c:a aac -b:a 192k -ar 44100 -ac 2 -shortest -movflags +faststart `
        $Mp4
    if ($LASTEXITCODE -ne 0) { throw "FFmpeg audio mux failed: exit=$LASTEXITCODE" }

    # 5) GIF preview remains intentionally silent.
    & ffmpeg -y -hide_banner -loglevel error `
        -i $Mp4 `
        -vf "fps=30,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256[p];[s1][p]paletteuse=dither=sierra2_4a" `
        -loop 0 `
        $Gif
    if ($LASTEXITCODE -ne 0) { throw "FFmpeg GIF packaging failed: exit=$LASTEXITCODE" }

    # 6) Final A/V probe.
    & ffprobe -v error `
        -show_entries format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,nb_frames,duration,sample_rate,channels `
        -of json `
        $Mp4 | Set-Content -Encoding UTF8 $Probe
    if ($LASTEXITCODE -ne 0) { throw "FFprobe validation failed: exit=$LASTEXITCODE" }

    $probe = Get-Content -Raw $Probe | ConvertFrom-Json
    $video = $probe.streams | Where-Object { $_.codec_type -eq 'video' } | Select-Object -First 1
    $audioStream = $probe.streams | Where-Object { $_.codec_type -eq 'audio' } | Select-Object -First 1
    if (-not $video) { throw 'Final MP4 has no video stream.' }
    if (-not $audioStream) { throw 'Final MP4 has no audio stream.' }
    if ([int]$video.width -ne 540) { throw "Width contract failed: $($video.width)" }
    if ([int]$video.height -ne 960) { throw "Height contract failed: $($video.height)" }
    if ([string]$video.r_frame_rate -ne '30/1') { throw "FPS contract failed: $($video.r_frame_rate)" }
    if ([int]$video.nb_frames -ne 300) { throw "Frame count contract failed: $($video.nb_frames)" }
    if ([math]::Abs([double]$video.duration - 10.0) -gt 0.05) { throw "Video duration contract failed: $($video.duration)" }
    if ([int]$audioStream.sample_rate -ne 44100) { throw "Audio sample-rate contract failed: $($audioStream.sample_rate)" }
    if ([int]$audioStream.channels -ne 2) { throw "Audio channel contract failed: $($audioStream.channels)" }

    $manifestObject = [ordered]@{
        prototype_id = 'C11-C.1_GEOMETRIC_WAVES_V1'
        revision = '1.0.2'
        status = 'PROTOTYPE_ONLY'
        seed = $Seed
        visual = [ordered]@{
            canvas = '540x960'
            body = 'y=144..816'
            duration_seconds = 10.0
            fps = 30
            frame_count = 300
        }
        editorial = [ordered]@{
            header = 'CUANDO LAS ONDAS DIBUJAN GEOMETRIA'
            footer = '(t)=2f/300  N=6  LISS 8:5  3 LAYERS  SEED $Seed'
        }
        audio = [ordered]@{
            mode = 'prototype_procedural_music'
            deterministic = $true
            source_script = 'generate_geometric_waves_music.py'
            sample_rate = 44100
            channels = 2
            duration_seconds = 10.0
            muxed_into_mp4 = $true
            C7_modified = $false
        }
        frozen_boundaries_modified = $false
    }
    $manifestObject | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 $Manifest

    Remove-Item -Force -LiteralPath $Mp4Silent
    Write-Host '[C11-C.1] PHYSICAL PROTOTYPE PASS - 540x960 / 30 FPS / 300 frames / ~10.0 s + AUDIO'
    Write-Host "[C11-C.1] MP4: $Mp4"
    Write-Host "[C11-C.1] GIF: $Gif"
    Write-Host "[C11-C.1] AUDIO: $Audio"
} finally {
    Pop-Location
}
