[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe,
    [string]$EvidenceRoot = "artifacts\production\c11e\E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8",
    [int]$TimeoutSeconds = 1800
)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($ProjectRoot)
if (!(Test-Path -LiteralPath $root -PathType Container)) { throw "PROJECT_ROOT_MISSING: $root" }
if (!(Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "PYTHON_EXE_MISSING: $PythonExe" }
$evidence = [IO.Path]::GetFullPath((Join-Path $root $EvidenceRoot))
if (!(Test-Path -LiteralPath $evidence -PathType Container) -or !$evidence.StartsWith($root.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)) { throw "EVIDENCE_ROOT_INVALID: $evidence" }
$script = Join-Path $root 'tools\c11d\d9\REQUALIFY_C11E_E4C_DRILL_AV_FROM_EXISTING_EVIDENCE_V2.py'
$consumer = Join-Path $root 'tools\c11d\d9\c11e_e4c_drill_visual_composition_consumer.py'
$amendment = Join-Path $root 'definitions\c11d\production\C11E_E4C_DRILL_EDITORIAL_FAMILY_TITLE_AMENDMENT_R1_20261114.json'
foreach ($p in @($script,$consumer,$amendment)) { if (!(Test-Path -LiteralPath $p -PathType Leaf)) { throw "R6_REQUIRED_INPUT_MISSING: $p" } }
$amendmentSha = (Get-FileHash -LiteralPath $amendment -Algorithm SHA256).Hash.ToLowerInvariant()
if ($amendmentSha -ne '1d0d5393368ca1e1ecb867059314e28463205fffc81e8af902909896e0ac7331') { throw 'R6_TITLE_AMENDMENT_SHA_MISMATCH' }
$utc = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$guid = [Guid]::NewGuid().ToString('N').Substring(0,8)
$outputId = "E4C-CLI-COMPOSITION-V2-R6-TITLE-BRIDGE-$utc-$guid"
$outputRoot = Join-Path $root "artifacts\production\c11e\$outputId"
if (Test-Path -LiteralPath $outputRoot) { throw "R6_OUTPUT_ALREADY_EXISTS: $outputRoot" }
$diagRoot = Join-Path $root "artifacts\tests\c11e\e4c_r6_requalification_diagnostics"
New-Item -ItemType Directory -Path $diagRoot -Force | Out-Null
$stdout = Join-Path $diagRoot "$outputId.stdout.log"
$stderr = Join-Path $diagRoot "$outputId.stderr.log"
$progressPath = Join-Path $outputRoot 'V2_REQUALIFICATION_PROGRESS.json'
$failurePath = Join-Path $outputRoot 'E4C_DRILL_V2_REQUALIFICATION_FAILURE.json'
function Quote-Arg([string]$Value) { '"' + $Value.Replace('"','\"') + '"' }
function Write-R6Diagnostic([string]$Reason, [int]$ExitCode) {
    $capture = Join-Path $diagRoot $outputId
    New-Item -ItemType Directory -Path $capture -Force | Out-Null
    foreach ($p in @($stdout,$stderr)) { if (Test-Path -LiteralPath $p) { Copy-Item -LiteralPath $p -Destination $capture -Force } }
    if (Test-Path -LiteralPath $outputRoot -PathType Container) { Copy-Item -LiteralPath $outputRoot -Destination (Join-Path $capture 'partial_output') -Recurse -Force }
    $source = Join-Path $capture 'source_evidence'
    New-Item -ItemType Directory -Path $source -Force | Out-Null
    foreach ($n in @('request.json','e1_intent.json','E4C_DRILL_AV_QUALIFICATION_RECEIPT.json','d_composition_plan.json')) {
        $p = Join-Path $evidence $n; if (Test-Path -LiteralPath $p -PathType Leaf) { Copy-Item -LiteralPath $p -Destination $source -Force }
    }
    $installed = Join-Path $capture 'installed_sources'
    New-Item -ItemType Directory -Path $installed -Force | Out-Null
    foreach ($p in @($script,$consumer,$amendment)) { if (Test-Path -LiteralPath $p -PathType Leaf) { Copy-Item -LiteralPath $p -Destination $installed -Force } }
    $rows = @()
    Get-ChildItem -LiteralPath $capture -Recurse -File | Sort-Object FullName | ForEach-Object {
        $rows += [pscustomobject]@{path=$_.FullName.Substring($capture.Length+1).Replace('\','/');bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
    }
    $manifest = [ordered]@{schema='C11E-E4C-R6-REQUALIFICATION-DIAGNOSTIC-MANIFEST-V1';request_id=$outputId;reason=$Reason;exit_code=$ExitCode;timeout_seconds=$TimeoutSeconds;frame_composition_repeated=$false;audio_generation_repeated=$false;production_dispatch=$false;release_authority='NONE';files=$rows}
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $capture 'R6_DIAGNOSTIC_MANIFEST.json') -Encoding UTF8
    $zip = Join-Path $diagRoot "$outputId.diagnostics.zip"
    if (Test-Path -LiteralPath $zip) { Remove-Item -LiteralPath $zip -Force }
    Compress-Archive -Path (Join-Path $capture '*') -DestinationPath $zip -CompressionLevel Optimal
    $hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Host "R6_DIAGNOSTIC_ZIP=$zip"
    Write-Host "R6_DIAGNOSTIC_SHA256=$hash"
}
try {
    $argsLine = @('-u', $script, '--project-root', $root, '--evidence-root', $evidence, '--output-id', $outputId) | ForEach-Object { Quote-Arg ([string]$_) }
    $argText = $argsLine -join ' '
    Write-Host "R6_OUTPUT_ID=$outputId"
    Write-Host "R6_TIMEOUT_SECONDS=$TimeoutSeconds"
    Write-Host "R6_TIMEOUT_MILLISECONDS=$([int64]$TimeoutSeconds * 1000)"
    $proc = Start-Process -FilePath $PythonExe -ArgumentList $argText -WorkingDirectory $root -NoNewWindow -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    $clock = [Diagnostics.Stopwatch]::StartNew()
    $lastStage = ''; $lastFrames = -1; $lastHeartbeat = [DateTime]::UtcNow
    while ($true) {
        $proc.Refresh()
        if ($proc.HasExited) { break }
        if (Test-Path -LiteralPath $progressPath -PathType Leaf) {
            try {
                $p = Get-Content -LiteralPath $progressPath -Raw | ConvertFrom-Json
                if ($p.stage -and $p.stage -ne $lastStage) { $lastStage=[string]$p.stage; Write-Host "R6_PROGRESS_STAGE=$lastStage" }
                if ($null -ne $p.frames_completed -and [int]$p.frames_completed -ne $lastFrames) { $lastFrames=[int]$p.frames_completed; Write-Host "R6_PROGRESS_FRAMES=$lastFrames/$($p.total_frames)" }
                $lastHeartbeat = [DateTime]::UtcNow
            } catch { }
        }
        if ($clock.Elapsed.TotalSeconds -ge $TimeoutSeconds) {
            & taskkill.exe /PID $proc.Id /T /F 2>&1 | Out-Null
            Start-Sleep -Milliseconds 500
            Write-R6Diagnostic 'R6_REQUALIFICATION_TIMEOUT' 124
            throw "R6_REQUALIFICATION_TIMEOUT; output=$outputRoot"
        }
        Start-Sleep -Seconds 2
    }
    $proc.WaitForExit()
    $exit = [int]$proc.ExitCode
    if ($exit -ne 0) {
        Write-R6Diagnostic 'R6_REQUALIFIER_NONZERO_EXIT' $exit
        $errTail = if (Test-Path $stderr) { (Get-Content -LiteralPath $stderr -Tail 40) -join "`n" } else { '' }
        throw "R6_REQUALIFIER_EXIT=$exit; $errTail"
    }
    if (!(Test-Path -LiteralPath $progressPath -PathType Leaf)) { throw 'R6_PROGRESS_RECEIPT_MISSING' }
    $progress = Get-Content -LiteralPath $progressPath -Raw | ConvertFrom-Json
    if ($progress.stage -ne 'OPERATOR_REVIEW_BUNDLE_CREATED') { throw "R6_FINAL_PROGRESS_STAGE_INVALID: $($progress.stage)" }
    $receiptPath = Join-Path $outputRoot 'E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json'
    $bundlePath = Join-Path $outputRoot 'E4C_V2_OPERATOR_REVIEW_BUNDLE.zip'
    if (!(Test-Path -LiteralPath $receiptPath -PathType Leaf) -or !(Test-Path -LiteralPath $bundlePath -PathType Leaf)) { throw 'R6_RECEIPT_OR_REVIEW_BUNDLE_MISSING' }
    $receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
    if ($receipt.status -ne 'PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE') { throw "R6_TECHNICAL_STATUS_INVALID: $($receipt.status)" }
    if ($receipt.operator_review_frames.Count -ne 7) { throw "R6_REVIEW_FRAME_COUNT_INVALID: $($receipt.operator_review_frames.Count)" }
    $bundleHash = (Get-FileHash -LiteralPath $bundlePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($receipt.operator_review_bundle_sha256 -ne $bundleHash) { throw 'R6_REVIEW_BUNDLE_SHA_MISMATCH' }
    Write-Host 'R6_RECOVERY=PASS'
    Write-Host "TECHNICAL_STATUS=$($receipt.status)"
    Write-Host "R6_OUTPUT_ROOT=$outputRoot"
    Write-Host "TECHNICAL_RECEIPT=$receiptPath"
    Write-Host "REVIEW_BUNDLE=$bundlePath"
    Write-Host "REVIEW_BUNDLE_SHA256=$bundleHash"
    Write-Host 'REVIEW_FRAMES=7/7 PASS'
    Write-Host 'FRAME_COMPOSITION_REPEATED=TRUE_FOR_NEW_FAMILY_TITLE_AMENDMENT'
    Write-Host 'ORIGINAL_NATIVE_CAPTURE_REPEATED=FALSE'
    Write-Host 'FAMILY_MUSIC_GENERATION_REPEATED=FALSE'
    Write-Host 'PRODUCTION_DISPATCH=FALSE'
    Write-Host 'RELEASE_AUTHORITY=NONE'
    exit 0
} catch {
    if (!(Test-Path -LiteralPath (Join-Path $diagRoot "$outputId.diagnostics.zip"))) {
        Write-R6Diagnostic $_.Exception.Message 1
    }
    Write-Error $_
    exit 1
}
