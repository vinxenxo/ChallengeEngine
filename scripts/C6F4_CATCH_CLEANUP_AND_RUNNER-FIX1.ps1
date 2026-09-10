$ErrorActionPreference = "Stop"

$projectRoot = (Get-Location).Path
$runAll = Join-Path $projectRoot "tests\run_all.py"
$oracle = Join-Path $projectRoot "core\execution\ChallengeLegacyRuntimeOracle.gd"
$diagnostic = Join-Path $projectRoot "tests\C6F4CatchLegacyDiagnosticTest.gd"
$cleanOracle = Join-Path $projectRoot "ChallengeLegacyRuntimeOracle-CLEAN.gd"

Write-Host "=== C6-F4.4 CATCH CLEANUP / RUNNER REGISTRATION FIX1 ==="

if (-not (Test-Path $runAll)) { throw "No existe tests\run_all.py" }
if (-not (Test-Path $oracle)) { throw "No existe core\execution\ChallengeLegacyRuntimeOracle.gd" }

# 1. Detect the optional helper first. It is a source file only and MUST NOT remain in res://.
$oracleText = Get-Content -Raw -Encoding UTF8 $oracle
$hasDiagnosticOracle = $oracleText.Contains("[ORACLE:CATCH]")

if ($hasDiagnosticOracle) {
    if (-not (Test-Path $cleanOracle)) {
        throw "El Oracle contiene instrumentación diagnóstica y no existe ChallengeLegacyRuntimeOracle-CLEAN.gd en la raíz."
    }
    Copy-Item $cleanOracle $oracle -Force
    Write-Host "[OK] Oracle restaurado a versión limpia desde el auxiliar."
}

# 2. Remove all temporary helper/diagnostic files from res:// before class scanning.
if (Test-Path $diagnostic) {
    Remove-Item $diagnostic -Force
    Write-Host "[OK] Eliminado tests\C6F4CatchLegacyDiagnosticTest.gd"
}

if (Test-Path $cleanOracle) {
    Remove-Item $cleanOracle -Force
    Write-Host "[OK] Eliminado auxiliar ChallengeLegacyRuntimeOracle-CLEAN.gd"
}

# 3. Guard: exactly one global Oracle class in the actual project tree.
$matches = @(
    Get-ChildItem -Recurse -File -Filter *.gd |
        Select-String -SimpleMatch "class_name ChallengeLegacyRuntimeOracle"
)

if ($matches.Count -ne 1) {
    $locations = ($matches | ForEach-Object { $_.Path }) -join "; "
    throw "Se esperaba exactamente 1 class_name ChallengeLegacyRuntimeOracle en res://; encontrados: $($matches.Count). Ubicaciones: $locations"
}
Write-Host "[OK] Único ChallengeLegacyRuntimeOracle confirmado."

# 4. Register the formal CATCH V2 suite idempotently.
$text = Get-Content -Raw -Encoding UTF8 $runAll
$marker = '"C6F4CanonicalV2CatchTest.gd": "[C6F4_CANONICAL_V2_CATCH_SUITE] PASS"'

if ($text.Contains($marker)) {
    Write-Host "[OK] C6F4CanonicalV2CatchTest ya está registrado."
}
else {
    $anchor = '"C6F4CanonicalV2HitTest.gd": "[C6F4_CANONICAL_V2_HIT_SUITE] PASS",'
    if (-not $text.Contains($anchor)) {
        throw "No se encontró el ancla HIT en tests\run_all.py. No se modifica el runner."
    }

    $replacement = $anchor + "`r`n    " + $marker + ","
    $newText = $text.Replace($anchor, $replacement)
    Set-Content -Path $runAll -Value $newText -Encoding UTF8 -NoNewline
    Write-Host "[OK] Registrado C6F4CanonicalV2CatchTest en run_all.py"
}

# 5. Formal test + PASS marker guard.
$catchTestPath = Join-Path $projectRoot "tests\C6F4CanonicalV2CatchTest.gd"
if (-not (Test-Path $catchTestPath)) { throw "No existe tests\C6F4CanonicalV2CatchTest.gd" }
$catchTest = Get-Content -Raw -Encoding UTF8 $catchTestPath
if (-not $catchTest.Contains("[C6F4_CANONICAL_V2_CATCH_SUITE] PASS")) {
    throw "El test CATCH no contiene el PASS marker esperado."
}
Write-Host "[OK] PASS marker normalizado."

Write-Host ""
Write-Host "C6-F4.4 CATCH cleanup completed (FIX1)."
Write-Host "No quedan auxiliares .gd duplicando el class_name global."
Write-Host ""
Write-Host "Ejecuta después:"
Write-Host "  godot --headless --path . --editor --quit"
Write-Host "  godot --headless -s .\tests\C6F4CanonicalV2CatchTest.gd"
Write-Host "  python .\tests\run_all.py"
Write-Host "  python build_factory.py --batch ./challenges --output ./output --workers 9"
