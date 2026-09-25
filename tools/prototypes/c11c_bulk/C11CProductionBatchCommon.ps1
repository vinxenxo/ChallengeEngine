param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path

function Get-C11CProductionSchedule {
    return @(
        # Monday
        @{ Day='Lunes'; DayIndex=1; Slot=1; Family='geometric'; Artistic='Geometric Waves'; Production='c11c_geometric_waves_v1'; Grammar='harmonic_membrane'; GrammarName='Harmonic Membrane' }
        @{ Day='Lunes'; DayIndex=1; Slot=2; Family='fractal'; Artistic='Fractal Bloom'; Production='c11c_fractal_bloom_v1'; Grammar='radial_bloom'; GrammarName='Radial Bloom' }
        @{ Day='Lunes'; DayIndex=1; Slot=3; Family='sacred_symmetry'; Artistic='Sacred Symmetry'; Production='c11c_sacred_symmetry_v1'; Grammar='astrolabe'; GrammarName='Astrolabe' }
        @{ Day='Lunes'; DayIndex=1; Slot=4; Family='living_particles'; Artistic='Living Particles'; Production='c11c_living_particles_v1'; Grammar='swarm'; GrammarName='Swarm' }
        # Tuesday
        @{ Day='Martes'; DayIndex=2; Slot=1; Family='invisible_forces'; Artistic='Invisible Forces'; Production='c11c_invisible_forces_v1'; Grammar='dipole_field'; GrammarName='Dipole Field' }
        @{ Day='Martes'; DayIndex=2; Slot=2; Family='geometric'; Artistic='Geometric Waves'; Production='c11c_geometric_waves_v1'; Grammar='interference_plane'; GrammarName='Interference Plane' }
        @{ Day='Martes'; DayIndex=2; Slot=3; Family='fractal'; Artistic='Fractal Bloom'; Production='c11c_fractal_bloom_v1'; Grammar='dendritic_tunnel'; GrammarName='Dendritic Tunnel' }
        @{ Day='Martes'; DayIndex=2; Slot=4; Family='sacred_symmetry'; Artistic='Sacred Symmetry'; Production='c11c_sacred_symmetry_v1'; Grammar='gear_train'; GrammarName='Gear Train' }
        # Wednesday
        @{ Day='Miércoles'; DayIndex=3; Slot=1; Family='living_particles'; Artistic='Living Particles'; Production='c11c_living_particles_v1'; Grammar='vortex'; GrammarName='Vortex' }
        @{ Day='Miércoles'; DayIndex=3; Slot=2; Family='invisible_forces'; Artistic='Invisible Forces'; Production='c11c_invisible_forces_v1'; Grammar='vortex_field'; GrammarName='Vortex Field' }
        @{ Day='Miércoles'; DayIndex=3; Slot=3; Family='geometric'; Artistic='Geometric Waves'; Production='c11c_geometric_waves_v1'; Grammar='parametric_ribbon'; GrammarName='Parametric Ribbon' }
        @{ Day='Miércoles'; DayIndex=3; Slot=4; Family='fractal'; Artistic='Fractal Bloom'; Production='c11c_fractal_bloom_v1'; Grammar='spiral_fractal'; GrammarName='Spiral Fractal' }
        # Thursday
        @{ Day='Jueves'; DayIndex=4; Slot=1; Family='sacred_symmetry'; Artistic='Sacred Symmetry'; Production='c11c_sacred_symmetry_v1'; Grammar='polygon_orrery'; GrammarName='Polygon Orrery' }
        @{ Day='Jueves'; DayIndex=4; Slot=2; Family='living_particles'; Artistic='Living Particles'; Production='c11c_living_particles_v1'; Grammar='collision_cloud'; GrammarName='Collision Cloud' }
        @{ Day='Jueves'; DayIndex=4; Slot=3; Family='invisible_forces'; Artistic='Invisible Forces'; Production='c11c_invisible_forces_v1'; Grammar='saddle_field'; GrammarName='Saddle Field' }
        @{ Day='Jueves'; DayIndex=4; Slot=4; Family='geometric'; Artistic='Geometric Waves'; Production='c11c_geometric_waves_v1'; Grammar='lattice_wave'; GrammarName='Lattice Wave' }
        # Friday
        @{ Day='Viernes'; DayIndex=5; Slot=1; Family='fractal'; Artistic='Fractal Bloom'; Production='c11c_fractal_bloom_v1'; Grammar='fractal_filigree'; GrammarName='Fractal Filigree' }
        @{ Day='Viernes'; DayIndex=5; Slot=2; Family='sacred_symmetry'; Artistic='Sacred Symmetry'; Production='c11c_sacred_symmetry_v1'; Grammar='origami_mandala'; GrammarName='Origami Mandala' }
        @{ Day='Viernes'; DayIndex=5; Slot=3; Family='living_particles'; Artistic='Living Particles'; Production='c11c_living_particles_v1'; Grammar='organic_pulse'; GrammarName='Organic Pulse' }
        @{ Day='Viernes'; DayIndex=5; Slot=4; Family='invisible_forces'; Artistic='Invisible Forces'; Production='c11c_invisible_forces_v1'; Grammar='quadrupole_field'; GrammarName='Quadrupole Field' }
        # Saturday
        @{ Day='Sábado'; DayIndex=6; Slot=1; Family='geometric'; Artistic='Geometric Waves'; Production='c11c_geometric_waves_v1'; Grammar='orbital_wave'; GrammarName='Orbital Wave' }
        @{ Day='Sábado'; DayIndex=6; Slot=2; Family='fractal'; Artistic='Fractal Bloom'; Production='c11c_fractal_bloom_v1'; Grammar='nested_worlds'; GrammarName='Nested Worlds' }
        @{ Day='Sábado'; DayIndex=6; Slot=3; Family='sacred_symmetry'; Artistic='Sacred Symmetry'; Production='c11c_sacred_symmetry_v1'; Grammar='celestial_chart'; GrammarName='Celestial Chart' }
        @{ Day='Sábado'; DayIndex=6; Slot=4; Family='living_particles'; Artistic='Living Particles'; Production='c11c_living_particles_v1'; Grammar='magnetic_filament_cloud'; GrammarName='Magnetic Filament Cloud' }
        # Sunday
        @{ Day='Domingo'; DayIndex=7; Slot=1; Family='invisible_forces'; Artistic='Invisible Forces'; Production='c11c_invisible_forces_v1'; Grammar='gravitational_lens'; GrammarName='Gravitational Lens' }
        @{ Day='Domingo'; DayIndex=7; Slot=2; Family='invisible_forces'; Artistic='Invisible Forces'; Production='c11c_invisible_forces_v1'; Grammar='topographic_basin'; GrammarName='Topographic Basin' }
        @{ Day='Domingo'; DayIndex=7; Slot=3; Family='invisible_forces'; Artistic='Invisible Forces'; Production='c11c_invisible_forces_v1'; Grammar='scalar_potential'; GrammarName='Scalar Potential' }
    )
}

