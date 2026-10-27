# C11-D Phase O — read-only source-frame / semantic-binding crosswalk.
# Windows PowerShell 5.1. Does not rerun Phase N, planner, Godot or payload/media generation.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$ExpectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..')).TrimEnd('\')
$Current = [IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\')
if (-not [string]::Equals($Root, $ExpectedRoot, [StringComparison]::OrdinalIgnoreCase) -or
    -not [string]::Equals($Current, $ExpectedRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Ejecuta desde la raiz exacta del checkout: $ExpectedRoot"
}

function Get-FileSha256([string]$Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Read-JsonFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "JSON ausente: $Path" }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}
function Assert-Sha([string]$Path, [string]$Expected, [string]$Label) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "$Label ausente: $Path" }
    $Observed = Get-FileSha256 $Path
    if ($Observed -ne $Expected) { throw "$Label SHA incorrecto: observado=$Observed esperado=$Expected" }
}
function Read-ProcessText([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return '' }
    return [IO.File]::ReadAllText($Path)
}
function Write-Utf8NoBom([string]$Path, [string]$Text) {
    [IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false)))
}

$ExpectedFrozenSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$ExpectedCheckpointSha = '9cccc148927a950a14f76a9e7afb13c1e0d8b8fa1f3ac556a7f01c7244985f2d'
$ExpectedLedgerSha = '7f44a13f633bd8847cfc60f24d635df6dfe17fb8024af38b8bf2404b68d2fa28'
$ExpectedAcceptanceRecordSha = 'a0faf6e6ddf145b69b649de45366bfadf0947c7b55a78444c4d546fe3efdeb96'
$ExpectedRuntimeReportSha = '7f96c9aec3849212299afbcabe7fd3045fee815807c9cafe555ad8cb947f91f2'
$ExpectedRuntimeStdoutSha = 'bacfa68d6cd7f89e2466baac2b28ec0a9b37af4bcd073af9581bd6e05bffd69a'
$ExpectedTestStdoutSha = '6e869618eb36c6f6ee74de8af851b9d3cb5810cfd35df37968176c06f17fb808'
$EmptySha = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
$Completed = Join-Path $env:TEMP 'C11D_PHASE_O_SEMANTIC_CROSSWALK_20261027.completed.json'
if (Test-Path -LiteralPath $Completed) { throw "Fase O ya tiene marcador PASS; no repetir: $Completed" }

$FrozenPath = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
Assert-Sha $FrozenPath $ExpectedFrozenSha 'Manifiesto C11-C'
if ((Get-Item -LiteralPath $FrozenPath).Length -ne 796318) { throw 'Tamano del manifiesto C11-C incorrecto.' }
Assert-Sha (Join-Path $Root 'docs\current\d\D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md') $ExpectedCheckpointSha 'Checkpoint Fase N'
Assert-Sha (Join-Path $Root 'docs\current\d\C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md') $ExpectedLedgerSha 'Ledger Fase N'
Assert-Sha (Join-Path $Root 'docs\current\d\C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_20261027_V1.md') $ExpectedAcceptanceRecordSha 'Registro de aceptacion Fase N'

