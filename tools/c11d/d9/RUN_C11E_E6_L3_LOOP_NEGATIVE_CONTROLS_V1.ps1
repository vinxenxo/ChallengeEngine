[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe
)
$ErrorActionPreference='Stop'
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'POWERSHELL_5_1_REQUIRED' }
$tokens=$null; $parseErrors=$null
[System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path,[ref]$tokens,[ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw ('POWERSHELL_5_1_AST_PARSE_FAILED:' + ($parseErrors | ForEach-Object { $_.Message } -join ';')) }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/RUNNER'
$ProjectRoot=[System.IO.Path]::GetFullPath($ProjectRoot)
$PythonExe=[System.IO.Path]::GetFullPath($PythonExe)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw 'PROJECT_ROOT_MISSING' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_EXE_MISSING' }
$runner=Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_l3_loop_negative_controls_v1.py'
$expected='d21442839de01dde8fe1acf94869b2584b327558ed8c1200cf387456613a2e7e'
if (-not (Test-Path -LiteralPath $runner -PathType Leaf)) { throw 'L3_RUNNER_SOURCE_MISSING' }
$actual=(Get-FileHash -LiteralPath $runner -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "L3_RUNNER_SOURCE_PIN_MISMATCH:$actual" }
Write-Host "L3_RUNNER_SOURCE_PIN=PASS/$actual"
& $PythonExe $runner --project-root $ProjectRoot
$exitCode=$LASTEXITCODE
if ($exitCode -ne 0) { throw "L3_LOOP_NEGATIVE_CONTROLS_BLOCKED:$exitCode; preserve logs and do not rerun blindly" }
