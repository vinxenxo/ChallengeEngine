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
  $args=@('-NoProfile','-ExecutionPolicy','Bypass','-File',$launcher,'-Seed',[string]$Seed)
  if($NoSound){$args+='-NoSound'}
  if($NoFooter){$args+='-NoFooter'}
  Write-Host "[C11-C-ALL] START $family seed=$Seed"
  & powershell.exe @args
  $exit=$LASTEXITCODE
  if($exit -ne 0){throw "Family failed: $family exit=$exit"}
  Write-Host "[C11-C-ALL] PASS $family seed=$Seed"
}
Write-Host "[C11-C-ALL] COMPLETE seed=$Seed families=$($families.Count)"
return
