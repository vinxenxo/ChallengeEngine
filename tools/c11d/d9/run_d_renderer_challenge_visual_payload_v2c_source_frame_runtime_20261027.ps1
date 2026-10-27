# C11-D Phase N: source-frame runtime receipts. Windows PowerShell 5.1.
# Run only from the active checkout root. Do not generate payload/media/render output.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$OldPyNoBytecode = $env:PYTHONDONTWRITEBYTECODE
$env:PYTHONDONTWRITEBYTECODE = '1'
try {

$ExpectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..')).TrimEnd('\')
$Current = [IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\')
if (-not [string]::Equals($Root, $ExpectedRoot, [StringComparison]::OrdinalIgnoreCase) -or
    -not [string]::Equals($Current, $ExpectedRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Run this launcher from the exact active checkout root: $ExpectedRoot"
}

function Get-FileSha256([string]$Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Write-Utf8NoBom([string]$Path, [string]$Text) {
    [IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false)))
}
function Invoke-CapturedProcess([string]$FilePath, [string]$ArgumentLine, [string]$WorkingDirectory, [string]$StdoutPath, [string]$StderrPath) {
    $Process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentLine -WorkingDirectory $WorkingDirectory -PassThru -Wait -RedirectStandardOutput $StdoutPath -RedirectStandardError $StderrPath
    return $Process.ExitCode
}
function Get-Text([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing captured file: $Path" }
    [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
}

$FrozenManifestPath = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$FrozenManifestSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$FrozenManifestBytes = 796318
$ContractRel = 'definitions\c11d\production\D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json'
$ContractSha = '6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c'
$RunnerRel = 'tools\c11d\d9\d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py'
$RunnerSha = 'a4f5aab8febfb49ec25a97d12f4604137dcbf1c63049a50b0fafe5c0c0c5cdcf'
$HarnessRel = 'tools\c11d\d9\challenge_visual_payload_v2c_source_frame_runtime_in_memory.gd'
$HarnessSha = 'ba8500c1db0b86539953c667bc1c48bc765e960f765f7ecef935ff4d206e2a9d'
$TestRel = 'tools\c11d\d9\test_d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py'
$TestSha = 'f8cb0717f9f90b46071dcbf292a4c308e3dac04b4090a3fd4a0ea53bf627ebfb'
$CheckpointRel = 'docs\current\d\D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md'
$CheckpointSha = '2d603f916af7a42a404cd701a3bc3c6967b28f75583ab0f8326a3c33e30ef30f'
$LedgerRel = 'docs\current\d\C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md'
$LedgerSha = '4858b05af9be26d5dbfac0e3ac3b8a4e7c2f2eb30a36674e3216423c2ee350b9'
$ExpectedV2BReportSha = '6e19e88bcce6249f613c7e8566b92f78497c4749bfd079dda2b01e20385072a0'
$ExpectedStaticReceiptSha = 'aa8cebd453b632e445becb936ff3520110d5f80fdf2a732818a6917885595e32'
$StaticMarkerPath = Join-Path $env:TEMP 'C11D_PHASE_KL_V2B_STATIC_GATE_20261027.completed.json'
$V2BCompletionPath = Join-Path $env:TEMP 'C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027.completed.json'
$AttemptMarkerPath = Join-Path $env:TEMP 'C11D_V2C_SOURCE_FRAME_RUNTIME_20261027.started.json'
$CompletionMarkerPath = Join-Path $env:TEMP 'C11D_V2C_SOURCE_FRAME_RUNTIME_20261027.completed.json'

if (Test-Path -LiteralPath $AttemptMarkerPath) { throw "V2-C runtime attempt already exists. Preserve evidence; do not rerun: $AttemptMarkerPath" }
if (Test-Path -LiteralPath $CompletionMarkerPath) { throw "V2-C source-frame runtime gate already completed: $CompletionMarkerPath" }
if (-not (Test-Path -LiteralPath $FrozenManifestPath -PathType Leaf) -or (Get-Item -LiteralPath $FrozenManifestPath).Length -ne $FrozenManifestBytes -or (Get-FileSha256 $FrozenManifestPath) -ne $FrozenManifestSha) { throw 'Frozen C11-C manifest hash/size mismatch.' }
foreach ($Pin in @(
    @{ Path=$ContractRel; Sha=$ContractSha },
    @{ Path=$RunnerRel; Sha=$RunnerSha },
    @{ Path=$HarnessRel; Sha=$HarnessSha },
    @{ Path=$TestRel; Sha=$TestSha },
    @{ Path=$CheckpointRel; Sha=$CheckpointSha },
    @{ Path=$LedgerRel; Sha=$LedgerSha }
)) {
    $Path = Join-Path $Root $Pin.Path
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf) -or (Get-FileSha256 $Path) -ne $Pin.Sha) { throw "Source/precondition SHA mismatch: $($Pin.Path)" }
}

if (-not (Test-Path -LiteralPath $StaticMarkerPath -PathType Leaf)) { throw 'Accepted Phase L static marker missing.' }
$StaticMarker = Get-Content -LiteralPath $StaticMarkerPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$StaticMarker.schema -ne 'C11D-PHASE-KL-V2B-STATIC-GATE-COMPLETION-V1' -or
    [string]$StaticMarker.V2B_static_tests -ne 'PASS_198_OF_198' -or
    [string]$StaticMarker.source_pins -ne '81/81' -or
    [string]$StaticMarker.authority_input_pins -ne '9/9' -or
    [string]$StaticMarker.static_receipt_sha256 -ne $ExpectedStaticReceiptSha) { throw 'Accepted Phase L marker fields mismatch.' }
$StaticReceiptPath = [IO.Path]::GetFullPath([string]$StaticMarker.static_receipt_path)
if (-not (Test-Path -LiteralPath $StaticReceiptPath -PathType Leaf) -or (Get-FileSha256 $StaticReceiptPath) -ne $ExpectedStaticReceiptSha) { throw 'Accepted Phase L static receipt missing or SHA mismatch.' }

if (-not (Test-Path -LiteralPath $V2BCompletionPath -PathType Leaf)) { throw 'Accepted Phase M runtime completion marker missing.' }
$V2BMarker = Get-Content -LiteralPath $V2BCompletionPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$V2BMarker.schema -ne 'C11D-V2B-RUNTIME-MATRIX-COMPLETION-V1' -or
    [string]$V2BMarker.report_sha256 -ne $ExpectedV2BReportSha -or
    [string]$V2BMarker.static_receipt_sha256 -ne $ExpectedStaticReceiptSha) { throw 'Phase M completion marker does not match accepted evidence.' }
