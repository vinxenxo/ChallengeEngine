[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe
)
$ErrorActionPreference = 'Stop'
$PSVersionTable.PSVersion.ToString() | Write-Verbose
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'POWERSHELL_5_1_REQUIRED' }
$tokens=$null; $parseErrors=$null
[System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path,[ref]$tokens,[ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw ('POWERSHELL_5_1_AST_PARSE_FAILED:' + ($parseErrors | ForEach-Object { $_.Message } -join ';')) }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/RUNNER'
$ProjectRoot=[System.IO.Path]::GetFullPath($ProjectRoot)
$Runner=Join-Path $ProjectRoot 'tools\c11d\d9\RUN_C11E_E6_L2_DIRECT_RGB24_VISUAL_PROBE_V1.py'
$ExpectedRunnerSha='ca5d0dbfe76314cdb883d4827b1d59d86ae2f0184c8fe7dc78ffd2d9edcbdf35'
function Get-Sha256([string]$Path) {
    $sha=[System.Security.Cryptography.SHA256]::Create()
    try { $stream=[System.IO.File]::OpenRead($Path); try { return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant() } finally { $stream.Dispose() } }
    finally { $sha.Dispose() }
}
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_EXE_MISSING' }
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'L2_DIRECT_RGB24_RUNNER_MISSING' }
$ActualRunnerSha=Get-Sha256 $Runner
if ($ActualRunnerSha -ne $ExpectedRunnerSha) { throw "L2_RUNNER_SOURCE_PIN_MISMATCH:$ActualRunnerSha" }
Write-Host "L2_RUNNER_SOURCE_PIN=PASS/$ActualRunnerSha"
& $PythonExe $Runner --project-root $ProjectRoot --python-exe $PythonExe
$ExitCode=$LASTEXITCODE
if ($ExitCode -ne 0) { throw "L2_DIRECT_RGB24_VISUAL_PROBE_BLOCKED:$ExitCode; preserve the generated receipt and logs" }
Write-Host 'L2_DIRECT_RGB24_VISUAL_PROBE=PASS_TEST_ONLY_PENDING_OPERATOR_VISUAL_REVIEW'
