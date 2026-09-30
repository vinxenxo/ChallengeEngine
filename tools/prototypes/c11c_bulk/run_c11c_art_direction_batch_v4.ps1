param(
    [Parameter(Mandatory=$false)][string]$ReviewRoot='',
    [ValidateRange(1,7)][int]$Workers=7,
    [int[]]$Seeds=@(),
    [switch]$ExportGif,
    [switch]$NoSound,
    [switch]$Reset,
    [switch]$Resume,
    [switch]$Loops,
    [switch]$Drills,
    [switch]$Longforms,
    [switch]$All
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
if($Reset -and $Resume){ throw 'Use either -Reset or -Resume, not both.' }
$selection=[ordered]@{loops=[bool]$Loops;drills=[bool]$Drills;longforms=[bool]$Longforms}
if($All -or (-not $Loops -and -not $Drills -and -not $Longforms)){ $selection.loops=$true; $selection.drills=$true; $selection.longforms=$true }

$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
. (Join-Path $PSScriptRoot 'C11CProductionBatchCommon.ps1')
. (Join-Path $PSScriptRoot 'C11CReviewWorkerIsolation.ps1')
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
        # 2.16.9 remains the authoritative Visual Loop review-contract revision; 2.19.4
        # changes only orchestration isolation and repository/tooling provenance.
        if([string]$existingState.revision -eq '2.16.9'){
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
        revision='2.16.9'
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
    param([string]$FamilyId,[string]$Grammar,[int]$Seed,[string]$FamilyRoot,[int]$WorkerSlot,[string]$WorkerRoot)
    $launcherRelative=Join-Path ("tools\prototypes\$FamilyId") 'run_prototype.ps1'
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
    $runnerArgs=@('-Seed',$Seed,'-Grammar',$Grammar,'-Duration','23','-OutputRoot',$FamilyRoot,'-OutputTag',$Grammar)
    if($NoSound){$runnerArgs += '-NoSound'}
    if($ExportGif){$runnerArgs += '-ExportGif'}
    $job=Start-Job -ScriptBlock {
        param($WorkerRoot,$LauncherRelative,$RunnerArgs,$AuthoringOutputPath,$WorkerSlot,$FamilyId,$Grammar,$Seed)
        Set-Location $WorkerRoot
        $env:C11C_REVIEW_WORKER_SLOT=[string]$WorkerSlot
        $env:C11C_AUTHORING_OUTPUT_PATH=[System.IO.Path]::GetFullPath($AuthoringOutputPath)
        $activityMarker=Join-Path $WorkerRoot '.c11c_worker_active'
        [System.IO.File]::WriteAllText($activityMarker,(Get-Date).ToString('o'),(New-Object System.Text.UTF8Encoding($false)))
        $workerLauncher=Join-Path $WorkerRoot $LauncherRelative
        if(-not(Test-Path -LiteralPath $workerLauncher)){throw "Worker launcher missing: $workerLauncher"}
        try {
            Write-Host "[C11-C-WORKER] slot=$WorkerSlot family=$FamilyId grammar=$Grammar seed=$Seed root=$WorkerRoot"
            & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $workerLauncher @RunnerArgs
            if($LASTEXITCODE -ne 0){throw "Review render failed: exit=$LASTEXITCODE"}
        } finally {
            Remove-Item -LiteralPath $activityMarker -Force -ErrorAction SilentlyContinue
        }
    } -ArgumentList $WorkerRoot,$launcherRelative,$runnerArgs,$authoringOutputPath,$WorkerSlot,$FamilyId,$Grammar,$Seed
    $job | Add-Member NoteProperty C11Family $FamilyId
    $job | Add-Member NoteProperty C11Grammar $Grammar
    $job | Add-Member NoteProperty C11Seed $Seed
    $job | Add-Member NoteProperty C11WorkerSlot $WorkerSlot
    $job | Add-Member NoteProperty C11WorkerRoot $WorkerRoot
    return $job
}

Write-Host '[C11-C-ART-DIRECTION] =========================================='
Write-Host '[C11-C-ART-DIRECTION] REVIEW V9 - 7-worker isolated / grouped / resumable / isolated artifacts'
Write-Host "[C11-C-ART-DIRECTION] Root: $ReviewRoot"
Write-Host "[C11-C-ART-DIRECTION] Workers: $Workers | seeds: $($Seeds.Count) | GIF=$ExportGif | Resume=$Resume | Loops=$($selection.loops) | Drills=$($selection.drills) | Longforms=$($selection.longforms)"
Write-Host '[C11-C-ART-DIRECTION] AVI temporary by default; GIF opt-in.'
Write-Host '============================================================'

if($selection.loops){
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
        Write-Host "[C11-C-ART-DIRECTION] RESUME PLAN - $($loopTasks.Count) loop(s) pending; completed artifacts will be skipped."
    }
    $workerPool=New-C11CReviewWorkerPool -ProjectRoot $ProjectRoot -Count $Workers
    $maxObservedWorkerConcurrency=0
    try {
        $active=@()
        $nextTaskIndex=0
        while($nextTaskIndex -lt $loopTasks.Count -or $active.Count -gt 0){
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
            $active=@($active | Where-Object {$_.State -notin @('Completed','Failed','Stopped')})
            $currentWorkerConcurrency=0
            foreach($worker in @($workerPool.Workers)){
                if(Test-Path -LiteralPath (Join-Path ([string]$worker.Root) '.c11c_worker_active')){ $currentWorkerConcurrency++ }
            }
            if($currentWorkerConcurrency -gt $maxObservedWorkerConcurrency){
                $maxObservedWorkerConcurrency=$currentWorkerConcurrency
                Write-Host "[C11-C-WORKER] observed_concurrency=$maxObservedWorkerConcurrency"
            }

            while($active.Count -lt $Workers -and $nextTaskIndex -lt $loopTasks.Count){
                $task=$loopTasks[$nextTaskIndex]
                $slot=-1
                for($candidate=0;$candidate -lt $workerPool.Workers.Count;$candidate++){
                    if(-not(@($active | Where-Object {$_.C11WorkerSlot -eq $candidate}).Count)){ $slot=$candidate; break }
                }
                if($slot -lt 0){break}
                $workerRoot=[string]$workerPool.Workers[$slot].WorkerRoot
                $active += Start-LoopReviewJob -FamilyId $task.FamilyId -Grammar $task.Grammar -Seed $task.Seed -FamilyRoot $task.FamilyRoot -WorkerSlot $slot -WorkerRoot $workerRoot
                $nextTaskIndex++
            }

            if($active.Count -gt 0){ Start-Sleep -Milliseconds 350 }
        }
    } finally {
        foreach($job in @($active)){
            if($job.State -eq 'Running'){ Stop-Job $job -ErrorAction SilentlyContinue }
            if($job.State -in @('Completed','Failed','Stopped')){ Remove-Job $job -Force -ErrorAction SilentlyContinue }
        }
        Remove-C11CReviewWorkerPool -Pool ([string]$workerPool.Root)
    }
    if($loopTasks.Count -gt 1 -and $Workers -gt 1){
        if($maxObservedWorkerConcurrency -lt 2){
            throw "Parallel review contract failed: Workers=$Workers but maximum observed worker concurrency was $maxObservedWorkerConcurrency."
        }
        Write-Host "[C11-C-WORKER] MAX_OBSERVED_CONCURRENCY=$maxObservedWorkerConcurrency"
    }
}