# Verify all input contracts pinned by the Phase O audit.
$Pins = @(
    @{Rel='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json'; Sha='6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c'; Name='Contrato de recibo V2-C'},
    @{Rel='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RECEIPT_SCHEMA_V1.json'; Sha='90f14fb8c68317f6cea2e473b775b044e69249a1fa4a4776905a140efed6f547'; Name='Schema recibo V2-C'},
    @{Rel='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_REPORT_SCHEMA_V1.json'; Sha='0f75fac465130fed3ea54099d296ad79b0d044cbf11ec37dd1540a09c139d57d'; Name='Schema informe V2-C'},
    @{Rel='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_V1.json'; Sha='d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa'; Name='Propuesta semantica'},
    @{Rel='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_SCHEMA_V1.json'; Sha='f017a8a0081cc42f08af6381e7d47accb7a522ce89301ab9724d003a51c2dcf7'; Name='Schema propuesta'},
    @{Rel='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_PROPOSAL_REPORT_SCHEMA_V1.json'; Sha='57fc91fd8ee19a0f511692ef24e802c8df9c88e8eee73a7f30d14b3d5e3d7051'; Name='Schema informe propuesta'},
    @{Rel='definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_V1.json'; Sha='de44f159c95f31d034fe8356f650b5be320cb5fb1555197073d07875cf0cf1f9'; Name='Contrato sidecar editorial'},
    @{Rel='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_CAPABILITY_MATRIX_V1.json'; Sha='3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75'; Name='Matriz de capacidad'},
    @{Rel='definitions/c11d/production/D_RENDERER_POLICY_DECISION_DOCKET_V1.json'; Sha='e008217bd57303b638e13329d21e5ae56ee3b4efef790566e3702c89ee41a83f'; Name='Policy docket'}
)
foreach ($Pin in $Pins) { Assert-Sha (Join-Path $Root ($Pin.Rel.Replace('/','\'))) $Pin.Sha $Pin.Name }

$AuditPath = Join-Path $Root 'tools\c11d\d9\audit_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.py'
$TestPath = Join-Path $Root 'tools\c11d\d9\test_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.py'
$SchemaPath = Join-Path $Root 'definitions\c11d\production\D_RENDERER_PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_AUDIT_SCHEMA_V1.json'
Assert-Sha $TestPath 'b5bbf67e071a5eac7e1aeb6eda002782914b1d4790ebce7b825fd774050c23f9' 'Tests Fase O'
Assert-Sha $SchemaPath 'a44ff98c7b3e82601f562dee764e0009c6377747807083ba608080871282d67d' 'Schema informe Fase O'

$RuntimeMarkerPath = Join-Path $env:TEMP 'C11D_V2C_SOURCE_FRAME_RUNTIME_20261027.completed.json'
$AcceptanceMarkerPath = Join-Path $env:TEMP 'C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_20261027.completed.json'
$RuntimeMarker = Read-JsonFile $RuntimeMarkerPath
$AcceptanceMarker = Read-JsonFile $AcceptanceMarkerPath
if ([string]$RuntimeMarker.schema -ne 'C11D-V2C-SOURCE-FRAME-RUNTIME-COMPLETION-V1' -or
    [string]$RuntimeMarker.runtime_status -ne 'PASS_SOURCE_FRAME_ROUTE_ONLY' -or
    [string]$RuntimeMarker.runtime_report_sha256 -ne $ExpectedRuntimeReportSha -or
    [string]$RuntimeMarker.runtime_stdout_sha256 -ne $ExpectedRuntimeStdoutSha -or
    [string]$RuntimeMarker.test_stdout_sha256 -ne $ExpectedTestStdoutSha -or
    [string]$RuntimeMarker.test_stderr_sha256 -ne $EmptySha -or
    [string]$RuntimeMarker.runtime_stderr_sha256 -ne $EmptySha -or
    [string]$RuntimeMarker.source_pin_count -ne '81' -or
    [string]$RuntimeMarker.planner_invocations -ne '9/9' -or
    [string]$RuntimeMarker.godot_runtime_process_invocations -ne '18/18' -or
    [string]$RuntimeMarker.accepted_selectors -ne '9/9' -or
    [string]$RuntimeMarker.process_evidence_files_verified -ne '36/36' -or
    [string]$RuntimeMarker.frozen_c11c_manifest -ne 'UNCHANGED' -or
    [string]$RuntimeMarker.renderer -ne 'OFF' -or $RuntimeMarker.media_created -ne $false -or
    $RuntimeMarker.payload_materialized -ne $false -or $RuntimeMarker.candidate_input_admissible -ne $false -or
    [string]$RuntimeMarker.D4_8 -ne 'BLOCKED' -or [string]$RuntimeMarker.release_authority -ne 'NONE') {
    throw 'Marker de runtime Fase N no coincide con la aceptacion conocida.'
}
if ([string]$AcceptanceMarker.schema -ne 'C11D-V2C-SOURCE-FRAME-RUNTIME-ACCEPTANCE-COMPLETION-V1' -or
    [string]$AcceptanceMarker.status -ne 'PASS_SOURCE_FRAME_ROUTE_ONLY' -or
    [string]$AcceptanceMarker.report_sha256 -ne $ExpectedRuntimeReportSha -or
    [string]$AcceptanceMarker.checkpoint_sha256 -ne $ExpectedCheckpointSha -or
    [string]$AcceptanceMarker.ledger_sha256 -ne $ExpectedLedgerSha -or
    [string]$AcceptanceMarker.acceptance_record_sha256 -ne $ExpectedAcceptanceRecordSha -or
    [string]$AcceptanceMarker.source_pins -ne '81/81' -or
    [string]$AcceptanceMarker.planner_invocations -ne '9/9' -or
    [string]$AcceptanceMarker.godot_runtime_processes -ne '18/18' -or
    [string]$AcceptanceMarker.selectors -ne '9/9' -or
    [string]$AcceptanceMarker.process_evidence_files -ne '36/36' -or
    [string]$AcceptanceMarker.release_authority -ne 'NONE') {
    throw 'Marker de aceptacion documental Fase N no coincide.'
}
$ReportPath = [IO.Path]::GetFullPath([string]$RuntimeMarker.runtime_report_path)
if ($ReportPath -ne [IO.Path]::GetFullPath([string]$AcceptanceMarker.report_path)) { throw 'Los markers de Fase N referencian informes distintos.' }
Assert-Sha $ReportPath $ExpectedRuntimeReportSha 'Informe runtime de Fase N'

$PythonCommand = Get-Command python.exe -ErrorAction Stop
$PythonPath = $PythonCommand.Source
$RunId = [Guid]::NewGuid().ToString('N')
$RunRoot = Join-Path $env:TEMP ('C11D_PHASE_O_SEMANTIC_CROSSWALK_20261027_' + $RunId)
$ReportDirectory = Join-Path $RunRoot 'reports'
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
$TestStdoutPath = Join-Path $RunRoot 'phase_o_tests.stdout.txt'
$TestStderrPath = Join-Path $RunRoot 'phase_o_tests.stderr.txt'
$AuditStdoutPath = Join-Path $RunRoot 'phase_o_audit.stdout.txt'
$AuditStderrPath = Join-Path $RunRoot 'phase_o_audit.stderr.txt'

$TestProcess = Start-Process -FilePath $PythonPath -ArgumentList ('"' + $TestPath + '"') -WorkingDirectory $Root -RedirectStandardOutput $TestStdoutPath -RedirectStandardError $TestStderrPath -Wait -PassThru -NoNewWindow
$TestStdout = Read-ProcessText $TestStdoutPath
$TestStderr = Read-ProcessText $TestStderrPath
$TestStdoutSha = Get-FileSha256 $TestStdoutPath
$TestStderrSha = Get-FileSha256 $TestStderrPath
if ($TestProcess.ExitCode -ne 0 -or -not $TestStdout.Contains('PHASE_O_UNIT_TESTS=28/28')) {
    Write-Host $TestStdout
    if ($TestStderr.Length -gt 0) { Write-Host $TestStderr }
    throw "Tests de la auditoria Phase O fallaron. Exit=$($TestProcess.ExitCode); logs=$RunRoot"
}

$AuditArgs = '"' + $AuditPath + '" --root "' + $Root + '" --runtime-marker "' + $RuntimeMarkerPath + '" --acceptance-marker "' + $AcceptanceMarkerPath + '" --output-dir "' + $ReportDirectory + '"'
$AuditProcess = Start-Process -FilePath $PythonPath -ArgumentList $AuditArgs -WorkingDirectory $Root -RedirectStandardOutput $AuditStdoutPath -RedirectStandardError $AuditStderrPath -Wait -PassThru -NoNewWindow
$AuditStdout = Read-ProcessText $AuditStdoutPath
$AuditStderr = Read-ProcessText $AuditStderrPath
$AuditStdoutSha = Get-FileSha256 $AuditStdoutPath
$AuditStderrSha = Get-FileSha256 $AuditStderrPath
if ($AuditProcess.ExitCode -ne 0 -or -not $AuditStdout.Contains('C11D_PHASE_O_SOURCE_FRAME_SEMANTIC_CROSSWALK=PASS')) {
    Write-Host $TestStdout
    Write-Host $AuditStdout
    if ($AuditStderr.Length -gt 0) { Write-Host $AuditStderr }
    throw "Auditoria Phase O fail-closed. No se modifico checkpoint/ledger; conserva el directorio $RunRoot"
}

$ReportPathOut = Join-Path $ReportDirectory 'phase_o_crosswalk_report.json'
$CsvPathOut = Join-Path $ReportDirectory 'phase_o_field_crosswalk.csv'
$SummaryPathOut = Join-Path $ReportDirectory 'phase_o_summary.md'
$OutputManifestPath = Join-Path $ReportDirectory 'output_manifest.json'
foreach ($Path in @($ReportPathOut, $CsvPathOut, $SummaryPathOut, $OutputManifestPath)) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Salida audit incompleta: $Path" }
}
$Crosswalk = Read-JsonFile $ReportPathOut
$OutputManifest = Read-JsonFile $OutputManifestPath
if ([string]$Crosswalk.status -ne 'PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL' -or
    [int]$Crosswalk.summary.selectors_verified -ne 9 -or
    [int]$Crosswalk.summary.runtime_receipts_verified -ne 18 -or
    [int]$Crosswalk.summary.process_evidence_files_verified -ne 36 -or
    [string]$Crosswalk.summary.stable_custom_data_candidate_occurrences -ne '6/6' -or
    [string]$Crosswalk.summary.static_source_pointers_present -ne '3/3' -or
    [int]$Crosswalk.summary.timebase_conflicts_unresolved -ne 2 -or
    [int]$Crosswalk.summary.approved_bindings -ne 0 -or
    [int]$Crosswalk.summary.approved_custom_data_bindings -ne 0 -or
    [int]$Crosswalk.summary.approved_renderer_projection_bindings -ne 0 -or
    [int]$Crosswalk.summary.editorial_fields_visually_consumed -ne 0 -or
    [string]$Crosswalk.summary.release_authority -ne 'NONE') {
    throw "Crosswalk report post-check did not satisfy Phase O scope. No docs/ledger updated; output=$RunRoot"
}
$ExpectedJsonOutputSha = [string]$OutputManifest.outputs.PSObject.Properties['phase_o_crosswalk_report.json'].Value
$ExpectedCsvOutputSha = [string]$OutputManifest.outputs.PSObject.Properties['phase_o_field_crosswalk.csv'].Value
$ExpectedMdOutputSha = [string]$OutputManifest.outputs.PSObject.Properties['phase_o_summary.md'].Value
if ((Get-FileSha256 $ReportPathOut) -ne $ExpectedJsonOutputSha -or
    (Get-FileSha256 $CsvPathOut) -ne $ExpectedCsvOutputSha -or
    (Get-FileSha256 $SummaryPathOut) -ne $ExpectedMdOutputSha) {
    throw 'Output manifest hashes do not match Phase O reports.'
}

# Source pins and governance must remain unchanged after the audit.
Assert-Sha $FrozenPath $ExpectedFrozenSha 'Manifiesto C11-C despues de auditoria'
Assert-Sha (Join-Path $Root 'docs\current\d\D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md') $ExpectedCheckpointSha 'Checkpoint despues de auditoria'
Assert-Sha (Join-Path $Root 'docs\current\d\C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md') $ExpectedLedgerSha 'Ledger despues de auditoria'

$CompletionData = [ordered]@{
    schema = 'C11D-PHASE-O-SOURCE-FRAME-SEMANTIC-CROSSWALK-COMPLETION-V1'
    completed_utc = (Get-Date).ToUniversalTime().ToString('o')
    status = [string]$Crosswalk.status
    audit_report_path = $ReportPathOut
    audit_report_sha256 = Get-FileSha256 $ReportPathOut
    field_crosswalk_path = $CsvPathOut
    field_crosswalk_sha256 = Get-FileSha256 $CsvPathOut
    summary_path = $SummaryPathOut
    summary_sha256 = Get-FileSha256 $SummaryPathOut
    output_manifest_path = $OutputManifestPath
    output_manifest_sha256 = Get-FileSha256 $OutputManifestPath
    test_exit_code = [int]$TestProcess.ExitCode
    test_result = '28/28'
    test_stdout_sha256 = $TestStdoutSha
    test_stderr_sha256 = $TestStderrSha
    audit_exit_code = [int]$AuditProcess.ExitCode
    audit_stdout_sha256 = $AuditStdoutSha
    audit_stderr_sha256 = $AuditStderrSha
    runtime_report_sha256 = $ExpectedRuntimeReportSha
    selectors = '9/9'
    receipts = '18/18'
    evidence_files = '36/36'
    stable_custom_data_candidates = '6/6'
    static_source_pointers = '3/3'
    unresolved_timebase_conflicts = 2
    approved_bindings = 0
    approved_custom_data_bindings = 0
    approved_renderer_projection_bindings = 0
    editorial_fields_visually_consumed = 0
    runtime_invocations = 0
    project_source_writes = 0
    output_directory = $RunRoot
    frozen_c11c_manifest = 'UNCHANGED'
    renderer = 'OFF'; media_created = $false; payload_materialized = $false
    candidate_input_admissible = $false; D4_8 = 'BLOCKED'; release_authority = 'NONE'
}
$CompletionMarker = Join-Path $env:TEMP 'C11D_PHASE_O_SEMANTIC_CROSSWALK_20261027.completed.json'
if (Test-Path -LiteralPath $CompletionMarker) { throw "Completion marker Phase O aparecio durante la ejecucion: $CompletionMarker" }
Write-Utf8NoBom $CompletionMarker (($CompletionData | ConvertTo-Json -Depth 12) + "`n")

Write-Host $TestStdout
Write-Host $AuditStdout
Write-Host 'C11D_PHASE_O_LAUNCHER=PASS'
Write-Host ('TEST_STDOUT_SHA256=' + $TestStdoutSha)
Write-Host ('TEST_STDERR_SHA256=' + $TestStderrSha)
Write-Host ('AUDIT_STDOUT_SHA256=' + $AuditStdoutSha)
Write-Host ('AUDIT_STDERR_SHA256=' + $AuditStderrSha)
Write-Host ('COMPLETION_MARKER=' + $CompletionMarker)
Write-Host ('LOG_DIRECTORY=' + $RunRoot)
Write-Host ('REPORT_PATH=' + $ReportPathOut)
Write-Host ('REPORT_SHA256=' + (Get-FileSha256 $ReportPathOut))
Write-Host ('CSV_PATH=' + $CsvPathOut)
Write-Host ('CSV_SHA256=' + (Get-FileSha256 $CsvPathOut))
Write-Host ('SUMMARY_PATH=' + $SummaryPathOut)
Write-Host ('SUMMARY_SHA256=' + (Get-FileSha256 $SummaryPathOut))
Write-Host 'RUNTIME_INVOCATIONS=0'
Write-Host 'PROJECT_SOURCE_WRITES=0'
Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
Write-Host 'RENDERER=OFF'
Write-Host 'MEDIA_CREATED=false'
Write-Host 'PAYLOAD_MATERIALIZED=false'
Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
Write-Host 'D4.8=BLOCKED'
Write-Host 'RELEASE_AUTHORITY=NONE'
