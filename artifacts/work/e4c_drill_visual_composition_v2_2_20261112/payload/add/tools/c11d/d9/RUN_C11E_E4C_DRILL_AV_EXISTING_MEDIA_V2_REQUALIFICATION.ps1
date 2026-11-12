#requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe,
    [string]$EvidenceRoot
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version 2.0
function Quote-Win32Argument([string]$Value) {
    if ($null -eq $Value) { $Value = '' }
    $b=New-Object System.Text.StringBuilder; [void]$b.Append('"'); $slashes=0
    foreach($ch in $Value.ToCharArray()) {
        if($ch -eq [char]92){$slashes++;continue}
        if($ch -eq [char]34){if($slashes -gt 0){[void]$b.Append(([string][char]92)*(2*$slashes+1))}else{[void]$b.Append([char]92)};[void]$b.Append([char]34);$slashes=0;continue}
        if($slashes -gt 0){[void]$b.Append(([string][char]92)*$slashes);$slashes=0};[void]$b.Append($ch)
    }
    if($slashes -gt 0){[void]$b.Append(([string][char]92)*(2*$slashes))};[void]$b.Append('"');return $b.ToString()
}
function Write-Json([string]$Path,$Value){$Value|ConvertTo-Json -Depth 40|Set-Content -LiteralPath $Path -Encoding UTF8}
$root=[System.IO.Path]::GetFullPath($ProjectRoot)
$python=[System.IO.Path]::GetFullPath($PythonExe)
if(!(Test-Path -LiteralPath $root -PathType Container)){throw "PROJECT_ROOT_MISSING: $root"}
if(!(Test-Path -LiteralPath $python -PathType Leaf)){throw "PYTHON_EXE_MISSING: $python"}
if([string]::IsNullOrWhiteSpace($EvidenceRoot)){$EvidenceRoot=Join-Path $root 'artifacts\production\c11e\E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8'}
$evidence=[System.IO.Path]::GetFullPath($EvidenceRoot)
$runner=Join-Path $root 'tools\c11d\d9\REQUALIFY_C11E_E4C_DRILL_AV_FROM_EXISTING_EVIDENCE_V2.py'
if(!(Test-Path -LiteralPath $runner -PathType Leaf)){throw "V2_REQUALIFIER_MISSING: $runner"}
if(!(Test-Path -LiteralPath (Join-Path $evidence 'E4C_DRILL_AV_QUALIFICATION_RECEIPT.json') -PathType Leaf)){throw "PRESERVED_CLI_EVIDENCE_MISSING: $evidence"}
$runId='E4C-CLI-COMPOSITION-V2-'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ',[Globalization.CultureInfo]::InvariantCulture)+'-'+[guid]::NewGuid().ToString('N').Substring(0,8)
$outputRoot=Join-Path $root ('artifacts\production\c11e\'+$runId)
if(Test-Path -LiteralPath $outputRoot){throw "OUTPUT_COLLISION: $outputRoot"}
$logRoot=Join-Path $root ('artifacts\tests\c11e\e4c_drill_v2_requalification\'+$runId)
New-Item -ItemType Directory -Path $logRoot -Force|Out-Null
$argsList=@('-u',$runner,'--project-root',$root,'--evidence-root',$evidence,'--output-id',$runId)
$quoted=New-Object System.Collections.Generic.List[string]
foreach($arg in $argsList){$quoted.Add((Quote-Win32Argument ([string]$arg)))}
$argumentLine=[string]::Join(' ',$quoted.ToArray())
$psi=New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName=$python;$psi.Arguments=$argumentLine;$psi.WorkingDirectory=$root;$psi.UseShellExecute=$false;$psi.CreateNoWindow=$true
$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true;$psi.RedirectStandardInput=$true
$proc=New-Object System.Diagnostics.Process;$proc.StartInfo=$psi
try{
    if(!$proc.Start()){throw 'V2_REQUALIFIER_START_FAILED'}
    $outTask=$proc.StandardOutput.ReadToEndAsync();$errTask=$proc.StandardError.ReadToEndAsync()
    try{$proc.StandardInput.Close()}catch{}
    if(!$proc.WaitForExit(1800)){try{$proc.Kill()}catch{};$proc.WaitForExit();$stdout=$outTask.GetAwaiter().GetResult();$stderr=$errTask.GetAwaiter().GetResult();
        [IO.File]::WriteAllText((Join-Path $logRoot 'stdout.log'),$stdout);[IO.File]::WriteAllText((Join-Path $logRoot 'stderr.log'),$stderr)
        $failure=[ordered]@{schema='C11E-E4C-DRILL-V2-REQUALIFICATION-RUNNER-FAILURE-V1';status='FAIL_TIMEOUT';request_id=$runId;command=($python+' '+$argumentLine);stdout=$stdout;stderr=$stderr;exit_code=$null;release_authority='NONE'};Write-Json (Join-Path $logRoot 'runner_failure.json') $failure;throw "V2_REQUALIFIER_TIMEOUT; logs=$logRoot"
    }
    $stdout=$outTask.GetAwaiter().GetResult();$stderr=$errTask.GetAwaiter().GetResult()
    [IO.File]::WriteAllText((Join-Path $logRoot 'stdout.log'),$stdout);[IO.File]::WriteAllText((Join-Path $logRoot 'stderr.log'),$stderr)
    $exit=[int]$proc.ExitCode
    if($exit -ne 0){$failure=[ordered]@{schema='C11E-E4C-DRILL-V2-REQUALIFICATION-RUNNER-FAILURE-V1';status='FAIL_CLOSED';request_id=$runId;command=($python+' '+$argumentLine);stdout=$stdout;stderr=$stderr;exit_code=$exit;release_authority='NONE'};Write-Json (Join-Path $logRoot 'runner_failure.json') $failure;throw "V2_REQUALIFIER_EXIT=$exit; logs=$logRoot"}
    $receiptPath=Join-Path $outputRoot 'E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json'
    if(!(Test-Path -LiteralPath $receiptPath -PathType Leaf)){throw 'V2_REQUALIFICATION_RECEIPT_MISSING'}
    $receipt=Get-Content -LiteralPath $receiptPath -Raw -Encoding UTF8|ConvertFrom-Json
    if($receipt.status -ne 'PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE' -or $receipt.request_id -ne $runId){throw 'V2_REQUALIFICATION_RECEIPT_STATUS_OR_ID_FAIL'}
    Write-Host 'V2_REQUALIFICATION=PASS_TECHNICAL_PENDING_OPERATOR_REVIEW'
    Write-Host "REQUEST_ID=$runId";Write-Host "EVIDENCE=$outputRoot";Write-Host "REVIEW_FRAMES=$(Join-Path $outputRoot 'operator_review')"
    Write-Host "RUNNER_LOGS=$logRoot";Write-Host 'NEW_NATIVE_CAPTURE=FALSE';Write-Host 'FAMILY_MUSIC_GENERATION=FALSE'
    Write-Host 'E1=PREPARE_ONLY';Write-Host 'FAMILY_ADAPTER=NOT_CONNECTED_E1';Write-Host 'PRODUCTION_DISPATCH=FALSE';Write-Host 'RELEASE_AUTHORITY=NONE'
} finally {$proc.Dispose()}
