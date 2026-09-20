$ErrorActionPreference = 'Stop'

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\\..\\..')).Path
$families = @(
    'c11c_sacred_symmetry_v1',
    'c11c_living_particles_v1',
    'c11c_invisible_forces_v1'
)

foreach ($family in $families) {
    $launcher = Join-Path $ProjectRoot ("tools\\prototypes\\$family\\run_prototype.ps1")
    if (-not (Test-Path -LiteralPath $launcher)) {
        throw "Missing launcher: $launcher"
    }
    Write-Host "[C11-C-BULK] START $family"
    & powershell -NoProfile -ExecutionPolicy Bypass -File $launcher
    $launcherExit = $LASTEXITCODE
    if ($launcherExit -ne 0) {
        throw "Bulk run failed for ${family}: exit=${launcherExit}"
    }
    Write-Host "[C11-C-BULK] PASS $family"
}

Write-Host '[C11-C-BULK] REMAINING VISUAL LOOP PROTOTYPES COMPLETE'
