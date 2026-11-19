# V2.3 Import-path recovery runbook

## Before installation

The V2.2 installation receipt is preserved at the path reported by the operator. Do not rerun V2.2 and do not delete V2.2 files. This V2.3 overlay is entirely add-only.

Verify the ZIP SHA-256 sidecar before extraction. Extract to a new directory ending `_20261119`; the installer checks its own embedded manifest and SHA pins. Use Windows PowerShell 5.1.

## Installation

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$Downloads = Join-Path $env:USERPROFILE 'Downloads'
$PackageZip = Join-Path $Downloads 'C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_3_IMPORT_PATH_FIX.zip'
$Sidecar = "$PackageZip.sha256"
$PackageRoot = Join-Path $Downloads 'C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_3_IMPORT_PATH_FIX_20261119'
if (Test-Path -LiteralPath $PackageRoot) { throw "USE_FRESH_PACKAGE_DIRECTORY:$PackageRoot" }
$ExpectedSha = ((Get-Content -LiteralPath $Sidecar -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$ActualSha = (Get-FileHash -LiteralPath $PackageZip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualSha -ne $ExpectedSha) { throw "PACKAGE_SHA256_MISMATCH:$ActualSha" }
Expand-Archive -LiteralPath $PackageZip -DestinationPath $PackageRoot
$Installer = Join-Path $PackageRoot 'INSTALL_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_3_IMPORT_PATH_FIX.ps1'
& (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File $Installer -ProjectRoot $ProjectRoot -PackageZip $PackageZip -ExpectedPackageZipSha256 $ExpectedSha
$InstallExit = $LASTEXITCODE
if ($InstallExit -ne 0) { throw "E6_OPTION_C_QT_V2_3_INSTALL_BLOCKED:$InstallExit; preserve output and receipt" }
```

Expected: PowerShell AST PASS, frozen C11-C and D4.8 V2 PASS/UNCHANGED, package manifest members all pass, receipt path budget max 220, `INSTALL_STATUS=PASS_ADD_ONLY`, and 10/10 new destinations verified (or exact identical skips on a repeat).

## Run the V2.3 probe

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_3\RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_3.py'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'V2_3_RUNNER_MISSING_AFTER_INSTALL' }
& $PythonExe $Runner --project-root $ProjectRoot --iterations 7
$RunnerExit = $LASTEXITCODE
if ($RunnerExit -ne 0) { throw "OPTION_C_NATIVE_QT_PROBE_V2_3_BLOCKED:$RunnerExit; preserve receipt and sidecar" }
```

A3 loading should print `A3_ADJUDICATOR_V3_PIN=PASS/PATH_LOADED`; the runner also prints whether the prior V2.2 support module exists with its expected hash. It then performs the same A3 adjudication, QImage 37-test stage and seven-iteration stage benchmark.

Optional isolated loader/A3 regression tests:

```powershell
$env:C11E_PROJECT_ROOT = $ProjectRoot
$PythonExe -m unittest discover -s (Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_3\tests') -p 'test_*.py' -v
$TestExit = $LASTEXITCODE
Remove-Item Env:\C11E_PROJECT_ROOT -ErrorAction SilentlyContinue
if ($TestExit -ne 0) { throw "V2_3_REGRESSION_TESTS_BLOCKED:$TestExit" }
```

Do not infer E6 acceptance, renderer authority, media authorization or release promotion from a QImage-stage PASS.
