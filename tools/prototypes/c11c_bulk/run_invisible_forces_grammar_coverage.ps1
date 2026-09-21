$ErrorActionPreference = "Stop"
$families = @(
    @{ Seed = 7; Name = "dipole_field" },
    @{ Seed = 37; Name = "vortex_field" },
    @{ Seed = 3; Name = "saddle_field" },
    @{ Seed = 4; Name = "quadrupole_field" },
    @{ Seed = 31; Name = "gravitational_lens" },
    @{ Seed = 1; Name = "topographic_basin" }
)
foreach ($item in $families) {
    Write-Host ("[C11-C.5-GRAMMAR] START seed={0} mode={1}" -f $item.Seed, $item.Name)
    & "$PSScriptRoot\..\c11c_invisible_forces_v1\run_prototype.ps1" -Seed $item.Seed
    if ($LASTEXITCODE -ne 0) { throw ("Invisible Forces grammar coverage failed for seed={0}" -f $item.Seed) }
}
Write-Host "[C11-C.5-GRAMMAR] COMPLETE 6/6"
