param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')]
    [string]$Family,
    [Parameter(Mandatory=$true)]
    [ValidateRange(1,2147483646)]
    [int]$Seed,
    [Parameter(Mandatory=$false)]
    [string]$OutputRoot='',
    [switch]$Force
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
. (Join-Path $PSScriptRoot 'C11CProductionBatchCommon.ps1')

$schedulePath=Join-Path $ProjectRoot 'profiles\presentation\c11c_visual_loop_longform_schedule.json'
$schedule=Get-Content -Raw -LiteralPath $schedulePath | ConvertFrom-Json
$familyKey = switch ($Family) {
    'c11c_geometric_waves_v1' { 'geometric' }
    'c11c_fractal_bloom_v1' { 'fractal' }
    'c11c_sacred_symmetry_v1' { 'sacred_symmetry' }
    'c11c_living_particles_v1' { 'living_particles' }
    'c11c_invisible_forces_v1' { 'invisible_forces' }
    default { throw "Unknown longform family: $Family" }
}
$familySchedule=$schedule.families.$familyKey
if($null -eq $familySchedule){throw "No longform schedule for family: $Family"}
$segments=@($familySchedule.segments)
$target=[double]$schedule.target_duration_seconds
$total=0.0
foreach($segment in $segments){$total += [double]$segment.duration_seconds}
if([math]::Abs($total-$target)-gt 0.01){throw "Longform schedule duration invalid for ${Family}: $total"}
foreach($segment in $segments){if([double]$segment.duration_seconds -lt 20.0 -or [double]$segment.duration_seconds -gt 23.0){throw "Longform segment outside 20..23s: $($segment.grammar_id)"}}

if([string]::IsNullOrWhiteSpace($OutputRoot)){ $OutputRoot=Join-Path $ProjectRoot 'artifacts\production\audiovisual_longform' }
$familyRoot=Join-Path $OutputRoot $Family
$productRoot=Join-Path $familyRoot ("$($familySchedule.artistic_name -replace ' ','')_Longform_seed_$Seed")
if((Test-Path -LiteralPath $productRoot) -and -not $Force){throw "Longform product already exists: $productRoot. Use -Force for deliberate replacement."}
if($Force -and (Test-Path -LiteralPath $productRoot)){Remove-Item -LiteralPath $productRoot -Recurse -Force}
New-Item -ItemType Directory -Force -Path $productRoot | Out-Null
$segmentRoot=Join-Path $productRoot 'segments'
New-Item -ItemType Directory -Force -Path $segmentRoot | Out-Null

function Get-LongformSeeds {
    param([int]$Count,[int]$BaseSeed,[string]$FamilyKey)
    $min=1000000; $max=2147483646; $binWidth=[double]($max-$min)/[double]($Count+1); $margin=$binWidth*0.30
    $values=@()
    for($i=1;$i -le $Count;$i++){
        $key="$BaseSeed|$FamilyKey|segment_$i"
        $sha=[System.Security.Cryptography.SHA256]::Create()
        try{$digest=$sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($key))}finally{$sha.Dispose()}
        $u=[BitConverter]::ToUInt64($digest,0)/[double]([UInt64]::MaxValue)
        $center=$min+($binWidth*$i)
        $candidate=[int][math]::Round(($center-$margin)+(2.0*$margin*$u))
        $values+=$candidate
    }
    Assert-C11CSeedSpacing -Seeds ([int[]]$values)
    return [int[]]$values
}

