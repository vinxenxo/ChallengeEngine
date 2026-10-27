# C11-D Phase M recovery from an existing runtime report; never reruns Godot.
# UTF-8 BOM is intentional for Windows PowerShell 5.1.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$ExpectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$ProjectRoot = [System.IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\')
if (-not [string]::Equals($ProjectRoot, $ExpectedRoot, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Run from the exact checkout root: $ExpectedRoot" }

function Get-FileSha256([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Write-Utf8NoBom([string]$Path, [string]$Text) { [System.IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false))) }
function Count-Exact([string]$Text, [string]$Needle) { return ([regex]::Matches($Text, [regex]::Escape($Needle))).Count }

$FrozenSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$FrozenBytes = 796318
$ExpectedReportSha = '6e19e88bcce6249f613c7e8566b92f78497c4749bfd079dda2b01e20385072a0'
$ExpectedStdoutSha = '939dc1c7a3891c03418f72c72f6d40a8067ad47b01e7de2af4de1acb25e4dabb'
$ExpectedStderrSha = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
$ExpectedReceiptSha = 'aa8cebd453b632e445becb936ff3520110d5f80fdf2a732818a6917885595e32'
$ExpectedContractSha = 'f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3'
$ExpectedDesignSha = 'e4f02e37fd4b9b2c89cbaa7597162f87b180da43182dc576d664263c1b937cfc'
$ExpectedMatrixSha = 'd69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a'
$ExpectedRunnerSha = '6a92aac96786acd2316f8e46b9d895f7cdcdfccbd75e9686378a4144a3a01a7f'
$ExpectedHarnessSha = 'aa175afe2ce357473aa46ed7c55ce46edf3f56457db461be28f7ec8e2f0b5ce2'
$ExpectedTestSha = '35a14f6d7ec56146b0cfaa3d304d18e5325757ed660e1fc08e1b4a0f767ecc87'
$ExpectedReceiptSchemaSha = '278ef5c1e4a96955d547dc70ab2e8cebc73f5ddb904dbb66563322be5c52e52c'
$ExpectedReportSchemaSha = '7152b4cb28f01dd33d140b22459d6eafd98d6a21811393d48ace97640c4a04b1'
$ExpectedContractSchemaSha = '0f804aeb51427286a6160aa445cdd98b2d3bbaaace19feacfa32f80e0fe738a5'
$ExpectedCheckpointSha = '93c07fd260e1cb56870e8448882f330a91b523fa735cad844ba2d941f041953b'
$ExpectedLedgerSha = '7155a14a03cd4a24e0eed00d04fefe086ea355e041f56bb1e2d2d485ac50121d'
$ExpectedStaticAcceptanceSha = '9be3d49f5498f87783c30db69fa0e6a47d0721a17b86258926077c7d10933d8f'
$ExpectedRunbookSha = '8b072a7bcaedfd67fbf2b45c9ad4cdf9138885c2f8f84115fc9893446c71d0a2'
$ExpectedWrapperSha = '6969d30038293974b70c0f36b3110de62e8d75d73fb57fc371fefe84c3694d23'

$ManifestPath = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$OverlayCompletionMarker = Join-Path $env:TEMP 'C11D_V2B_RUNTIME_MATRIX_RECOVERY_OVERLAY_20261027.completed.json'
$AttemptMarker = Join-Path $env:TEMP 'C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027.started.json'
$CompletionMarker = Join-Path $env:TEMP 'C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027.completed.json'
$StaticCompletionMarker = Join-Path $env:TEMP 'C11D_PHASE_KL_V2B_STATIC_GATE_20261027.completed.json'
$ExpectedLogLeaf = 'C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027_e1da037c4bad4c23853cc4e8b9f3d37f'

if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf) -or (Get-Item -LiteralPath $ManifestPath).Length -ne $FrozenBytes -or (Get-FileSha256 $ManifestPath) -ne $FrozenSha) { throw 'Frozen C11-C manifest mismatch.' }
if (-not (Test-Path -LiteralPath $AttemptMarker -PathType Leaf)) { throw "Runtime attempt marker missing: $AttemptMarker" }
if (Test-Path -LiteralPath $CompletionMarker) { throw "Runtime matrix already has a completion marker: $CompletionMarker" }
if (-not (Test-Path -LiteralPath $StaticCompletionMarker -PathType Leaf)) { throw 'Accepted Phase L static completion marker missing.' }
if (-not (Test-Path -LiteralPath $OverlayCompletionMarker -PathType Leaf)) { throw 'Recovery overlay completion marker missing; apply the guarded overlay first.' }
$overlayDone = Get-Content -LiteralPath $OverlayCompletionMarker -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$overlayDone.schema -ne 'C11D-V2B-RUNTIME-MATRIX-RECOVERY-OVERLAY-COMPLETION-V1' -or [string]$overlayDone.overlay_id -ne 'C11D_V2B_RUNTIME_MATRIX_POSTCHECK_RECOVERY_OVERLAY_20261027_V1' -or [string]$overlayDone.status -ne 'PASS') { throw 'Recovery overlay completion marker does not verify the expected overlay.' }
$attempt = Get-Content -LiteralPath $AttemptMarker -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$attempt.schema -ne 'C11D-V2B-RUNTIME-MATRIX-ATTEMPT-V1' -or [string]$attempt.project_root -ne $ProjectRoot) { throw 'Runtime attempt marker does not match this checkout.' }
$LogDirectory = [IO.Path]::GetFullPath([string]$attempt.log_directory)
if ((Split-Path -Leaf $LogDirectory) -cne $ExpectedLogLeaf -or -not (Test-Path -LiteralPath $LogDirectory -PathType Container)) { throw "Unexpected or absent runtime log directory: $LogDirectory" }
$static = Get-Content -LiteralPath $StaticCompletionMarker -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$static.schema -ne 'C11D-PHASE-KL-V2B-STATIC-GATE-COMPLETION-V1' -or [string]$static.V2B_static_tests -ne 'PASS_198_OF_198' -or [string]$static.source_pins -ne '81/81' -or [string]$static.authority_input_pins -ne '9/9' -or [string]$static.static_receipt_sha256 -ne $ExpectedReceiptSha) { throw 'Phase L completion marker does not verify the required static gate.' }
$ReceiptPath = [IO.Path]::GetFullPath([string]$static.static_receipt_path)
if (-not (Test-Path -LiteralPath $ReceiptPath -PathType Leaf) -or (Get-FileSha256 $ReceiptPath) -ne $ExpectedReceiptSha) { throw 'Accepted static receipt missing or hash mismatch.' }

