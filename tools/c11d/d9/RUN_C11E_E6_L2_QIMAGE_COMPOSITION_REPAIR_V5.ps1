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
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw 'PROJECT_ROOT_MISSING' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_EXE_MISSING' }
$Runner=Join-Path $ProjectRoot 'tools\c11d\d9\RUN_C11E_E6_L2_QIMAGE_COMPOSITION_REPAIR_V5.py'
if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw 'V5_RUNNER_MISSING' }
$sha=(Get-FileHash -LiteralPath $Runner -Algorithm SHA256).Hash.ToLowerInvariant()
if ($sha -ne '8453c9bfbcf4970cbe019134206b9d394577f8be3fe756a1769785114d6afa3c') { throw "V5_RUNNER_SOURCE_PIN_MISMATCH:$sha" }
Write-Host "V5_RUNNER_SOURCE_PIN=PASS/$sha"
& $PythonExe $Runner --project-root $ProjectRoot --python-exe $PythonExe
$exit=$LASTEXITCODE
if ($exit -ne 0) { throw "V5_QIMAGE_COMPOSITION_BLOCKED:$exit; preserve receipt and logs" }
exit 0
