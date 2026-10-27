# C11-D V2-B runtime matrix runner (Phase M)
# Windows PowerShell 5.1; no extraction; no payload/media/renderer dispatch.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$ExpectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
$ProjectRoot = [System.IO.Path]::GetFullPath((Get-Location).Path).TrimEnd('\')
if (-not [string]::Equals($ProjectRoot, $ExpectedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Ejecuta desde la raíz exacta del checkout: $ExpectedRoot. Actual: $ProjectRoot"
}
function Get-FileSha256([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Write-Utf8NoBom([string]$Path, [string]$Text) { [System.IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false))) }
function Quote-Arg([string]$Value) { return '"' + $Value.Replace('"','\"') + '"' }

$FrozenSha = 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
$FrozenBytes = 796318
$ExpectedContractSha = 'f89235640f40c81be6100f01f1007ed4e787990a1bbf7927fcd8d676ef2cb9a3'
$ExpectedRunnerSha = '6a92aac96786acd2316f8e46b9d895f7cdcdfccbd75e9686378a4144a3a01a7f'
$ExpectedHarnessSha = 'aa175afe2ce357473aa46ed7c55ce46edf3f56457db461be28f7ec8e2f0b5ce2'
$ExpectedMatrixSha = 'd69c3fb2aca78a26c3afbfda0084f7f7aef458ee404b37f65261c6d22e43121a'
$ExpectedReceiptSha = 'aa8cebd453b632e445becb936ff3520110d5f80fdf2a732818a6917885595e32'
$ExpectedCheckpointSha = '93c07fd260e1cb56870e8448882f330a91b523fa735cad844ba2d941f041953b'
$ExpectedLedgerSha = '7155a14a03cd4a24e0eed00d04fefe086ea355e041f56bb1e2d2d485ac50121d'
$ExpectedAcceptanceSha = '9be3d49f5498f87783c30db69fa0e6a47d0721a17b86258926077c7d10933d8f'

$ManifestPath = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
if ((Get-Item -LiteralPath $ManifestPath -ErrorAction Stop).Length -ne $FrozenBytes -or (Get-FileSha256 $ManifestPath) -ne $FrozenSha) { throw 'Manifiesto C11-C congelado distinto; no se ejecuta la matriz.' }
$checkpoint = Join-Path $ProjectRoot 'docs\current\d\D_RENDERER_REQUEST_PAYLOAD_INSTANCE_INTEGRATION_CHECKPOINT_V2_2.md'
$ledger = Join-Path $ProjectRoot 'docs\current\d\C11D_ENGINEERING_PHASE_LEDGER_20261027_V1.md'
$acceptance = Join-Path $ProjectRoot 'docs\current\d\C11D_V2B_RUNTIME_STATIC_TEST_ACCEPTANCE_20261027_V1.md'
$documentChecks = @(
    [pscustomobject]@{ Path = $checkpoint; Sha = $ExpectedCheckpointSha },
    [pscustomobject]@{ Path = $ledger; Sha = $ExpectedLedgerSha },
    [pscustomobject]@{ Path = $acceptance; Sha = $ExpectedAcceptanceSha }
)
foreach ($pair in $documentChecks) {
    if (-not (Test-Path -LiteralPath $pair.Path -PathType Leaf) -or (Get-FileSha256 $pair.Path) -ne $pair.Sha) { throw "Documento de fase L no coincide con aceptación: $($pair.Path)" }
}

$staticCompletion = Join-Path $env:TEMP 'C11D_PHASE_KL_V2B_STATIC_GATE_20261027.completed.json'
if (-not (Test-Path -LiteralPath $staticCompletion -PathType Leaf)) { throw "Falta el completion marker del gate estático: $staticCompletion" }
$static = Get-Content -LiteralPath $staticCompletion -Raw -Encoding UTF8 | ConvertFrom-Json
if ([string]$static.schema -ne 'C11D-PHASE-KL-V2B-STATIC-GATE-COMPLETION-V1' -or [string]$static.V2B_static_tests -ne 'PASS_198_OF_198' -or [string]$static.source_pins -ne '81/81' -or [string]$static.authority_input_pins -ne '9/9' -or [int]$static.runtime_invocations -ne 0 -or [string]$static.static_receipt_sha256 -ne $ExpectedReceiptSha) { throw 'Completion marker del gate estático no demuestra exactamente la evidencia aceptada.' }
$ReceiptPath = [System.IO.Path]::GetFullPath([string]$static.static_receipt_path)
if (-not (Test-Path -LiteralPath $ReceiptPath -PathType Leaf) -or (Get-FileSha256 $ReceiptPath) -ne $ExpectedReceiptSha) { throw "Recibo de implementación ausente o con SHA incorrecto: $ReceiptPath" }

$Contract = Join-Path $ProjectRoot 'definitions\c11d\production\D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SAFE_PROJECTION_RUNTIME_CONTRACT_V1.json'
$Matrix = Join-Path $ProjectRoot 'definitions\c11d\production\D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2B_SEED_TEST_MATRIX_V1.json'
$Runner = Join-Path $ProjectRoot 'tools\c11d\d9\d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py'
$Harness = Join-Path $ProjectRoot 'tools\c11d\d9\challenge_visual_payload_v2b_safe_projection_runtime_in_memory.gd'
$sourceChecks = @(
    [pscustomobject]@{ Path = $Contract; Sha = $ExpectedContractSha },
    [pscustomobject]@{ Path = $Runner; Sha = $ExpectedRunnerSha },
    [pscustomobject]@{ Path = $Harness; Sha = $ExpectedHarnessSha },
    [pscustomobject]@{ Path = $Matrix; Sha = $ExpectedMatrixSha }
)
foreach ($pair in $sourceChecks) {
    if (-not (Test-Path -LiteralPath $pair.Path -PathType Leaf) -or (Get-FileSha256 $pair.Path) -ne $pair.Sha) { throw "Fuente runtime matrix no coincide con su pin: $($pair.Path)" }
}

$Godot = 'C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe'
if (-not (Test-Path -LiteralPath $Godot -PathType Leaf)) { throw "No se encuentra el ejecutable Godot Mono fijado por la prueba previa: $Godot" }
$Python = (Get-Command python -ErrorAction Stop).Source

$AttemptMarker = Join-Path $env:TEMP 'C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027.started.json'
$CompletionMarker = Join-Path $env:TEMP 'C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027.completed.json'
if (Test-Path -LiteralPath $CompletionMarker) { throw "La matriz ya tiene completion marker; no se repite: $CompletionMarker" }
if (Test-Path -LiteralPath $AttemptMarker) { throw "Hay un intento previo de matriz; no se relanza a ciegas. Conserva evidencia: $AttemptMarker" }
$RunId = [Guid]::NewGuid().ToString('N')
$LogDirectory = Join-Path $env:TEMP ("C11D_V2B_SAFE_PROJECTION_RUNTIME_MATRIX_20261027_" + $RunId)
$EvidenceDirectory = Join-Path $LogDirectory 'process_evidence'
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
$stdout = Join-Path $LogDirectory 'runtime_matrix.stdout.txt'
$stderr = Join-Path $LogDirectory 'runtime_matrix.stderr.txt'
$reportPath = Join-Path $EvidenceDirectory 'report.json'
$attempt = [ordered]@{schema='C11D-V2B-RUNTIME-MATRIX-ATTEMPT-V1';run_id=$RunId;started_utc=(Get-Date).ToUniversalTime().ToString('o');project_root=$ProjectRoot;static_receipt_path=$ReceiptPath;static_receipt_sha256=$ExpectedReceiptSha;log_directory=$LogDirectory;evidence_directory=$EvidenceDirectory}
Write-Utf8NoBom $AttemptMarker (($attempt | ConvertTo-Json -Depth 8) + "`n")

$argValues = @('-B',$Runner,'--repo-root',$ProjectRoot,'--evidence-dir',$EvidenceDirectory,'--implementation-test-receipt',$ReceiptPath,'--contract-sha256',$ExpectedContractSha,'--godot',$Godot)
$argLine = (($argValues | ForEach-Object { Quote-Arg ([string]$_) }) -join ' ')
$proc = Start-Process -FilePath $Python -ArgumentList $argLine -WorkingDirectory $ProjectRoot -NoNewWindow -PassThru -Wait -RedirectStandardOutput $stdout -RedirectStandardError $stderr
$exitCode = [int]$proc.ExitCode
$stdoutText = [System.IO.File]::ReadAllText($stdout)
$stderrText = [System.IO.File]::ReadAllText($stderr)
$stdoutSha = Get-FileSha256 $stdout
$stderrSha = Get-FileSha256 $stderr
$reportSha = $null
if (Test-Path -LiteralPath $reportPath -PathType Leaf) { $reportSha = Get-FileSha256 $reportPath }

if (-not (Test-Path -LiteralPath $reportPath -PathType Leaf)) { throw "El runner no produjo reporte; exit=$exitCode. Logs: $LogDirectory" }
$report = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
$expectedStatus = 'PASS_SAFE_PROJECTION_SEED_SENSITIVITY'
$governanceOk = ([string]$report.governance_locks.renderer -eq 'OFF' -and $report.governance_locks.media_created -eq $false -and $report.governance_locks.payload_materialized -eq $false -and $report.governance_locks.candidate_input_admissible -eq $false -and $report.governance_locks.'D4.8' -eq 'BLOCKED' -and $report.governance_locks.release_authority -eq 'NONE')
$rowsOk = ($report.selectors.Count -eq 9 -and @($report.selectors | Where-Object { $_.status -eq 'ACCEPTED_SAFE_PROJECTION_RUNTIME' }).Count -eq 9)
$summaryOk = ($stdoutText -match '(?m)^C11D_V2B_RUNTIME_RESULT=PASS_SAFE_PROJECTION_SEED_SENSITIVITY$' -and $stdoutText -match '(?m)^C11D_V2B_PLANNER_INVOCATIONS=45/45$' -and $stdoutText -match '(?m)^C11D_V2B_GODOT_RUNTIME_PROCESSES=45/45$' -and $stdoutText -match '(?m)^C11D_V2B_SELECTORS=9/9$')
if ($exitCode -ne 0 -or [string]$report.status -ne $expectedStatus -or [int]$report.planner_invocations -ne 45 -or [int]$report.godot_runtime_process_invocations -ne 45 -or [string]$report.visual_seed_sensitivity -ne 'ACCEPTED_BY_SAFE_PROJECTION_HASH' -or -not $rowsOk -or -not $summaryOk -or -not $governanceOk) {
    Write-Host 'C11D_V2B_RUNTIME_MATRIX=BLOCKED'
    Write-Host ("EXIT_CODE=" + $exitCode)
    Write-Host ("REPORT_STATUS=" + [string]$report.status)
    Write-Host ("PLANNER_INVOCATIONS=" + [string]$report.planner_invocations + '/45')
    Write-Host ("GODOT_RUNTIME_PROCESSES=" + [string]$report.godot_runtime_process_invocations + '/45')
    Write-Host ("REPORT_SHA256=" + $reportSha)
    Write-Host ("STDOUT_SHA256=" + $stdoutSha)
    Write-Host ("STDERR_SHA256=" + $stderrSha)
    Write-Host ("LOG_DIRECTORY=" + $LogDirectory)
    Write-Host ("REPORT_FILE=" + $reportPath)
    Write-Host 'RENDERER=OFF;MEDIA_CREATED=false;PAYLOAD_MATERIALIZED=false;CANDIDATE_INPUT_ADMISSIBLE=false;D4.8=BLOCKED;RELEASE_AUTHORITY=NONE'
    throw 'La matriz no cumple las condiciones de aceptación; conservar logs y no relanzar a ciegas.'
}

if ((Get-FileSha256 $ManifestPath) -ne $FrozenSha -or (Get-Item -LiteralPath $ManifestPath).Length -ne $FrozenBytes) { throw 'El manifiesto C11-C no coincide después de la matriz.' }
$completion = [ordered]@{schema='C11D-V2B-RUNTIME-MATRIX-COMPLETION-V1';run_id=$RunId;completed_utc=(Get-Date).ToUniversalTime().ToString('o');status=[string]$report.status;planner_invocations=[int]$report.planner_invocations;godot_runtime_process_invocations=[int]$report.godot_runtime_process_invocations;selectors_accepted=9;runtime_contract_sha256=$ExpectedContractSha;static_receipt_sha256=$ExpectedReceiptSha;report_path=$reportPath;report_sha256=$reportSha;stdout_path=$stdout;stdout_sha256=$stdoutSha;stderr_path=$stderr;stderr_sha256=$stderrSha;log_directory=$LogDirectory;frozen_c11c_manifest='UNCHANGED';payload_materialized=$false;media_created=$false;renderer='OFF';candidate_input_admissible=$false;D4_8='BLOCKED';release_authority='NONE'}
Write-Utf8NoBom $CompletionMarker (($completion | ConvertTo-Json -Depth 10) + "`n")
Write-Host 'C11D_V2B_RUNTIME_MATRIX=PASS'
Write-Host 'V2B_SOURCE_STATE_SEED_SENSITIVITY=PASS'
Write-Host 'SELECTORS=9/9'
Write-Host 'CANONICAL_PLANNER_INVOCATIONS=45/45'
Write-Host 'INDEPENDENT_GODOT_MONO_PROCESSES=45/45'
Write-Host ('GODOT_VERSION=' + [string]$report.evidence.godot_version)
Write-Host ('STATIC_RECEIPT_SHA256=' + $ExpectedReceiptSha)
Write-Host ('REPORT_SHA256=' + $reportSha)
Write-Host ('STDOUT_SHA256=' + $stdoutSha)
Write-Host ('STDERR_SHA256=' + $stderrSha)
Write-Host ('LOG_DIRECTORY=' + $LogDirectory)
Write-Host ('REPORT_FILE=' + $reportPath)
Write-Host ('COMPLETION_MARKER=' + $CompletionMarker)
Write-Host 'FROZEN_C11C_MANIFEST=UNCHANGED'
Write-Host 'PAYLOAD_MATERIALIZED=false'
Write-Host 'MEDIA_CREATED=false'
Write-Host 'RENDERER=OFF'
Write-Host 'CANDIDATE_INPUT_ADMISSIBLE=false'
Write-Host 'D4.8=BLOCKED'
Write-Host 'RELEASE_AUTHORITY=NONE'
