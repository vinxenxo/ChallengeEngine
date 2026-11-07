[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [string]$R1PRecoveredZip = ''
)
$ErrorActionPreference = 'Stop'
$scriptStarted = [DateTime]::UtcNow
$runId = 'R1V_WRAPPER_V3_' + $scriptStarted.ToString('yyyyMMdd_HHmmss') + '_' + ([Guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
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
$pythonExe = $null
$status = 'FAIL_R1V_WRAPPER'
$errorText = $null
function Get-Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Quote-ProcessArgument([string]$Value) {
    # These arguments are paths/flags without embedded quotes. Quoting every token
    # preserves spaces in Windows paths when Start-Process joins ArgumentList.
    return '"' + $Value.Replace('"','\"') + '"'
}
function Resolve-Python313Executable {
    $candidates = New-Object System.Collections.Generic.List[string]
    $knownPaths = @()
    if (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
        $knownPaths += (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe')
    }
    if (-not [string]::IsNullOrWhiteSpace($env:ProgramFiles)) {
        $knownPaths += (Join-Path $env:ProgramFiles 'Python313\python.exe')
    }
    foreach ($known in $knownPaths) {
        if (Test-Path -LiteralPath $known -PathType Leaf) { $candidates.Add((Resolve-Path -LiteralPath $known).Path) }
    }
    $commands = @(Get-Command 'python.exe' -All -ErrorAction SilentlyContinue)
    foreach ($command in $commands) {
        if ($command.CommandType -eq 'Application') {
            $candidate = [string]$command.Source
            if ([string]::IsNullOrWhiteSpace($candidate)) { $candidate = [string]$command.Path }
            if (-not [string]::IsNullOrWhiteSpace($candidate) -and (Test-Path -LiteralPath $candidate -PathType Leaf)) {
                $candidates.Add((Resolve-Path -LiteralPath $candidate).Path)
            }
        }
    }
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($candidate in $candidates) {
        if (-not $seen.Add($candidate)) { continue }
        $probeId = 'C11E_R1V_PY313_PROBE_' + [Guid]::NewGuid().ToString('N')
        $probeOut = Join-Path $env:TEMP ($probeId + '.stdout.log')
        $probeErr = Join-Path $env:TEMP ($probeId + '.stderr.log')
        try {
            $probeCode = 'import sys; print(str(sys.version_info[0]) + "." + str(sys.version_info[1]))'
            $probeArgs = @('-c',$probeCode)
            $probeLine = (@($probeArgs | ForEach-Object { Quote-ProcessArgument ([string]$_) }) -join ' ')
            $probeProcess = Start-Process -FilePath $candidate -ArgumentList $probeLine -PassThru -Wait -NoNewWindow `
                -RedirectStandardOutput $probeOut -RedirectStandardError $probeErr
            $probeVersion = ''
            if (Test-Path -LiteralPath $probeOut -PathType Leaf) { $probeVersion = [System.IO.File]::ReadAllText($probeOut,[System.Text.Encoding]::UTF8).Trim() }
            if ([int]$probeProcess.ExitCode -eq 0 -and $probeVersion -eq '3.13') { return $candidate }
        }
        catch { }
        finally {
            foreach ($probeFile in @($probeOut,$probeErr)) {
                if (Test-Path -LiteralPath $probeFile -PathType Leaf) { Remove-Item -LiteralPath $probeFile -Force }
            }
        }
    }
    throw 'Python 3.13 python.exe not found. Direct executable probing failed; only direct executable probing is supported.'
}
function Invoke-LoggedPython([string]$PythonExe,[string[]]$Arguments,[string]$StdoutPath,[string]$StderrPath) {
    if (Test-Path -LiteralPath $StdoutPath) { throw ('Stdout path collision: ' + $StdoutPath) }
    if (Test-Path -LiteralPath $StderrPath) { throw ('Stderr path collision: ' + $StderrPath) }
    $argumentLine = (@($Arguments | ForEach-Object { Quote-ProcessArgument ([string]$_) }) -join ' ')
    # Direct interpreter process; native streams are redirected to files.
    $process = Start-Process -FilePath $PythonExe -ArgumentList $argumentLine -WorkingDirectory $project `
        -PassThru -Wait -NoNewWindow -RedirectStandardOutput $StdoutPath -RedirectStandardError $StderrPath
    return [int]$process.ExitCode
}
function Write-LogToHost([string]$Path) {
    if (Test-Path -LiteralPath $Path -PathType Leaf) {
        foreach ($line in [System.IO.File]::ReadAllLines($Path,[System.Text.Encoding]::UTF8)) { Write-Host $line }
    }
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
    $pythonTests = Join-Path $project 'tools\c11d\d9\test_c11e_r1v_five_family_qualification_v3.py'
    $pythonRunner = Join-Path $project 'tools\c11d\d9\c11e_r1v_five_family_qualification_v3.py'
    $policy = Join-Path $project 'definitions\c11d\production\C11E_D4_8_R1V_QUALIFICATION_ONLY_POLICY_V2.json'
    $approval = Join-Path $project 'definitions\c11d\production\C11E_D4_8_R1V_OPERATOR_APPROVAL_RECORD_20261107_V1.json'
    foreach ($path in @($pythonTests,$pythonRunner,$policy,$approval)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw ('Required installed R1V V3 file missing: ' + $path) }
    }
    $pythonExe = Resolve-Python313Executable
    $parseTokens = $null; $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$parseTokens,[ref]$parseErrors) | Out-Null
    if ($parseErrors.Count -gt 0) { throw ('PowerShell AST parse failed: ' + (($parseErrors | ForEach-Object { $_.Message }) -join '; ')) }

    Write-Host '========== C11-E R1V FIVE-FAMILY QUALIFICATION WRAPPER V3 =========='
    Write-Host ('PROJECT_ROOT=' + $project)
    Write-Host ('RUN_ID=' + $runId)
    Write-Host 'STEP=STATIC_AND_ACTIVE_CHECKOUT_TESTS'
    $testArgs = @($pythonTests,'--payload-root',$project,'--project-root',$project,'--r1p-archive',$R1PRecoveredZip)
    $testExit = Invoke-LoggedPython -PythonExe $pythonExe -Arguments $testArgs -StdoutPath $testStdout -StderrPath $testStderr
    Write-LogToHost $testStdout
    Write-LogToHost $testStderr
    if ($testExit -ne 0) { throw ('Static/active-checkout tests failed with exit code ' + $testExit + '; physical capture not started') }
    $testText = [System.IO.File]::ReadAllText($testStdout,[System.Text.Encoding]::UTF8)
    if ($testText -notmatch '"tests_run"\s*:\s*32' -or $testText -notmatch 'PASS_R1V_STATIC_AND_ACTIVE_CHECKOUT_TESTS') {
        throw 'Active-checkout test suite did not report the required 32/32 PASS result'
    }

    Write-Host 'STEP=AUTHORIZED_R1V_CAPTURE_10_LAUNCHERS'
    $runArgs = @($pythonRunner,'--project-root',$project,'--r1p-recovered-zip',$R1PRecoveredZip,'--policy',$policy,'--approval-record',$approval)
    $runExit = Invoke-LoggedPython -PythonExe $pythonExe -Arguments $runArgs -StdoutPath $runStdout -StderrPath $runStderr
    Write-LogToHost $runStdout
    Write-LogToHost $runStderr
    if ($runExit -ne 0) { throw ('R1V capture helper failed with exit code ' + $runExit) }
    $runText = [System.IO.File]::ReadAllText($runStdout,[System.Text.Encoding]::UTF8)
    if ($runText -notmatch 'PASS_R1V_FIVE_FAMILY_TECHNICAL_CAPTURE_10_OF_10_PENDING_OPERATOR_VISUAL_REVIEW') {
        throw 'R1V helper exited zero but the required technical PASS marker was not present'
    }
    $status = 'PASS_R1V_WRAPPER_10_OF_10_PENDING_OPERATOR_VISUAL_REVIEW'
}
catch {
    $errorText = $_.Exception.Message
    if ($testExit -eq $null) { $status = 'FAIL_R1V_WRAPPER_PREFLIGHT' }
    elseif ($testExit -ne 0) { $status = 'FAIL_R1V_WRAPPER_STATIC_TESTS' }
    elseif ($runExit -ne $null -and $runExit -ne 0) { $status = 'FAIL_R1V_CAPTURE' }
    elseif ($runExit -eq 0) { $status = 'FAIL_R1V_PASS_MARKER_MISSING' }
    else { $status = 'FAIL_R1V_WRAPPER' }
}
$receipt = [ordered]@{
    schema = 'C11E-R1V-WRAPPER-PROCESS-RECEIPT-V3'
    run_id = $runId
    started_utc = $scriptStarted.ToString('o')
    completed_utc = [DateTime]::UtcNow.ToString('o')
    project_root = $project
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_executable = $pythonExe
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
