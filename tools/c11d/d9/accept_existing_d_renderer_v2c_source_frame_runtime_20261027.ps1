# C11-D Phase N evidence acceptance and controlled documentation write-back.
# Windows PowerShell 5.1; never reruns Python tests, planner, or Godot.
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
function Get-CountExact([string]$Text, [string]$Needle) {
    $Count = 0
    $Offset = 0
    while ($true) {
        $Index = $Text.IndexOf($Needle, $Offset, [StringComparison]::Ordinal)
        if ($Index -lt 0) { break }
        $Count++
        $Offset = $Index + $Needle.Length
    }
    return $Count
}
function Read-JsonFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Falta evidencia JSON: $Path" }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}
function Write-Utf8NoBom([string]$Path, [string]$Text) {
    [IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false)))
}
function Assert-Sha([string]$Path, [string]$Expected, [string]$Label) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "$Label ausente: $Path" }
    $Actual = Get-FileSha256 $Path
    if ($Actual -ne $Expected) { throw "$Label SHA incorrecto: observado $Actual; esperado $Expected" }
}

$FrozenManifestSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$FrozenManifestBytes = 796318
$ExpectedContractSha = '6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c'
$ExpectedRunnerSha = 'a4f5aab8febfb49ec25a97d12f4604137dcbf1c63049a50b0fafe5c0c0c5cdcf'
$ExpectedHarnessSha = 'ba8500c1db0b86539953c667bc1c48bc765e960f765f7ecef935ff4d206e2a9d'
$ExpectedTestSha = 'f8cb0717f9f90b46071dcbf292a4c308e3dac04b4090a3fd4a0ea53bf627ebfb'
$ExpectedV2BReportSha = '6e19e88bcce6249f613c7e8566b92f78497c4749bfd079dda2b01e20385072a0'
$ExpectedStaticReceiptSha = 'aa8cebd453b632e445becb936ff3520110d5f80fdf2a732818a6917885595e32'
$ExpectedV2CTestStdoutSha = '6e869618eb36c6f6ee74de8af851b9d3cb5810cfd35df37968176c06f17fb808'
$ExpectedEmptySha = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
$ExpectedRuntimeReportSha = '7f96c9aec3849212299afbcabe7fd3045fee815807c9cafe555ad8cb947f91f2'
$ExpectedRuntimeStdoutSha = 'bacfa68d6cd7f89e2466baac2b28ec0a9b37af4bcd073af9581bd6e05bffd69a'
$ExpectedCheckpointSha = '2d603f916af7a42a404cd701a3bc3c6967b28f75583ab0f8326a3c33e30ef30f'
$ExpectedLedgerSha = '4858b05af9be26d5dbfac0e3ac3b8a4e7c2f2eb30a36674e3216423c2ee350b9'

$OverlayApplyMarkerPath = Join-Path $env:TEMP 'C11D_V2C_RUNTIME_ACCEPTANCE_OVERLAY_20261027.completed.json'
$OverlayApplyMarker = Read-JsonFile $OverlayApplyMarkerPath
if ([string]$OverlayApplyMarker.schema -ne 'C11D-V2C-RUNTIME-ACCEPTANCE-OVERLAY-COMPLETION-V1' -or
    [string]$OverlayApplyMarker.overlay_id -ne 'C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_AND_PHASE_O_OVERLAY_20261027_V1' -or
    [string]$OverlayApplyMarker.add_only_files -ne '3/3_HASH_VERIFIED' -or
    [string]$OverlayApplyMarker.frozen_c11c_manifest -ne 'UNCHANGED' -or
    [string]$OverlayApplyMarker.overlay_zip_sha256 -notmatch '^[0-9a-f]{64}$' -or
    [string]$OverlayApplyMarker.overlay_manifest_sha256 -notmatch '^[0-9a-f]{64}$') { throw 'Marcador de aplicacion del overlay de aceptacion no coincide.' }

$FrozenManifestPath = Join-Path $Root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
Assert-Sha $FrozenManifestPath $FrozenManifestSha 'Manifiesto C11-C'
if ((Get-Item -LiteralPath $FrozenManifestPath).Length -ne $FrozenManifestBytes) { throw 'Tamano del manifiesto C11-C incorrecto.' }
Assert-Sha (Join-Path $Root 'definitions\c11d\production\D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json') $ExpectedContractSha 'Contrato V2-C'
Assert-Sha (Join-Path $Root 'tools\c11d\d9\d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py') $ExpectedRunnerSha 'Runner V2-C'
Assert-Sha (Join-Path $Root 'tools\c11d\d9\challenge_visual_payload_v2c_source_frame_runtime_in_memory.gd') $ExpectedHarnessSha 'Harness V2-C'
Assert-Sha (Join-Path $Root 'tools\c11d\d9\test_d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py') $ExpectedTestSha 'Tests V2-C'

