[CmdletBinding()]
param(
    [string]$GodotExe = ''
)

$ErrorActionPreference = 'Stop'

if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) {
    throw "Windows PowerShell 5.1 is required. Current version: $($PSVersionTable.PSVersion)"
}

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$PythonScript = Join-Path $PSScriptRoot 'prepare_c11e_e4b_r1p_loop_parameter_payloads_v1.py'
$GodotScript = Join-Path $PSScriptRoot 'materialize_c11e_e4b_r1p_loop_parameter_payloads_v1.gd'
$StaticAudit = Join-Path $PSScriptRoot 'test_c11e_e4b_r1p_family_grammar_static_audit.py'

foreach ($required in @($PythonScript, $GodotScript, $StaticAudit)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required R1P tool is missing: $required"
    }
}

$PythonCommand = Get-Command py.exe -ErrorAction SilentlyContinue | Select-Object -First 1
if ($null -eq $PythonCommand) { throw 'Python launcher py.exe was not found. Python 3.13 is required.' }

if ([string]::IsNullOrWhiteSpace($GodotExe)) {
    if (-not [string]::IsNullOrWhiteSpace($env:GODOT_EXE) -and (Test-Path -LiteralPath $env:GODOT_EXE -PathType Leaf)) {
        $GodotExe = $env:GODOT_EXE
    } else {
        $GodotCommand = Get-Command godot_console.exe, godot.exe, godot -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -ne $GodotCommand) { $GodotExe = $GodotCommand.Source }
    }
}
if ([string]::IsNullOrWhiteSpace($GodotExe) -or -not (Test-Path -LiteralPath $GodotExe -PathType Leaf)) {
    throw 'Godot 4.7.1 executable not found. Re-run with -GodotExe "C:\path\to\Godot_v4.7.1-stable_win64_console.exe".'
}
$GodotExe = (Resolve-Path -LiteralPath $GodotExe).Path

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Invoke-CapturedProcess {
    param(
        [Parameter(Mandatory=$true)][string]$FilePath,
        [Parameter(Mandatory=$true)][string]$ArgumentLine,
        [Parameter(Mandatory=$true)][string]$WorkingDirectory,
        [Parameter(Mandatory=$true)][string]$StdOutPath,
        [Parameter(Mandatory=$true)][string]$StdErrPath
    )
    $parent = Split-Path -Parent $StdOutPath
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $process = Start-Process -FilePath $FilePath -ArgumentList $ArgumentLine -WorkingDirectory $WorkingDirectory -Wait -PassThru -NoNewWindow -RedirectStandardOutput $StdOutPath -RedirectStandardError $StdErrPath
    if (-not (Test-Path -LiteralPath $StdOutPath)) { [System.IO.File]::WriteAllText($StdOutPath, '', (New-Object System.Text.UTF8Encoding($false))) }
    if (-not (Test-Path -LiteralPath $StdErrPath)) { [System.IO.File]::WriteAllText($StdErrPath, '', (New-Object System.Text.UTF8Encoding($false))) }
    return [pscustomobject]@{
        exit_code = [int]$process.ExitCode
        stdout_path = $StdOutPath
        stderr_path = $StdErrPath
        stdout_sha256 = Get-Sha256 $StdOutPath
        stderr_sha256 = Get-Sha256 $StdErrPath
    }
}

$Stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$RunSuffix = [Guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant()
$RunId = "E4B_R1P_${Stamp}_${RunSuffix}"
$ArtifactBase = Join-Path $ProjectRoot 'artifacts\tests\c11e\e4b_r1p'
if (-not (Test-Path -LiteralPath $ArtifactBase -PathType Container)) {
    New-Item -ItemType Directory -Path $ArtifactBase -Force | Out-Null
}
$OutputRoot = Join-Path $ArtifactBase $RunId
if (Test-Path -LiteralPath $OutputRoot) { throw "Output collision; refusing overwrite: $OutputRoot" }
$WorkRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("C11E_R1P_" + $RunSuffix)
if (Test-Path -LiteralPath $WorkRoot) { throw "Temporary work collision; refusing overwrite: $WorkRoot" }
New-Item -ItemType Directory -Path $WorkRoot | Out-Null
$ProbeRoot = Join-Path $WorkRoot 'godot_probe_project'
New-Item -ItemType Directory -Path $ProbeRoot | Out-Null

$PythonVersionOut = Join-Path $WorkRoot 'python_version.stdout.log'
$PythonVersionErr = Join-Path $WorkRoot 'python_version.stderr.log'
$PythonPrepareOut = Join-Path $WorkRoot 'python_prepare.stdout.log'
$PythonPrepareErr = Join-Path $WorkRoot 'python_prepare.stderr.log'
$GodotVersionOut = Join-Path $WorkRoot 'godot_version.stdout.log'
$GodotVersionErr = Join-Path $WorkRoot 'godot_version.stderr.log'
$GodotOut = Join-Path $WorkRoot 'godot.stdout.log'
$GodotErr = Join-Path $WorkRoot 'godot.stderr.log'
$PythonFinalizeOut = Join-Path $WorkRoot 'python_finalize.stdout.log'
$PythonFinalizeErr = Join-Path $WorkRoot 'python_finalize.stderr.log'

$PythonVersionEvidence = $null
$PythonVersionText = ''
$PythonPrepareEvidence = $null
$GodotVersionEvidence = $null
$GodotEvidence = $null
$PythonFinalizeEvidence = $null
$GodotVersionText = ''
$OriginalDurationPresent = Test-Path Env:C11C_DURATION_SECONDS
$OriginalDurationValue = $env:C11C_DURATION_SECONDS
$OriginalInputPresent = Test-Path Env:C11E_R1P_INPUT_PATH
$OriginalInputValue = $env:C11E_R1P_INPUT_PATH
$Success = $false
$CopyEvidence = @()

Write-Host '========== C11-E E4B R1P LOOP PARAMETER PAYLOADS V1 =========='
Write-Host "PROJECT_ROOT=$ProjectRoot"
Write-Host "RUN_ID=$RunId"
Write-Host 'SCOPE=27 request-bound family parameter payloads; no render/frame/media'

try {
    $PythonVersionEvidence = Invoke-CapturedProcess -FilePath $PythonCommand.Source -ArgumentLine '-3.13 --version' -WorkingDirectory $ProjectRoot -StdOutPath $PythonVersionOut -StdErrPath $PythonVersionErr
    if ($PythonVersionEvidence.exit_code -ne 0) { throw "Python 3.13 version probe failed: exit=$($PythonVersionEvidence.exit_code)" }
    $PythonVersionText = ((Get-Content -LiteralPath $PythonVersionOut -Raw) + (Get-Content -LiteralPath $PythonVersionErr -Raw)).Trim()
    if ($PythonVersionText -notmatch '(?m)^Python 3\.13(?:\.|$)') { throw "Python 3.13 required; detected '$PythonVersionText'." }

    $pythonArgs = '-3.13 -B "' + $PythonScript + '" prepare --project-root "' + $ProjectRoot + '" --work-dir "' + $WorkRoot + '\prepare" --run-id "' + $RunId + '"'
    $PythonPrepareEvidence = Invoke-CapturedProcess -FilePath $PythonCommand.Source -ArgumentLine $pythonArgs -WorkingDirectory $ProjectRoot -StdOutPath $PythonPrepareOut -StdErrPath $PythonPrepareErr
    if ($PythonPrepareEvidence.exit_code -ne 0) {
        throw "Python D9.9/D9.10 preparation failed: exit=$($PythonPrepareEvidence.exit_code); stderr=$PythonPrepareErr"
    }
    $prepareReportPath = Join-Path $WorkRoot 'prepare\r1p_prepare_report.json'
    if (-not (Test-Path -LiteralPath $prepareReportPath -PathType Leaf)) { throw 'Python preparation did not create r1p_prepare_report.json.' }
    $prepareReport = Get-Content -LiteralPath $prepareReportPath -Raw | ConvertFrom-Json
    if ($prepareReport.status -ne 'PASS_D9_9_D9_10_PARENT_PREPARATION_27_OF_27' -or [int]$prepareReport.case_count -ne 27) {
        throw 'Python D9.9/D9.10 parent preparation did not pass 27/27.'
    }

    $scriptCopies = @(
        @{ source = (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CVariationProfile.gd'); dest = (Join-Path $ProbeRoot 'C11CVariationProfile.gd') },
        @{ source = (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CPaletteBank.gd'); dest = (Join-Path $ProbeRoot 'C11CPaletteBank.gd') },
        @{ source = (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CEditorialColors.gd'); dest = (Join-Path $ProbeRoot 'C11CEditorialColors.gd') },
        @{ source = (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\C11CVisualLoopDuration.gd'); dest = (Join-Path $ProbeRoot 'C11CVisualLoopDuration.gd') },
        @{ source = (Join-Path $ProjectRoot 'tools\prototypes\c11c_common\TechnobabbleGenerator.gd'); dest = (Join-Path $ProbeRoot 'TechnobabbleGenerator.gd') },
        @{ source = $GodotScript; dest = (Join-Path $ProbeRoot 'materialize_c11e_e4b_r1p_loop_parameter_payloads_v1.gd') }
    )
    foreach ($item in $scriptCopies) {
        Copy-Item -LiteralPath $item.source -Destination $item.dest
        $sourceHash = Get-Sha256 $item.source
        $copyHash = Get-Sha256 $item.dest
        if ($sourceHash -ne $copyHash) { throw "Temporary Godot source copy hash mismatch: $($item.source)" }
        $CopyEvidence += [pscustomobject]@{
            source_path = $item.source
            source_sha256 = $sourceHash
            temporary_copy_path = $item.dest
            temporary_copy_sha256 = $copyHash
        }
    }
    $projectConfig = "config_version=5`r`n`r`n[application]`r`nconfig/name=`"C11E_E4B_R1P_Isolated_Parameter_Probe`"`r`n"
    [System.IO.File]::WriteAllText((Join-Path $ProbeRoot 'project.godot'), $projectConfig, (New-Object System.Text.UTF8Encoding($false)))

    $GodotVersionEvidence = Invoke-CapturedProcess -FilePath $GodotExe -ArgumentLine '--version' -WorkingDirectory $ProbeRoot -StdOutPath $GodotVersionOut -StdErrPath $GodotVersionErr
    if ($GodotVersionEvidence.exit_code -ne 0) { throw "Godot --version failed: exit=$($GodotVersionEvidence.exit_code)" }
    $GodotVersionText = (Get-Content -LiteralPath $GodotVersionOut -Raw).Trim()
    if ($GodotVersionText -notmatch '^4\.7\.1(?:\.|$)') { throw "Godot 4.7.1 required; detected '$GodotVersionText'." }

    $env:C11E_R1P_INPUT_PATH = Join-Path $WorkRoot 'prepare\r1p_godot_input.json'
    Remove-Item Env:C11C_DURATION_SECONDS -ErrorAction SilentlyContinue
    $godotArgs = '--headless --path "' + $ProbeRoot + '" --script "res://materialize_c11e_e4b_r1p_loop_parameter_payloads_v1.gd"'
    $GodotEvidence = Invoke-CapturedProcess -FilePath $GodotExe -ArgumentLine $godotArgs -WorkingDirectory $ProbeRoot -StdOutPath $GodotOut -StdErrPath $GodotErr
    if ($GodotEvidence.exit_code -ne 0) { throw "Godot R1P materializer failed: exit=$($GodotEvidence.exit_code); stderr=$GodotErr" }

    $outputArgument = '"' + $OutputRoot + '"'
    $pythonFinalizeArgs = '-3.13 -B "' + $PythonScript + '" finalize --project-root "' + $ProjectRoot + '" --work-dir "' + (Join-Path $WorkRoot 'prepare') + '" --output-dir ' + $outputArgument + ' --godot-stdout "' + $GodotOut + '" --godot-stderr "' + $GodotErr + '" --python-prepare-stdout "' + $PythonPrepareOut + '" --python-prepare-stderr "' + $PythonPrepareErr + '" --python-prepare-exit-code ' + [string]$PythonPrepareEvidence.exit_code + ' --godot-exit-code ' + [string]$GodotEvidence.exit_code + ' --godot-version "' + $GodotVersionText + '"'
    $PythonFinalizeEvidence = Invoke-CapturedProcess -FilePath $PythonCommand.Source -ArgumentLine $pythonFinalizeArgs -WorkingDirectory $ProjectRoot -StdOutPath $PythonFinalizeOut -StdErrPath $PythonFinalizeErr
    if ($PythonFinalizeEvidence.exit_code -ne 0) {
        throw "Python receipt finalization failed: exit=$($PythonFinalizeEvidence.exit_code); stderr=$PythonFinalizeErr"
    }

    Copy-Item -LiteralPath $PythonVersionOut -Destination (Join-Path $OutputRoot 'python_version.stdout.log')
    Copy-Item -LiteralPath $PythonVersionErr -Destination (Join-Path $OutputRoot 'python_version.stderr.log')
    Copy-Item -LiteralPath $GodotVersionOut -Destination (Join-Path $OutputRoot 'godot_version.stdout.log')
    Copy-Item -LiteralPath $GodotVersionErr -Destination (Join-Path $OutputRoot 'godot_version.stderr.log')
    Copy-Item -LiteralPath $PythonFinalizeOut -Destination (Join-Path $OutputRoot 'python_finalize.stdout.log')
    Copy-Item -LiteralPath $PythonFinalizeErr -Destination (Join-Path $OutputRoot 'python_finalize.stderr.log')

    $processReceipt = [ordered]@{
        schema = 'C11E-E4B-R1P-RUNNER-PROCESS-RECEIPT-V1'
        run_id = $RunId
        powershell_version = [string]$PSVersionTable.PSVersion
        python_launcher = $PythonCommand.Source
        python_launcher_sha256 = Get-Sha256 $PythonCommand.Source
        python_version = $PythonVersionText
        python_version_process = $PythonVersionEvidence
        python_prepare = $PythonPrepareEvidence
        godot_executable = $GodotExe
        godot_executable_sha256 = Get-Sha256 $GodotExe
        godot_version = $GodotVersionText
        godot_version_process = $GodotVersionEvidence
        godot_materializer = $GodotEvidence
        godot_temporary_source_copies = $CopyEvidence
        python_finalize = $PythonFinalizeEvidence
        process_success = $true
        checkout_source_files_written = $false
        repository_evidence_artifacts_written = $true
        renderer_or_media_invoked = $false
    }
    $processJson = $processReceipt | ConvertTo-Json -Depth 12
    $processPath = Join-Path $OutputRoot 'runner_process_receipt.json'
    [System.IO.File]::WriteAllText($processPath, $processJson, (New-Object System.Text.UTF8Encoding($false)))
    $processHash = Get-Sha256 $processPath
    [System.IO.File]::WriteAllText((Join-Path $OutputRoot 'runner_process_receipt.sha256'), ($processHash + '  runner_process_receipt.json' + "`n"), [System.Text.Encoding]::ASCII)

    $receiptFolder = Join-Path $OutputRoot 'receipts'
    $receiptJsonFiles = @(Get-ChildItem -LiteralPath $receiptFolder -Filter '*.json' -File)
    $receiptSidecarFiles = @(Get-ChildItem -LiteralPath $receiptFolder -Filter '*.json.sha256' -File)
    if ($receiptJsonFiles.Count -ne 27 -or $receiptSidecarFiles.Count -ne 27) {
        throw "Finalized receipt count is invalid: JSON=$($receiptJsonFiles.Count); SHA256=$($receiptSidecarFiles.Count)"
    }
    $zipPath = $OutputRoot + '.zip'
    if (Test-Path -LiteralPath $zipPath) { throw "Archive collision; refusing overwrite: $zipPath" }
    Compress-Archive -Path (Join-Path $OutputRoot '*') -DestinationPath $zipPath -CompressionLevel Optimal
    $zipHash = Get-Sha256 $zipPath
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
    try {
        $archiveEntries = @($archive.Entries)
        if ($archiveEntries.Count -lt 50) { throw "R1P ZIP is unexpectedly incomplete: $($archiveEntries.Count) entries" }
        $receiptEntryCount = @($archiveEntries | Where-Object { $_.FullName -match '^receipts/[^/]+\.json$' }).Count
        if ($receiptEntryCount -ne 27) { throw "R1P ZIP contains $receiptEntryCount selector receipts; expected 27" }
    } finally {
        $archive.Dispose()
    }
    $report = Get-Content -LiteralPath (Join-Path $OutputRoot 'r1p_report.json') -Raw | ConvertFrom-Json
    if ($report.status -ne 'PASS_R1P_PARAMETER_PAYLOADS_27_OF_27' -or [int]$report.receipt_count -ne 27) {
        throw 'Final R1P report is not PASS 27/27.'
    }
    $Success = $true
    Write-Host "R1P_STATUS=$($report.status)"
    Write-Host "RECEIPTS=$($report.receipt_count)/27"
    Write-Host "PYTHON_VERSION=$PythonVersionText"
    Write-Host "GODOT_VERSION=$GodotVersionText"
    Write-Host "REPORT_SHA256=$($report.report_sha256)"
    Write-Host "PROCESS_RECEIPT_SHA256=$processHash"
    Write-Host "OUTPUT_ROOT=$OutputRoot"
    Write-Host "PACKAGE_ZIP=$zipPath"
    Write-Host "PACKAGE_SHA256=$zipHash"
} finally {
    if ($OriginalDurationPresent) { $env:C11C_DURATION_SECONDS = $OriginalDurationValue } else { Remove-Item Env:C11C_DURATION_SECONDS -ErrorAction SilentlyContinue }
    if ($OriginalInputPresent) { $env:C11E_R1P_INPUT_PATH = $OriginalInputValue } else { Remove-Item Env:C11E_R1P_INPUT_PATH -ErrorAction SilentlyContinue }
    if ($Success -and (Test-Path -LiteralPath $WorkRoot)) {
        Remove-Item -LiteralPath $WorkRoot -Recurse -Force
    } elseif (Test-Path -LiteralPath $WorkRoot) {
        Write-Host "DIAGNOSTIC_WORK_ROOT_RETAINED=$WorkRoot"
    }
}
