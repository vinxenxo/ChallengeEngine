# C11-D Phase O evidence acceptance and guarded documentation write-back.
# Windows PowerShell 5.1; no runtime invocation.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$Root = [IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\')
$ExpectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
if (-not [string]::Equals($Root, $ExpectedRoot, [StringComparison]::OrdinalIgnoreCase)) { throw "Unexpected repository root: $Root" }

function Get-FileSha([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Required file missing: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-Sha([string]$Path, [string]$Expected, [string]$Label) {
    $Actual = Get-FileSha $Path
    if ($Actual -ne $Expected) { throw "$Label SHA mismatch. Actual=$Actual Expected=$Expected" }
}
function Read-Json([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Required JSON missing: $Path" }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}
function Get-CountExact([string]$Text, [string]$Needle) {
    if ([string]::IsNullOrEmpty($Needle)) { throw 'Empty search token.' }
    return ([regex]::Matches($Text, [regex]::Escape($Needle))).Count
}
function Write-Utf8NoBom([string]$Path, [string]$Text) {
    $Encoding = New-Object System.Text.UTF8Encoding($false)
    [IO.File]::WriteAllText($Path, $Text, $Encoding)
}
function Assert-GovernanceLocks($Locks) {
    $Expected = [ordered]@{
        renderer='OFF'; media_created=$false; payload_materialized=$false
        candidate_input_admissible=$false; seed_domains_complete_for_candidate_input=$false
        automatic_seed_generation=$false; master_seed='NOT_ADOPTED'
        'D4.8'='BLOCKED'; 'D9.10'='PREPARE_ONLY'; 'D9.14'='BLOCKED'; 'D9.16'='BLOCKED'
        'D9.17'='BLOCKED_NO_GO'; D10='BLOCKED_FOR_PROMOTION'; baseline_approval='MISSING'
        freeze_eligible=$false; release_authority='NONE'
    }
    foreach ($Name in $Expected.Keys) {
        $LockProperty = $Locks.PSObject.Properties[$Name]
        if ($null -eq $LockProperty) { throw "Governance lock missing: $Name" }
        if ($LockProperty.Value -cne $Expected[$Name]) { throw "Governance lock changed: $Name" }
    }
}

$FrozenSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$FrozenBytes = 796318
$ExpectedCheckpointSha = '9cccc148927a950a14f76a9e7afb13c1e0d8b8fa1f3ac556a7f01c7244985f2d'
$ExpectedLedgerSha = '7f44a13f633bd8847cfc60f24d635df6dfe17fb8024af38b8bf2404b68d2fa28'
$ExpectedPhaseNAcceptanceSha = 'a0faf6e6ddf145b69b649de45366bfadf0947c7b55a78444c4d546fe3efdeb96'
$ExpectedRuntimeReportSha = '7f96c9aec3849212299afbcabe7fd3045fee815807c9cafe555ad8cb947f91f2'
$ExpectedPhaseOReportSha = '799d69eba67543b5254016dd3ebc9ac468a2a69f541acd99ee7476c1f53eb0bf'
$ExpectedCsvSha = 'a9a38bb2e9ebe01936074f23d9d3059cf3593622f357e3106c75e376a270b0ce'
$ExpectedSummarySha = '36eb3a9aff52e29b727e217cc276b42bafea7e4733ebbdbb3bfb7af12225005e'
$ExpectedOutputManifestSha = '3f9fda179304cdbded1993afccd097d8eaef93a7f158f92167626ecebce085a0'
$ExpectedTestStdoutSha = 'fe6e6a91d2cfd7747eb9a8844d44d2a93b63d8ee2a172a5b3098e2ab0b7e24c9'
$EmptySha = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
$ExpectedAuditStdoutSha = '1192a65afe2adf38a31bcbad55f2d36c9964a042d9c433fd137ab21458cd534d'
$ExpectedAuditSourceSha = '835ea27646209579900aaaed25272c01bbf92eee75c1fe87128149e2f2ae302f'
$ExpectedTestSourceSha = 'b5bbf67e071a5eac7e1aeb6eda002782914b1d4790ebce7b825fd774050c23f9'
$ExpectedRunnerSha = '4625d36d5673dbe8f2f759fe5b6a1a1f98ce138c077bb6a3f9dbf04203a1b80b'
$ExpectedSchemaSha = 'a44ff98c7b3e82601f562dee764e0009c6377747807083ba608080871282d67d'

$CompletionMarkerPath = Join-Path $env:TEMP 'C11D_PHASE_O_SEMANTIC_CROSSWALK_20261027.completed.json'
$OverlayV2MarkerPath = Join-Path $env:TEMP 'C11D_PHASE_O_CROSSWALK_V2_20261027.completed.json'
$OverlayV3MarkerPath = Join-Path $env:TEMP 'C11D_PHASE_O_RESOLVER_FIX_V3_20261027.completed.json'
$OverlayV4MarkerPath = Join-Path $env:TEMP 'C11D_PHASE_O_RUNNER_PIN_V4_20261027.completed.json'
$WritebackMarkerPath = Join-Path $env:TEMP 'C11D_PHASE_O_CROSSWALK_ACCEPTANCE_20261027.completed.json'
if (Test-Path -LiteralPath $WritebackMarkerPath) { throw "Phase O acceptance already complete: $WritebackMarkerPath" }

# Verify all overlay stages and the Phase N baseline before reading audit outputs.
$OverlayV2 = Read-Json $OverlayV2MarkerPath
if ([string]$OverlayV2.schema -ne 'C11D-PHASE-O-CROSSWALK-V2-OVERLAY-COMPLETION-V1' -or
    [string]$OverlayV2.overlay_id -ne 'C11D_PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_OVERLAY_20261027_V2' -or
    [string]$OverlayV2.add_only_files -ne '5/5_HASH_VERIFIED' -or
    [string]$OverlayV2.phase_n_report_sha256 -ne $ExpectedRuntimeReportSha -or
    [string]$OverlayV2.frozen_c11c_manifest -ne 'UNCHANGED') { throw 'Phase O V2 overlay marker mismatch.' }
$OverlayV3 = Read-Json $OverlayV3MarkerPath
if ([string]$OverlayV3.schema -ne 'C11D-PHASE-O-RESOLVER-FIX-V3-COMPLETION-V1' -or
    [string]$OverlayV3.overlay_id -ne 'C11D_PHASE_O_RESOLVER_SIGNATURE_FIX_OVERLAY_20261027_V3' -or
    [string]$OverlayV3.guarded_replacements -ne '3/3_HASH_VERIFIED' -or
    [string]$OverlayV3.add_only_files -ne '1/1_HASH_VERIFIED' -or
    [string]$OverlayV3.phase_n_report_sha256 -ne $ExpectedRuntimeReportSha -or
    [string]$OverlayV3.frozen_c11c_manifest -ne 'UNCHANGED') { throw 'Phase O V3 overlay marker mismatch.' }
$OverlayV4 = Read-Json $OverlayV4MarkerPath
if ([string]$OverlayV4.schema -ne 'C11D-PHASE-O-RUNNER-TEST-PIN-V4-COMPLETION-V1' -or
    [string]$OverlayV4.overlay_id -ne 'C11D_PHASE_O_RUNNER_TEST_PIN_CORRECTION_OVERLAY_20261027_V4' -or
    [string]$OverlayV4.guarded_replacements -ne '1/1_HASH_VERIFIED' -or
    [string]$OverlayV4.add_only_files -ne '1/1_HASH_VERIFIED' -or
    [string]$OverlayV4.test_sha256 -ne $ExpectedTestSourceSha -or
    [string]$OverlayV4.runner_sha256 -ne $ExpectedRunnerSha -or
    [string]$OverlayV4.frozen_c11c_manifest -ne 'UNCHANGED') { throw 'Phase O V4 overlay marker mismatch.' }

$Marker = Read-Json $CompletionMarkerPath
$MarkerChecks = @{
    schema='C11D-PHASE-O-SOURCE-FRAME-SEMANTIC-CROSSWALK-COMPLETION-V1'
    status='PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL'
    audit_report_sha256=$ExpectedPhaseOReportSha
    field_crosswalk_sha256=$ExpectedCsvSha
    summary_sha256=$ExpectedSummarySha
    output_manifest_sha256=$ExpectedOutputManifestSha
    test_result='28/28'
    test_stdout_sha256=$ExpectedTestStdoutSha
    test_stderr_sha256=$EmptySha
    audit_stdout_sha256=$ExpectedAuditStdoutSha
    audit_stderr_sha256=$EmptySha
    runtime_report_sha256=$ExpectedRuntimeReportSha
    selectors='9/9'; receipts='18/18'; evidence_files='36/36'
    stable_custom_data_candidates='6/6'; static_source_pointers='3/3'
    unresolved_timebase_conflicts=2; approved_bindings=0; approved_custom_data_bindings=0
    approved_renderer_projection_bindings=0; editorial_fields_visually_consumed=0
    runtime_invocations=0; project_source_writes=0; frozen_c11c_manifest='UNCHANGED'
    renderer='OFF'; media_created=$false; payload_materialized=$false
    candidate_input_admissible=$false; D4_8='BLOCKED'; release_authority='NONE'
}
foreach ($Name in $MarkerChecks.Keys) {
    if ($Marker.PSObject.Properties.Name -notcontains $Name -or $Marker.$Name -cne $MarkerChecks[$Name]) {
        throw "Phase O completion marker mismatch: $Name"
    }
}
if ([int]$Marker.test_exit_code -ne 0 -or [int]$Marker.audit_exit_code -ne 0) { throw 'Phase O process exit code was not zero.' }

$RunDirectory = [IO.Path]::GetFullPath([string]$Marker.output_directory)
$TempPrefix = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\') + '\'
if (-not $RunDirectory.StartsWith($TempPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'Phase O output directory outside TEMP.' }
$ReportsDirectory = Join-Path $RunDirectory 'reports'
$ReportPath = [IO.Path]::GetFullPath([string]$Marker.audit_report_path)
$CsvPath = [IO.Path]::GetFullPath([string]$Marker.field_crosswalk_path)
$SummaryPath = [IO.Path]::GetFullPath([string]$Marker.summary_path)
$OutputManifestPath = [IO.Path]::GetFullPath([string]$Marker.output_manifest_path)
if ($ReportPath -ne [IO.Path]::GetFullPath((Join-Path $ReportsDirectory 'phase_o_crosswalk_report.json')) -or
    $CsvPath -ne [IO.Path]::GetFullPath((Join-Path $ReportsDirectory 'phase_o_field_crosswalk.csv')) -or
    $SummaryPath -ne [IO.Path]::GetFullPath((Join-Path $ReportsDirectory 'phase_o_summary.md')) -or
    $OutputManifestPath -ne [IO.Path]::GetFullPath((Join-Path $ReportsDirectory 'output_manifest.json'))) {
    throw 'Phase O output paths do not match expected report directory.'
}
Assert-Sha $ReportPath $ExpectedPhaseOReportSha 'Phase O JSON report'
Assert-Sha $CsvPath $ExpectedCsvSha 'Phase O CSV crosswalk'
Assert-Sha $SummaryPath $ExpectedSummarySha 'Phase O Markdown summary'
Assert-Sha $OutputManifestPath $ExpectedOutputManifestSha 'Phase O output manifest'

$TestStdoutPath = Join-Path $RunDirectory 'phase_o_tests.stdout.txt'
$TestStderrPath = Join-Path $RunDirectory 'phase_o_tests.stderr.txt'
$AuditStdoutPath = Join-Path $RunDirectory 'phase_o_audit.stdout.txt'
$AuditStderrPath = Join-Path $RunDirectory 'phase_o_audit.stderr.txt'
Assert-Sha $TestStdoutPath $ExpectedTestStdoutSha 'Phase O test stdout'
Assert-Sha $TestStderrPath $EmptySha 'Phase O test stderr'
Assert-Sha $AuditStdoutPath $ExpectedAuditStdoutSha 'Phase O audit stdout'
Assert-Sha $AuditStderrPath $EmptySha 'Phase O audit stderr'

$Report = Read-Json $ReportPath
$OutputManifest = Read-Json $OutputManifestPath
if ([string]$Report.schema -ne 'C11D-PHASE-O-SOURCE-FRAME-SEMANTIC-BINDING-CROSSWALK-AUDIT-REPORT-V1' -or
    [string]$Report.schema_version -ne '1.0' -or
    [string]$Report.status -ne 'PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL') { throw 'Phase O report schema/status mismatch.' }
$Summary = $Report.summary
$SummaryChecks = @{
    selectors_verified=9; runtime_receipts_verified=18; process_evidence_files_verified=36
    asset_source_pins_verified=15; base_frame_field_rows=54
    stable_custom_data_candidate_occurrences='6/6'; static_source_pointers_present='3/3'
    timebase_conflicts_unresolved=2; challenge_editorial_sidecar_fields=6
    editorial_sidecar_slots_across_all_content_types=14; approved_bindings=0
    approved_custom_data_bindings=0; approved_renderer_projection_bindings=0
    editorial_fields_visually_consumed=0; custom_data_values_serialized=$false
    renderer='OFF'; media_created=$false; payload_materialized=$false
    candidate_input_admissible=$false; release_authority='NONE'
}
foreach ($Name in $SummaryChecks.Keys) {
    if ($Summary.PSObject.Properties.Name -notcontains $Name -or $Summary.$Name -cne $SummaryChecks[$Name]) {
        throw "Phase O report summary mismatch: $Name"
    }
}
if (@($Report.selector_crosswalk).Count -ne 9 -or @($Report.timebase_conflicts).Count -ne 2 -or
    @($Report.temporal_policy_fields).Count -ne 2 -or @($Report.asset_source_pins).Count -ne 15 -or
    @($Report.process_evidence_sha256.PSObject.Properties).Count -ne 36) { throw 'Phase O report array counts mismatch.' }
$ExpectedChallengeIds = @('CHALLENGE_001','CHALLENGE_002','CHALLENGE_003','CHALLENGE_004','CHALLENGE_005','CHALLENGE_006','CHALLENGE_007','CHALLENGE_008','CHALLENGE_009')
for ($Index = 0; $Index -lt 9; $Index++) {
    $Row = $Report.selector_crosswalk[$Index]
    if ([string]$Row.challenge_id -ne $ExpectedChallengeIds[$Index] -or
        [string]$Row.selector_status -ne 'ACCEPTED_SOURCE_FRAME_ONLY' -or
        $Row.repeat_agreement -ne $true -or @($Row.receipt_runs).Count -ne 2) {
        throw "Phase O selector row invalid: index=$Index"
    }
}
foreach ($Conflict in $Report.timebase_conflicts) {
    if (@('CHALLENGE_008','CHALLENGE_009') -notcontains [string]$Conflict.challenge_id -or
        [double]$Conflict.declared_total_seconds -ne 11.0 -or
        [double]$Conflict.phase_duration_sum_seconds -ne 12.0 -or
        [string]$Conflict.status -ne 'UNRESOLVED_BLOCKED_FROM_RUNTIME_MATERIALIZATION' -or
        $Conflict.decision_made -ne $false) { throw 'Phase O timebase conflict data changed.' }
}
$ExpectedTemporal = @{
    winning_frame='temporal_anchor'
    close_calls='episode_counter'
}
foreach ($Temporal in $Report.temporal_policy_fields) {
    $Name = [string]$Temporal.field
    if (-not $ExpectedTemporal.ContainsKey($Name) -or [string]$Temporal.category -ne $ExpectedTemporal[$Name] -or
        $Temporal.binding_approved -ne $false -or $Temporal.runtime_receipt_serialized -ne $false) {
        throw "Temporal policy mismatch: $Name"
    }
}
Assert-GovernanceLocks $Report.governance_locks
if ($Report.invariants.winning_frame_is_only_challenge_temporal_anchor -ne $true -or
    $Report.invariants.close_calls_is_episode_counter_only -ne $true -or
    $Report.invariants.custom_data_values_serialized -ne $false -or
    $Report.invariants.target_x_remains_scalar -ne $true -or
    $Report.invariants.challenge_004_v1_regression_modified -ne $false -or
    $Report.invariants.editorial_sidecar_visual_consumption -ne 'NOT_IMPLEMENTED' -or
    $Report.invariants.renderer_dispatch -ne $false -or
    $Report.invariants.payload_persisted -ne $false -or
    $Report.invariants.viewport_capture -ne $false -or
    $Report.invariants.media_or_video_created -ne $false -or
    $Report.invariants.source_mutation -ne $false) { throw 'Phase O report invariants changed.' }
if ([string]$Report.next_safe_increment -notlike '*six custom_data candidates*' -or
    [string]$Report.next_safe_increment -notlike '*do not bind or serialize*') { throw 'Phase O next-safe-increment guidance changed.' }

if ([string]$OutputManifest.schema -ne 'C11D-PHASE-O-CROSSWALK-OUTPUT-MANIFEST-V1' -or
    [string]$OutputManifest.status -ne 'PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL' -or
    [string]$OutputManifest.runtime_report_sha256 -ne $ExpectedRuntimeReportSha -or
    [int]$OutputManifest.runtime_invocations -ne 0 -or
    [int]$OutputManifest.project_files_written -ne 0 -or
    [int]$OutputManifest.binding_approval_count -ne 0) { throw 'Phase O output manifest contract mismatch.' }
$OutJsonSha = [string]$OutputManifest.outputs.PSObject.Properties['phase_o_crosswalk_report.json'].Value
$OutCsvSha = [string]$OutputManifest.outputs.PSObject.Properties['phase_o_field_crosswalk.csv'].Value
$OutMdSha = [string]$OutputManifest.outputs.PSObject.Properties['phase_o_summary.md'].Value
if ($OutJsonSha -ne $ExpectedPhaseOReportSha -or $OutCsvSha -ne $ExpectedCsvSha -or $OutMdSha -ne $ExpectedSummarySha) {
    throw 'Phase O report hashes do not match output manifest.'
}

# Validate the pinned sources and current Phase N documentation before write-back.
$FrozenPath = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
Assert-Sha $FrozenPath $FrozenSha 'Frozen C11-C manifest'
if ((Get-Item -LiteralPath $FrozenPath).Length -ne $FrozenBytes) { throw 'Frozen C11-C manifest byte count changed.' }
$CheckpointRel = 'docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md'
$LedgerRel = 'docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md'
$PhaseNAcceptanceRel = 'docs/current/d/C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_20261027_V1.md'
$CheckpointPath = Join-Path $Root ($CheckpointRel.Replace('/','\'))
$LedgerPath = Join-Path $Root ($LedgerRel.Replace('/','\'))
$PhaseNAcceptancePath = Join-Path $Root ($PhaseNAcceptanceRel.Replace('/','\'))
Assert-Sha $CheckpointPath $ExpectedCheckpointSha 'Phase N checkpoint'
Assert-Sha $LedgerPath $ExpectedLedgerSha 'Phase N ledger'
Assert-Sha $PhaseNAcceptancePath $ExpectedPhaseNAcceptanceSha 'Phase N acceptance record'
Assert-Sha (Join-Path $Root 'tools\c11d\d9\audit_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.py') $ExpectedAuditSourceSha 'Phase O audit code'
Assert-Sha (Join-Path $Root 'tools\c11d\d9\test_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.py') $ExpectedTestSourceSha 'Phase O test code'
Assert-Sha (Join-Path $Root 'tools\c11d\d9\run_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.ps1') $ExpectedRunnerSha 'Phase O launcher'
Assert-Sha (Join-Path $Root 'definitions\c11d\production\D_RENDERER_PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_AUDIT_SCHEMA_V1.json') $ExpectedSchemaSha 'Phase O schema'

$AcceptanceRel = 'docs/current/d/C11D_PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_ACCEPTANCE_20261027_V1.md'
$AcceptancePath = Join-Path $Root ($AcceptanceRel.Replace('/','\'))
if (Test-Path -LiteralPath $AcceptancePath) { throw "Phase O acceptance record already exists: $AcceptancePath" }
$PendingStatus = 'V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PASS; V2C_SOURCE_FRAME_RUNTIME_PASS; PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_PENDING'
$AcceptedStatus = 'V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PASS; V2C_SOURCE_FRAME_RUNTIME_PASS; PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_PASS; PHASE_P_SOURCE_VALUE_FRAME_VALUE_PROVENANCE_PENDING'
$CheckpointText = [IO.File]::ReadAllText($CheckpointPath, [Text.Encoding]::UTF8)
$LedgerText = [IO.File]::ReadAllText($LedgerPath, [Text.Encoding]::UTF8)
if ((Get-CountExact $CheckpointText $PendingStatus) -ne 2) { throw 'Expected two Phase O pending tokens in checkpoint; no write-back.' }
$OldPhaseMarker = 'PHASE_K_CHALLENGE_COLLISION_EXPANSION_PASS; PHASE_L_V2B_STATIC_TESTS_PASS; PHASE_M_V2B_RUNTIME_MATRIX_PASS; PHASE_N_V2C_SOURCE_FRAME_RUNTIME_PASS; NEXT_PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK'
if ((Get-CountExact $LedgerText $OldPhaseMarker) -ne 1) { throw 'Phase O ledger marker mismatch; no write-back.' }
$ActionLines = @([regex]::Split($LedgerText, "\r\n|\n|\r") | Where-Object { $_.StartsWith('**Pr') -and $_.Contains('source-frame') -and $_.Contains('binding') })
if ($ActionLines.Count -ne 1) { throw 'Cannot identify exactly one Phase O next-action line; no write-back.' }
$OldAction = [string]$ActionLines[0]
$NewAction = [regex]::Replace($OldAction, ':\*\*.*$', ':** prepare a narrow source-value versus frame-value provenance test for the six custom_data candidates; do not bind or serialize them until separate approval and dedicated tests pass.')
if ($NewAction -eq $OldAction -or $NewAction -notlike '*six custom_data candidates*') { throw 'Cannot transform the Phase O action line safely.' }
$NewPhaseMarker = 'PHASE_K_CHALLENGE_COLLISION_EXPANSION_PASS; PHASE_L_V2B_STATIC_TESTS_PASS; PHASE_M_V2B_RUNTIME_MATRIX_PASS; PHASE_N_V2C_SOURCE_FRAME_RUNTIME_PASS; PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_PASS; NEXT_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE'

$PhaseRecord = @"

### Phase O - Source-frame to semantic binding crosswalk (27-10-2026; Windows PASS; read-only)

- Phase O tests: 28/28; test stdout SHA-256 $ExpectedTestStdoutSha; test stderr SHA-256 $EmptySha (empty).
- Audit status: `PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL`; runtime invocation count 0; project source writes 0.
- Runtime input lineage: accepted V2-C report SHA-256 $ExpectedRuntimeReportSha; accepted source-frame route only, no Godot runtime re-execution in Phase O.
- Audit JSON report SHA-256 $ExpectedPhaseOReportSha; field CSV SHA-256 $ExpectedCsvSha; Markdown summary SHA-256 $ExpectedSummarySha; output manifest SHA-256 $ExpectedOutputManifestSha.
- Coverage: selectors 9/9; source-frame receipts 18/18; process evidence files 36/36; asset source pins verified 15; base field-shape rows 54; stable custom_data presence/type candidates 6/6; static source pointers present 3/3; unresolved timebase conflicts 2.
- Semantic guardrails: `winning_frame` remains the sole Challenge temporal anchor; `close_calls` remains episode counter only. Receipt data confirms shape/presence/type and projection hashes, not actual per-frame values or renderer visual consumption. `target_x` remains scalar; CHALLENGE_004 V1 was not modified.
- Editorial sidecar remains sidecar-only: 14 fields/slots across content types, visually consumed 0; approved bindings 0, approved custom_data bindings 0, approved renderer projection bindings 0.
- CHALLENGE_008 and CHALLENGE_009 remain unresolved: declared duration 11 seconds versus phase sum 12 seconds. No temporal decision was made.
- Output folder: $RunDirectory; `phase_o_crosswalk_report.json`, `phase_o_field_crosswalk.csv`, `phase_o_summary.md` and `output_manifest.json` are outside the repository. This phase wrote no project source files.
- Detailed write-back hashes are held in the immutable Phase O write-back manifest under TEMP and recorded in the acceptance completion marker.

**Next phase:** Phase P - a narrow, read-only source-value versus frame-value provenance test for six custom_data candidates: CHALLENGE_003 `target_x` (scalar); CHALLENGE_005/006/007 `target_position`; CHALLENGE_008 `active_selection`; CHALLENGE_009 `displayed_count`. The test must distinguish config/source values from effective frame values, emit only types/presence and value hashes in its report, and never serialize all `FrameSnapshot.custom_data`. No binding is approved by this audit; approval requires a separate decision record and dedicated tests.

**Governance unchanged:** `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
"@

$CheckpointNew = $CheckpointText.Replace($PendingStatus, $AcceptedStatus)
$LedgerNew = $LedgerText.Replace($OldPhaseMarker, $NewPhaseMarker).Replace($OldAction, $NewAction)
if ((Get-CountExact $CheckpointNew $AcceptedStatus) -ne 2 -or
    (Get-CountExact $LedgerNew $NewPhaseMarker) -ne 1 -or
    (Get-CountExact $LedgerNew $NewAction) -ne 1) { throw 'Phase O document text postcondition failed before write-back.' }
$CheckpointNew = $CheckpointNew.Replace("`r`n", "`n")
$LedgerNew = ($LedgerNew + $PhaseRecord).Replace("`r`n", "`n")
$CheckpointNew = ($CheckpointNew.TrimEnd() + "`n")
$LedgerNew = ($LedgerNew.TrimEnd() + "`n")

$BackupDirectory = Join-Path $env:TEMP ('C11D_PHASE_O_ACCEPTANCE_BACKUP_' + [Guid]::NewGuid().ToString('N'))
$WritebackManifestPath = Join-Path $env:TEMP ('C11D_PHASE_O_ACCEPTANCE_WRITEBACK_' + [Guid]::NewGuid().ToString('N') + '.json')
$Utf8 = New-Object System.Text.UTF8Encoding($false)
New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
Copy-Item -LiteralPath $CheckpointPath -Destination (Join-Path $BackupDirectory 'checkpoint.before.md')
Copy-Item -LiteralPath $LedgerPath -Destination (Join-Path $BackupDirectory 'ledger.before.md')
$WrittenCheckpoint = $false; $WrittenLedger = $false; $WrittenAcceptance = $false; $WrittenManifest = $false
try {
    $WrittenCheckpoint = $true
    Write-Utf8NoBom $CheckpointPath $CheckpointNew
    $WrittenLedger = $true
    Write-Utf8NoBom $LedgerPath $LedgerNew
    $CheckpointAfterSha = Get-FileSha $CheckpointPath
    $LedgerAfterSha = Get-FileSha $LedgerPath

    $AcceptanceText = @"
# C11-D - Fase O acceptance: source-frame / semantic binding crosswalk

**Estado:** `WINDOWS_PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL`.

## Evidence verified

- Tests: `28/28`; stdout SHA-256 $ExpectedTestStdoutSha; stderr SHA-256 $EmptySha (empty).
- Audit report status: `PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL`.
- Report JSON: $ReportPath; SHA-256 $ExpectedPhaseOReportSha.
- Field CSV: $CsvPath; SHA-256 $ExpectedCsvSha.
- Summary Markdown: $SummaryPath; SHA-256 $ExpectedSummarySha.
- Output manifest: $OutputManifestPath; SHA-256 $ExpectedOutputManifestSha.
- Audit stdout SHA-256 $ExpectedAuditStdoutSha; stderr SHA-256 $EmptySha (empty).
- Coverage: selectors `9/9`; source-frame receipts `18/18`; process evidence files `36/36`; asset source pins `15`; base field-shape rows `54`; custom_data presence/type candidates stable `6/6`; static source pointers present `3/3`.
- Unresolved duration conflicts: `2` (`CHALLENGE_008` and `CHALLENGE_009`, 11-second declaration versus 12-second phase sum).

## Interpretation

This phase classifies field shape, source lineage and repeated receipt observations. It does not prove actual per-frame custom_data values, text drawing, pixels, renderer consumption or video output. `winning_frame` remains the sole Challenge temporal anchor; `close_calls` remains an episode counter only. The six custom_data candidates remain unapproved. Editorial sidecar visual consumption is still `0`; approved bindings, approved custom_data bindings and approved renderer projection bindings are all `0`.

## Documentation write-back

- Checkpoint: $CheckpointPath; before SHA-256 $ExpectedCheckpointSha; after SHA-256 $CheckpointAfterSha.
- Ledger: $LedgerPath; before SHA-256 $ExpectedLedgerSha; after SHA-256 $LedgerAfterSha.
- Backup directory: $BackupDirectory.
- Write-back manifest: $WritebackManifestPath (contains source/output hashes and exact before/after document pins).
- Phase O audit completion marker: $CompletionMarkerPath.

## Next action

Phase P: prepare a narrow, read-only source-value versus frame-value provenance test for the six custom_data candidates. Do not bind or serialize them until a separate decision record and dedicated tests are approved.

## Governance locks

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
"@
    $WrittenAcceptance = $true
    Write-Utf8NoBom $AcceptancePath (($AcceptanceText.TrimEnd()) + "`n")
    $AcceptanceAfterSha = Get-FileSha $AcceptancePath

    Assert-Sha $FrozenPath $FrozenSha 'Frozen C11-C manifest after write-back'
    if ((Get-Item -LiteralPath $FrozenPath).Length -ne $FrozenBytes) { throw 'Frozen C11-C manifest byte count changed during write-back.' }
    if ((Get-CountExact ([IO.File]::ReadAllText($CheckpointPath, [Text.Encoding]::UTF8)) $AcceptedStatus) -ne 2) { throw 'Checkpoint accepted status count incorrect after write-back.' }
    if ((Get-CountExact ([IO.File]::ReadAllText($LedgerPath, [Text.Encoding]::UTF8)) $NewPhaseMarker) -ne 1) { throw 'Ledger phase marker incorrect after write-back.' }

    $Writeback = [ordered]@{
        schema='C11D-DYNAMIC-PHASE-O-CROSSWALK-WRITEBACK-V1'
        completed_utc=(Get-Date).ToUniversalTime().ToString('o')
        audit_status=[string]$Report.status
        report_path=$ReportPath; report_sha256=$ExpectedPhaseOReportSha
        csv_path=$CsvPath; csv_sha256=$ExpectedCsvSha
        summary_path=$SummaryPath; summary_sha256=$ExpectedSummarySha
        output_manifest_path=$OutputManifestPath; output_manifest_sha256=$ExpectedOutputManifestSha
        test_result='28/28'; test_stdout_sha256=$ExpectedTestStdoutSha; test_stderr_sha256=$EmptySha
        audit_stdout_sha256=$ExpectedAuditStdoutSha; audit_stderr_sha256=$EmptySha
        selectors='9/9'; receipts='18/18'; process_evidence_files='36/36'; asset_source_pins=15
        base_frame_field_rows=54; stable_custom_data_candidates='6/6'; static_source_pointers='3/3'
        unresolved_timebase_conflicts=2; approved_bindings=0; approved_custom_data_bindings=0
        approved_renderer_projection_bindings=0; editorial_fields_visually_consumed=0
        runtime_invocations=0; project_source_writes=0
        files=@(
            [ordered]@{path=$CheckpointRel;before_sha256=$ExpectedCheckpointSha;after_sha256=$CheckpointAfterSha},
            [ordered]@{path=$LedgerRel;before_sha256=$ExpectedLedgerSha;after_sha256=$LedgerAfterSha},
            [ordered]@{path=$AcceptanceRel;before_sha256=$null;after_sha256=$AcceptanceAfterSha}
        )
        backup_directory=$BackupDirectory; output_directory=$RunDirectory
        frozen_c11c_manifest='UNCHANGED'; renderer='OFF'; media_created=$false
        payload_materialized=$false; candidate_input_admissible=$false
        D4_8='BLOCKED'; release_authority='NONE'
    }
    $WrittenManifest = $true
    Write-Utf8NoBom $WritebackManifestPath (($Writeback | ConvertTo-Json -Depth 12) + "`n")

    $Completion = [ordered]@{
        schema='C11D-PHASE-O-SOURCE-FRAME-SEMANTIC-CROSSWALK-ACCEPTANCE-COMPLETION-V1'
        completed_utc=(Get-Date).ToUniversalTime().ToString('o')
        status='PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL'
        report_path=$ReportPath; report_sha256=$ExpectedPhaseOReportSha
        csv_path=$CsvPath; csv_sha256=$ExpectedCsvSha
        summary_path=$SummaryPath; summary_sha256=$ExpectedSummarySha
        output_manifest_path=$OutputManifestPath; output_manifest_sha256=$ExpectedOutputManifestSha
        test_result='28/28'; test_stdout_sha256=$ExpectedTestStdoutSha; test_stderr_sha256=$EmptySha
        audit_stdout_sha256=$ExpectedAuditStdoutSha; audit_stderr_sha256=$EmptySha
        selectors='9/9'; receipts='18/18'; process_evidence_files='36/36'; asset_source_pins=15
        base_frame_field_rows=54; stable_custom_data_candidates='6/6'; static_source_pointers='3/3'
        unresolved_timebase_conflicts=2; approved_bindings=0; approved_custom_data_bindings=0
        approved_renderer_projection_bindings=0; editorial_fields_visually_consumed=0
        runtime_invocations=0; project_source_writes=0; output_directory=$RunDirectory
        checkpoint_sha256=$CheckpointAfterSha; ledger_sha256=$LedgerAfterSha
        acceptance_record_sha256=$AcceptanceAfterSha; writeback_manifest=$WritebackManifestPath
        backup_directory=$BackupDirectory; frozen_c11c_manifest='UNCHANGED'
        renderer='OFF'; media_created=$false; payload_materialized=$false
        candidate_input_admissible=$false; D4_8='BLOCKED'; release_authority='NONE'
    }
    Write-Utf8NoBom $WritebackMarkerPath (($Completion | ConvertTo-Json -Depth 12) + "`n")
}
catch {
    if ($WrittenCheckpoint -and (Test-Path -LiteralPath (Join-Path $BackupDirectory 'checkpoint.before.md'))) {
        Copy-Item -LiteralPath (Join-Path $BackupDirectory 'checkpoint.before.md') -Destination $CheckpointPath -Force
    }
    if ($WrittenLedger -and (Test-Path -LiteralPath (Join-Path $BackupDirectory 'ledger.before.md'))) {
        Copy-Item -LiteralPath (Join-Path $BackupDirectory 'ledger.before.md') -Destination $LedgerPath -Force
    }
    if ($WrittenAcceptance -and (Test-Path -LiteralPath $AcceptancePath)) { Remove-Item -LiteralPath $AcceptancePath -Force }
    if ($WrittenManifest -and (Test-Path -LiteralPath $WritebackManifestPath)) { Remove-Item -LiteralPath $WritebackManifestPath -Force }
    if (Test-Path -LiteralPath $WritebackMarkerPath) { Remove-Item -LiteralPath $WritebackMarkerPath -Force }
    throw
}

Write-Host 'C11D_PHASE_O_SOURCE_FRAME_CROSSWALK_ACCEPTANCE=PASS'
Write-Host 'EXISTING_AUDIT_EVIDENCE=VERIFIED_NOT_RERUN'
Write-Host 'PHASE_O_TESTS=28/28'
Write-Host 'SELECTORS=9/9'
Write-Host 'SOURCE_FRAME_RECEIPTS=18/18'
Write-Host 'PROCESS_EVIDENCE_FILES=36/36'
Write-Host 'ASSET_SOURCE_PINS_VERIFIED=15'
Write-Host 'BASE_FRAME_FIELD_ROWS=54'
Write-Host 'CUSTOM_DATA_CANDIDATES_STABLE=6/6'
Write-Host 'STATIC_SOURCE_POINTERS=3/3'
Write-Host 'TIMEBASE_CONFLICTS_UNRESOLVED=2'
Write-Host 'APPROVED_BINDINGS=0'
Write-Host 'APPROVED_CUSTOM_DATA_BINDINGS=0'
Write-Host 'APPROVED_RENDERER_PROJECTION_BINDINGS=0'
Write-Host 'EDITORIAL_FIELDS_VISUALLY_CONSUMED=0'
Write-Host 'RUNTIME_INVOCATIONS=0'
Write-Host 'PROJECT_SOURCE_WRITES=0'
Write-Host ('REPORT_SHA256=' + $ExpectedPhaseOReportSha)
Write-Host ('CSV_SHA256=' + $ExpectedCsvSha)
Write-Host ('SUMMARY_SHA256=' + $ExpectedSummarySha)
Write-Host ('OUTPUT_MANIFEST_SHA256=' + $ExpectedOutputManifestSha)
Write-Host ('CHECKPOINT_SHA256=' + $CheckpointAfterSha)
Write-Host ('LEDGER_SHA256=' + $LedgerAfterSha)
Write-Host ('ACCEPTANCE_RECORD_SHA256=' + $AcceptanceAfterSha)
Write-Host ('WRITEBACK_MANIFEST=' + $WritebackManifestPath)
Write-Host ('BACKUP_DIRECTORY=' + $BackupDirectory)
Write-Host ('COMPLETION_MARKER=' + $WritebackMarkerPath)
Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
Write-Host 'RENDERER=OFF'
Write-Host 'MEDIA_CREATED=false'
Write-Host 'PAYLOAD_MATERIALIZED=false'
Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
Write-Host 'D4.8=BLOCKED'
Write-Host 'RELEASE_AUTHORITY=NONE'
