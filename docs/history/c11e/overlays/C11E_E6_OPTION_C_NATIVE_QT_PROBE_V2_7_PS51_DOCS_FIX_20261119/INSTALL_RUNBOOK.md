# V2.7 install and execution runbook

## Preconditions

- Use the active checkout at `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` as authority. The uploaded `ChallengeEngineV01_STATELESS-LATEST-20112026.zip` is reference-only and must never be extracted over the checkout.
- Keep the package ZIP outside the checkout; extract only to `%TEMP%\c11e27` after checking all expanded paths.
- Do not rerun V2.1–V2.6 installers/runners or repeat their already completed regression suites.
- Python 3.13.14 and PySide6 6.11.2 must already be installed; do not install or upgrade dependencies.

## Installation

Verify the ZIP SHA sidecar, inspect each archive path length, extract to a fresh short temporary path, then run the contained V2.7 installer. Require Windows PowerShell 5.1 AST PASS, immutable C11-C/D4.8 pins, complete member/hash checks, stage/write/receipt path budgets, full destination preflight, `INSTALL_STATUS=PASS_ADD_ONLY`, `INSTALL_FILES=18/18 VERIFIED`, and `DOCS_FILES=11/11 VERIFIED`.

The 7 code/test files install only under `tools/c11d/d9/c11e_e6_option_c_native_qt_probe_v2_7/`. The 9 overlay history files and 2 current-document updates install under `docs/` in the repository. No document is installed only to Downloads.

## Focused bootstrap regressions

Run once:

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$TestDir = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_7\tests'
& $PythonExe -m unittest discover -s $TestDir -p 'test_qimage_import_bootstrap_v1.py' -v
if ($LASTEXITCODE -ne 0) { throw 'V2_7_IMPORT_BOOTSTRAP_TESTS_BLOCKED' }
```

Expected: 8/8. A zero-test result is a hard failure; do not continue.

## Native Qt/QImage probe

```powershell
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_7\RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_7.py'
& $PythonExe $Runner --project-root $ProjectRoot --iterations 7
if ($LASTEXITCODE -ne 0) { throw 'V2_7_NATIVE_QT_PROBE_BLOCKED; preserve receipt and sidecar' }
```

Require A3 V4 PASS, 23/23 source checks, exact QImage module and test suite source pins, 37/37 target tests, and P95 <= 33.333 ms. The result may be only `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`.

## Visual and next gates

Inspect all three synthetic previews and explicitly accept/decline `SmoothTransformation` quality. The geometry approval remains 720x1280 canvas, 504x896 content at (108,192), black bands and side gutters. Geometry approval does not approve filter quality.

Only after that result, complete read-only source closure for the actual Loop frame/source metadata. A real copied-frame L2 test requires a separately approved D4.8 successor and exact E6 TEST_ONLY execution manifest. Do not run Godot, FFmpeg, FFprobe, audio, mux, renderer, dispatch or Smoke18 media.
