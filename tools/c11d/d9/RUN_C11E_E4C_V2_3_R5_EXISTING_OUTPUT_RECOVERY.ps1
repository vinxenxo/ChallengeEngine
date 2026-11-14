#requires -Version 5.1
[CmdletBinding()]
param(
    [string]$ProjectRoot = "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS",
    [string]$PythonExe = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$RunId = 'E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9'
$ExpectedRecoverySHA = '79aaf996dfce0c4bf81da595d310dc4c5d7fad8cd16e53ee468deeea5651c750'
$ExpectedReceiptSHA = '57fe829b2ae83fc16a962710b8a1ef8e4635ebf8fd4326714ed24c69c4a0f903'
$ExpectedIntentFileSHA = 'dfc861764302d7a6dec71de4532828dfe146708ed33dd2483b9c611bdd2f9a94'
$ExpectedIntentCanonicalSHA = '9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e'
$ExpectedPlanSHA = '3bbdabdb106461bafb699ae889205c9d53be41fe9e94f58c7254c925e8e628fe'
$ExpectedSilentSHA = 'd674aa7700414c49c5b5ca957c4390da6e0020cea2de9d84750f30c6f14e14a5'
$ExpectedFinals = @{
 'E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9_A_music_840001_A.mp4'='8808b5244c118dc74d9a6fcf9d5e5b49b8ddae33f686794a170fe76cbc971bc1'
 'E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9_B_music_840001_B.mp4'='8808b5244c118dc74d9a6fcf9d5e5b49b8ddae33f686794a170fe76cbc971bc1'
 'E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9_C_changed_music_840002.mp4'='677edb16b0b1fcf47962633624df53ec5c53201080c95d5f563f10b1957c1961'
}
function Get-Sha([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Write-Json([string]$Path,[object]$Value) { $Value | ConvertTo-Json -Depth 40 | Set-Content -LiteralPath $Path -Encoding UTF8 }
function Copy-IfPresent([string]$Source,[string]$Destination) {
 if (!(Test-Path -LiteralPath $Source -PathType Leaf)) { return }
 $parent=Split-Path -Parent $Destination
 if (!(Test-Path -LiteralPath $parent -PathType Container)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
 Copy-Item -LiteralPath $Source -Destination $Destination -Force
}
function New-Diagnostic([string]$Reason,[int]$ExitCode) {
 $snapshot=Join-Path $DiagRoot 'snapshot';$outSnap=Join-Path $snapshot 'output_root';$srcSnap=Join-Path $snapshot 'source_evidence';$codeSnap=Join-Path $snapshot 'installed_sources'
 New-Item -ItemType Directory -Path $outSnap,$srcSnap,$codeSnap -Force | Out-Null
 if (Test-Path -LiteralPath $OutputRoot -PathType Container) {
  Get-ChildItem -LiteralPath $OutputRoot -File -Recurse -Force | ForEach-Object {
   $rel=$_.FullName.Substring($OutputRoot.Length).TrimStart('\');$dst=Join-Path $outSnap $rel;$parent=Split-Path -Parent $dst
   if (!(Test-Path -LiteralPath $parent -PathType Container)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
   Copy-Item -LiteralPath $_.FullName -Destination $dst -Force
  }
 }
 foreach($name in @('E4C_DRILL_AV_QUALIFICATION_RECEIPT.json','e1_intent.json','request.json','d_composition_plan.json')) { Copy-IfPresent (Join-Path $EvidenceRoot $name) (Join-Path $srcSnap $name) }
 Copy-IfPresent $RecoveryPath (Join-Path $codeSnap 'RECOVER_C11E_E4C_V2_EXISTING_OUTPUT_REVIEW_V1.py')
 Copy-IfPresent (Join-Path (Split-Path -Parent $RecoveryPath) 'c11e_e4c_drill_execution.py') (Join-Path $codeSnap 'c11e_e4c_drill_execution.py')
 Copy-IfPresent (Join-Path (Split-Path -Parent $RecoveryPath) 'c11e_e4c_drill_visual_composition_consumer.py') (Join-Path $codeSnap 'c11e_e4c_drill_visual_composition_consumer.py')
 $inventory=@();Get-ChildItem -LiteralPath $DiagRoot -File -Recurse -Force|Where-Object{$_.Name -ne 'diagnostic.json'}|ForEach-Object{$inventory += [pscustomobject]@{path=$_.FullName.Substring($DiagRoot.Length).TrimStart('\').Replace('\','/');bytes=$_.Length;sha256=(Get-Sha $_.FullName)}}
 $frames=@();if(Test-Path -LiteralPath $ReviewDir -PathType Container){$frames=@(Get-ChildItem -LiteralPath $ReviewDir -Filter 'frame_*.png' -File -ErrorAction SilentlyContinue|Select-Object -ExpandProperty Name)}
 $diag=[ordered]@{schema='C11E-E4C-R5-EXISTING-OUTPUT-RECOVERY-DIAGNOSTIC-V1';status='RECOVERY_FAILED_OR_INCOMPLETE';request_id=$RunId;reason=$Reason;python_exit_code=$ExitCode;project_root=$ProjectRoot;evidence_root=$EvidenceRoot;output_root=$OutputRoot;recovery_script=$RecoveryPath;recovery_script_sha256=if(Test-Path -LiteralPath $RecoveryPath -PathType Leaf){Get-Sha $RecoveryPath}else{$null};intent_file_sha256=if(Test-Path -LiteralPath (Join-Path $EvidenceRoot 'e1_intent.json') -PathType Leaf){Get-Sha (Join-Path $EvidenceRoot 'e1_intent.json')}else{$null};expected_intent_file_sha256=$ExpectedIntentFileSHA;expected_intent_canonical_sha256=$ExpectedIntentCanonicalSHA;review_frames=$frames;review_bundle_exists=Test-Path -LiteralPath $BundlePath -PathType Leaf;inventory=$inventory;production_dispatch=$false;release_authority='NONE'}
 Write-Json (Join-Path $DiagRoot 'diagnostic.json') $diag
 $zipPath="$DiagRoot.zip";if(Test-Path -LiteralPath $zipPath){Remove-Item -LiteralPath $zipPath -Force};Add-Type -AssemblyName System.IO.Compression.FileSystem;[IO.Compression.ZipFile]::CreateFromDirectory($DiagRoot,$zipPath,[IO.Compression.CompressionLevel]::Optimal,$false)
 Write-Host "RECOVERY_DIAGNOSTIC_ZIP=$zipPath";Write-Host "RECOVERY_DIAGNOSTIC_SHA256=$(Get-Sha $zipPath)"
}
$ProjectRoot=[IO.Path]::GetFullPath($ProjectRoot);$EvidenceRoot=Join-Path $ProjectRoot 'artifacts\production\c11e\E4C-CLI-SMOKE-20261112T091253Z-5a2e96b8';$OutputRoot=Join-Path $ProjectRoot ('artifacts\production\c11e\'+$RunId);$RecoveryPath=Join-Path $ProjectRoot 'tools\c11d\d9\RECOVER_C11E_E4C_V2_EXISTING_OUTPUT_REVIEW_V1.py';$ReviewDir=Join-Path $OutputRoot 'operator_review';$BundlePath=Join-Path $OutputRoot 'E4C_V2_OPERATOR_REVIEW_BUNDLE.zip';$ReceiptOut=Join-Path $OutputRoot 'E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json'
$DiagBase=Join-Path $ProjectRoot 'artifacts\tests\c11e\e4c_r5_recovery_diagnostics';$Stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ');$DiagRoot=Join-Path $DiagBase ('R5_RECOVERY_'+$Stamp);$stdout=Join-Path $DiagRoot 'recovery_stdout.log';$stderr=Join-Path $DiagRoot 'recovery_stderr.log'
try {
 New-Item -ItemType Directory -Path $DiagBase,$DiagRoot -Force | Out-Null;[IO.File]::WriteAllText($stdout,'',(New-Object Text.UTF8Encoding($false)));[IO.File]::WriteAllText($stderr,'',(New-Object Text.UTF8Encoding($false)))
 if(!(Test-Path -LiteralPath $ProjectRoot -PathType Container) -or !(Test-Path -LiteralPath $PythonExe -PathType Leaf) -or !(Test-Path -LiteralPath $EvidenceRoot -PathType Container) -or !(Test-Path -LiteralPath $OutputRoot -PathType Container) -or !(Test-Path -LiteralPath $RecoveryPath -PathType Leaf)){throw 'PROJECT_PYTHON_EVIDENCE_OUTPUT_OR_RECOVERY_MISSING'}
 if((Get-Sha $RecoveryPath) -ne $ExpectedRecoverySHA){throw 'R5_RECOVERY_SCRIPT_SHA_MISMATCH'}
 $checks=@(
  @{path=(Join-Path $EvidenceRoot 'E4C_DRILL_AV_QUALIFICATION_RECEIPT.json');sha=$ExpectedReceiptSHA;label='SOURCE_RECEIPT'},
  @{path=(Join-Path $EvidenceRoot 'e1_intent.json');sha=$ExpectedIntentFileSHA;label='INTENT_RAW_FILE'},
  @{path=(Join-Path $OutputRoot 'd_composition_plan_v2.json');sha=$ExpectedPlanSHA;label='COMPOSITION_PLAN'},
  @{path=(Join-Path $OutputRoot 'qualification\d_composed_silent_v2.mp4');sha=$ExpectedSilentSHA;label='SILENT_INTERMEDIATE'}
 )
 foreach($row in $checks){if(!(Test-Path -LiteralPath $row.path -PathType Leaf)){throw ($row.label+'_MISSING')};$actual=Get-Sha $row.path;if($actual -ne $row.sha){throw ($row.label+'_SHA_MISMATCH: '+$actual)}}
 foreach($name in $ExpectedFinals.Keys){$p=Join-Path $OutputRoot $name;if(!(Test-Path -LiteralPath $p -PathType Leaf) -or (Get-Sha $p) -ne $ExpectedFinals[$name]){throw "FINAL_MEDIA_MISSING_OR_SHA_MISMATCH: $name"}}
 $intent=Get-Content -LiteralPath (Join-Path $EvidenceRoot 'e1_intent.json') -Raw -Encoding UTF8|ConvertFrom-Json
 if($intent.intent_sha256 -ne $ExpectedIntentCanonicalSHA){throw 'INTENT_CANONICAL_HASH_FIELD_MISMATCH'}
 if(Test-Path -LiteralPath $BundlePath -PathType Leaf){if(!(Test-Path -LiteralPath $ReceiptOut -PathType Leaf)){throw 'BUNDLE_EXISTS_WITHOUT_RECEIPT'};$r=Get-Content -LiteralPath $ReceiptOut -Raw|ConvertFrom-Json;if($r.status -ne 'PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE'){throw 'EXISTING_RECEIPT_NOT_PASS'};Write-Host 'R5_RECOVERY=ALREADY_COMPLETE';Write-Host "REVIEW_BUNDLE=$BundlePath";Write-Host "REVIEW_BUNDLE_SHA256=$(Get-Sha $BundlePath)";exit 0}
 $existing=@();if(Test-Path -LiteralPath $ReviewDir -PathType Container){$existing=@(Get-ChildItem -LiteralPath $ReviewDir -Filter 'frame_*.png' -File -ErrorAction SilentlyContinue)};if($existing.Count -gt 0){throw "PARTIAL_REVIEW_FRAMES_PRESERVED=$($existing.Count); refusing overwrite"}
 Write-Host 'R5_INPUT_HASHES=PASS';Write-Host 'INTENT_RAW_FILE_SHA256=PASS';Write-Host 'INTENT_CANONICAL_SELF_HASH=PASS';Write-Host 'RECOVERY_MODE=VERIFY_EXISTING_OUTPUTS_AND_EXTRACT_REVIEW_ONLY'
 & $PythonExe -u $RecoveryPath --project-root $ProjectRoot --evidence-root $EvidenceRoot --output-id $RunId 1> $stdout 2> $stderr
 $exit=$LASTEXITCODE;Write-Host "RECOVERY_EXIT_CODE=$exit"
 if($exit -eq 0 -and (Test-Path -LiteralPath $BundlePath -PathType Leaf) -and (Test-Path -LiteralPath $ReceiptOut -PathType Leaf)){$r=Get-Content -LiteralPath $ReceiptOut -Raw|ConvertFrom-Json;if($r.status -ne 'PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE'){throw 'TECHNICAL_RECEIPT_STATUS_NOT_PASS'};Write-Host 'RECOVERY_STDOUT_BEGIN';Get-Content -LiteralPath $stdout;Write-Host 'RECOVERY_STDOUT_END';Write-Host 'R5_RECOVERY=PASS';Write-Host "TECHNICAL_RECEIPT=$ReceiptOut";Write-Host "REVIEW_BUNDLE=$BundlePath";Write-Host "REVIEW_BUNDLE_SHA256=$(Get-Sha $BundlePath)";exit 0}
 New-Diagnostic "RECOVERY_EXIT=$exit" $exit;throw 'R5_RECOVERY_FAILED_DIAGNOSTIC_CAPTURED'
} catch { $msg=$_.Exception.Message;if((Test-Path -LiteralPath $DiagRoot -PathType Container) -and !(Test-Path -LiteralPath "$DiagRoot.zip" -PathType Leaf)){try{New-Diagnostic $msg -1}catch{Write-Host "DIAGNOSTIC_PACKAGING_FAILED=$($_.Exception.Message)"}};Write-Host "R5_RECOVERY_ERROR=$msg";exit 2 }