$V2BReportPath = [IO.Path]::GetFullPath([string]$V2BMarker.report_path)
if (-not (Test-Path -LiteralPath $V2BReportPath -PathType Leaf) -or (Get-FileSha256 $V2BReportPath) -ne $ExpectedV2BReportSha) { throw 'Phase M runtime report missing or hash mismatch.' }

$PythonExe = $null
if (-not [string]::IsNullOrWhiteSpace($env:C11D_PYTHON_EXECUTABLE) -and (Test-Path -LiteralPath $env:C11D_PYTHON_EXECUTABLE -PathType Leaf)) {
    $PythonExe = (Resolve-Path -LiteralPath $env:C11D_PYTHON_EXECUTABLE).Path
} else {
    $PythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $PythonCommand) { $PythonExe = $PythonCommand.Source }
}
if ([string]::IsNullOrWhiteSpace($PythonExe) -or -not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'Python 3.13 executable not found. Set C11D_PYTHON_EXECUTABLE to python.exe.' }

$GodotExe = $null
if (-not [string]::IsNullOrWhiteSpace($env:C11D_GODOT_EXECUTABLE) -and (Test-Path -LiteralPath $env:C11D_GODOT_EXECUTABLE -PathType Leaf)) {
    $GodotExe = (Resolve-Path -LiteralPath $env:C11D_GODOT_EXECUTABLE).Path
} else {
    $DefaultGodot = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe'
    if (Test-Path -LiteralPath $DefaultGodot -PathType Leaf) { $GodotExe = $DefaultGodot }
}
if ([string]::IsNullOrWhiteSpace($GodotExe) -or -not (Test-Path -LiteralPath $GodotExe -PathType Leaf)) { throw 'Godot 4.7.1 Mono executable not found; set C11D_GODOT_EXECUTABLE.' }

