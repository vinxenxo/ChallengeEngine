[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [string]$R1PRecoveredZip = ''
)
$ErrorActionPreference = 'Stop'
$scriptStarted = [DateTime]::UtcNow
$runId = 'R1V_WRAPPER_' + $scriptStarted.ToString('yyyyMMdd_HHmmss') + '_' + ([Guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$project = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $project -PathType Container)) { throw ('ProjectRoot missing: ' + $project) }
$receiptRoot = Join-Path $project ('artifacts\tests\c11e\r1v_five_family_qualification_process\' + $runId)
if (Test-Path -LiteralPath $receiptRoot) { throw ('Wrapper receipt collision: ' + $receiptRoot) }
$null = New-Item -ItemType Directory -Path $receiptRoot
$testStdout = Join-Path $receiptRoot 'static_active_tests.stdout.log'
$testStderr = Join-Path $receiptRoot 'static_active_tests.stderr.log'
$runStdout = Join-Path $receiptRoot 'r1v_capture.stdout.log'
$runStderr = Join-Path $receiptRoot 'r1v_capture.stderr.log'
$receiptPath = Join-Path $receiptRoot 'r1v_wrapper_process_receipt.json'
$testExit = $null
$runExit = $null
$py = $null
$status = 'FAIL_R1V_WRAPPER'
$errorText = $null
function Get-Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
try {
    if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -lt 1) {
        throw ('Windows PowerShell 5.1 required; found ' + $PSVersionTable.PSVersion.ToString())
    }
    $project = (Resolve-Path -LiteralPath $project).Path
    if ([string]::IsNullOrWhiteSpace($R1PRecoveredZip)) {
        $R1PRecoveredZip = Join-Path $project 'artifacts\tests\c11e\e4b_r1p\E4B_R1P_20261107_032743_5F75045C_RECOVERED.zip'
    }
    $R1PRecoveredZip = (Resolve-Path -LiteralPath $R1PRecoveredZip).Path
    $pythonTests = Join-Path $project 'tools\c11d\d9\test_c11e_r1v_five_family_qualification.py'
    $pythonRunner = Join-Path $project 'tools\c11d\d9\c11e_r1v_five_family_qualification.py'
    $policy = Join-Path $project 'definitions\c11d\production\C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json'
    $approval = Join-Path $project 'definitions\c11d\production\C11E_D4_8_R1V_OPERATOR_APPROVAL_RECORD_20261107_V1.json'
    foreach ($path in @($pythonTests,$pythonRunner,$policy,$approval)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('Required installed R1V file missing: ' + $path) }
    }
    $py = Get-Command 'py.exe' -ErrorAction Stop
    # Extra apply review: parse this runner with the Windows PowerShell 5.1 AST parser before execution.
    $parseTokens = $null; $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$parseTokens,[ref]$parseErrors) | Out-Null
    if ($parseErrors.Count -gt 0) { throw ('PowerShell AST parse failed: ' + (($parseErrors | ForEach-Object { $_.Message }) -join '; ')) }

    Write-Host '========== C11-E R1V FIVE-FAMILY QUALIFICATION WRAPPER =========='
    Write-Host ('PROJECT_ROOT=' + $project)
    Write-Host ('RUN_ID=' + $runId)
    Write-Host 'STEP=STATIC_AND_ACTIVE_CHECKOUT_TESTS'
    & $py.Source -3.13 $pythonTests --payload-root $project --project-root $project --r1p-archive $R1PRecoveredZip 1> $testStdout 2> $testStderr
    $testExit = $LASTEXITCODE
    if (Test-Path -LiteralPath $testStdout) { Get-Content -LiteralPath $testStdout | ForEach-Object { Write-Host $_ } }
    if (Test-Path -LiteralPath $testStderr) { Get-Content -LiteralPath $testStderr | ForEach-Object { Write-Host $_ } }
    if ($testExit -ne 0) { throw ('Static/active-checkout tests failed with exit code ' + $testExit + '; physical capture not started') }

    Write-Host 'STEP=AUTHORIZED_R1V_CAPTURE_10_LAUNCHERS'
    & $py.Source -3.13 $pythonRunner --project-root $project --r1p-recovered-zip $R1PRecoveredZip --policy $policy --approval-record $approval 1> $runStdout 2> $runStderr
    $runExit = $LASTEXITCODE
    if (Test-Path -LiteralPath $runStdout) { Get-Content -LiteralPath $runStdout | ForEach-Object { Write-Host $_ } }
    if (Test-Path -LiteralPath $runStderr) { Get-Content -LiteralPath $runStderr | ForEach-Object { Write-Host $_ } }
    if ($runExit -ne 0) { throw ('R1V capture helper failed with exit code ' + $runExit) }
    $runText = if (Test-Path -LiteralPath $runStdout) { Get-Content -Raw -LiteralPath $runStdout } else { '' }
    if ($runText -notmatch 'PASS_R1V_FIVE_FAMILY_TECHNICAL_CAPTURE_10_OF_10_PENDING_OPERATOR_VISUAL_REVIEW') {
        throw 'R1V helper exited zero but the required technical PASS marker was not present'
    }
    $status = 'PASS_R1V_WRAPPER_10_OF_10_PENDING_OPERATOR_VISUAL_REVIEW'
}
catch {
    $errorText = $_.Exception.Message
    if ($testExit -eq $null) { $status = 'FAIL_R1V_WRAPPER_PREFLIGHT' }
    elseif ($testExit -ne 0) { $status = 'FAIL_R1V_STATIC_ACTIVE_TESTS' }
    elseif ($runExit -ne $null -and $runExit -ne 0) { $status = 'FAIL_R1V_CAPTURE' }
    elseif ($runExit -eq 0) { $status = 'FAIL_R1V_PASS_MARKER_MISSING' }
    else { $status = 'FAIL_R1V_WRAPPER' }
}
$receipt = [ordered]@{
    schema = 'C11E-R1V-WRAPPER-PROCESS-RECEIPT-V1'
    run_id = $runId
    started_utc = $scriptStarted.ToString('o')
    completed_utc = [DateTime]::UtcNow.ToString('o')
    project_root = $project
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_launcher = $(if ($py) { $py.Source } else { $null })
    python_tests_exit_code = $testExit
    r1v_capture_exit_code = $runExit
    test_stdout_sha256 = Get-Sha256 $testStdout
    test_stderr_sha256 = Get-Sha256 $testStderr
    capture_stdout_sha256 = Get-Sha256 $runStdout
    capture_stderr_sha256 = Get-Sha256 $runStderr
    test_stdout_path = $testStdout
    test_stderr_path = $testStderr
    capture_stdout_path = $runStdout
    capture_stderr_path = $runStderr
    status = $status
    error = $errorText
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $receiptPath -Encoding UTF8
$receiptSha = Get-Sha256 $receiptPath
Write-Host ('WRAPPER_STATUS=' + $status)
Write-Host ('TEST_EXIT_CODE=' + [string]$testExit)
Write-Host ('CAPTURE_EXIT_CODE=' + [string]$runExit)
Write-Host ('WRAPPER_RECEIPT=' + $receiptPath)
Write-Host ('WRAPPER_RECEIPT_SHA256=' + $receiptSha)
if ($status -ne 'PASS_R1V_WRAPPER_10_OF_10_PENDING_OPERATOR_VISUAL_REVIEW') { exit 1 }
exit 0
