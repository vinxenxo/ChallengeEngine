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
if($Seeds.Count -eq 0){
    $bank=Get-Content -Raw (Join-Path $PSScriptRoot 'C11C_PRODUCTION_SEED_BANK_v1.json') | ConvertFrom-Json
    $Seeds=@($bank.seeds | Select-Object -First 8 | ForEach-Object {[int]$_})
}
$launcher=Join-Path $PSScriptRoot 'run_c11c_production.ps1'
foreach($seed in $Seeds){
    Write-Host "[C11-C-PRODUCTION-BULK] START family=$Family seed=$seed"
    $params=@{Family=$Family;Seed=[int]$seed}
    if($NoSound){$params.NoSound=$true}; if($NoFooter){$params.NoFooter=$true}; if($Force){$params.Force=$true}
    & $launcher @params
    if(-not $?){throw "Production bulk failed for $Family seed=$seed"}
    Write-Host "[C11-C-PRODUCTION-BULK] PASS family=$Family seed=$seed"
}
Write-Host "[C11-C-PRODUCTION-BULK] COMPLETE family=$Family products=$($Seeds.Count)"
return