$RunId = [Guid]::NewGuid().ToString('N')
$LogDirectory = Join-Path $env:TEMP ('C11D_V2C_SOURCE_FRAME_RUNTIME_LOGS_20261027_' + $RunId)
$EvidenceDirectory = Join-Path $env:TEMP ('C11D_V2C_SOURCE_FRAME_EVIDENCE_20261027_' + $RunId)
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
if (Test-Path -LiteralPath $EvidenceDirectory) { throw "Evidence directory must not pre-exist: $EvidenceDirectory" }

$PythonVersionOut = Join-Path $LogDirectory 'python_version.stdout.txt'
$PythonVersionErr = Join-Path $LogDirectory 'python_version.stderr.txt'
$PythonVersionExit = Invoke-CapturedProcess $PythonExe '--version' $Root $PythonVersionOut $PythonVersionErr
$PythonVersionText = ((Get-Text $PythonVersionOut) + "`n" + (Get-Text $PythonVersionErr)).Trim()
if ($PythonVersionExit -ne 0 -or $PythonVersionText -notmatch '^Python 3\.13\.') { throw "Python 3.13 required; observed '$PythonVersionText'. Logs: $LogDirectory" }

$TestPath = Join-Path $Root $TestRel
$TestStdoutPath = Join-Path $LogDirectory 'contract_tests.stdout.txt'
$TestStderrPath = Join-Path $LogDirectory 'contract_tests.stderr.txt'
$TestArguments = '"' + $TestPath + '"'
$TestExit = Invoke-CapturedProcess $PythonExe $TestArguments $Root $TestStdoutPath $TestStderrPath
$TestStdout = Get-Text $TestStdoutPath
$TestStderr = Get-Text $TestStderrPath
$TestStdoutSha = Get-FileSha256 $TestStdoutPath
$TestStderrSha = Get-FileSha256 $TestStderrPath
if ($TestExit -ne 0 -or -not $TestStdout.Contains('C11D_V2C_PYTHON_CONTRACT_TESTS_PASS=28/28')) {
    Write-Host $TestStdout
    if ($TestStderr.Length -gt 0) { Write-Host $TestStderr }
    throw "V2-C contract tests failed closed. Exit=$TestExit; logs=$LogDirectory"
}

$AttemptData = [ordered]@{
    schema='C11D-V2C-SOURCE-FRAME-RUNTIME-ATTEMPT-V1'
    run_id=$RunId
    started_utc=(Get-Date).ToUniversalTime().ToString('o')
    project_root=$Root
    python_executable=$PythonExe
    python_version=$PythonVersionText
    godot_executable=$GodotExe
    contract_sha256=$ContractSha
    runner_sha256=$RunnerSha
    harness_sha256=$HarnessSha
    test_sha256=$TestSha
    test_exit_code=$TestExit
    test_stdout_sha256=$TestStdoutSha
    test_stderr_sha256=$TestStderrSha
    evidence_directory=$EvidenceDirectory
    log_directory=$LogDirectory
    runtime_status='STARTED_NOT_YET_VERIFIED'
}
Write-Utf8NoBom $AttemptMarkerPath (($AttemptData | ConvertTo-Json -Depth 8) + "`n")

