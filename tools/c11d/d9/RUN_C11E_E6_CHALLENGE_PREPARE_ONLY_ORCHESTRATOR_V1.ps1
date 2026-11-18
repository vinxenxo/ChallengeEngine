[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ProjectRoot,
    [Parameter(Mandatory = $true)][string]$PythonExe
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$global:LASTEXITCODE = 1

function Assert-PathInsideRoot {
    param([string]$Root, [string]$RelativePath)
    if ([string]::IsNullOrWhiteSpace($RelativePath) -or $RelativePath.Contains('..') -or $RelativePath.Contains(':') -or $RelativePath.Contains('\')) {
        throw "UNSAFE_RELATIVE_PATH:$RelativePath"
    }
    $FullRoot = [System.IO.Path]::GetFullPath($Root).TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
    $FullPath = [System.IO.Path]::GetFullPath((Join-Path $Root ($RelativePath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))))
    if (-not $FullPath.StartsWith($FullRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "PATH_OUTSIDE_PROJECT_ROOT:$RelativePath"
    }
    $Cursor = $FullPath
    while ($Cursor.StartsWith($FullRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        if (Test-Path -LiteralPath $Cursor) {
            $Item = Get-Item -LiteralPath $Cursor -Force
            if (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "EVIDENCE_PATH_REPARSE_POINT:$Cursor"
            }
        }
        $Next = Split-Path -Parent $Cursor
        if ($Next -eq $Cursor) { break }
        $Cursor = $Next
    }
    return $FullPath
}

function Get-Sha256 {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "FILE_MISSING:$Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function ConvertTo-Win32Argument {
    param([string]$Value)
    if ($null -eq $Value) { $Value = '' }
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
    $Builder = New-Object System.Text.StringBuilder
    [void]$Builder.Append('"')
    $Backslashes = 0
    for ($Index = 0; $Index -lt $Value.Length; $Index++) {
        $Character = $Value[$Index]
        if ($Character -eq '\') {
            $Backslashes++
            continue
        }
        if ($Character -eq '"') {
            if ($Backslashes -gt 0) { [void]$Builder.Append(('\' * (2 * $Backslashes + 1))) }
            else { [void]$Builder.Append('\') }
            [void]$Builder.Append('"')
            $Backslashes = 0
            continue
        }
        if ($Backslashes -gt 0) {
            [void]$Builder.Append(('\' * $Backslashes))
            $Backslashes = 0
        }
        [void]$Builder.Append($Character)
    }
    if ($Backslashes -gt 0) { [void]$Builder.Append(('\' * (2 * $Backslashes))) }
    [void]$Builder.Append('"')
    return $Builder.ToString()
}

function Invoke-CapturedProcess {
    param(
        [string]$FilePath,
        [string[]]$Arguments,
        [string]$WorkingDirectory,
        [hashtable]$Environment = @{}
    )
    $Psi = New-Object System.Diagnostics.ProcessStartInfo
    $Psi.FileName = $FilePath
    $Quoted = @()
    foreach ($Argument in $Arguments) { $Quoted += (ConvertTo-Win32Argument $Argument) }
    $Psi.Arguments = [string]::Join(' ', $Quoted)
    $Psi.WorkingDirectory = $WorkingDirectory
    $Psi.UseShellExecute = $false
    $Psi.CreateNoWindow = $true
    $Psi.RedirectStandardOutput = $true
    $Psi.RedirectStandardError = $true
    foreach ($Key in $Environment.Keys) { $Psi.EnvironmentVariables[$Key] = [string]$Environment[$Key] }

    $Process = New-Object System.Diagnostics.Process
    $Process.StartInfo = $Psi
    if (-not $Process.Start()) { throw "PROCESS_START_FAILED:$FilePath" }
    $StdoutTask = $Process.StandardOutput.ReadToEndAsync()
    $StderrTask = $Process.StandardError.ReadToEndAsync()
    $Process.WaitForExit()
    $Stdout = $StdoutTask.Result
    $Stderr = $StderrTask.Result
    $ExitCode = $Process.ExitCode
    $Process.Dispose()
    if ($Stdout) { Write-Host $Stdout.TrimEnd() }
    if ($Stderr) { Write-Host $Stderr.TrimEnd() }
    return [pscustomobject]@{ ExitCode = $ExitCode; Stdout = $Stdout; Stderr = $Stderr }
}

try {
    if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) {
        throw "WINDOWS_POWERSHELL_5_1_REQUIRED:$($PSVersionTable.PSVersion)"
    }
    $Tokens = $null
    $ParseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath, [ref]$Tokens, [ref]$ParseErrors) | Out-Null
    if ($ParseErrors.Count -gt 0) { throw 'RUNNER_POWERSHELL_5_1_AST_PARSE_FAILED' }
    Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/RUNNER'

    $ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
    if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw "PROJECT_ROOT_NOT_FOUND:$ProjectRoot" }
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "PYTHON_EXE_NOT_FOUND:$PythonExe" }
    Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED'

    $Version = Invoke-CapturedProcess -FilePath $PythonExe -Arguments @('--version') -WorkingDirectory $ProjectRoot
    if ($Version.ExitCode -ne 0 -or ($Version.Stdout + $Version.Stderr) -notmatch 'Python 3\.13\.14') {
        throw "PYTHON_VERSION_REQUIRED_3_13_14:$($Version.Stdout)$($Version.Stderr)"
    }
    Write-Host 'PYTHON_VERSION=PASS/3.13.14'

    $InstallRoot = Join-Path $ProjectRoot 'artifacts\tests\c11e\e6_challenge_prepare_only_install'
    if (-not (Test-Path -LiteralPath $InstallRoot -PathType Container)) { throw 'INSTALL_EVIDENCE_ROOT_MISSING' }
    $ReceiptFiles = @(Get-ChildItem -LiteralPath $InstallRoot -Filter 'INSTALL_RECEIPT_V1.json' -File -Recurse | Sort-Object LastWriteTimeUtc -Descending)
    $InstallReceiptPath = $null
    $InstallReceipt = $null
    foreach ($Candidate in $ReceiptFiles) {
        try {
            $CandidateReceipt = Get-Content -LiteralPath $Candidate.FullName -Raw | ConvertFrom-Json
            if ($CandidateReceipt.overlay_id -eq 'C11E_E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_V1' -and
                $CandidateReceipt.status -eq 'PASS_ADD_ONLY_E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_INSTALL' -and
                $CandidateReceipt.tests.executed -eq 40 -and $CandidateReceipt.tests.failed -eq 0 -and
                $CandidateReceipt.tests.errors -eq 0 -and $CandidateReceipt.tests.skipped -eq 0 -and
                $CandidateReceipt.tests.status -eq 'PASS') {
                $InstallReceiptPath = $Candidate.FullName
                $InstallReceipt = $CandidateReceipt
                break
            }
        } catch { }
    }
    if ($null -eq $InstallReceipt) { throw 'NO_VALID_PASS_INSTALL_RECEIPT_WITH_40_TESTS' }

    foreach ($Payload in $InstallReceipt.payload_files) {
        $Destination = Assert-PathInsideRoot -Root $ProjectRoot -RelativePath $Payload.path
        if (-not (Test-Path -LiteralPath $Destination -PathType Leaf)) { throw "INSTALLED_PAYLOAD_MISSING:$($Payload.path)" }
        $Item = Get-Item -LiteralPath $Destination
        if ($Item.Length -ne $Payload.bytes) { throw "INSTALLED_PAYLOAD_SIZE_MISMATCH:$($Payload.path)" }
        $Actual = Get-Sha256 $Destination
        if ($Actual -ne $Payload.sha256) { throw "INSTALLED_PAYLOAD_SHA256_MISMATCH:$($Payload.path):$Actual" }
    }
    if ($InstallReceipt.payload_files.Count -ne 8) { throw 'INSTALL_RECEIPT_PAYLOAD_COUNT_MISMATCH' }
    Write-Host 'INSTALL_RECEIPT=PASS/8_PAYLOADS/40_TESTS'

    $PinsRel = 'definitions/c11d/production/C11E_E6_CHALLENGE_PREPARE_ONLY_SOURCE_PINS_V1.json'
    $PinsPath = Assert-PathInsideRoot -Root $ProjectRoot -RelativePath $PinsRel
    $ExpectedPinsSha = '3b2333b2ae02158f27363577069dba519bff3975714d1cd95e569728425a09b6'
    $PinsSha = Get-Sha256 $PinsPath
    if ($PinsSha -ne $ExpectedPinsSha) { throw "SOURCE_PIN_DOCUMENT_SHA256_MISMATCH:$PinsSha" }
    Write-Host 'SOURCE_PIN_DOCUMENT=PASS'

    $RunStamp = [DateTime]::UtcNow.ToString("yyyyMMdd'T'HHmmss'Z'")
    $RunGuid = [Guid]::NewGuid().ToString('N').Substring(0, 8).ToUpperInvariant()
    $RunId = "E6CHPREP_${RunStamp}_${RunGuid}"
    $Orchestrator = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_challenge_prepare_only_orchestrator_v1.py'
    if (-not (Test-Path -LiteralPath $Orchestrator -PathType Leaf)) { throw 'ORCHESTRATOR_PAYLOAD_MISSING' }

    $Run = Invoke-CapturedProcess -FilePath $PythonExe `
        -Arguments @($Orchestrator, '--project-root', $ProjectRoot, '--run-id', $RunId) `
        -WorkingDirectory $ProjectRoot `
        -Environment @{ C11E_PROJECT_ROOT = $ProjectRoot; PYTHONUTF8 = '1' }
    if ($Run.ExitCode -ne 0) { throw "E6_PREPARE_ONLY_ORCHESTRATOR_EXIT:$($Run.ExitCode)" }

    $RunRoot = Join-Path $ProjectRoot (Join-Path 'artifacts\tests\c11e\e6_challenge_prepare_only_orchestrator' $RunId)
    $ReceiptPath = Join-Path $RunRoot 'E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_RECEIPT_V1.json'
    $SidecarPath = $ReceiptPath + '.sha256'
    if (-not (Test-Path -LiteralPath $ReceiptPath -PathType Leaf)) { throw 'ORCHESTRATOR_RECEIPT_MISSING' }
    if (-not (Test-Path -LiteralPath $SidecarPath -PathType Leaf)) { throw 'ORCHESTRATOR_RECEIPT_SIDECAR_MISSING' }

    $ReceiptSha = Get-Sha256 $ReceiptPath
    $SidecarText = (Get-Content -LiteralPath $SidecarPath -Raw).Trim()
    $ExpectedSidecarText = "$ReceiptSha  $(Split-Path -Leaf $ReceiptPath)"
    if ($SidecarText -ne $ExpectedSidecarText) { throw 'ORCHESTRATOR_RECEIPT_SIDECAR_CONTENT_MISMATCH' }
    $Receipt = Get-Content -LiteralPath $ReceiptPath -Raw | ConvertFrom-Json
    if ($Receipt.status -ne 'PASS_PREPARE_ONLY_18_E1_INTENTS_18_D_ENVELOPES_EXECUTION_HELD') { throw "ORCHESTRATOR_RECEIPT_STATUS_MISMATCH:$($Receipt.status)" }
    if ($Receipt.counts.challenge_scenario_groups -ne 6 -or $Receipt.counts.challenge_probe_subruns -ne 18 -or
        $Receipt.counts.e1_intents -ne 18 -or $Receipt.counts.d_envelopes -ne 18) { throw 'ORCHESTRATOR_RECEIPT_COUNTS_MISMATCH' }
    if ($Receipt.governance.e1 -ne 'PREPARE_ONLY' -or $Receipt.governance.d4_8 -ne 'BLOCKED' -or $Receipt.governance.d4_8_overridden -ne $false -or
        $Receipt.governance.renderer -ne 'OFF' -or $Receipt.governance.release_authority -ne 'NONE' -or
        $Receipt.governance.e6_accepted_scenarios -ne 0 -or $Receipt.governance.e6_matrix_frozen -ne $false -or
        $Receipt.execution.mode -ne 'PREPARE_ONLY' -or $Receipt.execution.e6_test_only_authorized -ne $false -or
        $Receipt.execution.godot_invoked -ne $false -or $Receipt.execution.renderer_invoked -ne $false -or
        $Receipt.execution.ffmpeg_invoked -ne $false -or $Receipt.execution.ffprobe_invoked -ne $false -or
        $Receipt.execution.audio_generated -ne $false -or $Receipt.execution.mux_invoked -ne $false -or
        $Receipt.execution.media_created -ne $false -or $Receipt.execution.production_dispatch -ne $false -or
        $Receipt.execution.batch_id_consumed -ne $false -or $Receipt.execution.runtime_commands_emitted -ne $false) {
        throw 'ORCHESTRATOR_GOVERNANCE_BOUNDARY_MISMATCH'
    }
    if ($Receipt.input_manifest.sha256 -ne $Receipt.input_manifest.copy_sha256) { throw 'INPUT_MANIFEST_COPY_HASH_REFERENCE_MISMATCH' }
    $InputCopyPath = Assert-PathInsideRoot -Root $ProjectRoot -RelativePath $Receipt.input_manifest.copy_path
    if ((Get-Sha256 $InputCopyPath) -ne $Receipt.input_manifest.copy_sha256) { throw 'INPUT_MANIFEST_COPY_SHA256_MISMATCH' }
    $InputCopySidecarPath = Assert-PathInsideRoot -Root $ProjectRoot -RelativePath $Receipt.input_manifest.copy_sidecar
    $InputCopySidecarExpected = "$($Receipt.input_manifest.copy_sha256)  $(Split-Path -Leaf $InputCopyPath)"
    if ((Get-Content -LiteralPath $InputCopySidecarPath -Raw).Trim() -ne $InputCopySidecarExpected) { throw 'INPUT_MANIFEST_COPY_SIDECAR_MISMATCH' }

    if ($Receipt.written_evidence_files.Count -ne 36) { throw 'ORCHESTRATOR_EVIDENCE_FILE_COUNT_MISMATCH' }
    foreach ($Output in $Receipt.written_evidence_files) {
        $RelativeOutput = $Output.path
        $OutputPath = Assert-PathInsideRoot -Root $ProjectRoot -RelativePath $RelativeOutput
        if (-not (Test-Path -LiteralPath $OutputPath -PathType Leaf)) { throw "EVIDENCE_OUTPUT_MISSING:$RelativeOutput" }
        $OutputItem = Get-Item -LiteralPath $OutputPath
        if ($OutputItem.Length -ne $Output.bytes) { throw "EVIDENCE_OUTPUT_SIZE_MISMATCH:$RelativeOutput" }
        $OutputSha = Get-Sha256 $OutputPath
        if ($OutputSha -ne $Output.sha256) { throw "EVIDENCE_OUTPUT_SHA256_MISMATCH:$RelativeOutput" }
        $OutputSidecar = $OutputPath + '.sha256'
        if (-not (Test-Path -LiteralPath $OutputSidecar -PathType Leaf)) { throw "EVIDENCE_OUTPUT_SIDECAR_MISSING:$RelativeOutput" }
        $ExpectedLine = "$OutputSha  $(Split-Path -Leaf $OutputPath)"
        if ((Get-Content -LiteralPath $OutputSidecar -Raw).Trim() -ne $ExpectedLine) { throw "EVIDENCE_OUTPUT_SIDECAR_MISMATCH:$RelativeOutput" }
    }

    $PlanPath = Join-Path $RunRoot 'E6_CHALLENGE_PREPARE_ONLY_PLAN_V1.json'
    $PlanSidecarPath = $PlanPath + '.sha256'
    if (-not (Test-Path -LiteralPath $PlanPath -PathType Leaf) -or -not (Test-Path -LiteralPath $PlanSidecarPath -PathType Leaf)) { throw 'ORCHESTRATOR_PLAN_OR_SIDECAR_MISSING' }
    $PlanSha = Get-Sha256 $PlanPath
    $PlanSidecarExpected = "$PlanSha  $(Split-Path -Leaf $PlanPath)"
    if ((Get-Content -LiteralPath $PlanSidecarPath -Raw).Trim() -ne $PlanSidecarExpected) { throw 'ORCHESTRATOR_PLAN_SIDECAR_MISMATCH' }
    $Plan = Get-Content -LiteralPath $PlanPath -Raw | ConvertFrom-Json
    if ($Plan.receipt_sha256 -ne $ReceiptSha -or $Plan.run_id -ne $Receipt.run_id -or
        $Plan.challenge_groups.Count -ne 6 -or $Plan.e1_intents.Count -ne 18 -or $Plan.d_envelopes.Count -ne 18) {
        throw 'ORCHESTRATOR_PLAN_RECEIPT_LINKAGE_MISMATCH'
    }

    Write-Host 'E6_CHALLENGE_PREPARE_ONLY=PASS'
    Write-Host 'E6_CHALLENGE_GROUPS=6/6; E1_INTENTS=18/18; D_ENVELOPES=18/18'
    Write-Host 'E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; D4_8=BLOCKED; RENDERER=OFF; RELEASE_AUTHORITY=NONE'
    Write-Host "PREPARE_ONLY_RECEIPT=$ReceiptPath"
    Write-Host "PREPARE_ONLY_RECEIPT_SHA256=$ReceiptSha"
    Write-Host "PREPARE_ONLY_PLAN_SHA256=$PlanSha"
    $global:LASTEXITCODE = 0
    Write-Host 'E6_CHALLENGE_PREPARE_ONLY_RUNNER_FINAL=PASS'
}
catch {
    Write-Host "E6_CHALLENGE_PREPARE_ONLY_RUNNER=BLOCKED:$($_.Exception.Message)"
    $global:LASTEXITCODE = 1
    throw
}
