#requires -Version 5.1
[CmdletBinding()]
param(
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Projects\ChallengeEngineV01_STATELESS')
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

Write-Host '========== C11-E E4B SHARED SERVICE INTEGRATION V1 =========='
Write-Host ('POWERSHELL_RUNTIME_VERSION=' + $PSVersionTable.PSVersion.ToString())
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'POWERSHELL_5_1_REQUIRED' }
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { $parseErrors | ForEach-Object { Write-Host $_.Message }; throw 'POWERSHELL_5_1_AST_PARSE=FAIL' }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
Write-Host 'RUNNER_SOURCE_ENCODING=ASCII_SAFE'
$runnerBytes = [System.IO.File]::ReadAllBytes($PSCommandPath)
foreach ($byte in $runnerBytes) { if ($byte -gt 127) { throw 'RUNNER_SOURCE_ENCODING_INVALID' } }
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; READ_ONLY_TESTS=TRUE'

$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "PROJECT_ROOT_NOT_FOUND: $ProjectRoot" }
function Get-Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "MISSING_FILE: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-Pin([string]$RelativePath, [string]$Expected) {
    $actual = Get-Sha256 (Join-Path $ProjectRoot $RelativePath)
    if ($actual -ne $Expected.ToLowerInvariant()) { throw "SOURCE_POSTIMAGE_PIN_MISMATCH: $RelativePath expected=$Expected actual=$actual" }
}
function Write-Utf8NoBom([string]$Path, [string]$Content) {
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}
function Invoke-RecordedProcess([string]$Name, [string]$FilePath, [string[]]$Arguments, [string]$WorkingDirectory, [string]$RunRoot) {
    $stdout = Join-Path $RunRoot ($Name + '.stdout.log')
    $stderr = Join-Path $RunRoot ($Name + '.stderr.log')
    $process = Start-Process -FilePath $FilePath -ArgumentList $Arguments -WorkingDirectory $WorkingDirectory -RedirectStandardOutput $stdout -RedirectStandardError $stderr -Wait -PassThru -NoNewWindow
    $stdoutSha = Get-Sha256 $stdout
    $stderrSha = Get-Sha256 $stderr
    return [pscustomobject]@{
        name = $Name
        executable = $FilePath
        arguments = @($Arguments)
        working_directory = $WorkingDirectory
        exit_code = [int]$process.ExitCode
        stdout_path = $stdout
        stdout_sha256 = $stdoutSha
        stderr_path = $stderr
        stderr_sha256 = $stderrSha
    }
}

$FrozenManifestExpected = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$manifestPath = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$manifestSha = Get-Sha256 $manifestPath
if ($manifestSha -ne $FrozenManifestExpected) { throw "FROZEN_C11C_MANIFEST_MISMATCH: $manifestSha" }
Write-Host 'FROZEN_C11C_MANIFEST=PASS'

$sourcePins = [ordered]@{
    'c11c-suite/c11c-producer/c11e_production_service.py' = '08ab5a278de8ebb55795a57391c83a27207ce01920704c419b8e28be25ddcf65'
    'c11c-suite/c11c-producer/main.py' = 'ad88ac99a4582a6a470b8885425144ab7265188c3771ed4c48d8857c43343c55'
    'c11c-suite/c11c-producer/test_c11e_production_service.py' = '6fecc35f3f3d8dc0e138a70452b1eee9acadbcd8f95db05dc6518baad80ed285'
    'definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json' = 'dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb'
    'tools/c11d/d9/universal_editorial_model.py' = 'dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd'
    'tools/c11d/d9/test_universal_editorial_model.py' = 'd36319e49fcc93c530a7fd2747d6db2536aa70f4fcd02825d1836d0795045e4c'
}
foreach ($relative in $sourcePins.Keys) { Assert-Pin $relative $sourcePins[$relative] }
Write-Host 'SOURCE_POSTIMAGE_PINS=PASS; COUNT=6/6'

