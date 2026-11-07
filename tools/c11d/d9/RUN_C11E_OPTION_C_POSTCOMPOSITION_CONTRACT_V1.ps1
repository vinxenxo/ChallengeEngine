[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$ProjectRoot
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function ConvertTo-ProcessArgument {
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Value)
    return '"' + $Value.Replace('"', '\"') + '"'
}

function Write-Utf8Json {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)]$Value
    )
    $json = ConvertTo-Json -InputObject $Value -Depth 40
    [System.IO.File]::WriteAllText($Path, ($json + [Environment]::NewLine), (New-Object System.Text.UTF8Encoding($false)))
}

$ResolvedRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $ResolvedRoot -PathType Container)) {
    throw "PROJECT_ROOT_NOT_FOUND=$ResolvedRoot"
}

$FrozenManifest = Join-Path $ResolvedRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$StaticAudit = Join-Path $ResolvedRoot 'tools\c11d\d9\test_c11e_e4b_r1p_family_grammar_static_audit.py'
$RecoveredZip = Join-Path $ResolvedRoot 'artifacts\tests\c11e\e4b_r1p\E4B_R1P_20261107_032743_5F75045C_RECOVERED.zip'
$ContractScript = Join-Path $ResolvedRoot 'tools\c11d\d9\c11e_option_c_postcomposition_contract.py'
$TestScript = Join-Path $ResolvedRoot 'tools\c11d\d9\test_c11e_option_c_postcomposition_contract.py'

$ExpectedFrozenManifest = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ExpectedStaticAudit = '600c22dafe2e377cb02b4a69f8823a44745d705b71cdb0d6bcec38da52df3e92'
$ExpectedRecoveredZip = 'd49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52'

foreach ($Required in @($FrozenManifest, $StaticAudit, $RecoveredZip, $ContractScript, $TestScript)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "REQUIRED_FILE_MISSING=$Required"
    }
}

$FrozenActual = Get-Sha256Lower -Path $FrozenManifest
if ($FrozenActual -ne $ExpectedFrozenManifest) {
    throw "FROZEN_C11C_MANIFEST_MISMATCH=$FrozenActual"
}
$StaticActual = Get-Sha256Lower -Path $StaticAudit
if ($StaticActual -ne $ExpectedStaticAudit) {
    throw "ACCEPTED_STATIC_AUDIT_PIN_MISMATCH=$StaticActual"
}
$ArchiveActual = Get-Sha256Lower -Path $RecoveredZip
if ($ArchiveActual -ne $ExpectedRecoveredZip) {
    throw "RECOVERED_R1P_ARCHIVE_PIN_MISMATCH=$ArchiveActual"
}

$PythonCommand = Get-Command 'py.exe' -ErrorAction SilentlyContinue
if ($null -eq $PythonCommand) {
    $PythonCommand = Get-Command 'py' -ErrorAction SilentlyContinue
}
if ($null -eq $PythonCommand) {
    throw 'PYTHON_LAUNCHER_NOT_FOUND'
}
$PythonPath = $PythonCommand.Source
if ([string]::IsNullOrWhiteSpace($PythonPath)) { $PythonPath = $PythonCommand.Definition }

$RunStamp = Get-Date -Format 'yyyyMMdd_HHmmss_ffff'
$RunSuffix = ([Guid]::NewGuid().ToString('N')).Substring(0, 8).ToUpperInvariant()
$RunId = 'OPTION_C_CONTRACT_{0}_{1}' -f $RunStamp, $RunSuffix
$RunBase = Join-Path $ResolvedRoot 'artifacts\tests\c11e\option_c_postcomposition_contract'
if (-not (Test-Path -LiteralPath $RunBase -PathType Container)) {
    [void](New-Item -ItemType Directory -Path $RunBase -Force)
}
$RunRoot = Join-Path $RunBase $RunId
if (Test-Path -LiteralPath $RunRoot) {
    throw "RUN_ROOT_COLLISION=$RunRoot"
}
[void](New-Item -ItemType Directory -Path $RunRoot -Force:$false)

$TestsStdout = Join-Path $RunRoot 'unit_tests.stdout.log'
$TestsStderr = Join-Path $RunRoot 'unit_tests.stderr.log'
$MainStdout = Join-Path $RunRoot 'contract.stdout.log'
$MainStderr = Join-Path $RunRoot 'contract.stderr.log'
$ReportPath = Join-Path $RunRoot 'option_c_contract_report.json'
$ProcessReceiptPath = Join-Path $RunRoot 'option_c_contract_process_receipt.json'
$TestExit = -1
$MainExit = -1
$StartedUtc = [DateTime]::UtcNow.ToString('o')
$Processes = @()

