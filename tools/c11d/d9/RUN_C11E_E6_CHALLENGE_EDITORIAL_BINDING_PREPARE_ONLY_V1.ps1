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
            [void]$builder.Append([char]34)
            $slashes = 0
            continue
        }
        if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * $slashes); $slashes = 0 }
        [void]$builder.Append($character)
    }
    if ($slashes -gt 0) { [void]$builder.Append(([string][char]92) * (2 * $slashes)) }
    [void]$builder.Append('"')
    return $builder.ToString()
}

function Invoke-CapturedPython([string]$Label, [string[]]$Arguments, [string]$WorkingDirectory, [string]$LogRoot) {
    $outPath = Join-Path $LogRoot ($Label + '.stdout.log')
    $errPath = Join-Path $LogRoot ($Label + '.stderr.log')
    $quoted = New-Object System.Collections.Generic.List[string]
    foreach ($argument in $Arguments) { $quoted.Add((ConvertTo-Win32Argument $argument)) }
    $argumentLine = [string]::Join(' ', $quoted.ToArray())
    $process = Start-Process -FilePath $PythonExe -ArgumentList $argumentLine -WorkingDirectory $WorkingDirectory -Wait -PassThru -RedirectStandardOutput $outPath -RedirectStandardError $errPath
    $childExit = [int]$process.ExitCode
    $stdout = ''
    $stderr = ''
    if (Test-Path -LiteralPath $outPath -PathType Leaf) { $stdout = [IO.File]::ReadAllText($outPath, [Text.Encoding]::UTF8) }
    if (Test-Path -LiteralPath $errPath -PathType Leaf) { $stderr = [IO.File]::ReadAllText($errPath, [Text.Encoding]::UTF8) }
    Write-Host ('========== ' + $Label + ' STDOUT ==========')
    if (-not [string]::IsNullOrWhiteSpace($stdout)) { Write-Host $stdout }
    Write-Host ('========== ' + $Label + ' STDERR ==========')
    if (-not [string]::IsNullOrWhiteSpace($stderr)) { Write-Host $stderr }
    Write-Host ($Label + '_EXIT=' + $childExit)
    if ($childExit -ne 0) { throw ($Label + '_FAILED:' + $childExit) }
}

if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw 'REQUIRES_WINDOWS_POWERSHELL_5_1' }
$parseTokens = $null
$parseErrors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path, [ref]$parseTokens, [ref]$parseErrors)
if ($null -ne $parseErrors -and $parseErrors.Count -gt 0) { throw ('RUNNER_AST_PARSE_FAILED:' + $parseErrors[0].Message) }
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw 'PROJECT_ROOT_NOT_FOUND' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_EXE_NOT_FOUND' }
$modulePath = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_challenge_editorial_binding_prepare_only_v1.py'
$testPath = Join-Path $ProjectRoot 'tests\test_c11e_e6_challenge_editorial_binding_prepare_only_v1.py'
if (-not (Test-Path -LiteralPath $modulePath -PathType Leaf)) { throw 'BINDING_MODULE_NOT_INSTALLED' }
if (-not (Test-Path -LiteralPath $testPath -PathType Leaf)) { throw 'BINDING_TEST_NOT_INSTALLED' }
$logRoot = Join-Path $env:TEMP ('C11E_E6_CHALLENGE_BIND_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $logRoot | Out-Null
Invoke-CapturedPython 'PYTHON_VERSION' @('--version') $ProjectRoot $logRoot
$versionText = [IO.File]::ReadAllText((Join-Path $logRoot 'PYTHON_VERSION.stdout.log'), [Text.Encoding]::UTF8) + [IO.File]::ReadAllText((Join-Path $logRoot 'PYTHON_VERSION.stderr.log'), [Text.Encoding]::UTF8)
if ($versionText -notmatch '(?m)^Python 3\.13\.14\s*$') { throw ('PYTHON_VERSION_MISMATCH:' + $versionText.Trim()) }
Write-Host 'PYTHON_VERSION=PASS/3.13.14'
Invoke-CapturedPython 'PY_COMPILE' @('-m','py_compile',$modulePath,$testPath) $ProjectRoot $logRoot
Invoke-CapturedPython 'UNIT_TESTS' @('-m','unittest','discover','-s','tests','-p','test_c11e_e6_challenge_editorial_binding_prepare_only_v1.py','-v') $ProjectRoot $logRoot
$unitText = [IO.File]::ReadAllText((Join-Path $logRoot 'UNIT_TESTS.stdout.log'), [Text.Encoding]::UTF8) + "`n" + [IO.File]::ReadAllText((Join-Path $logRoot 'UNIT_TESTS.stderr.log'), [Text.Encoding]::UTF8)
if ($unitText -notmatch '(?m)^Ran 24 tests in ' -or $unitText -notmatch '(?m)^OK\s*$') { throw 'UNIT_TEST_SUMMARY_INVALID_EXPECTED_24_AND_OK' }
Write-Host 'UNIT_TESTS=24/24_PASS'
Invoke-CapturedPython 'CHALLENGE_BINDING_PREPARE_ONLY' @($modulePath,'--project-root',$ProjectRoot) $ProjectRoot $logRoot
Write-Host 'CHALLENGE_EDITORIAL_BINDING_PREPARE_ONLY=PASS'
Write-Host ('RUNNER_LOG_ROOT=' + $logRoot)
