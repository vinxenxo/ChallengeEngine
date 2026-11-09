[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$ProjectRoot,
 [string]$R1PArchive = "artifacts/tests/c11e/e4b_r1p/E4B_R1P_20261107_032743_5F75045C_RECOVERED.zip"
)
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion -lt [version]'5.1') { throw "Windows PowerShell 5.1 required; found $($PSVersionTable.PSVersion)" }
$root = [IO.Path]::GetFullPath($ProjectRoot)
$expectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
if (-not [string]::Equals($root,$expectedRoot,[StringComparison]::OrdinalIgnoreCase)) { throw "Unexpected active checkout: $root" }
if (-not (Test-Path -LiteralPath $root -PathType Container)) { throw "ProjectRoot does not exist: $root" }
$rootItem = Get-Item -LiteralPath $root -Force
if (($rootItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'ProjectRoot must not be a reparse point' }

function Get-Sha256([string]$Path) {
 if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Pinned file missing: $Path" }
 $item = Get-Item -LiteralPath $Path -Force
 if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "Pinned file must not be a reparse point: $Path" }
 return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-PinnedFile([string]$RelativePath,[string]$ExpectedSha) {
 $p = Join-Path $root ($RelativePath.Replace('/','\'))
 $observed = Get-Sha256 $p
 if ($observed -ne $ExpectedSha) { throw "Installed V1 source pin mismatch: $RelativePath ($observed)" }
 return $p
}
function ConvertTo-WindowsArgument([AllowEmptyString()][string]$Value) {
 if ($null -eq $Value) { $Value = '' }
 if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
 $builder = New-Object System.Text.StringBuilder
 [void]$builder.Append('"')
 $slashes = 0
 for ($i=0; $i -lt $Value.Length; $i++) {
  $ch = $Value[$i]
  if ($ch -eq [char]92) { $slashes++; continue }
  if ($ch -eq [char]34) {
   [void]$builder.Append(('\' * (2*$slashes+1)))
   [void]$builder.Append('"')
   $slashes = 0
   continue
  }
  if ($slashes -gt 0) { [void]$builder.Append(('\' * $slashes)); $slashes = 0 }
  [void]$builder.Append($ch)
 }
 if ($slashes -gt 0) { [void]$builder.Append(('\' * (2*$slashes))) }
 [void]$builder.Append('"')
 return $builder.ToString()
}
function Invoke-CapturedProcess {
 param(
  [Parameter(Mandatory=$true)][string]$FilePath,
  [Parameter(Mandatory=$true)][string[]]$ArgumentList,
  [Parameter(Mandatory=$true)][string]$WorkingDirectory,
  [int]$TimeoutSeconds = 0,
  [int]$HeartbeatSeconds = 0,
  [string]$Stage = 'PROCESS'
 )
 $psi = New-Object System.Diagnostics.ProcessStartInfo
 $psi.FileName = $FilePath
 $psi.Arguments = (($ArgumentList | ForEach-Object { ConvertTo-WindowsArgument ([string]$_) }) -join ' ')
 $psi.WorkingDirectory = $WorkingDirectory
 $psi.UseShellExecute = $false
 $psi.CreateNoWindow = $true
 $psi.RedirectStandardOutput = $true
 $psi.RedirectStandardError = $true
 $proc = New-Object System.Diagnostics.Process
 $proc.StartInfo = $psi
 $watch = [Diagnostics.Stopwatch]::StartNew()
 $lastHeartbeat = 0
 try {
  if (-not $proc.Start()) { throw "Could not start process: $FilePath" }
  # Begin draining both pipes before waiting; this prevents pipe-buffer deadlocks.
  $stdoutTask = $proc.StandardOutput.ReadToEndAsync()
  $stderrTask = $proc.StandardError.ReadToEndAsync()
  $timedOut = $false
  while (-not $proc.WaitForExit(1000)) {
   if ($TimeoutSeconds -gt 0 -and $watch.Elapsed.TotalSeconds -ge $TimeoutSeconds) {
    $timedOut = $true
    try { $proc.Kill() } catch {}
    $proc.WaitForExit()
    break
   }
   if ($HeartbeatSeconds -gt 0 -and ($watch.Elapsed.TotalSeconds - $lastHeartbeat) -ge $HeartbeatSeconds) {
    $lastHeartbeat = [int]$watch.Elapsed.TotalSeconds
    Write-Host ("{0}=RUNNING elapsed_seconds={1}" -f $Stage,$lastHeartbeat)
   }
  }
  $proc.WaitForExit()
  $stdout = $stdoutTask.GetAwaiter().GetResult()
  $stderr = $stderrTask.GetAwaiter().GetResult()
  return [pscustomobject]@{ ExitCode=[int]$proc.ExitCode; TimedOut=[bool]$timedOut; StdOut=[string]$stdout; StdErr=[string]$stderr; DurationSeconds=[math]::Round($watch.Elapsed.TotalSeconds,3) }
 }
 finally { $proc.Dispose() }
}
function Write-NewUtf8File([string]$Path,[string]$Content) {
 $encoding = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)
 $bytes = $encoding.GetBytes($Content)
 $stream = [IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
 try { $stream.Write($bytes,0,$bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
function Write-ProcessLogs([string]$Folder,[string]$Stem,$Result) {
 $outPath = Join-Path $Folder ($Stem + '.stdout.log')
 $errPath = Join-Path $Folder ($Stem + '.stderr.log')
 Write-NewUtf8File $outPath $Result.StdOut
 Write-NewUtf8File $errPath $Result.StdErr
 return [pscustomobject]@{ StdOutPath=$outPath; StdOutSha256=(Get-Sha256 $outPath); StdErrPath=$errPath; StdErrSha256=(Get-Sha256 $errPath) }
}
function Assert-ProcessExit($Result,[string]$Stage) {
 if ($Result.TimedOut) { throw "$Stage timed out; captured streams are preserved in the preflight evidence when the stage has logs." }
 if ($Result.ExitCode -ne 0) { throw "$Stage failed with exit code $($Result.ExitCode). See the captured stdout/stderr evidence." }
}

$runnerRel='tools/c11d/d9/c11e_e4b_loop22_av_qualification_v1.py'
$testsRel='tools/c11d/d9/test_c11e_e4b_loop22_av_qualification_v1.py'
$supportRel='tools/c11d/d9/c11e_e4b_loop22_av_support_v1.py'
$matrixRel='definitions/c11d/production/C11E_E4B_LOOP22_SELECTOR_MATRIX_V1.json'
$policyRel='definitions/c11d/production/C11E_E4B_LOOP22_AV_SCOPE_AMENDMENT_V1.json'
$approvalRel='definitions/c11d/production/C11E_E4B_LOOP22_AV_OPERATOR_APPROVAL_RECORD_20261109_V1.json'
$runner = Assert-PinnedFile $runnerRel '14924325393046d8d7a938f7e1aa6693a29a869a9930e5ad73f55590e202f920'
$tests = Assert-PinnedFile $testsRel '0671f1aafb45a44963fe50884f5a8c091800eabb03cb06bacae3f0891b09250b'
$support = Assert-PinnedFile $supportRel '4f79a33f063dc22e350fc707f82b572ed1007bb14d36b0c6d49b6fd511a0e6e1'
[void](Assert-PinnedFile $matrixRel 'eb0ce2fab5ee97c298e232685ec3452779fc1e1f4a8dcd1c9c994bff1a45a1a1')
[void](Assert-PinnedFile $policyRel 'c0869c23001ed4e04a4fd81e3b1c9a974493c7b1a48cae5351eb55384c988628')
[void](Assert-PinnedFile $approvalRel '00584ca6f4fc3ca7a0269f56a270d7d022b9d360bd91bc983d75c7b0934b5c98')
$frozen = Join-Path $root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
if ((Get-Sha256 $frozen) -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953') { throw 'Frozen C11-C manifest pin mismatch' }
$r1p = if ([IO.Path]::IsPathRooted($R1PArchive)) { [IO.Path]::GetFullPath($R1PArchive) } else { Join-Path $root $R1PArchive }
if ((Get-Sha256 $r1p) -ne 'd49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52') { throw 'R1P recovered archive pin mismatch' }
$installReceiptPath = Join-Path $root 'artifacts\tests\c11e\e4b_loop22_av_install\INSTALL_RECEIPT.json'
if (-not (Test-Path -LiteralPath $installReceiptPath -PathType Leaf)) { throw 'V1 add-only install receipt missing; install V1 before V2 bridge' }
$installReceipt = Get-Content -LiteralPath $installReceiptPath -Raw -Encoding UTF8 | ConvertFrom-Json
$installReceiptItem = Get-Item -LiteralPath $installReceiptPath -Force
if (($installReceiptItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'V1 install receipt must not be a reparse point' }
if ($installReceipt.status -ne 'PASS_ADD_ONLY_INSTALL' -or $installReceipt.package_manifest_sha256 -ne '36d3b37459817cac650e30d4da1c0a560e38e7db9d2f303d0bac3427358753d7' -or [int]$installReceipt.added_file_count -ne 16 -or [int]$installReceipt.source_pins_verified -ne 30) { throw 'V1 add-only install receipt does not match the accepted install' }

$pyLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
if ($null -eq $pyLauncher) { throw 'py.exe launcher not found; Python 3.13 is required' }
$probe = Invoke-CapturedProcess -FilePath $pyLauncher.Source -ArgumentList @('-3.13','-c',"import sys; print('.'.join(map(str,sys.version_info[:3])))") -WorkingDirectory $root -TimeoutSeconds 30 -Stage 'PYTHON_VERSION'
Assert-ProcessExit $probe 'Python launcher'
if ($probe.StdOut.Trim() -notmatch '^3\.13\.') { throw "Python 3.13 required; observed: $($probe.StdOut.Trim())" }
$pythonProbe = Invoke-CapturedProcess -FilePath $pyLauncher.Source -ArgumentList @('-3.13','-c','import sys; print(sys.executable)') -WorkingDirectory $root -TimeoutSeconds 30 -Stage 'PYTHON_PATH'
Assert-ProcessExit $pythonProbe 'Python executable resolution'
$python = $pythonProbe.StdOut.Trim()
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw "Resolved Python executable is missing: $python" }
$env:PATH = (Split-Path -Parent $python) + ';' + $env:PATH
$env:PYTHONDONTWRITEBYTECODE = '1'
$runId = 'PSB2_' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '_' + [Guid]::NewGuid().ToString('N').Substring(0,8)
$evidenceParent = Join-Path $root 'artifacts\tests\c11e\e4b_loop22_av_ps_bridge_v2'
$evidenceDir = Join-Path $evidenceParent $runId
New-Item -ItemType Directory -Path $evidenceDir -Force | Out-Null
Write-Host ("LOOP22_PS_BRIDGE_EVIDENCE_DIR={0}" -f $evidenceDir)

# Regression test: normal child stderr must not become a PowerShell ErrorRecord under Stop.
$temp = Join-Path ([IO.Path]::GetTempPath()) ('C11E_PS_STDIO_BRIDGE_' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temp | Out-Null
try {
 $probeScript = Join-Path $temp 'stdio_probe.py'
 Write-NewUtf8File $probeScript "import sys`nsys.stdout.write('O'*16384 + '\nSTDOUT_MARKER\n')`nsys.stdout.flush()`nsys.stderr.write('E'*16384 + '\nSTDERR_MARKER\n')`nsys.stderr.flush()`nsys.exit(int(sys.argv[1]))`n"
 $okBridge = Invoke-CapturedProcess -FilePath $python -ArgumentList @($probeScript,'0') -WorkingDirectory $temp -TimeoutSeconds 30 -Stage 'STDIO_BRIDGE_ZERO'
 $okBridgeLogs = Write-ProcessLogs $evidenceDir 'BRIDGE_EXIT_0' $okBridge
 if ($okBridge.TimedOut -or $okBridge.ExitCode -ne 0 -or $okBridge.StdOut -notmatch 'STDOUT_MARKER' -or $okBridge.StdErr -notmatch 'STDERR_MARKER' -or $okBridge.StdOut -match 'STDERR_MARKER' -or $okBridge.StdErr -match 'STDOUT_MARKER') { throw 'PowerShell native-process bridge regression test failed for exit code 0' }
 $nonzeroBridge = Invoke-CapturedProcess -FilePath $python -ArgumentList @($probeScript,'23') -WorkingDirectory $temp -TimeoutSeconds 30 -Stage 'STDIO_BRIDGE_NONZERO'
 $nonzeroBridgeLogs = Write-ProcessLogs $evidenceDir 'BRIDGE_EXIT_23' $nonzeroBridge
 if ($nonzeroBridge.TimedOut -or $nonzeroBridge.ExitCode -ne 23 -or $nonzeroBridge.StdOut -notmatch 'STDOUT_MARKER' -or $nonzeroBridge.StdErr -notmatch 'STDERR_MARKER') { throw 'PowerShell native-process bridge regression test failed to preserve non-zero exit code and separate streams' }
 Write-Host 'POWERSHELL_NATIVE_PROCESS_BRIDGE=PASS_STDOUT_STDERR_SEPARATED_EXIT_CODES_PRESERVED'
 $bridgeReceipt = [ordered]@{schema='C11E-E4B-LOOP22-PS-STDIO-BRIDGE-TEST-RECEIPT-V1';status='PASS';exit_codes=@(0,23);stdout_stderr_separated=$true;exit_codes_preserved=$true;exit_0_stdout_sha256=$okBridgeLogs.StdOutSha256;exit_0_stderr_sha256=$okBridgeLogs.StdErrSha256;exit_23_stdout_sha256=$nonzeroBridgeLogs.StdOutSha256;exit_23_stderr_sha256=$nonzeroBridgeLogs.StdErrSha256}
 Write-NewUtf8File (Join-Path $evidenceDir 'BRIDGE_SELF_TEST_RECEIPT.json') ((ConvertTo-Json -InputObject $bridgeReceipt -Depth 6) + "`n")
}
finally { Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue }

# Actual PowerShell parser; no checkout writes and no Git calls.
$tokens=$null; $parseErrors=$null
[System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path,[ref]$tokens,[ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) { throw "V2 wrapper AST parse failed: $($parseErrors -join '; ')" }
Write-Host 'POWERSHELL_AST_PARSE=PASS'
$astCode = "import ast,pathlib,sys; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8'),filename=p) for p in sys.argv[1:]]; print('PYTHON_AST_PARSE=PASS')"
$ast = Invoke-CapturedProcess -FilePath $python -ArgumentList @('-c',$astCode,$runner,$tests,$support) -WorkingDirectory $root -TimeoutSeconds 60 -Stage 'PYTHON_AST'
$astLogs = Write-ProcessLogs $evidenceDir 'PYTHON_AST' $ast
Assert-ProcessExit $ast 'Python AST parse'
if ($ast.StdOut -notmatch 'PYTHON_AST_PARSE=PASS') { throw 'Python AST parse marker missing' }

$archive = $r1p
$testResult = Invoke-CapturedProcess -FilePath $python -ArgumentList @('-u',$tests,'--project-root',$root,'--r1p-recovered-zip',$archive) -WorkingDirectory $root -TimeoutSeconds 1800 -HeartbeatSeconds 30 -Stage 'LOOP22_FOCUSED_TESTS' 
$testLogs = Write-ProcessLogs $evidenceDir 'FOCUSED_TESTS' $testResult
if (-not [string]::IsNullOrWhiteSpace($testResult.StdOut)) { Write-Host $testResult.StdOut.TrimEnd() }
if (-not [string]::IsNullOrWhiteSpace($testResult.StdErr)) { Write-Host $testResult.StdErr.TrimEnd() }
$testCombined = $testResult.StdOut + "`n" + $testResult.StdErr
$testMatch = [regex]::Match($testCombined,'Ran\s+(\d+)\s+tests?')
if ($testResult.ExitCode -ne 0) { throw "Loop22 focused tests failed with exit code $($testResult.ExitCode); inspect $($testLogs.StdErrPath)" }
if (-not $testMatch.Success -or [int]$testMatch.Groups[1].Value -ne 24) { throw 'Loop22 focused test count mismatch; expected exactly 24' }
Write-Host 'LOOP22_FOCUSED_TESTS=PASS_24_OF_24'
$preflightReceipt = [ordered]@{schema='C11E-E4B-LOOP22-PS-PREFLIGHT-RECEIPT-V2';status='PASS_PRELAUNCH';run_id=$runId;bridge_self_test='PASS_STDOUT_STDERR_SEPARATED_EXIT_CODES_0_AND_23';powershell_ast='PASS';python_ast='PASS';focused_tests=24;focused_test_exit_code=$testResult.ExitCode;focused_stdout_sha256=$testLogs.StdOutSha256;focused_stderr_sha256=$testLogs.StdErrSha256;python_ast_stdout_sha256=$astLogs.StdOutSha256;python_ast_stderr_sha256=$astLogs.StdErrSha256}
Write-NewUtf8File (Join-Path $evidenceDir 'PREFLIGHT_RECEIPT.json') ((ConvertTo-Json -InputObject $preflightReceipt -Depth 8) + "`n")
Write-Host 'LOOP22_MEDIA_PRELAUNCH=PASS_ALL_PRELAUNCH_GATES'

# This is the first and only point at which media work can begin.
$runnerResult = Invoke-CapturedProcess -FilePath $python -ArgumentList @('-u',$runner,'--project-root',$root,'--r1p-recovered-zip',$archive) -WorkingDirectory $root -HeartbeatSeconds 60 -Stage 'LOOP22_44_SLOT_QUALIFICATION'
$runnerLogs = Write-ProcessLogs $evidenceDir 'LOOP22_RUNNER' $runnerResult
if ($runnerResult.ExitCode -ne 0) { throw "Loop22 runner failed with exit code $($runnerResult.ExitCode); inspect $($runnerLogs.StdErrPath)" }
$runnerJsonLine = @($runnerResult.StdOut -split "`r?`n" | Where-Object { $_.Trim().StartsWith('{') } | Select-Object -Last 1)
if ($runnerJsonLine.Count -ne 1) { throw 'Loop22 runner did not return one JSON result line' }
$runnerSummary = $runnerJsonLine[0] | ConvertFrom-Json
if ($runnerSummary.status -ne 'PASS_E4B_LOOP22_AV_QUALIFICATION_44_OF_44_PENDING_OPERATOR_VISUAL_AUDIO_REVIEW' -or [int]$runnerSummary.silent_captures -ne 44 -or [int]$runnerSummary.launcher_invocations -ne 44 -or [int]$runnerSummary.av_outputs -ne 44 -or [int]$runnerSummary.ab_pairs_passed -ne 22) { throw 'Loop22 runner exit was zero but its structured 44/44 + 22/22 result did not match the acceptance contract' }
$receipt = [ordered]@{schema='C11E-E4B-LOOP22-PS-NATIVE-PROCESS-BRIDGE-RECEIPT-V2';run_id=$runId;status='PASS_E4B_LOOP22_AV_QUALIFICATION_44_OF_44_PENDING_OPERATOR_VISUAL_AUDIO_REVIEW';wrapper_sha256=(Get-Sha256 $MyInvocation.MyCommand.Path);frozen_c11c_manifest_sha256='e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953';v1_package_manifest_sha256='36d3b37459817cac650e30d4da1c0a560e38e7db9d2f303d0bac3427358753d7';python_version=$probe.StdOut.Trim();focused_tests=[ordered]@{exit_code=$testResult.ExitCode;tests_run=24;stdout_sha256=$testLogs.StdOutSha256;stderr_sha256=$testLogs.StdErrSha256};runner=[ordered]@{exit_code=$runnerResult.ExitCode;silent_captures=$runnerSummary.silent_captures;launcher_invocations=$runnerSummary.launcher_invocations;av_outputs=$runnerSummary.av_outputs;ab_pairs_passed=$runnerSummary.ab_pairs_passed;report_sha256=$runnerSummary.report_sha256;evidence_zip_sha256=$runnerSummary.evidence_zip_sha256;stdout_sha256=$runnerLogs.StdOutSha256;stderr_sha256=$runnerLogs.StdErrSha256};git_checks='SKIPPED';commits='OPERATOR_MANAGED';release_authority='NONE'}
$receiptPath = Join-Path $evidenceDir 'PS_BRIDGE_EXECUTION_RECEIPT.json'
Write-NewUtf8File $receiptPath ((ConvertTo-Json -InputObject $receipt -Depth 12) + "`n")
$receiptSha = Get-Sha256 $receiptPath
Write-NewUtf8File ($receiptPath + '.sha256') ($receiptSha + '  PS_BRIDGE_EXECUTION_RECEIPT.json' + "`n")
Write-Host ("LOOP22_RESULT={0}" -f $runnerSummary.status)
Write-Host ("LOOP22_PS_BRIDGE_RECEIPT={0}" -f $receiptPath)
Write-Host ("LOOP22_PS_BRIDGE_RECEIPT_SHA256={0}" -f $receiptSha)
Write-Host ("LOOP22_REPORT_SHA256={0}" -f $runnerSummary.report_sha256)
Write-Host ("LOOP22_EVIDENCE_ZIP_SHA256={0}" -f $runnerSummary.evidence_zip_sha256)
