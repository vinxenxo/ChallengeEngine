[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe
)
$ErrorActionPreference = 'Stop'
$ProjectRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
$RunnerPath = $MyInvocation.MyCommand.Path
$PythonAudit = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_render_gate_preflight_v1.py'
$Inputs = Join-Path $ProjectRoot 'definitions\c11e\test_only\C11E_E6_RENDER_GATE_PREFLIGHT_INPUTS_V1.json'
$Tests = Join-Path $ProjectRoot 'tests\test_c11e_e6_render_gate_preflight_v1.py'
$Policy = Join-Path $ProjectRoot 'definitions\c11e\test_only\C11E_E6_SMOKE18_SUCCESSOR_POLICY_DRAFT_V2.json'
foreach ($p in @($PythonExe,$PythonAudit,$Inputs,$Tests,$Policy)) { if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "PREFLIGHT_REQUIRED_FILE_MISSING:$p" } }
$tokens = $null; $errors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile($RunnerPath,[ref]$tokens,[ref]$errors)
if ($errors.Count -gt 0) { throw ('POWERSHELL_5_1_AST_PARSE=FAIL/RUNNER:' + ($errors | Out-String)) }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/RUNNER'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED'

function Invoke-PythonCapture([string]$Exe,[string[]]$Arguments,[string]$Label) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $Exe
    $psi.Arguments = (($Arguments | ForEach-Object { '"' + ($_ -replace '"','\"') + '"' }) -join ' ')
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $proc = New-Object System.Diagnostics.Process
    $proc.StartInfo = $psi
    if (-not $proc.Start()) { throw "$Label`_START_FAILED" }
    $outTask = $proc.StandardOutput.ReadToEndAsync()
    $errTask = $proc.StandardError.ReadToEndAsync()
    $proc.WaitForExit()
    $stdout = $outTask.Result; $stderr = $errTask.Result
    if ($stdout) { Write-Host $stdout.TrimEnd() }
    if ($stderr) { Write-Host $stderr.TrimEnd() }
    if ($proc.ExitCode -ne 0) { throw "$Label`_EXIT:$($proc.ExitCode)" }
}
Invoke-PythonCapture $PythonExe @('--version') 'PYTHON_VERSION'
Invoke-PythonCapture $PythonExe @('-m','unittest','discover','-s','tests','-p','test_c11e_e6_render_gate_preflight_v1.py','-v') 'UNIT_TESTS'
$RunId = 'E6RENDERGATE_' + (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + '_' + ([guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
Invoke-PythonCapture $PythonExe @($PythonAudit,'--project-root',$ProjectRoot,'--inputs',$Inputs,'--run-id',$RunId) 'RENDER_GATE_PREFLIGHT_AUDIT'
Write-Host 'E6_RENDER_GATE_PREFLIGHT_RUNNER_FINAL=PASS_AUDIT_ONLY'
Write-Host 'GODOT_INVOKED=FALSE; FFMPEG_INVOKED=FALSE; FFPROBE_INVOKED=FALSE; MEDIA_CREATED=FALSE'
Write-Host 'D4_8=BLOCKED; E6_TEST_ONLY_AUTHORIZED=FALSE; RENDERER=OFF; RELEASE_AUTHORITY=NONE'
