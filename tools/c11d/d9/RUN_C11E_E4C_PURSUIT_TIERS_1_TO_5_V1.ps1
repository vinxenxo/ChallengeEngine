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
$styleGuideV28 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V28.md'
$styleShaV28 = Get-Sha256 $styleGuideV28
if ($styleShaV28 -ne '24d9e24ac09a7a8a58445838525a306fc3f3fb8bb31f9dfa5ac7265ed3b71239') {
    throw "STYLE_GUIDE_V28_SHA_MISMATCH: $styleShaV28"
}
$styleGuideV29 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V29.md'
$styleShaV29 = Get-Sha256 $styleGuideV29
if ($styleShaV29 -ne '76d9187f7d8c9b44ed940f18fd242f2205e6caf357c8b7dc19756fa1cf8a0c0a') {
    throw "STYLE_GUIDE_V29_SHA_MISMATCH: $styleShaV29"
}
$styleGuideV30 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V30.md'
$styleShaV30 = Get-Sha256 $styleGuideV30
if ($styleShaV30 -ne '57d653890535849c7a1d55733c29b1f7fe574010a8cdb18b8d2fd86565b50c83') {
    throw "STYLE_GUIDE_V30_SHA_MISMATCH: $styleShaV30"
}
$styleGuideV31 = Join-Path $root 'docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V31.md'
$styleShaV31 = Get-Sha256 $styleGuideV31
if ($styleShaV31 -ne 'e856e3d2385aab67b6fcfb4f6cc05e013b2792e02ae3058e97172a9fd72edbac') {
    throw "STYLE_GUIDE_V31_SHA_MISMATCH: $styleShaV31"
}
$driver = Join-Path $root 'tools\c11d\d9\c11e_e4c_pursuit_tier_batch.py'
if (!(Test-Path -LiteralPath $driver -PathType Leaf)) { throw "PURSUIT_BATCH_DRIVER_MISSING: $driver" }
$driverSha = Get-Sha256 $driver
if ($driverSha -ne '04dec31bc882c9d48ff0a47751a6dfb726b8160374eb552c04158dca9536b6ca') { throw "PURSUIT_BATCH_DRIVER_SHA_MISMATCH: $driverSha" }

$tempRoot = Join-Path $env:TEMP ('C11E_E4C_PURSUIT_BATCH_RUNNER_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot | Out-Null
$stdoutPath = Join-Path $tempRoot 'batch.stdout.log'
$stderrPath = Join-Path $tempRoot 'batch.stderr.log'
$argsList = @($driver,'--project-root',$root,'--python-exe',$python,'--timeout-seconds',[string]$TimeoutSeconds,'--require-v31-guide')
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
Write-Host "STYLE_GUIDE_V28_SHA256=$styleShaV28"
Write-Host "STYLE_GUIDE_V29_SHA256=$styleShaV29"
Write-Host "STYLE_GUIDE_V30_SHA256=$styleShaV30"
Write-Host "STYLE_GUIDE_V31_SHA256=$styleShaV31"
if ($exitCode -ne 0) { throw "E4C_PURSUIT_TIER_BATCH_FAILED: exit=$exitCode; logs=$tempRoot" }
Write-Host 'PURSUIT_BATCH_RUNNER=PASS'
Write-Host 'PURSUIT_T1_RECOVERY=EXISTING_RECEIPT_AND_MEDIA_AUDITED_NO_RERENDER'
Write-Host 'PURSUIT_T2_TO_T5=EXECUTION_SCOPE'
if ($Execute) { Write-Host 'PURSUIT_BATCH_EXECUTION=TIERS_2_TO_5_COMPLETED_T1_REUSED_OPERATOR_REVIEW_PENDING' }
else { Write-Host 'PURSUIT_BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY_T1_RECOVERY_AUDITED' }
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
