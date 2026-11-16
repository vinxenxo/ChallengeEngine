[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe,
    [switch]$Execute,
    [string]$BatchId,
    [string]$ResultReceiptPath,
    [ValidateRange(1200,14400)][int]$TimeoutSeconds = 7200
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Get-Sha256([string]$Path) {
    if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { throw "PIN_MISSING: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
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

$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$tokens,[ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw "RUNNER_AST_PARSE_FAIL: $($parseErrors[0].Message)" }
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) {
    throw "WINDOWS_POWERSHELL_5_1_REQUIRED: $($PSVersionTable.PSVersion)"
}

$root = [System.IO.Path]::GetFullPath($ProjectRoot)
$python = [System.IO.Path]::GetFullPath($PythonExe)
if (!(Test-Path -LiteralPath $root -PathType Container)) { throw "PROJECT_ROOT_MISSING: $root" }
if (!(Test-Path -LiteralPath $python -PathType Leaf)) { throw "PYTHON_EXE_MISSING: $python" }
$styleChecks = @(
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V29.md'; Sha='76d9187f7d8c9b44ed940f18fd242f2205e6caf357c8b7dc19756fa1cf8a0c0a'; Label='V29' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V30.md'; Sha='57d653890535849c7a1d55733c29b1f7fe574010a8cdb18b8d2fd86565b50c83'; Label='V30' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V31.md'; Sha='e856e3d2385aab67b6fcfb4f6cc05e013b2792e02ae3058e97172a9fd72edbac'; Label='V31' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V33.md'; Sha='e37993b32a72144a6894c6e228b756ee4cf1b2892627929bbafbb01766662167'; Label='V33' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V34.md'; Sha='1cb7880a73b3d429ba15d411228980c16c9168101155a283db21b6f966545d8c'; Label='V34' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V35.md'; Sha='6680fabaabc8428cc33d0c0d38af6df443b6f0e2be8470362c1a144c5047ff8a'; Label='V35' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V36.md'; Sha='4f3940d50b07ccd48e30f44dbc8653a9021791d20382dbccdb7ca0d93f98f337'; Label='V36' }
)
foreach ($style in $styleChecks) {
    $path = Join-Path $root $style.Relative
    $sha = Get-Sha256 $path
    if ($sha -ne $style.Sha) { throw "STYLE_GUIDE_$($style.Label)_SHA_MISMATCH: $sha" }
}
$driver = Join-Path $root 'tools\c11d\d9\c11e_e4c_peripheral_scan_tier_batch.py'
$driverSha = Get-Sha256 $driver
if ($driverSha -ne '4ab6e3e6a0ab9c78054a46f11a0b937512eb7eba3eeba5c1a2776e139e8dd547') { throw "PERIPHERAL_SCAN_BATCH_DRIVER_SHA_MISMATCH: $driverSha" }

$tempRoot = Join-Path $env:TEMP ('C11E_E4C_PERIPHERAL_SCAN_BATCH_RUNNER_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot | Out-Null
$stdoutPath = Join-Path $tempRoot 'batch.stdout.log'
$stderrPath = Join-Path $tempRoot 'batch.stderr.log'
$argsList = @($driver,'--project-root',$root,'--python-exe',$python,'--timeout-seconds',[string]$TimeoutSeconds,'--require-v36-guide')
if (![string]::IsNullOrWhiteSpace($BatchId)) { $argsList += @('--batch-id',$BatchId) }
if ($Execute) { $argsList += '--execute' }
$argumentLine = ($argsList | ForEach-Object { Quote-Win32Argument ([string]$_) }) -join ' '
$resultReceiptFullPath = $null
if ($Execute) {
    if ([string]::IsNullOrWhiteSpace($ResultReceiptPath)) { throw 'PERIPHERAL_SCAN_EXECUTION_RECEIPT_PATH_REQUIRED_BEFORE_CHILD' }
    $resultReceiptFullPath = [System.IO.Path]::GetFullPath($ResultReceiptPath)
    $resultReceiptParent = Split-Path -Parent $resultReceiptFullPath
    if (-not (Test-Path -LiteralPath $resultReceiptParent -PathType Container)) { throw "RESULT_RECEIPT_PARENT_MISSING_BEFORE_CHILD: $resultReceiptParent" }
    if (Test-Path -LiteralPath $resultReceiptFullPath) { throw "PERIPHERAL_SCAN_RESULT_RECEIPT_COLLISION_BEFORE_CHILD: $resultReceiptFullPath" }
    Write-Host 'EXECUTION_RECEIPT_PREFLIGHT=PASS'
}
$process = Start-Process -FilePath $python -ArgumentList $argumentLine -WorkingDirectory $root -Wait -PassThru -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
$exitCode = [int]$process.ExitCode
$stdout = if (Test-Path -LiteralPath $stdoutPath -PathType Leaf) { Get-Content -LiteralPath $stdoutPath -Raw -Encoding UTF8 } else { '' }
$stderr = if (Test-Path -LiteralPath $stderrPath -PathType Leaf) { Get-Content -LiteralPath $stderrPath -Raw -Encoding UTF8 } else { '' }
if (![string]::IsNullOrWhiteSpace($stdout)) { Write-Host $stdout.TrimEnd() }
if (![string]::IsNullOrWhiteSpace($stderr)) { Write-Host $stderr.TrimEnd() }
Write-Host "PYTHON_BATCH_EXIT_CODE=$exitCode"
Write-Host "WRAPPER_LOG_ROOT=$tempRoot"
foreach ($style in $styleChecks) { Write-Host ("STYLE_GUIDE_{0}_SHA256={1}" -f $style.Label,$style.Sha) }
if ($exitCode -ne 0) { throw "E4C_PERIPHERAL_SCAN_TIER_BATCH_FAILED: exit=$exitCode; logs=$tempRoot" }
if ($Execute) {
    $result = $null
    try { $result = $stdout | ConvertFrom-Json -ErrorAction Stop }
    catch { throw "PERIPHERAL_SCAN_BATCH_RESULT_JSON_INVALID: logs=$tempRoot" }
    $expectedSelectors = @('peripheral_scan/tier-1','peripheral_scan/tier-2','peripheral_scan/tier-3','peripheral_scan/tier-4','peripheral_scan/tier-5')
    if ($result.status -ne 'PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW' -or
        @($result.selectors_expected).Count -ne 5 -or @($result.selectors_technical_pass).Count -ne 5 -or
        $result.source_pin_count -ne 38 -or $result.source_pins_pre_post_equal -ne $true -or
        $result.family_music_profile -ne 'ORBITAL_RITUAL' -or
        $result.timeline_contract.fps -ne 30 -or $result.timeline_contract.gameplay_frames -ne 510 -or
        $result.timeline_contract.pre_roll_frames -ne 90 -or $result.timeline_contract.end_cta_frames -ne 90 -or
        $result.timeline_contract.total_frames -ne 690 -or [math]::Abs([double]$result.timeline_contract.duration_seconds - 23.0) -gt 0.001 -or
        $result.governance.production_dispatch -ne $false -or $result.governance.release_authority -ne 'NONE') {
        throw 'PERIPHERAL_SCAN_BATCH_RESULT_CONTRACT_FAIL'
    }
    if ([string]$result.batch_id -notmatch '^E4C-PERIPHERAL-SCAN-T1-5-[A-Za-z0-9._-]{8,64}$') { throw 'PERIPHERAL_SCAN_BATCH_ID_INVALID' }
    for ($i=0; $i -lt 5; $i++) {
        if ([string]$result.selectors_expected[$i] -cne $expectedSelectors[$i] -or [string]$result.selectors_technical_pass[$i] -cne $expectedSelectors[$i]) { throw 'PERIPHERAL_SCAN_SELECTOR_COVERAGE_FAIL' }
    }
    $batchEvidenceBase = Join-Path $root 'artifacts\tests\c11e\e4c_peripheral_scan_tier_batch'
    $expectedEvidenceRoot = [IO.Path]::GetFullPath((Join-Path $batchEvidenceBase ([string]$result.batch_id)))
    if ([IO.Path]::GetFullPath([string]$result.evidence_root) -cne $expectedEvidenceRoot) { throw 'PERIPHERAL_SCAN_EVIDENCE_ROOT_MISMATCH' }
    $batchResultPath = Join-Path $expectedEvidenceRoot 'BATCH_RESULT.json'
    if (-not (Test-Path -LiteralPath $batchResultPath -PathType Leaf)) { throw "PERIPHERAL_SCAN_BATCH_RESULT_FILE_MISSING: $batchResultPath" }
    $batchResultObject = Get-Content -LiteralPath $batchResultPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($batchResultObject.batch_id -ne $result.batch_id -or $batchResultObject.status -ne 'PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW') { throw 'PERIPHERAL_SCAN_BATCH_RESULT_IDENTITY_MISMATCH' }
    $launchReceipt = [ordered]@{
        schema='C11E-PERIPHERAL-SCAN-BATCH-LAUNCH-RECEIPT-V1'
        status='PASS_TECHNICAL_PENDING_OPERATOR_A_V_REVIEW'
        batch_id=[string]$result.batch_id
        coverage=[string]$result.coverage
        selectors_expected=@($result.selectors_expected)
        selectors_technical_pass=@($result.selectors_technical_pass)
        source_pin_count=[int]$result.source_pin_count
        family_music_profile=[string]$result.family_music_profile
        source_pins_pre_post_equal=[bool]$result.source_pins_pre_post_equal
        timeline_contract=$result.timeline_contract
        evidence_root=[string]$result.evidence_root
        batch_result_path=$batchResultPath
        batch_result_sha256=(Get-Sha256 $batchResultPath)
        production_dispatch=$false
        release_authority='NONE'
        operator_review='PENDING'
        runner_log_root=$tempRoot
        completed_utc=[DateTime]::UtcNow.ToString('o')
    }
    $json = ConvertTo-Json -InputObject $launchReceipt -Depth 30
    $fs = [IO.File]::Open($resultReceiptFullPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {
        $bytes = (New-Object System.Text.UTF8Encoding($false)).GetBytes($json + "`n")
        $fs.Write($bytes,0,$bytes.Length)
        $fs.Flush($true)
    }
    finally { $fs.Dispose() }
    Write-Host "BATCH_LAUNCH_RECEIPT=$resultReceiptFullPath"
}
Write-Host 'PERIPHERAL_SCAN_BATCH_RUNNER=PASS'
Write-Host 'PERIPHERAL_SCAN_T1_TO_T5=EXECUTION_SCOPE'
if ($Execute) { Write-Host 'PERIPHERAL_SCAN_BATCH_EXECUTION=TIERS_1_TO_5_COMPLETED_OPERATOR_REVIEW_PENDING' }
else { Write-Host 'PERIPHERAL_SCAN_BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY' }
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