if($selection.longforms){
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

}

if($selection.drills){
    $drillStage=Join-Path $ReviewRoot '_drill_stage'
    if($Resume -and (Test-DrillsComplete -Root $ReviewRoot)){
        Write-Host '[C11-C-ART-DIRECTION] RESUME SKIP drills - complete.'
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

}

$manifest=[ordered]@{
    schema='C11-C-ART-DIRECTION-REVIEW-CORPUS-V5'
    revision='2.19.12'
    status='COMPLETE'
    selected_stages=$selection
    root=$ReviewRoot
    workers=$Workers
    worker_isolation='per_worker_temporary_godot_project'
    worker_bootstrap='source_project_godot_class_cache_then_private_worker_clone'
    worker_global_script_class_cache='required_per_worker'
    max_observed_worker_concurrency=if($selection.loops){$maxObservedWorkerConcurrency}else{0}
    seeds=@($Seeds)
    resume_enabled=$true
    gif_enabled=[bool]$ExportGif
    avi_retained=$false
    final_structure='family-flat'
    loop_duration_policy='23s review capture; source visual production manifests remain revision 2.16.3'
    longform_duration='180s'
    longform_transition='dissolve continuity; never through black'
    longform_final_fade='1s to black'
    family_folders=$familyFolder
    loop_families=@($loopFamilies.Keys)
    drill_families=@('tracking','saccade','pursuit','peripheral_scan')
}
[System.IO.File]::WriteAllText((Join-Path $ReviewRoot 'C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'),($manifest|ConvertTo-Json -Depth 10),(New-Object System.Text.UTF8Encoding($false)))
Write-Host "[C11-C-ART-DIRECTION] COMPLETE - grouped review root: $ReviewRoot"
