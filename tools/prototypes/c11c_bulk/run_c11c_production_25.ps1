param(
    [Parameter(Mandatory=$false)]
    [int[]]$Seeds = @(),
    [Parameter(Mandatory=$false)]
    [ValidateRange(1000000,2147483646)]
    [int]$RandomSeedMinimum = 1000000,
    [Parameter(Mandatory=$false)]
    [ValidateRange(1000001,2147483647)]
    [int]$RandomSeedMaximumExclusive = 2147483647,
    [switch]$NoSound,
    [switch]$NoFooter,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$ProductionRunner = Join-Path $PSScriptRoot 'run_c11c_production_bulk.ps1'
$ProductionRoot = Join-Path $ProjectRoot 'artifacts\production\audiovisual'
. (Join-Path $PSScriptRoot 'C11CProductionBatchCommon.ps1')

$Families = @(
    'c11c_geometric_waves_v1',
    'c11c_fractal_bloom_v1',
    'c11c_sacred_symmetry_v1',
    'c11c_living_particles_v1',
    'c11c_invisible_forces_v1'
)

$PrefixMap = @{
    c11c_geometric_waves_v1 = 'GeometricWaves_v1'
    c11c_fractal_bloom_v1 = 'FractalBloom_v1'
    c11c_sacred_symmetry_v1 = 'SacredSymmetry_v1'
    c11c_living_particles_v1 = 'LivingParticles_v1'
    c11c_invisible_forces_v1 = 'InvisibleForces_v1'
}

if (-not (Test-Path -LiteralPath $ProductionRunner)) {
    throw "Missing canonical production bulk runner: $ProductionRunner"
}

# Exactly five shared seeds: the same five seeds are rendered in all five families.
if ($Seeds.Count -eq 0) {
    $Seeds = @(New-C11CUniqueSeeds -Count 5 -Minimum $RandomSeedMinimum -MaximumExclusive $RandomSeedMaximumExclusive)
} else {
    if ($Seeds.Count -ne 5) {
        throw "Pass exactly 5 seeds when -Seeds is supplied. Received $($Seeds.Count)."
    }
    $Seeds = @($Seeds | ForEach-Object { [int]$_ })
    if ((@($Seeds | Select-Object -Unique)).Count -ne 5) {
        throw 'The five production seeds must be unique.'
    }
    Assert-C11CSeedSpacing -Seeds $Seeds -Minimum $RandomSeedMinimum -MaximumExclusive $RandomSeedMaximumExclusive
}

foreach ($seed in $Seeds) {
    if ($seed -lt $RandomSeedMinimum -or $seed -ge $RandomSeedMaximumExclusive) {
        throw "Seed out of range: $seed"
    }
}

# Preflight every final product path before rendering anything. Without -Force,
# an existing product aborts the batch up front, avoiding partial batches.
$products = @()
foreach ($family in $Families) {
    $productPrefix = $PrefixMap[$family]
    foreach ($seed in $Seeds) {
        $productId = "${productPrefix}_seed_${seed}"
        $productRoot = Join-Path (Join-Path $ProductionRoot $family) $productId
        $products += [pscustomobject]@{
            family = $family
            seed = [int]$seed
            product_id = $productId
            path = $productRoot
        }
        if ((Test-Path -LiteralPath $productRoot) -and -not $Force) {
            throw "Production batch already contains product $productId. Use -Force only for deliberate replacement."
        }
    }
}

Write-Host '[C11-C-PRODUCTION-25] =========================================='
Write-Host '[C11-C-PRODUCTION-25] RANDOM 5x5 FINAL PRODUCT BATCH'
Write-Host '[C11-C-PRODUCTION-25] No prototype cleanup is performed.'
Write-Host '[C11-C-PRODUCTION-25] Families: 5'
Write-Host '[C11-C-PRODUCTION-25] Seeds: 5'
Write-Host '[C11-C-PRODUCTION-25] Products: 25'
Write-Host "[C11-C-PRODUCTION-25] Seeds: $($Seeds -join ', ')"
Write-Host "[C11-C-PRODUCTION-25] Audio: $(-not $NoSound)"
Write-Host "[C11-C-PRODUCTION-25] Footer: $(-not $NoFooter)"
Write-Host "[C11-C-PRODUCTION-25] Force replacement: $([bool]$Force)"

$batchStarted = [DateTime]::UtcNow
$batchResults = [System.Collections.Generic.List[object]]::new()

foreach ($family in $Families) {
    Write-Host "[C11-C-PRODUCTION-25] FAMILY START $family"
    $runnerParams = @{
        Family = $family
        Seeds = @($Seeds)
    }
    if ($NoSound) { $runnerParams.NoSound = $true }
    if ($NoFooter) { $runnerParams.NoFooter = $true }
    if ($Force) { $runnerParams.Force = $true }

    try {
        & $ProductionRunner @runnerParams
        if (-not $?) {
            throw "Canonical production bulk runner returned failure for $family."
        }
    } catch {
        throw "25-product production batch failed in family=${family}: $($_.Exception.Message)"
    }

    foreach ($item in @($products | Where-Object { $_.family -eq $family })) {
        if (-not (Test-Path -LiteralPath $item.path)) {
            throw "Published product directory missing: $($item.path)"
        }
        $mp4s = @(Get-ChildItem -LiteralPath $item.path -Filter '*.mp4' -File)
        if ($mp4s.Count -ne 1) {
            throw "Production product must contain exactly one MP4: $($item.path). Found $($mp4s.Count)."
        }
        foreach ($required in @(
            "$($item.product_id)_social.txt",
            "$($item.product_id)_manifest.json",
            "$($item.product_id)_authoring.json",
            "$($item.product_id)_ffprobe.json",
            "$($item.product_id)_godot.log",
            'production_manifest.json',
            'PRODUCT.txt'
        )) {
            $requiredPath = Join-Path $item.path $required
            if (-not (Test-Path -LiteralPath $requiredPath)) {
                throw "Required production artifact missing: $requiredPath"
            }
        }
        $batchResults.Add([ordered]@{
            family = $item.family
            seed = $item.seed
            product_id = $item.product_id
            status = 'PASS'
            path = $item.path
            mp4 = (Get-ChildItem -LiteralPath $item.path -Filter '*.mp4' -File | Select-Object -First 1).FullName
        })
        Write-Host "[C11-C-PRODUCTION-25] PASS $($item.product_id)"
    }
}

$batchFinished = [DateTime]::UtcNow
$batchManifest = [ordered]@{
    schema = 'C11-C-PRODUCTION-25-BATCH-V1'
    revision = '2.13.0'
    status = 'COMPLETE'
    batch_type = '5_random_or_explicit_seeds_x_5_families'
    started_utc = $batchStarted.ToString('o')
    finished_utc = $batchFinished.ToString('o')
    family_count = 5
    seed_count = 5
    product_count = 25
    seeds = @($Seeds)
    seed_strategy = 'stratified_spread_random_v1'
    minimum_seed_gap = (Get-C11CMinimumSeedGap -Count $Seeds.Count -Minimum $RandomSeedMinimum -MaximumExclusive $RandomSeedMaximumExclusive)
    audio_enabled = (-not $NoSound)
    footer_enabled = (-not $NoFooter)
    delivery = [ordered]@{
        resolution = '720x1280'
        aspect_ratio = '9:16'
        fps = 30
        frames = 'round(duration_seconds*30)'
        duration_seconds = '20..30 policy-driven'
    }
    production_root = $ProductionRoot
    protected_from_review_cleanup = $true
    reproduction = 'Each product contains its own exact reproduction command in PRODUCT.txt and production_manifest.json.'
    products = @($batchResults)
}

New-Item -ItemType Directory -Force -Path $ProductionRoot | Out-Null
$batchFileName = 'C11C_PRODUCTION_BATCH_{0}.json' -f $batchFinished.ToString('yyyyMMdd_HHmmss')
$batchManifestPath = Join-Path $ProductionRoot $batchFileName
[System.IO.File]::WriteAllText(
    $batchManifestPath,
    ($batchManifest | ConvertTo-Json -Depth 12),
    (New-Object System.Text.UTF8Encoding($false))
)

Write-Host "[C11-C-PRODUCTION-25] COMPLETE - 25 final products published."
Write-Host "[C11-C-PRODUCTION-25] Batch manifest: $batchManifestPath"
Write-Host "[C11-C-PRODUCTION-25] Seeds: $($Seeds -join ', ')"
return
