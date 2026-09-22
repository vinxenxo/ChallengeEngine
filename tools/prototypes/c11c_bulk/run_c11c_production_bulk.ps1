param(
    [int[]]$Seeds = @(314159,271828,161803,112358,577215,8675309,424242,990001),
    [switch]$NoSound,
    [switch]$NoFooter
)
$ErrorActionPreference = 'Stop'
$families = @('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1')
foreach ($family in $families) {
    foreach ($seed in $Seeds) {
        $launcher = Join-Path $PSScriptRoot ("..\$family\run_prototype.ps1")
        if (-not (Test-Path -LiteralPath $launcher)) { throw "Launcher missing: $launcher" }
        Write-Host "[C11-C-PROD] START family=$family seed=$seed"
        $args = @('-Seed',[string]$seed)
        if ($NoSound) { $args += '-NoSound' }
        if ($NoFooter) { $args += '-NoFooter' }
        & $launcher @args
        if ($LASTEXITCODE -ne 0) { throw "Production bulk failed for ${family} seed=${seed}: exit=$LASTEXITCODE" }
        Write-Host "[C11-C-PROD] PASS family=$family seed=$seed"
    }
}
Write-Host "[C11-C-PROD] COMPLETE renders=$($families.Count * $Seeds.Count)"
