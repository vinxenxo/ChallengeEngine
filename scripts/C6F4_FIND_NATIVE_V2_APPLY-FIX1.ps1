$ErrorActionPreference = "Stop"

$projectRoot = (Get-Location).Path
$findMechanic = Join-Path $projectRoot "core\mechanics\find\FindMechanic.gd"
$bridge = Join-Path $projectRoot "core\execution\ChallengeRuntimeBridge.gd"
$runAll = Join-Path $projectRoot "tests\run_all.py"
$testTarget = Join-Path $projectRoot "tests\C6F4CanonicalV2FindTest.gd"

Write-Host "=== C6-F4.4 PHASE 5 FIND - NATIVE CANONICAL V2 APPLY FIX1 ==="

foreach ($path in @($findMechanic, $bridge, $runAll, $testTarget)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing required file: $path"
    }
}

# ------------------------------------------------------------
# 0. Guards: expected F4.4-P4 source shape.
# ------------------------------------------------------------
$findText = Get-Content -LiteralPath $findMechanic -Raw -Encoding UTF8
$bridgeText = Get-Content -LiteralPath $bridge -Raw -Encoding UTF8
$runnerText = Get-Content -LiteralPath $runAll -Raw -Encoding UTF8
$findTestText = Get-Content -LiteralPath $testTarget -Raw -Encoding UTF8

$findLegacyRead = 'var find_cfg: Dictionary = config.get("difficulty", {}).get("find", {})'
$findLegacyCount = ([regex]::Matches($findText, [regex]::Escape($findLegacyRead))).Count

if ($findLegacyCount -ne 3) {
    throw "Guard FIND failed: expected exactly 3 legacy difficulty.find reads, found $findLegacyCount. No source file was modified."
}

$nativeCurrent = 'if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1", "find_v1"]'
$nativePrevious = 'if mechanic_id in ["pilot", "parking_v2", "hit_v1", "catch_v1"]'

if ($bridgeText.Contains($nativeCurrent)) {
    Write-Host "[INFO] Bridge already contains find_v1 in native-V2 set."
}
elseif ($bridgeText.Contains($nativePrevious)) {
    $bridgeText = $bridgeText.Replace($nativePrevious, $nativeCurrent)
    Write-Host "[OK] Bridge: find_v1 added to native-V2 set."
}
else {
    throw "Guard Bridge failed: expected F4.4-P4 native-V2 boundary was not found. No source file was modified."
}

# ------------------------------------------------------------
# 1. FIND: V2-first configuration helper.
#    Avoid PowerShell here-strings entirely for PS 5.1 safety.
# ------------------------------------------------------------
$replacementRead = 'var find_cfg: Dictionary = _get_find_config(config)'
$findText = $findText.Replace($findLegacyRead, $replacementRead)

if ($findText.Contains($findLegacyRead)) {
    throw "Not all legacy difficulty.find reads were replaced."
}

$helperSignature = 'func _get_find_config(config: Dictionary) -> Dictionary:'

if (-not $findText.Contains($helperSignature)) {
    $anchor = 'func calculate_frame(f: int, config: Dictionary) -> Dictionary:'
    if (-not $findText.Contains($anchor)) {
        throw "Guard FIND failed: calculate_frame anchor was not found."
    }

    $helperLines = @(
        'func _get_find_config(config: Dictionary) -> Dictionary:',
        "`tvar simulation_cfg: Dictionary = config.get(" + '"' + 'simulation' + '"' + ", {})",
        "`tif simulation_cfg is Dictionary:",
        "`t`tvar params = simulation_cfg.get(" + '"' + 'parameters' + '"' + ", {})",
        "`t`tif params is Dictionary:",
        "`t`t`tvar v2_find = params.get(" + '"' + 'find' + '"' + ", {})",
        "`t`t`tif v2_find is Dictionary and not v2_find.is_empty():",
        "`t`t`t`treturn v2_find.duplicate(true)",
        "",
        "`tvar legacy_difficulty = config.get(" + '"' + 'difficulty' + '"' + ", {})",
        "`tif legacy_difficulty is Dictionary:",
        "`t`tvar legacy_find = legacy_difficulty.get(" + '"' + 'find' + '"' + ", {})",
        "`t`tif legacy_find is Dictionary:",
        "`t`t`treturn legacy_find.duplicate(true)",
        "",
        "`treturn {}"
    )
    $helper = ($helperLines -join "`r`n") + "`r`n"
    $findText = $findText.Replace($anchor, $helper + $anchor)
    Write-Host "[OK] FindMechanic: V2-first helper inserted."
}
else {
    Write-Host "[INFO] FindMechanic: V2-first helper already exists."
}

