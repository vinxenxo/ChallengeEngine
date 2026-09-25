param(
    [switch]$ResetReviewAssets
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$Root = Join-Path $ProjectRoot 'artifacts\prototypes\c11c_subtype_music_coverage'
if ($ResetReviewAssets -and (Test-Path -LiteralPath $Root)) { Remove-Item -LiteralPath $Root -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Root | Out-Null

# Exactly one seed per authored grammar/subtype.
$cases = @(
    @{ Family='geometric'; Production='c11c_geometric_waves_v1'; Seed=1;  Grammar='harmonic_membrane' },
    @{ Family='geometric'; Production='c11c_geometric_waves_v1'; Seed=2;  Grammar='lattice_wave' },
    @{ Family='geometric'; Production='c11c_geometric_waves_v1'; Seed=4;  Grammar='parametric_ribbon' },
    @{ Family='geometric'; Production='c11c_geometric_waves_v1'; Seed=7;  Grammar='interference_plane' },
    @{ Family='geometric'; Production='c11c_geometric_waves_v1'; Seed=30; Grammar='orbital_wave' },
    @{ Family='fractal'; Production='c11c_fractal_bloom_v1'; Seed=7; Grammar='radial_bloom' },
    @{ Family='fractal'; Production='c11c_fractal_bloom_v1'; Seed=1; Grammar='dendritic_tunnel' },
    @{ Family='fractal'; Production='c11c_fractal_bloom_v1'; Seed=3; Grammar='spiral_fractal' },
    @{ Family='fractal'; Production='c11c_fractal_bloom_v1'; Seed=2; Grammar='fractal_filigree' },
    @{ Family='fractal'; Production='c11c_fractal_bloom_v1'; Seed=4; Grammar='nested_worlds' },
    @{ Family='sacred_symmetry'; Production='c11c_sacred_symmetry_v1'; Seed=314159; Grammar='astrolabe' },
    @{ Family='sacred_symmetry'; Production='c11c_sacred_symmetry_v1'; Seed=8675309; Grammar='gear_train' },
    @{ Family='sacred_symmetry'; Production='c11c_sacred_symmetry_v1'; Seed=577215; Grammar='polygon_orrery' },
    @{ Family='sacred_symmetry'; Production='c11c_sacred_symmetry_v1'; Seed=161803; Grammar='origami_mandala' },
    @{ Family='sacred_symmetry'; Production='c11c_sacred_symmetry_v1'; Seed=271828; Grammar='celestial_chart' },
    @{ Family='living_particles'; Production='c11c_living_particles_v1'; Seed=424242; Grammar='swarm' },
    @{ Family='living_particles'; Production='c11c_living_particles_v1'; Seed=112358; Grammar='vortex' },
    @{ Family='living_particles'; Production='c11c_living_particles_v1'; Seed=161803; Grammar='collision_cloud' },
    @{ Family='living_particles'; Production='c11c_living_particles_v1'; Seed=314159; Grammar='organic_pulse' },
    @{ Family='living_particles'; Production='c11c_living_particles_v1'; Seed=246802; Grammar='magnetic_filament_cloud' },
    @{ Family='invisible_forces'; Production='c11c_invisible_forces_v1'; Seed=7; Grammar='dipole_field' },
    @{ Family='invisible_forces'; Production='c11c_invisible_forces_v1'; Seed=4; Grammar='vortex_field' },
    @{ Family='invisible_forces'; Production='c11c_invisible_forces_v1'; Seed=3; Grammar='saddle_field' },
    @{ Family='invisible_forces'; Production='c11c_invisible_forces_v1'; Seed=1; Grammar='quadrupole_field' },
    @{ Family='invisible_forces'; Production='c11c_invisible_forces_v1'; Seed=37; Grammar='gravitational_lens' },
    @{ Family='invisible_forces'; Production='c11c_invisible_forces_v1'; Seed=31; Grammar='topographic_basin' },
    @{ Family='invisible_forces'; Production='c11c_invisible_forces_v1'; Seed=43; Grammar='scalar_potential' }
)

function Get-FileSha256Hex([string]$Path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant() }
function Invoke-Checked([string]$Exe,[string[]]$Args,[string]$Label) {
    Write-Host "[C11-C-COVERAGE] $Label"
    & $Exe @Args
    if ($LASTEXITCODE -ne 0) { throw "$Label failed: exit=$LASTEXITCODE" }
}

$results = @()
$audioHashesByFamily = @{}
foreach ($case in $cases) {
    $launcher = Join-Path $ProjectRoot ("tools\prototypes\{0}\run_prototype.ps1" -f $case.Production)
    $familyRoot = Join-Path $ProjectRoot ("artifacts\prototypes\{0}" -f $case.Production)
    $stem = switch ($case.Production) {
        'c11c_geometric_waves_v1' { "GeometricWaves_v1_seed_$($case.Seed)" }
        'c11c_fractal_bloom_v1' { "FractalBloom_v1_seed_$($case.Seed)" }
        'c11c_sacred_symmetry_v1' { "SacredSymmetry_v1_seed_$($case.Seed)" }
        'c11c_living_particles_v1' { "LivingParticles_v1_seed_$($case.Seed)" }
        'c11c_invisible_forces_v1' { "InvisibleForces_v1_seed_$($case.Seed)" }
    }
    $mp4 = Join-Path $familyRoot "$stem.mp4"
    $wav = Join-Path $familyRoot "${stem}_music.wav"
    $manifest = Join-Path $familyRoot "${stem}_manifest.json"
    $social = Join-Path $familyRoot "${stem}_social.txt"

    Write-Host "[C11-C-COVERAGE] Render $($case.Family)/$($case.Grammar) seed=$($case.Seed)"
    & $launcher -Seed ([int]$case.Seed) -Grammar ([string]$case.Grammar)
    if ($LASTEXITCODE -ne 0) { throw "Render failed for $($case.Family)/$($case.Grammar) seed=$($case.Seed): exit=$LASTEXITCODE" }
    foreach ($required in @($mp4,$wav,$manifest,$social)) {
        if (-not (Test-Path -LiteralPath $required)) { throw "Missing expected artifact: $required" }
    }

    $m = Get-Content -Raw -LiteralPath $manifest | ConvertFrom-Json
    if ([string]$m.grammar_id -ne $case.Grammar) { throw "Grammar mismatch: expected technical_id $($case.Grammar), got $($m.grammar_id)" }
    if ([string]$m.audio.mode -ne 'FAMILY_MUSIC_V4') { throw "Audio mode mismatch for $($case.Grammar): $($m.audio.mode)" }
    if ([string]$m.audio.profile_id -eq '') { throw "Audio profile missing for $($case.Grammar)" }

    $probe = (ffprobe -v error -show_streams -show_format -of json $mp4 | Out-String) | ConvertFrom-Json
    $video = @($probe.streams | Where-Object { $_.codec_type -eq 'video' }) | Select-Object -First 1
    $audio = @($probe.streams | Where-Object { $_.codec_type -eq 'audio' }) | Select-Object -First 1
    if ($null -eq $video -or $null -eq $audio) { throw "MP4 stream contract failed for $($case.Grammar)" }
    if ([int]$video.width -ne 720 -or [int]$video.height -ne 1280) { throw "Resolution failed for $($case.Grammar)" }
    $duration=[double]$video.duration
    if ($duration -lt 20.0 -or $duration -gt 30.0) { throw "Duration failed for $($case.Grammar): $duration" }
    $expectedFrames=[int][math]::Round($duration * 30.0)
    if ([int]$video.nb_frames -ne $expectedFrames) { throw "Frame count failed for $($case.Grammar): $($video.nb_frames) expected $expectedFrames" }
    if ([int]$audio.sample_rate -ne 44100 -or [int]$audio.channels -ne 2) { throw "Audio format failed for $($case.Grammar)" }

    if (-not $audioHashesByFamily.ContainsKey($case.Family)) { $audioHashesByFamily[$case.Family] = @{} }
    $audioHash = Get-FileSha256Hex $wav
    if ($audioHashesByFamily[$case.Family].ContainsKey($audioHash)) { throw "Duplicate audio hash inside family $($case.Family): $($case.Grammar) duplicates $($audioHashesByFamily[$case.Family][$audioHash])" }
    $audioHashesByFamily[$case.Family][$audioHash] = $case.Grammar
    $results += [pscustomobject]@{ family=$case.Family; grammar=$case.Grammar; grammar_name=[string]$m.grammar; seed=$case.Seed; mp4=$mp4; wav=$wav; audio_profile=$m.audio.profile_id; audio_sha256=$audioHash; status='PASS' }
}

$summary = [ordered]@{
    schema='C11-C-VISUAL-LOOPS-SUBTYPE-MUSIC-COVERAGE-V1'
    revision='2.13.0'
    total=27
    audio_required=$true
    results=$results
}
$summaryPath = Join-Path $Root 'coverage_manifest.json'
$summary | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $summaryPath
Write-Host "[C11-C-COVERAGE] COMPLETE - $($results.Count)/27 subtype renders PASS with audio."