function Get-C11CMinimumSeedGap {
    param([Parameter(Mandatory=$true)][int]$Count,[int]$Minimum=1000000,[int]$MaximumExclusive=2147483647)
    if ($Count -lt 2) { return 0 }
    $range = [double]($MaximumExclusive - $Minimum - 1)
    return [int][math]::Floor(($range / [double]($Count + 1)) * 0.40)
}

function Assert-C11CSeedSpacing {
    param([Parameter(Mandatory=$true)][int[]]$Seeds,[int]$Minimum=1000000,[int]$MaximumExclusive=2147483647)
    if ($Seeds.Count -lt 1) { throw 'Seed count must be positive.' }
    foreach($seed in $Seeds){ if($seed -lt $Minimum -or $seed -ge $MaximumExclusive){ throw "Seed out of configured batch range: $seed" } }
    $sorted=@($Seeds | Sort-Object -Unique)
    if($sorted.Count -ne $Seeds.Count){ throw 'Batch seeds must be unique.' }
    $minGap=Get-C11CMinimumSeedGap -Count $Seeds.Count -Minimum $Minimum -MaximumExclusive $MaximumExclusive
    for($i=1;$i -lt $sorted.Count;$i++){
        $gap=[int64]$sorted[$i]-[int64]$sorted[$i-1]
        if($gap -lt $minGap){ throw "Batch seeds are too close: gap=$gap minimum_required=$minGap" }
    }
}

function New-C11CUniqueSeeds {
    param([Parameter(Mandatory=$true)][int]$Count,[int]$Minimum=1000000,[int]$MaximumExclusive=2147483647)
    if ($Count -lt 1) { throw 'Seed count must be positive.' }
    $binWidth=[double]($MaximumExclusive-$Minimum-1)/[double]($Count+1)
    $margin=$binWidth*0.30
    $result=[System.Collections.Generic.List[int]]::new()
    for($i=1;$i -le $Count;$i++){
        $center=$Minimum+($binWidth*$i)
        $low=[int][math]::Ceiling($center-$margin)
        $high=[int][math]::Floor($center+$margin)
        $candidate=Get-Random -Minimum $low -Maximum ($high+1)
        [void]$result.Add([int]$candidate)
    }
    $shuffled=@($result | Sort-Object { Get-Random })
    Assert-C11CSeedSpacing -Seeds $shuffled -Minimum $Minimum -MaximumExclusive $MaximumExclusive
    return $shuffled
}

