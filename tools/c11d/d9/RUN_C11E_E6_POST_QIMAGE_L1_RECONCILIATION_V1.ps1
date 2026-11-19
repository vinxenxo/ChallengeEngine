[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$tokens = $null; $parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$tokens,[ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw ('POWERSHELL_5_1_AST_PARSE=FAIL/RUNNER:' + (($parseErrors | ForEach-Object Message) -join '; ')) }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/RUNNER'
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw "POWERSHELL_VERSION_MISMATCH:$($PSVersionTable.PSVersion)" }
$ProjectRoot = [IO.Path]::GetFullPath($ProjectRoot)
$PythonExe = [IO.Path]::GetFullPath($PythonExe)
if (-not (Test-Path -LiteralPath $ProjectRoot -PathType Container)) { throw 'PROJECT_ROOT_MISSING' }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw 'PYTHON_EXE_MISSING' }
$Audit = Join-Path $ProjectRoot 'tools\c11d\d9\c11e_e6_post_qimage_l1_reconciliation_v1.py'
if (-not (Test-Path -LiteralPath $Audit -PathType Leaf)) { throw 'PHASE_RECONCILIATION_AUDITOR_MISSING' }
$ExpectedAuditSha256 = '2744a3e85e7f40096da789d2f09cb3086e10a538cf86f9935120d9752c3174c8'
$ActualAuditSha256 = (Get-FileHash -LiteralPath $Audit -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualAuditSha256 -ne $ExpectedAuditSha256) { throw "PHASE_RECONCILIATION_AUDITOR_PIN_MISMATCH:$ActualAuditSha256" }
Write-Host ('AUDITOR_SOURCE_PIN=PASS/' + $ActualAuditSha256)
$LogId = [Guid]::NewGuid().ToString('N').Substring(0,12)
$LogRoot = Join-Path ([IO.Path]::GetTempPath()) ('e6r' + $LogId)
if (Test-Path -LiteralPath $LogRoot) { throw 'RUNNER_LOG_ROOT_COLLISION' }
[IO.Directory]::CreateDirectory($LogRoot) | Out-Null
$Stdout = Join-Path $LogRoot 'out.txt'
$Stderr = Join-Path $LogRoot 'err.txt'
$argList = @('-B','-X','utf8',$Audit,'--project-root',$ProjectRoot)
$process = Start-Process -FilePath $PythonExe -ArgumentList $argList -NoNewWindow -Wait -PassThru -RedirectStandardOutput $Stdout -RedirectStandardError $Stderr
[int]$childExit = $process.ExitCode
$outText = if (Test-Path -LiteralPath $Stdout) { Get-Content -LiteralPath $Stdout -Raw } else { '' }
$errText = if (Test-Path -LiteralPath $Stderr) { Get-Content -LiteralPath $Stderr -Raw } else { '' }
if (-not [string]::IsNullOrEmpty($outText)) { Write-Host $outText.TrimEnd() }
if (-not [string]::IsNullOrEmpty($errText)) { Write-Host ('PYTHON_STDERR=' + $errText.TrimEnd()) }
if ($childExit -ne 0) { Write-Host 'NO_PASS_EMITTED=TRUE'; throw "PHASE_RECONCILIATION_BLOCKED:$childExit; preserve the output and stderr under $LogRoot" }
if ($outText -notmatch 'PHASE_RECONCILIATION_STATUS=PASS_READ_ONLY_E6_PHASE_RECONCILIATION_WITH_VISUAL_REVIEW_PENDING') { Write-Host 'NO_PASS_EMITTED=TRUE'; throw 'PHASE_RECONCILIATION_SUCCESS_MARKER_MISSING' }
Write-Host 'PHASE_RECONCILIATION_RUNNER=PASS_READ_ONLY'
