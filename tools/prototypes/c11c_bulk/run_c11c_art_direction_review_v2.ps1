param(
    [Parameter(Mandatory=$false)][string]$ReviewRoot='',
    [ValidateRange(1,4)][int]$Workers=1,
    [int[]]$Seeds=@(),
    [switch]$ExportGif,
    [switch]$NoSound,
    [switch]$Reset
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
. (Join-Path $PSScriptRoot 'C11CProductionBatchCommon.ps1')
if([string]::IsNullOrWhiteSpace($ReviewRoot)){ $ReviewRoot=Join-Path $ProjectRoot 'artifacts\prototypes\c11c_art_direction_review' }
if($Seeds.Count -eq 0){ $Seeds=New-C11CUniqueSeeds -Count 5 }
if($Seeds.Count -ne 5){ throw 'Art-direction review expects exactly five high-spread seeds.' }
Assert-C11CSeedSpacing -Seeds ([int[]]$Seeds)
if($Reset -and (Test-Path -LiteralPath $ReviewRoot)){Remove-Item -LiteralPath $ReviewRoot -Recurse -Force}
New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null

$loopFamilies=[ordered]@{
    geometric='c11c_geometric_waves_v1'; fractal='c11c_fractal_bloom_v1'; sacred_symmetry='c11c_sacred_symmetry_v1'; living_particles='c11c_living_particles_v1'; invisible_forces='c11c_invisible_forces_v1'
}
$loopGrammars=@{
    geometric=@('harmonic_membrane','lattice_wave','parametric_ribbon','interference_plane','orbital_wave');
    fractal=@('radial_bloom','dendritic_tunnel','spiral_fractal','fractal_filigree','nested_worlds');
    sacred_symmetry=@('astrolabe','gear_train','polygon_orrery','origami_mandala','celestial_chart');
    living_particles=@('swarm','vortex','collision_cloud','organic_pulse','magnetic_filament_cloud');
    invisible_forces=@('dipole_field','vortex_field','saddle_field','quadrupole_field','gravitational_lens','topographic_basin','scalar_potential')
}
$familyFolder=[ordered]@{geometric='01_Geometric_Waves';fractal='02_Fractal_Bloom';sacred_symmetry='03_Sacred_Symmetry';living_particles='04_Living_Particles';invisible_forces='05_Invisible_Forces';tracking='06_Tracking';saccade='07_Saccade';pursuit='08_Pursuit';peripheral_scan='09_Peripheral_Scan'}

function Start-LoopReviewJob {
    param([string]$FamilyId,[string]$Grammar,[int]$Seed,[string]$FamilyRoot)
    $launcher=Join-Path $ProjectRoot ("tools\prototypes\$FamilyId\run_prototype.ps1")
    $childArgs=@('-NoProfile','-ExecutionPolicy','Bypass','-File',$launcher,'-Seed',$Seed,'-Grammar',$Grammar,'-Duration','23','-OutputRoot',$FamilyRoot)
    if($NoSound){$childArgs += '-NoSound'}
    if($ExportGif){$childArgs += '-ExportGif'}
    return Start-Job -ScriptBlock {
        param($ChildArgs,$Root)
        Set-Location $Root
        & powershell.exe @ChildArgs
        if($LASTEXITCODE -ne 0){throw "Review render failed: exit=$LASTEXITCODE"}
    } -ArgumentList (,$childArgs),$ProjectRoot
}

Write-Host '[C11-C-ART-DIRECTION] =========================================='
Write-Host '[C11-C-ART-DIRECTION] REVIEW V2 — grouped by family'
Write-Host "[C11-C-ART-DIRECTION] Root: $ReviewRoot"
Write-Host "[C11-C-ART-DIRECTION] Workers: $Workers | seeds: $($Seeds.Count) | GIF=$ExportGif"
Write-Host '[C11-C-ART-DIRECTION] Final review structure is family-flat; AVI is temporary by default.'
Write-Host '[C11-C-ART-DIRECTION] Longform and Drill stages are serialized after Visual Loop workers.'
Write-Host '============================================================'

$active=@()
$loopIndex=0
foreach($familyKey in $loopFamilies.Keys){
    $familyRoot=Join-Path $ReviewRoot $familyFolder[$familyKey]
    New-Item -ItemType Directory -Force -Path $familyRoot | Out-Null
    foreach($grammar in @($loopGrammars[$familyKey])){
        $seed=[int]$Seeds[$loopIndex % $Seeds.Count]
        $loopIndex++
        $active += Start-LoopReviewJob -FamilyId ([string]$loopFamilies[$familyKey]) -Grammar $grammar -Seed $seed -FamilyRoot $familyRoot
        while(@($active | Where-Object {$_.State -eq 'Running'}).Count -ge $Workers){
            Start-Sleep -Milliseconds 350
            foreach($done in @($active | Where-Object {$_.State -in @('Completed','Failed','Stopped')})){
                if($done.State -ne 'Completed'){Receive-Job $done -ErrorAction Continue | Out-Host; Remove-Job $done -Force; throw 'Parallel Visual Loop review render failed.'}
                Receive-Job $done -ErrorAction Stop | Out-Host; Remove-Job $done -Force
            }
            $active=@($active | Where-Object {$_.State -eq 'Running'})
        }
    }
}
while($active.Count -gt 0){
    Start-Sleep -Milliseconds 350
    foreach($done in @($active | Where-Object {$_.State -in @('Completed','Failed','Stopped')})){
        if($done.State -ne 'Completed'){Receive-Job $done -ErrorAction Continue | Out-Host; Remove-Job $done -Force; throw 'Parallel Visual Loop review render failed.'}
        Receive-Job $done -ErrorAction Stop | Out-Host; Remove-Job $done -Force
    }
    $active=@($active | Where-Object {$_.State -eq 'Running'})
}

$longformStage=Join-Path $ReviewRoot '_longform_stage'
$familyIndex=0
foreach($familyKey in $loopFamilies.Keys){
    $seed=[int]$Seeds[$familyIndex % $Seeds.Count]; $familyIndex++
    & (Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_loop_longform_production.ps1') -Family $loopFamilies[$familyKey] -Seed $seed -OutputRoot $longformStage -Force
    if(-not $?){throw "Longform failed: $familyKey"}
    $src=Join-Path $longformStage $loopFamilies[$familyKey]
    $dest=Join-Path $ReviewRoot $familyFolder[$familyKey]
    foreach($item in @(Get-ChildItem -LiteralPath $src -Recurse -File | Where-Object { $_.Extension -eq '.mp4' -or $_.Name -like '*_social.txt' -or $_.Name -like '*_manifest.json' })){
        if($item.Extension -eq '.mp4' -or $item.Name -like '*_Longform_seed_*_social.txt' -or $item.Name -like '*_Longform_seed_*_manifest.json'){Copy-Item -LiteralPath $item.FullName -Destination $dest -Force}
    }
}
if(Test-Path -LiteralPath $longformStage){Remove-Item -LiteralPath $longformStage -Recurse -Force}

$drillStage=Join-Path $ReviewRoot '_drill_stage'
$drillArgs=@('-Seeds',$Seeds,'-ReviewRootOverride',$drillStage)
if($NoSound){$drillArgs += '-NoSound'}
if($ExportGif){$drillArgs += '-ExportGif'}
& (Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1') @drillArgs
if(-not $?){throw 'Visual Drill review stage failed.'}
foreach($family in @('tracking','saccade','pursuit','peripheral_scan')){
    $dest=Join-Path $ReviewRoot $familyFolder[$family]; New-Item -ItemType Directory -Force -Path $dest | Out-Null
    foreach($seed in $Seeds){
        $src=Join-Path $drillStage "$family\seed_$seed"
        if(-not(Test-Path -LiteralPath $src)){throw "Missing drill review folder: $src"}
        foreach($item in @(Get-ChildItem -LiteralPath $src -File | Where-Object { $_.Extension -eq '.mp4' -or $_.Name -like '*_social.txt' -or $_.Name -like '*_manifest.json' -or $_.Name -eq 'contact_sheet.jpg' -or $_.Name -like 'frame_*.png' })){
            Copy-Item -LiteralPath $item.FullName -Destination $dest -Force
        }
    }
}
if(Test-Path -LiteralPath $drillStage){Remove-Item -LiteralPath $drillStage -Recurse -Force}

$manifest=[ordered]@{
    schema='C11-C-ART-DIRECTION-REVIEW-CORPUS-V2'; revision='2.15.0'; status='COMPLETE'; root=$ReviewRoot; workers=$Workers; seeds=@($Seeds); gif_enabled=[bool]$ExportGif; avi_retained=$false
    final_structure='family-flat'; loop_duration_policy='20..23s; extraordinary review uses 23s for visual comparison'; longform_duration='180s'; longform_transition='crossfade continuity; never through black'; longform_final_fade='1s to black'
    family_folders=$familyFolder; loop_families=@($loopFamilies.Keys); drill_families=@('tracking','saccade','pursuit','peripheral_scan')
}
[System.IO.File]::WriteAllText((Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'),($manifest|ConvertTo-Json -Depth 10),(New-Object System.Text.UTF8Encoding($false)))
Write-Host "[C11-C-ART-DIRECTION] COMPLETE — grouped review root: $ReviewRoot"