$RuntimeScript = Join-Path $Root $RunnerRel
$RuntimeStdoutPath = Join-Path $LogDirectory 'source_frame_runtime.stdout.txt'
$RuntimeStderrPath = Join-Path $LogDirectory 'source_frame_runtime.stderr.txt'
$RuntimeArguments = '"' + $RuntimeScript + '" --repo-root "' + $Root + '" --evidence-dir "' + $EvidenceDirectory + '" --godot "' + $GodotExe + '"'
$RuntimeExit = Invoke-CapturedProcess $PythonExe $RuntimeArguments $Root $RuntimeStdoutPath $RuntimeStderrPath
$RuntimeStdout = Get-Text $RuntimeStdoutPath
$RuntimeStderr = Get-Text $RuntimeStderrPath
$RuntimeStdoutSha = Get-FileSha256 $RuntimeStdoutPath
$RuntimeStderrSha = Get-FileSha256 $RuntimeStderrPath
$ReportPath = Join-Path $EvidenceDirectory 'report.json'
if (-not (Test-Path -LiteralPath $ReportPath -PathType Leaf)) {
    Write-Host $RuntimeStdout
    if ($RuntimeStderr.Length -gt 0) { Write-Host $RuntimeStderr }
    throw "V2-C runner produced no report; preserve logs and attempt marker. Logs=$LogDirectory"
}
$ReportSha = Get-FileSha256 $ReportPath
$Report = Get-Content -LiteralPath $ReportPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ExpectedReportId = 'C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-REPORT-V1'
$StatusOk = ([string]$Report.schema -eq $ExpectedReportId -and [string]$Report.schema_version -eq '1.0' -and [string]$Report.status -eq 'PASS_SOURCE_FRAME_ROUTE_ONLY')
$CountsOk = ([int]$Report.source_pin_count -eq 81 -and [int]$Report.selector_count_expected -eq 9 -and [int]$Report.planner_invocations -eq 9 -and [int]$Report.godot_version_probe_invocations -eq 1 -and [int]$Report.godot_runtime_process_invocations -eq 18 -and [int]$Report.godot_runtime_processes_expected -eq 18)
$PinErrorCount = 0
if ($null -ne $Report.evidence.source_pin_errors_before_runtime) { $PinErrorCount = @($Report.evidence.source_pin_errors_before_runtime).Count }
$PolicyOk = ($Report.payload_materialized -eq $false -and $Report.media_created -eq $false -and [int]$Report.approved_bindings -eq 0 -and [string]$Report.visual_seed_sensitivity -eq 'NOT_TESTED' -and [string]$Report.contract_sha256 -eq $ContractSha -and [string]$Report.frozen_manifest_sha256 -eq $FrozenManifestSha -and [string]$Report.evidence.godot_version -eq '4.7.1.stable.mono.official.a13da4feb' -and [int]$Report.evidence.godot_version_probe_exit_code -eq 0 -and $PinErrorCount -eq 0 -and $null -eq $Report.evidence.failure)
$Governance = $Report.governance_locks
$D910 = [string]$Governance.PSObject.Properties['D9.10'].Value
$D914 = [string]$Governance.PSObject.Properties['D9.14'].Value
$D916 = [string]$Governance.PSObject.Properties['D9.16'].Value
$D917 = [string]$Governance.PSObject.Properties['D9.17'].Value
$D48 = [string]$Governance.PSObject.Properties['D4.8'].Value
$D10 = [string]$Governance.PSObject.Properties['D10'].Value
$GovernanceOk = ([string]$Governance.renderer -eq 'OFF' -and $Governance.media_created -eq $false -and $Governance.candidate_input_admissible -eq $false -and $Governance.seed_domains_complete_for_candidate_input -eq $false -and $Governance.automatic_seed_generation -eq $false -and [string]$Governance.master_seed -eq 'NOT_ADOPTED' -and $D48 -eq 'BLOCKED' -and $D910 -eq 'PREPARE_ONLY' -and $D914 -eq 'BLOCKED' -and $D916 -eq 'BLOCKED' -and $D917 -eq 'BLOCKED_NO_GO' -and $D10 -eq 'BLOCKED_FOR_PROMOTION' -and [string]$Governance.baseline_approval -eq 'MISSING' -and $Governance.freeze_eligible -eq $false -and [string]$Governance.release_authority -eq 'NONE' -and [string]$Governance.challenge_visual_seed_sensitivity -eq 'NOT_TESTED')
$Rows = @($Report.selectors)
$RowsOk = ($Rows.Count -eq 9)
$ProcessIds = New-Object System.Collections.ArrayList
$RunIds = New-Object System.Collections.ArrayList
if ($RowsOk) {
    $ExpectedIds = @('CHALLENGE_001','CHALLENGE_002','CHALLENGE_003','CHALLENGE_004','CHALLENGE_005','CHALLENGE_006','CHALLENGE_007','CHALLENGE_008','CHALLENGE_009')
    for ($i = 0; $i -lt 9; $i++) {
        $Row = $Rows[$i]
        $BlockReasonCount = 0
        if ($null -ne $Row.block_reasons) { $BlockReasonCount = @($Row.block_reasons).Count }
        if ([string]$Row.selector.challenge_id -ne $ExpectedIds[$i] -or [string]$Row.status -ne 'ACCEPTED_SOURCE_FRAME_ONLY' -or $BlockReasonCount -ne 0 -or $Row.repeat_agreement -ne $true -or [int]$Row.planner.invocations -ne 1 -or [string]$Row.planner.status -ne 'PLANNED' -or [string]$Row.planner.bridge_status -ne 'PLANNING_ONLY_NOT_RENDERABLE' -or [string]$Row.planner.adapter_status -ne 'PREPARED_NOT_DISPATCHED_RENDERER_DISABLED') {
            $RowsOk = $false; break
        }
        $Runs = @($Row.runtime_runs)
        if ($Runs.Count -ne 2) { $RowsOk = $false; break }
        foreach ($Run in $Runs) {
            if ([int]$Run.exit_code -ne 0 -or [int]$Run.process_id -le 0 -or $null -eq $Run.receipt -or [string]$Run.receipt.status -ne 'SOURCE_FRAME_RECEIPT' -or [string]$Run.receipt.route.runtime_bridge_method -ne 'ChallengeRuntimeBridge.run_effective_pipeline' -or $Run.receipt.side_effects.payload_file_written -ne $false -or $Run.receipt.side_effects.media_created -ne $false -or $Run.receipt.side_effects.renderer_native_input_emitted -ne $false -or $Run.receipt.side_effects.render_nodes_created -ne $false -or $Run.receipt.side_effects.rendering_server_called -ne $false -or $Run.receipt.side_effects.viewport_captured -ne $false -or $Run.receipt.side_effects.canonical_state_mutated -ne $false -or $Run.receipt.side_effects.production_dispatched -ne $false) {
                $RowsOk = $false; break
            }
            if ($ProcessIds.Contains([int]$Run.process_id) -or $RunIds.Contains([string]$Run.run_id)) { $RowsOk = $false; break }
            [void]$ProcessIds.Add([int]$Run.process_id)
            [void]$RunIds.Add([string]$Run.run_id)
        }
        if (-not $RowsOk) { break }
    }
}
$EvidenceMap = $Report.evidence.evidence_file_sha256
$EvidenceCount = 0
$EvidenceOk = ($null -ne $EvidenceMap)
if ($EvidenceOk) {
    foreach ($Property in $EvidenceMap.PSObject.Properties) {
        $Path = Join-Path $EvidenceDirectory $Property.Name
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf) -or (Get-FileSha256 $Path) -ne [string]$Property.Value) {
            $EvidenceOk = $false; break
        }
        $EvidenceCount++
    }
}
if ($EvidenceCount -ne 36 -or $ProcessIds.Count -ne 18 -or $RunIds.Count -ne 18) { $EvidenceOk = $false }
$SummaryOk = ($RuntimeExit -eq 0 -and $RuntimeStderr.Length -eq 0 -and $RuntimeStdout.Contains('C11D_V2C_RESULT=PASS_SOURCE_FRAME_ROUTE_ONLY') -and $RuntimeStdout.Contains('C11D_V2C_REPORT_SHA256=' + $ReportSha) -and $RuntimeStdout.Contains('C11D_V2C_PLANNER_INVOCATIONS=9/9') -and $RuntimeStdout.Contains('C11D_V2C_GODOT_RUNTIME_PROCESSES=18/18') -and $RuntimeStdout.Contains('C11D_V2C_SELECTORS=9/9'))

