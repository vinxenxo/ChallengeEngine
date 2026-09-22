# run_c11c_full_coverage.ps1
# C11-C v1.8.1: grammar coverage + export de assets.

$RepoRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$BulkDir  = Join-Path $RepoRoot 'tools\prototypes\c11c_bulk'

$Steps = @(
    @{ Name = 'Invisible Forces (seed=4 quadrupole crash)'; Script = 'run_invisible_forces_grammar_coverage.ps1' },
    @{ Name = 'Fractal Bloom (zoom no protagonista)';       Script = 'run_fractal_bloom_grammar_coverage.ps1' },
    @{ Name = 'Living Particles (colorways)';               Script = 'run_living_particles_grammar_coverage.ps1' },
    @{ Name = 'Sacred Symmetry (metales + accent)';         Script = 'run_sacred_symmetry_grammar_coverage.ps1' },
    @{ Name = 'Geometric Waves (fenomenos de onda)';        Script = 'run_geometric_waves_grammar_coverage.ps1' },
    @{ Name = 'Export review assets';                       Script = 'export_all_review_assets.ps1' }
)

if (-not (Test-Path $RepoRoot)) {
    Write-Host "ERROR: no existe el repo en $RepoRoot" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $BulkDir)) {
    Write-Host "ERROR: no existe $BulkDir" -ForegroundColor Red
    Write-Host "Has extraido el overlay v1.8.1 sobre el repo?" -ForegroundColor Yellow
    exit 1
}

Push-Location $RepoRoot

$resultados  = @()
$inicioTotal = Get-Date

foreach ($step in $Steps) {
    $ruta = Join-Path $BulkDir $step.Script

    Write-Host ''
    Write-Host ('=' * 78) -ForegroundColor Cyan
    Write-Host ("> " + $step.Name) -ForegroundColor Cyan
    Write-Host ("  " + $ruta) -ForegroundColor DarkGray
    Write-Host ('=' * 78) -ForegroundColor Cyan

    if (-not (Test-Path $ruta)) {
        Write-Host '  [SKIP] no existe el script' -ForegroundColor Yellow
        $resultados += [pscustomobject]@{
            Paso     = $step.Name
            Estado   = 'SKIP'
            Segundos = $null
        }
        continue
    }

    $t0 = Get-Date
    & $ruta
    $codigo = $LASTEXITCODE
    $t1 = Get-Date

    if ($null -eq $codigo -or $codigo -eq 0) {
        $estado = 'OK'
        $color  = 'Green'
    } else {
        $estado = "FAIL (exit $codigo)"
        $color  = 'Red'
    }

    $seg = [math]::Round(($t1 - $t0).TotalSeconds, 1)
    Write-Host ("  -> $estado  ($seg s)") -ForegroundColor $color

    $resultados += [pscustomobject]@{
        Paso     = $step.Name
        Estado   = $estado
        Segundos = $seg
    }
}

Pop-Location

$totalSeg = [math]::Round(((Get-Date) - $inicioTotal).TotalSeconds, 1)

Write-Host ''
Write-Host ('=' * 78) -ForegroundColor Cyan
Write-Host (" RESUMEN - $totalSeg s en total") -ForegroundColor Cyan
Write-Host ('=' * 78) -ForegroundColor Cyan
$resultados | Format-Table -AutoSize

$fallos = @($resultados | Where-Object { $_.Estado -ne 'OK' -and $_.Estado -ne 'SKIP' })
if ($fallos.Count -eq 0) {
    Write-Host 'Todo OK. Revisa los assets exportados.' -ForegroundColor Green
    exit 0
} else {
    Write-Host "$($fallos.Count) paso(s) fallaron." -ForegroundColor Red
    exit 1
}