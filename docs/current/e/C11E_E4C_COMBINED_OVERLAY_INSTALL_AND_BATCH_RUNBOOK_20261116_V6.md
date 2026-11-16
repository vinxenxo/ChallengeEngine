# E4C Combined Overlay Install + Batch Runbook — V6 (2026-11-16)

## One-command operation

Peripheral Scan is performed through one combined overlay invocation. The installer verifies the package and environment, runs all gates and PREPARE_ONLY checks, commits the exact ADD_ONLY set and immutable install receipt/journal, then starts the installed runner once when `-ExecuteBatch` is supplied. Do not call a separate runner and do not pass BatchId.

```powershell
$ErrorActionPreference = 'Stop'
$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$PythonExe = 'C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe'
$Zip = Join-Path $env:USERPROFILE 'Downloads\C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2_20261116.zip'
$Kit = Join-Path $env:USERPROFILE 'Downloads\C11E_E4C_PERIPHERAL_SCAN_COMBINED_V2_EXTRACT'
$Installer = Join-Path $Kit 'INSTALL_C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2.ps1'
$Expected = ((Get-Content -LiteralPath ($Zip + '.sha256') -Raw -Encoding ASCII).Trim() -split '\s+')[0].ToLowerInvariant()
$Actual = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) { throw "PERIPHERAL_SCAN_PACKAGE_SHA256_FAIL: $Actual" }
if (Test-Path -LiteralPath $Kit) { throw 'PERIPHERAL_SCAN_EXTRACTION_DIR_ALREADY_EXISTS: choose a new folder' }
New-Item -ItemType Directory -Path $Kit | Out-Null
Expand-Archive -LiteralPath $Zip -DestinationPath $Kit -ErrorAction Stop
if (-not (Test-Path -LiteralPath $Installer -PathType Leaf)) { throw "PERIPHERAL_SCAN_INSTALLER_MISSING: $Installer" }
$Tokens = $null; $ParseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($Installer,[ref]$Tokens,[ref]$ParseErrors) | Out-Null
if ($null -ne $ParseErrors -and $ParseErrors.Count -gt 0) {
    $Details = ($ParseErrors | ForEach-Object { $_.Message + ' @ ' + $_.Extent.StartLineNumber }) -join '; '
    throw "PERIPHERAL_SCAN_INSTALLER_AST_FAIL: $Details"
}
Write-Host 'PERIPHERAL_SCAN_INSTALLER_AST=PASS'
& (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File $Installer -PackageZip $Zip -ProjectRoot $ProjectRoot -PythonExe $PythonExe -ExecuteBatch
$InstallerExit = $LASTEXITCODE
if ($InstallerExit -ne 0) { throw "PERIPHERAL_SCAN_COMBINED_EXIT=$InstallerExit; preserve evidence; do not rerun automatically" }
```

## Expected gates and receipts

PowerShell AST/ASCII 4/4; Python 51/51; atomic I/O 7/7; source pins 38/38 pre/pre-transaction/post; frozen C11-C manifest exact; staged/installed PREPARE_ONLY; 21/21 ADD_ONLY; immutable `INSTALL_RECEIPT.json` and `INSTALL_TRANSACTION_JOURNAL.json`; five technical PASS rows; `BATCH_LAUNCH_RECEIPT.json`; acyclic `COMBINED_EXECUTION_RECEIPT.json`.

Install evidence: `artifacts/tests/c11e/e4c_peripheral_scan_combined_overlay_v2/<run-id>/`. Family batch evidence: `artifacts/tests/c11e/e4c_peripheral_scan_tier_batch/<batch-id>/`.

## Failure policy

Before commit, preserve installation journal/failure receipt and establish whether any ADD began. After install commit, installation remains committed even if the batch fails. `BATCH_LAUNCH_FAILURE.json` records BatchId/lock/logs when available, with `rerun_allowed=false`. A reserved BatchId is permanently consumed. Never rerun automatically.

## Governance

C11-C immutable; E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; production dispatch false; release authority none; Git checks skipped; commits operator-managed.