function Convert-ToSafeName {
    param([Parameter(Mandatory=$true)][string]$Text)
    $normalized = $Text -replace '[^A-Za-z0-9]+','_'
    return $normalized.Trim('_')
}

function Get-C11CProductionArtifacts {
    param([string]$Production,[int]$Seed)
    $prefix = switch ($Production) {
        'c11c_geometric_waves_v1' { 'GeometricWaves_v1' }
        'c11c_fractal_bloom_v1' { 'FractalBloom_v1' }
        'c11c_sacred_symmetry_v1' { 'SacredSymmetry_v1' }
        'c11c_living_particles_v1' { 'LivingParticles_v1' }
        'c11c_invisible_forces_v1' { 'InvisibleForces_v1' }
        default { throw "Unknown production id: $Production" }
    }
    $stem = "${prefix}_seed_${Seed}"
    $familyRoot = Join-Path $ProjectRoot "artifacts\production\audiovisual\$Production"
    $productRoot = Join-Path $familyRoot $stem
    return [ordered]@{
        Root=$productRoot
        MP4=(Join-Path $productRoot "$stem.mp4")
        Social=(Join-Path $productRoot "${stem}_social.txt")
        Manifest=(Join-Path $productRoot "${stem}_manifest.json")
        Authoring=(Join-Path $productRoot "${stem}_authoring.json")
        Probe=(Join-Path $productRoot "${stem}_ffprobe.json")
        GodotLog=(Join-Path $productRoot "${stem}_godot.log")
        Music=(Join-Path $productRoot "${stem}_music.wav")
        Gif=(Join-Path $productRoot "$stem.gif")
    }
}

