param(
    [Parameter(Mandatory=$false)][string]$ReviewRoot='',
    [ValidateRange(1,7)][int]$Workers=7,
    [int[]]$Seeds=@(),
    [switch]$ExportGif,
    [switch]$NoSound,
    [switch]$Reset,
    [switch]$Resume
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
if($Reset -and $Resume){ throw 'Use either -Reset or -Resume, not both.' }
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
. (Join-Path $PSScriptRoot 'C11CProductionBatchCommon.ps1')
if([string]::IsNullOrWhiteSpace($ReviewRoot)){ $ReviewRoot=Join-Path $ProjectRoot 'artifacts\prototypes\c11c_art_direction_review' }
if($Reset -and (Test-Path -LiteralPath $ReviewRoot)){Remove-Item -LiteralPath $ReviewRoot -Recurse -Force}
if($Resume -and -not (Test-Path -LiteralPath $ReviewRoot)){ throw "Cannot resume: review root does not exist: $ReviewRoot" }
New-Item -ItemType Directory -Force -Path $ReviewRoot | Out-Null
$statePath=Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_STATE.json'
$completedLoops=@{}
$completedLongforms=@{}
$drillsComplete=$false

if($Resume -and (Test-Path -LiteralPath $statePath)){
    try{
        $existingState=Get-Content -Raw -LiteralPath $statePath | ConvertFrom-Json
        if($existingState.seeds){ $Seeds=@($existingState.seeds | ForEach-Object {[int]$_}) }
        # Only reuse the completion ledger when it belongs to this exact review revision.
        # Older 2.16.x ledgers remain useful for seed recovery but must not hide new art changes.
        if([string]$existingState.revision -eq '2.16.3'){
            if($existingState.completed_loops){ foreach($item in @($existingState.completed_loops)){ $completedLoops[[string]$item]=$true } }
            if($existingState.completed_longforms){ foreach($item in @($existingState.completed_longforms)){ $completedLongforms[[string]$item]=$true } }
            $drillsComplete=[bool]$existingState.drills_complete
        }
    }catch{
        Write-Warning "Existing review state could not be parsed; artifact recovery will be attempted: $statePath"
    }
}
if($Resume -and $Seeds.Count -eq 0){
    $resumeManifestPath=Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'
    if(Test-Path -LiteralPath $resumeManifestPath){
        try{
            $resumeManifest=Get-Content -Raw -LiteralPath $resumeManifestPath | ConvertFrom-Json
            $Seeds=@($resumeManifest.seeds | ForEach-Object {[int]$_})
        }catch{
            throw "Cannot recover review seeds from existing manifest: $resumeManifestPath"
        }
    }
}
if($Resume -and $Seeds.Count -eq 0){
    $seedCandidates=@()
    Get-ChildItem -LiteralPath $ReviewRoot -Recurse -File -Filter '*_seed_*_manifest.json' -ErrorAction SilentlyContinue | ForEach-Object {
        if($_.Name -match '_seed_(\d+)_manifest\.json$'){ $seedCandidates += [int]$Matches[1] }
    }
    $Seeds=@($seedCandidates | Sort-Object -Unique | Select-Object -First 5)
}
if($Seeds.Count -eq 0){ $Seeds=New-C11CUniqueSeeds -Count 5 }
if($Seeds.Count -ne 5){ throw 'Art-direction review expects exactly five high-spread seeds.' }
Assert-C11CSeedSpacing -Seeds ([int[]]$Seeds)

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
$familyFolder=[ordered]@{
    geometric='01_Geometric_Waves'; fractal='02_Fractal_Bloom'; sacred_symmetry='03_Sacred_Symmetry';
    living_particles='04_Living_Particles'; invisible_forces='05_Invisible_Forces';
    tracking='06_Tracking'; saccade='07_Saccade'; pursuit='08_Pursuit'; peripheral_scan='09_Peripheral_Scan'
}

# Resume recovery: rebuild the completion ledger from final artifacts even if the prior
# process died before the global corpus manifest was written.
if($Resume){
    $loopRecoveryIndex=0
    foreach($familyKey in $loopFamilies.Keys){
        $familyRoot=Join-Path $ReviewRoot $familyFolder[$familyKey]
        foreach($grammarValue in @($loopGrammars[$familyKey])){
            $grammar=[string]$grammarValue
            $seed=[int]$Seeds[$loopRecoveryIndex % $Seeds.Count]
            $loopRecoveryIndex++
            if(Test-LoopComplete -FamilyKey $familyKey -FamilyRoot $familyRoot -Grammar $grammar -Seed $seed){
                $completedLoops["$familyKey/$grammar/$seed"]=$true
            }
        }
    }
    $familyIndex=0
    foreach($familyKey in $loopFamilies.Keys){
        $seed=[int]$Seeds[$familyIndex % $Seeds.Count]
        $familyIndex++
        $dest=Join-Path $ReviewRoot $familyFolder[$familyKey]
        if(Test-LongformComplete -FamilyKey $familyKey -FamilyRoot $dest -Seed $seed){ $completedLongforms["$familyKey/$seed"]=$true }
    }
    if(Test-DrillsComplete -Root $ReviewRoot){ $drillsComplete=$true }
}

function Save-State {
    param([string]$Stage,[string]$Key,[string]$Status)
    if($Status -in @('COMPLETE','SKIP_EXISTING')){
        if($Stage -eq 'LOOPS'){ $completedLoops[$Key]=$true }
        elseif($Stage -eq 'LONGFORM'){ $completedLongforms[$Key]=$true }
        elseif($Stage -eq 'DRILLS'){ $script:drillsComplete=$true }
    }
    $state=[ordered]@{
        schema='C11-C-ART-DIRECTION-REVIEW-STATE-V5'
        revision='2.16.3'
        status=$Stage
        updated=(Get-Date).ToString('o')
        workers=$Workers
        seeds=@($Seeds)
        resume_enabled=$true
        completed_loops=@($completedLoops.Keys | Sort-Object)
        completed_longforms=@($completedLongforms.Keys | Sort-Object)
        drills_complete=$drillsComplete
        last_item=[ordered]@{key=$Key;status=$Status}
    }
    $tmp=$statePath+'.tmp'
    [System.IO.File]::WriteAllText($tmp,($state|ConvertTo-Json -Depth 10),(New-Object System.Text.UTF8Encoding($false)))
    Move-Item -LiteralPath $tmp -Destination $statePath -Force
}

function Test-LoopComplete {
    param([string]$FamilyKey,[string]$FamilyRoot,[string]$Grammar,[int]$Seed)
    $key="$FamilyKey/$Grammar/$Seed"
    if(-not(Test-Path -LiteralPath $FamilyRoot)){return $false}
    foreach($m in @(Get-ChildItem -LiteralPath $FamilyRoot -File -Filter "*_seed_${Seed}_${Grammar}_manifest.json" -ErrorAction SilentlyContinue)){
        try{
            $x=Get-Content -Raw -LiteralPath $m.FullName | ConvertFrom-Json
            if([string]$x.grammar_id -eq $Grammar -and [string]$x.revision -eq '2.16.3'){
                $stem=$m.FullName -replace '_manifest\.json$',''
                return (Test-Path -LiteralPath ($stem+'.mp4')) -and (Test-Path -LiteralPath ($stem+'_social.txt'))
            }
        }catch{}
    }
    return $false
}

function Test-LongformComplete {
    param([string]$FamilyKey,[string]$FamilyRoot,[int]$Seed)
    $key="$FamilyKey/$Seed"
    if(-not(Test-Path -LiteralPath $FamilyRoot)){return $false}
    foreach($m in @(Get-ChildItem -LiteralPath $FamilyRoot -File -Filter "*_Longform_seed_${Seed}_manifest.json" -ErrorAction SilentlyContinue)){
        try{
            $x=Get-Content -Raw -LiteralPath $m.FullName | ConvertFrom-Json
            if([string]$x.revision -eq '2.16.3' -and [string]$x.composition_model -eq 'dissolve_continuity_v3' -and [double]$x.duration_seconds -eq 180.0){
                $stem=$m.FullName -replace '_manifest\.json$',''
                return (Test-Path -LiteralPath ($stem+'.mp4')) -and (Test-Path -LiteralPath ($stem+'_social.txt'))
            }
        }catch{}
    }
    return $false
}

function Test-DrillsComplete {
    param([string]$Root)
    foreach($family in @('tracking','saccade','pursuit','peripheral_scan')){
        $dest=Join-Path $Root $familyFolder[$family]
        foreach($seed in $Seeds){
            $m=Join-Path $dest "VisualDrill_${family}_seed_${seed}_manifest.json"
            $mp4=Join-Path $dest "VisualDrill_${family}_seed_${seed}.mp4"
            if(-not(Test-Path -LiteralPath $m) -or -not(Test-Path -LiteralPath $mp4)){return $false}
            try{
                $manifest=Get-Content -Raw -LiteralPath $m | ConvertFrom-Json
                if([string]$manifest.revision -ne '2.16.3'){return $false}
            }catch{return $false}
        }
    }
    return $true
}

function Start-LoopReviewJob {
    param([string]$FamilyId,[string]$Grammar,[int]$Seed,[string]$FamilyRoot)
    $launcher=Join-Path $ProjectRoot ("tools\prototypes\$FamilyId\run_prototype.ps1")
    # Invisible Forces has seven grammars and therefore reuses five seeds. The grammar tag
    # must be part of every filename so concurrent workers can never delete/overwrite each
    # other's authoring, manifest, social or MP4 artifacts.
    $stemPrefix=switch($FamilyId){
        'c11c_geometric_waves_v1' { 'GeometricWaves_v1' }
        'c11c_fractal_bloom_v1' { 'FractalBloom_v1' }
        'c11c_sacred_symmetry_v1' { 'SacredSymmetry_v1' }
        'c11c_living_particles_v1' { 'LivingParticles_v1' }
        'c11c_invisible_forces_v1' { 'InvisibleForces_v1' }
        default { throw "Unsupported review family id: $FamilyId" }
    }
    $outputTagSafe=if([string]::IsNullOrWhiteSpace($Grammar)){ '' } else { '_' + ($Grammar -replace '[^A-Za-z0-9_-]','_') }
    $reviewStem="${stemPrefix}_seed_${Seed}${outputTagSafe}"
    $authoringOutputPath=Join-Path $FamilyRoot ($reviewStem + '_authoring.json')
    $childArgs=@('-NoProfile','-ExecutionPolicy','Bypass','-File',$launcher,'-Seed',$Seed,'-Grammar',$Grammar,'-Duration','23','-OutputRoot',$FamilyRoot,'-OutputTag',$Grammar)
    if($NoSound){$childArgs += '-NoSound'}
    if($ExportGif){$childArgs += '-ExportGif'}
    $job=Start-Job -ScriptBlock {
        param($ChildArgs,$Root,$AuthoringOutputPath)
        Set-Location $Root
        # Explicit per-worker authoring path. This is intentionally scoped to the child
        # process so OutputRoot + grammar tag remain isolated under seven concurrent workers.
        $env:C11C_AUTHORING_OUTPUT_PATH=[System.IO.Path]::GetFullPath($AuthoringOutputPath)
        & powershell.exe @ChildArgs
        if($LASTEXITCODE -ne 0){throw "Review render failed: exit=$LASTEXITCODE"}
    } -ArgumentList (,$childArgs),$ProjectRoot,$authoringOutputPath
    $job | Add-Member NoteProperty C11Family $FamilyId
    $job | Add-Member NoteProperty C11Grammar $Grammar
    $job | Add-Member NoteProperty C11Seed $Seed
    return $job
}

Write-Host '[C11-C-ART-DIRECTION] =========================================='
Write-Host '[C11-C-ART-DIRECTION] REVIEW V5 — grouped by family / resumable / isolated artifacts'
Write-Host "[C11-C-ART-DIRECTION] Root: $ReviewRoot"
Write-Host "[C11-C-ART-DIRECTION] Workers: $Workers | seeds: $($Seeds.Count) | GIF=$ExportGif | Resume=$Resume"
Write-Host '[C11-C-ART-DIRECTION] AVI temporary by default; GIF opt-in.'
Write-Host '============================================================'

$loopTasks=@()
$loopIndex=0
foreach($familyKey in $loopFamilies.Keys){
    $familyRoot=Join-Path $ReviewRoot $familyFolder[$familyKey]
    New-Item -ItemType Directory -Force -Path $familyRoot | Out-Null
    foreach($grammarValue in @($loopGrammars[$familyKey])){
        $grammar=[string]$grammarValue
        $seed=[int]$Seeds[$loopIndex % $Seeds.Count]
        $loopIndex++
        if($Resume -and (Test-LoopComplete -FamilyKey $familyKey -FamilyRoot $familyRoot -Grammar $grammar -Seed $seed)){
            Write-Host "[C11-C-ART-DIRECTION] RESUME SKIP loop $familyKey/$grammar seed=$seed"
            Save-State -Stage 'LOOPS' -Key "$familyKey/$grammar/$seed" -Status 'SKIP_EXISTING'
            continue
        }
        $loopTasks += [pscustomobject]@{FamilyKey=$familyKey;FamilyId=[string]$loopFamilies[$familyKey];Grammar=$grammar;Seed=$seed;FamilyRoot=$familyRoot}
    }
}
if($Resume){
    Write-Host "[C11-C-ART-DIRECTION] RESUME PLAN — $($loopTasks.Count) loop(s) pending; completed artifacts will be skipped."
}
$active=@()
foreach($task in @($loopTasks)){
    $active += Start-LoopReviewJob -FamilyId $task.FamilyId -Grammar $task.Grammar -Seed $task.Seed -FamilyRoot $task.FamilyRoot
    while(@($active | Where-Object {$_.State -eq 'Running'}).Count -ge $Workers){
        Start-Sleep -Milliseconds 350
        foreach($done in @($active | Where-Object {$_.State -in @('Completed','Failed','Stopped')})){
            if($done.State -ne 'Completed'){
                Receive-Job $done -ErrorAction Continue | Out-Host
                Remove-Job $done -Force
                throw "Parallel Visual Loop review render failed: $($done.C11Family)/$($done.C11Grammar)/$($done.C11Seed)"
            }
            Receive-Job $done -ErrorAction Stop | Out-Host
            Save-State -Stage 'LOOPS' -Key "$($done.C11Family)/$($done.C11Grammar)/$($done.C11Seed)" -Status 'COMPLETE'
            Remove-Job $done -Force
        }
        $active=@($active | Where-Object {$_.State -eq 'Running'})
    }
}
while($active.Count -gt 0){
    Start-Sleep -Milliseconds 350
    foreach($done in @($active | Where-Object {$_.State -in @('Completed','Failed','Stopped')})){
        if($done.State -ne 'Completed'){
            Receive-Job $done -ErrorAction Continue | Out-Host
            Remove-Job $done -Force
            throw "Parallel Visual Loop review render failed: $($done.C11Family)/$($done.C11Grammar)/$($done.C11Seed)"
        }
        Receive-Job $done -ErrorAction Stop | Out-Host
        Save-State -Stage 'LOOPS' -Key "$($done.C11Family)/$($done.C11Grammar)/$($done.C11Seed)" -Status 'COMPLETE'
        Remove-Job $done -Force
    }
    $active=@($active | Where-Object {$_.State -eq 'Running'})
}

$longformStage=Join-Path $ReviewRoot '_longform_stage'
$familyIndex=0
foreach($familyKey in $loopFamilies.Keys){
    $seed=[int]$Seeds[$familyIndex % $Seeds.Count]
    $familyIndex++
    $dest=Join-Path $ReviewRoot $familyFolder[$familyKey]
    if($Resume -and (Test-LongformComplete -FamilyKey $familyKey -FamilyRoot $dest -Seed $seed)){
        Write-Host "[C11-C-ART-DIRECTION] RESUME SKIP longform $familyKey seed=$seed"
        Save-State -Stage 'LONGFORM' -Key "$familyKey/$seed" -Status 'SKIP_EXISTING'
        continue
    }
    New-Item -ItemType Directory -Force -Path $longformStage | Out-Null
    & (Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_loop_longform_production.ps1') -Family $loopFamilies[$familyKey] -Seed $seed -OutputRoot $longformStage -Force
    if(-not $?){throw "Longform failed: $familyKey"}
    $src=Join-Path $longformStage $loopFamilies[$familyKey]
    foreach($item in @(Get-ChildItem -LiteralPath $src -Recurse -File | Where-Object { $_.Extension -eq '.mp4' -or $_.Name -like '*_social.txt' -or $_.Name -like '*_manifest.json' })){
        Copy-Item -LiteralPath $item.FullName -Destination $dest -Force
    }
    if(Test-Path -LiteralPath $src){Remove-Item -LiteralPath $src -Recurse -Force}
    Save-State -Stage 'LONGFORM' -Key "$familyKey/$seed" -Status 'COMPLETE'
}
if(Test-Path -LiteralPath $longformStage){Remove-Item -LiteralPath $longformStage -Recurse -Force}

$drillStage=Join-Path $ReviewRoot '_drill_stage'
if($Resume -and (Test-DrillsComplete -Root $ReviewRoot)){
    Write-Host '[C11-C-ART-DIRECTION] RESUME SKIP drills — complete.'
    Save-State -Stage 'DRILLS' -Key 'all' -Status 'SKIP_EXISTING'
} else {
    $drillParams=@{
        Seeds = [int[]]$Seeds
        ReviewRootOverride = $drillStage
    }
    if($NoSound){$drillParams.NoSound=$true}
    if($ExportGif){$drillParams.ExportGif=$true}
    & (Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1') @drillParams
    if(-not $?){throw 'Visual Drill review stage failed.'}
    foreach($family in @('tracking','saccade','pursuit','peripheral_scan')){
        $dest=Join-Path $ReviewRoot $familyFolder[$family]
        New-Item -ItemType Directory -Force -Path $dest | Out-Null
        foreach($seed in $Seeds){
            $src=Join-Path $drillStage "$family\seed_$seed"
            if(-not(Test-Path -LiteralPath $src)){throw "Missing drill review folder: $src"}
            foreach($item in @(Get-ChildItem -LiteralPath $src -File | Where-Object { $_.Extension -eq '.mp4' -or $_.Name -like '*_social.txt' -or $_.Name -like '*_manifest.json' -or $_.Name -eq 'contact_sheet.jpg' -or $_.Name -like 'frame_*.png' })){
                Copy-Item -LiteralPath $item.FullName -Destination $dest -Force
            }
        }
    }
    if(Test-Path -LiteralPath $drillStage){Remove-Item -LiteralPath $drillStage -Recurse -Force}
    Save-State -Stage 'DRILLS' -Key 'all' -Status 'COMPLETE'
}

$manifest=[ordered]@{
    schema='C11-C-ART-DIRECTION-REVIEW-CORPUS-V5'
    revision='2.16.3'
    status='COMPLETE'
    root=$ReviewRoot
    workers=$Workers
    seeds=@($Seeds)
    resume_enabled=$true
    gif_enabled=[bool]$ExportGif
    avi_retained=$false
    final_structure='family-flat'
    loop_duration_policy='20..23s; extraordinary review uses 23s for visual comparison'
    longform_duration='180s'
    longform_transition='dissolve continuity; never through black'
    longform_final_fade='1s to black'
    family_folders=$familyFolder
    loop_families=@($loopFamilies.Keys)
    drill_families=@('tracking','saccade','pursuit','peripheral_scan')
}
[System.IO.File]::WriteAllText((Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'),($manifest|ConvertTo-Json -Depth 10),(New-Object System.Text.UTF8Encoding($false)))
Write-Host "[C11-C-ART-DIRECTION] COMPLETE — grouped review root: $ReviewRoot"
