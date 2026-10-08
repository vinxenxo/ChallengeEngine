[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$D80Inventory = 'artifacts/tests/c11d_d8/d8_0/d8_0_inventory.json',
    [int]$ProbeTimeoutSeconds = 120
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'

if([string]::IsNullOrWhiteSpace($ProjectRoot)){$ProjectRoot=(Get-Location).Path}
$ProjectRoot=(Resolve-Path -LiteralPath $ProjectRoot).Path
if(-not(Test-Path -LiteralPath (Join-Path $ProjectRoot 'tools/c11d/d8') -PathType Container)){throw "ProjectRoot does not look like ChallengeEngineV01_STATELESS: $ProjectRoot"}
$EvidenceRoot=Join-Path $ProjectRoot 'artifacts/tests/c11d_d8/d8_1'
$EvidenceRel='artifacts/tests/c11d_d8/d8_1'
$D80Rel=$D80Inventory.Replace('\','/').TrimStart('./')
$D80Path=Join-Path $ProjectRoot $D80Rel
. (Join-Path $ProjectRoot 'tools/c11d/d8/d8_media_scope.ps1')

function Write-Utf8NoBom([string]$Path,[string]$Text){$enc=New-Object System.Text.UTF8Encoding($false);[IO.File]::WriteAllText($Path,$Text,$enc)}
function CanonicalJson($Value){return ($Value|ConvertTo-Json -Depth 50 -Compress)}
function Sha256([string]$Path){return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Rel([string]$FullPath){$r=(Resolve-Path -LiteralPath $FullPath).Path;if($r.StartsWith($ProjectRoot,[System.StringComparison]::OrdinalIgnoreCase)){return $r.Substring($ProjectRoot.Length).TrimStart('\','/').Replace('\','/')};throw "Path escapes ProjectRoot: $r"}
function IsUnderEvidence([string]$RelativePath){$p=$RelativePath.Replace('\','/').TrimStart('./');return ($p -eq $EvidenceRel -or $p.StartsWith($EvidenceRel+'/'))}
function Snapshot-Files{$items=@();foreach($f in @(Get-ChildItem -LiteralPath $ProjectRoot -File -Recurse -Force)){$r=Rel $f.FullName;if(IsUnderEvidence $r){continue};$isMedia=(Get-D8MediaExtensions)-contains $f.Extension.ToLowerInvariant();$rec=[ordered]@{path=$r;bytes=[int64]$f.Length;last_write_utc_ticks=$f.LastWriteTimeUtc.Ticks;sha256=$null};if(-not$isMedia){$rec.sha256=Sha256 $f.FullName}else{$rec.fingerprint_mode='metadata-only-media'};$items+=$rec};return @($items|Sort-Object path)}
function Compare-Snapshot($Before,$After){$b=@{};foreach($x in @($Before)){$b[$x.path]=$x};$a=@{};foreach($x in @($After)){$a[$x.path]=$x};$added=@();$removed=@();$changed=@();foreach($k in $a.Keys){if(-not$b.ContainsKey($k)){$added+=$a[$k]}elseif($a[$k].bytes-ne$b[$k].bytes-or$a[$k].last_write_utc_ticks-ne$b[$k].last_write_utc_ticks-or$a[$k].sha256-ne$b[$k].sha256){$changed+=[ordered]@{path=$k;before=$b[$k];after=$a[$k]}}};foreach($k in $b.Keys){if(-not$a.ContainsKey($k)){$removed+=$b[$k]}};return [ordered]@{pass=($added.Count-eq0-and$removed.Count-eq0-and$changed.Count-eq0);added=@($added|Sort-Object path);removed=@($removed|Sort-Object path);changed=@($changed|Sort-Object path)}}
function Resolve-FFprobe{$c=Get-Command ffprobe -ErrorAction SilentlyContinue|Select-Object -First 1;if($null-eq$c){return $null};if(-not[string]::IsNullOrWhiteSpace($c.Source)){return $c.Source};return $c.Path}
function Get-JsonProp($Object,[string]$Name){if($null-eq$Object){return $null};$p=$Object.PSObject.Properties[$Name];if($null-eq$p){return $null};return $p.Value}
function Invoke-FFprobeJson([string]$Path,[string]$MediaPath,[int]$TimeoutSeconds){$psi=New-Object System.Diagnostics.ProcessStartInfo;$psi.FileName=$Path;$psi.Arguments='-v error -show_error -show_format -show_streams -show_programs -show_chapters -of json "'+$MediaPath+'"';$psi.UseShellExecute=$false;$psi.CreateNoWindow=$true;$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true;$proc=New-Object System.Diagnostics.Process;$proc.StartInfo=$psi;$start=Get-Date;[void]$proc.Start();$stdout=$proc.StandardOutput.ReadToEnd();$stderr=$proc.StandardError.ReadToEnd();$finished=$proc.WaitForExit($TimeoutSeconds*1000);if(-not$finished){try{$proc.Kill()}catch{};return [ordered]@{status='FAIL';reason='TIMEOUT';exit_code=$null;stdout=$stdout;stderr=$stderr}};$exit=$proc.ExitCode;return [ordered]@{status=if($exit-eq0){'PASS'}else{'FAIL'};reason=if($exit-eq0){$null}else{'FFPROBE_EXIT_NONZERO'};exit_code=$exit;stdout=$stdout;stderr=$stderr}}

if($ProbeTimeoutSeconds-lt5){throw 'ProbeTimeoutSeconds must be at least 5.'}
if(-not(Test-Path -LiteralPath $D80Path -PathType Leaf)){throw "D8.0 inventory not found: $D80Rel"}
$d80=Get-Content -LiteralPath $D80Path -Raw -Encoding UTF8|ConvertFrom-Json
if($null-eq$d80.media){throw 'D8.0 inventory does not contain media section.'}
if(-not(Test-Path -LiteralPath $EvidenceRoot -PathType Container)){New-Item -ItemType Directory -Path $EvidenceRoot -Force|Out-Null}
$before=Snapshot-Files
$scope=Get-D8MediaScopeDeclaration $ProjectRoot
$targets=@(Resolve-D8MediaScope $ProjectRoot)
$ffprobe=Resolve-FFprobe
$env=[ordered]@{contract='C11-D-D8.1-FFPROBE-ENVIRONMENT-V3';available=($null-ne$ffprobe);path=$ffprobe;ffmpeg_invoked=$false;media_mutation=$false;release_authority='NONE';scope_mode=$scope.scope_mode;candidate_count=$targets.Count}
if($null-ne$ffprobe){try{$env.version=@(& $ffprobe -version 2>&1|ForEach-Object{$_.ToString()})}catch{$env.version=@("ERROR: $($_.Exception.Message)")};$env.sha256=Sha256 $ffprobe}
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_1_ffprobe_environment.json') (CanonicalJson $env)
$scopeReceipt=[ordered]@{contract='C11-D-D8.1-MEDIA-SCOPE-RECEIPT-V1';declaration_path='definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json';scope_mode=$scope.scope_mode;candidate_count=$targets.Count;candidates=@($targets|ForEach-Object{[ordered]@{path=$_.path;bytes=$_.bytes;extension=$_.extension}});historical_roots=@($scope.historical_roots);release_authority='NONE'}
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_1_scope_manifest.json') (CanonicalJson $scopeReceipt)
$results=@()
foreach($t in $targets){
    if($null-eq$ffprobe){throw 'D8.1 scope contains media targets but ffprobe is unavailable.'}
    $f=Get-Item -LiteralPath $t.full_path -Force;$beforeBytes=[int64]$f.Length;$beforeTicks=$f.LastWriteTimeUtc.Ticks;$probe=Invoke-FFprobeJson $ffprobe $f.FullName $ProbeTimeoutSeconds;$parsed=$null;$parsePass=$false;$parseError=$null
    if($probe.status-eq'PASS'){try{$parsed=$probe.stdout|ConvertFrom-Json;$parsePass=$true}catch{$parseError=$_.Exception.Message}}
    $post=Get-Item -LiteralPath $f.FullName -Force;$stable=($post.Length-eq$beforeBytes-and$post.LastWriteTimeUtc.Ticks-eq$beforeTicks);$streams=@(Get-JsonProp $parsed 'streams');$structural=($parsePass-and$null-ne(Get-JsonProp $parsed 'format')-and$streams.Count-gt0-and$null-eq(Get-JsonProp $parsed 'error'));$status=if($probe.status-eq'PASS'-and$parsePass-and$structural-and$stable){'PASS'}else{'FAIL'};$reason=$null
    if(-not$stable){$reason='MEDIA_CHANGED_DURING_PROBE'}elseif($probe.status-ne'PASS'){$reason=$probe.reason}elseif(-not$parsePass){$reason='FFPROBE_JSON_PARSE_ERROR'}elseif(-not$structural){$reason='FFPROBE_STRUCTURAL_INTEGRITY_FAILURE'}
    $results+=[ordered]@{path=(Rel $f.FullName);bytes=$beforeBytes;last_write_utc_ticks=$beforeTicks;extension=$f.Extension.ToLowerInvariant();status=$status;reason=$reason;probe_exit_code=$probe.exit_code;stderr=$probe.stderr;stdout=$probe.stdout;parse_error=$parseError}
}
$results=@($results|Sort-Object path)
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_1_probe_results.json') (CanonicalJson $results)
$failed=@($results|Where-Object{$_.status-eq'FAIL'});$status=if($targets.Count-eq0){'PASS_NO_MEDIA'}elseif($failed.Count-eq0){'PASS'}else{'FAIL'};$reasons=@();if($targets.Count-gt0-and$null-eq$ffprobe){$status='BLOCKED';$reasons+='FFPROBE_UNAVAILABLE'}if($failed.Count-gt0){$reasons+='MEDIA_PROBE_FAILURES'}
$report=[ordered]@{contract='C11-D-D8.1-INTEGRITY-REPORT-V3';phase='D8.1';status=$status;d8_0_inventory=[ordered]@{path=$D80Rel;sha256=(Sha256 $D80Path)};scope=[ordered]@{declaration_path='definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json';scope_mode=$scope.scope_mode;candidate_count=$targets.Count};probe_scope='explicit_registry_only';probe_pass_count=@($results|Where-Object{$_.status-eq'PASS'}).Count;probe_fail_count=$failed.Count;workspace_inventory_used_as_operational_gate=$false;release_authority='NONE';production_execution=$false;renderer_execution=$false;ffmpeg_invoked=$false;media_modified_by_runner=$false;reasons=@($reasons)}
Write-Utf8NoBom (Join-Path $EvidenceRoot 'd8_1_integrity_report.json') (CanonicalJson $report)
$after=Snapshot-Files;$mutation=Compare-Snapshot $before $after;$mutationPath=Join-Path $EvidenceRoot 'd8_1_mutation_guard.json';Write-Utf8NoBom $mutationPath (CanonicalJson ([ordered]@{contract='C11-D-D8.1-MUTATION-GUARD-V3';scope='all files outside artifacts/tests/c11d_d8/d8_1/';result=$mutation}))
$final=if($mutation.pass){$status}else{'FAIL'};$receipt=[ordered]@{contract='C11-D-D8.1-VALIDATION-RECEIPT-V3';phase='D8.1';status=$final;next=if($final-in @('PASS','PASS_NO_MEDIA')){'D8.2'}else{'D8.1_REPAIR'};d8_0_inventory_sha256=(Sha256 $D80Path);scope_manifest_sha256=(Sha256 (Join-Path $EvidenceRoot 'd8_1_scope_manifest.json'));probe_results_sha256=(Sha256 (Join-Path $EvidenceRoot 'd8_1_probe_results.json'));integrity_report_sha256=(Sha256 (Join-Path $EvidenceRoot 'd8_1_integrity_report.json'));mutation_guard_pass=$mutation.pass;governance=[ordered]@{d4_8='BLOCKED';runtime_authority='NONE';production_execution=$false;renderer_execution=$false;master_seed='NOT_ADOPTED';cross_domain_seed_sharing='FORBIDDEN';release_authority='NONE'}};$receiptPath=Join-Path $EvidenceRoot 'd8_1_validation_receipt.json';Write-Utf8NoBom $receiptPath (CanonicalJson $receipt)
if(-not$mutation.pass){Write-Host "D8.1 FAIL | evidence=$EvidenceRel | reasons=MUTATION_GUARD";exit 1}
Write-Host "D8.1 $final | evidence=$EvidenceRel | scope_candidates=$($targets.Count)";if($final-in @('PASS','PASS_NO_MEDIA')){exit 0}else{exit 1}