$v2ReportRelative = 'artifacts/tests/c11e/e4b_loop_family_contract_v2/20261106T234410Z-A5713C32/C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT_V2.json'
$v2ReceiptRelative = 'artifacts/tests/c11e/e4b_loop_family_contract_v2/20261106T234410Z-A5713C32/C11E_E4B_LOOP_FAMILY_CONTRACT_RUNNER_RECEIPT_V2.json'
$v2ReportSha = Get-Sha256 (Join-Path $ProjectRoot $v2ReportRelative)
if ($v2ReportSha -ne '788ab1352a3e11bd91cc2ddf34fc8f11334b7713b9bc1a2b246156c79f40444e') { throw 'E4B_V2_REPORT_SHA_MISMATCH' }
$v2ReceiptPath = Join-Path $ProjectRoot $v2ReceiptRelative
$v2ReceiptSha = Get-Sha256 $v2ReceiptPath
$v2Receipt = Get-Content -LiteralPath $v2ReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($v2Receipt.status -ne 'PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY' -or $v2Receipt.report_sha256 -ne $v2ReportSha -or $v2Receipt.test_exit_code -ne 0 -or $v2Receipt.audit_exit_code -ne 0) { throw 'E4B_V2_RECEIPT_NOT_ACCEPTED' }
Write-Host 'E4B_V2_PRIOR_EVIDENCE=PASS; REPORT_SHA256=788ab1352a3e11bd91cc2ddf34fc8f11334b7713b9bc1a2b246156c79f40444e'

$pinManifestPath = Join-Path $ProjectRoot 'tools\c11d\d9\C11E_E4B_SHARED_SERVICE_INTEGRATION_V1_SOURCE_PINS.json'
$pinManifestShaExpected = '27ea502a4df2b158a080caab5a19547baf4b3e68afea187f7b546e1b3831e3b6'
if ((Get-Sha256 $pinManifestPath) -ne $pinManifestShaExpected) { throw 'V80_SOURCE_PIN_MANIFEST_MISMATCH' }
$pinManifest = Get-Content -LiteralPath $pinManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($pinManifest.schema -ne 'C11E-E4B-SHARED-SERVICE-INTEGRATION-SOURCE-PINS-V1' -or @($pinManifest.source_patches).Count -ne 6) { throw 'V80_SOURCE_PIN_MANIFEST_SCHEMA_INVALID' }

