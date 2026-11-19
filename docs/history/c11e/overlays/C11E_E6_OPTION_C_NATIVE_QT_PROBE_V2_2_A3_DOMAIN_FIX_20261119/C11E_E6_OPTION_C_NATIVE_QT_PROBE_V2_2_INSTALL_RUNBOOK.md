# V2.2 A3 domain fix — install and run

## 1. Package verification and install

Extract this package outside the checkout, in a fresh Downloads directory. Do not extract any package over the working tree. The installer is Windows PowerShell 5.1, verifies its own SHA-256, package ZIP SHA-256, every ZIP member against `PACKAGE_MANIFEST_V2.json`, the frozen C11-C manifest and D4.8 V2, then runs a complete destination collision preflight. It is add-only; existing byte-identical destinations are skipped and a mismatch blocks before any destination write.

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$Downloads = Join-Path $env:USERPROFILE 'Downloads'
$PackageZip = Join-Path $Downloads 'C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_2_A3_DOMAIN_FIX.zip'
$Sidecar = "$PackageZip.sha256"
$PackageRoot = Join-Path $Downloads 'C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_2_A3_DOMAIN_FIX_20261119'

if (Test-Path -LiteralPath $PackageRoot) { throw "USE_FRESH_PACKAGE_DIRECTORY:$PackageRoot" }
$ExpectedSha = ((Get-Content -LiteralPath $Sidecar -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$ActualSha = (Get-FileHash -LiteralPath $PackageZip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualSha -ne $ExpectedSha) { throw "PACKAGE_SHA256_MISMATCH:$ActualSha" }
Expand-Archive -LiteralPath $PackageZip -DestinationPath $PackageRoot
$Installer = Join-Path $PackageRoot 'INSTALL_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_2_A3_DOMAIN_FIX.ps1'
& (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File $Installer `
    -ProjectRoot $ProjectRoot -PackageZip $PackageZip -ExpectedPackageZipSha256 $ExpectedSha
$InstallExit = $LASTEXITCODE
if ($InstallExit -ne 0) { throw "E6_OPTION_C_QT_V2_2_INSTALL_BLOCKED:$InstallExit; preserve output and receipt" }
```

Expected installer signals include `POWERSHELL_5_1_AST_PARSE=PASS/INSTALLER`, the exact C11-C and D4.8 pins, all package members PASS, receipt-path budget PASS, full preflight PASS and `INSTALL_STATUS=PASS_ADD_ONLY`. There are only new V2.2 runner/support/test and documentation destinations. Do not clean or overwrite V2/V2.1 files.

## 2. Run the V2.2 synthetic probe

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_2\RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_2.py'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'V2_2_RUNNER_MISSING_AFTER_INSTALL' }
& $PythonExe $Runner --project-root $ProjectRoot --iterations 7
$RunnerExit = $LASTEXITCODE
if ($RunnerExit -ne 0) { throw "OPTION_C_NATIVE_QT_PROBE_V2_2_BLOCKED:$RunnerExit; preserve receipt and sidecar" }
```

The runner locates the existing V2 payload at its pinned V2 path; it does not copy or replace that payload. It uses a new V2.2 output root. It checks the new V3 adjudicator's SHA before loading it.

The installed A3 regression suite is also runnable on demand; it copies all pinned source documents to a temporary scratch directory and does not modify the checkout:

```powershell
$env:C11E_PROJECT_ROOT = $ProjectRoot
$TestDir = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_2\tests'
& $PythonExe -m unittest discover -s $TestDir -p 'test_a3_lineage_adjudicator_v3.py' -v
$TestExit = $LASTEXITCODE
Remove-Item Env:\C11E_PROJECT_ROOT -ErrorAction SilentlyContinue
if ($TestExit -ne 0) { throw "A3_V3_REGRESSION_TESTS_BLOCKED:$TestExit" }
```

## 3. Required adjudication and test outcomes

A3 must report `PASS_SPECIALIZED_A3_PASS_CLASSIFIED`, normalized 18/18, and exact one-pointer reconstruction. QImage test output should then report 37 tests. The benchmark runs seven iterations. Runtime timing is user-machine evidence and must not be pre-judged by package-build tests.

A green full runner status is still only `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`. Do not infer end-to-end performance or renderer admission. Preserve the complete receipt, sidecar, unit test log and three PNG previews, whether PASS or BLOCKED.
