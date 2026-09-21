$ErrorActionPreference = "Stop"
$families = @(
    @{ Seed = 1; Name = "radial_bloom" },
    @{ Seed = 2; Name = "dendritic_tunnel" },
    @{ Seed = 3; Name = "spiral_fractal" },
    @{ Seed = 7; Name = "fractal_filigree" },
    @{ Seed = 11; Name = "nested_worlds" }
)
foreach ($item in $families) {
    Write-Host ("[C11-C.2-GRAMMAR] START seed={0} mode={1}" -f $item.Seed, $item.Name)
    & "$PSScriptRoot\..\c11c_fractal_bloom_v1\run_prototype.ps1" -Seed $item.Seed
    if ($LASTEXITCODE -ne 0) { throw ("Fractal Bloom grammar coverage failed for seed={0}" -f $item.Seed) }
}
Write-Host "[C11-C.2-GRAMMAR] COMPLETE 5/5"
