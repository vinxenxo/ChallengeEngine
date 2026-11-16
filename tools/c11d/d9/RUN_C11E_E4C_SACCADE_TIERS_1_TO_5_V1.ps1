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
$styleChecks = @(
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V29.md'; Sha='76d9187f7d8c9b44ed940f18fd242f2205e6caf357c8b7dc19756fa1cf8a0c0a'; Label='V29' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V30.md'; Sha='57d653890535849c7a1d55733c29b1f7fe574010a8cdb18b8d2fd86565b50c83'; Label='V30' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V31.md'; Sha='e856e3d2385aab67b6fcfb4f6cc05e013b2792e02ae3058e97172a9fd72edbac'; Label='V31' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261115_V33.md'; Sha='e37993b32a72144a6894c6e228b756ee4cf1b2892627929bbafbb01766662167'; Label='V33' },
    @{ Relative='docs\current\e\C11E_POWERSHELL_RUNNER_STYLE_GUIDE_20261116_V34.md'; Sha='1cb7880a73b3d429ba15d411228980c16c9168101155a283db21b6f966545d8c'; Label='V34' }
)
foreach ($style in $styleChecks) {
    $path = Join-Path $root $style.Relative
    $sha = Get-Sha256 $path
    if ($sha -ne $style.Sha) { throw "STYLE_GUIDE_$($style.Label)_SHA_MISMATCH: $sha" }
}
$driver = Join-Path $root 'tools\c11d\d9\c11e_e4c_saccade_tier_batch.py'
$driverSha = Get-Sha256 $driver
if ($driverSha -ne '48dacd836141927c73e9d18dea6d95fd936e4104a44c0af1dd93ced0dadb07a4') { throw "SACCADE_BATCH_DRIVER_SHA_MISMATCH: $driverSha" }

$tempRoot = Join-Path $env:TEMP ('C11E_E4C_SACCADE_BATCH_RUNNER_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tempRoot | Out-Null
$stdoutPath = Join-Path $tempRoot 'batch.stdout.log'
$stderrPath = Join-Path $tempRoot 'batch.stderr.log'
$argsList = @($driver,'--project-root',$root,'--python-exe',$python,'--timeout-seconds',[string]$TimeoutSeconds,'--require-v34-guide')
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
foreach ($style in $styleChecks) { Write-Host ("STYLE_GUIDE_{0}_SHA256={1}" -f $style.Label,$style.Sha) }
if ($exitCode -ne 0) { throw "E4C_SACCADE_TIER_BATCH_FAILED: exit=$exitCode; logs=$tempRoot" }
Write-Host 'SACCADE_BATCH_RUNNER=PASS'
Write-Host 'SACCADE_T1_TO_T5=EXECUTION_SCOPE'
if ($Execute) { Write-Host 'SACCADE_BATCH_EXECUTION=TIERS_1_TO_5_COMPLETED_OPERATOR_REVIEW_PENDING' }
else { Write-Host 'SACCADE_BATCH_EXECUTION=NOT_STARTED_PREPARE_ONLY' }
Write-Host 'PRODUCTION_DISPATCH=FALSE'
Write-Host 'RELEASE_AUTHORITY=NONE'
