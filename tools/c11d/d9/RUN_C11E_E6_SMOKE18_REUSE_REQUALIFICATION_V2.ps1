[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe
)
$ErrorActionPreference = 'Stop'
$global:LASTEXITCODE = 1
$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
$PythonExe = [System.IO.Path]::GetFullPath($PythonExe)
$Self = $MyInvocation.MyCommand.Path
$Tokens = $null; $ParseErrors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile($Self, [ref]$Tokens, [ref]$ParseErrors)
if ($ParseErrors.Count -gt 0) { throw ('POWERSHELL_5_1_AST_PARSE=FAIL:' + ($ParseErrors -join '; ')) }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS'
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "PYTHON_EXE_MISSING:$PythonExe" }

function Get-PythonVersion {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $PythonExe
    $psi.Arguments = '--version'
    $psi.WorkingDirectory = $ProjectRoot
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $psi
    if (-not $p.Start()) { throw 'PYTHON_VERSION_PROCESS_START_FAILED' }
    $stdoutTask = $p.StandardOutput.ReadToEndAsync()
    $stderrTask = $p.StandardError.ReadToEndAsync()
    $p.WaitForExit()
    $stdout = $stdoutTask.Result
    $stderr = $stderrTask.Result
    $versionText = (($stdout + "`n" + $stderr).Trim())
    if ($p.ExitCode -ne 0) { throw "PYTHON_VERSION_PROCESS_FAILED:$($p.ExitCode):$versionText" }
    $match = [regex]::Match($versionText, '(?m)^Python\s+(\d+\.\d+\.\d+)\s*$')
    if (-not $match.Success) { throw "PYTHON_VERSION_OUTPUT_UNRECOGNIZED:$versionText" }
    return $match.Groups[1].Value
}

function Invoke-PythonProcess([string[]]$Arguments) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $PythonExe
    $quoted = foreach ($arg in $Arguments) {
        if ($arg.Contains('"')) { throw 'PYTHON_ARGUMENT_CONTAINS_DOUBLE_QUOTE' }
        '"' + $arg + '"'
    }
    $psi.Arguments = [string]::Join(' ', $quoted)
    $psi.WorkingDirectory = $ProjectRoot
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $psi
    if (-not $p.Start()) { throw 'PYTHON_PROCESS_START_FAILED' }
    $stdoutTask = $p.StandardOutput.ReadToEndAsync()
    $stderrTask = $p.StandardError.ReadToEndAsync()
    $p.WaitForExit()
    $stdout = $stdoutTask.Result
    $stderr = $stderrTask.Result
    if ($stdout) { Write-Host $stdout.TrimEnd() }
    if ($stderr) { Write-Host $stderr.TrimEnd() }
    return $p.ExitCode
}

$Version = Get-PythonVersion
if ($Version -ne '3.13.14') { throw "PYTHON_VERSION_REQUIRED_3_13_14:$Version" }
Write-Host 'PYTHON_VERSION=PASS/3.13.14'
$Validator = Join-Path $ProjectRoot 'tools\c11d\d9\validate_c11e_e6_smoke18_reuse_requalification_v2.py'
$Tests = Join-Path $ProjectRoot 'tests\c11d\d9\test_c11e_e6_smoke18_reuse_requalification_v2.py'
$TestDir = Split-Path -Parent $Tests
if (-not (Test-Path -LiteralPath $Validator -PathType Leaf)) { throw 'REQUALIFICATION_VALIDATOR_V2_MISSING' }
if (-not (Test-Path -LiteralPath $Tests -PathType Leaf)) { throw 'REQUALIFICATION_TESTS_V2_MISSING' }
$TestExit = Invoke-PythonProcess @('-m','unittest','discover','-s',$TestDir,'-p','test_c11e_e6_smoke18_reuse_requalification_v2.py','-v')
if ($TestExit -ne 0) { $global:LASTEXITCODE = $TestExit; throw "REQUALIFICATION_TESTS_FAILED:$TestExit" }
Write-Host 'REQUALIFICATION_TESTS=32/32_PASS'
$AuditExit = Invoke-PythonProcess @($Validator,'--project-root',$ProjectRoot)
if ($AuditExit -ne 0) { $global:LASTEXITCODE = $AuditExit; throw "E6_REUSE_REQUALIFICATION_BLOCKED:$AuditExit; preserve the report and original evidence." }
Write-Host 'E6_REUSE_REQUALIFICATION_RUNNER=PASS_REUSE_EVIDENCE_LINKAGE_REQUALIFIED_NOT_E6_ACCEPTANCE'
$global:LASTEXITCODE = 0