try {
    Write-Host '========== C11-E OPTION C POSTCOMPOSITION CONTRACT V1 =========='
    Write-Host ('PROJECT_ROOT=' + $ResolvedRoot)
    Write-Host ('RUN_ID=' + $RunId)
    Write-Host 'SCOPE=STATIC_AND_NEGATIVE_CONTRACT_VALIDATION_ONLY; NO_RENDER_NO_MEDIA'

    $TestArgumentValues = @(
        '-3.13',
        (ConvertTo-ProcessArgument -Value $TestScript),
        '--project-root', (ConvertTo-ProcessArgument -Value $ResolvedRoot),
        '--r1p-zip', (ConvertTo-ProcessArgument -Value $RecoveredZip)
    )
    $TestArguments = [string]::Join(' ', $TestArgumentValues)
    $TestProcess = Start-Process -FilePath $PythonPath -ArgumentList $TestArguments -WorkingDirectory $ResolvedRoot -Wait -PassThru -NoNewWindow -RedirectStandardOutput $TestsStdout -RedirectStandardError $TestsStderr
    $TestExit = [int]$TestProcess.ExitCode
    $Processes += [pscustomobject]@{
        name = 'OPTION_C_UNIT_TESTS'
        executable = $PythonPath
        arguments = $TestArguments
        exit_code = $TestExit
        stdout_path = $TestsStdout
        stdout_sha256 = (Get-Sha256Lower -Path $TestsStdout)
        stderr_path = $TestsStderr
        stderr_sha256 = (Get-Sha256Lower -Path $TestsStderr)
    }
    if ($TestExit -ne 0) {
        throw "OPTION_C_UNIT_TESTS_FAILED_EXIT=$TestExit"
    }
    $TestOutputText = Get-Content -LiteralPath $TestsStdout -Raw
    if ($TestOutputText -notmatch 'OPTION_C_UNIT_TESTS=9/9') {
        throw 'OPTION_C_UNIT_TEST_SUMMARY_MISSING_OR_NOT_9_OF_9'
    }

    $MainArgumentValues = @(
        '-3.13',
        (ConvertTo-ProcessArgument -Value $ContractScript),
        '--project-root', (ConvertTo-ProcessArgument -Value $ResolvedRoot),
        '--r1p-zip', (ConvertTo-ProcessArgument -Value $RecoveredZip),
        '--report-out', (ConvertTo-ProcessArgument -Value $ReportPath)
    )
    $MainArguments = [string]::Join(' ', $MainArgumentValues)
    $MainProcess = Start-Process -FilePath $PythonPath -ArgumentList $MainArguments -WorkingDirectory $ResolvedRoot -Wait -PassThru -NoNewWindow -RedirectStandardOutput $MainStdout -RedirectStandardError $MainStderr
    $MainExit = [int]$MainProcess.ExitCode
    $Processes += [pscustomobject]@{
        name = 'OPTION_C_CONTRACT_VALIDATION'
        executable = $PythonPath
        arguments = $MainArguments
        exit_code = $MainExit
        stdout_path = $MainStdout
        stdout_sha256 = (Get-Sha256Lower -Path $MainStdout)
        stderr_path = $MainStderr
        stderr_sha256 = (Get-Sha256Lower -Path $MainStderr)
    }
    if ($MainExit -ne 0) {
        throw "OPTION_C_CONTRACT_VALIDATION_FAILED_EXIT=$MainExit"
    }
    if (-not (Test-Path -LiteralPath $ReportPath -PathType Leaf)) {
        throw 'OPTION_C_REPORT_NOT_CREATED'
    }
    $Report = Get-Content -LiteralPath $ReportPath -Raw | ConvertFrom-Json
    if ($Report.status -ne 'PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY') {
        throw "OPTION_C_REPORT_STATUS_INVALID=$($Report.status)"
    }
    if ($Report.r1p.receipt_count -ne 27 -or $Report.option_c_handoff.handoff_count -ne 27) {
        throw 'OPTION_C_REPORT_27_OF_27_ASSERTION_FAILED'
    }
    if ($Report.governance.renderer -ne 'OFF' -or $Report.governance.media_created -ne $false -or $Report.governance.release_authority -ne 'NONE') {
        throw 'OPTION_C_GOVERNANCE_LOCK_ASSERTION_FAILED'
    }

    $ProcessReceipt = [ordered]@{
        schema = 'C11E-E-OPTION-C-POSTCOMPOSITION-PROCESS-RECEIPT-V1'
        run_id = $RunId
        started_utc = $StartedUtc
        completed_utc = [DateTime]::UtcNow.ToString('o')
        project_root = $ResolvedRoot
        recovered_r1p_zip = $RecoveredZip
        recovered_r1p_zip_sha256 = $ArchiveActual
        frozen_c11c_manifest_sha256 = $FrozenActual
        accepted_static_audit_sha256 = $StaticActual
        python_launcher = $PythonPath
        python_version_requested = '3.13'
        process_count = $Processes.Count
        processes = $Processes
        report_path = $ReportPath
        report_sha256 = (Get-Sha256Lower -Path $ReportPath)
        governance = [ordered]@{
            renderer = 'OFF'
            d4_8 = 'BLOCKED'
            d9_10 = 'PREPARE_ONLY'
            d9_14 = 'BLOCKED'
            d9_16 = 'BLOCKED'
            d9_17 = 'BLOCKED_NO_GO'
            d10 = 'BLOCKED_FOR_PROMOTION'
            release_authority = 'NONE'
            launcher_invoked = $false
            godot_invoked = $false
            ffprobe_invoked = $false
            ffmpeg_invoked = $false
            compositor_invoked = $false
            d3_audio_invoked = $false
            mux_invoked = $false
            media_created = $false
            c11c_source_mutation = $false
        }
        overall_status = 'PASS_OPTION_C_HANDOFF_CONTRACT_27_OF_27_PREPARE_ONLY'
    }
    Write-Utf8Json -Path $ProcessReceiptPath -Value $ProcessReceipt
    $ReceiptSha = Get-Sha256Lower -Path $ProcessReceiptPath

    Write-Host ('UNIT_TESTS_EXIT_CODE=' + $TestExit)
    Write-Host ('CONTRACT_EXIT_CODE=' + $MainExit)
    Write-Host ('OPTION_C_STATUS=' + $Report.status)
    Write-Host ('R1P_RECEIPTS=' + $Report.r1p.receipt_count + '/27')
    Write-Host ('OPTION_C_HANDOFFS=' + $Report.option_c_handoff.handoff_count + '/27')
    Write-Host ('R1P_SOURCE_PINS=' + $Report.r1p.r1p_source_pin_count + '/30')
    Write-Host ('R1P_PROCESS_LOGS=' + $Report.r1p.r1p_process_log_validation_count + '/4')
    Write-Host ('OPTION_C_POLICY_PINS=' + $Report.r1p.option_c_policy_pin_validation_count + '/3')
    Write-Host ('TOTAL_LIVE_PIN_VALIDATIONS=' + $Report.r1p.total_live_pin_validations + '/33')
    Write-Host ('R1V_QUALIFICATION_POLICY=' + $Report.r1v_qualification_request.status)
    Write-Host ('R1V_EXECUTION_AUTHORIZED=' + $Report.r1v_qualification_request.execution_authorized.ToString().ToUpperInvariant())
    Write-Host 'RENDERER=OFF'
    Write-Host 'MEDIA_CREATED=false'
    Write-Host 'RELEASE_AUTHORITY=NONE'
    Write-Host ('REPORT=' + $ReportPath)
    Write-Host ('REPORT_SHA256=' + (Get-Sha256Lower -Path $ReportPath))
    Write-Host ('PROCESS_RECEIPT=' + $ProcessReceiptPath)
    Write-Host ('PROCESS_RECEIPT_SHA256=' + $ReceiptSha)
}
catch {
    $FailureMessage = $_.Exception.Message
    $FailureReceipt = [ordered]@{
        schema = 'C11E-E-OPTION-C-POSTCOMPOSITION-PROCESS-RECEIPT-V1'
        run_id = $RunId
        started_utc = $StartedUtc
        completed_utc = [DateTime]::UtcNow.ToString('o')
        project_root = $ResolvedRoot
        recovered_r1p_zip = $RecoveredZip
        recovered_r1p_zip_sha256 = $ArchiveActual
        frozen_c11c_manifest_sha256 = $FrozenActual
        accepted_static_audit_sha256 = $StaticActual
        python_launcher = $PythonPath
        processes = $Processes
        report_path = $ReportPath
        report_sha256 = $(if (Test-Path -LiteralPath $ReportPath -PathType Leaf) { Get-Sha256Lower -Path $ReportPath } else { $null })
        failure = $FailureMessage
        governance = [ordered]@{
            renderer = 'OFF'; d4_8 = 'BLOCKED'; d9_10 = 'PREPARE_ONLY';
            release_authority = 'NONE'; launcher_invoked = $false; godot_invoked = $false;
            ffprobe_invoked = $false; ffmpeg_invoked = $false; compositor_invoked = $false;
            d3_audio_invoked = $false; mux_invoked = $false; media_created = $false; c11c_source_mutation = $false
        }
        overall_status = 'FAIL_OPTION_C_HANDOFF_CONTRACT'
    }
    if (-not (Test-Path -LiteralPath $ProcessReceiptPath)) {
        Write-Utf8Json -Path $ProcessReceiptPath -Value $FailureReceipt
    }
    Write-Host ("OPTION_C_STATUS=FAIL: " + $FailureMessage) -ForegroundColor Red
    exit 2
}
