param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')]
    [string]$Family,
    [Parameter(Mandatory=$true)]
    [ValidateRange(1,2147483646)]
    [int]$Seed,
    [Parameter(Mandatory=$false)]
    [string]$Grammar = '',
    [Alias('Silent')][switch]$NoSound,
    [switch]$NoFooter,
    [switch]$Force
)
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$launcher=Join-Path $ProjectRoot ("tools\prototypes\$Family\run_prototype.ps1")
if (-not (Test-Path -LiteralPath $launcher)) { throw "Prototype launcher not found: $launcher" }
$prefixMap=@{
    c11c_geometric_waves_v1='GeometricWaves_v1'
    c11c_fractal_bloom_v1='FractalBloom_v1'
    c11c_sacred_symmetry_v1='SacredSymmetry_v1'
    c11c_living_particles_v1='LivingParticles_v1'
    c11c_invisible_forces_v1='InvisibleForces_v1'
}
$productId="$($prefixMap[$Family])_seed_$Seed"
$productionRoot=Join-Path $ProjectRoot 'artifacts\production\audiovisual'
$productRoot=Join-Path (Join-Path $productionRoot $Family) $productId
if ((Test-Path -LiteralPath $productRoot) -and -not $Force) {
    throw "Production product already exists: $productRoot. Use -Force only for deliberate replacement."
}

Write-Host '[C11-C-PRODUCTION] =========================================='
Write-Host "[C11-C-PRODUCTION] Family=$Family Seed=$Seed Product=$productId"

# Render to prototype staging FIRST. An existing final product is never deleted before
# the replacement candidate has successfully rendered and passed its own contracts.
$launcherParams=@{Seed=[int]$Seed}
if(-not [string]::IsNullOrWhiteSpace($Grammar)){$launcherParams.Grammar=$Grammar}
if($NoSound){$launcherParams.NoSound=$true}
if($NoFooter){$launcherParams.NoFooter=$true}
& $launcher @launcherParams
if (-not $?) { throw 'Prototype generation failed.' }

$stage=Join-Path $ProjectRoot ("artifacts\prototypes\$Family")
$stem=$productId
$required=@(
    "$stem.mp4",
    "${stem}_social.txt",
    "${stem}_manifest.json",
    "${stem}_authoring.json",
    "${stem}_ffprobe.json",
    "${stem}_godot.log"
)
foreach ($name in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $stage $name))) { throw "Required production artifact missing: $name" }
}
$candidateMp4 = Join-Path $stage "$stem.mp4"
if (-not (Test-Path -LiteralPath $candidateMp4)) {
    throw "Canonical production candidate MP4 missing for seed ${Seed}: $candidateMp4"
}

# Only now is replacement allowed.
if ($Force -and (Test-Path -LiteralPath $productRoot)) { Remove-Item -LiteralPath $productRoot -Recurse -Force }
New-Item -ItemType Directory -Force -Path $productRoot | Out-Null
foreach ($name in ($required + @("$stem.gif","${stem}_music.wav"))) {
    $source=Join-Path $stage $name
    if (Test-Path -LiteralPath $source) { Copy-Item -LiteralPath $source -Destination (Join-Path $productRoot $name) -Force }
}

$repro=".\tools\prototypes\c11c_bulk\run_c11c_production.ps1 -Family $Family -Seed $Seed"
if(-not [string]::IsNullOrWhiteSpace($Grammar)){$repro+=" -Grammar $Grammar"}
if ($NoSound) { $repro+=' -NoSound' }
if ($NoFooter) { $repro+=' -NoFooter' }
$sourceManifest=Get-Content -Raw (Join-Path $stage "${stem}_manifest.json") | ConvertFrom-Json
$created=[DateTime]::UtcNow.ToString('o')
$prodManifest=[ordered]@{
    schema='C11-C-PRODUCTION-PRODUCT-V2'
    revision='2.1.6'
    status='FINAL_PRODUCT'
    product_id=$productId
    family=$Family
    seed=$Seed
    grammar_id=if([string]::IsNullOrWhiteSpace($Grammar)){[string]$sourceManifest.grammar_id}else{$Grammar}
    grammar_name=if([string]::IsNullOrWhiteSpace($Grammar)){[string]$sourceManifest.grammar}else{[string]$sourceManifest.grammar}
    created_utc=$created
    canvas='720x1280'
    fps=30
    duration_seconds=18.0
    frames=540
    sound_enabled=(-not $NoSound)
    footer_enabled=(-not $NoFooter)
    production_path=$productRoot
    source_prototype_revision=$sourceManifest.revision
    source_stage=$stage
    reproduction_command=$repro
    protected_from_review_cleanup=$true
    files=@()
}
$productText=@"
C11-C FINAL PRODUCT
===================
Product ID: $productId
Family: $Family
Seed: $Seed
Grammar technical id: $(if([string]::IsNullOrWhiteSpace($Grammar)){'(prototype default)'}else{$Grammar})
Resolution: 720x1280
FPS: 30
Duration: 18.00 s
Sound: $(-not $NoSound)
Footer: $(-not $NoFooter)

Reproduction command:
$repro

This directory is protected from C11-C review/cleanup scripts.
"@
[System.IO.File]::WriteAllText((Join-Path $productRoot 'PRODUCT.txt'),$productText,(New-Object System.Text.UTF8Encoding($false)))
$prodManifest.files=@(Get-ChildItem -LiteralPath $productRoot -File | Select-Object -ExpandProperty Name) + 'production_manifest.json'
[System.IO.File]::WriteAllText((Join-Path $productRoot 'production_manifest.json'),($prodManifest | ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))

$catalogPath=Join-Path $productionRoot 'C11C_PRODUCTION_CATALOG.json'
if (Test-Path -LiteralPath $catalogPath) {
    $catalog=Get-Content -Raw $catalogPath | ConvertFrom-Json
} else {
    New-Item -ItemType Directory -Force -Path $productionRoot | Out-Null
    $catalog=[pscustomobject]@{schema='C11-C-PRODUCTION-CATALOG-V2';revision='2.1.6';products=@()}
}
if ($null -eq $catalog.products) { $catalog.products=@() }
$catalog.products=@($catalog.products | Where-Object { $_.product_id -ne $productId })
$catalog.products += [pscustomobject]@{product_id=$productId;family=$Family;seed=$Seed;grammar_id=$sourceManifest.grammar_id;grammar_name=$sourceManifest.grammar;path=$productRoot;created_utc=$created;reproduction_command=$repro}
[System.IO.File]::WriteAllText($catalogPath,($catalog | ConvertTo-Json -Depth 10),(New-Object System.Text.UTF8Encoding($false)))
Write-Host '[C11-C-PRODUCTION] FINAL PRODUCT PUBLISHED.'
Write-Host "[C11-C-PRODUCTION] $productRoot"
return
