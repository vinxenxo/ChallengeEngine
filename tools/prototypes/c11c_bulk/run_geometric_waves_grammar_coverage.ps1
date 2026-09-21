param(
    [int[]]$Seeds = @(1, 2, 4, 7, 30)
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$Launcher = Join-Path $ProjectRoot 'tools\prototypes\c11c_geometric_waves_v1\run_prototype.ps1'

foreach ($Seed in $Seeds) {
    Write-Host "[C11-C.1-V1.5] START grammar coverage seed=$Seed"
    & $Launcher -Seed $Seed
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        throw "Geometric grammar coverage failed for seed=${Seed}: exit=${exitCode}"
    }
    Write-Host "[C11-C.1-V1.5] PASS grammar coverage seed=$Seed"
}

Write-Host '[C11-C.1-V1.5] GRAMMAR COVERAGE COMPLETE'
