param(
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Projects\ChallengeEngineV01_STATELESS')
)
$ErrorActionPreference = 'Stop'
$script:RunnerPath = $PSCommandPath

function Get-Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Missing file: $Path" }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Assert-AsciiSource([string]$Path) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    foreach ($byte in $bytes) { if ($byte -gt 127) { throw "Runner source is not ASCII-safe: $Path" } }
}

function Invoke-Python([string]$Python, [string[]]$Arguments, [string]$WorkingDirectory, [string]$Stdout, [string]$Stderr) {
    $quotedArguments = @()
    foreach ($argument in $Arguments) {
        $value = [string]$argument
        if ($value.Contains(' ') -or $value.Contains([char]9)) { $quotedArguments += ('"' + $value + '"') } else { $quotedArguments += $value }
    }
    $argumentLine = $quotedArguments -join ' '
    $process = Start-Process -FilePath $Python -ArgumentList $argumentLine -WorkingDirectory $WorkingDirectory -Wait -PassThru -NoNewWindow -RedirectStandardOutput $Stdout -RedirectStandardError $Stderr
    if ($null -eq $process) { throw 'Start-Process did not return a process result' }
    return $process.ExitCode
}

Write-Host '========== C11-E E4B LOOP FAMILY CONTRACT V1 =========='
Write-Host ('POWERSHELL_RUNTIME_VERSION=' + $PSVersionTable.PSVersion.ToString())
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'PowerShell 5.1 is required' }
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($script:RunnerPath, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw ('PowerShell AST parse failed: ' + ($parseErrors | Out-String)) }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
Assert-AsciiSource $script:RunnerPath
Write-Host 'RUNNER_SOURCE_ENCODING=ASCII_SAFE'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; READ_ONLY_AUDIT=TRUE'

