# V2.4 installation and execution runbook

## Preserve preceding evidence

Keep the V2.1, V2.2 and V2.3 install/run receipts and sidecars. Do not rerun any prior runner. This package adds a new namespace and a new evidence root; it does not replace old files.

## Download and install (Windows PowerShell 5.1)

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$Downloads = Join-Path $env:USERPROFILE 'Downloads'
$PackageZip = Join-Path $Downloads 'C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4_A3_LEGACY_FIELD_CONTRACT_FIX.zip'
$Sidecar = "$PackageZip.sha256"
$PackageRoot = Join-Path $Downloads 'C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4_A3_LEGACY_FIELD_CONTRACT_FIX_20261119'
if (Test-Path -LiteralPath $PackageRoot) { throw "USE_FRESH_PACKAGE_DIRECTORY:$PackageRoot" }
$ExpectedSha = ((Get-Content -LiteralPath $Sidecar -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
$ActualSha = (Get-FileHash -LiteralPath $PackageZip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualSha -ne $ExpectedSha) { throw "PACKAGE_SHA256_MISMATCH:$ActualSha" }
Expand-Archive -LiteralPath $PackageZip -DestinationPath $PackageRoot
$Installer = Join-Path $PackageRoot 'INSTALL_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4_A3_LEGACY_FIELD_CONTRACT_FIX.ps1'
& (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File $Installer -ProjectRoot $ProjectRoot -PackageZip $PackageZip -ExpectedPackageZipSha256 $ExpectedSha
$InstallExit = $LASTEXITCODE
if ($InstallExit -ne 0) { throw "E6_OPTION_C_QT_V2_4_INSTALL_BLOCKED:$InstallExit; preserve output and receipt" }
```

Expected: `POWERSHELL_5_1_AST_PARSE=PASS/INSTALLER`, frozen manifest and D4.8 V2 unchanged, all package members pass, `INSTALL_STATUS=PASS_ADD_ONLY`, all 11 new destination files verified (ADD/SKIP counts are computed from the active checkout).

## Focused regression tests and native Qt probe

```powershell
$PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$TestDir = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_4\tests'
$PreviousProjectRoot = $env:C11E_PROJECT_ROOT
try {
    $env:C11E_PROJECT_ROOT = $ProjectRoot
    & $PythonExe -m unittest discover -s $TestDir -p 'test_*.py' -v
    $TestExit = $LASTEXITCODE
}
finally {
    if ($null -eq $PreviousProjectRoot) { Remove-Item Env:\C11E_PROJECT_ROOT -ErrorAction SilentlyContinue }
    else { $env:C11E_PROJECT_ROOT = $PreviousProjectRoot }
}
if ($TestExit -ne 0) { throw "V2_4_REGRESSION_TESTS_BLOCKED:$TestExit" }
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_option_c_native_qt_probe_v2_4\RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2_4.py'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'V2_4_RUNNER_MISSING_AFTER_INSTALL' }
& $PythonExe $Runner --project-root $ProjectRoot --iterations 7
$RunnerExit = $LASTEXITCODE
if ($RunnerExit -ne 0) { throw "OPTION_C_NATIVE_QT_PROBE_V2_4_BLOCKED:$RunnerExit; preserve receipt and sidecar" }
```

The new focused suite has 17 tests. The runner will only proceed to the existing 37 QImage tests and seven benchmark iterations after all A3, source-pin, evidence and Python/PySide6 preflights pass.

## Decision boundary

A passing QImage stage remains synthetic-only and explicitly not end-to-end. It does not authorize renderer activation, Godot, FFmpeg, FFprobe, audio, mux, production dispatch, E6 acceptance or release. Preserve all receipts/sidecars and the full console transcript.