Write-Host ('PYTHON_CONTRACT_TESTS=28/28')
Write-Host ('TEST_STDOUT_SHA256=' + $TestStdoutSha)
Write-Host ('TEST_STDERR_SHA256=' + $TestStderrSha)
Write-Host ('RUNTIME_EXIT_CODE=' + $RuntimeExit)
Write-Host ('RUNTIME_REPORT_SHA256=' + $ReportSha)
Write-Host ('RUNTIME_STDOUT_SHA256=' + $RuntimeStdoutSha)
Write-Host ('RUNTIME_STDERR_SHA256=' + $RuntimeStderrSha)
Write-Host ('REPORT_STATUS_VALID=' + [string]$StatusOk)
Write-Host ('COUNTS_9_18_VALID=' + [string]$CountsOk)
Write-Host ('POLICY_AND_GODOT_IDENTITY_VALID=' + [string]$PolicyOk)
Write-Host ('GOVERNANCE_LOCKS_VALID=' + [string]$GovernanceOk)
Write-Host ('SELECTOR_RECEIPTS_VALID=' + [string]$RowsOk)
Write-Host ('PROCESS_EVIDENCE_FILES_VERIFIED=' + $EvidenceCount + '/36')
Write-Host ('RUNNER_SUMMARY_VALID=' + [string]$SummaryOk)
Write-Host ('LOG_DIRECTORY=' + $LogDirectory)
Write-Host ('EVIDENCE_DIRECTORY=' + $EvidenceDirectory)
if (-not $StatusOk -or -not $CountsOk -or -not $PolicyOk -or -not $GovernanceOk -or -not $RowsOk -or -not $EvidenceOk -or -not $SummaryOk) {
    Write-Host $RuntimeStdout
    if ($RuntimeStderr.Length -gt 0) { Write-Host $RuntimeStderr }
    throw 'V2-C source-frame runtime evidence did not satisfy every strict acceptance predicate. Preserve Temp logs and markers; do not rerun.'
}

