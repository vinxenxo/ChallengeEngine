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
$transition=[double]$schedule.transition_duration_seconds
$finalFade=[double]$schedule.final_fade_seconds
if($segments.Count -lt 2){throw 'Longform requires at least two segments.'}
foreach($segment in $segments){
    $segDuration=[double]$segment.duration_seconds
    if($segDuration -lt 20.0 -or $segDuration -gt 23.0){throw "Longform segment outside 20..23s: $($segment.grammar_id)"}
}
$rawTotal=0.0
foreach($segment in $segments){$rawTotal += [double]$segment.duration_seconds}
$expectedComposed=$rawTotal - ($transition * ($segments.Count - 1))
if([math]::Abs($expectedComposed-$target)-gt 0.01){throw "Longform composed duration invalid for ${Family}: raw=$rawTotal transition=$transition expected=$expectedComposed target=$target"}

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
$listPath=Join-Path $productRoot 'concat_sources.txt'
$segmentResults=@()
$sourcePaths=@()
for($i=0;$i -lt $segments.Count;$i++){
    $segment=$segments[$i]
    $segSeed=[int]$seedValues[$i]
    $duration=[double]$segment.duration_seconds
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
        if(-not $?){throw "Canonical production segment failed: $($segment.grammar_id) seed=$segSeed"}
        $source=Get-C11CProductionArtifacts -Production $production -Seed $segSeed
    }
    foreach($req in @($source.Manifest,$source.Music,$source.Social,$source.MP4)){
        if(-not(Test-Path -LiteralPath $req)){throw "Missing segment artifact: $req"}
    }
    $probeJson=& ffprobe -v error -show_streams -show_format -of json $source.MP4
    if($LASTEXITCODE -ne 0){throw "ffprobe failed for segment: $($segment.grammar_id)"}
    $probe=($probeJson -join "`n") | ConvertFrom-Json
    $video=@($probe.streams | Where-Object {$_.codec_type -eq 'video'}) | Select-Object -First 1
    $audio=@($probe.streams | Where-Object {$_.codec_type -eq 'audio'}) | Select-Object -First 1
    if($null -eq $video -or $null -eq $audio){throw "Longform segment must contain video and audio: $($segment.grammar_id)"}
    if([int]$video.width -ne 720 -or [int]$video.height -ne 1280 -or [string]$video.r_frame_rate -ne '30/1'){throw "Segment delivery contract failed: $($segment.grammar_id)"}
    if([int]$audio.sample_rate -ne 44100 -or [int]$audio.channels -ne 2){throw "Segment audio contract failed: $($segment.grammar_id)"}

    $segmentResults += [ordered]@{
        slot=($i+1)
        family=$familyKey
        grammar_id=[string]$segment.grammar_id
        grammar_name=[string]$segment.grammar_name
        seed=$segSeed
        duration_seconds=$duration
        source_product=$source.MP4
        source_manifest=$source.Manifest
        source_music=$source.Music
        loop_safe=$true
    }
    $sourcePaths += [string]$source.MP4
    $segmentManifestPath=Join-Path $segmentRoot ("{0:D2}_{1}_seed_{2}.json" -f ($i+1),$segment.grammar_id,$segSeed)
    [System.IO.File]::WriteAllText($segmentManifestPath,($segmentResults[-1]|ConvertTo-Json -Depth 8),(New-Object System.Text.UTF8Encoding($false)))
}

# Build filters without culture-sensitive PowerShell interpolation helpers.
$filterParts=@()
function Fmt([double]$value){ return $value.ToString('0.########', [System.Globalization.CultureInfo]::InvariantCulture) }
$videoLabel='[0:v]'
for($i=1;$i -lt $segments.Count;$i++){
    $outV="[v$i]"
    $offset=[double]$i * ($segments[0].duration_seconds - $transition)
    $inputV="[$($i-1):v]"
    if($i -gt 1){$inputV="[v$($i-1)]"}
    $filterParts += ("{0}[{1}:v]xfade=transition=fade:duration={2}:offset={3}{4}" -f $videoLabel, $i, (Fmt $transition), (Fmt $offset), $outV)
    $videoLabel=$outV
}
$audioLabel='[0:a]'
for($i=1;$i -lt $segments.Count;$i++){
    $outA="[a$i]"
    $left = if($i -eq 1){'[0:a]'}else{"[a$($i-1)]"}
    $filterParts += ("{0}[{1}:a]acrossfade=d={2}:c1=tri:c2=tri{3}" -f $left, $i, (Fmt $transition), $outA)
    $audioLabel=$outA
}
$finalStart=$target-$finalFade
$filterParts += "$videoLabel" + "fade=t=out:st=$(Fmt $finalStart):d=$(Fmt $finalFade):color=black[vout]"
$filterParts += "$audioLabel" + "afade=t=out:st=$(Fmt $finalStart):d=$(Fmt $finalFade)[aout]"
$filterComplex=$filterParts -join ';'