function Invoke-C11CProductionBatch {
    param(
        [Parameter(Mandatory=$true)][array]$Schedule,
        [Parameter(Mandatory=$true)][int[]]$Seeds,
        [Parameter(Mandatory=$true)][string]$OutputRoot,
        [Parameter(Mandatory=$true)][string]$BatchKind,
        [Parameter(Mandatory=$true)][string]$BatchId,
        [switch]$Force
    )
    if ($Schedule.Count -ne $Seeds.Count) { throw "Schedule count $($Schedule.Count) does not match seed count $($Seeds.Count)." }
    Assert-C11CSeedSpacing -Seeds $Seeds
    if ((Test-Path -LiteralPath $OutputRoot) -and -not $Force) { throw "Batch already exists: $OutputRoot. Use -Force for deliberate replacement." }
    if ($Force -and (Test-Path -LiteralPath $OutputRoot)) { Remove-Item -LiteralPath $OutputRoot -Recurse -Force }

    # Full destination preflight before rendering any item.
    $destinations = @()
    for ($i=0; $i -lt $Schedule.Count; $i++) {
        $item=$Schedule[$i]; $seed=[int]$Seeds[$i]
        $dayRoot=Join-Path $OutputRoot $item.Day
        $folderName = '{0:D2}_{1}_{2}_seed_{3}' -f [int]$item.Slot,(Convert-ToSafeName $item.Artistic),(Convert-ToSafeName $item.GrammarName),$seed
        $dest=Join-Path $dayRoot $folderName
        $destinations += [pscustomobject]@{Item=$item;Seed=$seed;Destination=$dest;SlotIndex=$i+1}
    }
    foreach($d in $destinations){ if(Test-Path -LiteralPath $d.Destination){throw "Destination already exists: $($d.Destination)"} }

    New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
    $results=@()
    foreach($d in $destinations){
        $item=$d.Item; $seed=$d.Seed
        $launcher=Join-Path $ProjectRoot "tools\prototypes\c11c_bulk\run_c11c_production.ps1"
        if(-not(Test-Path -LiteralPath $launcher)){throw "Missing production launcher: $launcher"}
        Write-Host "[C11-C-BATCH] $BatchKind $BatchId | $($item.Day) $($item.Slot) | $($item.Artistic) / $($item.GrammarName) | seed=$seed"
        & $launcher -Family $item.Production -Seed $seed -Grammar $item.Grammar
        if($LASTEXITCODE -ne 0){throw "Production render failed: $($item.Artistic) / $($item.GrammarName) seed=$seed"}

        $src=Get-C11CProductionArtifacts -Production $item.Production -Seed $seed
        foreach($required in @('MP4','Social','Manifest','Authoring','Probe','GodotLog','Music')){
            if(-not(Test-Path -LiteralPath $src[$required])){throw "Required artifact missing after render: $($src[$required])"}
        }

        New-Item -ItemType Directory -Force -Path $d.Destination | Out-Null
        foreach($key in @('MP4','Social','Manifest','Authoring','Probe','GodotLog','Music','Gif')){
            $source=$src[$key]
            if(Test-Path -LiteralPath $source){ Copy-Item -LiteralPath $source -Destination $d.Destination -Force }
        }
        $sourceManifest=Get-Content -Raw -LiteralPath $src.Manifest | ConvertFrom-Json
        $sourceAuthoring=Get-Content -Raw -LiteralPath $src.Authoring | ConvertFrom-Json
        $productId='{0:D2}_{1}_{2}_seed_{3}' -f [int]$item.Slot,(Convert-ToSafeName $item.Artistic),(Convert-ToSafeName $item.GrammarName),$seed
        $sourceDurationText=([double]$sourceManifest.visual.duration_seconds).ToString('F2')
        $sourceDurationInvariant=([double]$sourceManifest.visual.duration_seconds).ToString([System.Globalization.CultureInfo]::InvariantCulture)
        $productText=@"
C11-C BATCH PRODUCTION PRODUCT
==============================
Batch kind: $BatchKind
Batch id: $BatchId
Day: $($item.Day)
Order: $($item.Slot)
Family technical id: $($item.Family)
Artistic name: $($item.Artistic)
Grammar technical id: $($item.Grammar)
Grammar artistic name: $($item.GrammarName)
Seed: $seed
Resolution: 720x1280
FPS: 30
Duration: $sourceDurationText s
Audio: FAMILY_MUSIC_V4

Source reproduction:
.\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family $($item.Production) -Seed $seed -Grammar $($item.Grammar) -Duration $sourceDurationInvariant
"@
        [System.IO.File]::WriteAllText((Join-Path $d.Destination 'PRODUCT.txt'),$productText,(New-Object System.Text.UTF8Encoding($false)))
        $itemManifest=[ordered]@{
            schema='C11-C-BATCH-PRODUCT-V1'
            revision='2.13.0'
            status='FINAL_BATCH_PRODUCT'
            batch_kind=$BatchKind
            batch_id=$BatchId
            day=$item.Day
            day_index=[int]$item.DayIndex
            slot=[int]$item.Slot
            family=[ordered]@{technical_id=$item.Family; artistic_name=$item.Artistic; production_id=$item.Production}
            grammar=[ordered]@{technical_id=$item.Grammar; artistic_name=$item.GrammarName}
            seed=$seed
            visual=[ordered]@{resolution='720x1280';fps=[int]$sourceManifest.visual.fps;duration_seconds=[double]$sourceManifest.visual.duration_seconds;frames=[int]$sourceManifest.visual.frame_count}
            audio=[ordered]@{mode='FAMILY_MUSIC_V4';profile_id=[string]$sourceManifest.audio.profile_id;semantic_key=[string]$sourceManifest.audio.semantic_key;enabled=$true}
            source_revision=[string]$sourceManifest.revision
            source_authoring_grammar=[string]$sourceAuthoring.grammar_id
            source_manifest=$src.Manifest
            files=@(Get-ChildItem -LiteralPath $d.Destination -File | Select-Object -ExpandProperty Name) + 'batch_item_manifest.json' + 'PRODUCT.txt'
            reproduction_command=".\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family $($item.Production) -Seed $seed -Grammar $($item.Grammar) -Duration $sourceDurationInvariant"
        }
        [System.IO.File]::WriteAllText((Join-Path $d.Destination 'batch_item_manifest.json'),($itemManifest|ConvertTo-Json -Depth 10),(New-Object System.Text.UTF8Encoding($false)))
        $results += [pscustomobject]@{
            order=$d.SlotIndex;day=$item.Day;slot=[int]$item.Slot;family=$item.Family;artistic_name=$item.Artistic;grammar=$item.Grammar;grammar_name=$item.GrammarName;seed=$seed;path=$d.Destination;status='PASS'
        }
    }
    $manifest=[ordered]@{
        schema='C11-C-BATCH-MANIFEST-V1'
        revision='2.13.0'
        status='COMPLETE'
        batch_kind=$BatchKind
        batch_id=$BatchId
        count=$results.Count
        seed_count=@($Seeds|Select-Object -Unique).Count
        seed_strategy='stratified_spread_random_v1'
        minimum_seed_gap=(Get-C11CMinimumSeedGap -Count $Seeds.Count)
        unique_video_keys=@($results | ForEach-Object { "$($_.family)|$($_.grammar)|$($_.seed)" } | Select-Object -Unique).Count
        schedule_unique_keys=@($results | ForEach-Object { "$($_.family)|$($_.grammar)|$($_.seed)" } | Select-Object -Unique).Count
        output_root=$OutputRoot
        results=$results
    }
    [System.IO.File]::WriteAllText((Join-Path $OutputRoot 'batch_manifest.json'),($manifest|ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))
    Write-Host "[C11-C-BATCH] COMPLETE $BatchKind $BatchId | products=$($results.Count) | root=$OutputRoot"
}
