[CmdletBinding()]
param(
    [ValidateRange(1,2147483646)][int]$Seed = 24681357,
    [string]$OutputRoot = '',
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $ProjectRoot

if([string]::IsNullOrWhiteSpace($OutputRoot)){
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
    $OutputRoot=Join-Path $ProjectRoot "artifacts\qa\c11c_family_coverage_smoke\$stamp"
}else{$OutputRoot=[IO.Path]::GetFullPath($OutputRoot)}
New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

function Read-Json([string]$Path){ Get-Content -Raw -LiteralPath $Path -Encoding UTF8 | ConvertFrom-Json }
function Invoke-Child([string]$Label,[string]$Script,[string[]]$Arguments){
    Write-Host "[C11C-FAMILY] START $Label"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Script @Arguments
    if($LASTEXITCODE -ne 0){ throw "$Label failed with exit code $LASTEXITCODE" }
    Write-Host "[C11C-FAMILY] PASS $Label"
}
function Get-FirstFinalMp4([string]$Root,[string]$Label){
    $files=@(Get-ChildItem -LiteralPath $Root -Recurse -File -Filter '*.mp4' -ErrorAction SilentlyContinue | Where-Object {$_.Name -notlike '*_silent.mp4'})
    if($files.Count -ne 1){ throw "$Label expected exactly one final MP4 under $Root; found $($files.Count)." }
    return $files[0].FullName
}
function Assert-Media([string]$Path,[string]$Label,[int]$ExpectedFrames,[double]$ExpectedDuration,[int]$ExpectedWidth=720,[int]$ExpectedHeight=1280,[int]$ExpectedFps=30,[switch]$Audio48000,[switch]$Audio44100){
    if(-not(Test-Path -LiteralPath $Path -PathType Leaf)){throw "$Label missing MP4: $Path"}
    $raw=& ffprobe -v error -count_frames -show_streams -show_format -of json -- $Path 2>&1
    if($LASTEXITCODE -ne 0){throw "$Label ffprobe failed: $($raw -join "`n")"}
    $probe=($raw -join "`n")|ConvertFrom-Json
    $video=@($probe.streams|Where-Object{$_.codec_type -eq 'video'})|Select-Object -First 1
    $audio=@($probe.streams|Where-Object{$_.codec_type -eq 'audio'})|Select-Object -First 1
    if($null -eq $video){throw "$Label has no video stream."}
    if([int]$video.width -ne $ExpectedWidth -or [int]$video.height -ne $ExpectedHeight){throw "$Label resolution mismatch: $($video.width)x$($video.height); expected ${ExpectedWidth}x${ExpectedHeight}."}
    if([string]$video.r_frame_rate -ne ("{0}/1" -f $ExpectedFps)){throw "$Label FPS mismatch: $($video.r_frame_rate); expected ${ExpectedFps}/1."}
    if([int]$video.nb_read_frames -ne $ExpectedFrames){throw "$Label frame mismatch: $($video.nb_read_frames); expected $ExpectedFrames."}
    if([math]::Abs([double]$video.duration-$ExpectedDuration)-gt 0.10){throw "$Label duration mismatch: $($video.duration); expected $ExpectedDuration."}
    if($Audio48000 -or $Audio44100){
        if($null -eq $audio){throw "$Label must contain audio."}
        $rate=[int]$audio.sample_rate
        $expectedRate=if($Audio48000){48000}else{44100}
        if($rate -ne $expectedRate -or [int]$audio.channels -ne 2){throw "$Label audio mismatch: $rate Hz / $($audio.channels) channels; expected $expectedRate / 2."}
    }
    return $probe
}

$schema=Read-Json (Join-Path $ProjectRoot 'c11c-suite\c11c-producer\producer_schema.json')
$schedule=Read-Json (Join-Path $ProjectRoot 'profiles\presentation\c11c_visual_loop_longform_schedule.json')

# 5 Visual Loops: first canonical Longform grammar for each family, avoiding the auto grammar.
$loopFamilyMap=[ordered]@{
    c11c_geometric_waves_v1='harmonic_membrane'
    c11c_fractal_bloom_v1='radial_bloom'
    c11c_sacred_symmetry_v1='astrolabe'
    c11c_living_particles_v1='swarm'
    c11c_invisible_forces_v1='dipole_field'
}
$loopPrefixMap=@{
    c11c_geometric_waves_v1='GeometricWaves_v1'
    c11c_fractal_bloom_v1='FractalBloom_v1'
    c11c_sacred_symmetry_v1='SacredSymmetry_v1'
    c11c_living_particles_v1='LivingParticles_v1'
    c11c_invisible_forces_v1='InvisibleForces_v1'
}
$items=@()
$loopCount=0
foreach($family in $loopFamilyMap.Keys){
    if(-not $schema.families -contains $family){throw "Schema family missing: $family"}
    $grammar=$loopFamilyMap[$family]
    $familyKey=switch($family){
        'c11c_geometric_waves_v1'{'geometric'}
        'c11c_fractal_bloom_v1'{'fractal'}
        'c11c_sacred_symmetry_v1'{'sacred_symmetry'}
        'c11c_living_particles_v1'{'living_particles'}
        'c11c_invisible_forces_v1'{'invisible_forces'}
    }
    $scheduled=@($schedule.families.$familyKey.segments | Where-Object {[string]$_.grammar_id -eq $grammar})|Select-Object -First 1
    if($null -eq $scheduled){throw "Longform schedule does not expose representative grammar $grammar for $family"}
    $runner=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_production.ps1'
    Invoke-Child "Visual Loop $family / $grammar" $runner @('-Family',$family,'-Seed',[string]$Seed,'-Grammar',$grammar,'-Duration','23','-DeliveryProfile','REVIEW_720','-Force')
    $productRoot=Join-Path (Join-Path $ProjectRoot 'artifacts\production\audiovisual') (Join-Path $family ("$($loopPrefixMap[$family])_seed_$Seed"))
    $mp4=Join-Path $productRoot "$($loopPrefixMap[$family])_seed_$Seed.mp4"
    $manifest=Join-Path $productRoot 'production_manifest.json'
    if(-not(Test-Path $manifest)){throw "Loop production manifest missing: $manifest"}
    $m=Read-Json $manifest
    if([string]$m.grammar_id -ne $grammar){throw "Loop manifest grammar mismatch: $manifest"}
    Assert-Media $mp4 "Visual Loop $family" 690 23.0 -Audio44100 | Out-Null
    $items += [pscustomobject]@{kind='visual_loop';family=$family;grammar=$grammar;seed=$Seed;mp4=$mp4;status='PASS'}
    $loopCount++
}

# 4 Visual Drills: one seed for each drill family.
$drillRoot=Join-Path $OutputRoot 'visual_drills'
foreach($family in @('tracking','saccade','pursuit','peripheral_scan')){
    $runner=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1'
    $root=Join-Path $drillRoot $family
    Invoke-Child "Visual Drill $family" $runner @('-Seeds',[string]$Seed,'-Families',$family,'-Smoke','-ResetReviewAssets','-RegenerateEnvelopes','-ReviewRootOverride',$root)
    $mp4=Get-FirstFinalMp4 $root "Visual Drill $family"
    $frames=if($family -eq 'tracking'){810}else{690}
    $duration=if($family -eq 'tracking'){27.0}else{23.0}
    Assert-Media $mp4 "Visual Drill $family" $frames $duration -Audio44100 | Out-Null
    $items += [pscustomobject]@{kind='visual_drill';family=$family;grammar=$null;seed=$Seed;mp4=$mp4;status='PASS'}
}

# 9 Challenges: canonical C11 matrix is video-only; challenge FPS is definition-driven.
$challengeRoot=Join-Path $OutputRoot 'challenges'
$challengeRunner=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1'
$challengePaths=@(Get-ChildItem -LiteralPath (Join-Path $ProjectRoot 'challenges') -File -ErrorAction Stop | Where-Object { $_.Extension -ieq '.json' -and $_.BaseName -match '^CHALLENGE_[0-9]{3}$' } | Sort-Object Name)
if($challengePaths.Count -ne 9){throw "Expected 9 challenge definitions; found $($challengePaths.Count)."}
foreach($path in $challengePaths){
    $cfg=Read-Json $path.FullName
    $id=[string]$cfg.challenge_id
    $fps=[int]$cfg.video.fps
    $totalSeconds=0.0
    foreach($key in @('hook_duration','game_duration','cta_duration')){$totalSeconds += [double]$cfg.video.$key}
    # Some legacy C11 Challenge definitions omit reveal_duration. Treat it as 0s
    # for the QA timing calculation without modifying the source JSON.
    $revealDuration=0.0
    if($null -ne $cfg.video){
        $revealProperty=@($cfg.video.PSObject.Properties | Where-Object {$_.Name -ieq 'reveal_duration'}) | Select-Object -First 1
        if($null -ne $revealProperty){$revealDuration=[double]$revealProperty.Value}
    }
    $totalSeconds += $revealDuration
    $expectedFrames=[int][math]::Round($totalSeconds*$fps)
    $duration=$totalSeconds
    Invoke-Child "Challenge $id" $challengeRunner @('-ChallengeId',$id,'-Seed',[string]$Seed,'-DeliveryProfile','REVIEW_720','-OutputRoot',$challengeRoot,'-Force')
    $mp4=Join-Path (Join-Path $challengeRoot $id) "${id}_seed_${Seed}.mp4"
    $challengeProbe=Assert-Media $mp4 "Challenge $id" $expectedFrames $duration 720 1280 $fps
    $challengeAudio=@($challengeProbe.streams|Where-Object{$_.codec_type -eq 'audio'})
    if($challengeAudio.Count -ne 0){throw "Challenge $id must remain video-only for the C11 review matrix; audio streams=$($challengeAudio.Count)."}
    $items += [pscustomobject]@{kind='challenge';family=[string]$cfg.mechanic;challenge_id=$id;seed=$Seed;mp4=$mp4;status='PASS'}
}

# 5 Longforms: one base seed for every visual family.
$longRoot=Join-Path $OutputRoot 'longforms'
$longRunner=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_loop_longform_production.ps1'
$longFamilyKeyMap=@{
    c11c_geometric_waves_v1='geometric'
    c11c_fractal_bloom_v1='fractal'
    c11c_sacred_symmetry_v1='sacred_symmetry'
    c11c_living_particles_v1='living_particles'
    c11c_invisible_forces_v1='invisible_forces'
}
foreach($family in $loopFamilyMap.Keys){
    Invoke-Child "Longform $family" $longRunner @('-Family',$family,'-Seed',[string]$Seed,'-OutputRoot',$longRoot,'-Force')
    $art=$schedule.families.($longFamilyKeyMap[$family])
    $artistStem=($art.artistic_name -replace ' ','')
    $productRoot=Join-Path $longRoot $family
    $mp4=Join-Path $productRoot "${artistStem}_Longform_seed_${Seed}\${artistStem}_Longform_seed_${Seed}.mp4"
    Assert-Media $mp4 "Longform $family" 5400 180.0 -Audio44100 | Out-Null
    $items += [pscustomobject]@{kind='longform';family=$family;seed=$Seed;mp4=$mp4;status='PASS'}
}

$counts=@{
    visual_loops=[int]@($items|Where-Object kind -eq 'visual_loop').Count
    visual_drills=[int]@($items|Where-Object kind -eq 'visual_drill').Count
    challenges=[int]@($items|Where-Object kind -eq 'challenge').Count
    longforms=[int]@($items|Where-Object kind -eq 'longform').Count
}
$total=$counts.visual_loops+$counts.visual_drills+$counts.challenges+$counts.longforms
if($total -ne 23){throw "Family coverage smoke expected 23 products, got $total."}

$report=[ordered]@{
    schema='C11-C-FAMILY-COVERAGE-SMOKE-V1'
    revision='2.19.12'
    status='PASS'
    seed=$Seed
    physical_profile='720x1280@30'
    counts=$counts
    total_products=$total
    contracts=[ordered]@{
        visual_loops='5 families; 1 representative canonical grammar each; 23s / 690 frames'
        visual_drills='4 families; tracking 27s/810 frames; others 23s/690 frames'
        challenges='9 definitions; declarative four-phase timing; REVIEW_720 delivery'
        longforms='5 families; 180s / 5400 frames'
    }
    items=$items
    generated_at_utc=[DateTimeOffset]::UtcNow.ToString('o')
}
$reportPath=Join-Path $OutputRoot 'C11C_FAMILY_COVERAGE_SMOKE_REPORT.json'
[IO.File]::WriteAllText($reportPath,($report|ConvertTo-Json -Depth 12),(New-Object Text.UTF8Encoding($false)))
Write-Host "[C11C-FAMILY] COMPLETE PASS - 23 products (5 Visual Loops + 4 Visual Drills + 9 Challenges + 5 Longforms)"
Write-Host "[C11C-FAMILY] REPORT: $reportPath"
