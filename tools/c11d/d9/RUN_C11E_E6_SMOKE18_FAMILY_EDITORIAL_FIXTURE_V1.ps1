[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [string]$PythonExe = (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe')
)
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1) { throw "WINDOWS_POWERSHELL_5_1_REQUIRED:$($PSVersionTable.PSVersion)" }
$Tokens=$null; $ParseErrors=$null
[System.Management.Automation.Language.Parser]::ParseFile($PSCommandPath,[ref]$Tokens,[ref]$ParseErrors) | Out-Null
if ($ParseErrors.Count -gt 0) { throw 'RUNNER_POWERSHELL_5_1_AST_PARSE_FAILED' }
$Root=[System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $Root -PathType Container)) { throw "PROJECT_ROOT_NOT_FOUND:$Root" }
if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) { throw "PYTHON_EXE_NOT_FOUND:$PythonExe" }
Write-Host 'POWERSHELL_5_1_AST_PARSE=PASS/RUNNER'
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED'
$Version = & $PythonExe -c "import sys; print('.'.join(str(x) for x in sys.version_info[:3]))"
if ($LASTEXITCODE -ne 0 -or (($Version | Out-String).Trim() -ne '3.13.14')) { throw "PYTHON_VERSION_MISMATCH:$Version" }
Write-Host 'PYTHON_VERSION=PASS/3.13.14'
$InstallRoot=Join-Path $Root 'artifacts\tests\c11e\e6_smoke18_family_editorial_fixture_install'
if (-not (Test-Path -LiteralPath $InstallRoot -PathType Container)) { throw 'INSTALL_EVIDENCE_ROOT_MISSING' }
$InstallReceipts=@(Get-ChildItem -LiteralPath $InstallRoot -Filter 'INSTALL_RECEIPT_V1.json' -File -Recurse | Sort-Object LastWriteTimeUtc -Descending)
$ValidInstall=$null;$ValidInstallPath=$null
foreach ($f in $InstallReceipts) {
 try { $x=Get-Content -LiteralPath $f.FullName -Raw | ConvertFrom-Json; if ($x.status -eq 'PASS_ADD_ONLY_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_INSTALL_V1' -and $x.package_id -eq 'C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1_20261118' -and $x.payload_expected -eq 11 -and $x.files.Count -eq 11 -and $x.package_manifest_sha256 -match '^[0-9a-f]{64}$') { $ValidInstall=$x;$ValidInstallPath=$f.FullName;break } } catch { }
}
if ($null -eq $ValidInstall) { throw 'NO_VALID_FAMILY_EDITORIAL_FIXTURE_INSTALL_RECEIPT_FOR_THIS_PACKAGE' }
$ExpectedPaths=@('README_C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.md','definitions/c11e/test_only/C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.json','docs/current/e/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261118_V120.md','docs/current/e/C11E_E6_SMOKE18_FAMILY_EDITORIAL_COVERAGE_20261118_V1.md','docs/master-prompts/C11E_MASTER_HANDOVER_20261118_V14.md','prompts/C11E_CONTINUATION_MASTER_PROMPT_20261118_V184.md','prompts/C11E_FIRST_PROMPT_20261118_E6_FAMILY_EDITORIAL_FIXTURE_V1.md','prompts/C11E_NEXT_WINDOW_START_PROMPT_20261118_V183.md','tests/test_c11e_e6_smoke18_family_editorial_fixture_v1.py','tools/c11d/d9/RUN_C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.ps1','tools/c11d/d9/c11e_e6_smoke18_family_editorial_fixture_audit_v1.py')
$ActualPaths=@($ValidInstall.files | ForEach-Object { [string]$_.path } | Sort-Object)
$ExpectedPaths=@($ExpectedPaths | Sort-Object)
if (($ActualPaths -join '|') -ne ($ExpectedPaths -join '|')) { throw 'INSTALL_RECEIPT_PAYLOAD_PATH_SET_MISMATCH' }
$InstallReceiptSha=(Get-FileHash -LiteralPath $ValidInstallPath -Algorithm SHA256).Hash.ToLowerInvariant()
$InstallSidecar=$ValidInstallPath+'.sha256'
if (-not (Test-Path -LiteralPath $InstallSidecar -PathType Leaf)) { throw 'INSTALL_RECEIPT_SIDECAR_MISSING' }
$InstallSidecarExpected="$InstallReceiptSha  $(Split-Path -Leaf $ValidInstallPath)"
if ((Get-Content -LiteralPath $InstallSidecar -Raw).Trim() -ne $InstallSidecarExpected) { throw 'INSTALL_RECEIPT_SIDECAR_MISMATCH' }
foreach ($f in $ValidInstall.files) {
 $p=Join-Path $Root ($f.path.Replace('/','\'))
 if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "INSTALLED_PAYLOAD_MISSING:$($f.path)" }
 $h=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
 if ($h -ne $f.sha256 -or (Get-Item -LiteralPath $p).Length -ne [int64]$f.bytes) { throw "INSTALLED_PAYLOAD_IDENTITY_MISMATCH:$($f.path)" }
}
Write-Host 'INSTALL_RECEIPT=PASS/11_PAYLOADS/SIDECAR'
Write-Host "INSTALL_RECEIPT_SHA256=$InstallReceiptSha"
$Stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$RunId='E6FAMEDITORIAL_' + $Stamp + '_' + ([guid]::NewGuid().ToString('N').Substring(0,8).ToUpperInvariant())
$OutRoot=Join-Path $Root ('artifacts\tests\c11e\e6_smoke18_family_editorial_fixture\' + $RunId)
New-Item -ItemType Directory -Path $OutRoot | Out-Null
$TestOut=Join-Path $OutRoot 'UNIT_TESTS.stdout.txt'; $TestErr=Join-Path $OutRoot 'UNIT_TESTS.stderr.txt'
function ConvertTo-Win32Argument([string]$Value) {
 if ($null -eq $Value) { $Value='' }
 if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
 $b=New-Object System.Text.StringBuilder;[void]$b.Append('"');$slashes=0
 for ($i=0;$i -lt $Value.Length;$i++) {
  $ch=$Value[$i]
  if ($ch -eq '\') { $slashes++;continue }
  if ($ch -eq '"') { if ($slashes -gt 0) {[void]$b.Append(('\' * (2*$slashes+1)))} else {[void]$b.Append('\')};[void]$b.Append('"');$slashes=0;continue }
  if ($slashes -gt 0) {[void]$b.Append(('\' * $slashes));$slashes=0};[void]$b.Append($ch)
 }
 if ($slashes -gt 0) {[void]$b.Append(('\' * (2*$slashes)))};[void]$b.Append('"');return $b.ToString()
}
function Invoke-Captured([string]$FilePath,[string[]]$Arguments,[string]$WorkingDirectory,[string]$StdoutPath,[string]$StderrPath) {
 $psi=New-Object System.Diagnostics.ProcessStartInfo;$psi.FileName=$FilePath
 $q=@();foreach($a in $Arguments){$q+=(ConvertTo-Win32Argument $a)};$psi.Arguments=[string]::Join(' ',$q)
 $psi.WorkingDirectory=$WorkingDirectory;$psi.UseShellExecute=$false;$psi.CreateNoWindow=$true;$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
 $proc=New-Object System.Diagnostics.Process;$proc.StartInfo=$psi
 if(-not $proc.Start()){throw "PROCESS_START_FAILED:$FilePath"}
 $outTask=$proc.StandardOutput.ReadToEndAsync();$errTask=$proc.StandardError.ReadToEndAsync();$proc.WaitForExit()
 $outText=$outTask.Result;$errText=$errTask.Result;$exit=$proc.ExitCode;$proc.Dispose()
 [IO.File]::WriteAllText($StdoutPath,$outText,(New-Object System.Text.UTF8Encoding($false)))
 [IO.File]::WriteAllText($StderrPath,$errText,(New-Object System.Text.UTF8Encoding($false)))
 return [pscustomobject]@{ExitCode=$exit;Stdout=$outText;Stderr=$errText}
}
$TestArgs=@('-B','-m','unittest','discover','-s','tests','-p','test_c11e_e6_smoke18_family_editorial_fixture_v1.py','-v')
$TestProc=Invoke-Captured -FilePath $PythonExe -Arguments $TestArgs -WorkingDirectory $Root -StdoutPath $TestOut -StderrPath $TestErr
Write-Host "UNIT_TEST_EXIT=$($TestProc.ExitCode)"
if ($TestProc.Stdout) { Write-Host $TestProc.Stdout.TrimEnd() }
if ($TestProc.Stderr) { Write-Host $TestProc.Stderr.TrimEnd() }
if ($TestProc.ExitCode -ne 0) { throw "FAMILY_EDITORIAL_UNIT_TESTS_FAILED:$($TestProc.ExitCode); PRESERVE=$OutRoot" }
$AuditPath=Join-Path $Root 'tools\c11d\d9\c11e_e6_smoke18_family_editorial_fixture_audit_v1.py'
$AuditOut=Join-Path $OutRoot 'AUDIT.stdout.txt'; $AuditErr=Join-Path $OutRoot 'AUDIT.stderr.txt'
$AuditArgs=@('-B',$AuditPath,'--project-root',$Root,'--output-root',$OutRoot)
$AuditProc=Invoke-Captured -FilePath $PythonExe -Arguments $AuditArgs -WorkingDirectory $Root -StdoutPath $AuditOut -StderrPath $AuditErr
if ($AuditProc.Stdout) { Write-Host $AuditProc.Stdout.TrimEnd() }
if ($AuditProc.Stderr) { Write-Host $AuditProc.Stderr.TrimEnd() }
if ($AuditProc.ExitCode -ne 0) { throw "FAMILY_EDITORIAL_AUDIT_FAILED:$($AuditProc.ExitCode); PRESERVE=$OutRoot" }
$ReceiptPath=Join-Path $OutRoot 'E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_AUDIT_RECEIPT_V1.json'
$PlanPath=Join-Path $OutRoot 'E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_PLAN_V1.json'
foreach($p in @($ReceiptPath,$PlanPath)) {
 if (-not (Test-Path -LiteralPath $p -PathType Leaf) -or -not (Test-Path -LiteralPath ($p+'.sha256') -PathType Leaf)) { throw "AUDIT_OUTPUT_OR_SIDECAR_MISSING:$p" }
 $h=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
 $line="$h  $(Split-Path -Leaf $p)"
 if ((Get-Content -LiteralPath ($p+'.sha256') -Raw).Trim() -ne $line) { throw "AUDIT_OUTPUT_SIDECAR_MISMATCH:$p" }
}
$AuditReceipt=Get-Content -LiteralPath $ReceiptPath -Raw | ConvertFrom-Json
if ($AuditReceipt.status -ne 'PASS_PREPARE_ONLY_18_ROWS_30_TARGETS_RUNTIME_CONSUMPTION_NOT_PROVEN' -or $AuditReceipt.top_level_rows -ne 18 -or $AuditReceipt.editorial_targets -ne 30) { throw 'AUDIT_RECEIPT_CONTENT_MISMATCH' }
$Plan=Get-Content -LiteralPath $PlanPath -Raw | ConvertFrom-Json
if ($Plan.status -ne 'PASS_PREPARE_ONLY_18_ROWS_30_TARGETS_RUNTIME_CONSUMPTION_NOT_PROVEN' -or $Plan.top_level_rows_actual -ne 18 -or $Plan.editorial_targets_actual -ne 30) { throw 'AUDIT_PLAN_CONTENT_MISMATCH' }
$FinalReceiptSha=(Get-FileHash -LiteralPath $ReceiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "FAMILY_EDITORIAL_RECEIPT_SHA256=$FinalReceiptSha"
Write-Host 'E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE=PASS_PREPARE_ONLY'
Write-Host 'SMOKE18_ROWS=18/18; EDITORIAL_TARGETS=30/30'
Write-Host 'RUNTIME_EDITORIAL_CONSUMPTION=NOT_PROVEN; LOOP_D_COMPOSITOR=BLOCKED'
Write-Host 'E6_ACCEPTED=0; MATRIX_FROZEN=FALSE; D4_8=BLOCKED; RENDERER=OFF; RELEASE_AUTHORITY=NONE'
Write-Host "EVIDENCE_ROOT=$OutRoot"
Write-Host 'GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED'
Write-Host 'E6_SMOKE18_FAMILY_EDITORIAL_RUNNER_FINAL=PASS'
