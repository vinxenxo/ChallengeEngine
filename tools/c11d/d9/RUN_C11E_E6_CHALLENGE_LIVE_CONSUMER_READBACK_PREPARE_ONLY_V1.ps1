[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ProjectRoot,
    [Parameter(Mandatory = $true)][string]$PythonExe
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
function ConvertTo-Win32Argument([string]$Value) {
    if ($null -eq $Value) { $Value = '' }
    $builder = New-Object System.Text.StringBuilder
    [void]$builder.Append('"')
    $slashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ([int]$character -eq 92) { $slashes++; continue }
        if ([int]$character -eq 34) {
            if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * (2 * $slashes + 1)) }
            else { [void]$builder.Append([char]92) }
            [void]$builder.Append([char]34); $slashes = 0; continue
        }
        if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * $slashes); $slashes = 0 }
        [void]$builder.Append($character)
    }
    if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * (2 * $slashes)) }
    [void]$builder.Append('"')
    return $builder.ToString()
}
function Invoke-Captured([string]$Label,[string[]]$ArgsList,[string]$WorkDir,[string]$LogRoot) {
    $outPath=Join-Path $LogRoot ($Label+'.stdout.log'); $errPath=Join-Path $LogRoot ($Label+'.stderr.log')
    $quoted=New-Object System.Collections.Generic.List[string]
    foreach($arg in $ArgsList){$quoted.Add((ConvertTo-Win32Argument $arg))}
    $proc=Start-Process -FilePath $PythonExe -ArgumentList ([string]::Join(' ',$quoted.ToArray())) -WorkingDirectory $WorkDir -Wait -PassThru -RedirectStandardOutput $outPath -RedirectStandardError $errPath
    $exit=[int]$proc.ExitCode; $stdout='';$stderr=''
    if(Test-Path -LiteralPath $outPath -PathType Leaf){$stdout=[IO.File]::ReadAllText($outPath,[Text.Encoding]::UTF8)}
    if(Test-Path -LiteralPath $errPath -PathType Leaf){$stderr=[IO.File]::ReadAllText($errPath,[Text.Encoding]::UTF8)}
    Write-Host ('========== '+$Label+' STDOUT ==========');if(-not [string]::IsNullOrWhiteSpace($stdout)){Write-Host $stdout}
    Write-Host ('========== '+$Label+' STDERR ==========');if(-not [string]::IsNullOrWhiteSpace($stderr)){Write-Host $stderr}
    Write-Host ($Label+'_EXIT='+$exit)
    if($exit -ne 0){throw ($Label+'_FAILED:'+ $exit)}
    return ($stdout+"`n"+$stderr)
}
if($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1){throw 'REQUIRES_WINDOWS_POWERSHELL_5_1'}
$t=$null;$e=$null;[void][System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path,[ref]$t,[ref]$e)
if($null -ne $e -and $e.Count -gt 0){throw ('RUNNER_AST_FAILED:'+$e[0].Message)}
if(-not(Test-Path -LiteralPath $ProjectRoot -PathType Container)){throw 'PROJECT_ROOT_NOT_FOUND'}
if(-not(Test-Path -LiteralPath $PythonExe -PathType Leaf)){throw 'PYTHON_EXE_NOT_FOUND'}
$module=Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_challenge_live_consumer_readback_prepare_only_v1.py'
$test=Join-Path $ProjectRoot 'tests\test_c11e_e6_challenge_live_consumer_readback_prepare_only_v1.py'
if(-not(Test-Path -LiteralPath $module -PathType Leaf)){throw 'READBACK_MODULE_NOT_INSTALLED'}
if(-not(Test-Path -LiteralPath $test -PathType Leaf)){throw 'READBACK_TESTS_NOT_INSTALLED'}
$logRoot=Join-Path $env:TEMP ('C11E_E6_CHALLENGE_READBACK_'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory -Path $logRoot|Out-Null
$version=Invoke-Captured 'PYTHON_VERSION' @('--version') $ProjectRoot $logRoot
if($version -notmatch '(?m)^Python 3\.13\.14\s*$'){throw 'PYTHON_VERSION_MISMATCH'}
Write-Host 'PYTHON_VERSION=PASS/3.13.14'
Invoke-Captured 'PY_COMPILE' @('-m','py_compile',$module,$test) $ProjectRoot $logRoot|Out-Null
Write-Host 'PY_COMPILE=PASS/2_FILES'
$testsOut=Invoke-Captured 'UNIT_TESTS' @('-m','unittest','discover','-s','tests','-p','test_c11e_e6_challenge_live_consumer_readback_prepare_only_v1.py','-v') $ProjectRoot $logRoot
if($testsOut -notmatch '(?m)^Ran 38 tests in ' -or $testsOut -notmatch '(?m)^OK\s*$'){throw 'UNIT_TEST_SUMMARY_INVALID_EXPECTED_38_AND_OK'}
Write-Host 'UNIT_TESTS=38/38_PASS'
Invoke-Captured 'CHALLENGE_LIVE_CONSUMER_READBACK_PREPARE_ONLY' @($module,'--project-root',$ProjectRoot) $ProjectRoot $logRoot|Out-Null
Write-Host 'CHALLENGE_LIVE_CONSUMER_READBACK_PREPARE_ONLY=PASS'
Write-Host ('RUNNER_LOG_ROOT='+$logRoot)