$EvidenceDirectory = Join-Path $LogDirectory 'process_evidence'
$ReportPath = Join-Path $EvidenceDirectory 'report.json'
$StdoutPath = Join-Path $LogDirectory 'runtime_matrix.stdout.txt'
$StderrPath = Join-Path $LogDirectory 'runtime_matrix.stderr.txt'
foreach ($p in @($ReportPath,$StdoutPath,$StderrPath)) { if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Required existing evidence file missing: $p" } }
$reportSha = Get-FileSha256 $ReportPath
$stdoutSha = Get-FileSha256 $StdoutPath
$stderrSha = Get-FileSha256 $StderrPath
$stdoutText = [IO.File]::ReadAllText($StdoutPath)
$stderrText = [IO.File]::ReadAllText($StderrPath)
if ($reportSha -ne $ExpectedReportSha -or $stdoutSha -ne $ExpectedStdoutSha -or $stderrSha -ne $ExpectedStderrSha) { throw "Existing evidence hashes differ. report=$reportSha stdout=$stdoutSha stderr=$stderrSha" }
if ((Get-Item -LiteralPath $StderrPath).Length -ne 0 -or $stderrText.Length -ne 0) { throw 'Runtime stderr is not empty.' }
$report = Get-Content -LiteralPath $ReportPath -Raw -Encoding UTF8 | ConvertFrom-Json

# Re-evaluate all launcher postconditions from the existing report. No runner or Godot process is invoked here.
$statusOk = ([string]$report.schema -eq 'C11D-CHALLENGE-VISUAL-PAYLOAD-V2B-SAFE-PROJECTION-RUNTIME-REPORT-V1' -and [string]$report.schema_version -eq '1.0' -and [string]$report.status -eq 'PASS_SAFE_PROJECTION_SEED_SENSITIVITY')
$countsOk = ([int]$report.selector_count_expected -eq 9 -and [int]$report.planner_invocations -eq 45 -and [int]$report.planner_invocations_expected -eq 45 -and [int]$report.godot_runtime_process_invocations -eq 45 -and [int]$report.godot_runtime_processes_expected -eq 45)
$sensitivityOk = ([string]$report.visual_seed_sensitivity -eq 'ACCEPTED_BY_SAFE_PROJECTION_HASH')
$governance = $report.governance_locks
$governanceD48 = [string]$governance.PSObject.Properties['D4.8'].Value
$governanceD910 = [string]$governance.PSObject.Properties['D9.10'].Value
$governanceD10 = [string]$governance.PSObject.Properties['D10'].Value
$governanceOk = ([string]$governance.renderer -eq 'OFF' -and $governance.media_created -eq $false -and $governance.payload_materialized -eq $false -and $governance.candidate_input_admissible -eq $false -and $governanceD48 -eq 'BLOCKED' -and [string]$governance.release_authority -eq 'NONE' -and $governanceD910 -eq 'PREPARE_ONLY' -and $governanceD10 -eq 'BLOCKED_FOR_PROMOTION')
$rows = @($report.selectors)
$rowsOk = ($rows.Count -eq 9)
if ($rowsOk) {
    for ($i = 0; $i -lt 9; $i++) {
        $row = $rows[$i]
        $expectedId = ('CHALLENGE_{0:D3}' -f ($i + 1))
        if ([string]$row.selector.challenge_id -ne $expectedId -or [string]$row.status -ne 'ACCEPTED_SAFE_PROJECTION_RUNTIME' -or @($row.planner_variants).Count -ne 5 -or @($row.runtime_runs).Count -ne 5 -or @($row.block_reasons).Count -ne 0 -or [string]$row.comparison.status -ne 'PASS' -or $row.comparison.baseline_repeat_agreement -ne $true -or $row.comparison.gameplay_seed_safe_state_changed -ne $true -or $row.comparison.music_seed_safe_state_and_candidates_invariant -ne $true -or $row.comparison.editorial_safe_state_and_candidates_invariant -ne $true) { $rowsOk = $false; break }
        $expectedRoles = 'BASELINE_R1,BASELINE_R2,GAMEPLAY_SEED_MUTATION,MUSIC_SEED_MUTATION,EDITORIAL_MUTATION'
        $plannerRoles = (@($row.planner_variants | ForEach-Object { [string]$_.role }) -join ',')
        $runtimeRoles = (@($row.runtime_runs | ForEach-Object { [string]$_.role }) -join ',')
        if ($plannerRoles -cne $expectedRoles -or $runtimeRoles -cne $expectedRoles -or @($row.runtime_runs | Where-Object { [int]$_.exit_code -ne 0 -or [int]$_.process_id -le 0 -or [string]::IsNullOrWhiteSpace([string]$_.receipt_sha256) }).Count -ne 0) { $rowsOk = $false; break }
        foreach ($candidateProp in $row.comparison.candidate_probe_relations.PSObject.Properties) {
            if ($candidateProp.Value.gameplay_relation_pass -ne $true -or $candidateProp.Value.music_invariant_pass -ne $true -or $candidateProp.Value.editorial_invariant_pass -ne $true) { $rowsOk = $false; break }
        }
        if (-not $rowsOk) { break }
    }
}
$evidenceOk = ([string]$report.evidence.directory -eq $EvidenceDirectory -and [string]$report.runtime_contract_sha256 -eq $ExpectedContractSha -and [string]$report.design_contract_sha256 -eq $ExpectedDesignSha -and [string]$report.frozen_manifest_sha256 -eq $FrozenSha -and $report.payload_materialized -eq $false -and $report.media_created -eq $false -and [int]$report.approved_bindings -eq 0 -and [int]$report.approved_custom_data_bindings -eq 0 -and [string]$report.evidence.godot_version -eq '4.7.1.stable.mono.official.a13da4feb' -and [string]$report.evidence.implementation_test_receipt_sha256 -eq $ExpectedReceiptSha -and $null -eq $report.evidence.failure -and @($report.evidence.source_pin_errors_before_runtime).Count -eq 0 -and @($report.evidence.source_pin_errors_after_runtime).Count -eq 0)

$stdoutLines = [regex]::Split($stdoutText, "\r\n|\n|\r")
# The wrapper's Write-Host summary is captured by the interactive PowerShell host,
# not by runtime_matrix.stdout.txt. Validate report path/hash from the pinned on-disk
# evidence above; do not require those two host-only lines in the child stdout file.
$reportMetadataOk = ([IO.Path]::GetFullPath($ReportPath) -eq [IO.Path]::GetFullPath((Join-Path $EvidenceDirectory 'report.json')) -and $reportSha -eq $ExpectedReportSha)
$requiredLines = @(
    'C11D_V2B_RUNTIME_RESULT=PASS_SAFE_PROJECTION_SEED_SENSITIVITY',
    'C11D_V2B_PLANNER_INVOCATIONS=45/45',
    'C11D_V2B_GODOT_RUNTIME_PROCESSES=45/45',
    'C11D_V2B_SELECTORS=9/9',
    'C11D_V2B_GODOT_VERSION=4.7.1.stable.mono.official.a13da4feb',
    'C11D_V2B_GOVERNANCE=renderer=OFF;media_created=false;payload_materialized=false;approved_bindings=0;candidate_input_admissible=false;D4.8=BLOCKED;D9.10=PREPARE_ONLY;D10=BLOCKED_FOR_PROMOTION;release_authority=NONE'
)
$missingLines = @($requiredLines | Where-Object { [Array]::IndexOf($stdoutLines, [string]$_) -lt 0 })
$summaryOk = ($missingLines.Count -eq 0 -and $reportMetadataOk)

$SourcePins = @(
    @{Path='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json';Sha=$ExpectedContractSha},
    @{Path='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_VISUAL_PROJECTION_DESIGN_V1.json';Sha=$ExpectedDesignSha},
    @{Path='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json';Sha=$ExpectedMatrixSha},
    @{Path='tools/c11d/d9/d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py';Sha=$ExpectedRunnerSha},
    @{Path='tools/c11d/d9/challenge_visual_payload_v2b_safe_projection_runtime_in_memory.gd';Sha=$ExpectedHarnessSha},
    @{Path='tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py';Sha=$ExpectedTestSha},
    @{Path='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_RECEIPT_SCHEMA_V1.json';Sha=$ExpectedReceiptSchemaSha},
    @{Path='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_REPORT_SCHEMA_V1.json';Sha=$ExpectedReportSchemaSha},
    @{Path='definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_SCHEMA_V1.json';Sha=$ExpectedContractSchemaSha},
    @{Path='docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md';Sha=$ExpectedCheckpointSha},
    @{Path='docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md';Sha=$ExpectedLedgerSha},
    @{Path='docs/current/d/C11D_V2B_RUNTIME_STATIC_TEST_ACCEPTANCE_20261027_V1.md';Sha=$ExpectedStaticAcceptanceSha},
    @{Path='docs/current/d/C11D_V2B_RUNTIME_MATRIX_EXECUTION_RUNBOOK_20261027_V1.md';Sha=$ExpectedRunbookSha},
    @{Path='tools/c11d/d9/run_d_renderer_challenge_visual_payload_v2b_seed_matrix_20261027.ps1';Sha=$ExpectedWrapperSha}
)
$pinCount = 0
foreach ($pin in $SourcePins) {
    $path = Join-Path $ProjectRoot ($pin.Path.Replace('/','\'))
    if (-not (Test-Path -LiteralPath $path -PathType Leaf) -or (Get-FileSha256 $path) -ne $pin.Sha) { throw "Pinned source changed/missing; fail closed: $($pin.Path)" }
    $pinCount++
}
$processEvidenceCount = 0
$processEvidenceOk = $true
foreach ($prop in $report.evidence.evidence_file_sha256.PSObject.Properties) {
    if ($prop.Name.Contains('/') -or $prop.Name.Contains('\') -or [string]::IsNullOrWhiteSpace([string]$prop.Name)) { $processEvidenceOk = $false; break }
    $p = Join-Path $EvidenceDirectory $prop.Name
    if (-not (Test-Path -LiteralPath $p -PathType Leaf) -or (Get-FileSha256 $p) -ne [string]$prop.Value) { $processEvidenceOk = $false; break }
    $processEvidenceCount++
}
if ($processEvidenceCount -lt 45) { $processEvidenceOk = $false }

Write-Host ('REPORT_STATUS_VALID=' + [string]$statusOk)
Write-Host ('COUNTS_45_45_VALID=' + [string]$countsOk)
Write-Host ('SENSITIVITY_VALID=' + [string]$sensitivityOk)
Write-Host ('SELECTOR_ROWS_VALID=' + [string]$rowsOk)
Write-Host ('GOVERNANCE_LOCKS_VALID=' + [string]$governanceOk)
Write-Host ('RUNNER_SUMMARY_LINES_VALID=' + [string]($missingLines.Count -eq 0))
Write-Host ('REPORT_PATH_AND_HASH_VALID=' + [string]$reportMetadataOk)
Write-Host ('EVIDENCE_CONTRACT_VALID=' + [string]$evidenceOk)
Write-Host ('PROCESS_EVIDENCE_HASHES_VALID=' + [string]$processEvidenceOk)
Write-Host ('PROCESS_EVIDENCE_FILES_VERIFIED=' + $processEvidenceCount)
Write-Host ('SOURCE_PINS_VERIFIED=' + $pinCount + '/' + $SourcePins.Count)
if (-not $statusOk -or -not $countsOk -or -not $sensitivityOk -or -not $rowsOk -or -not $governanceOk -or -not $summaryOk -or -not $evidenceOk -or -not $processEvidenceOk) {
    Write-Host ('MISSING_SUMMARY_LINES=' + ($missingLines -join '|'))
    throw 'Existing evidence does not satisfy every runtime-matrix acceptance condition. No documents/markers changed; do not rerun the matrix.'
}

# Verify exact checkpoint/ledger preconditions before any write-back.
$cpRel = 'docs/current/d/D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md'
$ledgerRel = 'docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md'
$staticAcceptRel = 'docs/current/d/C11D_V2B_RUNTIME_STATIC_TEST_ACCEPTANCE_20261027_V1.md'
$acceptRel = 'docs/current/d/C11D_V2B_RUNTIME_MATRIX_ACCEPTANCE_20261027_V1.md'
$repairRel = 'docs/current/d/C11D_V2B_RUNTIME_MATRIX_POSTCHECK_RECOVERY_20261027_V1.md'
$cpTarget = Join-Path $ProjectRoot ($cpRel.Replace('/','\'))
$ledgerTarget = Join-Path $ProjectRoot ($ledgerRel.Replace('/','\'))
$staticAcceptTarget = Join-Path $ProjectRoot ($staticAcceptRel.Replace('/','\'))
$acceptTarget = Join-Path $ProjectRoot ($acceptRel.Replace('/','\'))
$repairTarget = Join-Path $ProjectRoot ($repairRel.Replace('/','\'))
if ((Get-FileSha256 $cpTarget) -ne $ExpectedCheckpointSha -or (Get-FileSha256 $ledgerTarget) -ne $ExpectedLedgerSha -or (Get-FileSha256 $staticAcceptTarget) -ne $ExpectedStaticAcceptanceSha) { throw 'Checkpoint/ledger/static acceptance precondition hash mismatch.' }
foreach ($target in @($acceptTarget,$repairTarget)) { if (Test-Path -LiteralPath $target) { throw "Add-only documentation destination already exists: $target" } }
$cpText = [IO.File]::ReadAllText($cpTarget, [Text.Encoding]::UTF8)
$ledgerText = [IO.File]::ReadAllText($ledgerTarget, [Text.Encoding]::UTF8)
$pendingStatus = 'V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PENDING'
if ((Count-Exact $cpText $pendingStatus) -ne 2) { throw 'Expected exactly two pending runtime status tokens in checkpoint; no document write-back.' }
$oldPhaseMarker = 'PHASE_K_CHALLENGE_COLLISION_EXPANSION_PASS; PHASE_L_V2B_STATIC_TESTS_PASS; NEXT_V2B_RUNTIME_MATRIX_GATE'
if ((Count-Exact $ledgerText $oldPhaseMarker) -ne 1) { throw 'Expected exactly one Phase L next-gate token in ledger; no document write-back.' }
$actionLines = @([regex]::Split($ledgerText, "\r\n|\n|\r") | Where-Object { $_.StartsWith('**Próxima acción única:**') -and $_.Contains('45 llamadas canónicas al planner') })
if ($actionLines.Count -ne 1) { throw 'Expected exactly one ledger next-action line for the existing runtime matrix.' }

$godotVersion = [string]$report.evidence.godot_version
$cpText = $cpText.Replace($pendingStatus, 'V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PASS; V2C_SOURCE_FRAME_RECEIPTS_PENDING')
$ledgerText = $ledgerText.Replace($oldPhaseMarker, 'PHASE_K_CHALLENGE_COLLISION_EXPANSION_PASS; PHASE_L_V2B_STATIC_TESTS_PASS; PHASE_M_V2B_RUNTIME_MATRIX_PASS; NEXT_V2C_SOURCE_FRAME_RECEIPTS_GATE')
$oldAction = $actionLines[0]
$newAction = '**Próxima acción única:** ejecutar la puerta V2-C de recibos runtime source-frame para los nueve Challenges, reutilizando el planner canónico y `ChallengeRuntimeBridge.run_effective_pipeline`; validar los recibos por selector sin materializar payload ni media y mantener el renderer apagado.'
$ledgerText = $ledgerText.Replace($oldAction, $newAction)

$phaseRecord = @"

### Fase M — Matriz V2-B de sensibilidad de estado visual seguro (27-10-2026, Windows PASS; recuperación de postcondición)

- Reporte runtime: `$ReportPath`; SHA-256 `$reportSha`; estado `PASS_SAFE_PROJECTION_SEED_SENSITIVITY`; `visual_seed_sensitivity=ACCEPTED_BY_SAFE_PROJECTION_HASH`.
- Planner canónico `45/45`; procesos independientes de Godot Mono `45/45`; selectores aceptados `9/9`; cinco variantes por selector (`BASELINE_R1`, `BASELINE_R2`, `GAMEPLAY_SEED_MUTATION`, `MUSIC_SEED_MUTATION`, `EDITORIAL_MUTATION`).
- Godot: `$godotVersion`; stdout agregado SHA-256 `$stdoutSha`; stderr SHA-256 `$stderrSha` (vacío). Se verificaron `$processEvidenceCount` archivos de evidencia por sus hashes.
- Test estático de implementación previo: `198/198`; recibo SHA-256 `$ExpectedReceiptSha`; pins estáticos `81/81` y authority-input pins `9/9` registrados en la aceptación de Fase L.
- Integridad de fuentes runtime: `$pinCount/$($SourcePins.Count)` pins confirmados; errores de pins antes/después vacíos; manifiesto congelado C11-C sin cambios.
- El wrapper original imprimió `C11D_V2B_RUNTIME_MATRIX=BLOCKED` pese a que el reporte estricto y las 45/45 ejecuciones comunicaban PASS; la comprobación post-run del wrapper no reconoció los marcadores de stdout. Esta recuperación volvió a comprobar el reporte, las nueve filas, los locks, el archivo de salida y sus líneas normalizadas, sin reejecutar la matriz ni iniciar procesos Godot.
- Alcance: evidencia de estado visual source-frame en memoria y sensibilidad de hash; **no es render de vídeo, no aprueba bindings y no admite input de candidato**.

**Siguiente puerta:** V2-C source-frame runtime receipts para los nueve Challenges mediante planner canónico y `ChallengeRuntimeBridge.run_effective_pipeline`, primero recibos en memoria y validación de contrato/pins. Mantener sin cambios la gobernanza de render.

**Bloqueos inalterados:** `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
"@
$cpText += $phaseRecord
$ledgerText += $phaseRecord
$cpText = $cpText -replace "`r`n", "`n"
$ledgerText = $ledgerText -replace "`r`n", "`n"

$acceptText = @"
# C11-D — Aceptación Windows de la matriz runtime V2-B (Fase M)

**Estado:** `WINDOWS_PASS_SAFE_PROJECTION_RUNTIME; SOURCE_FRAME_ONLY; NO_RENDER; POSTCHECK_RECOVERED`.

- Runner: `tools/c11d/d9/d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py`; reporte: `$ReportPath`.
- Report SHA-256: `$reportSha`; stdout SHA-256: `$stdoutSha`; stderr SHA-256: `$stderrSha` (vacío).
- Report status: `PASS_SAFE_PROJECTION_SEED_SENSITIVITY`; sensibilidad: `ACCEPTED_BY_SAFE_PROJECTION_HASH`.
- Invocaciones del planner canónico: `45/45`; procesos Godot Mono independientes: `45/45`; selectores: `9/9`; Godot `4.7.1.stable.mono.official.a13da4feb`.
- Las nueve filas están aceptadas, cada una con las cinco variantes de matriz; cada proceso reporta exit code `0` y recibo con SHA-256. Los hashes de los ficheros de evidencia incluidos en el propio reporte se verificaron contra el disco.
- Recibo estático precedente: `$ReceiptPath`; SHA-256 `$ExpectedReceiptSha`; `198/198` tests; `81/81` source pins; `9/9` authority-input pins.
- Wrapper PowerShell original: `C11D_V2B_RUNTIME_MATRIX=BLOCKED` en su post-check; el runner/report ya existente devolvió el estado PASS y exit code `0` indicado por la consola. El aceptador previo también exigía que dos líneas de metadatos (`C11D_V2B_RUNTIME_REPORT=` y `C11D_V2B_RUNTIME_REPORT_SHA256=`) aparecieran en el stdout del proceso secundario. El wrapper las emitió mediante `Write-Host` en la consola principal, por lo que no forman parte de esa captura. Esta recuperación verifica ruta y SHA del informe directamente desde el archivo fijado en disco, conserva la exigencia de los marcadores operacionales restantes y no vuelve a invocar el runner ni Godot.
- Log directory: `$LogDirectory`.

## Interpretación técnica

Se acepta la matriz de estado visual seguro en memoria: las repeticiones baseline son consistentes con procesos independientes; el cambio de gameplay seed cambia el hash del estado visual seguro; los cambios aislados de music seed y contenido editorial mantienen invariante dicho estado y los probes candidatos; la identidad canónica cambia para las mutaciones respectivas. La excepción de campo `CHALLENGE_003.target_x` sigue siendo una invariancia de campo, no una invariancia del estado visual completo.

Esto no valida coordenadas de entrega, remuestreo de `540×960` a `720×1280`, duración de timeline, texto dibujado, píxeles, vídeo final, binding aprobado ni admisibilidad del candidato. La discrepancia de `CHALLENGE_008/009` (11 s declarados frente a 12 s de fases) continúa bloqueada.

## Próxima puerta

`V2-C source-frame runtime receipts` para los nueve Challenges, utilizando el planner canónico y `ChallengeRuntimeBridge.run_effective_pipeline`, sin crear media ni habilitar renderer.

## Gobernanza inalterada

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
"@
$repairText = @"
# C11-D — Recuperación del post-check de la matriz V2-B

**Hallazgo:** el wrapper PowerShell emitió `C11D_V2B_RUNTIME_MATRIX=BLOCKED` aunque el reporte existente presentaba `PASS_SAFE_PROJECTION_SEED_SENSITIVITY`, exit code del runner `0`, 45 llamadas al planner y 45 procesos Godot. El chequeo de aceptación del wrapper no incluía una salida de diagnóstico por condición y bloqueó la aceptación al evaluar las líneas summary capturadas.

La recuperación no cambia el contrato, el runner Python, el harness Godot ni la matriz; no invoca el planner, Godot o los tests. Valida los hashes aceptados del reporte y stdout, la estructura estricta del reporte, los nueve selectores y cinco variantes por selector, los hashes de los archivos de evidencia, los source pins y las locks de gobernanza. La comprobación de salida exige las líneas operacionales que pertenecen al stdout del proceso; no exige `C11D_V2B_RUNTIME_REPORT=` ni `C11D_V2B_RUNTIME_REPORT_SHA256=` en ese fichero, porque esas dos líneas son emitidas por `Write-Host` del wrapper hacia la consola interactiva. Ruta y SHA del informe se comprueban directamente contra la ruta derivada del directorio de evidencia y el SHA-256 fijado. Esto elimina solo dos duplicados de presentación; no relaja las validaciones del reporte o de sus artefactos.

Resultados: report `$ExpectedReportSha`; stdout `$ExpectedStdoutSha`; stderr vacío (`$ExpectedStderrSha`); `45/45` planner; `45/45` procesos Godot Mono; `9/9` selectores aceptados. No se modifica `C11C_FREEZE_PACKAGE_MANIFEST.json`. No hay permiso para render, media, payload persistido, candidato admisible, baseline/freeze/promotion ni release.
"@

$BackupDirectory = Join-Path $env:TEMP ('C11D_PHASE_M_MATRIX_ACCEPTANCE_BACKUP_' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
Copy-Item -LiteralPath $cpTarget -Destination (Join-Path $BackupDirectory 'checkpoint.before.md')
Copy-Item -LiteralPath $ledgerTarget -Destination (Join-Path $BackupDirectory 'ledger.before.md')
$utf8 = New-Object System.Text.UTF8Encoding($false)
try {
    Write-Utf8NoBom $cpTarget $cpText
    Write-Utf8NoBom $ledgerTarget $ledgerText
    Write-Utf8NoBom $acceptTarget (($acceptText -replace "`r`n", "`n") + "`n")
    Write-Utf8NoBom $repairTarget (($repairText -replace "`r`n", "`n") + "`n")
    if ((Get-FileSha256 $ManifestPath) -ne $FrozenSha -or (Get-Item -LiteralPath $ManifestPath).Length -ne $FrozenBytes) { throw 'Frozen C11-C manifest changed during write-back.' }
    if ((Get-FileSha256 $cpTarget) -eq $ExpectedCheckpointSha -or (Get-FileSha256 $ledgerTarget) -eq $ExpectedLedgerSha) { throw 'Checkpoint/ledger hashes did not change after write-back.' }
    if ((Count-Exact ([IO.File]::ReadAllText($cpTarget, [Text.Encoding]::UTF8)) 'V2B_STATIC_TESTS_PASS; V2B_RUNTIME_MATRIX_PASS; V2C_SOURCE_FRAME_RECEIPTS_PENDING') -ne 2) { throw 'Checkpoint status write-back count is invalid.' }
    if ((Get-FileSha256 $ManifestPath) -ne $FrozenSha) { throw 'Frozen C11-C manifest changed before completion marker.' }

    $dynamicManifestPath = Join-Path $LogDirectory 'phase_m_dynamic_documentation_manifest.json'
    $dynamicManifest = [ordered]@{
        schema='C11D-DYNAMIC-PHASE-M-DOCUMENTATION-WRITEBACK-V1'; completed_utc=(Get-Date).ToUniversalTime().ToString('o')
        runtime_report_path=$ReportPath; runtime_report_sha256=$reportSha; stdout_sha256=$stdoutSha; stderr_sha256=$stderrSha
        backup_directory=$BackupDirectory; source_pins_verified=$pinCount; process_evidence_files_verified=$processEvidenceCount
        files=@(
            [ordered]@{path=$cpRel;before_sha256=$ExpectedCheckpointSha;after_sha256=(Get-FileSha256 $cpTarget)},
            [ordered]@{path=$ledgerRel;before_sha256=$ExpectedLedgerSha;after_sha256=(Get-FileSha256 $ledgerTarget)},
            [ordered]@{path=$acceptRel;before_sha256=$null;after_sha256=(Get-FileSha256 $acceptTarget)},
            [ordered]@{path=$repairRel;before_sha256=$null;after_sha256=(Get-FileSha256 $repairTarget)}
        )
    }
    Write-Utf8NoBom $dynamicManifestPath (($dynamicManifest | ConvertTo-Json -Depth 12) + "`n")
    $completion = [ordered]@{
        schema='C11D-V2B-RUNTIME-MATRIX-COMPLETION-V1'; run_id=[string]$attempt.run_id; completed_utc=(Get-Date).ToUniversalTime().ToString('o')
        status=[string]$report.status; planner_invocations=45; godot_runtime_process_invocations=45; selectors_accepted=9
        runtime_contract_sha256=$ExpectedContractSha; static_receipt_sha256=$ExpectedReceiptSha; report_path=$ReportPath; report_sha256=$reportSha
        stdout_path=$StdoutPath; stdout_sha256=$stdoutSha; stderr_path=$StderrPath; stderr_sha256=$stderrSha; log_directory=$LogDirectory
        frozen_c11c_manifest='UNCHANGED'; payload_materialized=$false; media_created=$false; renderer='OFF'; candidate_input_admissible=$false
        D4_8='BLOCKED'; release_authority='NONE'; recovered_from_wrapper_postcheck=$true; dynamic_documentation_manifest=$dynamicManifestPath
    }
    Write-Utf8NoBom $CompletionMarker (($completion | ConvertTo-Json -Depth 12) + "`n")
}
catch {
    Copy-Item -LiteralPath (Join-Path $BackupDirectory 'checkpoint.before.md') -Destination $cpTarget -Force
    Copy-Item -LiteralPath (Join-Path $BackupDirectory 'ledger.before.md') -Destination $ledgerTarget -Force
    foreach ($p in @($acceptTarget,$repairTarget)) { if (Test-Path -LiteralPath $p -PathType Leaf) { Remove-Item -LiteralPath $p -Force } }
    if (Test-Path -LiteralPath $CompletionMarker -PathType Leaf) { Remove-Item -LiteralPath $CompletionMarker -Force }
    throw
}

Write-Host 'C11D_PHASE_M_RUNTIME_MATRIX_ACCEPTANCE_RECOVERY=PASS'
Write-Host 'EXISTING_RUNTIME_EVIDENCE=VERIFIED_NOT_RERUN'
Write-Host 'REPORT_STATUS=PASS_SAFE_PROJECTION_SEED_SENSITIVITY'
Write-Host 'PLANNER_INVOCATIONS=45/45'
Write-Host 'GODOT_RUNTIME_PROCESSES=45/45'
Write-Host 'SELECTORS=9/9'
Write-Host ('SOURCE_PINS=' + $pinCount + '/' + $SourcePins.Count)
Write-Host ('PROCESS_EVIDENCE_FILES_VERIFIED=' + $processEvidenceCount)
Write-Host ('REPORT_SHA256=' + $reportSha)
Write-Host ('STDOUT_SHA256=' + $stdoutSha)
Write-Host ('STDERR_SHA256=' + $stderrSha)
Write-Host ('CHECKPOINT_SHA256=' + (Get-FileSha256 $cpTarget))
Write-Host ('LEDGER_SHA256=' + (Get-FileSha256 $ledgerTarget))
Write-Host ('ACCEPTANCE_RECORD_SHA256=' + (Get-FileSha256 $acceptTarget))
Write-Host ('RECOVERY_RECORD_SHA256=' + (Get-FileSha256 $repairTarget))
Write-Host ('LOG_DIRECTORY=' + $LogDirectory)
Write-Host ('BACKUP_DIRECTORY=' + $BackupDirectory)
Write-Host ('COMPLETION_MARKER=' + $CompletionMarker)
Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
Write-Host 'RENDERER=OFF'
Write-Host 'MEDIA_CREATED=false'
Write-Host 'PAYLOAD_MATERIALIZED=false'
Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
Write-Host 'D4.8=BLOCKED'
Write-Host 'RELEASE_AUTHORITY=NONE'