$CompletionData = [ordered]@{
    schema='C11D-V2C-SOURCE-FRAME-RUNTIME-COMPLETION-V1'
    run_id=$RunId
    completed_utc=(Get-Date).ToUniversalTime().ToString('o')
    project_root=$Root
    contract_sha256=$ContractSha
    runner_sha256=$RunnerSha
    harness_sha256=$HarnessSha
    test_sha256=$TestSha
    test_stdout_sha256=$TestStdoutSha
    test_stderr_sha256=$TestStderrSha
    test_result='PASS_28_OF_28'
    runtime_report_path=$ReportPath
    runtime_report_sha256=$ReportSha
    runtime_stdout_sha256=$RuntimeStdoutSha
    runtime_stderr_sha256=$RuntimeStderrSha
    runtime_status=[string]$Report.status
    source_pin_count=[int]$Report.source_pin_count
    planner_invocations=[string]($Report.planner_invocations.ToString() + '/9')
    godot_version_probe_invocations=[int]$Report.godot_version_probe_invocations
    godot_runtime_process_invocations=[string]($Report.godot_runtime_process_invocations.ToString() + '/18')
    accepted_selectors='9/9'
    process_evidence_files_verified=[string]($EvidenceCount.ToString() + '/36')
    evidence_directory=$EvidenceDirectory
    log_directory=$LogDirectory
    frozen_c11c_manifest='UNCHANGED'
    renderer='OFF'; media_created=$false; payload_materialized=$false; candidate_input_admissible=$false
    D4_8='BLOCKED'; D9_10='PREPARE_ONLY'; D10='BLOCKED_FOR_PROMOTION'; release_authority='NONE'
}
Write-Utf8NoBom $CompletionMarkerPath (($CompletionData | ConvertTo-Json -Depth 12) + "`n")
Write-Host 'C11D_PHASE_N_V2C_SOURCE_FRAME_RUNTIME=PASS'
Write-Host 'PYTHON_CONTRACT_TESTS=28/28'
Write-Host 'SOURCE_PINS=81/81'
Write-Host 'PLANNER_INVOCATIONS=9/9'
Write-Host 'GODOT_VERSION_PROBE_INVOCATIONS=1'
Write-Host 'GODOT_RUNTIME_PROCESSES=18/18'
Write-Host 'SELECTORS=9/9'
Write-Host ('RUNTIME_REPORT_SHA256=' + $ReportSha)
Write-Host ('COMPLETION_MARKER=' + $CompletionMarkerPath)
Write-Host ('LOG_DIRECTORY=' + $LogDirectory)
Write-Host ('EVIDENCE_DIRECTORY=' + $EvidenceDirectory)
Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
Write-Host 'RENDERER=OFF'
Write-Host 'MEDIA_CREATED=false'
Write-Host 'PAYLOAD_MATERIALIZED=false'
Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
Write-Host 'D4.8=BLOCKED'
Write-Host 'RELEASE_AUTHORITY=NONE'
} finally {
    if ($null -eq $OldPyNoBytecode) { Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue }
    else { $env:PYTHONDONTWRITEBYTECODE = $OldPyNoBytecode }
}
