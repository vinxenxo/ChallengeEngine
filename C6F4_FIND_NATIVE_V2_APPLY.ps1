$ErrorActionPreference = "Stop"

$projectRoot = (Get-Location).Path
$findMechanic = Join-Path $projectRoot "core\mechanics\find\FindMechanic.gd"
$bridge = Join-Path $projectRoot "core\execution\ChallengeRuntimeBridge.gd"
$runAll = Join-Path $projectRoot "tests\run_all.py"
$testTarget = Join-Path $projectRoot "tests\C6F4CanonicalV2FindTest.gd"

Write-Host "=== C6-F4.4 PHASE 5 FIND — NATIVE CANONICAL V2 APPLY ==="

foreach ($path in @($findMechanic, $bridge, $runAll)) {
    if (-not (Test-Path $path)) {
        throw "Falta archivo requerido: $path"
    }
}

# ------------------------------------------------------------
# 0. Guard: Phase 5 must start from the expected F4.4 structure.
# ------------------------------------------------------------
$findText = Get-Content -Raw -Encoding UTF8 $findMechanic
$bridgeText = Get-Content -Raw -Encoding UTF8 $bridge
$runnerText = Get-Content -Raw -Encoding UTF8 $runAll

$findLegacyRead = 'var find_cfg: Dictionary = config.get("difficulty", {}).get("find", {})'
$findLegacyCount = ([regex]::Matches($findText, [regex]::Escape($findLegacyRead))).Count

if ($findLegacyCount -ne 3) {
    throw "Guard FIND: se esperaban exactamente 3 lecturas legacy de difficulty.find; encontradas: $findLegacyCount. No se modifica FindMechanic.gd."
}

if ($bridgeText.Contains('if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1", "find_v1"]')) {
    Write-Host "[INFO] find_v1 ya figura en el conjunto native-V2. No se volverá a insertar."
}
elseif ($bridgeText.Contains('if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1"]')) {
    $oldNative = 'if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1"]'
    $newNative = 'if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1", "find_v1"]'
    $bridgeText = $bridgeText.Replace($oldNative, $newNative)
    Write-Host "[OK] Bridge: find_v1 añadido al conjunto native-V2."
}
else {
    throw "Guard Bridge: no se encontró exactamente la frontera native-V2 esperada de F4.4-P4. No se modifica el bridge."
}

# ------------------------------------------------------------
# 1. FIND: V2-first parameter source, legacy fallback.
#    Do this once and reuse it in setup/calculate_frame/simulate.
# ------------------------------------------------------------
$replacementRead = 'var find_cfg: Dictionary = _get_find_config(config)'
$findText = $findText.Replace($findLegacyRead, $replacementRead)

if ($findText.Contains($findLegacyRead)) {
    throw "No se pudieron sustituir todas las lecturas legacy de difficulty.find."
}

$helper = @'
func _get_find_config(config: Dictionary) -> Dictionary:
	var simulation_cfg: Dictionary = config.get("simulation", {})
	if simulation_cfg is Dictionary:
		var params = simulation_cfg.get("parameters", {})
		if params is Dictionary:
			var v2_find = params.get("find", {})
			if v2_find is Dictionary and not v2_find.is_empty():
				return v2_find.duplicate(true)

	var legacy_difficulty = config.get("difficulty", {})
	if legacy_difficulty is Dictionary:
		var legacy_find = legacy_difficulty.get("find", {})
		if legacy_find is Dictionary:
			return legacy_find.duplicate(true)

	return {}
'@

if (-not $findText.Contains("func _get_find_config(config: Dictionary) -> Dictionary:")) {
    $anchor = "func calculate_frame(f: int, config: Dictionary) -> Dictionary:"
    if (-not $findText.Contains($anchor)) {
        throw "No se encontró el ancla calculate_frame() para insertar _get_find_config()."
    }
    $findText = $findText.Replace($anchor, $helper + "`r`n" + $anchor)
    Write-Host "[OK] FindMechanic: helper V2-first creado con fallback legacy."
}
else {
    Write-Host "[INFO] FindMechanic: helper _get_find_config() ya existía."
}

# ------------------------------------------------------------
# 2. Write only the intended source files.
# ------------------------------------------------------------
Set-Content -Path $findMechanic -Value $findText -Encoding UTF8 -NoNewline
Set-Content -Path $bridge -Value $bridgeText -Encoding UTF8 -NoNewline

# ------------------------------------------------------------
# 3. Install the dedicated FIND V2 suite.
# ------------------------------------------------------------
if (-not (Test-Path $testTarget)) {
    throw "El script no contiene el test materializado. Copia C6F4CanonicalV2FindTest.gd a tests\ antes de ejecutar."
}

$findTestText = Get-Content -Raw -Encoding UTF8 $testTarget
if (-not $findTestText.Contains("[C6F4_CANONICAL_V2_FIND_SUITE] PASS")) {
    throw "El test FIND no contiene el PASS marker requerido."
}

$findMarker = '"C6F4CanonicalV2FindTest.gd": "[C6F4_CANONICAL_V2_FIND_SUITE] PASS"'
if ($runnerText.Contains($findMarker)) {
    Write-Host "[INFO] FIND test ya está registrado en tests\run_all.py."
}
else {
    $anchor = '"C6F4CanonicalV2CatchTest.gd": "[C6F4_CANONICAL_V2_CATCH_SUITE] PASS",'
    if (-not $runnerText.Contains($anchor)) {
        throw "No se encontró el ancla CATCH en tests\run_all.py. No se modifica el runner."
    }
    $replacement = $anchor + "`r`n    " + $findMarker + ","
    $runnerText = $runnerText.Replace($anchor, $replacement)
    Set-Content -Path $runAll -Value $runnerText -Encoding UTF8 -NoNewline
    Write-Host "[OK] Runner: C6F4CanonicalV2FindTest registrado."
}

# ------------------------------------------------------------
# 4. Static guards.
# ------------------------------------------------------------
$findTextFinal = Get-Content -Raw -Encoding UTF8 $findMechanic
$bridgeTextFinal = Get-Content -Raw -Encoding UTF8 $bridge
$runnerTextFinal = Get-Content -Raw -Encoding UTF8 $runAll

$remainingLegacy = ([regex]::Matches($findTextFinal, [regex]::Escape($findLegacyRead))).Count
if ($remainingLegacy -ne 0) {
    throw "Quedan lecturas directas de difficulty.find en FindMechanic.gd."
}

$helperCount = ([regex]::Matches($findTextFinal, [regex]::Escape("func _get_find_config(config: Dictionary) -> Dictionary:"))).Count
if ($helperCount -ne 1) {
    throw "Se esperaba exactamente 1 helper _get_find_config(); encontrados: $helperCount."
}

if (-not $bridgeTextFinal.Contains('if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1", "find_v1"]')) {
    throw "find_v1 no quedó registrado en la frontera native-V2 del bridge."
}

if (-not $runnerTextFinal.Contains($findMarker)) {
    throw "C6F4CanonicalV2FindTest no quedó registrado en run_all.py."
}

Write-Host ""
Write-Host "C6-F4.4 Phase 5 FIND patch prepared."
Write-Host "Principio preservado: V2-first; legacy fallback; ecuaciones/RNG sin cambios."
Write-Host ""
Write-Host "Ejecuta después:"
Write-Host "  godot --headless --path . --editor --quit"
Write-Host "  godot --headless -s .\tests\C6F4CanonicalV2FindTest.gd"
Write-Host "  python .\tests\run_all.py"
Write-Host "  python build_factory.py --batch ./challenges --output ./output --workers 9"
