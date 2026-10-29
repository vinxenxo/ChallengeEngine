[CmdletBinding()]
param([string]$GodotExecutable = '')
$ErrorActionPreference = 'Stop'
$repoRoot = (Get-Location).Path
if (-not (Test-Path -LiteralPath (Join-Path $repoRoot 'project.godot') -PathType Leaf)) { throw 'Ejecuta el runner desde la raiz del repositorio.' }
$manifestPath = Join-Path $repoRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
$manifestInfo = Get-Item -LiteralPath $manifestPath
$manifestHash = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($manifestInfo.Length -ne 796318 -or $manifestHash -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953') { throw 'FROZEN_C11C_MANIFEST_SHA_OR_SIZE_MISMATCH; se detiene sin lanzar Godot.' }
$contractPath = Join-Path $repoRoot 'definitions\c11d\production\D_RENDERER_PHASE_P_SOURCE_VALUE_VS_FRAME_VALUE_PROVENANCE_CONTRACT_V1.json'
$contract = Get-Content -LiteralPath $contractPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($contract.schema -ne 'C11D-PHASE-P-SOURCE-VALUE-FRAME-VALUE-PROVENANCE-CONTRACT-V1' -or $contract.source_pin_count -ne $contract.source_pins.Count -or $contract.expected_selector_count -ne 6 -or $contract.independent_processes_per_selector -ne 2) { throw 'PHASE_P_CONTRACT_DENOMINATOR_OR_IDENTITY_INVALID' }
$pythonLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
if (-not $pythonLauncher) { $pythonLauncher = Get-Command py -ErrorAction SilentlyContinue }
if (-not $pythonLauncher) { throw 'Python launcher py.exe not found.' }
$pythonVersionOutput = ((& $pythonLauncher.Source -3.13 --version 2>&1 | Out-String).Trim() -replace '^Python\s+', '')
$pythonVersionExitCode = $LASTEXITCODE
$pythonVersionText = (@($pythonVersionOutput) -join ' ').Trim()
$pythonVersionText = ([string]$pythonVersionText).Trim() -replace '^[^\d]*', ''
if ($pythonVersionExitCode -ne 0 -or $pythonVersionText -notmatch '^3\.13(?:\.|$)') { throw ('PYTHON_313_REQUIRED: ' + $pythonVersionText) }
$pythonExecutableOutput = & $pythonLauncher.Source -3.13 -c 'import sys; print(sys.executable)' 2>&1
$pythonExecutableExitCode = $LASTEXITCODE
$pythonExecutableText = (@($pythonExecutableOutput) -join "`n").Trim()
if ($pythonExecutableExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($pythonExecutableText) -or @($pythonExecutableOutput).Count -ne 1 -or -not (Test-Path -LiteralPath $pythonExecutableText -PathType Leaf)) { throw ('PYTHON_313_EXECUTABLE_REQUIRED: ' + $pythonExecutableText) }
$pythonExe = $pythonExecutableText
$testPath = Join-Path $repoRoot 'tools\c11d\d9\test_d_renderer_phase_p_source_value_frame_value_provenance_20261028.py'
$testOut = Join-Path $env:TEMP ('C11D_PHASE_P_STATIC_' + [guid]::NewGuid().ToString('N') + '.stdout.txt')
$testErr = Join-Path $env:TEMP ('C11D_PHASE_P_STATIC_' + [guid]::NewGuid().ToString('N') + '.stderr.txt')
$testProc = Start-Process -FilePath $pythonExe -ArgumentList @('-B', ('"' + $testPath + '"')) -WorkingDirectory $repoRoot -PassThru -Wait -NoNewWindow -RedirectStandardOutput $testOut -RedirectStandardError $testErr
$testOutput = Get-Content -LiteralPath $testOut -Raw
$testError = Get-Content -LiteralPath $testErr -Raw
$testPass = $testOutput -match 'PHASE_P_IMPLEMENTATION_STATIC_TESTS=\d+/\d+' -and $testOutput -match 'PHASE_P_IMPLEMENTATION_STATIC_TESTS=(\d+)/\1' -and $testProc.ExitCode -eq 0 -and [string]::IsNullOrWhiteSpace($testError)
if (-not $testPass) { Write-Output 'C11D_PHASE_P_STATIC_GATE=BLOCKED'; Write-Output ('STATIC_STDOUT=' + $testOut); Write-Output ('STATIC_STDERR=' + $testErr); if ($testOutput) { Write-Output $testOutput }; if ($testError) { Write-Output $testError }; throw 'Phase P static tests failed; runtime matrix was not started.' }
$runScript = Join-Path $repoRoot 'tools\c11d\d9\audit_d_renderer_phase_p_source_value_frame_value_provenance_20261028.py'
$evidenceDir = Join-Path $env:TEMP ('C11D_PHASE_P_SOURCE_VALUE_FRAME_PROVENANCE_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $evidenceDir | Out-Null
$auditDir = Join-Path $evidenceDir 'audit'
$runnerOut = Join-Path $evidenceDir 'runner.stdout.txt'
$runnerErr = Join-Path $evidenceDir 'runner.stderr.txt'
$args = @('-B', ('"' + $runScript + '"'), '--repo-root', ('"' + $repoRoot + '"'), '--evidence-dir', ('"' + $auditDir + '"'))
if (-not [string]::IsNullOrWhiteSpace($GodotExecutable)) { $args += @('--godot', ('"' + $GodotExecutable + '"')) }
$runProc = Start-Process -FilePath $pythonExe -ArgumentList $args -WorkingDirectory $repoRoot -PassThru -Wait -NoNewWindow -RedirectStandardOutput $runnerOut -RedirectStandardError $runnerErr
$runnerText = Get-Content -LiteralPath $runnerOut -Raw
$runnerErrorText = Get-Content -LiteralPath $runnerErr -Raw
$reportPath = Join-Path $auditDir 'phase_p_provenance_report.json'
if ($runProc.ExitCode -ne 0 -or $runnerText -notmatch 'C11D_PHASE_P_SOURCE_VALUE_FRAME_VALUE_PROVENANCE_AUDIT=PASS_SOURCE_FRAME_PROVENANCE_ONLY_NO_BINDING_APPROVAL' -or -not (Test-Path -LiteralPath $reportPath -PathType Leaf)) {
    Write-Output 'C11D_PHASE_P_RUNTIME_AUDIT=BLOCKED'
    Write-Output ('EVIDENCE_DIR=' + $evidenceDir)
    Write-Output ('RUNNER_STDOUT=' + $runnerOut)
    Write-Output ('RUNNER_STDERR=' + $runnerErr)
    if ($runnerText) { Write-Output $runnerText }
    if ($runnerErrorText) { Write-Output $runnerErrorText }
    throw 'Phase P runtime audit failed closed. Preserve this evidence directory; do not rerun blindly.'
}
$report = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($report.status -ne 'PASS_SOURCE_FRAME_PROVENANCE_ONLY_NO_BINDING_APPROVAL' -or $report.selector_count -ne 6 -or $report.canonical_planner_invocations -ne 6 -or $report.godot_runtime_process_invocations -ne 12 -or $report.approved_bindings -ne 0 -or $report.approved_custom_data_bindings -ne 0 -or $report.renderer -ne 'OFF' -or $report.release_authority -ne 'NONE') { throw 'PHASE_P_REPORT_POSTCONDITION_FAILED; evidence retained at ' + $evidenceDir }
$reportHash = (Get-FileHash -LiteralPath $reportPath -Algorithm SHA256).Hash.ToLowerInvariant()
$stdoutHash = (Get-FileHash -LiteralPath $runnerOut -Algorithm SHA256).Hash.ToLowerInvariant()
$stderrHash = (Get-FileHash -LiteralPath $runnerErr -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Output 'C11D_PHASE_P_SOURCE_VALUE_FRAME_VALUE_PROVENANCE_RUNTIME=PASS_PENDING_FORMAL_ACCEPTANCE'
Write-Output 'SELECTORS=6/6; CANONICAL_PLANNER_INVOCATIONS=6/6; GODOT_RUNTIME_PROCESSES=12/12'
Write-Output 'ACTUAL_CANDIDATE_VALUES_SERIALIZED=false; WHOLE_CUSTOM_DATA_MAP_SERIALIZED=false'
Write-Output 'RENDERER=OFF; MEDIA_CREATED=false; PAYLOAD_MATERIALIZED=false; APPROVED_BINDINGS=0; RELEASE_AUTHORITY=NONE'
Write-Output ('EVIDENCE_DIR=' + $evidenceDir)
Write-Output ('REPORT_SHA256=' + $reportHash)
Write-Output ('RUNNER_STDOUT_SHA256=' + $stdoutHash)
Write-Output ('RUNNER_STDERR_SHA256=' + $stderrHash)
Write-Output ('STATIC_TEST_STDOUT=' + $testOut)
Write-Output ('STATIC_TEST_STDERR=' + $testErr)