$outStem=("$($familySchedule.artistic_name -replace ' ','')_Longform_seed_$Seed")
$outMp4=Join-Path $productRoot "$outStem.mp4"
$ffArgs=@('-y','-hide_banner','-loglevel','error')
foreach($sourcePath in $sourcePaths){$ffArgs += @('-i',$sourcePath)}
$ffArgs += @('-filter_complex',$filterComplex,'-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','44100','-ac','2','-movflags','+faststart',$outMp4)
& ffmpeg @ffArgs
if($LASTEXITCODE -ne 0){throw "Longform FFmpeg composition failed: exit=$LASTEXITCODE"}

$probeJson=& ffprobe -v error -show_streams -show_format -of json $outMp4
if($LASTEXITCODE -ne 0){throw "Longform ffprobe failed: exit=$LASTEXITCODE"}
$probe=($probeJson -join "`n") | ConvertFrom-Json
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
$hook='¿Puedes ver cómo cambia el universo visual sin notar el paso entre mundos?'
$description="$($familySchedule.artistic_name.ToUpper()) - video long-form de arte generativa matemática y procedural.`n`nDuración: 180.00s`nSegmentos: $($segmentResults.Count) subfamilias visuales`nSeed base: $Seed`nAudio: música determinista por familia y subfamilia.`n`nLas variantes se enlazan mediante continuidad cromática y geométrica, sin fundidos a negro entre capítulos. El cierre final sí realiza un fundido a negro.`n`nDiseñado en código con #GodotEngine para contemplación prolongada."
$hashtags="#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying $($familyTags[$familyKey])"
$copyPaste="$hook`n`n$description`n`n$hashtags"
$socialPath=Join-Path $productRoot "${outStem}_social.txt"
$social=@('COPY_PASTE_READY:',$copyPaste,'','TITLE:',"$($familySchedule.artistic_name) - LONGFORM",'','DESCRIPTION:',$description,'',"FAMILY: $familyKey", "SEED: $Seed", ('DURATION: ' + $duration.ToString('0.00',[System.Globalization.CultureInfo]::InvariantCulture) + ' s'), "FPS: 30", "FRAMES: $frames", "TRANSITION: crossfade continuity; never through black", "FINAL FADE: $finalFade s to black", '','HEADER HOOK:',$hook,'','HASHTAGS:',$hashtags)
[System.IO.File]::WriteAllLines($socialPath,$social,(New-Object System.Text.UTF8Encoding($false)))

$manifest=[ordered]@{
    schema='C11-C-VISUAL-LOOP-LONGFORM-PRODUCTION-V2'
    revision='2.15.0'
    status='FINAL_LONGFORM_PRODUCT'
    family=[ordered]@{technical_id=$familyKey;artistic_name=$familySchedule.artistic_name;production_id=$familySchedule.production_id}
    base_seed=$Seed
    duration_seconds=$duration
    fps=30
    frames=$frames
    resolution='720x1280'
    audio=[ordered]@{mode='FAMILY_MUSIC_V4';sample_rate=44100;channels=2;composition='per-segment audio acrossfade';continuous_across_boundaries=$true}
    composition_model='crossfade_continuity_v2'
    raw_segment_seconds=$rawTotal
    transition_duration_seconds=$transition
    segment_overlap_count=($segments.Count-1)
    final_fade_seconds=$finalFade
    final_fade_color='black'
    transition_through_black=$false
    loop_safe_segments=$true
    overall_longform_loop=$false
    composition='canonical production segments + FFmpeg xfade/acrossfade; no new renderer'
    segments=$segmentResults
    output_mp4=$outMp4
    social=$socialPath
}
$manifestPath=Join-Path $productRoot "${outStem}_manifest.json"
[System.IO.File]::WriteAllText($manifestPath,($manifest|ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))
Remove-Item -LiteralPath $listPath -Force -ErrorAction SilentlyContinue
Write-Host "[C11-C-LONGFORM] PASS family=$familyKey | segments=$($segments.Count) | raw=$rawTotal s | composed=$duration s | transitions=$transition s | final fade=$finalFade s"
Write-Host "[C11-C-LONGFORM] MP4: $outMp4"
Write-Host "[C11-C-LONGFORM] MANIFEST: $manifestPath"
Write-Host "[C11-C-LONGFORM] SOCIAL: $socialPath"
return
