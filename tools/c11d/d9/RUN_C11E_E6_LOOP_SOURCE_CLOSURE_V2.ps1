[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ProjectRoot,[Parameter(Mandatory=$true)][string]$PythonExe)
$ErrorActionPreference='Stop'; Set-StrictMode -Version Latest
$tok=$null;$errs=$null;[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$tok,[ref]$errs)|Out-Null
if($errs.Count -gt 0){throw ('POWERSHELL_5_1_AST_PARSE=FAIL/RUNNER:'+ (($errs|% Message)-join '; '))}
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/RUNNER'
if($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1){throw 'POWERSHELL_5_1_REQUIRED'}
$ProjectRoot=[IO.Path]::GetFullPath($ProjectRoot);$PythonExe=[IO.Path]::GetFullPath($PythonExe)
$Auditor=Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_loop_source_closure_v2.py'
if(-not(Test-Path -LiteralPath $Auditor -PathType Leaf)){throw 'LOOP_SOURCE_CLOSURE_V2_AUDITOR_MISSING'}
$ExpectedAuditorSha='9db0c1edb354a4161e9bef077f8b7f6bfc18ed96dc139339d998a625107db034'
$ActualAuditorSha=(Get-FileHash -LiteralPath $Auditor -Algorithm SHA256).Hash.ToLowerInvariant()
if($ActualAuditorSha -ne $ExpectedAuditorSha){throw "AUDITOR_SOURCE_PIN_MISMATCH:$ActualAuditorSha"}
Write-Host "AUDITOR_SOURCE_PIN=PASS/$ActualAuditorSha"
if(-not(Test-Path -LiteralPath $PythonExe -PathType Leaf)){throw 'PYTHON313_MISSING'}
$PyVersion=& $PythonExe --version 2>&1
if($LASTEXITCODE -ne 0 -or ($PyVersion -join ' ') -ne 'Python 3.13.14'){throw "PYTHON_VERSION_MISMATCH:$($PyVersion -join ' ')"}
Write-Host 'PYTHON_VERSION=PASS/3.13.14'
& $PythonExe -B $Auditor --project-root $ProjectRoot
$Exit=$LASTEXITCODE
if($Exit -ne 0){Write-Host 'NO_PASS_EMITTED=TRUE';throw "LOOP_SOURCE_CLOSURE_V2_BLOCKED:$Exit"}
Write-Host 'LOOP_SOURCE_CLOSURE_V2_RUNNER=PASS_READ_ONLY'
