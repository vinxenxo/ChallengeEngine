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
$styleGuideV23 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261114_V23.md'
$styleShaV23 = Get-Sha256 $styleGuideV23
if ($styleShaV23 -ne '1900b8a06f52156ff18790adb44ef82268c386e2633d2b31237ebc705208c3a5') {
    throw "STYLE_GUIDE_V23_SHA_MISMATCH: $styleShaV23"
}
$styleGuideV27 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V27.md'
$styleShaV27 = Get-Sha256 $styleGuideV27
if ($styleShaV27 -ne '93b83ec7c5a640235edc3d70e877088896babe9d6d3b1fc3ed224fe0b6b07f43') {
    throw "STYLE_GUIDE_V27_SHA_MISMATCH: $styleShaV27"
}
$driver = Join-Path $root 'tools\c11d\d9\c11e_e4c_tracking_tier_batch.py'
if (!(Test-Path -LiteralPath $driver -PathType Leaf)) { throw "BATCH_DRIVER_MISSING: $driver" }
$driverSha = Get-Sha256 $driver
if ($driverSha -ne 'da1eaee79868ca1591246f5c31925d321bec23f092bde72534bc9879f858a7f1') { throw "BATCH_DRIVER_SHA_MISMATCH: $driverSha" }

$tempRoot = Join-Path $env:TEMP ('C11E_E4C_TRACKING_BATCH_RUNNER_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot | Out-Null
$stdoutPath = Join-Path $tempRoot 'batch.stdout.log'
$stderrPath = Join-Path $tempRoot 'batch.stderr.log'
$argsList = @($driver,'--project-root',$root,'--python-exe',$python,'--timeout-seconds',[string]$TimeoutSeconds,'--require-v27-guide')
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
Write-Host "STYLE_GUIDE_V23_SHA256=$styleShaV23"
Write-Host "STYLE_GUIDE_V27_SHA256=$styleShaV27"
if ($exitCode -ne 0) { throw "E4C_TRACKING_TIER_BATCH_FAILED: exit=$exitCode; logs=$tempRoot" }
Write-Host 'BATCH_RUNNER=PASS'
if ($Execute) { Write-Host 'BATCH_EXECUTION=COMPLETED_TECHNICAL_RECEIPTS_PENDING_OPERATOR_REVIEW' }
else { Write-Host 'BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY' }
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
