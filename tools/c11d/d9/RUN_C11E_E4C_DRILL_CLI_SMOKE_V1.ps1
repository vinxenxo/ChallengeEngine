[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe,
    [string]$BaseRequestPath,
    [string]$RequestId,
    [ValidateRange(5,240)][int]$TimeoutMinutes = 120
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-Sha256([string]$Path) {
    if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { throw "PIN_MISSING: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-SourcePins([string]$Root) {
    $pins = @(
        @('release/C11C_FREEZE_PACKAGE_MANIFEST.json','e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'),
        @('c11c-suite/c11c-producer/c11e_production_service.py','e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87'),
        @('tools/c11d/d9/c11e_e4c_drill_execution.py','51fe92c24506788918f896216055f2f1f21a7abf4ad9bf369c9ee63cbac5983a'),
        @('tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py','ba81e0b5e4a9f29b3ff5fd670bce424a592453dfa06ef5dce356e772044a99aa'),
        @('c11c-suite/c11c-producer/main.py','86eeca0c3fc37105c1202295db3f27e6dc249f4eafdcb48c5709cd2d76164393'),
        @('c11c-suite/c11c-producer/c11e_production_cli.py','3e530e535accc31455207d1e8e3253140c95b390348b4ee252ec8b5ee140869a'),
        @('c11c-suite/c11c-producer/run_visual_drill_production.ps1','ad6a7f0a6ce87804363810123f76ff0765b1582426cb2c8f69f6864ec3a0c808'),
        @('tools/prototypes/c11c_common/C11CSafeAmbient.py','c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c'),
        @('tools/prototypes/c11c_common/generate_c11c_family_music.py','41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d'),
        @('profiles/presentation/c11c_visual_music_profiles.json','b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58'),
        @('profiles/difficulty/visual_drill_tracking.json','6de8812bd46904e122ecdd0eae22fb2979bd75399c34779248c6569e833c921e'),
        @('profiles/difficulty/visual_drill_pursuit.json','ab6a29af53bdb45fb6976bfdd558e3275c477eb7ad9afd61b9d01e36d43afb05'),
        @('profiles/difficulty/visual_drill_saccade.json','6be50f582ef5ce11d36b72943750b88e72da67d858d67c3ac3d38d33c11ccf38'),
        @('profiles/difficulty/visual_drill_peripheral_scan.json','7c52112bf9c106152d7fe03b646bde0f415881a04efb75560d731fa3f18fa73e'),
        @('assets/fonts/Inter-Bold.otf','9fc6261e817d0b1b2bf1953d8799bb1c837d11aeebbf83ae352e7b4d6de6425d'),
        @('assets/fonts/NotoSansMono-Regular.ttf','6b692c4b6d15ccf59f1c1fe8d11cb8a92f51960f3e9f1f523781755a3af7e29f'),
        @('c11c-suite/c11c-producer/C11CVisualDrillProducerEnvelopeGenerator.gd','9e2a2f394db7efce6f646600d0bb8f4ee8488c87a184df1a0fb7f7cdcb9066e9'),
        @('core/presentation/rendering/VisualContentPlayer.gd','58d86d56ebd7507c9e800c83010103b9be12f1b5dca9356da61ca623e4cf0145'),
        @('core/presentation/rendering/VisualContentPlayer.tscn','8c3005a68aa0e818b078b06ae31054524d523b95e396dc1676dce28374ff8b27')
    )
    foreach ($pin in $pins) {
        $path = Join-Path $Root ($pin[0] -replace '/', '\')
        $actual = Get-Sha256 $path
        if ($actual -ne $pin[1]) { throw "SOURCE_PIN_FAIL: $($pin[0]) expected=$($pin[1]) actual=$actual" }
    }
    return $pins.Count
}
function Quote-Win32Argument([string]$Value) {
    if ($null -eq $Value) { $Value = '' }
    $builder = New-Object System.Text.StringBuilder
    [void]$builder.Append('"')
    $slashes = 0
    foreach ($ch in $Value.ToCharArray()) {
        if ($ch -eq [char]92) { $slashes++; continue }
        if ($ch -eq [char]34) {
            if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * (2 * $slashes + 1)) }
            else { [void]$builder.Append([char]92) }
            [void]$builder.Append([char]34)
            $slashes = 0
            continue
        }
        if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * $slashes); $slashes = 0 }
        [void]$builder.Append($ch)
    }
    if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * (2 * $slashes)) }
    [void]$builder.Append('"')
    return $builder.ToString()
}
function Write-Utf8NoBom([string]$Path,[string]$Content) {
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path,$Content,$encoding)
}

