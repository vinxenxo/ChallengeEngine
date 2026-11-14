# C11-E E4C V2.3 R4 — Install, audit and recover existing V2 outputs

**Purpose:** complete the R3 `tracking/tier-1` run without repeating its successful 810-frame composition or A/B/C audio mux.

## Accepted upstream state

- R3 package install: PASS (`1 REPLACE + 16 ADD` is R4 only; R3 itself was `2 REPLACE + 15 ADD`).
- R3 independent post-install audit: PASS.
- R3 output id: `E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9`.
- R3 output inventory: silent V2 intermediate 785,860 bytes, A/B MP4 1,455,889 bytes each, C MP4 1,454,787 bytes. Exact SHA-256 values are pinned by the recovery utility.
- R3 error: FFmpeg rejected `-vsync` during review frame 0 extraction. Composition, three muxes and elementary stream equality checks had already returned successfully.

## 1. Install R4 overlay

Download the ZIP and `.sha256` sidecar into `Downloads`. Run from the active checkout:

```powershell
$ErrorActionPreference = "Stop"
$Project = "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
$Zip = "$env:USERPROFILE\Downloads\C11E_E4C_DRILL_HISTORICAL_REQUALIFIER_V2_3_R4_20261114.zip"
$Package = "$env:USERPROFILE\Downloads\C11E_E4C_DRILL_HISTORICAL_REQUALIFIER_V2_3_R4_20261114"
$Expected = ((Get-Content -LiteralPath "$Zip.sha256" -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$Actual = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) { throw "R4_ZIP_SHA_MISMATCH" }
if (Test-Path -LiteralPath $Package) { throw "R4_PACKAGE_DIRECTORY_ALREADY_EXISTS" }
Expand-Archive -LiteralPath $Zip -DestinationPath $Package
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File "$Package\INSTALL_C11E_E4C_V2_3_R4_FFMPEG_REVIEW_RECOVERY.ps1" `
  -ProjectRoot $Project `
  -PythonExe "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" `
  -PackageZip $Zip
if ($LASTEXITCODE -ne 0) { throw "C11E_E4C_V2_3_R4_INSTALL_FAILED" }
```

Expected: `PACKAGE_FILES=20/20`, 21/21 source pins, frozen C11-C, PowerShell AST 3/3, `py_compile=3/3`, recovery contract tests 12/12, File.Replace forward/rollback, and `INSTALL_STATUS=PASS_REPLACE_AND_ADD_ONLY_INSTALL` with **1 REPLACE + 16 ADD_ONLY**.

## 2. Independent installation audit

Use the exact `RUN_ID` printed by the installer:

```powershell
$Audit = "$Package\VERIFY_C11E_E4C_V2_3_R4_INSTALL_V1.ps1"
$RunId = "PASTE_EXACT_R4_RUN_ID_FROM_INSTALLER"
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File $Audit `
  -ProjectRoot $Project `
  -PackageRoot $Package `
  -PackageZip $Zip `
  -RunId $RunId
if ($LASTEXITCODE -ne 0) { throw "R4_INDEPENDENT_AUDIT_FAILED" }
```

Do not proceed unless `INDEPENDENT_AUDIT_STATUS=PASS_INDEPENDENT_POST_INSTALL_AUDIT` and the receipt exists. This audit verifies the one replacement, sixteen additions, 17 postimages, one backup, 21 source pins, frozen C11-C and immutable operator decision JSON.

## 3. Recover the existing R3 output — no recomposition or remux

Only after R4 audit PASS:

```powershell
$Recovery = Join-Path $Project "tools\c11d\d9\RECOVER_C11E_E4C_V2_EXISTING_OUTPUT_REVIEW_V1.py"
$EvidenceRoot = Join-Path $Project "artifacts\production\c11e\E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8"
$OutputId = "E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9"
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -u $Recovery `
  --project-root $Project `
  --evidence-root $EvidenceRoot `
  --output-id $OutputId
if ($LASTEXITCODE -ne 0) { throw "E4C_V2_EXISTING_OUTPUT_RECOVERY_FAILED" }
```

The recovery utility is cryptographically pinned to this single R3 output id. It rechecks the original accepted receipt/intent, 91 E1 pins, frozen manifest, exact saved V2 composition plan, silent intermediate and A/B/C MP4 hashes; FFprobes the native/silent/final media; recomputes video and audio elementary stream hashes; confirms video A/B/C equality and AAC A/B equality/C difference; then extracts seven PNG stills using `-fps_mode passthrough`.

It does **not** invoke `compose_all_frames_v2`, `mux_audio`, C11-C, Godot or FAMILY_MUSIC_V4. `frame_composition_repeated=false` and `audio_mux_repeated=false` are recorded in the receipt. Existing review PNGs are never overwritten.

Expected technical status:

```text
PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE
REVIEW_FRAMES=7/7 PASS
VIDEO_STREAM_HASHES_A_B_C_IDENTICAL=PASS
AUDIO_STREAM_HASHES_A_B_IDENTICAL_C_DISTINCT=PASS
FFPROBE=27_SECONDS_810_FRAMES_H264_HIGH_YUV420P_TV_AAC_LC_48K_STEREO
E1_SOURCE_PINS=91/91 UNCHANGED
PRODUCTION_DISPATCH=FALSE
RELEASE_AUTHORITY=NONE
```

The script produces:

- `E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json`
- `V2_EXISTING_OUTPUT_RECOVERY_AUDIT.json`
- `OPERATOR_REVIEW_CHECKLIST.md`
- Seven PNGs in `operator_review`
- `E4C_V2_OPERATOR_REVIEW_BUNDLE.zip` containing the three final MP4s, seven review images and the receipts

## 4. Human review and phase status

The receipt is technical only. Review all seven images and watch/listen to A/B/C. The V2 selector count remains 0/20 until the operator expressly accepts visual and audio quality for `tracking/tier-1`. Only then record 1/20 and qualify the other 19 selectors. E4C closes at 20/20, then E5 → E6 Smoke18 → E7 Matrix101 → E8.

## Governance and no-repeat rules

Do not repeat R3 installation/audit, the R3 810-frame composition, the three muxes, the accepted E1 CLI smoke, GUI smoke, native capture, Godot or family music generation. R2/R3 failures remain historical evidence and must not be deleted. C11-C remains frozen (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`); E1 remains PREPARE_ONLY; family adapter NOT_CONNECTED_E1; production dispatch false; release authority NONE. `GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`.