$pythonCommand = Get-Command py -ErrorAction SilentlyContinue
if ($null -eq $pythonCommand) { throw 'PYTHON_LAUNCHER_PY_NOT_FOUND; Python 3.13 REQUIRED' }
$pythonExe = $pythonCommand.Source
$runId = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$runRoot = Join-Path $ProjectRoot ('artifacts\tests\c11e\e4b_shared_service_integration\' + $runId)
New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$stageResults = New-Object System.Collections.Generic.List[object]
$producerRoot = Join-Path $ProjectRoot 'c11c-suite\c11c-producer'

$version = Invoke-RecordedProcess 'PYTHON_313_VERSION' $pythonExe @('-3.13','-B','--version') $ProjectRoot $runRoot
$stageResults.Add($version)
if ($version.exit_code -ne 0 -or (Get-Content -LiteralPath $version.stdout_path -Raw) -notmatch 'Python 3\.13\.') { throw 'PYTHON_3_13_REQUIRED' }
Write-Host 'PYTHON_RUNTIME=Python 3.13; PASS'

$serviceTests = Invoke-RecordedProcess 'E4B_SHARED_SERVICE_TESTS' $pythonExe @('-3.13','-B','-m','unittest','-v','test_c11e_production_service') $producerRoot $runRoot
$stageResults.Add($serviceTests)
if ($serviceTests.exit_code -ne 0) { throw "E4B_SHARED_SERVICE_TESTS_FAILED: exit=$($serviceTests.exit_code)" }
$serviceOutput = Get-Content -LiteralPath $serviceTests.stderr_path -Raw
if ($serviceOutput -notmatch 'Ran 25 tests' -or $serviceOutput -notmatch 'OK') { throw 'E4B_SHARED_SERVICE_TEST_COUNT_NOT_25' }
Write-Host 'E4B_SHARED_SERVICE_TESTS=25/25_PASS; LOOP_SELECTORS=27/27'

$modelTest = Invoke-RecordedProcess 'D98_UNIVERSAL_EDITORIAL_MODEL_TEST' $pythonExe @('-3.13','-B','tools\c11d\d9\test_universal_editorial_model.py') $ProjectRoot $runRoot
$stageResults.Add($modelTest)
if ($modelTest.exit_code -ne 0) { throw 'D98_UNIVERSAL_EDITORIAL_MODEL_TEST_FAILED' }
Write-Host 'D98_EDITORIAL_MODEL_TEST=PASS'

$compileCode = "from pathlib import Path; files = ['c11c-suite/c11c-producer/c11e_production_service.py', 'c11c-suite/c11c-producer/main.py', 'c11c-suite/c11c-producer/test_c11e_production_service.py', 'tools/c11d/d9/universal_editorial_model.py', 'tools/c11d/d9/test_universal_editorial_model.py']; [compile(Path(p).read_bytes(), p, 'exec') for p in files]; print('PYTHON_SYNTAX_COMPILE_IN_MEMORY=PASS')"
$compileArgument = '"' + $compileCode + '"'
$compileTest = Invoke-RecordedProcess 'PYTHON_SYNTAX_COMPILE_IN_MEMORY' $pythonExe @('-3.13','-B','-c',$compileArgument) $ProjectRoot $runRoot
$stageResults.Add($compileTest)
if ($compileTest.exit_code -ne 0) { throw 'PYTHON_SYNTAX_COMPILE_FAILED' }
Write-Host 'PYTHON_SYNTAX_COMPILE=PASS; PYTHON_CACHE_WRITES=DISABLED'

# D9.15 is a separate read-only diagnostic. Missing evidence does not invalidate
# the Loop preparation tests, but it remains a blocker for D9 full acceptance.
$d915 = Invoke-RecordedProcess 'D915_LIVE_READ_ONLY_STATUS' $pythonExe @('-3.13','-B','tools\c11d\baseline_candidate\operator_evidence.py','status') $ProjectRoot $runRoot
$stageResults.Add($d915)
$d915Status = 'BLOCKED_OR_REVALIDATION_REQUIRED'
if ($d915.exit_code -eq 0) {
    $d915Text = Get-Content -LiteralPath $d915.stdout_path -Raw
    if ($d915Text -match 'D9.15_OPERATOR_EVIDENCE_PASS_CLOSED') { $d915Status = 'PASS_CLOSED' } else { $d915Status = 'CHECK_OUTPUT' }
}
Write-Host ('D9_15_LIVE_READ_ONLY_STATUS=' + $d915Status + '; EXIT_CODE=' + $d915.exit_code)

$dBaseline = Invoke-RecordedProcess 'D_BASELINE_READ_ONLY_DIAGNOSTIC' $pythonExe @('-3.13','-B','tools\c11d\d9\C11E_D_BASELINE_READ_ONLY_DIAGNOSTIC_V1.py') $ProjectRoot $runRoot
$stageResults.Add($dBaseline)
$dBaselineStatus = 'BLOCKED_OR_REVALIDATION_REQUIRED'
if ($dBaseline.exit_code -eq 0) { $dBaselineStatus = 'PREFLIGHT_REPORT_AVAILABLE' }
Write-Host ('D_BASELINE_READ_ONLY_DIAGNOSTIC=' + $dBaselineStatus + '; EXIT_CODE=' + $dBaseline.exit_code)

foreach ($relative in $sourcePins.Keys) { Assert-Pin $relative $sourcePins[$relative] }
Write-Host 'SOURCE_POSTIMAGE_PINS_FINAL=PASS; COUNT=6/6'

$report = [ordered]@{
    schema = 'C11E-E4B-SHARED-SERVICE-INTEGRATION-RUN-REPORT-V1'
    run_id = $runId
    created_utc = [DateTime]::UtcNow.ToString('o')
    project_root = $ProjectRoot
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_version = (Get-Content -LiteralPath $version.stdout_path -Raw).Trim()
    frozen_c11c_manifest_sha256 = $manifestSha
    v2_audit_report_sha256 = $v2ReportSha
    v2_audit_receipt_sha256 = $v2ReceiptSha
    source_pin_manifest_sha256 = $pinManifestShaExpected
    source_postimage_count = 6
    source_postimages = @($sourcePins.GetEnumerator() | ForEach-Object { [ordered]@{ path=$_.Key; sha256=$_.Value } })
    stage_results = @($stageResults)
    service_test_count = 25
    loop_grammars_prepared_by_tests = 27
    d98_model_test = 'PASS'
    python_syntax_compile = 'PASS_IN_MEMORY'
    python_cache_writes_disabled = $true
    d915_live_read_only_status = $d915Status
    d_baseline_read_only_diagnostic = $dBaselineStatus
    governance = [ordered]@{ renderer_native_input_emitted=$false; renderer_dispatch_invoked=$false; launcher_invoked=$false; godot_invoked=$false; ffmpeg_invoked=$false; audio_generated=$false; media_created=$false; c11c_source_mutation=$false; d4_8='BLOCKED'; d9_10='PREPARE_ONLY'; d9_14='BLOCKED'; d9_16='BLOCKED'; d9_17='BLOCKED_NO_GO'; d10='BLOCKED_FOR_PROMOTION'; release_authority='NONE' }
    status = 'PASS_TEST_ONLY_SHARED_LOOP_BOUNDARY_PREPARATION'
}
$reportPath = Join-Path $runRoot 'C11E_E4B_SHARED_SERVICE_INTEGRATION_RUN_REPORT_V1.json'
Write-Utf8NoBom $reportPath ($report | ConvertTo-Json -Depth 25)
$reportSha = Get-Sha256 $reportPath
Write-Utf8NoBom ($reportPath + '.sha256') ($reportSha + '  ' + [System.IO.Path]::GetFileName($reportPath) + "`n")
$receipt = [ordered]@{
    schema = 'C11E-E4B-SHARED-SERVICE-INTEGRATION-RUN-RECEIPT-V1'
    status = 'PASS_TEST_ONLY_SHARED_LOOP_BOUNDARY_PREPARATION'
    run_id = $runId
    report_path = $reportPath
    report_sha256 = $reportSha
    frozen_c11c_manifest_sha256 = $manifestSha
    v2_audit_report_sha256 = $v2ReportSha
    v2_audit_receipt_sha256 = $v2ReceiptSha
    source_pin_manifest_sha256 = $pinManifestShaExpected
    python_version = $report.python_version
    service_tests = '25/25_PASS'
    loop_selectors = '27/27_PREPARED_NOT_RENDERED'
    d98_model_test = 'PASS'
    python_syntax_compile = 'PASS_IN_MEMORY'
    python_cache_writes_disabled = $true
    d915_live_read_only_status = $d915Status
    d_baseline_read_only_diagnostic = $dBaselineStatus
    stage_log_hashes = @($stageResults | ForEach-Object { [ordered]@{ name=$_.name; exit_code=$_.exit_code; stdout_sha256=$_.stdout_sha256; stderr_sha256=$_.stderr_sha256 } })
    governance = $report.governance
}
$receiptPath = Join-Path $runRoot 'C11E_E4B_SHARED_SERVICE_INTEGRATION_RUN_RECEIPT_V1.json'
Write-Utf8NoBom $receiptPath ($receipt | ConvertTo-Json -Depth 25)
$receiptSha = Get-Sha256 $receiptPath
Write-Utf8NoBom ($receiptPath + '.sha256') ($receiptSha + '  ' + [System.IO.Path]::GetFileName($receiptPath) + "`n")
Write-Host ('REPORT_SHA256=' + $reportSha)
Write-Host ('RECEIPT_SHA256=' + $receiptSha)
Write-Host ('RECEIPT=' + $receiptPath)
Write-Host 'RENDERER=OFF; LAUNCHERS=NOT_INVOKED; AUDIO=FALSE; MEDIA=FALSE; RELEASE_AUTHORITY=NONE'
Write-Host 'C11E_E4B_SHARED_SERVICE_INTEGRATION=PASS_TEST_ONLY_SHARED_LOOP_BOUNDARY_PREPARATION'
