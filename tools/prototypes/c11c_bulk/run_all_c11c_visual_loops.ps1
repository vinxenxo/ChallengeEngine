param(
    [int]$Seed = 314159,
    [switch]$NoSound,
    [switch]$NoFooter
)
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$families=@('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')
foreach($family in $families){
    $launcher=Join-Path $ProjectRoot ("tools\prototypes\$family\run_prototype.ps1")
    Write-Host "[C11-C-ALL] START $family seed=$Seed"
    $params=@{Seed=[int]$Seed}
    if($NoSound){$params.NoSound=$true}; if($NoFooter){$params.NoFooter=$true}
    & $launcher @params
    if(-not $?){throw "Family failed: $family"}
    Write-Host "[C11-C-ALL] PASS $family seed=$Seed"
}
Write-Host "[C11-C-ALL] COMPLETE seed=$Seed families=$($families.Count)"
return
