param(
    [Parameter(Mandatory=$true)]
    [int[]]$Seeds
)
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$families=@('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')
$stemMap=@{
    c11c_geometric_waves_v1='GeometricWaves_v1'; c11c_fractal_bloom_v1='FractalBloom_v1';
    c11c_sacred_symmetry_v1='SacredSymmetry_v1'; c11c_living_particles_v1='LivingParticles_v1';
    c11c_invisible_forces_v1='InvisibleForces_v1'
}
if($Seeds.Count -lt 1){throw 'At least one seed is required.'}
foreach($seed in $Seeds){if($seed -lt 1 -or $seed -gt 2147483646){throw "Seed out of range: $seed"}}
$root=Join-Path $ProjectRoot 'artifacts\prototypes\c11c_bulk_multiseed'
New-Item -ItemType Directory -Force -Path $root | Out-Null
$results=@()
foreach($family in $families){
    $launcher=Join-Path $ProjectRoot ("tools\prototypes\$family\run_prototype.ps1")
    if(-not(Test-Path -LiteralPath $launcher)){throw "Missing launcher: $launcher"}
    foreach($seed in $Seeds){
        Write-Host "[C11-C-MULTISEED] START family=$family seed=$seed"
        try {
            $launcherParams=@{Seed=[int]$seed}
            & $launcher @launcherParams
            if(-not $?) { throw "Launcher returned failure: $launcher" }
        } catch { throw "Multi-seed run failed for ${family} seed=${seed}: $($_.Exception.Message)" }
        $artifactDir=Join-Path $ProjectRoot ("artifacts\prototypes\$family")
        $stem="$($stemMap[$family])_seed_$seed"
        $mp4=Join-Path $artifactDir "$stem.mp4"
        $probePath=Join-Path $artifactDir "${stem}_ffprobe.json"
        $social=Join-Path $artifactDir "${stem}_social.txt"
        foreach($required in @($mp4,$probePath,$social)){if(-not(Test-Path -LiteralPath $required)){throw "Missing artifact after successful launcher: $required"}}
        $probe=Get-Content -Raw $probePath | ConvertFrom-Json
        $video=$probe.streams | Where-Object {$_.codec_type -eq 'video'} | Select-Object -First 1
        if(-not $video){throw "No video stream in probe: $probePath"}
        if([int]$video.width -ne 720 -or [int]$video.height -ne 1280){throw "Delivery resolution contract failed for ${family} seed=${seed}: $($video.width)x$($video.height)"}
        if([string]$video.r_frame_rate -ne '30/1'){throw "FPS contract failed for ${family} seed=${seed}: $($video.r_frame_rate)"}
        $duration=[double]$video.duration
        if($duration -lt 20.0 -or $duration -gt 30.0){throw "Duration contract failed for ${family} seed=${seed}: $duration (expected 20..30s)"}
        $expectedFrames=[int][math]::Round($duration * 30.0)
        if([int]$video.nb_frames -ne $expectedFrames){throw "Frame count contract failed for ${family} seed=${seed}: $($video.nb_frames), expected $expectedFrames"}
        $results += [ordered]@{family=$family;seed=$seed;status='PASS';mp4=$mp4;duration_seconds=$duration;frame_count=$expectedFrames}
        Write-Host "[C11-C-MULTISEED] PASS family=$family seed=$seed 720x1280 / 30 FPS / $expectedFrames frames / $duration s"
    }
}
$manifest=[ordered]@{schema='C11-C-MULTISEED-BULK-V2';revision='2.13.0';status='COMPLETE';seeds=@($Seeds);family_count=$families.Count;seed_count=$Seeds.Count;render_count=$families.Count*$Seeds.Count;results=$results;visual_contract=[ordered]@{canvas='720x1280';body='y=192..1088';fps=30;duration_seconds='20..30 policy-driven';frames='round(duration_seconds*30)'};audio_contract='default ON; safe mobile ambient; -NoSound/-Silent disables audio';frozen_boundaries_modified=$false}
$manifestPath=Join-Path $root 'C11-C_MULTISEED_BULK_MANIFEST.json'
[System.IO.File]::WriteAllText($manifestPath,($manifest|ConvertTo-Json -Depth 10),(New-Object System.Text.UTF8Encoding($false)))
Write-Host "[C11-C-MULTISEED] COMPLETE renders=$($families.Count*$Seeds.Count) manifest=$manifestPath"
return
