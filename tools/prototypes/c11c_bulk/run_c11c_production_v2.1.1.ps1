param(
    [Parameter(Mandatory=$true)][ValidateSet('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')][string]$Family,
    [Parameter(Mandatory=$true)][ValidateRange(1,2147483646)][int]$Seed,
    [Alias('Silent')][switch]$NoSound,
    [switch]$NoFooter,
    [switch]$Force
)
$args=@{ Family=$Family; Seed=$Seed }
if ($NoSound) { $args.NoSound=$true }
if ($NoFooter) { $args.NoFooter=$true }
if ($Force) { $args.Force=$true }
& (Join-Path $PSScriptRoot 'run_c11c_production.ps1') @args
if (-not $?) { throw 'Canonical production launcher failed.' }
return
