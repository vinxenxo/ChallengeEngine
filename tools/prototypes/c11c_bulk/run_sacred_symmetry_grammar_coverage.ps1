$ErrorActionPreference = "Stop"
$seeds = @(314159, 271828, 161803, 577215, 8675309)
foreach ($seed in $seeds) {
    Write-Host "[C11-C.3-GRAMMAR] START seed=$seed"
    & "$PSScriptRoot\..\c11c_sacred_symmetry_v1\run_prototype.ps1" -Seed $seed
    if ($LASTEXITCODE -ne 0) { throw "Sacred Symmetry grammar coverage failed for seed=$seed" }
}
Write-Host "[C11-C.3-GRAMMAR] COMPLETE seeds=$($seeds.Count)"
