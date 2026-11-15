[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe,
    [switch]$Execute,
    [string]$BatchId,
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
$styleGuide = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261114_V23.md'
$styleSha = Get-Sha256 $styleGuide
if ($styleSha -ne '1900b8a06f52156ff18790adb44ef82268c386e2633d2b31237ebc705208c3a5') {
    throw "STYLE_GUIDE_V23_SHA_MISMATCH: $styleSha"
}
$styleGuideV24 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V24.md'
$styleShaV24 = Get-Sha256 $styleGuideV24
if ($styleShaV24 -ne '301ef3b1344e017f405ebf2829950d2a90b77b90a74c59d724083530225c1ec2') {
    throw "STYLE_GUIDE_V24_SHA_MISMATCH: $styleShaV24"
}
$styleGuideV25 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V25.md'
$styleShaV25 = Get-Sha256 $styleGuideV25
if ($styleShaV25 -ne '28be41f57d0a07e2d22bdcffa5b0a019f2e99b9c6ef1bfb3a484c689989ac23c') {
    throw "STYLE_GUIDE_V25_SHA_MISMATCH: $styleShaV25"
}
$styleGuideV26 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V26.md'
$styleShaV26 = Get-Sha256 $styleGuideV26
if ($styleShaV26 -ne '74ffaee6e4b6d1cf5fe070189aa049cc38182617c13e6cc73b0e1e07c7533c1b') {
    throw "STYLE_GUIDE_V26_SHA_MISMATCH: $styleShaV26"
}
$driver = Join-Path $root 'tools\c11d\d9\c11e_e4c_tracking_tier_batch.py'
if (!(Test-Path -LiteralPath $driver -PathType Leaf)) { throw "BATCH_DRIVER_MISSING: $driver" }
$driverSha = Get-Sha256 $driver
if ($driverSha -ne 'a032f759baad9c339ce8c58ff47062694050264d86b1b31d51a699c07de2f946') { throw "BATCH_DRIVER_SHA_MISMATCH: $driverSha" }

$tempRoot = Join-Path $env:TEMP ('C11E_E4C_TRACKING_BATCH_RUNNER_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot | Out-Null
$stdoutPath = Join-Path $tempRoot 'batch.stdout.log'
$stderrPath = Join-Path $tempRoot 'batch.stderr.log'
$argsList = @($driver,'--project-root',$root,'--python-exe',$python,'--timeout-seconds',[string]$TimeoutSeconds,'--require-v26-guide')
if (![string]::IsNullOrWhiteSpace($BatchId)) { $argsList += @('--batch-id',$BatchId) }
if ($Execute) { $argsList += '--execute' }
$argumentLine = ($argsList | ForEach-Object { Quote-Win32Argument ([string]$_) }) -join ' '
$process = Start-Process -FilePath $python -ArgumentList $argumentLine -WorkingDirectory $root -Wait -PassThru -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
$exitCode = [int]$process.ExitCode
$stdout = if (Test-Path -LiteralPath $stdoutPath -PathType Leaf) { Get-Content -LiteralPath $stdoutPath -Raw -Encoding UTF8 } else { '' }
$stderr = if (Test-Path -LiteralPath $stderrPath -PathType Leaf) { Get-Content -LiteralPath $stderrPath -Raw -Encoding UTF8 } else { '' }
if (![string]::IsNullOrWhiteSpace($stdout)) { Write-Host $stdout.TrimEnd() }
if (![string]::IsNullOrWhiteSpace($stderr)) { Write-Host $stderr.TrimEnd() }
Write-Host "PYTHON_BATCH_EXIT_CODE=$exitCode"
Write-Host "WRAPPER_LOG_ROOT=$tempRoot"
Write-Host "STYLE_GUIDE_V23_SHA256=$styleSha"
Write-Host "STYLE_GUIDE_V24_SHA256=$styleShaV24"
Write-Host "STYLE_GUIDE_V25_SHA256=$styleShaV25"
Write-Host "STYLE_GUIDE_V26_SHA256=$styleShaV26"
if ($exitCode -ne 0) { throw "E4C_TRACKING_TIER_BATCH_FAILED: exit=$exitCode; logs=$tempRoot" }
Write-Host 'BATCH_RUNNER=PASS'
if ($Execute) { Write-Host 'BATCH_EXECUTION=COMPLETED_TECHNICAL_RECEIPTS_PENDING_OPERATOR_REVIEW' }
else { Write-Host 'BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY' }
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
