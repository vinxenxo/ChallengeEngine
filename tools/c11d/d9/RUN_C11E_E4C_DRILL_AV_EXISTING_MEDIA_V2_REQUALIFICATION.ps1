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
function New-DiagnosticBundle {
    param([string]$Reason,[string]$Root,[string]$Evidence,[string]$OutputRoot,[string]$LogRoot,[string]$RunId)
    $capture=Join-Path $env:TEMP ('C11E_E4C_V2_DIAG_'+[guid]::NewGuid().ToString('N'))
    $zipPath=Join-Path $LogRoot ('V2_REQUALIFIER_DIAGNOSTICS_'+$RunId+'.zip')
    New-Item -ItemType Directory -Path $capture -Force|Out-Null
    foreach($folder in @('context','input_evidence','installed_sources','partial_output','runner_logs')){New-Item -ItemType Directory -Path (Join-Path $capture $folder) -Force|Out-Null}
    try {
        $summary=[ordered]@{schema='C11E-E4C-V2-REQUALIFIER-DIAGNOSTIC-CAPTURE-V1';request_id=$RunId;failure_reason=$Reason;project_root=$Root;evidence_root=$Evidence;output_root=$OutputRoot;output_root_exists=(Test-Path -LiteralPath $OutputRoot -PathType Container);source_checkout_mutation=$false;release_authority='NONE'}
        Write-Json (Join-Path $capture 'context\capture_summary.json') $summary
        $inputNames=@('E4C_DRILL_AV_QUALIFICATION_RECEIPT.json','e1_intent.json','request.json','d_composition_plan.json')
        foreach($name in $inputNames){$src=Join-Path $Evidence $name;if(Test-Path -LiteralPath $src -PathType Leaf){Copy-Item -LiteralPath $src -Destination (Join-Path $capture ('input_evidence\'+$name)) -Force}}
        $sourceFiles=@(
            @{Path=$PSCommandPath;Name='RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1'},
            @{Path=$runner;Name='REQUALIFY_C11E_E4C_DRILL_AV_FROM_EXISTING_EVIDENCE_V2.py'},
            @{Path=(Join-Path $Root 'tools\c11d\d9\c11e_e4c_drill_visual_composition_consumer.py');Name='c11e_e4c_drill_visual_composition_consumer.py'},
            @{Path=(Join-Path $Root 'tools\c11d\d9\c11e_e4c_drill_execution.py');Name='c11e_e4c_drill_execution.py'}
        )
        foreach($row in $sourceFiles){if(Test-Path -LiteralPath $row.Path -PathType Leaf){Copy-Item -LiteralPath $row.Path -Destination (Join-Path $capture ('installed_sources\'+$row.Name)) -Force}}
        if(Test-Path -LiteralPath $OutputRoot -PathType Container){
            $partial=Join-Path $capture ('partial_output\'+$RunId);New-Item -ItemType Directory -Path $partial -Force|Out-Null
            Get-ChildItem -LiteralPath $OutputRoot -Force -Recurse|ForEach-Object{
                $rel=$_.FullName.Substring($OutputRoot.TrimEnd('\').Length).TrimStart('\');$dest=Join-Path $partial $rel
                if($_.PSIsContainer){New-Item -ItemType Directory -Path $dest -Force|Out-Null}else{New-Item -ItemType Directory -Path (Split-Path -Parent $dest) -Force|Out-Null;Copy-Item -LiteralPath $_.FullName -Destination $dest -Force}
            }
        }
        if(Test-Path -LiteralPath $LogRoot -PathType Container){Get-ChildItem -LiteralPath $LogRoot -File -Force|Where-Object{$_.FullName -ne $zipPath}|ForEach-Object{Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $capture ('runner_logs\'+$_.Name)) -Force}}
        $inventory=New-Object System.Collections.ArrayList
        foreach($file in (Get-ChildItem -LiteralPath $capture -File -Recurse)){$rel=$file.FullName.Substring($capture.Length).TrimStart('\').Replace('\','/');[void]$inventory.Add([ordered]@{path=$rel;bytes=[long]$file.Length;sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()})}
        Write-Json (Join-Path $capture 'context\file_inventory.json') @($inventory)
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        if(Test-Path -LiteralPath $zipPath){Remove-Item -LiteralPath $zipPath -Force}
        [System.IO.Compression.ZipFile]::CreateFromDirectory($capture,$zipPath,[System.IO.Compression.CompressionLevel]::Optimal,$false)
        $digest=(Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
        Write-Host 'DIAGNOSTIC_CAPTURE=AUTO_PASS';Write-Host "DIAGNOSTIC_ZIP=$zipPath";Write-Host "DIAGNOSTIC_ZIP_SHA256=$digest"
    } finally {if(Test-Path -LiteralPath $capture){Remove-Item -LiteralPath $capture -Recurse -Force -ErrorAction SilentlyContinue}}
}

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
    # Process.WaitForExit(int) takes MILLISECONDS, not seconds.
    $timeoutSeconds=1800
    $timeoutMilliseconds=[int]($timeoutSeconds*1000)
    Write-Host "REQUALIFIER_TIMEOUT_SECONDS=$timeoutSeconds"
    Write-Host "REQUALIFIER_TIMEOUT_MILLISECONDS=$timeoutMilliseconds"
    $progressPath=Join-Path $outputRoot 'V2_REQUALIFICATION_PROGRESS.json'
    $lastProgressKey=''
    $watch=[System.Diagnostics.Stopwatch]::StartNew()
    $timedOut=$false
    while($true){
        $proc.Refresh()
        if($proc.HasExited){break}
        if(Test-Path -LiteralPath $progressPath -PathType Leaf){
            try{
                $progress=Get-Content -LiteralPath $progressPath -Raw -Encoding UTF8|ConvertFrom-Json
                $stage=[string]$progress.stage
                $frameProperty=$progress.PSObject.Properties['frames_completed']
                $frames='';$total=''
                if($frameProperty){$frames=[string]$frameProperty.Value;$total=[string]$progress.total_frames}
                $progressKey=$stage+'|'+$frames+'|'+$total
                if($progressKey -and $progressKey -ne $lastProgressKey){
                    Write-Host "REQUALIFIER_PROGRESS_STAGE=$stage"
                    if($frames){Write-Host "REQUALIFIER_PROGRESS_FRAMES=$frames/$total"}
                    $lastProgressKey=$progressKey
                }
            }catch{Write-Warning ('PROGRESS_READ_RETRY: '+$_.Exception.Message)}
        }
        $remaining=$timeoutMilliseconds-[int]$watch.ElapsedMilliseconds
        if($remaining -le 0){$timedOut=$true;break}
        $waitMilliseconds=[int][Math]::Min(3000,$remaining)
        [void]$proc.WaitForExit($waitMilliseconds)
    }
    if($timedOut){
        $treeKillOutput=''
        $taskkill=Join-Path $env:SystemRoot 'System32\taskkill.exe'
        if(Test-Path -LiteralPath $taskkill -PathType Leaf){$treeKillOutput=(& $taskkill /PID $proc.Id /T /F 2>&1|Out-String)}
        if(!$proc.HasExited){try{$proc.Kill()}catch{}}
        $proc.WaitForExit()
        $stdout=$outTask.GetAwaiter().GetResult();$stderr=$errTask.GetAwaiter().GetResult()
        [IO.File]::WriteAllText((Join-Path $logRoot 'stdout.log'),$stdout);[IO.File]::WriteAllText((Join-Path $logRoot 'stderr.log'),$stderr)
        $lastProgress=$null
        if(Test-Path -LiteralPath $progressPath -PathType Leaf){try{$lastProgress=Get-Content -LiteralPath $progressPath -Raw -Encoding UTF8|ConvertFrom-Json}catch{}}
        $failure=[ordered]@{schema='C11E-E4C-DRILL-V2-REQUALIFICATION-RUNNER-FAILURE-V2';status='FAIL_TIMEOUT';request_id=$runId;command=($python+' '+$argumentLine);timeout_seconds=$timeoutSeconds;timeout_milliseconds=$timeoutMilliseconds;elapsed_milliseconds=[long]$watch.ElapsedMilliseconds;stdout=$stdout;stderr=$stderr;last_progress=$lastProgress;process_tree_kill_output=$treeKillOutput;exit_code=$null;release_authority='NONE'}
        Write-Json (Join-Path $logRoot 'runner_failure.json') $failure
        throw "V2_REQUALIFIER_TIMEOUT; timeout_seconds=$timeoutSeconds; logs=$logRoot"
    }
    $proc.WaitForExit()
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
} catch {
    $reason=$_.Exception.Message
    try {
        if($logRoot -and (Test-Path -LiteralPath $logRoot -PathType Container)){
            if(!(Test-Path -LiteralPath (Join-Path $logRoot 'runner_failure.json') -PathType Leaf)){
                $failure=[ordered]@{schema='C11E-E4C-DRILL-V2-REQUALIFICATION-RUNNER-FAILURE-V2';status='FAIL_CLOSED';request_id=$runId;error=$reason;release_authority='NONE'}
                Write-Json (Join-Path $logRoot 'runner_failure.json') $failure
            }
            New-DiagnosticBundle -Reason $reason -Root $root -Evidence $evidence -OutputRoot $outputRoot -LogRoot $logRoot -RunId $runId
        }
    } catch { Write-Warning ('DIAGNOSTIC_AUTO_BUNDLE_FAILED: '+$_.Exception.Message+'; original_failure='+$reason) }
    throw
} finally {$proc.Dispose()}