$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
$toolRoot = Join-Path $ProjectRoot 'tools\c11d\d9'
$testPath = Join-Path $toolRoot 'test_c11e_e4b_loop_family_contract.py'
$auditPath = Join-Path $toolRoot 'c11e_e4b_loop_family_contract_audit.py'
$builderPath = Join-Path $toolRoot 'c11e_e4b_loop_family_stage_contract.py'
$pinsPath = Join-Path $toolRoot 'C11E_E4B_LOOP_FAMILY_CONTRACT_SOURCE_PINS_V1.json'
$frozenPath = Join-Path $ProjectRoot 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
foreach ($path in @($testPath, $auditPath, $builderPath, $pinsPath, $frozenPath)) { if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing runner input: $path" } }

$frozenSha = Get-Sha256 $frozenPath
if ($frozenSha -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953') { throw 'Frozen C11-C manifest mismatch' }
Write-Host 'FROZEN_C11C_MANIFEST=PASS'

$pins = Get-Content -LiteralPath $pinsPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($pins.source_pins.Count -ne 40) { throw ('Expected 40 source pins; found ' + $pins.source_pins.Count) }
foreach ($pin in $pins.source_pins) {
    $relative = ([string]$pin.path).Replace('/', '\')
    if ([System.IO.Path]::IsPathRooted($relative) -or $relative.Contains('..')) { throw "Unsafe source pin path: $relative" }
    $path = Join-Path $ProjectRoot $relative
    if ((Get-Sha256 $path) -ne ([string]$pin.sha256).ToLowerInvariant()) { throw "Source pin mismatch: $relative" }
}
$localPins = @(
    @{ Path = $testPath; Sha = 'ae2b89c51498d8db5a9fafea991e559bbbf7cca54e68b4ec8eb3a936377a6f1f' },
    @{ Path = $auditPath; Sha = 'aff432bd49bdf15e20f43093298a5486aebc633448ac34984263a155fa9034b0' },
    @{ Path = $builderPath; Sha = 'bfbfa0cc108f00b78003e5480c86af1ee5ca63772d24a7792f8cdb6953b6af5d' },
    @{ Path = $pinsPath; Sha = 'f46ea9db3b31bfa820598ddfdda5170f2d0b9b32ed8853f33714d6d7ef89dd3c' }
)
foreach ($local in $localPins) {
    if ((Get-Sha256 $local.Path) -ne $local.Sha) { throw ('Local tool hash mismatch: ' + $local.Path) }
}
Write-Host 'SOURCE_PINS=PASS; COUNT=40; LOCAL_TOOL_PINS=4/4'

$python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    $launcher = Get-Command 'py.exe' -ErrorAction SilentlyContinue
    if ($null -eq $launcher) { throw 'Python 3.13 not found at the standard path and py.exe is unavailable' }
    $resolveOut = Join-Path $env:TEMP ('C11E_PYTHON313_' + [Guid]::NewGuid().ToString('N') + '.txt')
    $resolveErr = Join-Path $env:TEMP ('C11E_PYTHON313_ERR_' + [Guid]::NewGuid().ToString('N') + '.txt')
    $resolveExit = Invoke-Python $launcher.Source @('-3.13', '-c', 'import sys; print(sys.executable)') $ProjectRoot $resolveOut $resolveErr
    if ($resolveExit -ne 0) { throw 'py.exe could not resolve Python 3.13' }
    $python = (Get-Content -LiteralPath $resolveOut -Raw).Trim()
    Remove-Item -LiteralPath $resolveOut, $resolveErr -Force -ErrorAction SilentlyContinue
    if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw 'Resolved Python 3.13 executable does not exist' }
}
$versionOut = Join-Path $env:TEMP ('C11E_PYTHON_VERSION_' + [Guid]::NewGuid().ToString('N') + '.txt')
$versionErr = Join-Path $env:TEMP ('C11E_PYTHON_VERSION_ERR_' + [Guid]::NewGuid().ToString('N') + '.txt')
$versionExit = Invoke-Python $python @('--version') $ProjectRoot $versionOut $versionErr
if ($versionExit -ne 0) { throw 'Python version check failed' }
$pythonVersion = (Get-Content -LiteralPath $versionOut -Raw).Trim()
Remove-Item -LiteralPath $versionOut, $versionErr -Force -ErrorAction SilentlyContinue
if ($pythonVersion -notmatch '^Python 3\.13\.') { throw "Python 3.13 required; observed $pythonVersion" }
Write-Host ('PYTHON_RUNTIME=' + $pythonVersion)

$runId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$outRoot = Join-Path $ProjectRoot ('artifacts\tests\c11e\e4b_loop_family_contract\' + $runId)
New-Item -ItemType Directory -Path $outRoot -Force | Out-Null
$testStdout = Join-Path $outRoot 'python_tests.stdout.log'
$testStderr = Join-Path $outRoot 'python_tests.stderr.log'
$auditStdout = Join-Path $outRoot 'audit.stdout.log'
$auditStderr = Join-Path $outRoot 'audit.stderr.log'
$reportPath = Join-Path $outRoot 'C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT_V1.json'

$oldProject = $env:C11E_PROJECT_ROOT
try {
    $env:C11E_PROJECT_ROOT = $ProjectRoot
    Write-Host 'STAGE=FOCUSED_FAMILY_CONTRACT_TESTS'
    $testExit = Invoke-Python $python @('-m', 'unittest', '-v', 'test_c11e_e4b_loop_family_contract') $toolRoot $testStdout $testStderr
    if ($testExit -ne 0) { throw "Family contract tests failed with exit code $testExit" }
    $testText = (Get-Content -LiteralPath $testStdout -Raw) + (Get-Content -LiteralPath $testStderr -Raw)
    if ($testText -notmatch 'Ran 7 tests' -or $testText -notmatch 'OK') { throw 'Expected seven passing Python test methods were not confirmed in stdout' }
    Write-Host 'FAMILY_CONTRACT_TESTS=7/7_PASS; CANONICAL_SELECTORS=27/27'

    Write-Host 'STAGE=READ_ONLY_SOURCE_AND_POLICY_AUDIT'
    $auditExit = Invoke-Python $python @($auditPath, '--project-root', $ProjectRoot, '--output', $reportPath) $toolRoot $auditStdout $auditStderr
    if ($auditExit -ne 0) { throw "Static audit failed with exit code $auditExit" }
    $report = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($report.status -ne 'PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY' -or $report.source_pin_count -ne 40 -or $report.family_interface_audit.grammar_count -ne 27) { throw 'Static audit report status/schema/count mismatch' }
    if ($report.historical_product_coverage.mp4_present_in_snapshot_count -ne 0) { throw 'Unexpected MP4 visual evidence count; reconcile before acceptance' }
    $reportSha = Get-Sha256 $reportPath
    [System.IO.File]::WriteAllText(($reportPath + '.sha256'), ($reportSha + '  ' + (Split-Path -Leaf $reportPath) + "`n"), [System.Text.Encoding]::ASCII)
} finally {
    $env:C11E_PROJECT_ROOT = $oldProject
}

$receipt = [ordered]@{
    schema = 'C11E-E4B-LOOP-FAMILY-CONTRACT-RUNNER-RECEIPT-V1'
    status = 'PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY'
    run_id = $runId
    project_root = $ProjectRoot
    powershell_version = $PSVersionTable.PSVersion.ToString()
    python_version = $pythonVersion
    frozen_c11c_manifest_sha256 = $frozenSha
    source_pin_count = 40
    local_tool_pins = 4
    focused_test_methods = 7
    tested_canonical_selectors = 27
    report_path = $reportPath
    report_sha256 = $reportSha
    stdout_sha256 = [ordered]@{ tests = (Get-Sha256 $testStdout); audit = (Get-Sha256 $auditStdout) }
    stderr_sha256 = [ordered]@{ tests = (Get-Sha256 $testStderr); audit = (Get-Sha256 $auditStderr) }
    test_exit_code = $testExit
    audit_exit_code = $auditExit
    renderer_native_input_emitted = $false
    launcher_invoked = $false
    godot_invoked = $false
    ffmpeg_invoked = $false
    audio_generated = $false
    media_created = $false
    c11c_source_mutation = $false
    d4_8 = 'BLOCKED'
    d9_10 = 'PREPARE_ONLY'
    release_authority = 'NONE'
}
$receiptPath = Join-Path $outRoot 'C11E_E4B_LOOP_FAMILY_CONTRACT_RUNNER_RECEIPT_V1.json'
$receiptJson = ($receipt | ConvertTo-Json -Depth 12) + "`n"
[System.IO.File]::WriteAllText($receiptPath, $receiptJson, (New-Object System.Text.UTF8Encoding($false)))
$receiptSha = Get-Sha256 $receiptPath
[System.IO.File]::WriteAllText(($receiptPath + '.sha256'), ($receiptSha + '  ' + (Split-Path -Leaf $receiptPath) + "`n"), [System.Text.Encoding]::ASCII)
Write-Host ('REPORT_SHA256=' + $reportSha)
Write-Host ('RECEIPT=' + $receiptPath)
Write-Host 'RENDERER=OFF; LAUNCHERS=NOT_INVOKED; AUDIO=FALSE; MEDIA=FALSE; RELEASE_AUTHORITY=NONE'
Write-Host 'C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT=PASS_OPERATOR_DECISIONS_AND_FAMILY_STATIC_CONTRACT_AUDIT_ONLY'