$StaticMarkerPath = Join-Path $env:TEMP 'C11D_PHASE_KL_V2B_STATIC_GATE_20261027.completed.json'
$V2BMarkerPath = Join-Path $env:TEMP 'C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027.completed.json'
$AttemptPath = Join-Path $env:TEMP 'C11D_V2C_SOURCE_FRAME_RUNTIME_20261027.started.json'
$CompletionPath = Join-Path $env:TEMP 'C11D_V2C_SOURCE_FRAME_RUNTIME_20261027.completed.json'
$StaticMarker = Read-JsonFile $StaticMarkerPath
$V2BMarker = Read-JsonFile $V2BMarkerPath
$Attempt = Read-JsonFile $AttemptPath
$Completion = Read-JsonFile $CompletionPath
if ([string]$StaticMarker.schema -ne 'C11D-PHASE-KL-V2B-STATIC-GATE-COMPLETION-V1' -or
    [string]$StaticMarker.V2B_static_tests -ne 'PASS_198_OF_198' -or
    [string]$StaticMarker.source_pins -ne '81/81' -or
    [string]$StaticMarker.authority_input_pins -ne '9/9' -or
    [string]$StaticMarker.static_receipt_sha256 -ne $ExpectedStaticReceiptSha) { throw 'Marcador de aceptacion estatica Fase L inconsistente.' }
$StaticReceiptPath = [IO.Path]::GetFullPath([string]$StaticMarker.static_receipt_path)
Assert-Sha $StaticReceiptPath $ExpectedStaticReceiptSha 'Recibo estatico Fase L'
if ([string]$V2BMarker.schema -ne 'C11D-V2B-RUNTIME-MATRIX-COMPLETION-V1' -or
    [string]$V2BMarker.report_sha256 -ne $ExpectedV2BReportSha -or
    [string]$V2BMarker.static_receipt_sha256 -ne $ExpectedStaticReceiptSha) { throw 'Marcador de aceptacion runtime Fase M inconsistente.' }
Assert-Sha ([IO.Path]::GetFullPath([string]$V2BMarker.report_path)) $ExpectedV2BReportSha 'Informe Fase M'

if ([string]$Completion.schema -ne 'C11D-V2C-SOURCE-FRAME-RUNTIME-COMPLETION-V1' -or
    [string]$Completion.run_id -ne '994e039b597b496094eb72bf0ae145c5' -or
    [string]$Completion.test_result -ne 'PASS_28_OF_28' -or
    [string]$Completion.test_stdout_sha256 -ne $ExpectedV2CTestStdoutSha -or
    [string]$Completion.test_stderr_sha256 -ne $ExpectedEmptySha -or
    [string]$Completion.runtime_status -ne 'PASS_SOURCE_FRAME_ROUTE_ONLY' -or
    [string]$Completion.runtime_report_sha256 -ne $ExpectedRuntimeReportSha -or
    [string]$Completion.runtime_stdout_sha256 -ne $ExpectedRuntimeStdoutSha -or
    [string]$Completion.runtime_stderr_sha256 -ne $ExpectedEmptySha -or
    [string]$Completion.source_pin_count -ne '81' -or
    [string]$Completion.planner_invocations -ne '9/9' -or
    [int]$Completion.godot_version_probe_invocations -ne 1 -or
    [string]$Completion.godot_runtime_process_invocations -ne '18/18' -or
    [string]$Completion.accepted_selectors -ne '9/9' -or
    [string]$Completion.process_evidence_files_verified -ne '36/36' -or
    [string]$Completion.frozen_c11c_manifest -ne 'UNCHANGED' -or
    [string]$Completion.renderer -ne 'OFF' -or
    $Completion.media_created -ne $false -or
    $Completion.payload_materialized -ne $false -or
    $Completion.candidate_input_admissible -ne $false -or
    [string]$Completion.D4_8 -ne 'BLOCKED' -or
    [string]$Completion.release_authority -ne 'NONE') { throw 'Marcador de finalizacion V2-C inconsistente.' }
if ([string]$Attempt.schema -ne 'C11D-V2C-SOURCE-FRAME-RUNTIME-ATTEMPT-V1' -or
    [string]$Attempt.run_id -ne [string]$Completion.run_id -or
    [string]$Attempt.test_stdout_sha256 -ne $ExpectedV2CTestStdoutSha -or
    [string]$Attempt.test_stderr_sha256 -ne $ExpectedEmptySha -or
    [string]$Attempt.log_directory -ne [string]$Completion.log_directory -or
    [string]$Attempt.evidence_directory -ne [string]$Completion.evidence_directory) { throw 'Marcador de intento V2-C no coincide con la finalizacion.' }

