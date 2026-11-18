# C11-E E6 Smoke18 — Family-wide Editorial Fixture V1

**Disposition:** `ADD_ONLY / PREPARE_ONLY / RUNTIME_CONSUMPTION_NOT_PROVEN`  
**Date:** 2026-11-18

## Why this overlay exists

The operator expanded the editorial requirement from Challenge-only to all three Smoke18 families. The fixture assigns distinct, synthetic Spanish editorial copy to every one of the 18 top-level rows: six Challenge, six Visual Loop and six Visual Drill. Challenge's A/B/C probes remain nested inside its six rows, producing 18 Challenge editorial targets. Loop and Drill each have six targets. The total is **18 top-level scenarios and 30 editorial targets**, not 36 Smoke18 scenarios.

The copy uses an explicit `E6` marker so it is visibly test-only. Values are assistant-authored fixture candidates under the operator-approved scope. A successful plan audit proves mapping and coverage only; actual visual consumption and comparison against each active family default must still be proven by each consumer. The Loop D pixel consumer remains blocked/not admitted.

## Family fixture copy

| Family | Title | Subtitle | CTA |
|---|---|---|---|
| Challenge | `E6 · DESAFÍO EN PRUEBA` | `RITMO Y PRECISIÓN EN PRUEBA` | `PROBAR DESAFÍO` |
| Visual Loop | `E6 · BUCLE EN PRUEBA` | `SECUENCIA VISUAL EN PRUEBA` | `REPETIR BUCLE` |
| Visual Drill | `E6 · DRILL EN PRUEBA` | `CONTROL DE SERIES EN PRUEBA` | `INICIAR SERIE` |

Each family's triplet is applied to all six of that family's rows. Challenge receives the same family triplet on A, B_REPEAT and C_CHANGED_MUSIC_SEED. The editorial assignment must not modify gameplay seed, music seed, family profile, source timebase or A/B/C isolation.

## Correct package layout

The installer is at the **archive root**, not under `payload`. This avoids the V2 README path mistake. Extract to a new temporary folder and invoke the root installer exactly as shown below.

## Install (Windows PowerShell 5.1)

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$Archive = Join-Path $env:USERPROFILE 'Downloads\C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1_20261118.zip'
$Sidecar = $Archive + '.sha256'
if (-not (Test-Path -LiteralPath $Archive -PathType Leaf) -or -not (Test-Path -LiteralPath $Sidecar -PathType Leaf)) { throw 'ARCHIVE_OR_SIDECAR_MISSING' }
$Expected = ((Get-Content -LiteralPath $Sidecar -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$Actual = (Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) { throw "ZIP_SHA256_MISMATCH:$Actual" }
Write-Host "ZIP_SHA256=PASS/$Actual"
$PackageRoot = Join-Path $env:TEMP ('C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $PackageRoot | Out-Null
Expand-Archive -LiteralPath $Archive -DestinationPath $PackageRoot
$Installer = Join-Path $PackageRoot 'INSTALL_C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.ps1'
if (-not (Test-Path -LiteralPath $Installer -PathType Leaf)) { throw "INSTALLER_NOT_AT_ARCHIVE_ROOT:$Installer" }
Write-Host "INSTALLER_PATH=PASS/$Installer"
Unblock-File -LiteralPath $Installer
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Installer -ProjectRoot $ProjectRoot -PackageRoot $PackageRoot
$InstallExit = $LASTEXITCODE
if ($InstallExit -ne 0) { throw "FAMILY_EDITORIAL_INSTALL_FAILED:$InstallExit; PRESERVE_ALL_EVIDENCE" }
```

The installer verifies PowerShell 5.1 AST for itself and the runner, package manifest/sidecar, every payload SHA-256 and byte count, all add-only collisions, protected C11-C and D4.8 pins, and four predecessor evidence pins before writing. It skips byte-identical destinations and aborts on any differing destination. It does not use Git.

## Run audit (only after exact install PASS)

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\RUN_C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.ps1'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw "RUNNER_NOT_INSTALLED:$Runner" }
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner -ProjectRoot $ProjectRoot -PythonExe $PythonExe
$AuditExit = $LASTEXITCODE
if ($AuditExit -ne 0) { throw "FAMILY_EDITORIAL_AUDIT_FAILED:$AuditExit; PRESERVE_REPORT_AND_LOGS" }
```

Expected: `UNIT_TEST_EXIT=0`, `SMOKE18_TOP_LEVEL_ROWS=18/18`, `EDITORIAL_TARGETS=30/30`, and a receipt `PASS_PREPARE_ONLY_18_ROWS_30_TARGETS_RUNTIME_CONSUMPTION_NOT_PROVEN`.

## What this does not do

- It does not rewrite the existing Challenge PREPARE_ONLY input manifest, 18 E1 intents, 18 D envelopes or their receipts.
- It does not mutate C11-C, D4.8, canonical family definitions, product defaults, E1 request defaults or existing E4 media/evidence.
- It does not claim rendered text has been consumed or visually accepted.
- It does not implement the missing Loop D compositor.
- It does not invoke Godot, FFmpeg, FFprobe, D3/audio, PCM, mux, renderer, dispatch, BatchId or media creation.
- It does not authorize E6 media execution, freeze Matrix, release or promotion.

## Immutable anchors

C11-C frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. D4.8 R1V V2 SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`, unchanged and BLOCKED. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`.
