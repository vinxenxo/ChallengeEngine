# C11-E E6 Option C — Native Qt/QImage probe V2 — Runbook

## Purpose

Run the exact A3 lineage adjudication and then the 37 target QImage tests plus a 7-iteration synthetic one-frame benchmark on the existing Windows runtime. No renderer/media process is invoked.

## Install

1. Preserve the V1 blocked receipt. Do not rerun V1.
2. Download the ZIP, its `.sha256` sidecar and the separate installer `.ps1`. Do not extract files over the checkout.
3. Invoke the standalone installer through a child Windows PowerShell 5.1 process. It opens the ZIP itself, stages to a unique `%TEMP%` directory, validates its self-hash against the ZIP member and uses the exact install destinations pinned by the package manifest.
4. It checks the frozen C11-C and D4.8 V2 pins, completes all destination collision checks before the first write, uses sibling `CreateNew` temp files and non-overwriting atomic moves, verifies postimages and writes an install receipt/sidecar. Existing identical files are skipped; differing files block without overwrite.

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$PackageZip = 'C:\PATH\TO\C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2.zip'
$ExpectedZipSha256 = 'REPLACE_WITH_THE_SHA256_PRINTED_WITH_THE_DELIVERABLE'
$Installer = 'C:\PATH\TO\INSTALL_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2.ps1'
& (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File $Installer -ProjectRoot $ProjectRoot -PackageZip $PackageZip -ExpectedPackageZipSha256 $ExpectedZipSha256
$InstallExit = $LASTEXITCODE
if ($InstallExit -ne 0) { throw "E6_OPTION_C_QT_V2_INSTALL_FAILED:$InstallExit" }
```

The ZIP is self-contained; no separate PackageRoot or manual extraction is required. Do not use `-Force`, `-Overwrite`, or manual file copy.

## Execute

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2\RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2.py'
& $PythonExe $Runner --project-root $ProjectRoot --iterations 7
$RunnerExit = $LASTEXITCODE
if ($RunnerExit -ne 0) { throw "OPTION_C_NATIVE_QT_PROBE_V2_BLOCKED:$RunnerExit; preserve the new receipt; do not repeat blindly" }
```

## Required target preflight

- Python 3.13.14 exactly.
- PySide6 6.11.2 and Qt 6.11.2 exactly; no package install/upgrade.
- All active checkout source pins and evidence archives exact.
- A3 proof: 17 literal PASS + 1 validated specialized PASS, exact historical/current whole-manifest pins, and structural one-pointer reconstruction.
- QImage test result 37/37, no skips/errors/failures.
- Seven-iteration synthetic benchmark; P95 must be <=33.333 ms for the 30 FPS stage budget. Preferred threshold <=16.667 ms remains separately reported.

## Expected successful stage status

`OPTION_C_NATIVE_QT_PROBE_STATUS=PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`

The result is not E6 acceptance, end-to-end factory qualification or renderer authorization. Geometry was approved; the SmoothTransformation resampler quality still needs visual approval. The probe uses only synthetic frames and emits preview PNGs plus receipts.

## Failure handling

- Preserve every receipt and log.
- Never retry the same V1/V2 package blindly.
- A3 failure: report `loop_policy_a3_adjudication.error` and its diagnostic values; do not weaken the pointer/manifest checks.
- QImage functional failure: keep test transcript and generated previews; no source update unless the defect is isolated and a new overlay is supplied.
- P95 >33.333 ms: block this backend as the 30 FPS hot path; do not change the threshold.
- Any source pin mismatch: stop before Qt tests; reconcile the exact path/hash.