$LogDirectory = [IO.Path]::GetFullPath([string]$Completion.log_directory)
$EvidenceDirectory = [IO.Path]::GetFullPath([string]$Completion.evidence_directory)
$TempRoot = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\') + '\'
if (-not $LogDirectory.StartsWith($TempRoot, [StringComparison]::OrdinalIgnoreCase) -or
    -not $EvidenceDirectory.StartsWith($TempRoot, [StringComparison]::OrdinalIgnoreCase) -or
    -not $LogDirectory.Contains('C11D_V2C_SOURCE_FRAME_RUNTIME_LOGS_20261027_994e039b597b496094eb72bf0ae145c5') -or
    -not $EvidenceDirectory.Contains('C11D_V2C_SOURCE_FRAME_EVIDENCE_20261027_994e039b597b496094eb72bf0ae145c5')) { throw 'Directorios V2-C fuera de ubicacion/temp o run id inesperado.' }
$ReportPath = [IO.Path]::GetFullPath([string]$Completion.runtime_report_path)
if ($ReportPath -ne [IO.Path]::GetFullPath((Join-Path $EvidenceDirectory 'report.json'))) { throw 'Ruta del informe no coincide con el directorio de evidencia.' }

$TestStdoutPath = Join-Path $LogDirectory 'contract_tests.stdout.txt'
$TestStderrPath = Join-Path $LogDirectory 'contract_tests.stderr.txt'
$RuntimeStdoutPath = Join-Path $LogDirectory 'source_frame_runtime.stdout.txt'
$RuntimeStderrPath = Join-Path $LogDirectory 'source_frame_runtime.stderr.txt'
Assert-Sha $TestStdoutPath $ExpectedV2CTestStdoutSha 'stdout tests contrato V2-C'
Assert-Sha $TestStderrPath $ExpectedEmptySha 'stderr tests contrato V2-C'
Assert-Sha $RuntimeStdoutPath $ExpectedRuntimeStdoutSha 'stdout runtime V2-C'
Assert-Sha $RuntimeStderrPath $ExpectedEmptySha 'stderr runtime V2-C'
Assert-Sha $ReportPath $ExpectedRuntimeReportSha 'Informe runtime V2-C'
$TestStdout = [IO.File]::ReadAllText($TestStdoutPath, [Text.Encoding]::UTF8)
$RuntimeStdout = [IO.File]::ReadAllText($RuntimeStdoutPath, [Text.Encoding]::UTF8)
$RuntimeStderr = [IO.File]::ReadAllText($RuntimeStderrPath, [Text.Encoding]::UTF8)
if (-not $TestStdout.Contains('C11D_V2C_PYTHON_CONTRACT_TESTS_PASS=28/28') -or
    -not $RuntimeStdout.Contains('C11D_V2C_RESULT=PASS_SOURCE_FRAME_ROUTE_ONLY') -or
    -not $RuntimeStdout.Contains('C11D_V2C_REPORT_SHA256=' + $ExpectedRuntimeReportSha) -or
    -not $RuntimeStdout.Contains('C11D_V2C_PLANNER_INVOCATIONS=9/9') -or
    -not $RuntimeStdout.Contains('C11D_V2C_GODOT_RUNTIME_PROCESSES=18/18') -or
    -not $RuntimeStdout.Contains('C11D_V2C_SELECTORS=9/9') -or $RuntimeStderr.Length -ne 0) { throw 'Marcadores operacionales del stdout/stderr V2-C no coinciden.' }
$Report = Read-JsonFile $ReportPath
if ([string]$Report.schema -ne 'C11D-CHALLENGE-VISUAL-PAYLOAD-V2C-SOURCE-FRAME-RUNTIME-REPORT-V1' -or
    [string]$Report.schema_version -ne '1.0' -or
    [string]$Report.status -ne 'PASS_SOURCE_FRAME_ROUTE_ONLY' -or
    [int]$Report.source_pin_count -ne 81 -or
    [int]$Report.selector_count_expected -ne 9 -or
    [int]$Report.planner_invocations -ne 9 -or
    [int]$Report.godot_version_probe_invocations -ne 1 -or
    [int]$Report.godot_runtime_process_invocations -ne 18 -or
    [int]$Report.godot_runtime_processes_expected -ne 18 -or
    [string]$Report.contract_sha256 -ne $ExpectedContractSha -or
    [string]$Report.frozen_manifest_sha256 -ne $FrozenManifestSha -or
    [string]$Report.evidence.godot_version -ne '4.7.1.stable.mono.official.a13da4feb' -or
    [int]$Report.evidence.godot_version_probe_exit_code -ne 0 -or
    $Report.payload_materialized -ne $false -or $Report.media_created -ne $false -or
    [int]$Report.approved_bindings -ne 0 -or [string]$Report.visual_seed_sensitivity -ne 'NOT_TESTED' -or
    $null -ne $Report.evidence.failure) { throw 'Informe V2-C no cumple schema, conteos, identidad o limites de politica.' }
