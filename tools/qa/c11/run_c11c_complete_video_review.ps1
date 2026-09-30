[CmdletBinding()]
param(
    [ValidateRange(1,7)][int]$Workers=7,
    [switch]$Reset,
    [switch]$Resume,
    [switch]$ExportGif
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

if($Reset -and $Resume){throw 'Use either -Reset or -Resume, not both.'}
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
Set-Location $Root
$ReviewRoot=Join-Path $Root 'artifacts\prototypes\c11c_art_direction_review'
$Batch=Join-Path $Root 'tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1'

if($Reset -or $Resume -or -not(Test-Path -LiteralPath (Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'))){
  $batchArgs=@('-NoProfile','-ExecutionPolicy','Bypass','-File',$Batch,'-Workers',$Workers,'-All')
  if($Reset){$batchArgs+='-Reset'} elseif($Resume){$batchArgs+='-Resume'}
  if($ExportGif){$batchArgs+='-ExportGif'}
  Write-Host '[C11-C-COMPLETE-REVIEW] Generating canonical 52-video review corpus.'
  & powershell.exe @batchArgs
  if($LASTEXITCODE -ne 0){throw "Canonical Art Direction batch failed with exit code $LASTEXITCODE"}
}

function Read-Json([string]$Path){Get-Content -Raw -LiteralPath $Path | ConvertFrom-Json}
function Get-FirstVideo([object]$Probe){@($Probe.streams | Where-Object {$_.codec_type -eq 'video'}) | Select-Object -First 1}
function Get-FirstAudio([object]$Probe){@($Probe.streams | Where-Object {$_.codec_type -eq 'audio'}) | Select-Object -First 1}
function Resolve-LoopMediaPath([object]$Manifest,[string]$ManifestPath){
  if($Manifest.PSObject.Properties.Name -contains 'output_mp4'){
    $value=[string]$Manifest.output_mp4
    if(-not [string]::IsNullOrWhiteSpace($value)){return $value}
  }
  if($Manifest.PSObject.Properties.Name -contains 'mp4'){
    $value=[string]$Manifest.mp4
    if(-not [string]::IsNullOrWhiteSpace($value)){return $value}
  }
  return ($ManifestPath -replace '_manifest\.json$','.mp4')
}
function Assert-Media([string]$Path,[int]$ExpectedFrames,[double]$ExpectedDuration,[string]$Label){
  if(-not(Test-Path -LiteralPath $Path)){throw "$Label missing media: $Path"}
  $raw=& ffprobe -v error -show_streams -show_format -of json $Path 2>&1
  if($LASTEXITCODE -ne 0){throw "$Label ffprobe failed: $Path`n$($raw -join "`n")"}
  $probe=($raw -join "`n") | ConvertFrom-Json
  $v=Get-FirstVideo $probe; $a=Get-FirstAudio $probe
  if($null -eq $v -or $null -eq $a){throw "$Label must contain video and audio streams: $Path"}
  if([int]$v.width -ne 720 -or [int]$v.height -ne 1280){throw "$Label resolution mismatch: $($v.width)x$($v.height)"}
  if([string]$v.r_frame_rate -ne '30/1'){throw "$Label FPS mismatch: $($v.r_frame_rate)"}
  if([int]$v.nb_frames -ne $ExpectedFrames){throw "$Label frame count mismatch: $($v.nb_frames), expected $ExpectedFrames"}
  if([math]::Abs([double]$v.duration-$ExpectedDuration) -gt 0.10){throw "$Label duration mismatch: $($v.duration), expected ~$ExpectedDuration"}
  if([int]$a.sample_rate -ne 44100 -or [int]$a.channels -ne 2){throw "$Label audio format mismatch."}
}

$manifestPath=Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'
if(-not(Test-Path -LiteralPath $manifestPath)){throw "Missing corpus manifest: $manifestPath"}
$batchManifest=Read-Json $manifestPath
if([string]$batchManifest.status -ne 'COMPLETE'){throw 'Art Direction corpus manifest is not COMPLETE.'}
if([int]$batchManifest.workers -ne $Workers){throw "Corpus worker count is $($batchManifest.workers), expected $Workers."}
if($Workers -gt 1 -and [int]$batchManifest.max_observed_worker_concurrency -le 1){throw 'Genuine parallel capture was not proven (MAX_OBSERVED_CONCURRENCY <= 1).'}
if([string]$batchManifest.worker_isolation -ne 'per_worker_temporary_godot_project'){throw 'Worker isolation contract mismatch.'}
if([string]$batchManifest.worker_global_script_class_cache -ne 'required_per_worker'){throw 'Worker global script class-cache contract mismatch.'}
if([string]$batchManifest.worker_bootstrap -ne 'source_project_godot_class_cache_then_private_worker_clone'){throw 'Worker bootstrap contract mismatch.'}

$loopFamilies=[ordered]@{
  geometric=@('harmonic_membrane','lattice_wave','parametric_ribbon','interference_plane','orbital_wave')
  fractal=@('radial_bloom','dendritic_tunnel','spiral_fractal','fractal_filigree','nested_worlds')
  sacred_symmetry=@('astrolabe','gear_train','polygon_orrery','origami_mandala','celestial_chart')
  living_particles=@('swarm','vortex','collision_cloud','organic_pulse','magnetic_filament_cloud')
  invisible_forces=@('dipole_field','vortex_field','saddle_field','quadrupole_field','gravitational_lens','topographic_basin','scalar_potential')
}
$familyFolders=[ordered]@{geometric='01_Geometric_Waves';fractal='02_Fractal_Bloom';sacred_symmetry='03_Sacred_Symmetry';living_particles='04_Living_Particles';invisible_forces='05_Invisible_Forces';tracking='06_Tracking';saccade='07_Saccade';pursuit='08_Pursuit';peripheral_scan='09_Peripheral_Scan'}
$loopTechnicalIds=@{geometric='geometric';fractal='fractal';sacred_symmetry='kaleidoscope';living_particles='particle_flow';invisible_forces='vector_field'}

$seeds=@($batchManifest.seeds | ForEach-Object {[int]$_})
if($seeds.Count -ne 5){throw "Expected exactly five review seeds, got $($seeds.Count)."}
$summary=[ordered]@{revision='2.19.12';status='PASS';generated_at_utc=(Get-Date).ToUniversalTime().ToString('o');workers=$Workers;max_observed_worker_concurrency=[int]$batchManifest.max_observed_worker_concurrency;expected_video_count=52;loops=0;drills=0;longforms=0;items=@()}

$loopIndex=0
foreach($familyKey in $loopFamilies.Keys){
  $folder=Join-Path $ReviewRoot $familyFolders[$familyKey]
  foreach($grammar in @($loopFamilies[$familyKey])){
    $seed=$seeds[$loopIndex % $seeds.Count]; $loopIndex++
    $matches=@(Get-ChildItem -LiteralPath $folder -File -Filter "*_seed_${seed}_${grammar}_manifest.json" -ErrorAction SilentlyContinue)
    if($matches.Count -ne 1){throw "Expected one loop manifest for $familyKey/$grammar seed=$seed; found $($matches.Count)."}
    $m=Read-Json $matches[0].FullName
    $expectedTechnicalId=[string]$loopTechnicalIds[$familyKey]
    if([string]$m.technical_id -ne [string]$expectedTechnicalId -or [string]$m.grammar_id -ne $grammar){throw "Loop manifest identity mismatch: $($matches[0].Name)"}
    $mp4=Resolve-LoopMediaPath $m $matches[0].FullName
    Assert-Media $mp4 690 23.0 "Loop $familyKey/$grammar/$seed"
    $summary.loops++
    $summary.items += [pscustomobject]@{kind='loop';family=$familyKey;grammar=$grammar;seed=$seed;mp4=$mp4}
  }
}

foreach($family in @('tracking','saccade','pursuit','peripheral_scan')){
  foreach($seed in $seeds){
    $folder=Join-Path $ReviewRoot $familyFolders[$family]
    $mp=Join-Path $folder "VisualDrill_${family}_seed_${seed}_manifest.json"
    if(-not(Test-Path -LiteralPath $mp)){throw "Missing drill manifest: $mp"}
    $m=Read-Json $mp
    $expectedGameplay=if($family -eq 'tracking'){21.0}else{17.0}
    $expectedTotal=if($family -eq 'tracking'){27.0}else{23.0}
    $expectedFrames=if($family -eq 'tracking'){810}else{690}
    if([int]$m.gameplay_frame_count -ne [int]($expectedGameplay*30)){throw "Drill gameplay frame mismatch: $mp"}
    if([math]::Abs([double]$m.total_duration_seconds-$expectedTotal) -gt 0.10){throw "Drill total duration mismatch: $mp"}
    if([int]$m.total_frame_count -ne $expectedFrames){throw "Drill presentation frames mismatch: $mp"}
    $video=Join-Path $folder "VisualDrill_${family}_seed_${seed}.mp4"
    Assert-Media $video $expectedFrames $expectedTotal "Drill $family/$seed"
    $summary.drills++
    $summary.items += [pscustomobject]@{kind='drill';family=$family;seed=$seed;mp4=$video}
  }
}

$familyIndex=0
$artisticNames=@{geometric='GeometricWaves';fractal='FractalBloom';sacred_symmetry='SacredSymmetry';living_particles='LivingParticles';invisible_forces='InvisibleForces'}
foreach($familyKey in $loopFamilies.Keys){
  $seed=$seeds[$familyIndex % $seeds.Count]; $familyIndex++
  $folder=Join-Path $ReviewRoot $familyFolders[$familyKey]
  $matches=@(Get-ChildItem -LiteralPath $folder -File -Filter "*$($artisticNames[$familyKey])_Longform_seed_${seed}_manifest.json" -ErrorAction SilentlyContinue)
  if($matches.Count -ne 1){throw "Expected one longform manifest for $familyKey seed=$seed; found $($matches.Count)."}
  $m=Read-Json $matches[0].FullName
  if([int]$m.fps -ne 30 -or [string]$m.resolution -ne '720x1280'){throw "Longform format metadata mismatch: $($matches[0].Name)"}
  Assert-Media (Join-Path $folder ([IO.Path]::GetFileName([string]$m.output_mp4))) 5400 180.0 "Longform $familyKey/$seed"
  $summary.longforms++
  $summary.items += [pscustomobject]@{kind='longform';family=$familyKey;seed=$seed;mp4=(Join-Path $folder ([IO.Path]::GetFileName([string]$m.output_mp4)))}
}

if($summary.loops -ne 27 -or $summary.drills -ne 20 -or $summary.longforms -ne 5){throw "Corpus count mismatch: loops=$($summary.loops), drills=$($summary.drills), longforms=$($summary.longforms)."}
$reportPath=Join-Path $ReviewRoot 'C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json'
[IO.File]::WriteAllText($reportPath,($summary|ConvertTo-Json -Depth 8),(New-Object Text.UTF8Encoding($false)))
Write-Host '[C11-C-COMPLETE-REVIEW] PASS - 52/52 videos validated (27 loops + 20 drills + 5 longforms).'
Write-Host "[C11-C-COMPLETE-REVIEW] Report: $reportPath"
