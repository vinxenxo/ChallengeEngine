param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe
)
$ErrorActionPreference = 'Stop'
$RunnerPath = $MyInvocation.MyCommand.Path
$Tokens = $null; $ParseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($RunnerPath,[ref]$Tokens,[ref]$ParseErrors) | Out-Null
if ($ParseErrors.Count -gt 0) { throw 'RUNNER_POWERSHELL_AST_PARSE_FAILED' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "PYTHON_EXE_MISSING:$PythonExe" }
$Version = & $PythonExe -c "import sys; print('.'.join(str(x) for x in sys.version_info[:3]))"
if ($LASTEXITCODE -ne 0 -or (($Version | Out-String).Trim() -ne '3.13.14')) { throw "PYTHON_VERSION_MISMATCH:$Version" }
$TestPath = Join-Path $ProjectRoot 'tests\test_c11e_e6_composition_readiness_audit_v1.py'
$AuditPath = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_composition_readiness_audit_v1.py'
foreach ($Required in @($TestPath,$AuditPath)) { if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) { throw "REQUIRED_AUDIT_FILE_MISSING:$Required" } }
$Stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$RunId = 'E6COMPREADINESS_' + $Stamp + '_' + ([guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$OutRoot = Join-Path $ProjectRoot ('artifacts\tests\c11e\e6_composition_readiness\' + $RunId)
New-Item -ItemType Directory -Path $OutRoot | Out-Null
$TestOut = Join-Path $OutRoot 'UNIT_TESTS.stdout.txt'
$TestErr = Join-Path $OutRoot 'UNIT_TESTS.stderr.txt'
$AuditOut = Join-Path $OutRoot 'AUDIT.stdout.txt'
$AuditErr = Join-Path $OutRoot 'AUDIT.stderr.txt'
$TestArgs = @('-B','-m','unittest','discover','-s','tests','-p','test_c11e_e6_composition_readiness_audit_v1.py','-v')
$TestProc = Start-Process -FilePath $PythonExe -ArgumentList $TestArgs -WorkingDirectory $ProjectRoot -NoNewWindow -Wait -PassThru -RedirectStandardOutput $TestOut -RedirectStandardError $TestErr
Write-Host "UNIT_TEST_EXIT=$($TestProc.ExitCode)"
if ($TestProc.ExitCode -ne 0) { throw "COMPOSITION_READINESS_UNIT_TESTS_FAILED:$($TestProc.ExitCode); PRESERVE=$OutRoot" }
$AuditArgs = @('-B',$AuditPath,'--project-root',$ProjectRoot,'--output-root',(Join-Path $OutRoot 'receipt'))
$AuditProc = Start-Process -FilePath $PythonExe -ArgumentList $AuditArgs -WorkingDirectory $ProjectRoot -NoNewWindow -Wait -PassThru -RedirectStandardOutput $AuditOut -RedirectStandardError $AuditErr
Get-Content -LiteralPath $AuditOut
if ($AuditProc.ExitCode -ne 0) { Get-Content -LiteralPath $AuditErr; throw "COMPOSITION_READINESS_AUDIT_BLOCKED:$($AuditProc.ExitCode); PRESERVE=$OutRoot" }
Write-Host "E6_COMPOSITION_READINESS_RUNNER=PASS_AUDIT_ONLY"
Write-Host "RUN_ID=$RunId"
Write-Host "EVIDENCE_ROOT=$OutRoot"
