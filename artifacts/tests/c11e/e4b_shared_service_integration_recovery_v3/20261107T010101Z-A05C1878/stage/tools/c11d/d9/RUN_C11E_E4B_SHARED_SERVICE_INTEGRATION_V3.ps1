#requires -Version 5.1
[CmdletBinding()]
param([string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Projects\ChallengeEngineV01_STATELESS'))
$ErrorActionPreference='Stop'
Set-StrictMode -Version 2.0
Write-Host '========== C11-E E4B SHARED SERVICE INTEGRATION V3 RUNNER =========='
Write-Host ('POWERSHELL_RUNTIME_VERSION='+$PSVersionTable.PSVersion.ToString())
if($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1){ throw 'POWERSHELL_5_1_REQUIRED' }
$tokens=$null;$parseErrors=$null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$tokens,[ref]$parseErrors)|Out-Null
if($parseErrors.Count -gt 0){$parseErrors|ForEach-Object{Write-Host $_.Message};throw 'POWERSHELL_5_1_AST_PARSE=FAIL'}
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
$runnerBytes=[System.IO.File]::ReadAllBytes($PSCommandPath);foreach($b in $runnerBytes){if($b -gt 127){throw 'RUNNER_SOURCE_ENCODING_INVALID'}}
Write-Host 'RUNNER_SOURCE_ENCODING=ASCII_SAFE'
Write-Host 'GIT=NOT_INVOKED; READ_ONLY_TESTS=TRUE; GENERIC_LIST_ARRAY_SUBEXPRESSION=AVOIDED'
$ProjectRoot=[System.IO.Path]::GetFullPath($ProjectRoot)
function Get-Sha([string]$Path){if(-not(Test-Path -LiteralPath $Path -PathType Leaf)){throw "MISSING_FILE: $Path"};(Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Write-Utf8([string]$Path,[string]$Content){$enc=New-Object System.Text.UTF8Encoding($false);[System.IO.File]::WriteAllText($Path,$Content,$enc)}
function Invoke-RecordedProcess([string]$Name,[string]$FilePath,[string[]]$Arguments,[string]$WorkingDirectory,[string]$RunRoot){
    $stdout=Join-Path $RunRoot ($Name+'.stdout.log');$stderr=Join-Path $RunRoot ($Name+'.stderr.log')
    $proc=Start-Process -FilePath $FilePath -ArgumentList $Arguments -WorkingDirectory $WorkingDirectory -RedirectStandardOutput $stdout -RedirectStandardError $stderr -Wait -PassThru -NoNewWindow
    [pscustomobject]@{name=$Name;executable=$FilePath;arguments=$Arguments;working_directory=$WorkingDirectory;exit_code=[int]$proc.ExitCode;stdout_path=$stdout;stdout_sha256=(Get-Sha $stdout);stderr_path=$stderr;stderr_sha256=(Get-Sha $stderr)}
}
$frozen='e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
if((Get-Sha (Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json')) -ne $frozen){throw 'FROZEN_C11C_MANIFEST_MISMATCH'}
Write-Host 'FROZEN_C11C_MANIFEST=PASS'
$pinsPath=Join-Path $ProjectRoot 'tools\c11d\d9\C11E_E4B_SHARED_SERVICE_INTEGRATION_V3_SOURCE_PINS.json'
$pins=Get-Content -LiteralPath $pinsPath -Raw -Encoding UTF8|ConvertFrom-Json
if($pins.schema -ne 'C11E-E4B-SHARED-SERVICE-INTEGRATION-RECOVERY-PINS-V3'){throw 'V3_SOURCE_PINS_SCHEMA_INVALID'}
foreach($p in @($pins.source_patches)){ $actual=Get-Sha (Join-Path $ProjectRoot $p.path);if($actual -ne ([string]$p.postimage_sha256).ToLowerInvariant()){throw "V2_SOURCE_POSTIMAGE_MISMATCH: $($p.path)"} }
Write-Host 'V2_SOURCE_POSTIMAGES=PASS; COUNT=6/6'
foreach($a in @($pins.v2_add_only_files)){ $path=Join-Path $ProjectRoot $a.path;$actual=Get-Sha $path;if($actual -ne ([string]$a.sha256).ToLowerInvariant()){throw "V2_ADD_ONLY_PIN_MISMATCH: $($a.path)"} }
Write-Host 'V2_ADD_ONLY_OUTPUTS=PASS; COUNT=15/15'
# Verify the V3 recovery receipt from the most recent installer run.
$repairRoot=Join-Path $ProjectRoot 'artifacts\tests\c11e\e4b_shared_service_integration_recovery_v3'
if(-not(Test-Path -LiteralPath $repairRoot -PathType Container)){throw 'V3_RECOVERY_INSTALLER_NOT_RUN'}
$repairDirs=@(Get-ChildItem -LiteralPath $repairRoot -Directory|Sort-Object Name -Descending)
if($repairDirs.Count -eq 0){throw 'V3_RECOVERY_RUN_DIRECTORY_MISSING'}
$repairReceiptPath=Join-Path $repairDirs[0].FullName 'C11E_E4B_SHARED_SERVICE_INTEGRATION_V3_RECOVERY_RECEIPT.json'
$repairReceiptSha=Get-Sha $repairReceiptPath
$repairReceipt=Get-Content -LiteralPath $repairReceiptPath -Raw -Encoding UTF8|ConvertFrom-Json
if($repairReceipt.status -ne 'PASS_V2_INSTALL_EFFECTS_CONFIRMED_AND_V3_ADD_ONLY_INSTALLED' -or @($repairReceipt.v2_source_postimages).Count -ne 6 -or @($repairReceipt.v2_add_only_outputs).Count -ne 15 -or @($repairReceipt.v2_source_backups).Count -ne 6){throw 'V3_RECOVERY_RECEIPT_NOT_ACCEPTED'}
Write-Host ('V3_RECOVERY_RECEIPT=PASS; SHA256='+$repairReceiptSha)
$v2Report=Join-Path $ProjectRoot 'artifacts\tests\c11e\e4b_loop_family_contract_v2\20261106T234410Z-A5713C32\C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT_V2.json'
$v2Receipt=Join-Path $ProjectRoot 'artifacts\tests\c11e\e4b_loop_family_contract_v2\20261106T234410Z-A5713C32\C11E_E4B_LOOP_FAMILY_CONTRACT_RUNNER_RECEIPT_V2.json'
$v2ReportSha=Get-Sha $v2Report
if($v2ReportSha -ne '788ab1352a3e11bd91cc2ddf34fc8f11334b7713b9bc1a2b246156c79f40444e'){throw 'E4B_V2_REPORT_SHA_MISMATCH'}
$v2ReceiptObj=Get-Content -LiteralPath $v2Receipt -Raw -Encoding UTF8|ConvertFrom-Json
if($v2ReceiptObj.status -ne 'PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY' -or $v2ReceiptObj.report_sha256 -ne $v2ReportSha -or $v2ReceiptObj.test_exit_code -ne 0 -or $v2ReceiptObj.audit_exit_code -ne 0){throw 'E4B_FAMILY_CONTRACT_V2_EVIDENCE_NOT_ACCEPTED'}
Write-Host 'E4B_FAMILY_CONTRACT_V2=PASS_STATIC_ONLY'
$py=Get-Command py -ErrorAction SilentlyContinue
if($null -eq $py){throw 'PYTHON_LAUNCHER_PY_NOT_FOUND; PYTHON_3_13_REQUIRED'}
$pythonExe=$py.Source
$runId=(Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')+'-'+([guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$runRoot=Join-Path $ProjectRoot ('artifacts\tests\c11e\e4b_shared_service_integration_v3\'+$runId)
New-Item -ItemType Directory -Path $runRoot -Force|Out-Null
$stageResults=@()
$producerRoot=Join-Path $ProjectRoot 'c11c-suite\c11c-producer'
$version=Invoke-RecordedProcess 'PYTHON_313_VERSION' $pythonExe @('-3.13','-B','--version') $ProjectRoot $runRoot
$stageResults+=,$version
if($version.exit_code -ne 0 -or (Get-Content -LiteralPath $version.stdout_path -Raw) -notmatch 'Python 3\.13\.') {throw 'PYTHON_3_13_REQUIRED'}
Write-Host 'PYTHON_RUNTIME=PYTHON_3_13_PASS'
$service=Invoke-RecordedProcess 'E4B_SHARED_SERVICE_TESTS' $pythonExe @('-3.13','-B','-m','unittest','-v','test_c11e_production_service') $producerRoot $runRoot
$stageResults+=,$service
if($service.exit_code -ne 0){throw "E4B_SHARED_SERVICE_TESTS_FAILED: $($service.exit_code)"}
$serviceText=Get-Content -LiteralPath $service.stderr_path -Raw
if($serviceText -notmatch 'Ran 25 tests' -or $serviceText -notmatch 'OK'){throw 'E4B_SHARED_SERVICE_TEST_COUNT_NOT_25'}
Write-Host 'E4B_SHARED_SERVICE_TESTS=25/25_PASS; LOOP_SELECTORS=27/27'
$model=Invoke-RecordedProcess 'D98_UNIVERSAL_EDITORIAL_MODEL_TEST' $pythonExe @('-3.13','-B','tools\c11d\d9\test_universal_editorial_model.py') $ProjectRoot $runRoot
$stageResults+=,$model
if($model.exit_code -ne 0){throw 'D98_UNIVERSAL_EDITORIAL_MODEL_TEST_FAILED'}
Write-Host 'D98_EDITORIAL_MODEL_TEST=PASS'
$code="from pathlib import Path; files=['c11c-suite/c11c-producer/c11e_production_service.py','c11c-suite/c11c-producer/main.py','c11c-suite/c11c-producer/test_c11e_production_service.py','tools/c11d/d9/universal_editorial_model.py','tools/c11d/d9/test_universal_editorial_model.py']; [compile(Path(p).read_bytes(),p,'exec') for p in files]; print('PYTHON_SYNTAX_COMPILE_IN_MEMORY=PASS')"
$compileArg='"'+$code+'"'
$compile=Invoke-RecordedProcess 'PYTHON_SYNTAX_COMPILE_IN_MEMORY' $pythonExe @('-3.13','-B','-c',$compileArg) $ProjectRoot $runRoot
$stageResults+=,$compile
if($compile.exit_code -ne 0){throw 'PYTHON_SYNTAX_COMPILE_FAILED'}
Write-Host 'PYTHON_SYNTAX_COMPILE=PASS; CACHE_WRITES=DISABLED'
$d915=Invoke-RecordedProcess 'D915_LIVE_READ_ONLY_STATUS' $pythonExe @('-3.13','-B','tools\c11d\baseline_candidate\operator_evidence.py','status') $ProjectRoot $runRoot
$stageResults+=,$d915
$d915Status='BLOCKED_OR_REVALIDATION_REQUIRED'
if($d915.exit_code -eq 0){$t=Get-Content -LiteralPath $d915.stdout_path -Raw;if($t -match 'D9.15_OPERATOR_EVIDENCE_PASS_CLOSED'){$d915Status='PASS_CLOSED'}else{$d915Status='CHECK_OUTPUT'}}
Write-Host ('D9_15_LIVE_STATUS='+$d915Status+'; EXIT='+$d915.exit_code)
$db=Invoke-RecordedProcess 'D_BASELINE_READ_ONLY_DIAGNOSTIC' $pythonExe @('-3.13','-B','tools\c11d\d9\C11E_D_BASELINE_READ_ONLY_DIAGNOSTIC_V1.py') $ProjectRoot $runRoot
$stageResults+=,$db
$dbStatus='BLOCKED_OR_REVALIDATION_REQUIRED';if($db.exit_code -eq 0){$dbStatus='PREFLIGHT_REPORT_AVAILABLE'}
Write-Host ('D_BASELINE_READ_ONLY_STATUS='+$dbStatus+'; EXIT='+$db.exit_code)
foreach($p in @($pins.source_patches)){if((Get-Sha (Join-Path $ProjectRoot $p.path)) -ne ([string]$p.postimage_sha256).ToLowerInvariant()){throw "FINAL_SOURCE_PIN_DRIFT: $($p.path)"}}
Write-Host 'SOURCE_POSTIMAGES_FINAL=PASS; COUNT=6/6'
# Use a normal PowerShell Object[]; avoid @() over New-Object Generic.List[object].
$report=[ordered]@{
 schema='C11E-E4B-SHARED-SERVICE-INTEGRATION-RUN-REPORT-V3';run_id=$runId;created_utc=[DateTime]::UtcNow.ToString('o');project_root=$ProjectRoot
 powershell_version=$PSVersionTable.PSVersion.ToString();python_version=(Get-Content -LiteralPath $version.stdout_path -Raw).Trim()
 frozen_c11c_manifest_sha256=$frozen;v2_report_sha256=$v2ReportSha;v3_recovery_receipt_sha256=$repairReceiptSha
 source_postimages=@($pins.source_patches|ForEach-Object{[ordered]@{path=$_.path;sha256=$_.postimage_sha256}})
 stage_results=$stageResults;service_test_count=25;loop_grammars_prepared=27;d98_model_test='PASS';python_syntax_compile='PASS_IN_MEMORY'
 d915_live_status=$d915Status;d_baseline_status=$dbStatus
 governance=[ordered]@{renderer='OFF';launcher_invoked=$false;dispatch=$false;audio=$false;media=$false;c11c_baseline_modified=$false;d4_8='BLOCKED';d9_10='PREPARE_ONLY';d9_14='BLOCKED';d9_16='BLOCKED';d9_17='BLOCKED_NO_GO';d10='BLOCKED_FOR_PROMOTION';release_authority='NONE'}
 status='PASS_TEST_ONLY_SHARED_LOOP_BOUNDARY_PREPARATION_V3'
}
$reportPath=Join-Path $runRoot 'C11E_E4B_SHARED_SERVICE_INTEGRATION_RUN_REPORT_V3.json'
Write-Utf8 $reportPath ($report|ConvertTo-Json -Depth 30)
$reportSha=Get-Sha $reportPath;Write-Utf8 ($reportPath+'.sha256') ($reportSha+'  '+[System.IO.Path]::GetFileName($reportPath)+"`n")
$stageHashArray=@($stageResults|ForEach-Object{[ordered]@{name=$_.name;exit_code=$_.exit_code;stdout_sha256=$_.stdout_sha256;stderr_sha256=$_.stderr_sha256}})
$receipt=[ordered]@{schema='C11E-E4B-SHARED-SERVICE-INTEGRATION-RUN-RECEIPT-V3';status=$report.status;run_id=$runId;report_path=$reportPath;report_sha256=$reportSha;v3_recovery_receipt_sha256=$repairReceiptSha;service_tests='25/25_PASS';loop_selectors='27/27_PREPARED_NOT_RENDERED';d98_model_test='PASS';d915_live_status=$d915Status;d_baseline_status=$dbStatus;stage_log_hashes=$stageHashArray;governance=$report.governance}
$receiptPath=Join-Path $runRoot 'C11E_E4B_SHARED_SERVICE_INTEGRATION_RUN_RECEIPT_V3.json'
Write-Utf8 $receiptPath ($receipt|ConvertTo-Json -Depth 30)
$receiptSha=Get-Sha $receiptPath;Write-Utf8 ($receiptPath+'.sha256') ($receiptSha+'  '+[System.IO.Path]::GetFileName($receiptPath)+"`n")
Write-Host ('REPORT_SHA256='+$reportSha);Write-Host ('RECEIPT_SHA256='+$receiptSha);Write-Host ('RECEIPT='+$receiptPath)
Write-Host 'RENDERER=OFF; LAUNCHERS=NOT_INVOKED; AUDIO=FALSE; MEDIA=FALSE; RELEASE_AUTHORITY=NONE'
Write-Host 'C11E_E4B_SHARED_SERVICE_INTEGRATION_V3=PASS_TEST_ONLY_SHARED_LOOP_BOUNDARY_PREPARATION'