$seedValues=Get-LongformSeeds -Count $segments.Count -BaseSeed $Seed -FamilyKey $familyKey
$listPath=Join-Path $productRoot 'concat.txt'
$list=@()
$segmentResults=@()
for($i=0;$i -lt $segments.Count;$i++){
    $segment=$segments[$i]; $segSeed=[int]$seedValues[$i]; $duration=[double]$segment.duration_seconds
    $production=$familySchedule.production_id
    $launcher=Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_production.ps1'
    $source=Get-C11CProductionArtifacts -Production $production -Seed $segSeed
    $needsRender=$true
    if(Test-Path -LiteralPath $source.Manifest){
        try{
            $existing=Get-Content -Raw -LiteralPath $source.Manifest | ConvertFrom-Json
            $needsRender=([string]$existing.grammar_id -ne [string]$segment.grammar_id -or [math]::Abs([double]$existing.duration_seconds-$duration)-gt 0.01)
        }catch{$needsRender=$true}
    }
    if($needsRender -or -not(Test-Path -LiteralPath $source.MP4)){
        & $launcher -Family $production -Seed $segSeed -Grammar $segment.grammar_id -Duration $duration -Force
        if($LASTEXITCODE -ne 0){throw "Canonical production segment failed: $($segment.grammar_id) seed=$segSeed"}
        $source=Get-C11CProductionArtifacts -Production $production -Seed $segSeed
    }
    if(-not(Test-Path -LiteralPath $source.MP4)){throw "Missing segment MP4: $($source.MP4)"}
    foreach($req in @($source.Manifest,$source.Music,$source.Social)){
        if(-not(Test-Path -LiteralPath $req)){throw "Missing segment artifact: $req"}
    }
    $probe=(ffprobe -v error -show_streams -show_format -of json $source.MP4 | Out-String) | ConvertFrom-Json
    $video=@($probe.streams | Where-Object {$_.codec_type -eq 'video'}) | Select-Object -First 1
    $audio=@($probe.streams | Where-Object {$_.codec_type -eq 'audio'}) | Select-Object -First 1
    if($null -eq $video -or $null -eq $audio){throw "Longform segment must contain video and audio: $($segment.grammar_id)"}
    if([int]$video.width -ne 720 -or [int]$video.height -ne 1280 -or [string]$video.r_frame_rate -ne '30/1'){throw "Segment delivery contract failed: $($segment.grammar_id)"}
    if([int]$audio.sample_rate -ne 44100 -or [int]$audio.channels -ne 2){throw "Segment audio contract failed: $($segment.grammar_id)"}
    $concatPath=$source.MP4.Replace('\','/')
    $list += "file '$concatPath'"
    $segmentManifest=[ordered]@{slot=($i+1);family=$familyKey;grammar_id=[string]$segment.grammar_id;grammar_name=[string]$segment.grammar_name;seed=$segSeed;duration_seconds=$duration;source_product=$source.MP4;source_manifest=$source.Manifest;source_music=$source.Music;loop_safe=$true}
    $segmentManifestPath=Join-Path $segmentRoot ("{0:D2}_{1}_seed_{2}.json" -f ($i+1),($segment.grammar_id),$segSeed)
    [System.IO.File]::WriteAllText($segmentManifestPath,($segmentManifest|ConvertTo-Json -Depth 8),(New-Object System.Text.UTF8Encoding($false)))
    $segmentResults += $segmentManifest
}
[System.IO.File]::WriteAllLines($listPath,$list,(New-Object System.Text.UTF8Encoding($false)))

$stem=("$($familySchedule.artistic_name -replace ' ','')_Longform_seed_$Seed")
$outMp4=Join-Path $productRoot "$stem.mp4"
& ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i $listPath -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart $outMp4
if($LASTEXITCODE -ne 0){throw "Longform FFmpeg composition failed: exit=$LASTEXITCODE"}
$probe=(ffprobe -v error -show_streams -show_format -of json $outMp4 | Out-String) | ConvertFrom-Json
$video=@($probe.streams | Where-Object {$_.codec_type -eq 'video'}) | Select-Object -First 1
$audio=@($probe.streams | Where-Object {$_.codec_type -eq 'audio'}) | Select-Object -First 1
if($null -eq $video -or $null -eq $audio){throw 'Longform MP4 missing required streams.'}
$duration=[double]$probe.format.duration
$frames=[int]$video.nb_frames
if([math]::Abs($duration-$target)-gt 0.10){throw "Longform duration failed: $duration expected $target"}
if([string]$video.r_frame_rate -ne '30/1'){throw "Longform FPS failed: $($video.r_frame_rate)"}
if([int]$video.width -ne 720 -or [int]$video.height -ne 1280){throw "Longform resolution failed: $($video.width)x$($video.height)"}
if([int]$audio.sample_rate -ne 44100 -or [int]$audio.channels -ne 2){throw 'Longform audio format failed.'}

$familyTags=@{
    geometric='#GeometricWaves #WaveArt #MathematicalArt #ProceduralArt #DigitalArt #TechArt';
    fractal='#FractalBloom #FractalArt #MathematicalArt #ProceduralArt #JuliaSet #DigitalArt';
    sacred_symmetry='#SacredSymmetry #GeometricArt #Astrolabe #CelestialArt #ProceduralArt #DigitalArt';
    living_particles='#LivingParticles #ParticleArt #FluidArt #OrganicArt #ProceduralArt #DigitalArt';
    invisible_forces='#InvisibleForces #VectorField #PhysicsArt #TopographicArt #ProceduralArt #DigitalArt'
}
$first=$segmentResults[0]
$social=@(
    "¿Puedes ver cómo cambia el universo visual sin notar el paso entre mundos?",
    '',
    "**$($familySchedule.artistic_name.ToUpper())** — video long-form de arte generativa matemática y procedural.",
    '',
    "- **Duración:** 180.00s",
    "- **Segmentos:** $($segmentResults.Count) subfamilias visuales",
    "- **Seed base:** $Seed",
    "- **Audio:** música ambiental determinista por familia y subfamilia.",
    '',
    'Cada capítulo utiliza el renderer canónico de su subfamilia y conserva su propio cierre visual.',
    '',
    'Diseñado en código con #GodotEngine para contemplación prolongada.',
    '',
    "#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying $($familyTags[$familyKey])"
)
$socialPath=Join-Path $productRoot "${stem}_social.txt"
[System.IO.File]::WriteAllLines($socialPath,$social,(New-Object System.Text.UTF8Encoding($false)))

$manifest=[ordered]@{
    schema='C11-C-VISUAL-LOOP-LONGFORM-PRODUCTION-V1'
    revision='2.14.0'
    status='FINAL_LONGFORM_PRODUCT'
    family=[ordered]@{technical_id=$familyKey;artistic_name=$familySchedule.artistic_name;production_id=$familySchedule.production_id}
    base_seed=$Seed
    duration_seconds=$duration
    fps=30
    frames=$frames
    resolution='720x1280'
    audio=[ordered]@{mode='FAMILY_MUSIC_V4';sample_rate=44100;channels=2;composition='segment-concat';continuous_across_boundaries=$false}
    loop_safe_segments=$true
    overall_longform_loop=$false
    composition='canonical production segments + FFmpeg concat; no new renderer'
    segments=$segmentResults
    output_mp4=$outMp4
    social=$socialPath
}
$manifestPath=Join-Path $productRoot "${stem}_manifest.json"
[System.IO.File]::WriteAllText($manifestPath,($manifest|ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))
Remove-Item -LiteralPath $listPath -Force
Write-Host "[C11-C-LONGFORM] PASS family=$familyKey | segments=$($segments.Count) | 180.00s | 720x1280 / 30 FPS / audio"
Write-Host "[C11-C-LONGFORM] MP4: $outMp4"
Write-Host "[C11-C-LONGFORM] MANIFEST: $manifestPath"
Write-Host "[C11-C-LONGFORM] SOCIAL: $socialPath"
return
