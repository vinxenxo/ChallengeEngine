$ErrorActionPreference = "Stop"
$seeds = @(424242, 112358, 161803, 314159, 246802)
foreach ($seed in $seeds) {
    Write-Host "[C11-C.4-GRAMMAR] START seed=$seed"
    & "$PSScriptRoot\..\c11c_living_particles_v1\run_prototype.ps1" -Seed $seed
    if ($LASTEXITCODE -ne 0) { throw "Living Particles grammar coverage failed for seed=$seed" }
}
Write-Host "[C11-C.4-GRAMMAR] COMPLETE seeds=$($seeds.Count)"
