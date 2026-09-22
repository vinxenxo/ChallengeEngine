param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')]
    [string]$Family,
    [Parameter(Mandatory=$false)]
    [int[]]$Seeds = @(),
    [switch]$NoSound,
    [switch]$NoFooter,
    [switch]$Force
)
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
if($Seeds.Count -eq 0){
  $bankPath=Join-Path $PSScriptRoot 'C11C_PRODUCTION_SEED_BANK_v1.json'
  if(-not(Test-Path -LiteralPath $bankPath)){throw "Seed bank missing: $bankPath"}
  $bank=Get-Content -Raw $bankPath | ConvertFrom-Json
  $Seeds=@($bank.seeds | Select-Object -First 8 | ForEach-Object {[int]$_})
}
foreach($seed in $Seeds){
  $args=@('-NoProfile','-ExecutionPolicy','Bypass','-File',(Join-Path $PSScriptRoot 'run_c11c_production.ps1'),'-Family',$Family,'-Seed',[string]$seed)
  if($NoSound){$args+='-NoSound'}
  if($NoFooter){$args+='-NoFooter'}
  if($Force){$args+='-Force'}
  & powershell.exe @args
  $exit=$LASTEXITCODE
  if($exit -ne 0){throw "Production bulk failed for $Family seed=$seed exit=$exit"}
}
Write-Host "[C11-C-PRODUCTION-BULK] COMPLETE family=$Family products=$($Seeds.Count)"
return
