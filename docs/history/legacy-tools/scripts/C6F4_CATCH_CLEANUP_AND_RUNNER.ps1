$ErrorActionPreference = "Stop"

$projectRoot = (Get-Location).Path
$runAll = Join-Path $projectRoot "tests\run_all.py"
$oracle = Join-Path $projectRoot "core\execution\ChallengeLegacyRuntimeOracle.gd"
$diagnostic = Join-Path $projectRoot "tests\C6F4CatchLegacyDiagnosticTest.gd"
$cleanOracle = Join-Path $projectRoot "ChallengeLegacyRuntimeOracle-CLEAN.gd"

Write-Host "=== C6-F4.4 CATCH CLEANUP / RUNNER REGISTRATION ==="

if (-not (Test-Path $runAll)) {
    throw "No existe tests\run_all.py"
}

if (-not (Test-Path $oracle)) {
    throw "No existe core\execution\ChallengeLegacyRuntimeOracle.gd"
}

# 1. Guard: exactly one global Oracle class in res://
$duplicates = Get-ChildItem -Recurse -Filter *.gd |
    Select-String "class_name ChallengeLegacyRuntimeOracle"

if ($duplicates.Count -ne 1) {
    throw "Se esperaba exactamente 1 class_name ChallengeLegacyRuntimeOracle; encontrados: $($duplicates.Count)"
}

# 2. Restore clean Oracle only when a diagnostic marker is present.
$oracleText = Get-Content -Raw -Encoding UTF8 $oracle

if ($oracleText.Contains("[ORACLE:CATCH]")) {
    if (-not (Test-Path $cleanOracle)) {
        throw "El Oracle contiene instrumentación diagnóstica pero no existe el archivo CLEAN."
    }

    Copy-Item $cleanOracle $oracle -Force
    Write-Host "[OK] Oracle restaurado a versión limpia."
}
else {
    Write-Host "[OK] Oracle ya está limpio."
}

# 3. Remove temporary diagnostic suite. It is deliberately NOT registered.
if (Test-Path $diagnostic) {
    Remove-Item $diagnostic -Force
    Write-Host "[OK] Eliminado tests\C6F4CatchLegacyDiagnosticTest.gd"
}
else {
    Write-Host "[OK] No existe el diagnóstico temporal."
}

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

    if ($newText -eq $text) {
        throw "No se pudo registrar C6F4CanonicalV2CatchTest."
    }

    Set-Content -Path $runAll -Value $newText -Encoding UTF8 -NoNewline
    Write-Host "[OK] Registrado C6F4CanonicalV2CatchTest en run_all.py"
}

# 5. Validate the formal PASS marker expected by run_all.
if (-not (Test-Path (Join-Path $projectRoot "tests\C6F4CanonicalV2CatchTest.gd"))) {
    throw "No existe tests\C6F4CanonicalV2CatchTest.gd"
}

$catchTest = Get-Content -Raw -Encoding UTF8 (Join-Path $projectRoot "tests\C6F4CanonicalV2CatchTest.gd")

if (-not $catchTest.Contains("[C6F4_CANONICAL_V2_CATCH_SUITE] PASS")) {
    throw "El test CATCH no contiene el PASS marker esperado."
}

Write-Host "[OK] PASS marker normalizado: [C6F4_CANONICAL_V2_CATCH_SUITE] PASS"

# 6. Final class-count guard.
$duplicatesAfter = Get-ChildItem -Recurse -Filter *.gd |
    Select-String "class_name ChallengeLegacyRuntimeOracle"

if ($duplicatesAfter.Count -ne 1) {
    throw "Guard final fallido: class_name ChallengeLegacyRuntimeOracle duplicado."
}

Write-Host ""
Write-Host "C6-F4.4 CATCH cleanup completed."
Write-Host "Archivos permanentes:"
Write-Host "  - core\execution\ChallengeLegacyRuntimeOracle.gd"
Write-Host "  - tests\C6F4CanonicalV2CatchTest.gd"
Write-Host "  - tests\run_all.py"
Write-Host ""
Write-Host "El archivo CLEAN se usa solo como fuente de restauración:"
Write-Host "  - ChallengeLegacyRuntimeOracle-CLEAN.gd"
Write-Host ""
Write-Host "Ejecuta después:"
Write-Host "  godot --headless --path . --editor --quit"
Write-Host "  godot --headless -s .\tests\C6F4CanonicalV2CatchTest.gd"
Write-Host "  python .\tests\run_all.py"
Write-Host "  python build_factory.py --batch ./challenges --output ./output --workers 9"
