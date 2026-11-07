[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$RunId = 'E4B_R1P_20261107_032743_5F75045C'
)

$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) {
    throw "Windows PowerShell 5.1 is required. Current version: $($PSVersionTable.PSVersion)"
}
if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
}
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "ProjectRoot is not a directory: $ProjectRoot" }
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
if ($RunId -notmatch '^E4B_R1P_[A-Z0-9_]+$') { throw "Invalid R1P RunId: $RunId" }

$PythonScript = Join-Path $PSScriptRoot 'verify_c11e_e4b_r1p_existing_run_v1.py'
if (-not (Test-Path -LiteralPath $PythonScript -PathType Leaf)) { throw "R1P recovery verifier missing: $PythonScript" }
$PythonCommand = Get-Command py.exe -ErrorAction SilentlyContinue | Select-Object -First 1
if ($null -eq $PythonCommand) { throw 'Python launcher py.exe was not found. Python 3.13 is required.' }

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$CaptureRoot = Join-Path $ProjectRoot 'artifacts\tests\c11e\e4b_r1p_recovery_process'
if (-not (Test-Path -LiteralPath $CaptureRoot -PathType Container)) { New-Item -ItemType Directory -Path $CaptureRoot -Force | Out-Null }
$CaptureId = 'R1P_RECOVERY_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '_' + [Guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant()
$CaptureDir = Join-Path $CaptureRoot $CaptureId
if (Test-Path -LiteralPath $CaptureDir) { throw "Recovery process capture collision: $CaptureDir" }
New-Item -ItemType Directory -Path $CaptureDir | Out-Null
$StdOut = Join-Path $CaptureDir 'python.stdout.log'
$StdErr = Join-Path $CaptureDir 'python.stderr.log'
$ProcessReceipt = Join-Path $CaptureDir 'recovery_process_receipt.json'
$ProcessSidecar = Join-Path $CaptureDir 'recovery_process_receipt.sha256'
$ArgumentLine = '-3.13 -B "' + $PythonScript + '" --project-root "' + $ProjectRoot + '" --run-id "' + $RunId + '"'

Write-Host '========== C11-E E4B R1P EXISTING-RUN RECOVERY V1 =========='
Write-Host "PROJECT_ROOT=$ProjectRoot"
Write-Host "RUN_ID=$RunId"
Write-Host 'MODE=VERIFY_EXISTING_OUTPUT_AND_REPACKAGE_ONLY; NO_GODOT_RERUN'

$Process = Start-Process -FilePath $PythonCommand.Source -ArgumentList $ArgumentLine -WorkingDirectory $ProjectRoot -Wait -PassThru -NoNewWindow -RedirectStandardOutput $StdOut -RedirectStandardError $StdErr
if (-not (Test-Path -LiteralPath $StdOut)) { [System.IO.File]::WriteAllText($StdOut, '', (New-Object System.Text.UTF8Encoding($false))) }
if (-not (Test-Path -LiteralPath $StdErr)) { [System.IO.File]::WriteAllText($StdErr, '', (New-Object System.Text.UTF8Encoding($false))) }
$StdOutHash = Get-Sha256 $StdOut
$StdErrHash = Get-Sha256 $StdErr
$ScriptHash = Get-Sha256 $PythonScript
$StdOutText = Get-Content -LiteralPath $StdOut -Raw
$StdErrText = Get-Content -LiteralPath $StdErr -Raw
$Result = $null
if ($Process.ExitCode -eq 0) {
    try { $Result = $StdOutText | ConvertFrom-Json } catch { throw "Recovery verifier returned non-JSON stdout. Capture: $CaptureDir" }
}

$RecoveryStatus = 'NOT_AVAILABLE'
$RecoveredZipPath = ''
$RecoveredZipHash = ''
if ($null -ne $Result) {
    $RecoveryStatus = [string]$Result.status
    $RecoveredZipPath = [string]$Result.recovered_zip
    $RecoveredZipHash = [string]$Result.recovered_zip_sha256
}
$Receipt = [ordered]@{
    schema = 'C11E-E4B-R1P-ARCHIVE-RECOVERY-PROCESS-RECEIPT-V1'
    capture_id = $CaptureId
    run_id = $RunId
    powershell_version = [string]$PSVersionTable.PSVersion
    python_launcher = $PythonCommand.Source
    python_arguments = $ArgumentLine
    verifier_path = $PythonScript
    verifier_sha256 = $ScriptHash
    exit_code = [int]$Process.ExitCode
    stdout_path = $StdOut
    stderr_path = $StdErr
    stdout_sha256 = $StdOutHash
    stderr_sha256 = $StdErrHash
    recovery_status = $RecoveryStatus
    recovered_zip_path = $RecoveredZipPath
    recovered_zip_sha256 = $RecoveredZipHash
    checkout_source_files_modified = $false
    renderer_or_media_invoked = $false
    godot_reinvoked = $false
}
$ReceiptJson = $Receipt | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($ProcessReceipt, $ReceiptJson + "`n", (New-Object System.Text.UTF8Encoding($false)))
$ReceiptHash = Get-Sha256 $ProcessReceipt
[System.IO.File]::WriteAllText($ProcessSidecar, ($ReceiptHash + '  recovery_process_receipt.json' + "`n"), [System.Text.Encoding]::ASCII)

Write-Host "PROCESS_EXIT_CODE=$($Process.ExitCode)"
Write-Host "VERIFIER_SHA256=$ScriptHash"
Write-Host "STDOUT_SHA256=$StdOutHash"
Write-Host "STDERR_SHA256=$StdErrHash"
Write-Host "PROCESS_RECEIPT=$ProcessReceipt"
Write-Host "PROCESS_RECEIPT_SHA256=$ReceiptHash"
if (-not [string]::IsNullOrWhiteSpace($StdOutText)) { Write-Host $StdOutText.Trim() }
if (-not [string]::IsNullOrWhiteSpace($StdErrText)) { Write-Host $StdErrText.Trim() }
if ($Process.ExitCode -ne 0) { throw "R1P archive recovery failed with exit $($Process.ExitCode). Captures retained at $CaptureDir" }
if ($null -eq $Result -or $Result.status -ne 'PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27') {
    throw "R1P archive recovery did not return its exact PASS status. Captures retained at $CaptureDir"
}
Write-Host 'RECOVERY_STATUS=PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27'
Write-Host "RECOVERED_ZIP=$($Result.recovered_zip)"
Write-Host "RECOVERED_ZIP_SHA256=$($Result.recovered_zip_sha256)"
Write-Host "RECOVERY_REPORT=$($Result.recovery_report)"
Write-Host "RECOVERY_REPORT_SHA256=$($Result.recovery_report_sha256)"
