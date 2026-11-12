# C11-E E4C Drill visual composition V2.0 — consolidated installer and existing-media requalification

**Date:** 2026-11-12  
**Package:** `C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_2_20261112.zip`  
**Status:** rebuilt candidate; V2.1 path-length failure closed before destination mutation; installation/runtime qualification pending.

## What changed

V2.0 failed before transaction at Test 04 because `validate_plan()` did not bind `source_frame_viewport` to the social body. V2.1 adds the accepted fail-closed comparison to `EXPECTED_SOCIAL_REGIONS["body_rect"]`. The accepted consumer is SHA-256 `e5cf97651e546ad86e2a4d46698553038e4161dc97a55da2654f197ed71f623c`, 36,678 bytes. The 20-test module is unchanged. No proposal/decision/timebase hash, native media, D A/V executor/requalifier, E1 service, GUI/CLI, binder or C11-C source changes.

## Geometry authority

Pinned `core/presentation/PresentationProfile.gd` SHA-256 `187b1cf8ab96b9031785a0f36b0054a60383c97cb3d81906c7d9bbcd373bef24` defines `get_social_regions()` on 540x960 logical coordinates with 15% header, 70% body and 15% footer. The REVIEW_720 output is the exact 4/3 projection: canvas 720x1280; header `(0,0,720,192)`; body `(0,192,720,896)`; footer `(0,1088,720,192)`. The canvas's `aspect_ratio="9:16"` is required contract metadata, not an unexpected extra key.

## Package and transaction

- One exact-hash replacement: `tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`.
- Twenty-four `ADD_ONLY` destinations.
- Twenty-one active source pins; frozen C11-C manifest exact.
- Full ZIP/package inventory and one-to-one payload/operation closure.
- Windows PowerShell 5.1 AST 2/2; Python 3.13/PySide6/Qt offscreen; py_compile 3/3; 20/20 tests.
- File.Replace round-trip; exact pre/postimages; journal before first destination write; atomic replacement/add; SHA-guarded rollback.
- A pre-transaction failure may create a diagnostic under the designated artifacts evidence root, but no destination writes occur.

## Install

Extract to a new directory. Verify the adjacent SHA-256 sidecar before running. Do not extract over the active checkout. Do not use V1.7, V1.8 or V1.9.

```powershell
$Zip = "$env:USERPROFILE\Downloads\C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_1_20261112.zip"
$Package = "$env:USERPROFILE\Downloads\C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_1_20261112"
$Expected = ((Get-Content -LiteralPath "$Zip.sha256" -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$Actual = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) { throw "ZIP_SHA_MISMATCH: $Actual != $Expected" }
if (Test-Path -LiteralPath $Package) { throw "PACKAGE_DIRECTORY_ALREADY_EXISTS: $Package" }
Expand-Archive -LiteralPath $Zip -DestinationPath $Package
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File "$Package\INSTALL_C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_V2_2.ps1" `
  -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS" `
  -PythonExe "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" `
  -PackageZip $Zip
```

Required output before transaction: `PACKAGE_INVENTORY=27/27 PASS`, `SOURCE_PINS=21/21 PASS`, `POWERSHELL_AST=2/2 PASS`, `DESTINATION_CLASSIFICATION=1_REPLACE+24_ADD_ONLY`, `PY_COMPILE=3/3 PASS`, `STAGED_TESTS=20/20 PASS`, `FILE_REPLACE_PREFLIGHT=FORWARD_AND_ROLLBACK_PASS`, `IMMEDIATE_RECHECK=PASS`. Installation must end `PASS_REPLACE_AND_ADD_ONLY_INSTALL`; otherwise stop and preserve diagnostics. Do not edit the installer or package manually.

## Existing-media requalification after install only

Use the already captured CLI MP4 and WAV A/B/C. Do not invoke Godot, C11-C native capture, GUI/CLI smoke or music generation.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File ".\tools\c11d\d9\RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1" `
  -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS" `
  -PythonExe "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" `
  -EvidenceRoot ".\artifacts\production\c11e\E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8"
```

Acceptance: 630/630 GAME body frames byte-exact, 180/180 full-frame PRE_ROLL/END_CTA identity, 90/630/90 mapping, 91/91 support pins, H.264 A/B/C identical, WAV/AAC A/B identical and C distinct, FFprobe/audio-video sync correct. The receipt remains pending operator visual/audio acceptance. Exported review frames and media are evidence, not approval.

## Governance

C11-C 2.19.12 is sole production authority. Frozen manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. E1 remains `PREPARE_ONLY` / `NOT_CONNECTED_E1`. No Git, no pip, no C11-C mutation, no production dispatch, `release_authority=NONE`. E4C remains open until operator acceptance and 20/20 A/V matrix.