$root = [System.IO.Path]::GetFullPath($ProjectRoot)
$python = [System.IO.Path]::GetFullPath($PythonExe)
if (!(Test-Path -LiteralPath $root -PathType Container)) { throw "PROJECT_ROOT_MISSING: $root" }
if (!(Test-Path -LiteralPath $python -PathType Leaf)) { throw "PYTHON_EXE_MISSING: $python" }
if ([string]::IsNullOrWhiteSpace($BaseRequestPath)) {
    $BaseRequestPath = Join-Path $root 'artifacts\production\c11e\D99-GUI-6514F1066E79\request.json'
}
if (!(Test-Path -LiteralPath $BaseRequestPath -PathType Leaf)) { throw "BASE_REQUEST_MISSING: $BaseRequestPath" }
$baseRequestFull = [System.IO.Path]::GetFullPath($BaseRequestPath)
if ([string]::IsNullOrWhiteSpace($RequestId)) {
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ',[System.Globalization.CultureInfo]::InvariantCulture)
    $RequestId = 'E4C-CLI-SMOKE-' + $stamp + '-' + ([guid]::NewGuid().ToString('N').Substring(0,8))
}
if ($RequestId -notmatch '^[A-Za-z0-9][A-Za-z0-9._-]{7,63}$') { throw "REQUEST_ID_INVALID: $RequestId" }
$productionRoot = Join-Path $root ('artifacts\production\c11e\' + $RequestId)
$evidenceRoot = Join-Path $root ('artifacts\tests\c11e\e4c_cli_smoke\' + $RequestId)
if (Test-Path -LiteralPath $productionRoot) { throw "OUTPUT_COLLISION: $productionRoot" }
if (Test-Path -LiteralPath $evidenceRoot) { throw "EVIDENCE_COLLISION: $evidenceRoot" }
$cli = Join-Path $root 'c11c-suite\c11c-producer\c11e_production_cli.py'
if (!(Test-Path -LiteralPath $cli -PathType Leaf)) { throw 'CLI_FACADE_MISSING' }

$pinCount = Assert-SourcePins $root
Write-Host "SOURCE_PINS_PRE=PASS/$pinCount"
$baseRequestSha = Get-Sha256 $baseRequestFull
if ($baseRequestSha -ne '711749f3a7c4bb20340b5256da6100971e2be4f12a57c7b9c7267703ddb96a7e') { throw "BASE_GUI_REQUEST_SHA_FAIL: $baseRequestSha" }
$baseEvidenceRoot = Split-Path -Parent $baseRequestFull
$baseReceiptPath = Join-Path $baseEvidenceRoot 'E4C_DRILL_AV_QUALIFICATION_RECEIPT.json'
if (!(Test-Path -LiteralPath $baseReceiptPath -PathType Leaf)) { throw 'BASE_GUI_QUALIFICATION_RECEIPT_MISSING' }
$baseReceiptSha = Get-Sha256 $baseReceiptPath
if ($baseReceiptSha -ne 'd8aad7176ed99d8bc0c067cece58272c5ac44045d55d746c768ea72324d459db') { throw "BASE_GUI_RECEIPT_SHA_FAIL: $baseReceiptSha" }
$baseReceipt = Get-Content -LiteralPath $baseReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$request = Get-Content -LiteralPath $baseRequestFull -Raw -Encoding UTF8 | ConvertFrom-Json
if ($baseReceipt.status -ne 'PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION' -or $baseReceipt.request_id -ne $request.request_id -or $baseReceipt.request_origin -ne 'GUI') { throw 'BASE_GUI_ACCEPTED_RECEIPT_MISMATCH' }
if ($baseReceipt.c11c_frozen_manifest_unchanged -ne $true -or $baseReceipt.c11c_source_mutation -ne $false -or $baseReceipt.production_dispatch -ne $false -or $baseReceipt.release_authority -ne 'NONE') { throw 'BASE_GUI_GOVERNANCE_MISMATCH' }
if ($request.selection.content_type -ne 'visual_drills' -or $request.selection.family_id -ne 'tracking' -or $request.selection.variant_id -ne 'tier-1') { throw 'BASE_SELECTOR_MISMATCH_EXPECTED_tracking_tier-1' }
if ($request.mode -ne 'PRODUCTION' -or $request.delivery_profile_id -ne 'REVIEW_720' -or $request.audio_enabled -ne $true -or $request.personalization_enabled -ne $true) { throw 'BASE_REQUEST_MODE_PROFILE_AUDIO_PERSONALIZATION_MISMATCH' }
if ([int]$request.seed -ne 12345 -or [int]$request.music_seed -ne 840001) { throw 'BASE_REQUEST_SEED_MISMATCH' }
foreach ($field in @('title','subtitle','call_to_action')) {
    if ([string]::IsNullOrWhiteSpace([string]$request.production_override.$field)) { throw "BASE_EDITORIAL_EMPTY: $field" }
}
$request.request_id = $RequestId
$request.provenance.request_origin = 'CLI'
New-Item -ItemType Directory -Path $evidenceRoot -Force | Out-Null
$requestPath = Join-Path $evidenceRoot 'CLI_REQUEST.json'
$resultPath = Join-Path $evidenceRoot 'CLI_EXECUTION_RESULT.json'
$stdoutPath = Join-Path $evidenceRoot 'CLI_STDOUT.log'
$stderrPath = Join-Path $evidenceRoot 'CLI_STDERR.log'
$runnerReceiptPath = Join-Path $evidenceRoot 'CLI_SMOKE_RUNNER_RECEIPT.json'
Write-Utf8NoBom $requestPath ((ConvertTo-Json -InputObject $request -Depth 100) + "`n")

$arguments = @($cli,'--request',$requestPath,'--origin','CLI','--execute-drill-av','--output',$resultPath)
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $python
$psi.WorkingDirectory = $root
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.Arguments = (($arguments | ForEach-Object { Quote-Win32Argument ([string]$_) }) -join ' ')
$process = New-Object System.Diagnostics.Process
$process.StartInfo = $psi
$started = Get-Date
try {
    if (!$process.Start()) { throw 'CLI_PROCESS_START_FAILED' }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $timeoutMs = [int]($TimeoutMinutes * 60000)
    if (!$process.WaitForExit($timeoutMs)) {
        try { $process.Kill() } catch {}
        $process.WaitForExit()
        $stdout = $stdoutTask.GetAwaiter().GetResult()
        $stderr = $stderrTask.GetAwaiter().GetResult()
        Write-Utf8NoBom $stdoutPath $stdout
        Write-Utf8NoBom $stderrPath $stderr
        throw "CLI_TIMEOUT_AFTER_MINUTES=$TimeoutMinutes"
    }
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    Write-Utf8NoBom $stdoutPath $stdout
    Write-Utf8NoBom $stderrPath $stderr
    $exitCode = $process.ExitCode
}
finally { $process.Dispose() }
$finished = Get-Date
if ($exitCode -ne 0) { throw "CLI_EXIT_CODE=$exitCode; EVIDENCE=$evidenceRoot" }
if (!(Test-Path -LiteralPath $resultPath -PathType Leaf)) { throw "CLI_RESULT_MISSING; EVIDENCE=$evidenceRoot" }
$summary = Get-Content -LiteralPath $resultPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($summary.status -ne 'PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION') { throw "CLI_QUALIFICATION_STATUS=$($summary.status); EVIDENCE=$evidenceRoot" }
$receiptPath = [string]$summary.receipt
if (!(Test-Path -LiteralPath $receiptPath -PathType Leaf)) { throw "FULL_QUALIFICATION_RECEIPT_MISSING: $receiptPath" }
$receipt = Get-Content -LiteralPath $receiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($receipt.status -ne 'PASS_E4C_DRILL_SINGLE_SELECTOR_A_V_QUALIFICATION') { throw "FULL_RECEIPT_STATUS=$($receipt.status)" }
if ($receipt.request_id -ne $RequestId -or $receipt.request_origin -ne 'CLI') { throw 'CLI_REQUEST_ID_OR_ORIGIN_MISMATCH' }
if ($receipt.family_adapter_execution.shared_entrypoint -ne 'c11e_e4c_drill_execution.py' -or $receipt.family_adapter_execution.gui_and_cli_use_same_implementation -ne $true) { throw 'SHARED_EXECUTOR_INVARIANT_FAIL' }
if ($receipt.e1_gui_cli_parity.semantic_identity_equal -ne $true -or $receipt.e1_gui_cli_parity.status -ne 'PASS_E1_SHARED_GUI_CLI_INTENT_PARITY') { throw 'E1_GUI_CLI_PARITY_FAIL' }
if ($receipt.e1_validation.status -ne 'PASS_E1_PREPARATION_ONLY' -or $receipt.family_adapter_preparation_status -ne 'NOT_CONNECTED_E1') { throw 'E1_GOVERNANCE_BOUNDARY_FAIL' }
if ($receipt.source_pin_count -ne 91 -or $receipt.source_pins_pre_post_equal -ne $true) { throw 'E1_SOURCE_PIN_RECEIPT_FAIL' }
if ($receipt.bitstream_isolation.video_stream_identical -ne $true -or $receipt.bitstream_isolation.audio_stream_changed -ne $true) { throw 'AV_BITSTREAM_ISOLATION_FAIL' }
if ($receipt.family_music.same_seed_ab_identical -ne $true -or $receipt.family_music.changed_seed_c_distinct -ne $true) { throw 'FAMILY_MUSIC_SEED_ISOLATION_FAIL' }
if ($receipt.c11c_frozen_manifest_unchanged -ne $true -or $receipt.c11c_source_mutation -ne $false -or $receipt.production_dispatch -ne $false -or $receipt.release_authority -ne 'NONE') { throw 'GOVERNANCE_INVARIANT_FAIL' }
$postPinCount = Assert-SourcePins $root
if ($postPinCount -ne $pinCount) { throw 'SOURCE_PIN_COUNT_CHANGED' }
Write-Host "SOURCE_PINS_POST=PASS/$postPinCount"
$runnerReceipt = [ordered]@{
    schema = 'C11E-E4C-CLI-SMOKE-RUNNER-RECEIPT-V1'
    status = 'PASS_E4C_DRILL_CLI_SINGLE_SELECTOR_AV_SMOKE'
    request_id = $RequestId
    request_origin = 'CLI'
    selector = 'tracking/tier-1'
    gameplay_seed = 12345
    music_seed_a_b = 840001
    music_seed_c = 840002
    source_pins_pre = $pinCount
    source_pins_post = $postPinCount
    shared_executor = 'c11e_e4c_drill_execution.py'
    qualification_receipt = $receiptPath
    cli_summary = $resultPath
    stdout_log = $stdoutPath
    stderr_log = $stderrPath
    started_local = $started.ToString('o')
    finished_local = $finished.ToString('o')
    process_exit_code = $exitCode
    c11c_source_mutation = $false
    production_dispatch = $false
    release_authority = 'NONE'
}
Write-Utf8NoBom $runnerReceiptPath (($runnerReceipt | ConvertTo-Json -Depth 20) + "`n")
Write-Host 'CLI_ENTRYPOINT=PASS'
Write-Host 'SHARED_EXECUTOR=PASS'
Write-Host 'E1_GUI_CLI_PARITY=PASS'
Write-Host 'AV_BITSTREAM_ISOLATION=PASS'
Write-Host 'FAMILY_MUSIC_SEED_ISOLATION=PASS'
Write-Host 'CLI_SMOKE=PASS_E4C_DRILL_CLI_SINGLE_SELECTOR_AV_SMOKE'
Write-Host "REQUEST_ID=$RequestId"
Write-Host "EVIDENCE=$evidenceRoot"
Write-Host "QUALIFICATION_RECEIPT=$receiptPath"
Write-Host 'RELEASE_AUTHORITY=NONE'