# ------------------------------------------------------------
# 2. Write only the intended source files.
# ------------------------------------------------------------
Set-Content -LiteralPath $findMechanic -Value $findText -Encoding UTF8
Set-Content -LiteralPath $bridge -Value $bridgeText -Encoding UTF8

# ------------------------------------------------------------
# 3. Register the dedicated FIND suite in run_all.py.
# ------------------------------------------------------------
$findPassMarker = '"C6F4CanonicalV2FindTest.gd": "[C6F4_CANONICAL_V2_FIND_SUITE] PASS"'
$catchAnchor = '"C6F4CanonicalV2CatchTest.gd": "[C6F4_CANONICAL_V2_CATCH_SUITE] PASS",'

$runnerTextCurrent = Get-Content -LiteralPath $runAll -Raw -Encoding UTF8
if ($runnerTextCurrent.Contains($findPassMarker)) {
    Write-Host "[INFO] FIND test is already registered in run_all.py."
}
else {
    if (-not $runnerTextCurrent.Contains($catchAnchor)) {
        throw "Guard runner failed: CATCH registration anchor was not found."
    }

    $runnerReplacement = $catchAnchor + "`r`n    " + $findPassMarker + ","
    $runnerTextCurrent = $runnerTextCurrent.Replace($catchAnchor, $runnerReplacement)
    Set-Content -LiteralPath $runAll -Value $runnerTextCurrent -Encoding UTF8
    Write-Host "[OK] Runner: C6F4CanonicalV2FindTest registered."
}

# ------------------------------------------------------------
# 4. Static post-write guards.
# ------------------------------------------------------------
$findTextFinal = Get-Content -LiteralPath $findMechanic -Raw -Encoding UTF8
$bridgeTextFinal = Get-Content -LiteralPath $bridge -Raw -Encoding UTF8
$runnerTextFinal = Get-Content -LiteralPath $runAll -Raw -Encoding UTF8

$remainingLegacy = ([regex]::Matches($findTextFinal, [regex]::Escape($findLegacyRead))).Count
if ($remainingLegacy -ne 0) {
    throw "Post-write guard failed: direct difficulty.find reads remain in FindMechanic.gd."
}

$helperCount = ([regex]::Matches($findTextFinal, [regex]::Escape($helperSignature))).Count
if ($helperCount -ne 1) {
    throw "Post-write guard failed: expected exactly 1 _get_find_config helper, found $helperCount."
}

if (-not $bridgeTextFinal.Contains($nativeCurrent)) {
    throw "Post-write guard failed: find_v1 is not in native-V2 bridge set."
}

if (-not $runnerTextFinal.Contains($findPassMarker)) {
    throw "Post-write guard failed: FIND test is not registered in run_all.py."
}

if (-not $findTestText.Contains("[C6F4_CANONICAL_V2_FIND_SUITE] PASS")) {
    throw "Guard test failed: FIND suite PASS marker is missing."
}

Write-Host ""
Write-Host "C6-F4.4 Phase 5 FIND FIX1 applied successfully."
Write-Host "Preserved: RNG, FIND equations, SimulationResult, WinningFrameDetector, VideoTimeline, build_factory."
Write-Host ""
Write-Host "Next gates:"
Write-Host "  godot --headless --path . --editor --quit"
Write-Host "  godot --headless -s .\tests\C6F4CanonicalV2FindTest.gd"
Write-Host "  python .\tests\run_all.py"
Write-Host "  python build_factory.py --batch ./challenges --output ./output --workers 9"
