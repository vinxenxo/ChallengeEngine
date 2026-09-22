param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')]
    [string]$Family,
    [Parameter(Mandatory=$true)]
    [ValidateRange(1,2147483646)]
    [int]$Seed,
    [Alias('Silent')]
    [switch]$NoSound,
    [switch]$NoFooter,
    [switch]$Force
)

$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$launcher=Join-Path $ProjectRoot ("tools\prototypes\$Family\run_prototype.ps1")
if (-not (Test-Path -LiteralPath $launcher)) { throw "Prototype launcher not found: $launcher" }
$prefixMap=@{ c11c_geometric_waves_v1='GeometricWaves_v1'; c11c_fractal_bloom_v1='FractalBloom_v1'; c11c_sacred_symmetry_v1='SacredSymmetry_v1'; c11c_living_particles_v1='LivingParticles_v1'; c11c_invisible_forces_v1='InvisibleForces_v1' }
$productId="$($prefixMap[$Family])_seed_$Seed"
$productionRoot=Join-Path $ProjectRoot 'artifacts\production\audiovisual'
$productRoot=Join-Path (Join-Path $productionRoot $Family) $productId
if ((Test-Path -LiteralPath $productRoot) -and -not $Force) { throw "Production product already exists: $productRoot. Use -Force only for deliberate replacement." }
if ($Force -and (Test-Path -LiteralPath $productRoot)) { Remove-Item -LiteralPath $productRoot -Recurse -Force }
New-Item -ItemType Directory -Force -Path $productionRoot | Out-Null

$launcherArgs=@('-Seed',$Seed)
if ($NoSound) { $launcherArgs += '-NoSound' }
if ($NoFooter) { $launcherArgs += '-NoFooter' }
Write-Host '[C11-C-PRODUCTION] =========================================='
Write-Host "[C11-C-PRODUCTION] Family=$Family Seed=$Seed Product=$productId"
try { & $launcher @launcherArgs } catch { throw "Prototype generation failed: $($_.Exception.Message)" }
if (-not $?) { throw 'Prototype launcher returned failure.' }

$stage=Join-Path $ProjectRoot ("artifacts\prototypes\$Family")
$stem=$productId
$required=@("$stem.mp4","${stem}_social.txt","${stem}_manifest.json","${stem}_authoring.json","${stem}_ffprobe.json","${stem}_godot.log")
foreach ($name in $required) { if (-not (Test-Path -LiteralPath (Join-Path $stage $name))) { throw "Required production artifact missing: $name" } }
New-Item -ItemType Directory -Force -Path $productRoot | Out-Null
foreach ($name in $required + @("$stem.gif","${stem}_music.wav")) {
    $source=Join-Path $stage $name
    if (Test-Path -LiteralPath $source) { Copy-Item -LiteralPath $source -Destination (Join-Path $productRoot $name) -Force }
}

$repro=".\tools\prototypes\c11c_bulk\run_c11c_production_v2.1.0.ps1 -Family $Family -Seed $Seed"
if ($NoSound) { $repro+=' -NoSound' }
if ($NoFooter) { $repro+=' -NoFooter' }
$sourceManifest=Get-Content -Raw (Join-Path $stage "${stem}_manifest.json") | ConvertFrom-Json
$created=[DateTime]::UtcNow.ToString('o')
$prodManifest=[ordered]@{
    schema='C11-C-PRODUCTION-PRODUCT-V1'; revision='2.1.0'; status='FINAL_PRODUCT'; product_id=$productId; family=$Family; seed=$Seed
    created_utc=$created; canvas='720x1280'; fps=30; duration_seconds=18.0; frames=540; sound_enabled=(-not $NoSound); footer_enabled=(-not $NoFooter)
    production_path=$productRoot; source_prototype_revision=$sourceManifest.revision; source_stage=$stage; reproduction_command=$repro
    protected_from_review_cleanup=$true; files=@()
}
$prodManifestPath=Join-Path $productRoot 'production_manifest.json'
$prodManifest.files=@(Get-ChildItem -LiteralPath $productRoot -File | Select-Object -ExpandProperty Name)
$prodManifest | ConvertTo-Json -Depth 12 | Set-Content -Encoding UTF8 $prodManifestPath
$readme=@"
C11-C FINAL PRODUCT
===================
Product ID: $productId
Family: $Family
Seed: $Seed
Resolution: 720x1280
FPS: 30
Duration: 18.00 s
Sound: $(-not $NoSound)
Footer: $(-not $NoFooter)

Reproduction command:
$repro

This directory is under artifacts\production\audiovisual and is protected from C11-C review/cleanup scripts.
The prototype staging directory under artifacts\prototypes may be cleaned independently.
"@
[System.IO.File]::WriteAllText((Join-Path $productRoot 'PRODUCT.txt'),$readme,(New-Object System.Text.UTF8Encoding($false)))

$catalogPath=Join-Path $productionRoot 'C11C_PRODUCTION_CATALOG.json'
if (Test-Path -LiteralPath $catalogPath) { $catalog=Get-Content -Raw $catalogPath | ConvertFrom-Json; if ($null -eq $catalog.products) { $catalog.products=@() } } else { $catalog=[pscustomobject]@{schema='C11-C-PRODUCTION-CATALOG-V1';revision='2.1.0';products=@()} }
$catalog.products=@($catalog.products | Where-Object { $_.product_id -ne $productId })
$catalog.products += [pscustomobject]@{product_id=$productId;family=$Family;seed=$Seed;path=$productRoot;created_utc=$created;reproduction_command=$repro}
$catalog | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $catalogPath
Write-Host '[C11-C-PRODUCTION] FINAL PRODUCT PUBLISHED.'
Write-Host "[C11-C-PRODUCTION] $productRoot"
return