$PinErrors = 0
if ($null -ne $Report.evidence.source_pin_errors_before_runtime) { $PinErrors = @($Report.evidence.source_pin_errors_before_runtime).Count }
if ($PinErrors -ne 0) { throw 'El informe V2-C contiene errores de source pins.' }
$Governance = $Report.governance_locks
$D48 = [string]$Governance.PSObject.Properties['D4.8'].Value
$D910 = [string]$Governance.PSObject.Properties['D9.10'].Value
$D914 = [string]$Governance.PSObject.Properties['D9.14'].Value
$D916 = [string]$Governance.PSObject.Properties['D9.16'].Value
$D917 = [string]$Governance.PSObject.Properties['D9.17'].Value
$D10 = [string]$Governance.PSObject.Properties['D10'].Value
if ([string]$Governance.renderer -ne 'OFF' -or $Governance.media_created -ne $false -or
    $Governance.candidate_input_admissible -ne $false -or $Governance.seed_domains_complete_for_candidate_input -ne $false -or
    $Governance.automatic_seed_generation -ne $false -or [string]$Governance.master_seed -ne 'NOT_ADOPTED' -or
    $D48 -ne 'BLOCKED' -or $D910 -ne 'PREPARE_ONLY' -or $D914 -ne 'BLOCKED' -or
    $D916 -ne 'BLOCKED' -or $D917 -ne 'BLOCKED_NO_GO' -or $D10 -ne 'BLOCKED_FOR_PROMOTION' -or
    [string]$Governance.baseline_approval -ne 'MISSING' -or $Governance.freeze_eligible -ne $false -or
    [string]$Governance.release_authority -ne 'NONE' -or [string]$Governance.challenge_visual_seed_sensitivity -ne 'NOT_TESTED') {
    throw 'Los bloqueos de gobernanza del informe V2-C no coinciden.'
}

$ExpectedSelectorIds = @('CHALLENGE_001','CHALLENGE_002','CHALLENGE_003','CHALLENGE_004','CHALLENGE_005','CHALLENGE_006','CHALLENGE_007','CHALLENGE_008','CHALLENGE_009')
$Rows = @($Report.selectors)
if ($Rows.Count -ne 9) { throw 'Numero de filas selector V2-C incorrecto.' }
$ProcessIds = New-Object System.Collections.ArrayList
$RunIds = New-Object System.Collections.ArrayList
for ($i=0; $i -lt 9; $i++) {
    $Row = $Rows[$i]
    $BlockedCount = 0
    if ($null -ne $Row.block_reasons) { $BlockedCount = @($Row.block_reasons).Count }
    if ([string]$Row.selector.challenge_id -ne $ExpectedSelectorIds[$i] -or
        [string]$Row.status -ne 'ACCEPTED_SOURCE_FRAME_ONLY' -or $BlockedCount -ne 0 -or
        $Row.repeat_agreement -ne $true -or [int]$Row.planner.invocations -ne 1 -or
        [string]$Row.planner.status -ne 'PLANNED' -or
        [string]$Row.planner.bridge_status -ne 'PLANNING_ONLY_NOT_RENDERABLE' -or
        [string]$Row.planner.adapter_status -ne 'PREPARED_NOT_DISPATCHED_RENDERER_DISABLED') { throw "Fila de selector no valida: $i" }
    $Runs = @($Row.runtime_runs)
    if ($Runs.Count -ne 2) { throw "No hay dos recibos runtime para $($ExpectedSelectorIds[$i])." }
    foreach ($Run in $Runs) {
        if ([int]$Run.exit_code -ne 0 -or [int]$Run.process_id -le 0 -or $null -eq $Run.receipt -or
            [string]$Run.receipt.status -ne 'SOURCE_FRAME_RECEIPT' -or
            [string]$Run.receipt.route.runtime_bridge_method -ne 'ChallengeRuntimeBridge.run_effective_pipeline' -or
            $Run.receipt.side_effects.payload_file_written -ne $false -or $Run.receipt.side_effects.media_created -ne $false -or
            $Run.receipt.side_effects.renderer_native_input_emitted -ne $false -or $Run.receipt.side_effects.render_nodes_created -ne $false -or
            $Run.receipt.side_effects.rendering_server_called -ne $false -or $Run.receipt.side_effects.viewport_captured -ne $false -or
            $Run.receipt.side_effects.canonical_state_mutated -ne $false -or $Run.receipt.side_effects.production_dispatched -ne $false) {
            throw "Recibo source-frame o side-effects invalido para $($ExpectedSelectorIds[$i])."
        }
        if ($ProcessIds.Contains([int]$Run.process_id) -or $RunIds.Contains([string]$Run.run_id)) { throw 'process_id/run_id duplicado en V2-C.' }
        [void]$ProcessIds.Add([int]$Run.process_id)
        [void]$RunIds.Add([string]$Run.run_id)
    }
}
$EvidenceMap = $Report.evidence.evidence_file_sha256
if ($null -eq $EvidenceMap) { throw 'Falta el mapa de hashes de evidencia V2-C.' }
$EvidenceCount = 0
foreach ($Property in $EvidenceMap.PSObject.Properties) {
    $Rel = [string]$Property.Name
    if ([string]::IsNullOrWhiteSpace($Rel) -or $Rel.StartsWith('/') -or $Rel.Contains('..') -or $Rel.Contains(':') -or $Rel.Contains('\')) { throw "Nombre de archivo de evidencia inseguro: $Rel" }
    $Path = Join-Path $EvidenceDirectory $Rel
    Assert-Sha $Path ([string]$Property.Value) "Artefacto de evidencia $Rel"
    $EvidenceCount++
}
if ($EvidenceCount -ne 36 -or $ProcessIds.Count -ne 18 -or $RunIds.Count -ne 18) { throw 'Conteo de evidencia/procesos/recibos V2-C incorrecto.' }

# Only now may the documentation write-back proceed.
$CheckpointRel = 'docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md'
$LedgerRel = 'docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md'
$AcceptanceRel = 'docs/current/d/C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_20261027_V1.md'
$CheckpointPath = Join-Path $Root ($CheckpointRel.Replace('/','\'))
$LedgerPath = Join-Path $Root ($LedgerRel.Replace('/','\'))
$AcceptancePath = Join-Path $Root ($AcceptanceRel.Replace('/','\'))
Assert-Sha $CheckpointPath $ExpectedCheckpointSha 'Checkpoint Phase M'
Assert-Sha $LedgerPath $ExpectedLedgerSha 'Ledger Phase M'
if (Test-Path -LiteralPath $AcceptancePath) { throw "Registro add-only ya existe: $AcceptancePath" }
$CheckpointText = [IO.File]::ReadAllText($CheckpointPath, [Text.Encoding]::UTF8)
$LedgerText = [IO.File]::ReadAllText($LedgerPath, [Text.Encoding]::UTF8)
$PendingStatus = 'V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PASS; V2C_SOURCE_FRAME_RECEIPTS_PENDING'
if ((Get-CountExact $CheckpointText $PendingStatus) -ne 2) { throw 'Se esperaban dos tokens pending en checkpoint; no se modifica documentación.' }
$OldPhaseMarker = 'PHASE_K_CHALLENGE_COLLISION_EXPANSION_PASS; PHASE_L_V2B_STATIC_TESTS_PASS; PHASE_M_V2B_RUNTIME_MATRIX_PASS; NEXT_V2C_SOURCE_FRAME_RECEIPTS_GATE'
if ((Get-CountExact $LedgerText $OldPhaseMarker) -ne 1) { throw 'El marcador de fase del ledger no coincide; no se modifica documentación.' }
$ActionLines = @([regex]::Split($LedgerText, "\r\n|\n|\r") | Where-Object { $_.StartsWith('**Próxima acción única:**') -and $_.Contains('puerta V2-C de recibos runtime source-frame') })
if ($ActionLines.Count -ne 1) { throw 'No se identifica una única próxima acción Phase N en el ledger.' }

$NewStatus = 'V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PASS; V2C_SOURCE_FRAME_RUNTIME_PASS; PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK_PENDING'
$CheckpointText = $CheckpointText.Replace($PendingStatus, $NewStatus)
$LedgerText = $LedgerText.Replace($OldPhaseMarker, 'PHASE_K_CHALLENGE_COLLISION_EXPANSION_PASS; PHASE_L_V2B_STATIC_TESTS_PASS; PHASE_M_V2B_RUNTIME_MATRIX_PASS; PHASE_N_V2C_SOURCE_FRAME_RUNTIME_PASS; NEXT_PHASE_O_SOURCE_FRAME_SEMANTIC_BINDING_CROSSWALK')
$OldAction = $ActionLines[0]
$NewAction = '**Próxima acción única:** auditar en modo de solo lectura los nueve recibos source-frame V2-C y cruzarlos con la propuesta de binding semántico existente; clasificar datos temporales, contadores de episodio, candidatos de custom_data y ausencias, sin aprobar bindings ni materializar payload/media.'
$LedgerText = $LedgerText.Replace($OldAction, $NewAction)

$PhaseRecord = @"

### Fase N — Runtime source-frame V2-C (27-10-2026, Windows PASS; route-only)

- Contrato Python: `28/28`; stdout SHA-256 `$ExpectedV2CTestStdoutSha`; stderr SHA-256 `$ExpectedEmptySha` (vacío).
- Contrato V2-C y source pins: `81/81`; planner canónico `9/9`; sonda de versión Godot `1`; procesos Godot Mono independientes `18/18`; selectores aceptados `9/9`; artefactos de proceso `36/36` con hashes verificados.
- Godot: `4.7.1.stable.mono.official.a13da4feb`; estado de reporte `PASS_SOURCE_FRAME_ROUTE_ONLY`.
- Reporte: `$ReportPath`; SHA-256 `$ExpectedRuntimeReportSha`; stdout SHA-256 `$ExpectedRuntimeStdoutSha`; stderr SHA-256 `$ExpectedEmptySha` (vacío).
- Directorio de logs: `$LogDirectory`; directorio de evidencia: `$EvidenceDirectory`; completion marker: `$CompletionPath`.
- Cada Challenge tiene una llamada al planner y dos procesos aislados con recibos `SOURCE_FRAME_RECEIPT` a través de `ChallengeRuntimeBridge.run_effective_pipeline`. Los recibos confirman ausencia de escritura de payload, creación de media, emisión de input nativo de renderer, nodos de render, llamadas al servidor de render, captura de viewport, mutación del estado canónico y dispatch de producción.
- Alcance aceptado: repetibilidad de recibo source-frame y ruta runtime efectiva en memoria. `visual_seed_sensitivity=NOT_TESTED`; esta fase no demuestra dibujo de texto, píxeles, proyección de entrega ni vídeo.

**Siguiente puerta:** Fase O — auditoría de solo lectura del cruce recibo source-frame → propuesta de binding semántico, sin aprobar ningún binding. Debe distinguir `winning_frame` como único anclaje temporal Challenge y `close_calls` como contador, y mantener en revisión cualquier campo `custom_data`, proyección y tratamiento temporal.

**Gobernanza inalterada:** `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`. El conflicto CHALLENGE_008/009 (11 s declarados y 12 s de fases) sigue pendiente.
"@
$CheckpointText += $PhaseRecord
$LedgerText += $PhaseRecord
$CheckpointText = $CheckpointText -replace "`r`n", "`n"
$LedgerText = $LedgerText -replace "`r`n", "`n"

$AcceptanceText = @"
# C11-D — Aceptación Windows V2-C Source-Frame Runtime (Fase N)

**Estado:** `WINDOWS_PASS_SOURCE_FRAME_ROUTE_ONLY; NO_RENDER; NO_MEDIA; GOVERNANCE_LOCKS_PRESERVED`.

## Evidencia validada en el checkout Windows

- Python contract tests `28/28`; stdout SHA-256 `$ExpectedV2CTestStdoutSha`; stderr vacío, SHA-256 `$ExpectedEmptySha`.
- Contrato source-frame pins `81/81`; planner canónico `9/9`; sonda de identidad Godot `1/1`; runtime Godot Mono independiente `18/18`; selectores `9/9`; archivos stdout/stderr de proceso verificados `36/36`.
- Reporte: `$ReportPath`; SHA-256 `$ExpectedRuntimeReportSha`; status `PASS_SOURCE_FRAME_ROUTE_ONLY`.
- Runtime stdout: `$RuntimeStdoutPath`; SHA-256 `$ExpectedRuntimeStdoutSha`; stderr: `$RuntimeStderrPath`; SHA-256 `$ExpectedEmptySha` (vacío).
- Godot `4.7.1.stable.mono.official.a13da4feb`. Todos los recibos son `SOURCE_FRAME_RECEIPT`; los IDs de proceso y run son únicos y cada selector presenta acuerdo entre las dos repeticiones.
- Se comprobaron 36 artefactos contra el mapa de SHA-256 del propio informe. Las filas de selector están en orden `CHALLENGE_001` a `CHALLENGE_009`, con estado `ACCEPTED_SOURCE_FRAME_ONLY` y sin block reasons.
- Cada recibo usa `ChallengeRuntimeBridge.run_effective_pipeline`. Los flags de side-effect informan `false` para payload escrito, media creada, renderer-native input emitido, nodos de render, render server llamado, viewport capturado, estado canónico mutado y dispatch de producción.

## Interpretación y límites

Esta aceptación demuestra un recibo source-frame repetible en una ruta runtime efectiva para los nueve Challenges. No es una aprobación de render: el bridge permanece `PLANNING_ONLY_NOT_RENDERABLE` y el adaptador `PREPARED_NOT_DISPATCHED_RENDERER_DISABLED`. `visual_seed_sensitivity=NOT_TESTED`; no demuestra píxeles, texto dibujado, proyección de entrega, sincronización final ni vídeo. El sidecar editorial sigue sin tener bindings aprobados. El conflicto temporal de `CHALLENGE_008/009` (11 segundos declarados frente a 12 segundos de fases) sigue bloqueado.

## Siguiente puerta

Fase O: auditar de solo lectura los recibos source-frame y cruzarlos con la propuesta de binding semántico. Clasificar disponibilidad, linaje, naturaleza temporal y alcance de cada dato candidato, especialmente `winning_frame`, `close_calls` y candidatos de `custom_data`. El cruce no puede declarar bindings aprobados; requiere decisiones explícitas y evidencia propia.

## Gobernanza

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

## SHA-256 de documentación tras write-back

- Checkpoint: `CHECKPOINT_AFTER_SHA_PLACEHOLDER`.
- Ledger: `LEDGER_AFTER_SHA_PLACEHOLDER`.
- Este registro: se calcula al finalizar el write-back y se incluye en el manifiesto dinámico de Temp.
"@

$BackupDirectory = Join-Path $env:TEMP ('C11D_PHASE_N_SOURCE_FRAME_ACCEPTANCE_BACKUP_' + [Guid]::NewGuid().ToString('N'))
$WritebackManifestPath = Join-Path $env:TEMP ('C11D_PHASE_N_SOURCE_FRAME_WRITEBACK_' + [Guid]::NewGuid().ToString('N') + '.json')
$CompletionAcceptancePath = Join-Path $env:TEMP 'C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_20261027.completed.json'
if (Test-Path -LiteralPath $CompletionAcceptancePath) { throw "Aceptacion documental ya completada: $CompletionAcceptancePath" }
New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
Copy-Item -LiteralPath $CheckpointPath -Destination (Join-Path $BackupDirectory 'checkpoint.before.md')
Copy-Item -LiteralPath $LedgerPath -Destination (Join-Path $BackupDirectory 'ledger.before.md')
$WrittenAcceptance = $false
$WrittenCheckpoint = $false
$WrittenLedger = $false
try {
    Write-Utf8NoBom $CheckpointPath $CheckpointText
    $WrittenCheckpoint = $true
    Write-Utf8NoBom $LedgerPath $LedgerText
    $WrittenLedger = $true
    $CheckpointAfterSha = Get-FileSha256 $CheckpointPath
    $LedgerAfterSha = Get-FileSha256 $LedgerPath
    $AcceptanceText = $AcceptanceText -replace 'CHECKPOINT_AFTER_SHA_PLACEHOLDER', $CheckpointAfterSha
    $AcceptanceText = $AcceptanceText -replace 'LEDGER_AFTER_SHA_PLACEHOLDER', $LedgerAfterSha
    Write-Utf8NoBom $AcceptancePath ($AcceptanceText.TrimEnd() + "`n")
    $WrittenAcceptance = $true

    if ((Get-FileSha256 $FrozenManifestPath) -ne $FrozenManifestSha -or (Get-Item -LiteralPath $FrozenManifestPath).Length -ne $FrozenManifestBytes) { throw 'El manifiesto C11-C cambio en write-back.' }
    if ((Get-CountExact ([IO.File]::ReadAllText($CheckpointPath, [Text.Encoding]::UTF8)) $NewStatus) -ne 2) { throw 'Postcondicion de estado del checkpoint incorrecta.' }
    if ((Get-FileSha256 $CheckpointPath) -eq $ExpectedCheckpointSha -or (Get-FileSha256 $LedgerPath) -eq $ExpectedLedgerSha) { throw 'Los hashes del checkpoint/ledger no cambiaron.' }

    $WritebackManifest = [ordered]@{
        schema='C11D-DYNAMIC-PHASE-N-DOCUMENTATION-WRITEBACK-V1'
        completed_utc=(Get-Date).ToUniversalTime().ToString('o')
        runtime_report_path=$ReportPath
        runtime_report_sha256=$ExpectedRuntimeReportSha
        runtime_stdout_sha256=$ExpectedRuntimeStdoutSha
        runtime_stderr_sha256=$ExpectedEmptySha
        test_stdout_sha256=$ExpectedV2CTestStdoutSha
        test_stderr_sha256=$ExpectedEmptySha
        source_pins_verified='81/81'
        planner_invocations='9/9'
        godot_runtime_processes='18/18'
        selectors='9/9'
        evidence_files='36/36'
        backup_directory=$BackupDirectory
        files=@(
            [ordered]@{path=$CheckpointRel;before_sha256=$ExpectedCheckpointSha;after_sha256=(Get-FileSha256 $CheckpointPath)},
            [ordered]@{path=$LedgerRel;before_sha256=$ExpectedLedgerSha;after_sha256=(Get-FileSha256 $LedgerPath)},
            [ordered]@{path=$AcceptanceRel;before_sha256=$null;after_sha256=(Get-FileSha256 $AcceptancePath)}
        )
    }
    Write-Utf8NoBom $WritebackManifestPath (($WritebackManifest | ConvertTo-Json -Depth 12) + "`n")
    $Final = [ordered]@{
        schema='C11D-V2C-SOURCE-FRAME-RUNTIME-ACCEPTANCE-COMPLETION-V1'
        completed_utc=(Get-Date).ToUniversalTime().ToString('o')
        status='PASS_SOURCE_FRAME_ROUTE_ONLY'
        test_result='28/28'
        source_pins='81/81'
        planner_invocations='9/9'
        godot_runtime_processes='18/18'
        selectors='9/9'
        process_evidence_files='36/36'
        report_path=$ReportPath
        report_sha256=$ExpectedRuntimeReportSha
        stdout_sha256=$ExpectedRuntimeStdoutSha
        stderr_sha256=$ExpectedEmptySha
        checkpoint_sha256=(Get-FileSha256 $CheckpointPath)
        ledger_sha256=(Get-FileSha256 $LedgerPath)
        acceptance_record_sha256=(Get-FileSha256 $AcceptancePath)
        writeback_manifest=$WritebackManifestPath
        backup_directory=$BackupDirectory
        frozen_c11c_manifest='UNCHANGED'
        renderer='OFF'; media_created=$false; payload_materialized=$false; candidate_input_admissible=$false
        D4_8='BLOCKED'; release_authority='NONE'
    }
    Write-Utf8NoBom $CompletionAcceptancePath (($Final | ConvertTo-Json -Depth 12) + "`n")
}
catch {
    if ($WrittenCheckpoint -and (Test-Path -LiteralPath (Join-Path $BackupDirectory 'checkpoint.before.md'))) {
        Copy-Item -LiteralPath (Join-Path $BackupDirectory 'checkpoint.before.md') -Destination $CheckpointPath -Force
    }
    if ($WrittenLedger -and (Test-Path -LiteralPath (Join-Path $BackupDirectory 'ledger.before.md'))) {
        Copy-Item -LiteralPath (Join-Path $BackupDirectory 'ledger.before.md') -Destination $LedgerPath -Force
    }
    if ($WrittenAcceptance -and (Test-Path -LiteralPath $AcceptancePath)) { Remove-Item -LiteralPath $AcceptancePath -Force }
    if (Test-Path -LiteralPath $CompletionAcceptancePath) { Remove-Item -LiteralPath $CompletionAcceptancePath -Force }
    throw
}

Write-Host 'C11D_PHASE_N_V2C_SOURCE_FRAME_ACCEPTANCE=PASS'
Write-Host 'EXISTING_RUNTIME_EVIDENCE=VERIFIED_NOT_RERUN'
Write-Host 'PYTHON_CONTRACT_TESTS=28/28'
Write-Host 'SOURCE_PINS=81/81'
Write-Host 'PLANNER_INVOCATIONS=9/9'
Write-Host 'GODOT_VERSION_PROBE_INVOCATIONS=1'
Write-Host 'GODOT_RUNTIME_PROCESSES=18/18'
Write-Host 'SELECTORS=9/9'
Write-Host 'PROCESS_EVIDENCE_FILES_VERIFIED=36/36'
Write-Host ('REPORT_SHA256=' + $ExpectedRuntimeReportSha)
Write-Host ('STDOUT_SHA256=' + $ExpectedRuntimeStdoutSha)
Write-Host ('STDERR_SHA256=' + $ExpectedEmptySha)
Write-Host ('CHECKPOINT_SHA256=' + (Get-FileSha256 $CheckpointPath))
Write-Host ('LEDGER_SHA256=' + (Get-FileSha256 $LedgerPath))
Write-Host ('ACCEPTANCE_RECORD_SHA256=' + (Get-FileSha256 $AcceptancePath))
Write-Host ('WRITEBACK_MANIFEST=' + $WritebackManifestPath)
Write-Host ('BACKUP_DIRECTORY=' + $BackupDirectory)
Write-Host ('COMPLETION_MARKER=' + $CompletionAcceptancePath)
Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
Write-Host 'RENDERER=OFF'
Write-Host 'MEDIA_CREATED=false'
Write-Host 'PAYLOAD_MATERIALIZED=false'
Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
Write-Host 'D4.8=BLOCKED'
Write-Host 'RELEASE_AUTHORITY=NONE'
